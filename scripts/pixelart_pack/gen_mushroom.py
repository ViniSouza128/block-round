"""18_mushroom_bone (parcial mushroom) — 2 PNGs.

mushroom_block_skin_brown e mushroom_block_skin_red — pele de
cogumelo gigante. Brown e marrom uniforme; red tem pintinhas brancas
classicas (icone de amanita).
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_MUSHROOM_BROWN,
    PALETA_MUSHROOM_RED,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Padrao base de pele — mesma estrutura granulada para os 2.
PELE_PATTERN = [
    '.M..e..M.M..eM.M',  # 0
    'M.M..eM..M.eM..e',
    '.eM..M..eM.M..eM',
    'M..M.eM..M.eM..M',
    '.M.eM..M.M..eM.M',
    'eM..M.eM..M.eM..',
    '.M.eM..M.eM..M.M',
    'M..M.eM..eM..M.M',
    '.eM..M.eM.M.eM..',
    'M..M.eM..M.eM.M.',
    '.M.eM..M.eM..eM.',
    'M.eM..eM..M.eM.M',
    '.M..M.eM.eM..M.M',
    'eM.eM..M..M.eM..',
    '.M.eM.eM..M.eM.M',
    '.M..e..M.M..eM.M',  # 15
]
_K_PELE = {'.': 'base', 'M': 'claro', 'e': 'escuro'}


def _gerar_pele(paleta: dict):
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(PELE_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, paleta[_K_PELE[ch]])
    return img


def gerar_mushroom_block_skin_brown():
    p = PALETA_MUSHROOM_BROWN
    img = _gerar_pele(p)
    # algumas pintinhas claras esparsas (sutil — marrom nao tem pintas brancas)
    pontos = [(3, 5), (10, 4), (6, 11), (13, 12)]
    for x, y in pontos:
        helpers.px(img, x, y, p['pinta'])
    return img


def gerar_mushroom_block_skin_red():
    p = PALETA_MUSHROOM_RED
    img = _gerar_pele(p)
    # pintinhas brancas grandes (icone amanita) — 5 grupos de 2x2
    pintas = [
        (3,  3), (10, 3), (5, 8), (12, 9), (3, 12),
    ]
    for cx, cy in pintas:
        for dx in (0, 1):
            for dy in (0, 1):
                helpers.px(img, cx + dx, cy + dy, p['pinta'])
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'mushroom_block_skin_brown.png': gerar_mushroom_block_skin_brown(),
        'mushroom_block_skin_red.png':   gerar_mushroom_block_skin_red(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
