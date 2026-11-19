# Checklist da GS 2026.2 — Citizen Assist AI

Atualizado em 18/11/2026, à noite. Marque com `x` dentro dos colchetes conforme for terminando: `[x]`.

Integrantes: Ryan Luther Roque (RM 572993) e João Guilherme Figueiredo (RM 572697)

Prazos e formato de envio: **conferir no Portal** (não estão nos enunciados).

---

## Resumo rápido

| Disciplina | Código e documentos | GitHub | O que falta |
|---|---|---|---|
| Computer Science | pronto | idêntico à pasta (nada a subir) | conferir regra de IA; enviar no Portal |
| DSA | pronto | falta **1 arquivo** (turma no README) | demonstração; enviar no Portal |
| Arquitetura | pronto, acesso pela internet testado | faltam **3 arquivos** (2 READMEs e o relatório) | vídeo; enviar no Portal |
| SERS | pronto, pesquisa de 18/11 feita | publicado em 18/11 às 19h40 (nada a subir) | vídeo; link no `.txt`; enviar no Portal |

Todas as pastas estão em `Downloads\GS-ENTREGA`, uma pasta por matéria.

---

## Verificação feita em 18/11/2026 (código contra o enunciado)

- [x] **Computer Science:** 16 de 16 combinações iguais nas cinco representações; conferi a lógica por conta própria a partir da regra da lei
- [x] **Arquitetura:** 19 de 19 testes; as 4 situações mínimas do enunciado funcionaram num servidor temporário (3 chegadas, 2 conclusões, saída com fila vazia recusada com erro 409, estimativa atualizada)
- [x] **DSA:** 15 de 15 testes; programa rodado de ponta a ponta pelo roteiro, sem erros
- [x] **SERS:** 18 de 18 testes; roteiro do vídeo executado bloco por bloco com os números conferidos
- [ ] O professor precisa de Python 3.10 ou mais novo (está nos READMEs)

---

## Onde está cada coisa

| Disciplina | Pasta para entregar (`Downloads\GS-ENTREGA`) | GitHub |
|---|---|---|
| Computer Science | `01-Computer-Science\projeto` | https://github.com/ryanlutherroque10-bit/GS-2026-Computer-Science |
| Arquitetura | `02-Arquitetura\projeto` (roteiro do vídeo em `videos\`) | https://github.com/ryanlutherroque10-bit/GS-2026-Arquitetura |
| DSA | `03-DSA\projeto` | https://github.com/ryanlutherroque10-bit/GS-2026-DSA |
| SERS | `04-SERS\projeto` (roteiro em `ROTEIRO_VIDEO_SERS_3min.md`; arquivo do Portal em `ARQUIVO_PARA_O_PORTAL_entrega_SERS.txt`) | https://github.com/ryanlutherroque10-bit/GS-2026-SERS |

**Atenção com os remotos antigos:** as pastas de trabalho em `Downloads\GS` ainda apontam para nomes de repositório que não existem mais (`computer-science-GS2`, `GS-Citizen-AI`, `arquitetura-GS2`, `sers-citizen-assist-ai`). Para subir, use sempre um **clone novo** dos repositórios `GS-2026-*`. Não use a cópia antiga `C:\Users\ryanl\arquitetura-GS2`.

Os enunciados estão na pasta `enunciado` de cada disciplina.

---

## 1. Computer Science

### Feito
- [x] 4 variáveis, 3 saídas, tabela-verdade com as 16 combinações
- [x] Forma canônica, simplificação por álgebra, De Morgan, mapas de Karnaugh
- [x] Circuito original e simplificado, com comparação de portas (15 para 6)
- [x] Simulação no Logic.ly com 16 prints (pasta `prints`)
- [x] Relatório em PDF, fontes com data de consulta, limitações e instruções de execução
- [x] Publicado no GitHub, idêntico à pasta

### Falta
- [ ] **Regra de IA:** o enunciado tira 4 pontos se a tabela-verdade, o Karnaugh ou o circuito forem feitos com IA (a IA só pode fazer o relatório). Conferir como foram feitos e saber refazer à mão
- [ ] Abrir o PDF e ler do começo ao fim
- [ ] Ryan e João: saber explicar A, B, C, D e as saídas T, U, K
- [ ] Enviar no Portal: PDF + 16 prints + instruções

Não precisa de vídeo nem de GitHub (o enunciado não exige).

---

## 2. DSA

### Feito
- [x] Lista encadeada própria (classe `No`), cadastro, consulta, pesquisa, atualização, exclusão
- [x] Insertion Sort religando os nós, indicador por categoria, menu no terminal
- [x] Trata opção inválida, ID repetido e lista vazia
- [x] Documentação técnica, análise Big-O, evidências de testes
- [x] Turma corrigida de 1CCR para **1CC-FEV** no README (só na pasta `GS-ENTREGA`)
- [x] Script `demo_dsa.py` para a demonstração (restaura o CSV no fim; **não vai para o GitHub**)

### Falta
- [ ] **Subir ao GitHub 1 arquivo:** `06-dsa-python/README.md`
- [ ] Fazer a demonstração prática (roteiro em `06-dsa-python\testes\PLANO_DE_TESTES.md`), ao vivo ou gravada, como o professor orientar
- [ ] Enviar no Portal no formato pedido

Para rodar: `cd 06-dsa-python` e `python main.py`. Faça cópia da pasta antes de demonstrar: cadastrar, excluir e ordenar alteram o CSV.

Não precisa de vídeo (o enunciado pede demonstração prática).

---

## 3. Arquitetura

### Feito
- [x] Servidor + painel web + terminal de atendimento usando a mesma fila
- [x] Chegada e conclusão, bloqueio de fila negativa, eventos com horário
- [x] Estimativa por média histórica comparada com regressão linear (dados simulados identificados)
- [x] Diagrama, relatório técnico, plano de testes, roteiro do vídeo
- [x] Acesso pela internet testado em 18/11/2026 (túnel Cloudflare, celular em dados móveis), registrado na seção 7.5 do relatório
- [x] Simulação do Pico W no Wokwi: https://wokwi.com/projects/480879311582717953
- [x] Testes: 19 de 19 passam

### Falta
- [ ] **Subir ao GitHub 3 arquivos:** `README.md`, `fila-virtual-citizen-assist/README.md` e `fila-virtual-citizen-assist/docs/relatorio-tecnico.md`
- [ ] **Vídeo de até 5 minutos** — roteiro em `02-Arquitetura\videos\ROTEIRO_VIDEO_ARQUITETURA_5min.md`
- [ ] Abrir o link do Wokwi, clicar em ▶ e conferir o potenciômetro e os LEDs
- [ ] Confirmar que o João é integrante deste trabalho
- [ ] Enviar no Portal: link do repositório, relatório, diagrama e link do vídeo

Para rodar: `cd fila-virtual-citizen-assist`, `python app.py` e abrir http://127.0.0.1:8000. Em outra janela: `python tools/terminal_simulado.py`.

---

## 4. SERS

### Feito
- [x] Tema: o banho quente da família (chuveiro elétrico × banho mais curto × aquecedor solar)
- [x] Cálculo de consumo, custo (com Tarifa Social) e emissões; comparação sem contar economia em dobro
- [x] Assistente no terminal com resumo, "como a conta foi feita", comparação de potências, aviso para quem mora de aluguel, recomendações, limites e fontes
- [x] Análise (`docs\analise.md`) e referências (`docs\referencias.md`)
- [x] Pesquisa com 5 pessoas, remota, em 18/11/2026, aplicada por Ryan (clareza 4,2/5; utilidade 4,6/5), registrada em `docs\testes-com-usuarios.md` e `evidencias\respostas-SERS-5-pessoas.txt`
- [x] Ajustes no assistente a partir da pesquisa
- [x] Publicado no GitHub em 18/11 às 19h40; 18 de 18 testes passam, com GitHub Actions
- [x] Roteiro do vídeo reescrito e executado passo a passo

### Falta
- [ ] **Vídeo de até 3 minutos** no YouTube, como "não listado" — roteiro em `04-SERS\ROTEIRO_VIDEO_SERS_3min.md`
- [ ] Colocar o link do vídeo no `entrega_SERS.txt` e **apagar o aviso** de "PENDENTE" (e depois fazer o commit no GitHub)
- [ ] Abrir os links de `docs\referencias.md` e conferir os valores
- [ ] Se possível, trocar as hipóteses do aquecedor solar (preço, desempenho) por um orçamento real
- [ ] Enviar no Portal: **somente** o arquivo `.txt` (nomes e RMs, link do GitHub, link do YouTube)

Para rodar: `python -m energia.assistente`. Se for citar a pesquisa no vídeo, diga só o que está em `docs\testes-com-usuarios.md`.

---

## Vídeos (gravação pendente)

| Vídeo | Duração máxima | Roteiro | Situação |
|---|---|---|---|
| SERS | 3 minutos, YouTube "não listado" | `04-SERS\ROTEIRO_VIDEO_SERS_3min.md` | roteiro pronto e testado; **falta gravar** |
| Arquitetura | 5 minutos | `02-Arquitetura\videos\ROTEIRO_VIDEO_ARQUITETURA_5min.md` | roteiro pronto; **falta gravar** |

- [ ] Gravar e publicar o vídeo do SERS (e colar o link no `.txt`)
- [ ] Gravar e publicar o vídeo de Arquitetura (e colocar o link no relatório e no README)

DSA e Computer Science não pedem vídeo.

---

## 5. Geral

- [ ] Conferir prazo e formato de cada entrega no Portal
- [ ] Combinar com o João quem grava e quem apresenta cada parte
- [x] Linha de coautoria do Claude removida dos commits em 16/11/2026 (os prompts mandam não adicioná-la de novo)
- [ ] Depois de qualquer mudança nos arquivos, publicar de novo no GitHub

## Ordem sugerida

1. Subir ao GitHub os 3 arquivos de Arquitetura e o README do DSA (um clone novo de cada `GS-2026-*`)
2. Gravar os vídeos do SERS (3 min) e da Arquitetura (5 min)
3. Colocar o link do vídeo no `.txt` do SERS e fazer o commit
4. Conferir o Computer Science (regra de IA) e preparar a demonstração do DSA
5. Enviar tudo no Portal

