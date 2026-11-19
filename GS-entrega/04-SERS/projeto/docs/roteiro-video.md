# Roteiro do vídeo (até 3 minutos, YouTube não listado)

> Este arquivo é só o roteiro. **O vídeo ainda não foi gravado.** Depois de publicar como "não listado", coloque o link em `entrega_SERS.txt` e no README.

**Antes de gravar:** abra o terminal na pasta do repositório com letra grande; deixe `docs/analise.md` aberto na seção 4 (tabela de comparação); teste o áudio; ensaie com cronômetro.

| Tempo | O que mostrar | O que dizer |
| --- | --- | --- |
| 0:00–0:25 | Rosto ou título; README, seção "Público e problema" | "Somos Ryan e João. Esta é a parte de energia do Citizen Assist AI. O público são famílias de baixa renda, principalmente as que têm ou buscam a Tarifa Social. A necessidade é o banho quente: o chuveiro elétrico é o aparelho de maior potência da casa e pode fazer a família passar dos 80 kWh gratuitos da Tarifa Social." |
| 0:25–0:55 | `docs/analise.md`, seção 3 (fórmula e exemplo) | "Energia é potência vezes tempo. Um chuveiro de 5.500 watts, com 4 banhos de 8 minutos, gasta 88 kWh por mês, cerca de mil reais por ano com a tarifa do exemplo. Os valores sugeridos são estimativas e hipóteses, e cada um tem a fonte indicada." |
| 0:55–1:35 | Tabela de comparação da seção 4 | "Comparamos duas alternativas para o mesmo banho, em 12 meses. A: banho de 5 minutos, sem custo, economiza 376 reais por ano. B: aquecedor solar, uma fonte renovável, com apoio elétrico; reduz 60% da eletricidade, mas exige cerca de 3 mil reais e se paga em uns 6 anos. Juntando as duas não se soma a economia: quem já toma banho curto tem menos a economizar com o sol, e o retorno sobe para quase 11 anos." |
| 1:35–2:30 | Terminal: `python -m energia.assistente` | Responda às perguntas ao vivo (use `?` em uma delas para mostrar a origem do número). Mostre o resultado: gasto atual, tabela, recomendações, limites e fontes. Em seguida simule uma família com Tarifa Social em casa alugada e mostre que a resposta muda: o aquecedor não é indicado e a economia em reais pode ser zero. |
| 2:30–3:00 | Lista "Limites desta estimativa" na tela | "As recomendações: começar pelo banho mais curto; avaliar o aquecedor solar só com orçamento real e se puder instalar. Limitações: são estimativas, não garantias; preço e desempenho do aquecedor são hipóteses; a conta ignora bandeiras e reajustes. Fizemos testes com usuários e ajustamos…" (**fale desta parte somente se os testes tiverem sido feitos; diga o que realmente aconteceu**) |

Checklist do enunciado para o vídeo: público e necessidade ✔ · análise de consumo e comparação com a fonte renovável ✔ · demonstração das funcionalidades no assistente ✔ · recomendações e limitações ✔ · até 3 minutos · não listado.
