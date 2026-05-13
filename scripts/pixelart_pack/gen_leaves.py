"""Familia 03_leaves — leaves_oak.png (16x16, COM alpha).

Folhas de carvalho — aglomerado denso verde-medio com pixels mais claros
espalhados, alguns pixels translucidos (alpha 0) nas "frestas" entre
folhas para dar a sensacao de cluster com vazios. A textura original da
Mojang tem 84 pixels com alpha < 255; nossa versao tem ~78 pixels alpha=0
distribuidos pra dar o mesmo aspecto sem reproduzir o pattern exato.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import PALETA_LEAVES_OAK


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Padrao 16x16. Legenda:
#   . = base       M = claro       e = escuro     b = borda
#   _ = transparente (alpha 0) — frestas entre folhas
LEAVES_PATTERN = [
    'M.._.bM..eM_.M.b',  # 0
    '.Mb..M_e..M.b_.M',  # 1
    'b.Me.._M.b.eM..b',  # 2
    '.b._M.b.._Me.bM.',  # 3
    'M_.bM.._eM.b.._M',  # 4
    '.M.eb_M.b.M_eM.b',  # 5
    'b._M.b_.eMb.._Me',  # 6
    'M.b._Me.b._M.eb_',  # 7
    '_e.bM.._eM.b_M.M',  # 8
    'b.M._eM.b._M.eb_',  # 9
    'M_.b.M_eb._.bM.M',  # 10
    '.M_b.._M.beM.._b',  # 11
    'b.Me.._.MbM_.eMb',  # 12
    '.b.M_eb..M.bM_e.',  # 13
    'Me_.b.M_eb._.bM.',  # 14
    'M.._.bM..eM_.M.b',  # 15  — identica a row 0 (tilear topo/base)
]

_CH_TO_TOM = {
    '.': 'base',
    'M': 'claro',
    'e': 'escuro',
    'b': 'borda',
    '_': 'transparente',
}


def gerar_leaves_oak():
    p = PALETA_LEAVES_OAK
    img = helpers.nova_img(16, 16)  # ja comeca totalmente transparente
    for y, row in enumerate(LEAVES_PATTERN):
        for x, ch in enumerate(row):
            cor = p[_CH_TO_TOM[ch]]
            helpers.px(img, x, y, cor)
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    img = gerar_leaves_oak()
    out = DST_DIR / 'leaves_oak.png'
    img.save(out)
    n_alpha = sum(1 for px in img.getdata() if px[3] < 255)
    print(f'  gerado {out.relative_to(REPO_ROOT)} (alpha_px={n_alpha})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
