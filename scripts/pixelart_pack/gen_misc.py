"""22_misc_solids (resto) — bedrock + bricks + sponge.

Os outros do grupo 22 (gravel, glowstone, sponge) ja foram cobertos
em rodadas anteriores. Aqui ficam os 3 ultimos.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_BEDROCK,
    PALETA_BRICKS,
    PALETA_SPONGE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# ---------------------------------------------------------------------------
# BEDROCK — cinza escuro indestrutivel com manchas pretas
# ---------------------------------------------------------------------------

BEDROCK_PATTERN = [
    '.M.e.kM..eM.k.M.',  # 0   k = mancha (preto)
    'M.M.eM.k.eM..eM.',
    '.eM..M..eMk..M.k',
    'M..eM..M.eM..M.M',
    '.M.kMe.M..eM.eM.',
    'M.eM..M.kM..M.kM',
    '.M..eM..eM.k.M.M',
    'eM..M.k.M.eM..eM',
    '.M.eM..eMk.M.eM.',
    'M..M.eM.k.M.eM.M',
    '.eM..eM..M.kM..',
    'M.eM..M.eM..M.kM',
    '.M.kM.eM.eM..M.M',
    'eM..M.k.M.eMk..M',
    '.M.eM..M.eM..M.k',
    '.M.e.kM..eM.k.M.',  # 15
]
_K_BEDROCK = {'.': 'base', 'M': 'claro', 'e': 'escuro', 'k': 'mancha'}


def gerar_bedrock():
    p = PALETA_BEDROCK
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(BEDROCK_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_BEDROCK[ch]])
    return img


# ---------------------------------------------------------------------------
# BRICKS — tijolinhos vermelhos com rejunte cinza
# ---------------------------------------------------------------------------

def gerar_bricks():
    p = PALETA_BRICKS
    img = helpers.nova_img(16, 16)
    helpers.fill(img, p['rejunte'])

    # tijolos 4x3 com offset alternado por fileira (running bond classico).
    # 5 fileiras com altura 3 + rejunte 0 entre = 15px + ultima rejunte y=15
    fileiras = [
        (1,  3,  [(0, 3),  (5, 8),  (10, 13)]),
        (4,  6,  [(0, 1),  (3, 6),  (8, 11), (13, 15)]),
        (7,  9,  [(0, 3),  (5, 8),  (10, 13)]),
        (10, 12, [(0, 1),  (3, 6),  (8, 11), (13, 15)]),
        (13, 14, [(0, 3),  (5, 8),  (10, 13)]),
    ]
    for y0, y1, tijs in fileiras:
        for x0, x1 in tijs:
            for yy in range(y0, y1 + 1):
                for xx in range(x0, x1 + 1):
                    helpers.px(img, xx, yy, p['tijolo'])
            for xx in range(x0, x1 + 1):
                helpers.px(img, xx, y0, p['tijolo_claro'])
            for xx in range(x0, x1 + 1):
                helpers.px(img, xx, y1, p['tijolo_escuro'])
    return img


# ---------------------------------------------------------------------------
# SPONGE — amarelo poroso com furos escuros
# ---------------------------------------------------------------------------

SPONGE_PATTERN = [
    '.M..e..M.M..eM.M',  # 0
    'M.M.fM..M.eM.fM.',  # f = furo
    '.eM.fM.eM.fM..eM',
    'M..M.eM..M.eM..M',
    '.MfM..M.M.fM.eM.',
    'M.eM..fM..M.eM.f',
    '.M..M.eM.M.eM.M.',
    'eM.fM..M.eM..M.f',
    '.M.eM..fM.M.eM..',
    'M..M.eM..M.fM.M.',
    '.MfM..M.M.eM..eM',
    'M..M.eM.fM..M.eM',
    '.M.eMf.M.M.eM.M.',
    'eM..M.eMf..M.eM.',
    '.MfM..eM.M.eM.M.',
    '.M..e..M.M..eM.M',  # 15
]
_K_SPONGE = {'.': 'base', 'M': 'claro', 'e': 'escuro', 'f': 'furo'}


def gerar_sponge():
    p = PALETA_SPONGE
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(SPONGE_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_SPONGE[ch]])
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'bedrock.png': gerar_bedrock(),
        'bricks.png':  gerar_bricks(),
        'sponge.png':  gerar_sponge(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
