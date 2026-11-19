"""Gera docs/relatorio.html (e, com --pdf, docs/relatorio.pdf via Microsoft Edge).

Mapas de Karnaugh e diagramas dos circuitos são desenhados aqui em SVG a partir
das mesmas expressões usadas em orientador_tsee.py, para que figuras e código
não fiquem dessincronizados.
"""

from __future__ import annotations

import html
import subprocess
import sys
from itertools import product
from pathlib import Path

import orientador_tsee as o

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
DATA_CONSULTA = "12 nov. 2026"
GRAY = ["00", "01", "11", "10"]
CORES = ["#1f6feb", "#d1242f", "#1a7f37", "#8250df"]


# =============================================================================== Karnaugh
def kmap_svg(nome: str, mintermos: set[int], grupos: list[tuple[str, list[int], list[int]]]) -> str:
    """grupos: (rótulo, índices de linha na ordem Gray, índices de coluna na ordem Gray)."""
    cel, x0, y0 = 46, 70, 62
    p = [f'<svg viewBox="0 0 330 254" class="kmap" role="img" aria-label="Mapa de Karnaugh de {nome}">']
    p.append(f'<text x="8" y="16" class="kt">{nome}</text>')
    p.append(f'<text x="{x0 - 10}" y="{y0 - 14}" text-anchor="end" class="kl">AB \\ CD</text>')
    for j, cd in enumerate(GRAY):
        p.append(f'<text x="{x0 + j * cel + cel / 2}" y="{y0 - 12}" text-anchor="middle" class="kl">{cd}</text>')
    for i, ab in enumerate(GRAY):
        p.append(f'<text x="{x0 - 10}" y="{y0 + i * cel + cel / 2 + 5}" text-anchor="end" class="kl">{ab}</text>')
        for j, cd in enumerate(GRAY):
            m = int(ab + cd, 2)
            x, y = x0 + j * cel, y0 + i * cel
            p.append(f'<rect x="{x}" y="{y}" width="{cel}" height="{cel}" class="kc"/>')
            p.append(f'<text x="{x + cel / 2}" y="{y + cel / 2 + 6}" text-anchor="middle" '
                     f'class="kv{" on" if m in mintermos else ""}">{1 if m in mintermos else 0}</text>')
            p.append(f'<text x="{x + 4}" y="{y + 11}" class="km">m{m}</text>')

    def runs(idx):
        idx = sorted(idx)
        segs, cur = [], [idx[0]]
        for k in idx[1:]:
            if k == cur[-1] + 1:
                cur.append(k)
            else:
                segs.append(cur)
                cur = [k]
        segs.append(cur)
        return segs

    for g, (rotulo, linhas, colunas) in enumerate(grupos):
        cor = CORES[g % len(CORES)]
        pad = 4 + g * 4
        for rs in runs(linhas):
            for cs in runs(colunas):
                x = x0 + cs[0] * cel + pad
                y = y0 + rs[0] * cel + pad
                w = len(cs) * cel - 2 * pad
                h = len(rs) * cel - 2 * pad
                p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{cor}" '
                         f'fill-opacity="0.10" stroke="{cor}" stroke-width="2.4"/>')
        p.append(f'<rect x="{x0 + 4 * cel + 14}" y="{y0 + g * 26}" width="14" height="14" rx="3" fill="{cor}"/>')
        p.append(f'<text x="{x0 + 4 * cel + 34}" y="{y0 + g * 26 + 12}" class="kg">{html.escape(rotulo)}</text>')
    p.append("</svg>")
    return "".join(p)


# =============================================================================== circuitos
def and_gate(x, y, w=34, h=26):
    return (f'<path d="M{x},{y} h{w / 2} a{h / 2},{h / 2} 0 0 1 0,{h} h-{w / 2} z" class="g"/>', x + w / 2 + h / 2)


def or_gate(x, y, w=40, h=30):
    d = (f"M{x},{y} q{w * 0.35},{h / 2} 0,{h} q{w * 0.65},0 {w},-{h / 2} "
         f"q-{w * 0.35},-{h / 2} -{w},-{h / 2} z")
    return f'<path d="{d}" class="g"/>', x + w


def sop_svg(titulo: str, saidas: list[tuple[str, list[str]]], nota: str) -> str:
    """Desenha somas de produtos: cada termo é uma AND rotulada; as ANDs de uma saída vão a uma OR."""
    linha_h, bloco_gap = 34, 22
    altura = 40 + sum(max(1, len(t)) * linha_h + bloco_gap for _, t in saidas) + 30
    p = [f'<svg viewBox="0 0 640 {altura}" class="circ" role="img" aria-label="{html.escape(titulo)}">',
         f'<text x="8" y="20" class="ct">{html.escape(titulo)}</text>']
    y = 40
    for nome, termos in saidas:
        topo = y
        saidas_and = []
        for termo in termos:
            literais = termo.split("·")
            gx = 210
            p.append(f'<text x="{gx - 8}" y="{y + 18}" text-anchor="end" class="lit">{html.escape(termo)}</text>')
            if len(literais) > 1:
                svg, sx = and_gate(gx, y + 4)
                p.append(svg)
                p.append(f'<text x="{gx + 13}" y="{y + 21}" class="gn">{len(literais)}</text>')
            else:
                p.append(f'<line x1="{gx}" y1="{y + 17}" x2="{gx + 47}" y2="{y + 17}" class="w"/>')
                sx = gx + 47
            saidas_and.append((sx, y + 17))
            y += linha_h
        meio = (topo + y - linha_h + 34) / 2 - 15
        ox = 360
        for sx, sy in saidas_and:
            p.append(f'<path d="M{sx},{sy} C{sx + 50},{sy} {ox - 40},{meio + 15} {ox + 8},{meio + 15}" class="w"/>')
        if len(termos) > 1:
            svg, fx = or_gate(ox, meio)
            p.append(svg)
            p.append(f'<text x="{ox + 14}" y="{meio + 20}" class="gn">{len(termos)}</text>')
        else:
            fx = ox + 8
        p.append(f'<line x1="{fx}" y1="{meio + 15}" x2="{fx + 60}" y2="{meio + 15}" class="w"/>')
        p.append(f'<circle cx="{fx + 66}" cy="{meio + 15}" r="6" class="out"/>')
        p.append(f'<text x="{fx + 80}" y="{meio + 20}" class="on">{nome}</text>')
        y += bloco_gap
    p.append(f'<text x="8" y="{altura - 10}" class="nota">{html.escape(nota)}</text>')
    p.append("</svg>")
    return "".join(p)


def literais_mintermo(m: int) -> str:
    bits = f"{m:04b}"
    return "·".join(v + ("" if b == "1" else "′") for v, b in zip("ABCD", bits))


# =============================================================================== conteúdo
def tabela_verdade() -> str:
    linhas = []
    for a, b, c, d in product((0, 1), repeat=4):
        m = o.indice(a, b, c, d)
        r = int((a and b) or c)
        s = o.regra_original(a, b, c, d)
        ativa = [n for n, v in s.items() if v][0]
        linhas.append(
            f"<tr><td>m{m}</td><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td class='r'>{r}</td>"
            + "".join(f"<td class='{'hi' if s[n] else ''}'>{s[n]}</td>" for n in "TUK")
            + f"<td class='txt'>{ {'T': 'Indício de direito nesta unidade', 'U': 'Atende a uma condição; conferir a unidade com a distribuidora', 'K': 'Condições modeladas não atendidas: procurar o CRAS'}[ativa] }</td></tr>")
    return "".join(linhas)


def tabela_validacao() -> str:
    linhas = []
    for a, b, c, d in product((0, 1), repeat=4):
        m = o.indice(a, b, c, d)
        nomes = ["".join(n for n, v in f(a, b, c, d).items() if v)
                 for f in (o.regra_original, o.forma_simplificada)]
        obs = o.OBSERVADO_LOGICLY[m]
        ok = len(set(nomes + [obs])) == 1
        linhas.append(f"<tr><td>m{m}</td><td>{a}{b}{c}{d}</td>" + "".join(f"<td>{n}</td>" for n in nomes)
                      + f"<td>{obs}</td><td class='{'ok' if ok else 'bad'}'>{'✔' if ok else '✘'}</td></tr>")
    return "".join(linhas)


def galeria_prints() -> str:
    itens = []
    for a, b, c, d in product((0, 1), repeat=4):
        m = o.indice(a, b, c, d)
        bits = f"{a}{b}{c}{d}"
        itens.append(f'<figure class="thumb"><img src="../prints/m{m:02d}_ABCD_{bits}.jpg" alt="Logic.ly, '
                     f'entradas {bits}"><figcaption>m{m} · ABCD = {bits} → <b>{o.OBSERVADO_LOGICLY[m]}</b>'
                     f'</figcaption></figure>')
    return "".join(itens)


def montar_html() -> str:
    km_t = kmap_svg("T = Σm(3,7,11,13,15)", o.MINTERMOS["T"],
                    [("C·D", [0, 1, 2, 3], [2]), ("A·B·D", [2], [1, 2])])
    km_u = kmap_svg("U = Σm(2,6,10,12,14)", o.MINTERMOS["U"],
                    [("C·D′", [0, 1, 2, 3], [3]), ("A·B·D′", [2], [0, 3])])
    km_k = kmap_svg("K = Σm(0,1,4,5,8,9)", o.MINTERMOS["K"],
                    [("A′·C′", [0, 1], [0, 1]), ("B′·C′", [0, 3], [0, 1])])
    circ_original = sop_svg(
        "Circuito original — forma canônica (soma de mintermos)",
        [(n, [literais_mintermo(m) for m in sorted(o.MINTERMOS[n])]) for n in "TUK"],
        "Cada AND recebe 4 literais; A′, B′, C′ e D′ vêm de 4 portas NOT compartilhadas. "
        "O número dentro da porta é o total de entradas.")
    circ_original = circ_original.replace('class="circ"', 'class="circ big"', 1)
    circ_simpl = sop_svg(
        "Circuito simplificado — somas de produtos mínimas (Karnaugh)",
        [("T", ["C·D", "A·B·D"]), ("U", ["C·D′", "A·B·D′"]), ("K", ["A′·C′", "B′·C′"])],
        "A′, B′, C′ e D′ vêm de 4 portas NOT compartilhadas; nenhuma AND/OR é compartilhada entre saídas.")
    css = (ROOT / "docs" / "relatorio.css").read_text(encoding="utf-8")
    corpo = (ROOT / "docs" / "relatorio_corpo.html").read_text(encoding="utf-8")
    trocas = {
        "{{CSS}}": css, "{{TABELA_VERDADE}}": tabela_verdade(), "{{KM_T}}": km_t, "{{KM_U}}": km_u,
        "{{KM_K}}": km_k, "{{CIRC_ORIGINAL}}": circ_original, "{{CIRC_SIMPLIFICADO}}": circ_simpl,
        "{{TABELA_VALIDACAO}}": tabela_validacao(), "{{GALERIA}}": galeria_prints(),
        "{{DATA_CONSULTA}}": DATA_CONSULTA,
    }
    for chave, valor in trocas.items():
        corpo = corpo.replace(chave, valor)
    return corpo


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    destino = DOCS / "relatorio.html"
    destino.write_text(montar_html(), encoding="utf-8")
    print(f"HTML: {destino}")
    if "--pdf" in sys.argv:
        pdf = DOCS / "Relatorio_Computer_Science_Tarifa_Social.pdf"
        subprocess.run([str(EDGE), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", destino.as_uri()], check=True, timeout=120)
        print(f"PDF: {pdf}")


if __name__ == "__main__":
    main()
