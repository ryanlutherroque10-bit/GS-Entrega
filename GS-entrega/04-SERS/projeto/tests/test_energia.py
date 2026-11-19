"""Testes técnicos dos cálculos e do assistente (python -m unittest discover -s tests -v)."""

from __future__ import annotations

import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from energia import assistente  # noqa: E402
from energia.calculos import (
    Entrada,
    EntradaInvalida,
    comparar,
    consumo_mensal_kwh,  # noqa: E402
    emissoes_kg,
    fatura_mensal,
    recomendar,
)


class TestFormulas(unittest.TestCase):
    def test_consumo_confere_com_exemplo_publico(self):
        # 5.500 W por 30 min/dia em 30 dias = 82,5 kWh (exemplo citado nas referências)
        self.assertAlmostEqual(consumo_mensal_kwh(5500, 30, 1), 82.5)
        self.assertAlmostEqual(consumo_mensal_kwh(5500, 8, 4), 88.0)  # cenário padrão
        self.assertAlmostEqual(consumo_mensal_kwh(1000, 60, 1, dias=1), 1.0)  # 1 kW por 1 h = 1 kWh

    def test_fatura_sem_e_com_tarifa_social(self):
        self.assertAlmostEqual(fatura_mensal(200, 0.95), 190.0)
        self.assertAlmostEqual(fatura_mensal(200, 0.95, tarifa_social=True), 114.0)  # paga só 120 kWh
        self.assertEqual(fatura_mensal(80, 0.95, tarifa_social=True), 0.0)  # limite exato
        self.assertEqual(fatura_mensal(50, 0.95, tarifa_social=True), 0.0)
        self.assertAlmostEqual(fatura_mensal(81, 1.0, tarifa_social=True), 1.0)

    def test_emissoes(self):
        self.assertAlmostEqual(emissoes_kg(1000, 0.0385), 38.5)
        self.assertEqual(emissoes_kg(0, 0.0385), 0.0)

    def test_entradas_invalidas(self):
        for args in (
            (0, 8, 4),
            (-5500, 8, 4),
            (5500, 0, 4),
            (5500, 8, 0),
            (5500, 61, 4),
            (20000, 8, 4),
            ("5500", 8, 4),
            (float("nan"), 8, 4),
            (float("inf"), 8, 4),
            (True, 8, 4),
        ):
            with self.assertRaises(EntradaInvalida, msg=args):
                consumo_mensal_kwh(*args)
        with self.assertRaises(EntradaInvalida):
            fatura_mensal(100, 0)
        with self.assertRaises(EntradaInvalida):
            fatura_mensal(-1, 0.9)


class TestComparacao(unittest.TestCase):
    def setUp(self):
        self.e = Entrada()
        self.c = comparar(self.e)

    def test_cenario_padrao_documentado(self):
        ref, a, b, ab = (self.c[k] for k in ("referencia", "A", "B", "A+B"))
        self.assertAlmostEqual(ref.kwh_mes, 88.0)
        self.assertAlmostEqual(a.kwh_mes, 55.0)
        self.assertAlmostEqual(b.kwh_mes, 35.2)
        self.assertAlmostEqual(ab.kwh_mes, 22.0)
        self.assertAlmostEqual(ref.custo_energia_ano, 1003.2)
        self.assertAlmostEqual(a.economia_ano, 376.2)
        self.assertAlmostEqual(b.economia_ano, 501.92)  # 601,92 de energia − 100 de manutenção
        self.assertAlmostEqual(b.payback_anos, 3000 / 501.92)
        # A+B: o solar só é creditado pelo que economiza além de A (652,40 − 376,20 = 276,20/ano)
        self.assertAlmostEqual(ab.economia_ano, 652.4)
        self.assertAlmostEqual(ab.payback_anos, 3000 / 276.2)
        self.assertGreater(ab.payback_anos, b.payback_anos)
        self.assertAlmostEqual(ref.co2_kg_ano, 88 * 12 * 0.0385)
        self.assertAlmostEqual(b.custo_total_horizonte, 3000 + (401.28 + 100) * 10)
        self.assertIsNone(a.payback_anos)
        self.assertEqual(ref.economia_ano, 0.0)

    def test_combinacao_nao_conta_economia_em_dobro(self):
        ref, a, b, ab = (self.c[k] for k in ("referencia", "A", "B", "A+B"))
        soma_ingenua = a.kwh_evitados_ano + b.kwh_evitados_ano
        self.assertLess(ab.kwh_evitados_ano, soma_ingenua)
        self.assertLessEqual(ab.kwh_evitados_ano, ref.kwh_mes * 12)
        self.assertAlmostEqual(ab.kwh_mes, a.kwh_mes * (1 - self.e.fracao_solar))

    def test_tarifa_social_reduz_economia_em_reais_mas_nao_em_kwh(self):
        # casa de baixo consumo: 30 kWh de outros usos + 44 kWh de banho = 74 kWh (< 80)
        e = replace(self.e, tarifa_social=True, outros_consumos_kwh_mes=30, banhos_por_dia=2)
        c = comparar(e)
        self.assertEqual(c["referencia"].custo_energia_ano, 0.0)
        self.assertEqual(c["A"].economia_ano, 0.0)
        self.assertGreater(c["A"].kwh_evitados_ano, 0)
        self.assertIsNone(c["B"].payback_anos)
        texto = " ".join(recomendar(e, c))
        self.assertIn("Tarifa Social", texto)
        self.assertIn("não se paga", texto)

    def test_limites(self):
        igual = comparar(replace(self.e, minutos_reduzidos=8))  # A sem mudança
        self.assertEqual(igual["A"].kwh_evitados_ano, 0.0)
        self.assertIn("igual ao uso atual", recomendar(replace(self.e, minutos_reduzidos=8), igual)[0])
        sem_sol = comparar(replace(self.e, fracao_solar=0))
        self.assertAlmostEqual(sem_sol["B"].kwh_mes, sem_sol["referencia"].kwh_mes)
        self.assertIsNone(sem_sol["B"].payback_anos)
        gratis = comparar(replace(self.e, investimento_solar_rs=0, manutencao_solar_rs_ano=0))
        self.assertIsNone(gratis["B"].payback_anos)
        self.assertGreater(gratis["B"].economia_ano, 0)

    def test_recomendacoes_dependem_das_condicoes(self):
        caro = replace(self.e, investimento_solar_rs=20000)
        self.assertIn("não compensa", " ".join(recomendar(caro, comparar(caro))))
        inquilino = replace(self.e, pode_instalar_solar=False)
        self.assertIn("não é indicado", " ".join(recomendar(inquilino, comparar(inquilino))))
        normal = " ".join(recomendar(self.e, self.c))
        self.assertIn("Comece pela alternativa A", normal)
        self.assertIn("se pagaria em cerca de 6,0 anos", normal)
        self.assertIn("sobe para cerca de 10,9 anos", normal)

    def test_entradas_incoerentes(self):
        for mudanca in (
            {"minutos_reduzidos": 9},
            {"potencia_reduzida_w": 6000},
            {"fracao_solar": 1.2},
            {"fracao_solar": -0.1},
            {"tarifa_rs_kwh": 0},
            {"investimento_solar_rs": -1},
            {"horizonte_anos": 0},
            {"tarifa_social": "sim"},
            {"fator_emissao_kg_kwh": 5},
        ):
            with self.assertRaises(EntradaInvalida, msg=mudanca):
                comparar(replace(self.e, **mudanca))

    def test_padroes_do_codigo_iguais_ao_arquivo_de_premissas(self):
        premissas = json.loads((RAIZ / "dados" / "premissas.json").read_text(encoding="utf-8"))["parametros"]
        for nome, item in premissas.items():
            self.assertEqual(getattr(self.e, nome), item["valor"], nome)
            self.assertIn(item["tipo"], ("dado público", "estimado", "hipótese"))
            self.assertTrue(item["fonte"] and item["justificativa"])


class TestAssistente(unittest.TestCase):
    def conversar(self, respostas, argumentos=()):
        fila, saida = list(respostas), []

        def ler(pergunta):
            saida.append(pergunta)
            if not fila:
                raise EOFError
            return fila.pop(0)

        codigo = assistente.main(list(argumentos), ler, lambda *partes: saida.append(" ".join(map(str, partes))))
        return codigo, "\n".join(saida)

    def test_exemplo_mostra_calculo_recomendacao_limites_e_fontes(self):
        codigo, texto = self.conversar([], ["--exemplo"])
        self.assertEqual(codigo, 0)
        for trecho in (
            "88 kWh por mês",
            "Comece pela alternativa A",
            "aquecedor solar",
            "Limites desta estimativa",
            "não garantias",
            "De onde vêm os números",
            "Lei nº 12.212/2010",
            "38,5 kg CO2/MWh",
        ):
            self.assertIn(trecho, texto)

    def test_conversa_completa_com_valores_do_usuario(self):
        # 4400 W, 10 min, 3 banhos, R$ 1,00, 120 kWh, sem TS, meta 6 min, pode instalar, R$ 2500, fração 0,5, não repetir
        codigo, texto = self.conversar(["4400", "10", "3", "1,00", "120", "n", "6", "s", "R$ 2500", "0,5", "n"])
        self.assertEqual(codigo, 0)
        self.assertIn("66 kWh por mês", texto)  # 4,4 kW × (10/60) h × 3 × 30
        self.assertIn("kWh é a unidade de energia da conta", texto)
        self.assertIn("Até logo!", texto)

    def test_entrada_invalida_ajuda_e_valores_fora_da_faixa(self):
        codigo, texto = self.conversar(["abc", "?", "", "", "", "", "", "", "", "", "", "", "n"])
        self.assertIn("Não entendi", texto)
        self.assertIn("ESTIMADO", texto)  # ajuda da potência
        self.assertIn("88 kWh por mês", texto)
        codigo, texto = self.conversar(["99999", "", "", "", "", "", "", "", "", "", "n"])
        self.assertIn("Não foi possível calcular", texto)
        self.assertIn("Potência do chuveiro", texto)
        codigo, texto = self.conversar(["x", "y", "z", "n"])
        self.assertEqual(codigo, 0)
        self.assertIn("Muitas respostas inválidas", texto)
        self.assertNotIn("RESULTADO", texto)

    def test_resumo_explicacao_e_comparacao_de_potencias(self):
        _, texto = self.conversar([], ["--exemplo"])
        for trecho in (
            "Em resumo:",
            "R$ 83,60 por mês, ou R$ 1.003 por ano",
            "R$ 31,35 por mês",
            "se paga em cerca de 6,0 anos",
            "Como a conta foi feita:",
            "Retorno = investimento ÷ economia por ano",
            "outra potência",
            "4.400 W",
            "7.700 W",
            "(o seu)",
        ):
            self.assertIn(trecho, texto)

    def test_casa_alugada_recebe_orientacao_propria(self):
        # 4400 W, 10 min, 3 banhos, R$ 1,00, 60 kWh, com Tarifa Social, meta 6 min, NÃO pode instalar, valores padrão, não repetir
        _, texto = self.conversar(["4400", "10", "3", "1,00", "60", "s", "6", "n", "", "", "n"])
        self.assertIn("Para quem mora de aluguel", texto)
        self.assertIn("autorização do proprietário", texto)
        self.assertIn("não indicado agora", texto)

    def test_tarifa_social_e_solar_indisponivel_ficam_claros(self):
        entrada = replace(Entrada(), tarifa_social=True, pode_instalar_solar=False)
        saida = []
        assistente.responder(entrada, saida.append)
        texto = "\n".join(saida)
        self.assertIn("primeiros 80 kWh", texto)
        self.assertIn("B e A+B são apenas comparações numéricas", texto)
        self.assertIn("Opção viável agora: A", texto)

    def test_sair_e_fim_da_entrada(self):
        self.assertIn("Atendimento encerrado", self.conversar(["sair"])[1])
        self.assertEqual(self.conversar([])[0], 0)


if __name__ == "__main__":
    unittest.main()
