"""Familia 15_prismarine_sea — 4 PNGs (1 strip 16x80 incluso).

  - prismarine_bricks.png   tijolinhos turquesa
  - prismarine_dark.png     padrao escuro carved
  - prismarine_rough.png    STRIP 16x64 = 4 frames (animacao de ondas)
  - sea_lantern.png         STRIP 16x80 = 5 frames (luz pulsante)
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from PIL import Image

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import PALETA_PRISMARINE, PALETA_SEA_LANTERN


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# ---------------------------------------------------------------------------
# PRISMARINE BRICKS — tijolinhos com rejunte
# ---------------------------------------------------------------------------

def gerar_prismarine_bricks():
    p = PALETA_PRISMARINE
    img = helpers.nova_img(16, 16)
    helpers.fill(img, p['rejunte'])

    # tijolinhos pequenos 3x2 com offset alternado por fileira.
    # y=0 e y=15 ficam como rejunte pra tilear topo/base sem
    # estourar luma_dist (rejunte vs claro = 110, fora do limite).
    fileiras = [
        (1,  2,  [(0, 2),  (4, 6),  (8, 10), (12, 15)]),
        (4,  5,  [(0, 1),  (3, 5),  (7, 9),  (11, 13), (15, 15)]),
        (7,  8,  [(0, 2),  (4, 6),  (8, 10), (12, 15)]),
        (10, 11, [(0, 1),  (3, 5),  (7, 9),  (11, 13), (15, 15)]),
        (13, 14, [(0, 2),  (4, 6),  (8, 10), (12, 15)]),
    ]
    for y0, y1, tijs in fileiras:
        for x0, x1 in tijs:
            for yy in range(y0, y1 + 1):
                for xx in range(x0, x1 + 1):
                    helpers.px(img, xx, yy, p['tijolo_meio'])
            # highlight no topo
            for xx in range(x0, x1 + 1):
                helpers.px(img, xx, y0, p['claro'])
            # sombra no fundo
            for xx in range(x0, x1 + 1):
                helpers.px(img, xx, y1, p['escuro'])
    return img


# ---------------------------------------------------------------------------
# PRISMARINE DARK — padrao carved escuro
# ---------------------------------------------------------------------------

DARK_PATTERN = [
    '.M..e..M..e.M..e',  # 0
    'M.M..eM.M..M.eM.',
    '.eM..M..eM.M..eM',
    'M..eM..M.eM..M.M',
    '.M..M.eM..eM..M.',
    'eM..eM..M..M.eM.',
    '.M.eM..M.eM.M..e',
    'M..M.eM..eM..M.M',
    '.eM..M.eM..M.eM.',
    'M.eM..M..eM.M..M',
    '.M..eM..M.eM..eM',
    'M.eM.eM..M.eM..M',
    '.M..M.eM..eM.M..',
    'eM..M.eM..M.eM.M',
    '.M.eM..M.eM..eM.',
    '.M..e..M..e.M..e',  # 15
]
_K_DARK = {'.': 'dark_base', 'M': 'dark_claro', 'e': 'dark_escuro'}


def gerar_prismarine_dark():
    p = PALETA_PRISMARINE
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(DARK_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_DARK[ch]])
    # cruz central decorativa (sugere bloco esculpido)
    for k in (3, 4, 11, 12):
        helpers.px(img, k, 7, p['claro'])
        helpers.px(img, k, 8, p['claro'])
    for k in (3, 4, 11, 12):
        helpers.px(img, 7, k, p['claro'])
        helpers.px(img, 8, k, p['claro'])
    return img


# ---------------------------------------------------------------------------
# PRISMARINE ROUGH — strip 16x64 (4 frames de ondas)
# ---------------------------------------------------------------------------

# Padrao base (mesmo entre frames)
ROUGH_BASE = [
    '.M..e..M.M..e.M.',  # 0
    'M.eM.M.eM..M.eM.',
    '.eM..M..eM..M..M',
    'M..M.eM..M.eM..M',
    '.M.eM..M.M..eM.M',
    'M.eM.M.eM..M.eM.',
    '.M..M.eM..M.eM..',
    'M..eM..M.eM..M.M',
    '.M..M.eM..M.eM.M',
    'M.eM..M.eM..M..M',
    '.M.eM..M..eM.eM.',
    'M..M.eM.M..M.eM.',
    '.eM..M..eM.M..M.',
    'M..eM..M.eM..M.M',
    '.M.eM..M..eM.eM.',
    '.M..e..M.M..e.M.',  # 15
]
_K_ROUGH = {'.': 'base', 'M': 'claro', 'e': 'escuro'}

# Cada frame adiciona uma "onda" (linha sinuosa de pixels claros) em
# posicoes diferentes — sugere a agua se movendo.
ONDAS_FRAMES = [
    # frame 0 — onda em y=3
    [(2, 3), (3, 2), (4, 3), (5, 4), (6, 3), (7, 2), (8, 3), (9, 4), (10, 3), (11, 2), (12, 3), (13, 4)],
    # frame 1 — onda em y=4
    [(2, 4), (3, 3), (4, 4), (5, 5), (6, 4), (7, 3), (8, 4), (9, 5), (10, 4), (11, 3), (12, 4), (13, 5)],
    # frame 2 — onda em y=11
    [(2, 11), (3, 10), (4, 11), (5, 12), (6, 11), (7, 10), (8, 11), (9, 12), (10, 11), (11, 10), (12, 11), (13, 12)],
    # frame 3 — onda em y=12
    [(2, 12), (3, 11), (4, 12), (5, 13), (6, 12), (7, 11), (8, 12), (9, 13), (10, 12), (11, 11), (12, 12), (13, 13)],
]


def _rough_frame(idx: int):
    p = PALETA_PRISMARINE
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(ROUGH_BASE):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_ROUGH[ch]])
    for x, y in ONDAS_FRAMES[idx]:
        helpers.px(img, x, y, p['claro'])
    return img


def gerar_prismarine_rough():
    """Strip 16x64 = 4 frames empilhados verticalmente."""
    strip = Image.new('RGBA', (16, 64), (0, 0, 0, 0))
    for i in range(4):
        strip.paste(_rough_frame(i), (0, i * 16), _rough_frame(i))
    return strip


# ---------------------------------------------------------------------------
# SEA LANTERN — strip 16x80 (5 frames de luminosidade pulsante)
# ---------------------------------------------------------------------------

# Base de cristais comum a todos os frames
SL_BASE = [
    '.M.eM.eM.M.eM.M.',  # 0
    'M.M.M..eM.M.eM.M',
    '.M..M.eM..eM.M.e',
    'eM.M..M..M.M.eM.',
    '.M.eM..M.M.eM.M.',
    'M..M.eM..M..eM.M',
    '.M..M.eM.M.eM.M.',
    'eM..M.eM..M.eM.M',
    '.M.eM..M.M.eM..M',
    'M..M.eM..M.eM.M.',
    '.M..M.eM.M.eM.M.',
    'M.eM..M..eM..M.M',
    '.M.eM..M.M.eM.M.',
    'eM..M.eM..M.eM.M',
    '.M.eM..M.eM..M.M',
    '.M.eM.eM.M.eM.M.',  # 15
]
_K_SL = {'.': 'base', 'M': 'claro', 'e': 'escuro'}

# Cristais em posicoes fixas — quadrados 2x2 com brilho variavel por frame
CRISTAIS_POS = [
    (3, 3), (10, 3), (6, 7), (3, 11), (12, 11),
]
# Intensidade do brilho por frame: 0=sutil, 2=auge, 4=de volta a sutil
INTENSIDADES = ['cristal', 'cristal', 'cristal_glow', 'cristal_glow', 'cristal']


def _sl_frame(idx: int):
    p = PALETA_SEA_LANTERN
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(SL_BASE):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_SL[ch]])
    cor = p[INTENSIDADES[idx]]
    for cx, cy in CRISTAIS_POS:
        for dx in (0, 1):
            for dy in (0, 1):
                helpers.px(img, cx + dx, cy + dy, cor)
    return img


def gerar_sea_lantern():
    """Strip 16x80 = 5 frames empilhados verticalmente."""
    strip = Image.new('RGBA', (16, 80), (0, 0, 0, 0))
    for i in range(5):
        strip.paste(_sl_frame(i), (0, i * 16), _sl_frame(i))
    return strip


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'prismarine_bricks.png': gerar_prismarine_bricks(),
        'prismarine_dark.png':   gerar_prismarine_dark(),
        'prismarine_rough.png':  gerar_prismarine_rough(),
        'sea_lantern.png':       gerar_sea_lantern(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        marca = f' ({img.size})' if img.size != (16, 16) else ''
        print(f'  gerado {out.relative_to(REPO_ROOT)}{marca}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
