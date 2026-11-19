# Roteiro do vídeo SERS — até 3 minutos (YouTube, não listado)

Tema: **o banho quente da família** (chuveiro elétrico × banho mais curto × aquecedor solar).
Texto de fala: cerca de 390 palavras, para caber em 2:40 a 2:50 falando em ritmo calmo. Sobram uns 10 a 20 segundos de folga. **Ensaie com cronômetro: se passar de 3:00, corte as frases marcadas com ✂.**

O enunciado pede 4 coisas no vídeo, e cada bloco abaixo cobre uma: **(1)** público e necessidade, **(2)** análise de consumo e comparação com a fonte renovável, **(3)** demonstração no assistente, **(4)** recomendações e limitações.

---

## Antes de gravar (5 minutos)

- [ ] Terminal na pasta do repositório (`cd ...\sers-citizen-assist-ai`), **fonte grande** (Ctrl + roda do mouse) e janela limpa (`cls`).
- [ ] Teste uma vez: `python -m energia.assistente --exemplo` (tem de mostrar "Em resumo" e a tabela).
- [ ] `docs/analise.md` aberto na **seção 4** (tabela de comparação), em outra janela.
- [ ] Notificações desligadas; microfone testado; só um monitor compartilhado.
- [ ] Os dois integrantes falam? Combine quem fala cada bloco (sugestão: Ryan 1 e 2; João 3 e 4).
- [ ] Não mostre nome de pessoas da pesquisa, só P1 a P5.

---

## Bloco 1 — Público e necessidade (0:00 a 0:25)

**Na tela:** título do README (`# Citizen Assist AI — Energia em casa: o banho quente`) e a seção "Público e problema".

**Fala:**
> "Somos Ryan e João. Esta é a parte de energia do Citizen Assist AI. O público são famílias de baixa renda, principalmente as que têm ou buscam a Tarifa Social. A necessidade é o banho quente: o chuveiro elétrico é o aparelho de maior potência da casa, e pode fazer a família passar dos 80 kWh que a Tarifa Social cobre."

## Bloco 2 — Análise de consumo e comparação (0:25 a 1:20)

**Na tela (25 a 45 s):** `docs/analise.md`, seção 3 (a fórmula). Depois role até a **tabela da seção 4**.

**Fala:**
> "Energia é potência vezes tempo. Um chuveiro de 5.500 watts, com 4 banhos de 8 minutos por dia, gasta 88 quilowatts-hora por mês, cerca de 84 reais por mês ou mil reais por ano. ✂ Esses valores são estimativas, e cada um tem a fonte indicada."
>
> "Comparamos três opções para o mesmo banho, em 12 meses. **A**: reduzir o banho para 5 minutos, sem custo, economiza 376 reais por ano. **B**: aquecedor solar, a fonte renovável, com apoio elétrico; cobre 60% da energia, mas custa cerca de 3 mil reais e se paga em 6 anos. E **A mais B**: a economia não se soma. Quem já toma banho curto tem menos a economizar com o sol, e o retorno do aquecedor sobe para quase 11 anos."

**Dica de tela:** passe o cursor ou destaque a coluna **Retorno** (6,0 e 10,9 anos).

## Bloco 3 — Demonstração no assistente (1:20 a 2:25)

**Na tela:** terminal. Rode `python -m energia.assistente`.

**Roteiro da demonstração (digite devagar; "Enter" = aceitar o valor entre colchetes):**

| Pergunta do assistente | Digite |
|---|---|
| Potência do chuveiro | **`?`** (mostra de onde vem o número) e depois Enter |
| Minutos por banho | Enter |
| Banhos por dia na casa | **`2`** |
| Preço do kWh | Enter |
| Consumo do resto da casa | Enter |
| Recebe a Tarifa Social? | **`s`** |
| Para quantos minutos o banho poderia cair | Enter |
| A casa é própria ou o dono autoriza? | **`n`** (casa alugada) |
| Preço do aquecedor / fração solar | Enter, Enter |

**Fala (enquanto o resultado aparece):**
> "No assistente, a família responde sobre o banho e a conta. Aqui, uma casa alugada, com Tarifa Social e 2 banhos por dia. Primeiro, o resumo: o banho custa cerca de 42 reais por mês, e o banho mais curto economiza uns 16 reais por mês, sem gastar nada. Veja que, em casa alugada, o aquecedor solar **não é indicado agora**: precisa da autorização do proprietário. O assistente mostra a conta passo a passo, compara as opções e explica a regra da Tarifa Social."

**Na tela, nesta ordem (2 a 3 s em cada):** bloco **"Em resumo"** → **"Como a conta foi feita"** → a tabela → a recomendação **"Para quem mora de aluguel"**.

> **Se estiver estourando o tempo:** pule a explicação de "como a conta foi feita" e vá direto da tabela para as recomendações. Não responda a pergunta "simular outra situação" (digite `n`).

## Bloco 4 — Recomendações e limitações (2:25 a 3:00)

**Na tela:** role até **"O que recomendamos"** e depois **"Limites desta estimativa"**.

**Fala:**
> "As recomendações: começar pelo banho mais curto, que não custa nada, e só avaliar o aquecedor solar com orçamento real e se for possível instalar. As limitações: são estimativas, não garantias; o preço e o desempenho do aquecedor são hipóteses que precisam de orçamento; e a conta ignora bandeiras tarifárias e reajustes. [FRASE DA PESQUISA, se for usar, veja abaixo.] Obrigado!"

---

## Frase sobre os testes com usuários (opcional)

O enunciado **não** pede isso no vídeo, só no repositório. Se for citar, use **só o que estiver no `docs/testes-com-usuarios.md` publicado**, sem números inventados:

> "Testamos o assistente de forma remota com **[NÚMERO]** pessoas, e ajustamos a resposta depois dos comentários: **[AJUSTE REAL 1]** e **[AJUSTE REAL 2]**."

Preencha os colchetes só depois de confirmar qual versão da pesquisa é a oficial. Se houver dúvida, **não cite a pesquisa no vídeo**: não perde pontos.

---

## Gravação e entrega

1. Grave a tela com narração (Win + G, OBS ou outro). Resolução 1080p, áudio claro.
2. Se passar de 3 minutos, **corte antes de subir**: o YouTube não limita, mas o enunciado sim.
3. Envie ao YouTube como **"Não listado"** (não "Privado": o professor precisa abrir o link).
4. Abra o link **em outra janela sem login** para conferir que ele toca.
5. Cole o link em `entrega_SERS.txt`, **apague o aviso** de "PENDENTE" e envie só esse arquivo no Portal.

## Checklist do enunciado

- [ ] Público e necessidade energética (Bloco 1)
- [ ] Análise de consumo e comparação, incluindo a fonte renovável (Bloco 2)
- [ ] Demonstração das funcionalidades no assistente (Bloco 3)
- [ ] Principais recomendações e limitações (Bloco 4)
- [ ] Duração máxima de 3 minutos
- [ ] YouTube, **não listado**
