"""Cálculos de energia do Citizen Assist AI (SERS): banho quente em casa.

Necessidade analisada: aquecer a água do banho de uma família durante 12 meses.
Situação de referência: chuveiro elétrico.
Alternativa A (economia): banhos mais curtos e/ou posição de menor potência.
Alternativa B (fonte renovável): aquecedor solar térmico com apoio elétrico.
Combinação A + B: o aquecedor solar atua sobre o consumo já reduzido (sem dupla contagem).

Todas as funções são puras: recebem números, validam e devolvem números.
Unidades: potência em W, tempo em minutos, energia em kWh, dinheiro em R$,
emissões em kg de CO2. Fórmulas e fontes em docs/analise.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

DIAS_POR_MES = 30  # mês de referência
MESES_POR_ANO = 12
LIMITE_TARIFA_SOCIAL_KWH = 80.0  # Lei 12.212/2010, art. 1º (redação da Lei 15.235/2025)


class EntradaInvalida(ValueError):
    """Valor fora da faixa aceita; a mensagem explica o que corrigir."""


def _numero(nome: str, valor, minimo: float, maximo: float, inclui_minimo: bool = True) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise EntradaInvalida(f"{nome}: informe um número.")
    valor = float(valor)
    if not math.isfinite(valor):
        raise EntradaInvalida(f"{nome}: informe um número finito.")
    abaixo = valor < minimo if inclui_minimo else valor <= minimo
    if abaixo or valor > maximo:
        sinal = "de" if inclui_minimo else "maior que"
        raise EntradaInvalida(f"{nome}: o valor deve ser {sinal} {minimo:g} até {maximo:g} (recebido: {valor:g}).")
    return valor


# --------------------------------------------------------------------------- consumo
def consumo_mensal_kwh(
    potencia_w: float, minutos_por_banho: float, banhos_por_dia: float, dias: int = DIAS_POR_MES
) -> float:
    """Energia (kWh) = potência (kW) × tempo (h).

    kWh/mês = (W / 1000) × (minutos por banho / 60) × banhos por dia × dias
    """
    potencia = _numero("Potência do chuveiro (W)", potencia_w, 500, 12000)
    minutos = _numero("Minutos por banho", minutos_por_banho, 0, 60, inclui_minimo=False)
    banhos = _numero("Banhos por dia", banhos_por_dia, 0, 40, inclui_minimo=False)
    dias = _numero("Dias no mês", dias, 1, 31)
    return (potencia / 1000) * (minutos / 60) * banhos * dias


def fatura_mensal(consumo_total_kwh: float, tarifa_rs_kwh: float, tarifa_social: bool = False) -> float:
    """Valor aproximado da energia na fatura do mês (R$).

    Sem Tarifa Social: consumo × tarifa.
    Com Tarifa Social: os primeiros 80 kWh têm desconto de 100%; o restante paga a
    tarifa informada. Simplificação: ignora bandeiras, iluminação pública e a
    variação de impostos; por isso é uma estimativa, não o valor da conta.
    """
    consumo = _numero("Consumo total da casa (kWh/mês)", consumo_total_kwh, 0, 5000)
    tarifa = _numero("Tarifa (R$/kWh)", tarifa_rs_kwh, 0, 5, inclui_minimo=False)
    if tarifa_social:
        consumo = max(0.0, consumo - LIMITE_TARIFA_SOCIAL_KWH)
    return consumo * tarifa


def emissoes_kg(energia_kwh: float, fator_kg_co2_por_kwh: float) -> float:
    """Emissões indiretas da eletricidade: kWh × fator de emissão da rede (kg CO2/kWh)."""
    energia = _numero("Energia (kWh)", energia_kwh, 0, 1e7)
    fator = _numero("Fator de emissão (kg CO2/kWh)", fator_kg_co2_por_kwh, 0, 2)
    return energia * fator


# --------------------------------------------------------------------------- cenários
@dataclass(frozen=True)
class Entrada:
    """Informações da família. Os padrões estão justificados em dados/premissas.json."""

    potencia_w: float = 5500.0
    minutos_por_banho: float = 8.0
    banhos_por_dia: float = 4.0
    tarifa_rs_kwh: float = 0.95
    outros_consumos_kwh_mes: float = 100.0  # resto da casa (geladeira, luz, TV…)
    tarifa_social: bool = False
    # Alternativa A — economia
    minutos_reduzidos: float = 5.0
    potencia_reduzida_w: float | None = None  # None = mantém a potência
    # Alternativa B — aquecedor solar térmico (hipóteses a confirmar com orçamento)
    fracao_solar: float = 0.6  # parte da energia do banho fornecida pelo sol
    investimento_solar_rs: float = 3000.0
    manutencao_solar_rs_ano: float = 100.0
    vida_util_solar_anos: float = 15.0
    pode_instalar_solar: bool = True  # imóvel próprio/autorizado e telhado com sol
    # Ambiente
    fator_emissao_kg_kwh: float = 0.0385
    horizonte_anos: float = 10.0


@dataclass(frozen=True)
class Cenario:
    nome: str
    kwh_mes: float  # energia elétrica do banho
    custo_energia_ano: float  # parte da fatura anual atribuída ao banho
    investimento: float
    manutencao_ano: float
    co2_kg_ano: float
    economia_ano: float  # em relação à referência, já descontada a manutenção
    kwh_evitados_ano: float
    payback_anos: float | None  # None = sem investimento ou sem retorno. Em A+B é o retorno
    # do aquecedor solar sobre o que ele economiza ALÉM de A.
    custo_total_horizonte: float  # investimento + (energia + manutenção) × horizonte


def _validar(e: Entrada) -> None:
    consumo_mensal_kwh(e.potencia_w, e.minutos_por_banho, e.banhos_por_dia)
    _numero("Tarifa (R$/kWh)", e.tarifa_rs_kwh, 0, 5, inclui_minimo=False)
    _numero("Outros consumos da casa (kWh/mês)", e.outros_consumos_kwh_mes, 0, 3000)
    _numero("Minutos por banho na alternativa A", e.minutos_reduzidos, 0, 60, inclui_minimo=False)
    if e.minutos_reduzidos > e.minutos_por_banho:
        raise EntradaInvalida("Minutos por banho na alternativa A: deve ser menor ou igual ao tempo atual.")
    if e.potencia_reduzida_w is not None:
        _numero("Potência reduzida (W)", e.potencia_reduzida_w, 500, 12000)
        if e.potencia_reduzida_w > e.potencia_w:
            raise EntradaInvalida("Potência reduzida (W): deve ser menor ou igual à potência atual.")
    _numero("Fração solar", e.fracao_solar, 0, 0.95)
    _numero("Investimento no aquecedor solar (R$)", e.investimento_solar_rs, 0, 100000)
    _numero("Manutenção do aquecedor solar (R$/ano)", e.manutencao_solar_rs_ano, 0, 10000)
    _numero("Vida útil do aquecedor solar (anos)", e.vida_util_solar_anos, 1, 40)
    _numero("Fator de emissão (kg CO2/kWh)", e.fator_emissao_kg_kwh, 0, 2)
    _numero("Horizonte de comparação (anos)", e.horizonte_anos, 1, 40)
    if not isinstance(e.tarifa_social, bool) or not isinstance(e.pode_instalar_solar, bool):
        raise EntradaInvalida("Tarifa Social e possibilidade de instalar: responda sim ou não.")


def comparar(e: Entrada) -> dict[str, Cenario]:
    """Compara referência, A, B e A+B para a mesma família e o mesmo período (12 meses)."""
    _validar(e)
    kwh_ref = consumo_mensal_kwh(e.potencia_w, e.minutos_por_banho, e.banhos_por_dia)
    kwh_a = consumo_mensal_kwh(e.potencia_reduzida_w or e.potencia_w, e.minutos_reduzidos, e.banhos_por_dia)
    kwh_b = kwh_ref * (1 - e.fracao_solar)  # o apoio elétrico cobre o que o sol não cobre
    kwh_ab = kwh_a * (1 - e.fracao_solar)  # solar sobre o consumo já reduzido

    def fatura_ano(kwh_banho: float) -> float:
        return fatura_mensal(e.outros_consumos_kwh_mes + kwh_banho, e.tarifa_rs_kwh, e.tarifa_social) * MESES_POR_ANO

    fatura_sem_banho = fatura_ano(0.0)
    fatura_ref = fatura_ano(kwh_ref)

    def montar(
        nome: str, kwh: float, investimento: float, manutencao: float, economia_sem_investir: float = 0.0
    ) -> Cenario:
        fatura = fatura_ano(kwh)
        economia = (fatura_ref - fatura) - manutencao
        # O investimento só "se paga" com a economia que ele mesmo traz: em A+B, a parte
        # que o banho mais curto já economizaria de graça não entra na conta do retorno.
        ganho_do_investimento = economia - economia_sem_investir
        payback = investimento / ganho_do_investimento if investimento > 0 and ganho_do_investimento > 0 else None
        custo_energia = fatura - fatura_sem_banho
        return Cenario(
            nome=nome,
            kwh_mes=kwh,
            custo_energia_ano=custo_energia,
            investimento=investimento,
            manutencao_ano=manutencao,
            co2_kg_ano=emissoes_kg(kwh * MESES_POR_ANO, e.fator_emissao_kg_kwh),
            economia_ano=economia,
            kwh_evitados_ano=(kwh_ref - kwh) * MESES_POR_ANO,
            payback_anos=payback,
            custo_total_horizonte=investimento + (custo_energia + manutencao) * e.horizonte_anos,
        )

    cenario_a = montar("A — Economia: banho mais curto / menor potência", kwh_a, 0.0, 0.0)
    return {
        "referencia": montar("Referência: chuveiro elétrico como é usado hoje", kwh_ref, 0.0, 0.0),
        "A": cenario_a,
        "B": montar(
            "B — Renovável: aquecedor solar com apoio elétrico",
            kwh_b,
            e.investimento_solar_rs,
            e.manutencao_solar_rs_ano,
        ),
        "A+B": montar(
            "A + B — banho mais curto com aquecedor solar (retorno do solar além de A)",
            kwh_ab,
            e.investimento_solar_rs,
            e.manutencao_solar_rs_ano,
            cenario_a.economia_ano,
        ),
    }


# --------------------------------------------------------------------------- orientação
def _n(valor: float, casas: int = 0) -> str:
    """Número no padrão brasileiro: 1.234,5"""
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def recomendar(e: Entrada, cenarios: dict[str, Cenario]) -> list[str]:
    """Orientações em linguagem simples, cada uma apoiada em um número calculado."""
    ref, a, b, ab = (cenarios[k] for k in ("referencia", "A", "B", "A+B"))
    linhas: list[str] = []

    if a.kwh_evitados_ano > 0:
        linhas.append(
            f"Comece pela alternativa A: ela não custa nada e evita cerca de {_n(a.kwh_evitados_ano)} kWh por ano"
            + (
                f", perto de R$ {_n(a.economia_ano)} por ano na conta."
                if a.economia_ano > 0.5
                else ". Na sua conta, porém, a economia em dinheiro é pequena ou nula (veja o aviso sobre a Tarifa Social)."
            )
        )
    else:
        linhas.append(
            "A alternativa A está igual ao uso atual: informe um tempo de banho ou potência menor para ver a economia."
        )

    if not e.pode_instalar_solar:
        linhas.append(
            "O aquecedor solar (B) não é indicado no seu caso agora: é preciso poder instalar no imóvel "
            "(casa própria ou autorização do proprietário) e ter telhado ou laje com sol."
        )
        linhas.append(
            "Para quem mora de aluguel: o aquecedor solar é uma obra no imóvel, então só vale conversar se o "
            "proprietário autorizar e souber de quem é o equipamento se você se mudar. Enquanto isso, o que está ao "
            "seu alcance é a alternativa A: banhos mais curtos e o chuveiro na potência mais baixa em que o banho "
            "continue confortável. Troque o chuveiro só se o contrato permitir."
        )
    elif b.payback_anos is None:
        linhas.append(
            "Com os valores informados, o aquecedor solar (B) não se paga: a economia anual não cobre a manutenção. "
            "Ele ainda reduz o consumo de eletricidade e as emissões, mas não é vantajoso financeiramente."
        )
    elif b.payback_anos > e.vida_util_solar_anos:
        linhas.append(
            f"O aquecedor solar (B) levaria cerca de {_n(b.payback_anos)} anos para se pagar, mais que a vida útil "
            f"considerada ({_n(e.vida_util_solar_anos)} anos). Financeiramente não compensa com esses valores."
        )
    else:
        prazo = "menos de 1 ano" if b.payback_anos < 1 else f"cerca de {_n(b.payback_anos, 1)} anos"
        linhas.append(
            f"O aquecedor solar (B), sem mudar o banho, evita cerca de {_n(b.kwh_evitados_ano)} kWh por ano e se pagaria em "
            f"{prazo} (investimento de R$ {_n(b.investimento)}). Em {_n(e.horizonte_anos)} anos, o custo total estimado é "
            f"R$ {_n(b.custo_total_horizonte)}, contra R$ {_n(ref.custo_total_horizonte)} mantendo tudo como está."
        )
        if a.kwh_evitados_ano > 0:
            ganho_extra = ab.economia_ano - a.economia_ano
            if ab.payback_anos is None:
                retorno = "o aquecedor deixa de se pagar"
            elif ab.payback_anos > e.vida_util_solar_anos:
                retorno = (
                    f"o retorno do aquecedor sobe para cerca de {_n(ab.payback_anos)} anos, mais que a vida útil "
                    f"considerada ({_n(e.vida_util_solar_anos)} anos)"
                )
            else:
                retorno = f"o retorno do aquecedor sobe para cerca de {_n(ab.payback_anos, 1)} anos"
            linhas.append(
                f"Atenção ao juntar as duas (A + B): o consumo do banho cai para {_n(ab.kwh_mes)} kWh por mês, o menor de todos, "
                f"mas quem já toma banho mais curto tem menos a economizar com o sol. O aquecedor passa a render só "
                f"R$ {_n(ganho_extra)} por ano além de A, e {retorno}. Faça A primeiro e decida sobre B com um orçamento real."
            )

    if e.tarifa_social:
        linhas.append(
            f"Tarifa Social: os primeiros {_n(LIMITE_TARIFA_SOCIAL_KWH)} kWh do mês têm desconto de 100%. "
            "A economia em reais só aparece na parte do consumo acima desse limite; abaixo dele, economizar energia "
            "continua ajudando o meio ambiente e evita ultrapassar o limite."
        )

    linhas.append(
        f"Meio ambiente: o banho como é hoje responde por cerca de {_n(ref.co2_kg_ano)} kg de CO2 por ano; "
        f"com A seriam {_n(a.co2_kg_ano)} kg e com B, {_n(b.co2_kg_ano)} kg (eletricidade da rede brasileira). "
        "O aquecedor solar também tem impacto de fabricação e transporte, que esta conta não inclui."
    )
    return linhas


AVISOS = (
    "São estimativas, não garantias: o resultado depende do uso real, do clima, da tarifa e do orçamento do equipamento.",
    "A fração solar, o preço, a manutenção e a vida útil do aquecedor solar são hipóteses. Peça ao menos dois orçamentos "
    "e confirme com o instalador quanto do banho o sol cobre na sua cidade.",
    "O valor em reais usa a tarifa informada e ignora bandeiras tarifárias, iluminação pública e mudanças de imposto.",
    "Não mexa na instalação elétrica nem no telhado sem um profissional habilitado.",
    "Protótipo educacional: não é canal oficial e não guarda nenhuma informação digitada.",
)
