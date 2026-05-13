"""Granulares — gravel.png e soul_sand.png.

Gravel usa `random.seed(42)` (deterministico) para distribuir pedrinhas
brancas e pretas — o resultado e reproduzivel byte-a-byte.

Soul sand usa padrao fixo com 3 "buracos/rostos" sugeridos.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import PALETA_GRAVEL, PALETA_SOUL_SAND


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


def gerar_gravel():
    """Gravel — distribuicao aleatoria mas deterministica (seed=42).

    Cada pixel:
      55% base
      18% claro (sombra clara)
      15% escuro (sombra escura)
      6%  pedra_branca (pedrinha clara)
      6%  pedra_preta (pedrinha escura)

    Para tilear, forca a row 15 igual a row 0 e ajusta col 0/15 pra
    ficarem com luma proximo.
    """
    p = PALETA_GRAVEL
    rng = random.Random(42)

    img = helpers.nova_img(16, 16)
    pesos = [
        ('base',         55),
        ('claro',        18),
        ('escuro',       15),
        ('pedra_branca', 6),
        ('pedra_preta',  6),
    ]
    keys, ws = zip(*pesos)
    cumul = []
    s = 0
    for w in ws:
        s += w
        cumul.append(s)
    total = cumul[-1]

    grid = [[None] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            r = rng.uniform(0, total)
            for k, c in zip(keys, cumul):
                if r < c:
                    grid[y][x] = k
                    break

    # forca tileabilidade: row 15 = row 0
    grid[15] = list(grid[0])
    # col 15 = col 0 em luma proximo: se col 15 for pedra_branca/preta
    # (extremos), troca por base
    for y in range(16):
        if grid[y][15] in ('pedra_branca', 'pedra_preta'):
            grid[y][15] = 'base'
        if grid[y][0] in ('pedra_branca', 'pedra_preta'):
            grid[y][0] = 'base'

    for y in range(16):
        for x in range(16):
            helpers.px(img, x, y, p[grid[y][x]])
    return img


# Soul sand — padrao fixo com 3 "rostos" sugeridos por buracos triangulares.
SOULSAND_PATTERN = [
    '.M.e..M..e.M..e.',  # 0
    'M..R...e.M..M..e',  # 1   R = rosto (buraco)
    '.eRR.M..M.e.M..M',  # 2
    'M.R..e.M..eM..M.',  # 3
    '.M..M.eRR..M..eM',  # 4
    'M.e.M.RR.eM..M.e',  # 5
    '..M.eM..R.M..eM.',  # 6
    'M.eM..M.M..eM.M.',  # 7
    '.M.e..M..e.M..eM',  # 8
    'M..M.e..eRR..M.e',  # 9
    '.eM..M.e.RR.M..M',  # 10
    'M..eM..M.R..eM.M',  # 11
    '.M.e..M.M..M.e..',  # 12
    'eM..eM..M.eM.M.M',  # 13
    '.M.e..M..eM..eM.',  # 14
    '.M.e..M..e.M..e.',  # 15  — identica a row 0
]
_KEY_SOULSAND = {
    '.': 'base',
    'M': 'claro',
    'e': 'escuro',
    'R': 'rosto',
}


def gerar_soul_sand():
    p = PALETA_SOUL_SAND
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(SOULSAND_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_KEY_SOULSAND[ch]])
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'gravel.png':    gerar_gravel(),
        'soul_sand.png': gerar_soul_sand(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
