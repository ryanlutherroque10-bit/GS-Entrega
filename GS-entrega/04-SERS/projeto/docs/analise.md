# Análise energética — o banho quente no Citizen Assist AI

## 1. Contexto

**Público.** Famílias de baixa renda atendidas pelo Citizen Assist AI, em especial as que recebem ou procuram a Tarifa Social de Energia Elétrica. O recorte é coerente com os outros módulos do projeto, que orientam sobre a Tarifa Social e sobre serviços ao cidadão.

**Necessidade energética.** Aquecer a água do banho da família. Escolhemos essa necessidade por três motivos:

1. O chuveiro elétrico é o aparelho de maior potência de uma casa comum (4.400 a 7.700 W), então poucos minutos de uso pesam na conta.
2. A Tarifa Social dá desconto de 100% só na parcela do consumo até 80 kWh por mês. No cenário de referência, o banho sozinho consome 88 kWh: é ele que decide se a família passa ou não do limite.
3. É uma necessidade que tem alternativa de economia sem custo e alternativa com fonte renovável (solar térmica), o que permite comparar opções para **a mesma necessidade**.

**Como a orientação contribui.** A família deixa de ouvir "economize energia" de forma genérica e passa a ver, com os próprios números, quanto o banho custa, quanto cada alternativa economiza e em que condições cada uma vale a pena.

## 2. Dados de consumo e premissas

Todos os parâmetros estão em [`dados/premissas.json`](../dados/premissas.json), cada um com valor, unidade, tipo, justificativa e fonte. Resumo:

| Parâmetro | Valor padrão | Unidade | Tipo | Origem |
| --- | --- | --- | --- | --- |
| Potência do chuveiro | 5.500 | W | estimado | faixa de guias públicos; o real está na etiqueta do aparelho |
| Duração do banho | 8 | min | estimado | exemplos públicos usam 30 a 32 min de chuveiro por dia na casa |
| Banhos por dia | 4 | banhos | hipótese | família de 4 pessoas |
| Tarifa | 0,95 | R$/kWh | hipótese | valor ilustrativo; o real é o total da fatura ÷ kWh |
| Consumo do resto da casa | 100 | kWh/mês | hipótese | só influencia o cálculo com Tarifa Social |
| Limite da Tarifa Social | 80 | kWh/mês | dado público | Lei nº 12.212/2010, art. 1º (redação da Lei nº 15.235/2025) |
| Banho na alternativa A | 5 | min | hipótese | meta de uso consciente |
| Fração solar | 0,6 | — | hipótese | parte do banho aquecida pelo sol; confirmar com o instalador |
| Investimento no aquecedor solar | 3.000 | R$ | hipótese | sem preço médio público verificável; usar orçamento |
| Manutenção do aquecedor | 100 | R$/ano | hipótese | limpeza e revisão |
| Vida útil do aquecedor | 15 | anos | hipótese | confirmar com o fabricante |
| Fator de emissão da eletricidade | 0,0385 | kg CO2/kWh | dado público | média do Sistema Interligado Nacional em 2023 (MCTI) |

**Período de referência:** 12 meses, com mês de 30 dias. Para somar investimento e gastos, horizonte de 10 anos com tarifa constante.

**Dados estimados e hipóteses não são medições.** Nenhuma casa foi medida neste trabalho. O assistente pede os valores reais ao usuário e só usa os padrões quando a pessoa não sabe responder.

## 3. Fórmulas

Potência é a taxa de uso de energia (W). Energia é potência multiplicada pelo tempo (kWh).

```
consumo do banho (kWh/mês) = potência (W) ÷ 1000 × minutos por banho ÷ 60 × banhos por dia × 30

fatura (R$/mês)            = consumo total da casa × tarifa                      (sem Tarifa Social)
                           = máx(0, consumo total − 80 kWh) × tarifa             (com Tarifa Social)

custo do banho (R$/ano)    = [fatura com o banho − fatura sem o banho] × 12

alternativa A (kWh/mês)    = mesma fórmula do consumo, com o tempo (ou a potência) reduzido
alternativa B (kWh/mês)    = consumo de referência × (1 − fração solar)
A + B (kWh/mês)            = consumo de A × (1 − fração solar)

economia (R$/ano)          = custo de referência − custo da alternativa − manutenção anual
retorno simples (anos)     = investimento ÷ economia anual trazida pelo investimento
custo total em N anos      = investimento + (custo de energia + manutenção) × N
emissões (kg CO2/ano)      = kWh por ano × fator de emissão da rede
```

O código valida cada entrada (tipo, número finito e faixa) e recusa valores incoerentes, como banho reduzido maior que o atual ou fração solar acima de 0,95.

### Exemplo resolvido (cenário de referência)

- Referência: 5.500 ÷ 1000 × 8 ÷ 60 × 4 × 30 = **88 kWh/mês**; 88 × 0,95 × 12 = **R$ 1.003,20/ano**; 88 × 12 × 0,0385 = **40,7 kg CO2/ano**.
- A (5 min): 5,5 × 5 ÷ 60 × 4 × 30 = **55 kWh/mês**; R$ 627,00/ano; economia de **R$ 376,20/ano**.
- B (fração 0,6): 88 × 0,4 = **35,2 kWh/mês**; R$ 401,28/ano; economia de 601,92 − 100 de manutenção = **R$ 501,92/ano**; retorno de 3.000 ÷ 501,92 = **6,0 anos**.
- A + B: 55 × 0,4 = **22 kWh/mês**; economia total de R$ 652,40/ano.

## 4. Comparação das alternativas

Mesma necessidade (banho quente da mesma família), mesmo período (12 meses):

| Critério | Referência: chuveiro elétrico | A — banho mais curto | B — aquecedor solar com apoio elétrico |
| --- | --- | --- | --- |
| Tipo | situação atual | economia (uso consciente) | fornecimento por fonte renovável (solar térmica) |
| Eletricidade | 88 kWh/mês | 55 kWh/mês (−37,5%) | 35,2 kWh/mês (−60%) |
| Custo de energia | R$ 1.003/ano | R$ 627/ano | R$ 401/ano |
| Investimento | nenhum | nenhum | R$ 3.000 (hipótese) + R$ 100/ano de manutenção |
| Economia líquida | — | R$ 376/ano | R$ 502/ano |
| Retorno do investimento | — | imediato | 6,0 anos |
| Custo total em 10 anos | R$ 10.032 | R$ 6.270 | R$ 8.013 |
| Emissões (eletricidade) | 40,7 kg CO2/ano | 25,4 kg CO2/ano | 16,3 kg CO2/ano |
| Viabilidade | — | depende só de hábito; a família precisa conseguir manter | exige imóvel próprio ou autorização, telhado ou laje com sol, estrutura que suporte o reservatório e dinheiro (ou financiamento) para o investimento |
| Outros impactos | — | também economiza água | usa energia do sol no local; fabricação e transporte do equipamento têm impacto não calculado aqui |

### Combinar A e B sem contar a economia duas vezes

Somar as economias de A (396 kWh/ano) e de B (634 kWh/ano) daria 1.030 kWh/ano, mas isso está errado: o aquecedor solar só pode economizar a energia que o banho ainda gasta. Com o banho mais curto, o cálculo correto é 55 × (1 − 0,6) = 22 kWh/mês, ou seja, 792 kWh evitados por ano.

Consequência para a decisão: se a família já adotou A, o aquecedor passa a render só R$ 276/ano além de A (652,40 − 376,20), e o retorno dele sobe de 6,0 para **10,9 anos**. Em 10 anos, o custo total de A sozinha (R$ 6.270) fica menor que o de A + B (R$ 6.508).

### Análise de sensibilidade

Como preço e fração solar são hipóteses, variamos um parâmetro por vez (os demais ficam no padrão):

| Variação | Economia de B (R$/ano) | Retorno de B | Custo de B em 10 anos | Observação |
| --- | ---: | ---: | ---: | --- |
| Padrão | 502 | 6,0 anos | R$ 8.013 | |
| Fração solar 0,4 | 301 | 10,0 anos | R$ 10.019 | empata com a referência (R$ 10.032) |
| Fração solar 0,8 | 703 | 4,3 anos | R$ 6.006 | fica melhor que A sozinha |
| Investimento de R$ 2.000 | 502 | 4,0 anos | R$ 7.013 | |
| Investimento de R$ 5.000 | 502 | 10,0 anos | R$ 10.013 | empata com a referência |
| Tarifa de R$ 0,75/kWh | 375 | 8,0 anos | R$ 7.168 | |
| Tarifa de R$ 1,15/kWh | 629 | 4,8 anos | R$ 8.858 | |
| Fator de emissão 0,077 kg/kWh (média de 2015 a 2024) | 502 | 6,0 anos | R$ 8.013 | emissões dobram: referência 81,3 kg; B 32,5 kg |
| Tarifa Social, casa de baixo consumo (30 kWh de outros usos, 2 banhos) | −100 | não se paga | R$ 4.000 | consumo total de 74 kWh fica dentro dos 80 kWh gratuitos |

A conclusão sobre A (primeira medida, sem custo) não muda em nenhuma variação. A conclusão sobre B muda bastante: por isso o assistente pede o orçamento e a fração solar ao usuário e não trata o retorno como garantido.

## 5. Justificativa das recomendações

1. **A primeiro.** Custo zero, efeito imediato, sem depender de imóvel ou de crédito. Reduz 37,5% da energia do banho no cenário de referência.
2. **B quando as condições existem.** É a opção que mais reduz eletricidade e emissões e usa fonte renovável, mas só é recomendada quando a família pode instalar, o retorno calculado cabe na vida útil do equipamento e o valor veio de orçamento real. Caso contrário, o assistente diz que não é indicada ou que não compensa financeiramente.
3. **Tarifa Social.** Para quem consome até 80 kWh por mês, a economia em reais é zero, porque a energia já tem desconto de 100%. O assistente avisa isso em vez de prometer economia. Economizar ainda importa para não ultrapassar o limite e pelo impacto ambiental. Para essas famílias, investir R$ 3.000 em aquecedor solar não se paga.
4. **Impacto ambiental.** A eletricidade brasileira emite pouco CO2 por kWh, então a redução de emissões é modesta (cerca de 15 a 24 kg por ano no cenário de referência). O ganho ambiental mais relevante é aliviar a rede no horário de pico, entre o fim da tarde e o começo da noite, quando muitos chuveiros ligam ao mesmo tempo; esse efeito não foi calculado.

## 6. Integração ao assistente

`energia/assistente.py` é a parte do Citizen Assist AI que conversa com o cidadão sobre energia. Cada resposta do assistente vem de um cálculo desta análise:

| O que o assistente diz | De onde vem |
| --- | --- |
| "Hoje o banho gasta cerca de 88 kWh por mês…" | `consumo_mensal_kwh` (seção 3) |
| Tabela com kWh, custo, investimento, economia, retorno, CO2 e custo em 10 anos | `comparar` (seção 4) |
| "Comece pela alternativa A…" / "O aquecedor solar se pagaria em…" / "não é indicado no seu caso" | `recomendar` (seção 5) |
| "Limites desta estimativa" | lista `AVISOS` (seção 7) |
| "De onde vêm os números" e a ajuda `?` | `dados/premissas.json` e [referencias.md](referencias.md) |

Exemplos de execução real estão em [`evidencias/saida-exemplo.txt`](../evidencias/saida-exemplo.txt) e [`evidencias/saida-conversa.txt`](../evidencias/saida-conversa.txt). O módulo é independente dos módulos das outras disciplinas (pode ser testado separadamente) e usa a mesma regra da Tarifa Social do módulo de Computer Science.

## 7. Condições e limitações

- **Estimativas, não garantias.** Economia, geração solar e retorno dependem de uso real, clima, tarifa e equipamento.
- **Hipóteses do aquecedor solar.** Preço, fração solar, manutenção e vida útil não vêm de dado público verificado; devem ser trocados por orçamentos e pelo dimensionamento do instalador.
- **Conta de luz simplificada.** Sem bandeiras tarifárias, iluminação pública, custo de disponibilidade, variação de impostos, reajustes ou juros. O retorno é simples, sem valor do dinheiro no tempo.
- **Quando a recomendação B não é adequada:** imóvel alugado sem autorização, telhado sombreado ou sem estrutura, família dentro do limite gratuito da Tarifa Social, orçamento alto para o consumo da casa, retorno maior que a vida útil.
- **Quando a recomendação A não é adequada como está:** pessoas com necessidades de saúde ou cuidado que exigem banhos mais longos; a meta deve ser ajustada pela família.
- **Emissões:** só a eletricidade da rede; o fator muda a cada ano.
- **Segurança:** instalação elétrica e hidráulica só com profissional habilitado.
- **Testes com usuários:** feitos em 18/11/2026, de forma remota, com 5 pessoas (P1 a P5). Todas entenderam as orientações principais; a clareza média foi 4,2/5 e a utilidade 4,6/5. Pediram mais destaque ao gasto anual e ao retorno, cálculos mais simples, orientação para quem mora de aluguel e comparação de potências; esses ajustes foram feitos no assistente. A amostra é pequena e não representa toda a população (ver [testes-com-usuarios.md](testes-com-usuarios.md)).
