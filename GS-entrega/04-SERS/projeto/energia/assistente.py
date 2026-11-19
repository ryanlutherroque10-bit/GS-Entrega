"""Citizen Assist AI — assistente de energia no terminal (SERS).

Pergunta os dados do banho da família, calcula o consumo e compara:
referência (chuveiro elétrico), A (economia) e B (aquecedor solar, fonte renovável).

Uso (a partir da pasta do repositório):
    python -m energia.assistente            conversa interativa
    python -m energia.assistente --exemplo  mostra o cenário de referência documentado

Em cada pergunta, Enter aceita o valor entre colchetes. Digite "?" para ver de onde
vem o valor sugerido e "sair" para encerrar. Nada do que é digitado é gravado.
"""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

from .calculos import AVISOS, Cenario, Entrada, EntradaInvalida, _n, comparar, consumo_mensal_kwh, recomendar

PREMISSAS = json.loads((Path(__file__).resolve().parents[1] / "dados" / "premissas.json").read_text(encoding="utf-8"))
TENTATIVAS = 3


class Encerrar(Exception):
    pass


def _ajuda(chave: str) -> str:
    p = PREMISSAS["parametros"][chave]
    return f"    {p['tipo'].upper()}: {p['justificativa']} Fonte: {p['fonte']}"


def perguntar_numero(texto: str, padrao: float, chave: str, ler=input, escrever=print) -> float:
    for _ in range(TENTATIVAS):
        resposta = ler(f"{texto} [{padrao:g}]: ").strip().lower()
        if resposta in ("sair", "q"):
            raise Encerrar
        if resposta == "?":
            escrever(_ajuda(chave))
            continue
        if not resposta:
            return float(padrao)
        try:
            return float(resposta.replace("r$", "").replace(" ", "").replace(",", "."))
        except ValueError:
            escrever(
                "    Não entendi. Digite só o número (exemplo: 5500 ou 0,95), ? para ajuda ou Enter para o valor sugerido."
            )
    raise EntradaInvalida(f"Muitas respostas inválidas em: {texto}")


def perguntar_sim_nao(texto: str, padrao: bool, ler=input, escrever=print) -> bool:
    for _ in range(TENTATIVAS):
        resposta = ler(f"{texto} [{'s' if padrao else 'n'}]: ").strip().lower()
        if resposta in ("sair", "q"):
            raise Encerrar
        if not resposta:
            return padrao
        if resposta in ("s", "sim", "1"):
            return True
        if resposta in ("n", "nao", "não", "0"):
            return False
        escrever("    Responda s (sim) ou n (não).")
    raise EntradaInvalida(f"Muitas respostas inválidas em: {texto}")


def coletar(ler=input, escrever=print) -> Entrada:
    p = Entrada()
    n = lambda texto, valor, chave: perguntar_numero(texto, valor, chave, ler, escrever)  # noqa: E731
    escrever("\n-- Como é o banho hoje --")
    potencia = n("Potência do chuveiro em watts (está na etiqueta ou na embalagem)", p.potencia_w, "potencia_w")
    minutos = n("Quantos minutos dura cada banho, em média", p.minutos_por_banho, "minutos_por_banho")
    banhos = n("Quantos banhos por dia na casa (somando todo mundo)", p.banhos_por_dia, "banhos_por_dia")
    escrever("\n-- Sua conta de luz --")
    escrever("kWh é a unidade de energia da conta. Procure 'consumo (kWh)' e 'valor total' na fatura;")
    escrever("se não encontrar, pressione Enter para usar os valores sugeridos e trate o resultado como exemplo.")
    tarifa = n("Preço do kWh em reais (total da conta dividido pelos kWh do mês)", p.tarifa_rs_kwh, "tarifa_rs_kwh")
    outros = n(
        "Consumo do resto da casa em kWh por mês (kWh da conta menos o banho)",
        p.outros_consumos_kwh_mes,
        "outros_consumos_kwh_mes",
    )
    social = perguntar_sim_nao("A família recebe a Tarifa Social de Energia", p.tarifa_social, ler, escrever)
    escrever("\n-- Alternativa A: economizar --")
    reduzido = n("Para quantos minutos o banho poderia cair", min(p.minutos_reduzidos, minutos), "minutos_reduzidos")
    escrever("\n-- Alternativa B: aquecedor solar (fonte renovável) --")
    pode = perguntar_sim_nao(
        "A casa é própria (ou o dono autoriza) e tem telhado ou laje que pega sol", True, ler, escrever
    )
    investimento = n(
        "Preço do aquecedor solar instalado, em reais (use um orçamento, se tiver)",
        p.investimento_solar_rs,
        "investimento_solar_rs",
    )
    fracao = n(
        "Quanto do banho o sol consegue aquecer, de 0 a 0,95 (pergunte ao instalador)", p.fracao_solar, "fracao_solar"
    )
    return replace(
        p,
        potencia_w=potencia,
        minutos_por_banho=minutos,
        banhos_por_dia=banhos,
        tarifa_rs_kwh=tarifa,
        outros_consumos_kwh_mes=outros,
        tarifa_social=social,
        minutos_reduzidos=reduzido,
        pode_instalar_solar=pode,
        investimento_solar_rs=investimento,
        fracao_solar=fracao,
    )


def _reais(valor: float, casas: int = 0) -> str:
    return f"R$ {_n(valor, casas)}"


def tabela(cenarios: dict[str, Cenario], horizonte: float) -> str:
    linhas = [
        f"{'Opção':<10}{'kWh/mês':>9}{'Energia/ano':>13}{'Investimento':>14}{'Economia/ano':>14}"
        f"{'Retorno':>10}{'CO2 kg/ano':>12}{f'Total {horizonte:.0f} anos':>15}"
    ]
    for chave, c in cenarios.items():
        retorno = "—" if c.payback_anos is None else f"{_n(c.payback_anos, 1)} anos"
        linhas.append(
            f"{chave:<10}{_n(c.kwh_mes, 1):>9}{_reais(c.custo_energia_ano):>13}{_reais(c.investimento):>14}"
            f"{_reais(c.economia_ano):>14}{retorno:>10}{_n(c.co2_kg_ano, 1):>12}{_reais(c.custo_total_horizonte):>15}"
        )
    return "\n".join(linhas)


def resumo(entrada: Entrada, cenarios: dict[str, Cenario]) -> list[str]:
    """Frases curtas com os números principais (gasto por mês e por ano, economia, retorno)."""
    ref, a, b = cenarios["referencia"], cenarios["A"], cenarios["B"]
    linhas = [
        f"O banho custa cerca de {_reais(ref.custo_energia_ano / 12, 2)} por mês, ou {_reais(ref.custo_energia_ano)} por ano.",
    ]
    if a.economia_ano > 0.5:
        linhas.append(
            f"Banho mais curto (A): economiza cerca de {_reais(a.economia_ano / 12, 2)} por mês "
            f"({_reais(a.economia_ano)} por ano), sem gastar nada."
        )
    if not entrada.pode_instalar_solar:
        linhas.append(
            "Aquecedor solar (B): não indicado agora; antes é preciso a autorização do proprietário (imóvel alugado) "
            "e um telhado ou laje com sol."
        )
    elif b.payback_anos is None:
        linhas.append("Aquecedor solar (B): com esses valores a economia não cobre a manutenção.")
    else:
        linhas.append(
            f"Aquecedor solar (B): custa {_reais(b.investimento)} e se paga em cerca de {_n(b.payback_anos, 1)} anos."
        )
    return linhas


def responder(entrada: Entrada, escrever=print) -> dict[str, Cenario]:
    cenarios = comparar(entrada)
    ref = cenarios["referencia"]
    escrever("\n================ RESULTADO ================")
    escrever(
        f"Hoje o banho gasta cerca de {_n(ref.kwh_mes)} kWh por mês "
        f"({_n(entrada.potencia_w)} W × {entrada.minutos_por_banho:g} min × {entrada.banhos_por_dia:g} banhos × 30 dias), "
        f"ou {_reais(ref.custo_energia_ano)} por ano na conta."
    )
    escrever("\nEm resumo:")
    for linha in resumo(entrada, cenarios):
        escrever(f" • {linha}")
    if entrada.tarifa_social:
        escrever(
            "Tarifa Social neste modelo: os primeiros 80 kWh do consumo total da casa no mês têm desconto de 100%. "
            "Exemplo: se a casa consumir 100 kWh, paga a energia dos 20 kWh acima do limite. "
            "O custo atribuído ao banho depende também dos outros aparelhos."
        )
    escrever("\nComo a conta foi feita:")
    escrever(
        f" • Energia do banho = potência × tempo. {_n(entrada.potencia_w)} W = {_n(entrada.potencia_w / 1000, 1)} kW; "
        f"{entrada.minutos_por_banho:g} min × {entrada.banhos_por_dia:g} banhos × 30 dias = "
        f"{_n(entrada.minutos_por_banho * entrada.banhos_por_dia * 30 / 60, 1)} horas por mês."
    )
    escrever(
        f" • Dinheiro = kWh × preço do kWh (R$ {_n(entrada.tarifa_rs_kwh, 2)}). "
        'Economia = quanto a conta cai em relação ao "referencia" (como é hoje).'
    )
    escrever(" • Retorno = investimento ÷ economia por ano: em quantos anos o aquecedor se paga.")
    escrever("\nComparação para a mesma família, em 12 meses:")
    escrever(tabela(cenarios, entrada.horizonte_anos))
    escrever("  kWh/mês = energia do banho por mês; Energia/ano = gasto do banho em 12 meses.")
    escrever("  Economia/ano = diferença anual em relação a hoje; Total em 10 anos = gasto acumulado, com investimento.")
    escrever(
        "  Economia/ano: em relação à referência, já descontada a manutenção. Retorno: anos para a economia pagar o"
    )
    escrever("  investimento; em A+B conta só o que o aquecedor economiza além de A. Tarifa mantida constante.")
    if not entrada.pode_instalar_solar:
        escrever("  B e A+B são apenas comparações numéricas: aquecedor solar indisponível neste imóvel sem autorização/condições de instalação.")
        escrever("  Opção viável agora: A (banho mais curto), se o tempo proposto for menor que o atual.")
    for chave, c in cenarios.items():
        escrever(f"  {chave}: {c.nome}")
    escrever("\nSe o chuveiro tivesse outra potência (mesmo tempo e mesmo número de banhos):")
    for potencia in sorted({4400.0, 5500.0, 7700.0, entrada.potencia_w}):
        kwh = consumo_mensal_kwh(potencia, entrada.minutos_por_banho, entrada.banhos_por_dia)
        marca = "  (o seu)" if potencia == entrada.potencia_w else ""
        escrever(f"   {_n(potencia):>6} W: {_n(kwh, 1):>6} kWh/mês, {_reais(kwh * entrada.tarifa_rs_kwh * 12)} por ano{marca}")
    escrever("   (valor bruto, sem o desconto da Tarifa Social; potências típicas de chuveiros elétricos)")
    escrever("\nO que recomendamos:")
    for i, linha in enumerate(recomendar(entrada, cenarios), 1):
        escrever(f" {i}. {linha}")
    escrever("\nLimites desta estimativa:")
    for aviso in AVISOS:
        escrever(f" - {aviso}")
    escrever("\nDe onde vêm os números:")
    for ref_ in PREMISSAS["referencias_resumidas"]:
        escrever(f" - {ref_}")
    escrever(" Lista completa, datas de consulta e fórmulas: docs/analise.md e docs/referencias.md")
    return cenarios


def main(argumentos: list[str] | None = None, ler=input, escrever=print) -> int:
    argumentos = sys.argv[1:] if argumentos is None else argumentos
    escrever("Citizen Assist AI — energia em casa: quanto custa o banho quente e como gastar menos")
    escrever(
        "Protótipo educacional. Não é canal oficial e não guarda o que você digitar. Não informe nome, CPF ou endereço."
    )
    try:
        if "--exemplo" in argumentos:
            escrever("\nCenário de referência documentado em docs/analise.md (valores sugeridos, não medidos).")
            responder(Entrada(), escrever)
            return 0
        escrever('Enter aceita o valor entre colchetes; "?" mostra de onde ele vem; "sair" encerra.')
        while True:
            try:
                responder(coletar(ler, escrever), escrever)
            except EntradaInvalida as erro:
                escrever(f"\nNão foi possível calcular: {erro}\nConfira o valor e tente de novo.")
            if not perguntar_sim_nao("\nQuer simular outra situação", False, ler, escrever):
                escrever("Até logo!")
                return 0
    except (Encerrar, EOFError, KeyboardInterrupt):
        escrever("\nAtendimento encerrado.")
        return 0
    except EntradaInvalida as erro:
        escrever(f"\nAtendimento encerrado: {erro}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
