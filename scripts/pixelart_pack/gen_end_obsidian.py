"""end_stone, obsidian (familia 14_end_obsidian) + glowstone (22_misc).

  - end_stone.png   amarelo-palido com leves variacoes
  - obsidian.png    roxo quase preto com reflexos sutis
  - glowstone.png   dourado-laranja luminoso com pontos brilhantes
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_END_STONE,
    PALETA_GLOWSTONE,
    PALETA_OBSIDIAN,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Padrao genérico para os 3 — distribuicao de tons base/claro/escuro/destaque.
# Legenda: . = base, M = claro, e = escuro, x = destaque (sombra ou gota).
GENERIC_PATTERN = [
    '.M.e..M..e.M..e.',  # 0
    'M.M..e.x.M..M.e.',
    '.eM..M..eM..M.eM',
    'M.e.x.M..M.eM..M',
    '.M.M.e..M.eM.M.e',
    'eM..M.eM..M.e.x.',
    '.M..M..eM.M.e..M',
    'M.eM..M.x.eM.M.M',
    '.M.e.M.M..M.eM..',
    'M.M.eM..eM..M.eM',
    '.eM..M.x.M.eM..M',
    'M.e.M.M.eM..M.eM',
    '.M..M.eM.eM..M.x',
    'eM..M.eM..eM.M..',
    '.M.eM..M..M.eM.M',
    '.M.e..M..e.M..e.',  # 15
]
_KEY = {'.': 'base', 'M': 'claro', 'e': 'escuro', 'x': None}  # x usa chave dada


def _gerar_generico(paleta: dict, destaque_chave: str):
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(GENERIC_PATTERN):
        for x, ch in enumerate(row):
            chave = destaque_chave if ch == 'x' else _KEY[ch]
            helpers.px(img, x, y, paleta[chave])
    return img


def gerar_end_stone(): return _gerar_generico(PALETA_END_STONE, destaque_chave='sombra')
def gerar_obsidian():  return _gerar_generico(PALETA_OBSIDIAN,  destaque_chave='reflexo')
def gerar_glowstone(): return _gerar_generico(PALETA_GLOWSTONE, destaque_chave='gota')


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'end_stone.png':  gerar_end_stone(),
        'obsidian.png':   gerar_obsidian(),
        'glowstone.png':  gerar_glowstone(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
