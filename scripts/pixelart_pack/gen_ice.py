"""Familia 11_ice_snow — 4 PNGs.

  - ice.png         translucido (todos 256 pixels com alpha < 255) +
                    rachaduras finas
  - ice_packed.png  opaco, sem rachaduras
  - blue_ice.png    azul saturado, brilhante
  - snow.png        branco quase puro com leves sombras azuladas

Critico: ice e o unico arquivo desta familia onde o original tem alpha
em todos os 256 pixels (verificado via _inventory.py). Reproduzimos
isso com 'alpha=180' como base.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_ICE,
    PALETA_ICE_BLUE,
    PALETA_ICE_PACKED,
    PALETA_SNOW,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Padrao base para gelo (com ou sem alpha) — distribuicao tileavel.
ICE_PATTERN = [
    '.M.e..M..e.M..e.',  # 0
    'M..M.e..M..e.M..',  # 1
    '.e.M..M..e..M.e.',  # 2
    'M..e.M..M.e..M..',  # 3
    '.M..M.e..M.M..e.',  # 4
    'eM..e.M..eM..M.e',  # 5
    '.M..M.eM..e.M..M',  # 6
    'M.e..M..e.M..eM.',  # 7
    '.M.e..M..M.e.M..',  # 8
    'M..M.e.M..e..M.e',  # 9
    '.e..M.M..e.M..M.',  # 10
    'M..e.M..M.eM..e.',  # 11
    '.M.M..eM..M.e.M.',  # 12
    'eM..e.M..M.e..M.',  # 13
    '.M..M.e..eM..M.e',  # 14
    '.M.e..M..e.M..e.',  # 15  — identica a row 0
]
_KEY_ICE = {'.': 'base', 'M': 'claro', 'e': 'escuro'}


# Rachaduras finas para ice — sequencia de pixels em linhas
# diagonais/zigzag, marcadas com 'crack'.
ICE_CRACKS = [
    (2, 1), (3, 2), (4, 3), (5, 3), (6, 4), (7, 5),
    (10, 8), (11, 9), (12, 9), (13, 10), (14, 11),
    (1, 12), (2, 13), (3, 13), (4, 12),
]


def _gerar_ice_base(paleta: dict):
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(ICE_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, paleta[_KEY_ICE[ch]])
    return img


def gerar_ice():
    """Gelo translucido com rachaduras."""
    img = _gerar_ice_base(PALETA_ICE)
    for x, y in ICE_CRACKS:
        helpers.px(img, x, y, PALETA_ICE['crack'])
    return img


def gerar_ice_packed():
    """Gelo compacto opaco — sem rachaduras."""
    return _gerar_ice_base(PALETA_ICE_PACKED)


def gerar_blue_ice():
    """Gelo azul saturado com pontos de destaque (brilho)."""
    img = _gerar_ice_base(PALETA_ICE_BLUE)
    # destaques (pontos brancos sugerindo brilho/reflexo)
    destaques = [(2, 2), (8, 4), (13, 7), (5, 11), (11, 13)]
    for x, y in destaques:
        helpers.px(img, x, y, PALETA_ICE_BLUE['destaque'])
    return img


# Snow tem padrao mais homogeneo — quase tudo claro com algumas sombras
SNOW_PATTERN = [
    '.M.e..M.M..M..e.',  # 0
    'M..M..M..e..M.M.',
    '..M.e.M..M.M..e.',
    'M.M..M.e.M..M..M',
    '.e.M.M..M..e.M.M',
    'M..M..e.M.M..M..',
    '..M.eM..M.M.eM..',
    'M.M.M..e.M..M.M.',
    '.eM..M.M..M.M..e',
    'M..M.eM..M..e.M.',
    '.M.M..M.M..M.M..',
    'M..e.M..M.eM..M.',
    '.M.M..M.M..M.M.M',
    'M..M.eM..M..M..e',
    '..M.M..M.eM..M..',
    '.M.e..M.M..M..e.',  # 15  — identica a row 0
]


def gerar_snow():
    p = PALETA_SNOW
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(SNOW_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_KEY_ICE[ch]])
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'ice.png':         gerar_ice(),
        'ice_packed.png':  gerar_ice_packed(),
        'blue_ice.png':    gerar_blue_ice(),
        'snow.png':        gerar_snow(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        n_alpha = sum(1 for px in img.getdata() if px[3] < 255)
        marca = f' (alpha_px={n_alpha})' if n_alpha else ''
        print(f'  gerado {out.relative_to(REPO_ROOT)}{marca}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
