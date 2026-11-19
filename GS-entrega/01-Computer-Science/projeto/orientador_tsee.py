"""Citizen Assist AI — módulo de decisão lógica: Tarifa Social de Energia Elétrica.

Protótipo educacional. NÃO é canal oficial e NÃO confirma a concessão do benefício.
Regras modeladas a partir da Lei nº 12.212/2010 (art. 1º e art. 2º, incisos I e II e § 2º),
com redação atualizada pela Lei nº 15.235/2025 — fontes e datas de consulta no relatório.

Variáveis (1 = sim, 0 = não):
    A  família inscrita no CadÚnico
    B  renda familiar mensal por pessoa de até meio salário mínimo
    C  algum morador recebe o Benefício de Prestação Continuada (BPC)
    D  a conta é de unidade residencial e é a única da família com o benefício

Saídas (exatamente uma vale 1):
    T  há indício de direito à Tarifa Social nesta unidade
    U  a família atende a uma condição, mas D = 0: a unidade não é residencial ou não é a
       única da família com o benefício; conferir a situação com a distribuidora
    K  as condições do art. 2º não foram atendidas: orientar a procurar o CRAS

Uso:
    python orientador_tsee.py            modo interativo
    python orientador_tsee.py --testar   valida as 16 combinações
"""

from __future__ import annotations

import sys
from itertools import product

VARIAVEIS = {
    "A": "A família está inscrita no CadÚnico?",
    "B": "A renda mensal por pessoa da família é de até meio salário mínimo?",
    "C": "Alguém que mora na casa recebe o BPC (Benefício de Prestação Continuada)?",
    "D": "A conta de luz é de uma casa (unidade residencial) e é a única da família com o benefício?",
}

MINTERMOS = {                      # forma canônica: soma de mintermos (A é o bit mais significativo)
    "T": {3, 7, 11, 13, 15},
    "U": {2, 6, 10, 12, 14},
    "K": {0, 1, 4, 5, 8, 9},
}

ORIENTACOES = {
    "T": ("Há indício de direito à Tarifa Social nesta unidade. A lei prevê desconto de 100% "
          "no consumo de até 80 kWh/mês. Confirme com a sua distribuidora de energia; "
          "a decisão é dela, com base no CadÚnico."),
    "U": ("A família atende a uma das condições da Tarifa Social, mas a resposta sobre a conta "
          "foi 'não': ou ela não é de unidade residencial, ou a família já tem o benefício em outra "
          "unidade. A lei aplica a tarifa a uma única unidade residencial por família. Confirme com "
          "a distribuidora a classificação desta unidade e em qual conta o benefício pode ser "
          "aplicado. Isto não garante nem nega o benefício."),
    "K": ("Pelas respostas, nenhuma das duas condições do art. 2º da Lei 12.212/2010 foi atendida. "
          "Procure o CRAS para inscrever ou atualizar o CadÚnico e verificar outras situações "
          "previstas em lei. Isto não é uma negativa oficial."),
}

AVISO = ("Protótipo educacional do Citizen Assist AI. Não é canal oficial, não guarda respostas "
         "e não confirma a concessão de serviços ou direitos. Não informe nome, CPF ou endereço.")


# ----------------------------------------------------------------------------- representações
def indice(a: int, b: int, c: int, d: int) -> int:
    return a * 8 + b * 4 + c * 2 + d


def regra_original(a: int, b: int, c: int, d: int) -> dict[str, int]:
    """Regra escrita como no texto da lei (art. 2º, I ou II; § 2º)."""
    condicao_inciso_i = a == 1 and b == 1          # CadÚnico com renda até ½ salário mínimo
    condicao_inciso_ii = c == 1                    # morador que recebe BPC
    atende_art_2 = condicao_inciso_i or condicao_inciso_ii
    if not atende_art_2:
        saida = "K"
    elif d == 1:
        saida = "T"
    else:
        saida = "U"
    return {nome: int(nome == saida) for nome in "TUK"}


def forma_canonica(a: int, b: int, c: int, d: int) -> dict[str, int]:
    """Soma de mintermos, exatamente como na tabela-verdade."""
    m = indice(a, b, c, d)
    return {nome: int(m in conjunto) for nome, conjunto in MINTERMOS.items()}


def forma_simplificada(a: int, b: int, c: int, d: int) -> dict[str, int]:
    """Somas de produtos mínimas obtidas pelos mapas de Karnaugh."""
    na, nb, nc, nd = 1 - a, 1 - b, 1 - c, 1 - d
    return {
        "T": (c & d) | (a & b & d),               # T = CD + ABD
        "U": (c & nd) | (a & b & nd),             # U = CD' + ABD'
        "K": (na & nc) | (nb & nc),               # K = A'C' + B'C'
    }


def circuito_logicly(a: int, b: int, c: int, d: int) -> dict[str, int]:
    """Mesmas 6 portas do circuito montado no Logic.ly (subexpressão R compartilhada)."""
    g1 = a & b                 # AND
    r = g1 | c                 # OR   -> R = AB + C
    t = r & d                  # AND  -> T = D·R
    d_neg = 1 - d              # NOT  -> D'
    u = r & d_neg              # AND  -> U = D'·R
    k = 1 - r                  # NOT  -> K = R'  (De Morgan: R' = (A'+B')C')
    return {"T": t, "U": u, "K": k}


# Saídas observadas no Logic.ly (prints/mXX_ABCD_xxxx.jpg): lâmpada acesa em cada combinação.
OBSERVADO_LOGICLY = ["K", "K", "U", "T", "K", "K", "U", "T",
                     "K", "K", "U", "T", "U", "T", "U", "T"]


# ----------------------------------------------------------------------------- entrada
RESPOSTAS = {"1": 1, "s": 1, "sim": 1, "0": 0, "n": 0, "nao": 0, "não": 0}


def interpretar(texto: str) -> int | None:
    """Converte a resposta em 0/1; devolve None se ela for inválida."""
    return RESPOSTAS.get(texto.strip().lower())


def perguntar(variavel: str, ler=input, escrever=print, tentativas: int = 3) -> int:
    for _ in range(tentativas):
        valor = interpretar(ler(f"{variavel}) {VARIAVEIS[variavel]} [s/n]: "))
        if valor is not None:
            return valor
        escrever("  Resposta inválida. Digite s (sim) ou n (não); também vale 1 ou 0.")
    raise ValueError(f"Muitas respostas inválidas para {variavel}.")


def orientar(saidas: dict[str, int]) -> str:
    ativas = [nome for nome, valor in saidas.items() if valor == 1]
    if len(ativas) != 1:
        raise RuntimeError(f"Estado lógico inconsistente: {saidas}")
    return f"[{ativas[0]}] {ORIENTACOES[ativas[0]]}"


# ----------------------------------------------------------------------------- validação
def validar_tudo(escrever=print) -> bool:
    escrever("m   A B C D | original | canônica | simplificada | Logic.ly(portas) | Logic.ly(print) | ok")
    tudo_ok = True
    for a, b, c, d in product((0, 1), repeat=4):
        m = indice(a, b, c, d)
        resultados = [f(a, b, c, d) for f in (regra_original, forma_canonica,
                                                forma_simplificada, circuito_logicly)]
        nomes = ["".join(n for n, v in r.items() if v) for r in resultados]
        observado = OBSERVADO_LOGICLY[m]
        ok = all(r == resultados[0] for r in resultados) and nomes[0] == observado \
            and sum(resultados[0].values()) == 1
        tudo_ok &= ok
        escrever(f"m{m:<2} {a} {b} {c} {d} |    {nomes[0]}     |    {nomes[1]}     |      {nomes[2]}       "
                 f"|        {nomes[3]}         |        {observado}        | {'OK' if ok else 'FALHA'}")
    escrever("Resultado: " + ("16/16 combinações equivalentes nas cinco representações."
                              if tudo_ok else "há divergências."))
    return tudo_ok


def main() -> int:
    if "--testar" in sys.argv:
        return 0 if validar_tudo() else 1
    print("Citizen Assist AI — orientação sobre a Tarifa Social de Energia Elétrica")
    print(AVISO, "\n")
    try:
        respostas = [perguntar(v) for v in "ABCD"]
    except (ValueError, EOFError, KeyboardInterrupt) as erro:
        print(f"\nAtendimento encerrado: {erro if isinstance(erro, ValueError) else 'entrada interrompida'}.")
        return 1
    saidas = forma_simplificada(*respostas)
    print("\nEntradas A B C D =", *respostas, "| Saídas T U K =", saidas["T"], saidas["U"], saidas["K"])
    print(orientar(saidas))
    print("\nFonte: Lei nº 12.212/2010, arts. 1º e 2º (redação da Lei nº 15.235/2025).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
