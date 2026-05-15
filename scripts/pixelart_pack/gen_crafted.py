"""Familia 19_crafted_workstations — bookshelf + crafting_table (3) + furnace (3).

Reusa paleta de planks oak para a base de madeira (coerencia com a familia
de tabuas) e paleta de stone para a base do furnace (coerencia com pedra).
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.gen_planks import gerar_planks_base
from scripts.pixelart_pack.palette import (
    PALETA_BOOKSHELF,
    PALETA_CRAFTING,
    PALETA_FURNACE,
    PALETA_PLANKS_OAK,
    PALETA_STONE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# ---------------------------------------------------------------------------
# BOOKSHELF (1) — borda madeira em cima e embaixo + 5 livros no meio
# ---------------------------------------------------------------------------

def gerar_bookshelf():
    p = PALETA_BOOKSHELF

    # comeca com madeira (oak planks reduzido)
    img = gerar_planks_base(PALETA_PLANKS_OAK)

    # area dos livros: y=2..13 (cobre apenas o miolo, deixando 2 px de
    # tabua em cima e 2 embaixo)
    # 5 livros de larguras: 3, 3, 4, 3, 3 px = 16 (sem rejunte interno)
    livros = [
        (0,  2,  'capa_vermelha'),
        (3,  5,  'capa_azul'),
        (6,  9,  'capa_verde'),
        (10, 12, 'capa_amarela'),
        (13, 15, 'capa_marrom'),
    ]
    y0, y1 = 2, 13

    for x0, x1, capa in livros:
        # corpo do livro
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                helpers.px(img, xx, yy, p[capa])
        # paginas do topo + da base (1 px cada)
        for xx in range(x0, x1 + 1):
            helpers.px(img, xx, y0, p['paginas'])
            helpers.px(img, xx, y1, p['paginas_sombra'])
        # contorno escuro nas laterais (sugere borda de capa)
        for yy in range(y0, y1 + 1):
            helpers.px(img, x0, yy, p['madeira_escuro'])
            if x1 < 15:
                helpers.px(img, x1, yy, p['madeira_escuro'])

    # bordas de madeira (sobrescreve y=0,1 e y=14,15 com tabua)
    # rows 0 e 15 ficam IDENTICAS pra tilear topo/base (madeira_claro
    # vs madeira_escuro tem luma diff > 90, estouraria o limite)
    for x in range(16):
        helpers.px(img, x, 0,  p['madeira'])
        helpers.px(img, x, 1,  p['madeira_claro'])
        helpers.px(img, x, 14, p['madeira_escuro'])
        helpers.px(img, x, 15, p['madeira'])

    return img


# ---------------------------------------------------------------------------
# CRAFTING TABLE (3): top, side, front
# ---------------------------------------------------------------------------

def _crafting_madeira_base():
    """Base de madeira (oak planks) usada por todas as 3 faces."""
    return gerar_planks_base(PALETA_PLANKS_OAK)


def gerar_crafting_table_top():
    """Top: madeira + grid 3x3 de ferramentas estilizado."""
    p = PALETA_CRAFTING
    img = _crafting_madeira_base()

    # grid 3x3 — 9 celulas com ferramenta minima em cada
    # cell em x=(2..4), (7..9), (12..14) e y=(2..4), (7..9), (12..14)
    cells = [(cx, cy) for cy in (3, 8, 13) for cx in (3, 8, 13)]
    # alterna ferramenta (M = metal, m = madeira-cabo) por cell
    for i, (cx, cy) in enumerate(cells):
        if i % 2 == 0:
            # cabeca de metal pequena (1x2)
            helpers.px(img, cx,     cy - 1, p['metal'])
            helpers.px(img, cx,     cy,     p['metal_escuro'])
            helpers.px(img, cx - 1, cy - 1, p['metal'])
            helpers.px(img, cx - 1, cy,     p['metal_escuro'])
        else:
            # cabo de madeira vertical
            helpers.px(img, cx, cy - 1, p['cabo_madeira'])
            helpers.px(img, cx, cy,     p['cabo_madeira'])
            helpers.px(img, cx, cy + 1, p['gaveta_escuro'])

    return img


def gerar_crafting_table_side():
    """Side: madeira + 2 gavetas horizontais escuras."""
    p = PALETA_CRAFTING
    img = _crafting_madeira_base()
    # gaveta 1 em y=3..5 (com puxador no centro)
    for yy in range(3, 6):
        for xx in range(2, 14):
            helpers.px(img, xx, yy, p['gaveta'])
    # contorno
    for xx in range(2, 14):
        helpers.px(img, xx, 3, p['gaveta_escuro'])
        helpers.px(img, xx, 5, p['gaveta_escuro'])
    for yy in range(3, 6):
        helpers.px(img, 2,  yy, p['gaveta_escuro'])
        helpers.px(img, 13, yy, p['gaveta_escuro'])
    # puxador (metal)
    helpers.px(img, 7, 4, p['metal'])
    helpers.px(img, 8, 4, p['metal_escuro'])

    # gaveta 2 em y=10..12 (sem puxador, simulando gaveta lisa)
    for yy in range(10, 13):
        for xx in range(2, 14):
            helpers.px(img, xx, yy, p['gaveta'])
    for xx in range(2, 14):
        helpers.px(img, xx, 10, p['gaveta_escuro'])
        helpers.px(img, xx, 12, p['gaveta_escuro'])
    for yy in range(10, 13):
        helpers.px(img, 2,  yy, p['gaveta_escuro'])
        helpers.px(img, 13, yy, p['gaveta_escuro'])
    helpers.px(img, 7,  11, p['metal'])
    helpers.px(img, 8,  11, p['metal_escuro'])

    return img


def gerar_crafting_table_front():
    """Front: madeira + ferramentas penduradas (martelo + serra)."""
    p = PALETA_CRAFTING
    img = _crafting_madeira_base()

    # martelo na metade esquerda — cabeca metal + cabo
    # cabeca: retangulo 4x2 em (2..5, 4..5)
    for yy in range(4, 6):
        for xx in range(2, 6):
            helpers.px(img, xx, yy, p['metal'])
    helpers.px(img, 5, 5, p['metal_escuro'])  # sombra
    # cabo: vertical em x=4 indo de y=6..11
    for yy in range(6, 12):
        helpers.px(img, 4, yy, p['cabo_madeira'])

    # serra na metade direita — lamina horizontal + cabo
    # lamina (linha de dentes) em y=8 de x=8..14
    for xx in range(8, 15):
        helpers.px(img, xx, 8, p['metal'])
    # dentes (4 pixels mais escuros abaixo)
    for xx in (9, 11, 13):
        helpers.px(img, xx, 9, p['metal_escuro'])
    # cabo (madeira) em x=14 indo de y=4..7
    for yy in range(4, 8):
        helpers.px(img, 14, yy, p['cabo_madeira'])

    return img


# ---------------------------------------------------------------------------
# FURNACE (3): top, side, front_off
# ---------------------------------------------------------------------------

def _furnace_pedra_base():
    """Base de pedra cinza padrao (compacta)."""
    p = PALETA_FURNACE
    img = helpers.nova_img(16, 16)
    # padrao chapado com leve noise
    helpers.fill(img, p['pedra_base'])
    perturbs = {
        2:  [(3, 'pedra_claro'), (10, 'pedra_escuro')],
        4:  [(7, 'pedra_claro'), (13, 'pedra_escuro')],
        6:  [(2, 'pedra_escuro'), (11, 'pedra_claro')],
        8:  [(5, 'pedra_claro'), (14, 'pedra_escuro')],
        10: [(1, 'pedra_escuro'), (9, 'pedra_claro')],
        12: [(4, 'pedra_claro'), (12, 'pedra_escuro')],
        14: [(7, 'pedra_escuro'), (13, 'pedra_claro')],
    }
    for y, ms in perturbs.items():
        for x, k in ms:
            helpers.px(img, x, y, p[k])
    return img


def gerar_furnace_top():
    """Top: pedra + circulo central escuro."""
    p = PALETA_FURNACE
    img = _furnace_pedra_base()
    # circulo central — quadrado 4x4 com cantos arredondados
    centro = [
        (6, 6), (7, 6), (8, 6), (9, 6),
        (6, 7), (9, 7),
        (6, 8), (9, 8),
        (6, 9), (7, 9), (8, 9), (9, 9),
    ]
    for x, y in centro:
        helpers.px(img, x, y, p['topo_circulo'])
    # interior do circulo um pouco mais escuro
    for x, y in [(7, 7), (8, 7), (7, 8), (8, 8)]:
        helpers.px(img, x, y, p['moldura'])
    return img


def gerar_furnace_side():
    """Side: pedra lisa + leve moldura escura nas bordas."""
    p = PALETA_FURNACE
    img = _furnace_pedra_base()
    # moldura escura de 1 px nos 4 lados (assinatura de bloco "fechado")
    for k in range(16):
        helpers.px(img, k,  0,  p['moldura'])
        helpers.px(img, k,  15, p['moldura'])
        helpers.px(img, 0,  k,  p['moldura'])
        helpers.px(img, 15, k,  p['moldura'])
    return img


def gerar_furnace_front_off():
    """Front (apagado): abertura escura central + grelha horizontal de barras."""
    p = PALETA_FURNACE
    img = _furnace_pedra_base()

    # moldura externa 1 px
    for k in range(16):
        helpers.px(img, k,  0,  p['moldura'])
        helpers.px(img, k,  15, p['moldura'])
        helpers.px(img, 0,  k,  p['moldura'])
        helpers.px(img, 15, k,  p['moldura'])

    # abertura central — retangulo 10x8 em (3..12, 4..11)
    for yy in range(4, 12):
        for xx in range(3, 13):
            helpers.px(img, xx, yy, p['abertura'])

    # grelha horizontal — 3 barras em y=5, 8, 10 (apagada, mais escura)
    for yy in (5, 8, 10):
        for xx in range(3, 13):
            helpers.px(img, xx, yy, p['grelha'])

    # contorno da abertura (1 px claro acima/sombra abaixo) — sugere relevo
    for xx in range(3, 13):
        helpers.px(img, xx, 3,  p['pedra_escuro'])
        helpers.px(img, xx, 12, p['moldura'])

    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'bookshelf.png':            gerar_bookshelf(),
        'crafting_table_top.png':   gerar_crafting_table_top(),
        'crafting_table_side.png':  gerar_crafting_table_side(),
        'crafting_table_front.png': gerar_crafting_table_front(),
        'furnace_top.png':          gerar_furnace_top(),
        'furnace_side.png':         gerar_furnace_side(),
        'furnace_front_off.png':    gerar_furnace_front_off(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
