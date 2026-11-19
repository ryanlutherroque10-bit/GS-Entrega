# Citizen Assist AI — Energia em casa: o banho quente

Global Solution 2026.2 · Soluções em Energias Renováveis e Sustentáveis (SERS) · Ciência da Computação, 1º ano

**Integrantes:** Ryan Luther Roque (RM 572993) e João Guilherme Figueiredo (RM 572697)

Contribuição de SERS ao assistente digital Citizen Assist AI: um assistente de terminal que calcula quanto a família gasta de energia com o banho quente e compara, com números, duas formas de gastar menos, uma delas com fonte renovável.

> Protótipo educacional. Não é canal oficial, não guarda o que é digitado e apresenta **estimativas**, não garantias de economia.

## Público e problema

- **Público:** famílias de baixa renda atendidas pelo Citizen Assist AI, em especial as que recebem ou buscam a Tarifa Social de Energia Elétrica (tema dos módulos de Computer Science e DSA do mesmo projeto).
- **Necessidade energética:** aquecer a água do banho. O chuveiro elétrico é o aparelho de maior potência da casa (4.400 a 7.700 W) e, para quem tem Tarifa Social, pode ser o que faz o consumo passar dos 80 kWh mensais com desconto de 100%.
- **Como a orientação ajuda:** a família informa cinco números simples (potência, minutos, banhos, preço do kWh, consumo do resto da casa) e recebe o gasto atual, a comparação das alternativas e uma recomendação com as condições em que ela vale.

## Funcionalidades de energia

| Funcionalidade | Onde |
| --- | --- |
| Consumo do banho em kWh/mês a partir de potência e tempo, com validação de unidades e faixas | `energia/calculos.py` (`consumo_mensal_kwh`) |
| Custo na conta, com a regra da Tarifa Social (100% de desconto até 80 kWh/mês) | `fatura_mensal` |
| Comparação, para a mesma família e 12 meses: **referência** (chuveiro elétrico) × **A — economia** (banho mais curto) × **B — renovável** (aquecedor solar térmico com apoio elétrico) × **A + B** sem dupla contagem | `comparar` |
| Custo, investimento, retorno, custo total em 10 anos e emissões de CO2 de cada opção | `Cenario` |
| Recomendações em linguagem simples, que mudam conforme o caso (casa alugada, investimento que não se paga, Tarifa Social) | `recomendar` |
| Conversa no terminal com valores sugeridos, ajuda (`?`) que mostra a origem de cada número, limites e fontes | `energia/assistente.py` |

## Como executar

Requer Python 3.10 ou superior. Não usa bibliotecas externas.

```bash
python -m energia.assistente            # conversa interativa
python -m energia.assistente --exemplo  # cenário de referência documentado
```

Em cada pergunta, Enter aceita o valor entre colchetes, `?` explica de onde ele vem e `sair` encerra.

## Como testar

```bash
python -m unittest discover -s tests -v
```

O conjunto atual tem 18 testes técnicos (fórmulas, cenário documentado, Tarifa Social, limites, entradas inválidas, conversa, resumo e orientações para imóvel alugado). Os **18 testes passaram** com Python 3.14.4 no [GitHub Actions](https://github.com/ryanlutherroque10-bit/GS-2026-SERS/actions/runs/44413788371), que também executou o cenário de exemplo. [`evidencias/saida-testes.txt`](evidencias/saida-testes.txt) registra a execução anterior de 17 testes.

## Resultado do cenário de referência

Família de 4 pessoas, chuveiro de 5.500 W, banhos de 8 minutos, R$ 0,95/kWh (valores sugeridos; ver premissas):

| Opção | kWh/mês | Energia/ano | Investimento | Economia/ano | Retorno | CO2/ano | Custo em 10 anos |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Referência: chuveiro elétrico | 88,0 | R$ 1.003 | — | — | — | 40,7 kg | R$ 10.032 |
| A — banho de 5 min | 55,0 | R$ 627 | R$ 0 | R$ 376 | imediato | 25,4 kg | R$ 6.270 |
| B — aquecedor solar (fração solar 0,6) | 35,2 | R$ 401 | R$ 3.000 | R$ 502 | 6,0 anos | 16,3 kg | R$ 8.013 |
| A + B | 22,0 | R$ 251 | R$ 3.000 | R$ 652 | 10,9 anos* | 10,2 kg | R$ 6.508 |

\* Retorno do aquecedor considerando só o que ele economiza além de A.

**Leitura:** a alternativa A é a primeira recomendação, por não ter custo. O aquecedor solar é o que mais reduz a eletricidade e as emissões, mas depende de investimento, de poder instalar e de hipóteses (preço e fração solar) que mudam muito o resultado. A análise completa, com fórmulas, sensibilidade e justificativas, está em [`docs/analise.md`](docs/analise.md).

## Organização do repositório

```
energia/calculos.py        fórmulas, validação, comparação e recomendações
energia/assistente.py      interface de conversa no terminal
dados/premissas.json       cada parâmetro com valor, unidade, tipo (dado público, estimado ou hipótese), justificativa e fonte
docs/analise.md            contexto, dados, cálculos, comparação, justificativas e limitações
docs/referencias.md        fontes com endereço e data de consulta
docs/testes-com-usuarios.md  roteiro, resultados e ajustes dos testes com usuários
docs/roteiro-video.md      roteiro do vídeo de até 3 minutos
tests/test_energia.py      testes técnicos
evidencias/                saídas reais dos testes e do assistente
entrega_SERS.txt           arquivo de entrega do Portal (ainda com pendência)
```

## Situação da entrega

| Item do enunciado | Situação em 18/11/2026 |
| --- | --- |
| Contexto, análise de consumo, comparação, integração ao assistente, referências e limitações | feito (código, dados e documentação neste repositório) |
| Testes técnicos | 18/18 aprovados no GitHub Actions; cenário de exemplo executado |
| Testes com usuários | feito em 18/11/2026, de forma remota, com 5 pessoas (clareza média 4,2/5; utilidade média 4,6/5). Resultados e ajustes em `docs/testes-com-usuarios.md` |
| **Vídeo de até 3 minutos no YouTube (não listado)** | **pendente da equipe.** Roteiro em `docs/roteiro-video.md` |
| **Arquivo `.txt` do Portal** | **incompleto:** falta o link do vídeo |
| Conferência das fontes pela equipe | pendente: abrir cada link de `docs/referencias.md` e confirmar os valores |

## Limitações

- Preço, fração solar, manutenção e vida útil do aquecedor solar são **hipóteses**, não dados medidos. O usuário deve trocá-las por orçamentos reais.
- A tarifa é informada pelo usuário e mantida constante; bandeiras, iluminação pública, reajustes e juros não entram na conta.
- A fração solar real varia com a cidade, a estação, o tamanho do sistema e o horário dos banhos.
- As emissões consideram só a eletricidade da rede; fabricação e transporte dos equipamentos ficam de fora.
- O protótipo não substitui a distribuidora, o CRAS nem um profissional habilitado.

## Uso de IA

Este trabalho foi desenvolvido com apoio de IA generativa (código, textos e busca das fontes). Conforme o enunciado, a equipe é responsável por verificar dados, cálculos, referências e recomendações e por saber explicar as decisões adotadas.
