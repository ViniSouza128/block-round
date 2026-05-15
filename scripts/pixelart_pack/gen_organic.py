"""Familia 17_crops_organic — pumpkin, hay, melon (7 PNGs).

Multi-face: cada bloco compartilha paleta entre side/top/face.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import PALETA_HAY, PALETA_MELON, PALETA_PUMPKIN


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# ---------------------------------------------------------------------------
# PUMPKIN (3): top, side, face_off
# ---------------------------------------------------------------------------

# Padrao de granulado laranja para top/side/face — base + variacoes claro/escuro
PUMPKIN_NOISE = [
    '.M..e..M..e.M..e',  # 0
    'M.M..eM..M.eM..M',
    '.eM..M..eM.M..eM',
    'M..e.M.M..M.eM..',
    '.M.eM..M.eM..M.e',
    'M.eM..eM..M.eM.M',
    '.M..M..eM..eM.M.',
    'M.eM.M..M.eM..eM',
    '.M..M.eM..M.M.e.',
    'M.eM..M.eM..eM.M',
    '.eM..M.M..M.M.eM',
    'M..eM..M.eM..M..',
    '.M.eM.eM..M.eM.M',
    'M..M.eM..eM..M.e',
    '.eM..eM.M..M.eM.',
    '.M..e..M..e.M..e',  # 15
]
_K_PUMPKIN = {'.': 'laranja_base', 'M': 'laranja_claro', 'e': 'laranja_escuro'}


def _pumpkin_base():
    """Aplica granulado laranja em todo o bloco."""
    p = PALETA_PUMPKIN
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(PUMPKIN_NOISE):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_PUMPKIN[ch]])
    return img


def gerar_pumpkin_top():
    """Top: laranja + talo verde central + sombra do talo."""
    p = PALETA_PUMPKIN
    img = _pumpkin_base()
    # talo verde — pequeno disco em (7,7)..(8,8) com pixels ao redor
    talo = [
        (7, 6, 'talo_escuro'), (8, 6, 'talo_escuro'),
        (6, 7, 'talo_escuro'), (7, 7, 'talo_verde'), (8, 7, 'talo_claro'), (9, 7, 'talo_escuro'),
        (6, 8, 'talo_escuro'), (7, 8, 'talo_claro'), (8, 8, 'talo_verde'), (9, 8, 'talo_escuro'),
        (7, 9, 'talo_escuro'), (8, 9, 'talo_escuro'),
    ]
    for x, y, k in talo:
        helpers.px(img, x, y, p[k])
    return img


def gerar_pumpkin_side():
    """Side: laranja + 3 ranhuras verticais sutis."""
    p = PALETA_PUMPKIN
    img = _pumpkin_base()
    for x in (3, 8, 12):
        for y in range(1, 15):
            helpers.px(img, x, y, p['ranhura'])
    return img


def gerar_pumpkin_face_off():
    """Front: laranja + 2 olhos triangulares + boca recortada."""
    p = PALETA_PUMPKIN
    img = _pumpkin_base()
    # olho esquerdo (triangulo 3x3 em (3..5, 5..7))
    olho_e = [(3, 5), (4, 5), (5, 5), (4, 6), (5, 6), (5, 7)]
    olho_d = [(10, 5), (11, 5), (12, 5), (10, 6), (11, 6), (10, 7)]
    # boca — linha horizontal com dentes
    boca = [
        (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10),
        (5, 11), (8, 11), (10, 11),
        (4, 12), (6, 12), (7, 12), (9, 12), (11, 12),
    ]
    for x, y in olho_e + olho_d + boca:
        helpers.px(img, x, y, p['recorte'])
    return img


# ---------------------------------------------------------------------------
# HAY (2): top, side
# ---------------------------------------------------------------------------

# Top: feno em padrao circular tipo "amarrado" centrado.
HAY_TOP_PATTERN = [
    'fM.e..f.M..e.f.M',  # 0  f = fio
    'M.f..M.f.eM.f..e',
    '.M.fM.eM.fM.eM.f',
    'M.e.fM.eMf..M.fM',
    '.fM..fMM..fM..eM',
    'M.eM.MfM.eMf.M.f',
    '.f.MeM.fMe.MfM.M',
    'M.M.fMe.MfeM.MfM',
    '.MfM.eMf.eMf.MeM',
    'M.eMf.MeMf.MeMfM',
    '.fM.eM.fMe.fMe.M',
    'M.eMf.MeM.fMeMfM',
    '.MfM.eMf.eM.MfeM',
    'M.eMfM.fMe.fM.eM',
    '.fM.eM.MfMe.fMeM',
    'fM.e..f.M..e.f.M',  # 15
]
_K_HAY = {'.': 'base', 'M': 'claro', 'e': 'escuro', 'f': 'fio'}


def gerar_hay_block_top():
    p = PALETA_HAY
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(HAY_TOP_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_HAY[ch]])
    return img


def gerar_hay_block_side():
    """Side: feno horizontal + 2 amarras (cordas) em y=4 e y=11."""
    p = PALETA_HAY
    img = helpers.nova_img(16, 16)
    helpers.fill(img, p['base'])

    # palhas horizontais — perturbacoes claro/escuro/fio
    perturbs = {
        1:  [(2, 'M'), (6, 'f'), (10, 'M'), (13, 'e')],
        2:  [(0, 'M'), (4, 'e'), (8, 'M'), (12, 'f')],
        3:  [(3, 'M'), (7, 'e'), (11, 'M')],
        6:  [(1, 'f'), (5, 'M'), (9, 'e'), (14, 'M')],
        7:  [(2, 'M'), (6, 'e'), (10, 'M'), (13, 'f')],
        8:  [(0, 'e'), (4, 'M'), (8, 'f'), (12, 'M')],
        9:  [(3, 'M'), (7, 'e'), (11, 'M'), (15, 'f')],
        13: [(1, 'M'), (5, 'f'), (9, 'M'), (13, 'e')],
        14: [(0, 'f'), (4, 'M'), (8, 'e'), (12, 'M')],
    }
    for y, ms in perturbs.items():
        for x, ch in ms:
            helpers.px(img, x, y, p[_K_HAY[ch]])

    # 2 amarras horizontais (cordas escuras) em y=4 e y=11
    for y in (4, 11):
        for x in range(16):
            helpers.px(img, x, y, p['amarra'])
        # leve highlight da amarra (sugere relevo)
        for x in range(0, 16, 3):
            helpers.px(img, x, y, p['fio'])
    return img


# ---------------------------------------------------------------------------
# MELON (2): top, side
# ---------------------------------------------------------------------------

MELON_NOISE = [
    '.M..e..M..e.M..e',  # 0
    'M.M..eM..M.eM..M',
    '.eM..M..eM.M..eM',
    'M..e.M.M..M.eM..',
    '.M.eM..M.eM..M.e',
    'M.eM..eM..M.eM.M',
    '.M..M..eM..eM.M.',
    'M.eM.M..M.eM..eM',
    '.M..M.eM..M.M.e.',
    'M.eM..M.eM..eM.M',
    '.eM..M.M..M.M.eM',
    'M..eM..M.eM..M..',
    '.M.eM.eM..M.eM.M',
    'M..M.eM..eM..M.e',
    '.eM..eM.M..M.eM.',
    '.M..e..M..e.M..e',  # 15
]
_K_MELON = {'.': 'verde_base', 'M': 'verde_claro', 'e': 'verde_escuro'}


def gerar_melon_top():
    p = PALETA_MELON
    img = helpers.nova_img(16, 16)
    # uniforme verde com pontos claros (suco/brilho)
    for y, row in enumerate(MELON_NOISE):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_MELON[ch]])
    # alguns pontos extras claros sugerindo "suculencia"
    pontos = [(3, 4), (10, 6), (5, 11), (12, 13)]
    for x, y in pontos:
        helpers.px(img, x, y, p['listra_clara'])
    return img


def gerar_melon_side():
    """Side: verde + listras escuras verticais (caracteristica visual da melancia)."""
    p = PALETA_MELON
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(MELON_NOISE):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_K_MELON[ch]])
    # listras verticais escuras em x=2, 6, 9, 13 (com leve variacao por linha)
    for x in (2, 6, 9, 13):
        for y in range(16):
            helpers.px(img, x, y, p['listra'])
    # sub-listra clara adjacente (sugere relevo)
    for x in (3, 7, 10, 14):
        for y in range(0, 16, 2):
            helpers.px(img, x, y, p['listra_clara'])
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'pumpkin_top.png':       gerar_pumpkin_top(),
        'pumpkin_side.png':      gerar_pumpkin_side(),
        'pumpkin_face_off.png':  gerar_pumpkin_face_off(),
        'hay_block_top.png':     gerar_hay_block_top(),
        'hay_block_side.png':    gerar_hay_block_side(),
        'melon_top.png':         gerar_melon_top(),
        'melon_side.png':        gerar_melon_side(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
