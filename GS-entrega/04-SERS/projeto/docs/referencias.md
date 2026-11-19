# Referências

Fontes localizadas por busca na internet em **16/11/2026**. Os valores usados foram os retornados pela busca; **a equipe deve abrir cada endereço, confirmar o trecho citado e atualizar a data de consulta antes da entrega**. Onde está escrito "endereço a conferir", a página oficial não foi aberta diretamente.

## Legislação

1. BRASIL. **Lei nº 12.212, de 20 de janeiro de 2010.** Dispõe sobre a Tarifa Social de Energia Elétrica. Texto compilado. Presidência da República. <https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2010/lei/l12212.htm>. Uso: desconto de 100% na parcela do consumo até 80 kWh/mês e 0% acima (art. 1º, I e II).
2. BRASIL. **Lei nº 15.235, de 8 de outubro de 2025** (conversão da Medida Provisória nº 1.300/2025). Câmara dos Deputados, Legislação Informatizada. <https://www2.camara.leg.br/legin/fed/lei/2025/lei-15235-8-outubro-2025-798121-norma-pl.html>. Uso: redação atual do art. 1º da Lei nº 12.212/2010.
3. ANEEL. **Resolução Normativa nº 1.147, de 9 de dezembro de 2025**, que regulamenta a aplicação da Tarifa Social. Não foi lida para este trabalho; citada para a equipe conferir se há regra adicional aplicável.

## Consumo do chuveiro elétrico

4. IDEC — Instituto de Defesa de Consumidores. **Saiba quais são os vilões de consumo de energia no inverno.** <https://idec.org.br/consultas/dicas-e-direitos/saiba-quais-so-os-viloes-de-consumo-de-energia-no-inverno>. Uso: o chuveiro elétrico como principal consumo e exemplos de potência e tempo de uso.
5. VALOR FINAL. **Tabela de potência dos aparelhos.** <https://valorfinal.com.br/tabela-potencia-aparelhos>. Uso: faixa de potência de chuveiros (4.400 a 7.700 W) e exemplo de 5.500 W por 30 minutos diários = 82,5 kWh/mês (o cálculo é reproduzido nos testes). Fonte secundária, não oficial: a potência que vale é a da etiqueta do Programa Brasileiro de Etiquetagem (Inmetro) no produto.

## Emissões da eletricidade

6. MCTI — Ministério da Ciência, Tecnologia e Inovação. **Fatores de emissão de CO2 do Sistema Interligado Nacional (fator médio, para inventários).** Publicação oficial na plataforma SIRENE (endereço a conferir: <https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao>). Uso: fator médio anual.
7. EIXOS. **Brasil tem menor taxa de emissão de carbono na geração elétrica em onze anos.** <https://eixos.com.br/energia-eletrica/brasil-tem-menor-taxa-de-emissao-de-carbono-na-geracao-eletrica-em-onze-anos/>. Uso: valor de 2023, 38,5 kg de CO2 por MWh (0,0385 kg/kWh), atribuído ao MCTI.
8. SAGAZ, Julia. **Sistema Brasileiro de Comércio de Emissões** (apresentação, ABRAPCH, 2025). <https://abrapch.org.br/wp-content/uploads/2025/03/JULIA_SAGAZ_Sistema_Brasileiro_de_Comercio_de_Emissoes.pdf>. Uso: média do fator de emissão do SIN de 2015 a 2024, cerca de 77 g CO2/kWh, usada na análise de sensibilidade.

Observação: a partir de janeiro de 2025 o MCTI mudou a base de dados do cálculo; valores de 2025 não são diretamente comparáveis com a série anterior. O valor oficial de 2024 não foi localizado.

## Aquecimento solar de água

9. IDEC. **Economia com aquecedor solar.** <https://idec.org.br/dicas-e-direitos/economia-com-aquecedor-solar>. Uso: contexto sobre o aquecedor solar como complemento ao chuveiro elétrico.
10. ABNT. **NBR 15569 — Sistema de aquecimento solar de água em circuito direto: projeto e instalação.** Uso: referência para o dimensionamento que o instalador deve fazer (norma não consultada; citada como orientação).

**Não foi encontrada fonte pública verificável** para o preço médio de um sistema de cerca de 200 litros, para a fração solar típica por cidade, para o custo de manutenção e para a vida útil. Esses quatro parâmetros estão marcados como **hipótese** em `dados/premissas.json` e na análise, e o assistente pede o orçamento real ao usuário.

## Tarifa de energia

11. ANEEL. **Ranking das tarifas residenciais.** Portal da ANEEL (endereço a conferir: <https://portalrelatorios.aneel.gov.br/luznatarifa/rankingtarifas>). Uso: comparação opcional; o valor usado no cálculo é sempre o da fatura do usuário. O padrão de R$ 0,95/kWh é uma hipótese ilustrativa.
