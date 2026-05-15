"""21_translucent (resto) — slime + honey (3 faces). Alpha preservado.

Glass ja foi gerado em gen_glass.py (rodada 3). Aqui ficam os 4 blocos
gelatinosos restantes.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import PALETA_HONEY, PALETA_SLIME


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Padrao base translucido — granulado leve com bolhas
TRANS_PATTERN = [
    '.M..e..M.M..e.M.',  # 0
    'M.M..eM..M.eM..M',
    '.eM..M..eM..M.eM',
    'M..eM..M.eM..M..',
    '.M..M.eM..M.eM.M',
    'M.eM..eM..M.eM.M',
    '.M..M.eM..M.eM..',
    'M..eM..M.eM..M.M',
    '.M.eM..M..M.eM.M',
    'M..M.eM..eM..M.e',
    '.eM..M.eM..M.eM.',
    'M..eM..M..M.eM.M',
    '.M.eM..M.eM..eM.',
    'M..M.eM..M.eM..M',
    '.eM..M.eM..M.eM.',
    '.M..e..M.M..e.M.',  # 15
]
_K_TRANS = {'.': 'base', 'M': 'claro', 'e': 'escuro'}


def _gerar_trans(paleta: dict, com_bolhas: bool, bolhas_chave: str = 'bolha'):
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(TRANS_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, paleta[_K_TRANS[ch]])
    # borda mais opaca nos 4 lados (sugere "skin" do bloco translucido)
    for k in range(16):
        helpers.px(img, k,  0,  paleta['borda'])
        helpers.px(img, k,  15, paleta['borda'])
        helpers.px(img, 0,  k,  paleta['borda'])
        helpers.px(img, 15, k,  paleta['borda'])
    if com_bolhas:
        # 4 bolhas circulares (pequenos discos 2x2) em posicoes fixas
        bolhas = [(4, 4), (11, 5), (5, 10), (12, 11)]
        for cx, cy in bolhas:
            for dx in (0, 1):
                for dy in (0, 1):
                    helpers.px(img, cx + dx, cy + dy, paleta[bolhas_chave])
    return img


def gerar_slime():
    """Slime — gel verde com bolhas internas."""
    return _gerar_trans(PALETA_SLIME, com_bolhas=True, bolhas_chave='bolha')


def gerar_honey_top():
    """Honey top — mel ambar com brilhos no topo."""
    return _gerar_trans(PALETA_HONEY, com_bolhas=True, bolhas_chave='brilho')


def gerar_honey_side():
    """Honey side — mel com brilho mais sutil."""
    img = _gerar_trans(PALETA_HONEY, com_bolhas=False)
    # gotas escorrendo (linhas verticais em x=4, x=11)
    p = PALETA_HONEY
    for x in (4, 11):
        for y in (3, 4, 5, 9, 10, 11):
            helpers.px(img, x, y, p['escuro'])
        helpers.px(img, x, 6,  p['brilho'])
        helpers.px(img, x, 12, p['brilho'])
    return img


def gerar_honey_bottom():
    """Honey bottom — mel mais escuro, sem brilho central."""
    img = _gerar_trans(PALETA_HONEY, com_bolhas=False)
    # 2 manchas escuras (sugerem o mel mais denso embaixo)
    p = PALETA_HONEY
    manchas = [(5, 5), (5, 6), (6, 5), (6, 6),
               (10, 9), (10, 10), (11, 9), (11, 10)]
    for x, y in manchas:
        helpers.px(img, x, y, p['escuro'])
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'slime.png':         gerar_slime(),
        'honey_top.png':     gerar_honey_top(),
        'honey_side.png':    gerar_honey_side(),
        'honey_bottom.png':  gerar_honey_bottom(),
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
