"""Testes da carga do CSV com defeito e do menu interativo completo."""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import main
from main import ListaServicos

CABECALHO = "id;categoria;titulo;descricao;requisitos;local\n"
LINHA_OK = "1;Direitos;Tarifa Social;Descrição;Requisito;Canal oficial\n"


class TestCargaCsvInvalido(unittest.TestCase):
    """Linhas defeituosas devem gerar erro claro, com o número da linha."""

    def carregar(self, conteudo):
        with tempfile.TemporaryDirectory() as temp:
            caminho = Path(temp) / "servicos.csv"
            caminho.write_text(conteudo, encoding="utf-8")
            return ListaServicos.carregar_csv(caminho)

    def test_linha_incompleta_gera_erro_com_numero_da_linha(self):
        with self.assertRaisesRegex(ValueError, "linha 3.*faltam os campos: titulo"):
            self.carregar(CABECALHO + LINHA_OK + "2;Categoria\n")

    def test_coluna_excedente(self):
        with self.assertRaisesRegex(ValueError, "linha 2.*mais colunas"):
            self.carregar(CABECALHO + LINHA_OK.strip() + ";extra\n")

    def test_campo_vazio_e_id_invalido(self):
        with self.assertRaisesRegex(ValueError, "linha 2.*campos vazios: titulo"):
            self.carregar(CABECALHO + "1;Direitos; ;Descrição;Requisito;Canal\n")
        for id_ruim in ("abc", "0", "-4", "1.5"):
            with self.assertRaisesRegex(ValueError, "linha 2.*inteiro positivo"):
                self.carregar(CABECALHO + LINHA_OK.replace("1;", id_ruim + ";", 1))

    def test_id_duplicado_e_cabecalho_errado(self):
        with self.assertRaisesRegex(ValueError, "linha 3.*já está cadastrado"):
            self.carregar(CABECALHO + LINHA_OK + LINHA_OK)
        with self.assertRaisesRegex(ValueError, "Cabeçalho inválido"):
            self.carregar("id;titulo\n1;x\n")

    def test_arquivo_inexistente_ou_so_cabecalho_resulta_em_lista_vazia(self):
        self.assertEqual(len(ListaServicos.carregar_csv(Path("nao_existe_12345.csv"))), 0)
        self.assertEqual(len(self.carregar(CABECALHO)), 0)

    def test_arquivo_vazio_resulta_em_lista_vazia(self):
        self.assertEqual(len(self.carregar("")), 0)
        self.assertEqual(len(self.carregar("  \n\n")), 0)


class TestMenu(unittest.TestCase):
    """Executa o menu real com entradas simuladas sobre um CSV temporário."""

    def rodar(self, conteudo_csv, entradas):
        with tempfile.TemporaryDirectory() as temp:
            caminho = Path(temp) / "servicos.csv"
            if conteudo_csv is not None:
                caminho.write_text(conteudo_csv, encoding="utf-8")
            saida = io.StringIO()
            entrada = mock.Mock(side_effect=entradas)
            with (
                mock.patch.object(main, "ARQUIVO_DADOS", caminho),
                mock.patch.object(ListaServicos.carregar_csv.__func__, "__defaults__", (caminho,)),
                mock.patch.object(ListaServicos.salvar_csv, "__defaults__", (caminho,)),
                mock.patch.object(main.ler_inteiro, "__defaults__", (entrada,)),
                mock.patch.object(main.ler_texto, "__defaults__", (entrada,)),
                mock.patch("builtins.input", entrada),
                contextlib.redirect_stdout(saida),
            ):
                main.executar()
            final = caminho.read_text(encoding="utf-8") if caminho.exists() else None
            return saida.getvalue(), final

    def test_csv_danificado_nao_e_sobrescrito(self):
        danificado = CABECALHO + LINHA_OK + "2;Categoria\n"
        # Nenhuma entrada é fornecida: o programa deve encerrar antes do menu.
        saida, final = self.rodar(danificado, [])
        self.assertIn("Não foi possível carregar", saida)
        self.assertIn("linha 3", saida)
        self.assertIn("não foi alterado", saida)
        self.assertEqual(final, danificado)

    def test_crud_completo_pelo_menu(self):
        entradas = [
            "1",
            "2",
            "Energia",
            "Consumo consciente",
            "Dicas",
            "Comparar aparelhos",
            "Orientação",  # cadastra
            "1",
            "2",
            "X",
            "X",
            "X",
            "X",
            "X",  # ID duplicado
            "2",
            "2",  # consulta
            "3",
            "energia",  # pesquisa
            "3",
            "zzz",  # pesquisa sem resultado
            "4",
            "2",
            "Energia",
            "Uso consciente",
            "Dicas",
            "Comparar aparelhos",
            "Orientação",  # atualiza
            "7",  # ordena
            "8",  # análise
            "5",
            "1",  # exclui
            "5",
            "99",  # exclui inexistente
            "2",
            "abc",  # ID inválido
            "9",  # opção inválida
            "0",
        ]
        saida, final = self.rodar(CABECALHO + LINHA_OK, entradas)
        for trecho in (
            "Serviço cadastrado.",
            "Esse ID já está cadastrado.",
            "Título: Consumo consciente",
            "Nenhum resultado para essa busca.",
            "Serviço atualizado.",
            "1 - Tarifa Social\n2 - Uso consciente",
            "Total de serviços: 2",
            "- Energia: 1",
            "Serviço excluído.",
            "ID inexistente; nada foi excluído.",
            "Digite um inteiro positivo válido.",
            "Opção inválida.",
            "Dados salvos.",
        ):
            self.assertIn(trecho, saida)
        self.assertEqual(final, CABECALHO + "2;Energia;Uso consciente;Dicas;Comparar aparelhos;Orientação\n")

    def test_id_com_digitos_demais_e_recusado_com_mensagem_clara(self):
        saida, final = self.rodar(CABECALHO + LINHA_OK, ["2", "9" * 5000, "2", "1234567890", "0"])
        self.assertEqual(saida.count("Digite um inteiro positivo válido."), 2)
        self.assertNotIn("limit", saida)
        self.assertEqual(final, CABECALHO + LINHA_OK)

    def test_fim_da_entrada_ou_ctrl_c_salva_e_sai_sem_erro(self):
        for interrupcao in (EOFError(), KeyboardInterrupt()):
            saida, final = self.rodar(CABECALHO + LINHA_OK, ["7", interrupcao])
            self.assertIn("Entrada encerrada. Dados salvos.", saida)
            self.assertEqual(final, CABECALHO + LINHA_OK)

    def test_menu_com_lista_vazia(self):
        saida, final = self.rodar(None, ["2", "3", "4", "5", "6", "7", "8", "0"])
        self.assertEqual(saida.count("Lista vazia."), 6)
        self.assertIn("Não há categorias para resumir.", saida)
        self.assertEqual(final, CABECALHO)


if __name__ == "__main__":
    unittest.main()
