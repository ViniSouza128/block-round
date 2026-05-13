"""Familia 10_sand_sandstone — 5 PNGs com paleta beige compartilhada.

  - sand.png            graos finos uniformes
  - sandstone.png       lateral: ranhuras VERTICAIS sutis
  - sandstone_top.png   tampa lisa + moldura escura nas 4 bordas
  - sandstone_bottom.png base lisa SEM moldura
  - red_sandstone_top.png mesma estrutura do sandstone_top com paleta quente
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_RED_SANDSTONE,
    PALETA_SAND,
    PALETA_SANDSTONE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Padrao de graos finos pra sand. Distribuicao tileavel.
SAND_PATTERN = [
    '.M.e.gM.e.M..gM.',  # 0
    'M..e.M..gM.e..M.',  # 1
    '.e.M.gM..eM.g.M.',  # 2
    'M.e..M.gM.e.M..M',  # 3
    '..gM.e..M.gM.e..',  # 4
    'M.eM..g.eM..M.gM',  # 5
    '.M.e.gM.e..gM..M',  # 6
    'g.M..e.gM.e.M.e.',  # 7
    '.M.eg..M.e.gM.e.',  # 8
    'M.e..gM..eg.M..M',  # 9
    '..gM.e..gM.e.M.g',  # 10
    'M.e..gM.e..M.gM.',  # 11
    '.M.e.gM..eg.M.eM',  # 12
    'g.M.e..M.eM.gM..',  # 13
    '.M.eg..M.e.M.eM.',  # 14
    '.M.e.gM.e.M..gM.',  # 15  — identica a row 0
]
_KEY_SAND = {'.': 'base', 'M': 'claro', 'e': 'escuro', 'g': 'grao'}


def gerar_sand():
    p = PALETA_SAND
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(SAND_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_KEY_SAND[ch]])
    return img


# Sandstone lateral: base + ranhuras verticais finas em x=4 e x=11.
# Pequeno noise pra evitar parecer pintado.
SANDSTONE_LATERAL_PATTERN = [
    '.M..r..M.e.r..M.',  # 0
    '...M.r.e.M.r..M.',  # 1
    'M..e.r.M.e.r..eM',  # 2
    '..M..r.e.M.r.M..',  # 3
    '.e.M.r.M.e.r..M.',  # 4
    'M..e.rM..e.r.M..',  # 5
    '..M..r.e.M.r.eM.',  # 6
    'e.M.er.M.e.r.M.M',  # 7
    '.M..r.eM.e.r..eM',  # 8
    'M.e.Mr.M..M.r..e',  # 9
    '..M..r.e.eM.r.M.',  # 10
    'eM.e.r.M.e.r..M.',  # 11
    '.M.e.rM..e.rM.e.',  # 12
    '..M.er.M.e.r..eM',  # 13
    '.eM..rM..e.r..M.',  # 14
    '.M..r..M.e.r..M.',  # 15  — identica a row 0
]
_KEY_LATERAL = {'.': 'base', 'M': 'claro', 'e': 'escuro', 'r': 'ranhura'}


def gerar_sandstone():
    """Lateral — base + 2 ranhuras verticais sutis."""
    p = PALETA_SANDSTONE
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(SANDSTONE_LATERAL_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_KEY_LATERAL[ch]])
    return img


# Top: padrao base bem suave + moldura escura nas 4 bordas (tipo tampa
# lisa de bloco cortado).
TOP_PATTERN = [
    '.M..e..M..e..M..',  # 0
    'M.M..M.eM..M.M..',  # 1
    '.M.eM..M.eM..M.e',  # 2
    'e.M..M.e.M..M..M',  # 3
    '.M.e.M..eM.eM.M.',  # 4
    'M..M.eM..M..M..M',  # 5
    '..M.e..M.e..eM..',  # 6
    'M.eM..M.e..M..M.',  # 7
    '.M..e.eM..M.e.M.',  # 8
    'M.M..M.e.M.M..eM',  # 9
    '..eM.eM..M..M.M.',  # 10
    'M..M..M.eM..eM..',  # 11
    '.M.eM..M..M.M..e',  # 12
    'M..M.eM..eM..M.M',  # 13
    '..M..M.eM..M.e.M',  # 14
    '.M..e..M..e..M..',  # 15  — identica a row 0
]
_KEY_TOP = {'.': 'base', 'M': 'claro', 'e': 'escuro'}


def _sandstone_topo(paleta: dict, com_moldura: bool):
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(TOP_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, paleta[_KEY_TOP[ch]])
    if com_moldura:
        # moldura escura de 1 px nos 4 lados
        for k in range(16):
            helpers.px(img, k,  0,  paleta['moldura'])
            helpers.px(img, k,  15, paleta['moldura'])
            helpers.px(img, 0,  k,  paleta['moldura'])
            helpers.px(img, 15, k,  paleta['moldura'])
    return img


def gerar_sandstone_top():    return _sandstone_topo(PALETA_SANDSTONE, com_moldura=True)
def gerar_sandstone_bottom(): return _sandstone_topo(PALETA_SANDSTONE, com_moldura=False)
def gerar_red_sandstone_top():return _sandstone_topo(PALETA_RED_SANDSTONE, com_moldura=True)


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'sand.png':              gerar_sand(),
        'sandstone.png':         gerar_sandstone(),
        'sandstone_top.png':     gerar_sandstone_top(),
        'sandstone_bottom.png':  gerar_sandstone_bottom(),
        'red_sandstone_top.png': gerar_red_sandstone_top(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
