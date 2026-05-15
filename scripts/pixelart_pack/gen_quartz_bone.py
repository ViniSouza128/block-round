"""quartz_block (3 faces) + bone_block (2 faces).

Compartilham filosofia de "branco com nervuras" mas com hues distintos:
quartz e branco-creme com vein cinza; bone e marfim mais quente.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import PALETA_BONE, PALETA_QUARTZ


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# ---------------------------------------------------------------------------
# QUARTZ (3): top, side, bottom
# ---------------------------------------------------------------------------

QUARTZ_NOISE = [
    '.M.e..M.e..M..e.',  # 0
    'M..M.eM..eM.M..e',
    '.eM..M..M.eM..eM',
    'M..M.eM..M.eM..M',
    '.M..eM.eM..M.eM.',
    'M.eM..M..eM..M.M',
    '..M.eM..M.eM.eM.',
    'M.eM..eM.M..eM.M',
    '.M..M.eM..eM..M.',
    'M.eM..M.eM..M.eM',
    '.M..eM.M..eM..M.',
    'M.eM..eM..M.eM.M',
    '.M.eM..M.eM..eM.',
    'M..M.eM..M.eM..M',
    '.eM..M.eM..M.eM.',
    '.M.e..M.e..M..e.',  # 15
]
_K_QUARTZ = {'.': 'base', 'M': 'claro', 'e': 'escuro'}


def _quartz_base():
    p = PALETA_QUARTZ
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(QUARTZ_NOISE):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_QUARTZ[ch]])
    return img


def gerar_quartz_block_top():
    """Top: branco-creme + linha decorativa horizontal central + moldura fina."""
    p = PALETA_QUARTZ
    img = _quartz_base()
    # moldura fina nos 4 lados
    for k in range(16):
        helpers.px(img, k,  0,  p['moldura'])
        helpers.px(img, k,  15, p['moldura'])
        helpers.px(img, 0,  k,  p['moldura'])
        helpers.px(img, 15, k,  p['moldura'])
    # linha decorativa interna — quadrado 8x8 centrado, sem preencher
    for k in range(4, 12):
        helpers.px(img, k,  4,  p['simbolo'])
        helpers.px(img, k,  11, p['simbolo'])
        helpers.px(img, 4,  k,  p['simbolo'])
        helpers.px(img, 11, k,  p['simbolo'])
    return img


def gerar_quartz_block_side():
    """Side: branco-creme com leves veins verticais sutis."""
    p = PALETA_QUARTZ
    img = _quartz_base()
    # veins verticais sutis em x=4 e x=11
    for x in (4, 11):
        for y in range(2, 14):
            helpers.px(img, x, y, p['veining'])
    return img


def gerar_quartz_block_bottom():
    """Bottom: liso branco-creme, sem moldura."""
    return _quartz_base()


# ---------------------------------------------------------------------------
# BONE BLOCK (2): top, side
# ---------------------------------------------------------------------------

BONE_NOISE = [
    '.M.e.M..e.M..e.M',  # 0
    'M..M..eM.M..M.eM',
    '.eM.M..M.eM..M.e',
    'M..eM.M..M.eM..M',
    '.M..M.eM.M..eM.M',
    'M.eM..M.M.eM..eM',
    '.M..M.eM..M.eM..',
    'eM..M.M.eM..M.eM',
    '.M.eM..M..M.eM.M',
    'M..M.eM..eM..M.e',
    '.eM..M.eM..M.eM.',
    'M.eM..eM..M.eM.M',
    '.M.eM..M.eM..eM.',
    'M..M.eM..M.eM..M',
    '.eM..M.eM..M.eM.',
    '.M.e.M..e.M..e.M',  # 15
]
_K_BONE = {'.': 'base', 'M': 'claro', 'e': 'escuro'}


def _bone_base():
    p = PALETA_BONE
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(BONE_NOISE):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_BONE[ch]])
    return img


def gerar_bone_block_top():
    """Top: marfim + circulo concentrico (corte transversal de osso)."""
    p = PALETA_BONE
    img = _bone_base()
    # 3 aneis concentricos centrados em (7.5, 7.5)
    for y in range(16):
        for x in range(16):
            dx = abs(x - 7.5)
            dy = abs(y - 7.5)
            d = max(dx, dy)
            if 5.5 <= d < 6.5:
                helpers.px(img, x, y, p['nervura'])
            elif 3.5 <= d < 4.5:
                helpers.px(img, x, y, p['sombra'])
            elif d < 1.5:
                helpers.px(img, x, y, p['escuro'])  # canal medular
    return img


def gerar_bone_block_side():
    """Side: marfim + 4 nervuras verticais (sugerindo costelas/sulcos do osso)."""
    p = PALETA_BONE
    img = _bone_base()
    for x in (2, 6, 10, 14):
        for y in range(16):
            helpers.px(img, x, y, p['nervura'])
    # leve highlight a esquerda de cada nervura
    for x in (1, 5, 9, 13):
        for y in range(0, 16, 2):
            helpers.px(img, x, y, p['claro'])
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'quartz_block_top.png':    gerar_quartz_block_top(),
        'quartz_block_side.png':   gerar_quartz_block_side(),
        'quartz_block_bottom.png': gerar_quartz_block_bottom(),
        'bone_block_top.png':      gerar_bone_block_top(),
        'bone_block_side.png':     gerar_bone_block_side(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
