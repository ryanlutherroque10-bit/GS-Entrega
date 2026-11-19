"""Terminal de atendimento em software, ligado ao servidor por HTTP + JSON.

Representa o terminal de entrada da arquitetura (os dois botões) em um computador
qualquer: cada tecla vira um evento enviado ao servidor, que é a fonte oficial da
fila. O painel web consulta o mesmo servidor, então uma ação feita aqui aparece
no painel em até 3 segundos.

Uso:
    python tools/terminal_simulado.py                       # servidor local
    python tools/terminal_simulado.py https://exemplo.com   # servidor na internet
    FILA_TOKEN=codigo python tools/terminal_simulado.py     # servidor protegido

Teclas: c = chegada | s <minutos> = concluir atendimento | e = estado | q = sair

Falhas de rede: cada evento recebe um identificador único (event_id). Se o envio
falhar, o terminal tenta de novo com o MESMO identificador; o servidor descarta
repetições, então um evento nunca é contado duas vezes. Se todas as tentativas
falharem, o evento não é aplicado e o operador é avisado.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

TENTATIVAS = 3
ESPERA_ENTRE_TENTATIVAS_S = 1.0


class TerminalFila:
    def __init__(
        self,
        base_url: str,
        token: str = "",
        origem: str = "terminal",
        espera: float = ESPERA_ENTRE_TENTATIVAS_S,
        abrir=urllib.request.urlopen,
    ):
        self.base = base_url.rstrip("/")
        self.token = token
        self.origem = origem
        self.espera = espera
        self.abrir = abrir  # substituível nos testes para simular falha de rede

    def _requisicao(self, metodo: str, caminho: str, corpo: dict | None = None) -> tuple[int, dict]:
        dados = json.dumps(corpo).encode("utf-8") if corpo is not None else None
        cabecalhos = {"Content-Type": "application/json"}
        if self.token:
            cabecalhos["X-Fila-Token"] = self.token
        req = urllib.request.Request(self.base + caminho, data=dados, method=metodo, headers=cabecalhos)
        try:
            with self.abrir(req, timeout=5) as resposta:
                return resposta.status, json.loads(resposta.read())
        except urllib.error.HTTPError as erro:  # resposta do servidor com erro (409, 400, 401…)
            with erro:
                return erro.code, json.loads(erro.read())

    def _enviar_evento(self, caminho: str, corpo: dict) -> tuple[int, dict]:
        """Envia um evento com identificador único e repete em caso de falha de rede."""
        corpo = {"source": self.origem, "event_id": f"{self.origem}-{uuid.uuid4().hex}", **corpo}
        ultimo_erro: Exception | None = None
        for tentativa in range(1, TENTATIVAS + 1):
            try:
                return self._requisicao("POST", caminho, corpo)
            except (urllib.error.URLError, OSError, TimeoutError) as erro:
                ultimo_erro = erro
                if tentativa < TENTATIVAS:
                    time.sleep(self.espera)
        raise ConnectionError(f"servidor inacessível após {TENTATIVAS} tentativas ({ultimo_erro})")

    def chegada(self) -> tuple[int, dict]:
        return self._enviar_evento("/api/arrivals", {})

    def conclusao(self, minutos: float) -> tuple[int, dict]:
        return self._enviar_evento("/api/completions", {"duration_minutes": minutos})

    def estado(self) -> dict:
        return self._requisicao("GET", "/api/state")[1]


def mostrar(estado: dict) -> None:
    """Equivale ao display do terminal: mostra o estado oficial devolvido pelo servidor."""
    print(
        f"  Fila: {estado['queue_count']} | Concluídos: {estado['completed_count']} | "
        f"Conv: {estado['conventional_wait_minutes']} min | IA: {estado['ai_wait_minutes']} min"
    )


def main() -> None:
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    terminal = TerminalFila(base, os.environ.get("FILA_TOKEN", ""))
    print(f"Terminal ligado a {base}")
    print("Teclas: c = chegada | s <minutos> = concluir | e = estado | q = sair")
    try:
        mostrar(terminal.estado())
    except (urllib.error.URLError, OSError) as erro:
        print(f"  ! Servidor inacessível: {erro}")
    while True:
        try:
            partes = input("> ").strip().lower().split()
        except EOFError:
            return
        if not partes:
            continue
        try:
            if partes[0] == "q":
                return
            if partes[0] == "e":
                mostrar(terminal.estado())
                continue
            if partes[0] == "c":
                status, dados = terminal.chegada()
            elif partes[0] == "s":
                minutos = float(partes[1].replace(",", ".")) if len(partes) > 1 else 7.0
                status, dados = terminal.conclusao(minutos)
            else:
                print("  ! Tecla desconhecida. Use c, s <minutos>, e ou q.")
                continue
        except ValueError:
            print("  ! Informe os minutos como número, por exemplo: s 7.5")
            continue
        except (ConnectionError, urllib.error.URLError, OSError) as erro:
            print(f"  ! Evento NÃO registrado: {erro}")
            continue
        if status == 200:
            print("  OK (evento registrado no servidor)")
            mostrar(dados)
        else:
            print(f"  ! Recusado pelo servidor (HTTP {status}): {dados.get('error', '')}")
            if "state" in dados:
                mostrar(dados["state"])


if __name__ == "__main__":
    main()
