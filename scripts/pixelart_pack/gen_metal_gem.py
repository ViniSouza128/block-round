"""Familia 09_metal_gem_blocks — copper, iron, gold, diamond, emerald.

Todos compartilham o mesmo layout 3x3 de "lingotes/gemas" — 3 fileiras
e 3 colunas de celulas separadas por bordas escuras. Cada celula tem
canto superior-esquerdo com highlight e canto inferior-direito com
sombra (volume). Para gems (diamond/emerald), uma faisca extra no
centro de cada celula sugere face cristalina.

Layout em 16x16:
  - cells nas colunas x=0..4, x=6..9, x=11..15 (larguras 5/4/5)
  - cells nas linhas  y=0..4, y=6..9, y=11..15 (alturas 5/4/5)
  - borda escura em x=5, x=10, y=5, y=10 (separadores internos)

Tileabilidade: pixels nas extremidades (x=0, x=15, y=0, y=15) ficam
em cor 'base' (sem highlight/sombra extra), assim a borda entre tiles
casa visualmente.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_GEM_DIAMOND,
    PALETA_GEM_EMERALD,
    PALETA_METAL_COPPER,
    PALETA_METAL_GOLD,
    PALETA_METAL_IRON,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Coordenadas das 9 cells em formato (x0, y0, x1, y1) — inclusivas.
_CELLS = [
    (x0, y0, x1, y1)
    for y0, y1 in ((0, 4), (6, 9), (11, 15))
    for x0, x1 in ((0, 4), (6, 9), (11, 15))
]

# Coordenadas das bordas internas (separadores 1px)
_BORDAS_X = (5, 10)
_BORDAS_Y = (5, 10)


def _desenhar_cell(img, x0, y0, x1, y1, paleta, com_faceta: bool) -> None:
    p = paleta
    # corpo da cell em base
    for yy in range(y0, y1 + 1):
        for xx in range(x0, x1 + 1):
            helpers.px(img, xx, yy, p['base'])

    # highlight no canto superior-esquerdo: linha y0 (exceto extremos do tile)
    # e coluna x0 (exceto extremos)
    for xx in range(x0, x1 + 1):
        if y0 != 0:                  # nao mexer na borda do tile inteiro
            helpers.px(img, xx, y0, p['brilho'])
    for yy in range(y0, y1 + 1):
        if x0 != 0:
            helpers.px(img, x0, yy, p['brilho'])

    # sombra no canto inferior-direito: linha y1 e coluna x1
    for xx in range(x0, x1 + 1):
        if y1 != 15:
            helpers.px(img, xx, y1, p['sombra'])
    for yy in range(y0, y1 + 1):
        if x1 != 15:
            helpers.px(img, x1, yy, p['sombra'])

    # faceta central — pequeno highlight em forma de "+" no meio da cell
    if com_faceta:
        cx = (x0 + x1) // 2
        cy = (y0 + y1) // 2
        helpers.px(img, cx,     cy,     p['brilho'])
        helpers.px(img, cx + 1, cy,     p['brilho'])
        helpers.px(img, cx,     cy + 1, p['brilho'])


def _gerar_grade(paleta, com_faceta: bool = False):
    img = helpers.nova_img(16, 16)
    # bordas internas — 2 linhas verticais + 2 horizontais em 'borda'
    for x in _BORDAS_X:
        for y in range(16):
            helpers.px(img, x, y, paleta['borda'])
    for y in _BORDAS_Y:
        for x in range(16):
            helpers.px(img, x, y, paleta['borda'])
    # cells
    for x0, y0, x1, y1 in _CELLS:
        _desenhar_cell(img, x0, y0, x1, y1, paleta, com_faceta)
    return img


# ---------------------------------------------------------------------------
# Variantes
# ---------------------------------------------------------------------------

def gerar_copper_block():  return _gerar_grade(PALETA_METAL_COPPER)
def gerar_iron_block():    return _gerar_grade(PALETA_METAL_IRON)
def gerar_gold_block():    return _gerar_grade(PALETA_METAL_GOLD)
def gerar_diamond_block(): return _gerar_grade(PALETA_GEM_DIAMOND, com_faceta=True)
def gerar_emerald_block(): return _gerar_grade(PALETA_GEM_EMERALD, com_faceta=True)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'copper_block.png':  gerar_copper_block(),
        'iron_block.png':    gerar_iron_block(),
        'gold_block.png':    gerar_gold_block(),
        'diamond_block.png': gerar_diamond_block(),
        'emerald_block.png': gerar_emerald_block(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
