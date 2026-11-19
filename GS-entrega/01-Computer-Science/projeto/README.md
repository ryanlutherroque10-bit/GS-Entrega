# Citizen Assist AI — módulo de decisão lógica (Computer Science)

Global Solution 2026.2 · Ciência da Computação · Turma 1CC-FEV
Integrantes: Ryan Luther Roque (RM 572993) e João Guilherme Figueiredo (RM 572697)

O módulo orienta o cidadão sobre a **Tarifa Social de Energia Elétrica** a partir de quatro respostas de sim/não. As regras vêm da Lei nº 12.212/2010 (art. 2º, I e II, e § 2º; art. 1º com a redação da Lei nº 15.235/2025).

> Protótipo educacional: não é canal oficial, não coleta dados pessoais e não confirma a concessão de serviços ou direitos.

| Variável | 1 | 0 |
| --- | --- | --- |
| A | família inscrita no CadÚnico | não inscrita |
| B | renda por pessoa até ½ salário mínimo | acima disso |
| C | algum morador recebe o BPC | ninguém recebe |
| D | a conta é de unidade residencial **e** é a única da família com o benefício | pelo menos uma das duas coisas não vale (não residencial, ou outra unidade da família já tem o benefício) |

| Saída | Expressão simplificada | Orientação |
| --- | --- | --- |
| T | `CD + ABD = D(AB + C)` | indício de direito nesta unidade (100% até 80 kWh/mês) |
| U | `CD' + ABD' = D'(AB + C)` | atende a uma condição, mas D = 0: conferir com a distribuidora se a unidade é residencial e em qual conta da família o benefício pode ser aplicado |
| K | `A'C' + B'C' = (AB + C)'` | nenhuma das duas condições modeladas foi atendida: procurar o CRAS (não é negativa oficial; há hipóteses legais fora do modelo) |

## Entregáveis

- **Relatório em PDF:** [`docs/Relatorio_Computer_Science_Tarifa_Social.pdf`](docs/Relatorio_Computer_Science_Tarifa_Social.pdf). Contém problema, variáveis, regras e fontes com data de consulta, tabela-verdade, formas canônicas, álgebra com De Morgan, mapas de Karnaugh, circuitos, validação das 16 combinações, prints e instruções.
- **Prints da simulação no Logic.ly:** [`prints/`](prints/), um para cada uma das 16 combinações (`mXX_ABCD_xxxx.jpg`).
- **Instruções de execução:** seção abaixo e seção 12 do relatório.

## Como executar (simulador Logic.ly)

1. Abra <https://logic.ly/demo/>.
2. Coloque 4 *Toggle Switch* (A, B, C, D), 3 *AND*, 1 *OR*, 2 *NOT* e 3 *Light Bulb* (K, T, U).
3. Faça as ligações:
   - `AND(A, B)` e `C` vão para a `OR`; a saída da OR é **R**.
   - `NOT(R)` vai para a lâmpada **K**.
   - `AND(R, D)` vai para a lâmpada **T**.
   - `AND(R, NOT D)` vai para a lâmpada **U**.
4. Clique nas chaves (fio azul = 1) e compare a lâmpada acesa com a tabela-verdade.

A equivalência entre as expressões (tabela-verdade, forma simplificada e circuito) é uma verificação lógica; ela não comprova que as regras jurídicas estão completas ou atualizadas. O modelo cobre só os incisos I e II e o § 2º do art. 2º.

## Uso de IA (regra do enunciado)

O enunciado não permite usar IA para fazer a tabela-verdade, os mapas de Karnaugh e o circuito lógico (desconto de 4 pontos) e permite IA apenas no relatório. Neste repositório, as figuras do PDF (mapas e circuitos) são **desenhadas por um programa** (`gerar_relatorio.py`) a partir dos mintermos e agrupamentos definidos no código. **A equipe precisa conferir e declarar ao professor como a tabela-verdade, os agrupamentos de Karnaugh e o circuito foram elaborados** e estar pronta para refazê-los à mão e explicá-los. Este aviso não afirma nem nega autoria; registra o ponto que depende da equipe.

## Arquivos auxiliares

`gerar_relatorio.py` e `orientador_tsee.py` só foram usados para desenhar os mapas de Karnaugh e os circuitos do PDF e para conferir a tabela-verdade. Não fazem parte da entrega e não são necessários para executar a simulação. Para regenerar o PDF (requer Python 3 e Microsoft Edge):

```bash
python gerar_relatorio.py --pdf
```
