"""Familia 13_nether — 5 PNGs (soul_sand fica em gen_granular).

  - netherrack.png         rocha vermelha base
  - nether_bricks.png      tijolos vermelho-escuros com rejunte
  - magma.png              STRIP 16x48 (3 frames de animacao — cracks
                           de lava se movendo lentamente)
  - shroomlight.png        cogumelo luminoso laranja-amarelo brilhante
  - crying_obsidian.png    obsidian roxo escuro com lagrimas magenta
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from PIL import Image

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_CRYING_OBSIDIAN,
    PALETA_MAGMA,
    PALETA_NETHER_BRICKS,
    PALETA_NETHER_RACK,
    PALETA_SHROOMLIGHT,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# ---------------------------------------------------------------------------
# Netherrack — vermelho-tijolo medio com manchas
# ---------------------------------------------------------------------------

NETHERRACK_PATTERN = [
    '.M.e..p..M..e.M.',  # 0
    'e.M..M.p.e.M..pM',
    '.M.p.e.M..p.M.e.',
    'M.e..M.e.M.e.p.M',
    '.p..eM..M.p.M..e',
    'M.M.eM.p.M.M.e.M',
    '..p.M..eM.e.M.M.',
    'M.e..p.M.eM.p..M',
    '.M.M.e..pM.e.M.p',
    'e..p.M.M.e..pM..',
    '.M.eM..p.M.e.M.M',
    'M.e..pM.eM..M..p',
    '.M..e.p.M.e.M.M.',
    'e.M..M.p.eM..p.M',
    '.M.eMp..eM.M.M.M',
    '.M.e..p..M..e.M.',  # 15  — identica a row 0
]
_KEY_NETHER = {'.': 'base', 'M': 'claro', 'e': 'escuro', 'p': 'pedra'}


def gerar_netherrack():
    p = PALETA_NETHER_RACK
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(NETHERRACK_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_KEY_NETHER[ch]])
    return img


# ---------------------------------------------------------------------------
# Nether bricks — tijolos pequenos com rejunte horizontal/vertical
# ---------------------------------------------------------------------------

def gerar_nether_bricks():
    p = PALETA_NETHER_BRICKS
    img = helpers.nova_img(16, 16)
    # base preenchida com rejunte
    helpers.fill(img, p['rejunte'])

    # tijolos 4x3 px com offset alternado por fileira
    # Fileira A (y=0..2): tijolos x=[0..3], [5..8], [10..13], [15..15+0]
    # Para tilear, ultimo tijolo "wrappa" — vou colocar 3 tijolos completos
    # + 1 truncado, com tijolo do tile seguinte completando o ciclo.
    fileiras = [
        # (y0, y1, lista de (x0, x1))
        (0,  2,  [(0, 3),  (5, 8),  (10, 13)]),       # fileira A — sem offset
        (4,  6,  [(0, 1),  (3, 6),  (8, 11), (13, 15)]),  # offset
        (8,  10, [(0, 3),  (5, 8),  (10, 13)]),
        (12, 14, [(0, 1),  (3, 6),  (8, 11), (13, 15)]),
    ]
    for y0, y1, tijs in fileiras:
        for x0, x1 in tijs:
            for yy in range(y0, y1 + 1):
                for xx in range(x0, x1 + 1):
                    helpers.px(img, xx, yy, p['tijolo'])
            # highlight no topo
            for xx in range(x0, x1 + 1):
                helpers.px(img, xx, y0, p['tijolo_claro'])
            # sombra no fundo
            for xx in range(x0, x1 + 1):
                helpers.px(img, xx, y1, p['tijolo_escuro'])
    return img


# ---------------------------------------------------------------------------
# Magma strip — 16x48 = 3 frames empilhados (top->bottom).
# Cada frame: rocha escura + cracks laranja-amarelo brilhante. Os 3
# frames mostram a lava se movendo (cracks deslocadas levemente entre
# eles).
# ---------------------------------------------------------------------------

# Padrao base por frame — mesmo "fundo" de pedra escura.
MAGMA_PEDRA_BASE = [
    'PpP.P.pPp.P.P.pP',  # 0
    'pPpPp.PpP.pPp.Pp',
    'P.pP.PpP.PpP.pPp',
    'pPpP.PpP.pPp.PpP',
    'P.pPpPp.PpP.pPp.',
    'pPp.P.pPp.P.P.pP',
    'P.pP.pPp.PpP.PpP',
    'pPpPp.PpP.pPp.Pp',
    'P.pP.PpP.PpP.pPp',
    'pPpP.PpP.pPp.PpP',
    'P.pPpPp.PpP.pPp.',
    'pPp.P.pPp.P.P.pP',
    'P.pP.pPp.PpP.PpP',
    'pPpPp.PpP.pPp.Pp',
    'P.pP.PpP.PpP.pPp',
    'PpP.P.pPp.P.P.pP',  # 15  — identica a row 0
]
_KEY_MAGMA_BASE = {'.': 'pedra', 'P': 'pedra', 'p': 'pedra_clara'}

# Cracks por frame — cada frame tem cracks levemente deslocadas.
# crack: lista de (x, y, tom) onde tom in {'lava', 'lava_quente', 'lava_escura'}.
CRACKS_FRAMES = [
    # frame 0
    [(2, 1, 'lava_escura'), (3, 2, 'lava'), (4, 2, 'lava_quente'), (5, 3, 'lava'),
     (10, 5, 'lava_escura'), (11, 6, 'lava'), (12, 6, 'lava_quente'), (13, 7, 'lava'),
     (1, 9, 'lava_escura'), (2, 10, 'lava'), (3, 10, 'lava_quente'), (4, 11, 'lava'),
     (8, 12, 'lava_escura'), (9, 13, 'lava'), (10, 13, 'lava_quente'), (11, 14, 'lava')],
    # frame 1 — cracks deslocadas 1 pixel
    [(3, 1, 'lava_escura'), (4, 2, 'lava'), (5, 2, 'lava_quente'), (6, 3, 'lava'),
     (11, 5, 'lava_escura'), (12, 6, 'lava'), (13, 6, 'lava_quente'), (14, 7, 'lava'),
     (2, 9, 'lava_escura'), (3, 10, 'lava'), (4, 10, 'lava_quente'), (5, 11, 'lava'),
     (9, 12, 'lava_escura'), (10, 13, 'lava'), (11, 13, 'lava_quente'), (12, 14, 'lava')],
    # frame 2 — mais movimento, +brilho
    [(4, 1, 'lava'), (5, 2, 'lava_quente'), (6, 2, 'lava_quente'), (7, 3, 'lava'),
     (12, 5, 'lava'), (13, 6, 'lava_quente'), (14, 6, 'lava_quente'), (15, 7, 'lava'),
     (3, 9, 'lava'), (4, 10, 'lava_quente'), (5, 10, 'lava_quente'), (6, 11, 'lava'),
     (10, 12, 'lava'), (11, 13, 'lava_quente'), (12, 13, 'lava_quente'), (13, 14, 'lava')],
]


def _gerar_magma_frame(idx_frame: int):
    """Gera um frame 16x16 do magma."""
    p = PALETA_MAGMA
    img = helpers.nova_img(16, 16)
    # base de pedra
    for y, row in enumerate(MAGMA_PEDRA_BASE):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_KEY_MAGMA_BASE[ch]])
    # cracks do frame correspondente
    for x, y, tom in CRACKS_FRAMES[idx_frame]:
        helpers.px(img, x, y, p[tom])
    return img


def gerar_magma():
    """Strip 16x48 — 3 frames empilhados verticalmente."""
    strip = Image.new('RGBA', (16, 48), (0, 0, 0, 0))
    for i in range(3):
        frame = _gerar_magma_frame(i)
        strip.paste(frame, (0, i * 16), frame)
    return strip


# ---------------------------------------------------------------------------
# Shroomlight — cogumelo luminoso laranja-amarelo brilhante
# ---------------------------------------------------------------------------

SHROOM_PATTERN = [
    'CcCC.cCc.CcCC.cC',  # 0
    'cCcc.CcC.cCc.Ccc',
    '.CcC.cCc.CcC.cCC',
    'cCcc.CcC.cCc.Ccc',
    'CcCC.cCc.CcCC.cC',  # 4
    'cCcc.CcC.cCc.Ccc',
    '.CcCxCcc.CcC.cCC',  # x = cap (highlight no centro)
    'cCccxCcCxcCc.Ccc',
    'CcCCxcCcxCcCC.cC',
    'cCcc.CcCxcCc.Ccc',
    '.CcC.cCc.CcC.cCC',
    'cCcc.CcC.cCc.Ccc',
    'CcCC.cCc.CcCC.cC',
    'cCcc.CcC.cCc.Ccc',
    '.CcC.cCc.CcC.cCC',
    'CcCC.cCc.CcCC.cC',  # 15  — identica a row 0
]
_KEY_SHROOM = {'.': 'base', 'C': 'claro', 'c': 'escuro', 'x': 'cap'}


def gerar_shroomlight():
    p = PALETA_SHROOMLIGHT
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(SHROOM_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_KEY_SHROOM[ch]])
    return img


# ---------------------------------------------------------------------------
# Crying obsidian — base obsidian roxo escuro + lagrimas magenta vivas
# ---------------------------------------------------------------------------

CRYING_PATTERN = [
    '.M.e..M..e.M..e.',  # 0
    'M.M.e.M.M.e.M.e.',
    '.eM..eM..M.eM..M',
    'M.e.M.e.M.M.e.M.',
    '.M..M.e.M.eM..eM',
    'eM.M..M..eM.M.e.',
    '.e..M.eM..M.eM.M',
    'M.M.eM.M..eM..eM',
    '.M.e..M..M.eM.M.',
    'M..M.M.e.M..M.eM',
    '.eM..eM..eM.M.e.',
    'M.M.e.M.M.M.e.eM',
    '.M..M.eM.eM..M.e',
    'eM.M..M..eM.eM.M',
    '.e..M.eM..M.eM.e',
    '.M.e..M..e.M..e.',  # 15  — identica a row 0
]
_KEY_CRYING = {'.': 'base', 'M': 'claro', 'e': 'escuro'}

# Lagrimas: posicoes fixas com gota magenta + halo claro
LAGRIMAS = [
    (3,  4,  'lagrima'),   (3,  5,  'lagrima_claro'),
    (8,  2,  'lagrima'),   (8,  3,  'lagrima_claro'),
    (13, 6,  'lagrima'),   (13, 7,  'lagrima_claro'),
    (5,  10, 'lagrima'),   (5,  11, 'lagrima_claro'),
    (11, 12, 'lagrima'),   (11, 13, 'lagrima_claro'),
]


def gerar_crying_obsidian():
    p = PALETA_CRYING_OBSIDIAN
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(CRYING_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_KEY_CRYING[ch]])
    for x, y, tom in LAGRIMAS:
        helpers.px(img, x, y, p[tom])
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'netherrack.png':       gerar_netherrack(),
        'nether_bricks.png':    gerar_nether_bricks(),
        'magma.png':            gerar_magma(),
        'shroomlight.png':      gerar_shroomlight(),
        'crying_obsidian.png':  gerar_crying_obsidian(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        marca = f' ({img.size})' if img.size != (16, 16) else ''
        print(f'  gerado {out.relative_to(REPO_ROOT)}{marca}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
