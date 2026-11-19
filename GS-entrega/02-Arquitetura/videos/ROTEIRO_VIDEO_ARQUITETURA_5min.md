# Roteiro do vídeo de demonstração (até 5 minutos)

> Este arquivo é só o roteiro. **O vídeo ainda precisa ser gravado pela equipe**; não há gravação nem link no repositório.

**Antes de gravar**
- Abra o projeto do Wokwi já com `main.py` e `diagram.json` colados (ou o link salvo).
- Inicie o servidor (`python app.py`) e abra <http://127.0.0.1:8000>. Clique em **Reiniciar** no painel para zerar a fila.
- Em outra janela, deixe pronto o terminal em rede: `python tools/terminal_simulado.py`.
- Se for mostrar o acesso pela internet, siga antes a seção "Acesso pela internet" do README e teste a URL no celular (dados móveis).
- Deixe o diagrama [diagrama-arquitetura.svg](../projeto/fila-virtual-citizen-assist/docs/diagrama-arquitetura.svg) aberto em outra aba.

---

### 0:00–0:30 — Apresentação
"Este é o Sistema Inteligente de Filas Virtuais do Citizen Assist AI. O protótipo principal é um servidor com painel web e um terminal de atendimento ligados em rede, compartilhando a mesma fila. À parte, um Raspberry Pi Pico W simulado no Wokwi mostra as mesmas regras rodando em um microcontrolador."

### 0:30–1:15 — Arquitetura (diagrama)
Mostre o diagrama. Aponte:
- **CPU:** RP2040 com 2 núcleos Cortex-M0+ (clock de 125 MHz, máximo de 133 MHz) no Pico W; CPU x86-64 no servidor.
- **Memória:** SRAM de 264 KB com a fila em buffer circular; flash de 2 MB com o programa; SSD com `estado.json`.
- **Entradas:** botões nos GPIO 14 e 15 com interrupção; potenciômetro no ADC.
- **Saídas:** OLED por I2C, LEDs, painel web.
- **Comunicação:** I2C, USB serial, HTTP + JSON sobre TCP/IP.

### 1:15–2:00 — Experimento no Raspberry Pi Pico W (Wokwi)
Diga que este terminal funciona sozinho: a fila dele não é a do painel.
1. Clique em ▶. Mostre a primeira linha do monitor serial: CPU 125 MHz e RAM livre.
2. **Cenário 3:** aperte **Concluir** com a fila vazia → LED vermelho, display "! FILA VAZIA", log `rejeitado`.
3. **Cenário 1:** aperte **Chegada** 3 vezes → "Fila: 3/32", LED verde, estimativas Conv e IA no display.
4. **Cenário 2:** gire o potenciômetro (mostre "Dur." mudando) e aperte **Concluir** → a pessoa 1 sai, concluídos = 1, o log mostra a espera medida.

### 2:00–3:20 — Painel web e terminal em rede (mesma fila)
Deixe o painel e a janela do terminal lado a lado.
1. **Cenário 3:** clique em **Concluir atendimento** com a fila vazia → mensagem de erro e "1 operação inválida recusada".
2. **Cenário 1:** registre 4 chegadas → lista com posições e horários.
3. **Cenário 2:** informe 10 min e conclua → fila 3, concluídos 1, evento no registro.
4. **Comunicação:** na janela do terminal, digite `c` → a nova pessoa aparece no painel em até 3 s, com "origem: terminal" no registro. Digite `s 7` → a fila diminui no painel. Clique em **Registrar chegada** no painel e digite `e` no terminal → o terminal mostra a mesma fila.
4b. Se o acesso pela internet tiver sido preparado: abra a URL pública no celular e mostre o mesmo painel se atualizando.
5. Clique em **Exportar CSV** e mostre os eventos com data e hora.

### 3:20–4:15 — Previsão inteligente (Cenário 4)
- Mostre o cartão "Como estimamos": convencional = pessoas × média; IA = regressão linear `y = a + b·x`.
- "Com os 60 registros simulados, a regressão erra em média 2,86 min, contra 3,35 min da média histórica, cerca de 15% menos. O coeficiente b = 1,065 mostra que a espera real é maior que a conta simples, por causa do tempo de chamada."
- Conclua mais um atendimento e mostre a estimativa e a base de treinamento mudando ("60 simulados + N observados").
- Deixe claro: "Os dados iniciais são simulados e estão identificados no CSV."

### 4:15–5:00 — Análise e limitações
- Memória: o terminal usa 12 KB e deixa 193 KB livres; a fila tem tamanho fixo, então não cresce.
- Desempenho: "Nos testes encontramos a validação do modelo em O(n²), que levava 278 ms por consulta. Otimizamos para O(n): 0,59 ms."
- Conectividade: o Pico W do Wokwi não envia eventos ao servidor; essa ligação é só prevista. A comunicação em rede é a do terminal em software e do painel com o servidor, com reenvio sem duplicar eventos.
- Encerramento: "22 testes automatizados cobrem os quatro cenários do enunciado e as operações inválidas."
