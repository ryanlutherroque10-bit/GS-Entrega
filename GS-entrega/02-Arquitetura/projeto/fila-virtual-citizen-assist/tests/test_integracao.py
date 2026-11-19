"""Testes da comunicação terminal → servidor → painel e da proteção das operações.

O terminal em software (tools/terminal_simulado.py) e o painel usam a mesma API;
o servidor é a única fonte do estado da fila. Aqui o servidor real é iniciado em
uma porta livre e o terminal conversa com ele por HTTP.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
sys.path.insert(0, str(PROJECT / "tools"))
if "FILA_DATA_DIR" not in os.environ:
    _TMP = tempfile.TemporaryDirectory()
    os.environ["FILA_DATA_DIR"] = _TMP.name

import app  # noqa: E402
from terminal_simulado import TerminalFila  # noqa: E402


class IntegracaoTest(unittest.TestCase):
    def setUp(self) -> None:
        app.STATE_FILE.unlink(missing_ok=True)
        self.server = app.create_server("127.0.0.1", 0)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()

    def post(self, path: str, body: dict, headers: dict | None = None) -> tuple[int, dict]:
        req = urllib.request.Request(
            self.base + path,
            data=json.dumps(body).encode(),
            method="POST",
            headers={"Content-Type": "application/json", **(headers or {})},
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            with error:
                return error.code, json.loads(error.read())

    def painel(self) -> dict:
        """O que o painel web recebe ao consultar o servidor."""
        with urllib.request.urlopen(self.base + "/api/state", timeout=5) as response:
            return json.loads(response.read())

    # ------------------------------------------------------- estado compartilhado
    def test_acao_no_terminal_aparece_no_painel(self) -> None:
        terminal = TerminalFila(self.base)
        self.assertEqual(terminal.chegada()[0], 200)
        self.assertEqual(terminal.chegada()[0], 200)
        visto_pelo_painel = self.painel()
        self.assertEqual(visto_pelo_painel["queue_count"], 2)
        self.assertEqual(visto_pelo_painel["events"][0]["source"], "terminal")
        # Uma ação do painel muda o que o terminal lê: a fila é uma só.
        self.post("/api/completions", {"duration_minutes": 6, "source": "painel"})
        self.assertEqual(terminal.estado()["queue_count"], 1)
        self.assertEqual(terminal.estado()["completed_count"], 1)

    def test_terminal_recebe_recusa_com_fila_vazia(self) -> None:
        status, dados = TerminalFila(self.base).conclusao(5)
        self.assertEqual(status, 409)
        self.assertEqual(dados["state"]["queue_count"], 0)

    # ------------------------------------------------------- reenvio sem duplicar
    def test_event_id_repetido_nao_conta_duas_vezes(self) -> None:
        corpo = {"source": "terminal", "event_id": "terminal-abc"}
        status1, primeiro = self.post("/api/arrivals", corpo)
        status2, segundo = self.post("/api/arrivals", corpo)
        self.assertEqual((status1, status2), (200, 200))
        self.assertNotIn("duplicate", primeiro)
        self.assertTrue(segundo["duplicate"])
        self.assertEqual(self.painel()["queue_count"], 1)

    def test_resposta_perdida_e_reenvio_nao_duplicam(self) -> None:
        """A requisição chega ao servidor, mas a resposta se perde; o terminal reenvia."""
        chamadas = {"n": 0}

        def rede_instavel(req, timeout=5):
            chamadas["n"] += 1
            resposta = urllib.request.urlopen(req, timeout=timeout)
            if chamadas["n"] == 1:
                resposta.close()
                raise urllib.error.URLError("resposta perdida (simulado)")
            return resposta

        terminal = TerminalFila(self.base, espera=0, abrir=rede_instavel)
        status, dados = terminal.chegada()
        self.assertEqual(status, 200)
        self.assertEqual(chamadas["n"], 2)
        self.assertTrue(dados["duplicate"])
        self.assertEqual(self.painel()["queue_count"], 1)

    def test_servidor_inacessivel_nao_registra_evento(self) -> None:
        terminal = TerminalFila("http://127.0.0.1:9", espera=0)  # porta sem servidor
        with self.assertRaises(ConnectionError):
            terminal.chegada()
        self.assertEqual(self.painel()["queue_count"], 0)

    # ------------------------------------------------------- proteção das alterações
    def test_reenvio_de_operacao_recusada_continua_recusado(self) -> None:
        # Fila vazia: a conclusão é recusada. Se a resposta se perder e o mesmo evento for
        # reenviado, ele deve ser recusado de novo, e não parecer um sucesso duplicado.
        corpo = {"duration_minutes": 5, "event_id": "evento-recusado"}
        self.assertEqual(self.post("/api/completions", corpo)[0], 409)
        status, dados = self.post("/api/completions", corpo)
        self.assertEqual(status, 409)
        self.assertNotIn("duplicate", dados)
        self.assertEqual(self.painel()["completed_count"], 0)
        # Depois que há alguém na fila, o mesmo evento passa a valer uma única vez.
        self.post("/api/arrivals", {"event_id": "chegada-1"})
        self.assertEqual(self.post("/api/completions", corpo)[0], 200)
        self.assertTrue(self.post("/api/completions", corpo)[1].get("duplicate"))
        self.assertEqual(self.painel()["completed_count"], 1)

    def test_content_length_invalido_recebe_400(self) -> None:
        import http.client
        porta = self.server.server_address[1]
        for valor in ("abc", "-5"):
            conexao = http.client.HTTPConnection("127.0.0.1", porta, timeout=5)
            conexao.putrequest("POST", "/api/arrivals")
            conexao.putheader("Content-Type", "application/json")
            conexao.putheader("Content-Length", valor)
            conexao.endheaders()
            resposta = conexao.getresponse()
            self.assertEqual(resposta.status, 400, valor)
            self.assertIn("Content-Length", json.loads(resposta.read())["error"])
            conexao.close()
        self.assertEqual(self.painel()["queue_count"], 0)

    def test_codigo_do_operador_com_acento_nao_derruba_a_requisicao(self) -> None:
        with mock.patch.object(app, "TOKEN", "ação-123"):
            self.assertEqual(self.post("/api/arrivals", {})[0], 401)
            bruto = "ação-123".encode("utf-8").decode("latin-1")  # como um cliente UTF-8 envia
            self.assertEqual(self.post("/api/arrivals", {}, {"X-Fila-Token": bruto})[0], 200)
        self.assertEqual(self.painel()["queue_count"], 1)

    def test_codigo_do_operador_protege_alteracoes(self) -> None:
        with mock.patch.object(app, "TOKEN", "segredo-da-demo"):
            self.assertTrue(self.painel()["write_protected"])  # consulta continua pública
            self.assertEqual(self.post("/api/arrivals", {})[0], 401)
            self.assertEqual(self.post("/api/arrivals", {}, {"X-Fila-Token": "errado"})[0], 401)
            self.assertEqual(self.post("/api/reset", {})[0], 401)
            self.assertEqual(self.painel()["queue_count"], 0)
            self.assertEqual(self.post("/api/arrivals", {}, {"X-Fila-Token": "segredo-da-demo"})[0], 200)
            self.assertEqual(TerminalFila(self.base, token="segredo-da-demo").chegada()[0], 200)
            self.assertEqual(self.painel()["queue_count"], 2)

    def test_reinicio_mantem_protecao_contra_reenvio(self) -> None:
        self.post("/api/arrivals", {"event_id": "x1"})
        self.post("/api/reset", {})
        self.assertTrue(self.post("/api/arrivals", {"event_id": "x1"})[1]["duplicate"])
        self.assertEqual(self.painel()["queue_count"], 0)


if __name__ == "__main__":
    unittest.main()
