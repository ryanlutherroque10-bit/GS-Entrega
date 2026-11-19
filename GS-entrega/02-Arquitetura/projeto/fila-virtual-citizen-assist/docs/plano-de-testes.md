# Plano de testes e evidências

Os quatro cenários mínimos do enunciado (seção 6) foram executados em quatro frentes, que não devem ser confundidas:

- **API (testes automatizados)** — reexecutados em 18/11/2026: 22/22 aprovados (`docs/evidencias/saida-testes.txt`).
- **Terminal em rede → servidor → painel** — executado em 16/11/2026 (`docs/evidencias/demonstracao-terminal-painel.txt`).
- **Painel web no navegador** — registro manual da equipe de 12/11/2026 (não repetido em 16/11).
- **Firmware do Pico W no Wokwi** — registro da equipe de 12/11/2026 (não repetido em 16/11). É um experimento autônomo: sua fila não é a do servidor.

## Cenários mínimos

| Cenário | Ação | Resultado esperado | Evidência obtida |
| --- | --- | --- | --- |
| (1) Chegada de novos cidadãos | 3 toques no botão verde (Pico) / 4 cliques em **Registrar chegada** (painel) | fila cresce 1 a 1, em ordem de chegada, cada evento com horário | Pico: `chegada;1`, `chegada;2`, `chegada;3` com data e hora. Painel: fila 0 → 4, convencional 28,9 min, IA 30,7 min. Teste `test_1` ✔ |
| (2) Conclusão de atendimentos | botão azul com o potenciômetro em 7,0 min / **Concluir atendimento** com 10 min | a primeira pessoa sai (FIFO), concluídos +1, espera medida e estimativas atualizadas | Pico: `conclusao;pessoa=1;espera=0.0`, `pessoa=2;espera=7.0`, `pessoa=3;espera=14.0`. Painel: fila 4 → 3 → 2, concluídos 0 → 1 → 2. Teste `test_2` ✔ |
| (3) Tentativa de saída com fila vazia | concluir sem ninguém na fila | operação recusada; fila continua 0; concluídos não mudam | Pico: LED vermelho, display `! FILA VAZIA`, log `rejeitado;conclusao com fila vazia`. Painel: mensagem "A fila está vazia…", contador de recusadas = 1. API: HTTP 409. Teste `test_3` ✔ |
| (4) Atualização da estimativa de espera | registrar chegadas e concluir atendimentos com durações diferentes | convencional = fila × média; IA recalculada; modelo aprende com as observações | Painel: média 7,2 → 10,0 min após atendimentos de 10 min; base 60 simulados + 2 observados. Pico: modelo de a = −0,100/b = 1,065 para a = −0,121/b = 1,066 (n = 62). Teste `test_4` ✔ |

## Verificações adicionais

| Verificação | Resultado |
| --- | --- |
| Duração 0, −5, 241 ou texto | HTTP 400; fila inalterada (`test_duracao_invalida_e_rejeitada`) ✔ |
| JSON malformado / rota inexistente | HTTP 400 / 404 ✔ |
| Fila cheia | 201ª chegada recusada no servidor (`test_capacidade_maxima`); no Pico, a pessoa 32 entrou e a 33ª foi recusada (`rejeitado;capacidade maxima`) ✔ |
| Toques repetidos (repique do botão) | filtro de 200 ms na interrupção ✔ |
| Persistência | após reiniciar o servidor, fila e eventos continuam (`test_estado_sobrevive_reinicio_do_servidor`) ✔ |
| Exportação de eventos | `GET /api/events.csv` gera CSV com data/hora, tipo, fila e origem ✔ |
| Terminal e painel na mesma fila | `tools/terminal_simulado.py` registra chegadas; `GET /api/state` mostra os eventos com origem `terminal`; ação do painel muda a leitura do terminal (`test_acao_no_terminal_aparece_no_painel`, evidência de 16/11) ✔ |
| Reenvio após falha de rede | mesmo `event_id` não é contado duas vezes; servidor inacessível → evento não registrado e operador avisado (3 testes) ✔ |
| Código do operador | com `FILA_TOKEN`, alterações sem o código → HTTP 401; consulta continua pública (`test_codigo_do_operador_protege_alteracoes`) ✔ |
| Acesso pela internet | **pendente da equipe**: preparado (README), ainda não executado nem verificado fora da rede local |
| Duas abas abertas | cada aba consulta `GET /api/state` a cada 3 s e mostra as mudanças feitas na outra (mostrar no vídeo) |
| Desempenho da API | `GET /api/state` em 0,59 ms com 560 registros de treinamento (antes da otimização: 278 ms) ✔ |

## Como repetir

```bash
cd fila-virtual-citizen-assist
python -m unittest discover -s tests -v
```

Para o terminal físico, siga [firmware-pico-w/README.md](../firmware-pico-w/README.md). O log da simulação aparece no monitor serial do Wokwi.

## Registro da execução

- **12/11/2026** — Python 3.14.7 no Windows 11; navegador Chromium; Wokwi com Raspberry Pi Pico W e MicroPython v1.28.0. 12/12 testes automatizados aprovados; os quatro cenários reproduzidos manualmente no painel e no Pico W simulado. Registro feito pela equipe (Ryan Luther Roque e João Guilherme Figueiredo); o registro original não identifica qual integrante executou cada passo.
- **18/11/2026** — Python 3.14 no Windows 11. 22/22 testes automatizados aprovados, incluindo 3 novos (reenvio de operação recusada, Content-Length inválido e código do operador com acento).
- **16/11/2026** — Python 3.14 no Windows 11. 19/19 testes automatizados aprovados e demonstração terminal → servidor → painel por linha de comando. Execução automatizada feita com apoio de assistente de IA a pedido da equipe; saídas guardadas em `docs/evidencias/`. O painel no navegador e o Wokwi não foram reexecutados nessa data.
- **16/11/2026 (Wokwi)** — projeto salvo em <https://wokwi.com/projects/480879311582717953>. Com a simulação rodando: conclusão com fila vazia → `rejeitado`; três chegadas → `pessoa=1`, `2`, `3`; conclusão → `pessoa=1;duracao=7.0`, display "Atendido #1". Potenciômetro e LEDs não foram conferidos nesta execução.
- **A fazer pela equipe:** conferir os resultados, repetir os quatro cenários no navegador durante a gravação e registrar o teste de acesso pela internet.
- **Observação:** os 60 registros iniciais (`data/historico_simulado.csv`) são **simulados** e identificados como tal.
