"""Familia 04_wools — 8 cores de la, mesmo padrao de tricô.

`gerar_wool_base(paleta)` aplica o mesmo padrao 16x16 com 3 tons
(base, claro, escuro). Sugere fibra/malha entrelacada via pequenos
"pontos" alternados em padrao staggered.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_WOOL_BLACK,
    PALETA_WOOL_BLUE,
    PALETA_WOOL_GREEN,
    PALETA_WOOL_LIGHT_BLUE,
    PALETA_WOOL_ORANGE,
    PALETA_WOOL_RED,
    PALETA_WOOL_WHITE,
    PALETA_WOOL_YELLOW,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Padrao de tricô: pontos claros e escuros alternados em staggered, sugerindo
# fibra entrelacada. Padrao puro deterministico — nao depende de seed.
# Legenda:  . = base   M = claro   e = escuro
# Tileavel: row 0 == row 15; col 0 ~= col 15 dentro do limite luma.
WOOL_PATTERN = [
    'M.eM.e..M.eM.e..',  # 0
    '.e..M..e.e..M..e',  # 1
    '..M.e.M...M.e.M.',  # 2
    'e..M.e..e..M.e..',  # 3
    '.e.M.e..M.e.M.e.',  # 4
    'M.e..M.e..M.e.M.',  # 5
    '..M.e..M...M.e.M',  # 6
    'e.M..e.M.e.M..e.',  # 7
    '.M.e..M.e..M.e..',  # 8
    'M.e.M..e.M.e.M..',  # 9
    '..e.M.e..M..e.M.',  # 10
    'e..M.e..e..M.e..',  # 11
    '.M..e.M...M..e.M',  # 12
    'M.e..M.e..M.e..M',  # 13
    '..M.e..M...M.e..',  # 14
    'M.eM.e..M.eM.e..',  # 15  — identica a row 0
]
_KEY = {'.': 'base', 'M': 'claro', 'e': 'escuro'}


def gerar_wool_base(paleta: dict):
    """Reutilizada pelas 8 variantes — so a paleta muda."""
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(WOOL_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, paleta[_KEY[ch]])
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'white_wool.png':       gerar_wool_base(PALETA_WOOL_WHITE),
        'black_wool.png':       gerar_wool_base(PALETA_WOOL_BLACK),
        'red_wool.png':         gerar_wool_base(PALETA_WOOL_RED),
        'orange_wool.png':      gerar_wool_base(PALETA_WOOL_ORANGE),
        'yellow_wool.png':      gerar_wool_base(PALETA_WOOL_YELLOW),
        'green_wool.png':       gerar_wool_base(PALETA_WOOL_GREEN),
        'blue_wool.png':        gerar_wool_base(PALETA_WOOL_BLUE),
        'light_blue_wool.png':  gerar_wool_base(PALETA_WOOL_LIGHT_BLUE),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
