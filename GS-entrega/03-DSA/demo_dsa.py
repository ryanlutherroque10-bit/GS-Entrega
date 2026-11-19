"""Demonstração do DSA para gravação de tela.

Roda o main.py desta pasta (projeto/06-dsa-python) e digita as entradas na tela, tudo corrido.
Faz uma cópia de segurança do servicos.csv antes e a restaura no fim, para o projeto ficar igual.

Uso (de qualquer lugar):  python GS-ENTREGA\\03-DSA\\demo_dsa.py
"""
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

PASTA = Path(__file__).resolve().parent / "projeto" / "06-dsa-python"  # o DSA desta mesma pasta
CSV = PASTA / "dados" / "servicos.csv"
BACKUP = CSV.with_suffix(".csv.bak-demo")
sys.stdout.reconfigure(encoding="utf-8")

EXECUCOES = [
    [
        ("PASSOS 2 e 3 — consultar por ID (existente e inexistente)", ["2", "1", "2", "99"]),
        ("PASSO 3 — pesquisar por título/categoria (com e sem resultado)", ["3", "energia", "3", "xyz"]),
        ("PASSO 4 — cadastrar o ID 6 e tentar repetir o ID",
         ["1", "6", "Saúde", "Cartão do SUS", "Como solicitar o cartão", "Documento com foto", "UBS",
          "1", "6", "Saúde", "Cartão do SUS", "Como solicitar o cartão", "Documento com foto", "UBS"]),
        ("PASSO 5 — atualizar o ID 6, ordenar por título e ver a análise",
         ["4", "6", "Saúde", "Cartão Nacional de Saúde", "Solicitar o cartão", "Documento com foto", "UBS", "7", "8"]),
        ("PASSO 6 — ID e opção inválidos", ["2", "abc", "9"]),
        ("PASSO 7 — salvar e sair", ["0"]),
    ],
    [
        ("PASSO 7 — reabrir: os dados continuam (o ID 6 está salvo)", ["6"]),
        ("PASSO 6 — excluir o ID 6 e tentar excluir o ID 99", ["5", "6", "5", "99", "6"]),
        ("PASSO 7 — salvar e sair", ["0"]),
    ],
]


def digitar(texto: str) -> None:
    for c in texto:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.04)
    sys.stdout.write("\n")
    sys.stdout.flush()


def executar(passos) -> None:
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    proc = subprocess.Popen(
        [sys.executable, "-u", "main.py"], cwd=PASTA, env=env,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    ultimo = [time.time()]

    def ler():
        while True:
            b = proc.stdout.read(1)
            if not b:
                break
            ultimo[0] = time.time()
            sys.stdout.buffer.write(b)
            sys.stdout.buffer.flush()

    t = threading.Thread(target=ler, daemon=True)
    t.start()

    def esperar_parado(minimo=0.6):
        while time.time() - ultimo[0] < minimo:
            time.sleep(0.05)

    for titulo, entradas in passos:
        esperar_parado()
        print(f"\n\n>>> {titulo}")
        time.sleep(2.5)
        for entrada in entradas:
            esperar_parado()
            time.sleep(0.5)
            digitar(entrada)
            proc.stdin.write((entrada + "\n").encode("utf-8"))
            proc.stdin.flush()
            time.sleep(0.3)
    proc.wait(timeout=10)
    t.join(timeout=2)


shutil.copy2(CSV, BACKUP)
try:
    print("=== DEMONSTRAÇÃO DSA — Catálogo de Serviços (lista encadeada) ===")
    print("PASSO 1: no código, as classes Servico, No e ListaServicos (main.py).")
    time.sleep(4)
    print("\n$ python main.py")
    executar(EXECUCOES[0])
    print("\n\n>>> Fechou. Agora vamos reabrir o programa para provar que os dados foram salvos.")
    time.sleep(3)
    print("\n$ python main.py")
    executar(EXECUCOES[1])
    print("\n\n>>> FIM da demonstração.")
finally:
    shutil.copy2(BACKUP, CSV)
    BACKUP.unlink(missing_ok=True)
    print("(servicos.csv restaurado ao estado original)")
