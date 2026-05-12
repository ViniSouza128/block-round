"""Familia 05_stone_family — stone, smooth_stone, cobblestone, mossy_cobblestone.

Exporta `gerar_matriz_stone(img)` — funcao reutilizada por `gen_ores.py`
para garantir que a matriz de fundo dos ores seja pixel-perfect identica
a `stone.png`.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import PALETA_STONE


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Padrao de ruido fixo (determinismo total). Cada caractere mapeia
# pra um tom da PALETA_STONE. Escolhido a mao para:
#   - parecer pedra rugosa MC sem repeticao obvia
#   - tilear (luma_dist entre col 0 e col 15 < 60 em todas as linhas;
#     idem topo/base) — confirmado por verify.py
# Legenda:  . = meio   m = meio_escuro   M = meio_claro   d = escuro   b = claro
STONE_PATTERN = [
    '.m..M.d...m..M..',   # 0
    'M..m...b.m......',   # 1   (col15 = '.', col0 = 'M') — luma diff 24, ok
    '...m..M...d.m...',   # 2
    '.m.....m.M...b..',   # 3
    '..M..d..M..m....',   # 4
    'm...b..M....m.d.',   # 5
    '...m.....m.M....',   # 6
    'M.d...m........m',   # 7
    '.m..M....b.m...M',   # 8
    '....m.......d...',   # 9
    'm..d...M.m...b..',   # 10
    '..M..m........mM',   # 11
    'd........m..M...',   # 12
    '.m....b.....m...',   # 13
    '...M...m..d.m..M',   # 14
    '..m..d.......m..',   # 15
]

# Mapeamento caractere -> chave de PALETA_STONE
_CH_TO_TOM = {
    '.': 'meio',
    'm': 'meio_escuro',
    'M': 'meio_claro',
    'd': 'escuro',
    'b': 'claro',
}


# ---------------------------------------------------------------------------
# Matriz reutilizavel
# ---------------------------------------------------------------------------

def gerar_matriz_stone(img) -> None:
    """Preenche `img` (16x16 RGBA) com a matriz de pedra cinza padrao.

    Reutilizavel: chame em qualquer imagem 16x16 e o resultado e sempre
    o mesmo conjunto de 256 pixels. Os ores em `gen_ores.py` chamam isto
    primeiro e depois aplicam suas proprias inclusoes por cima.
    """
    p = PALETA_STONE
    for y, row in enumerate(STONE_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_CH_TO_TOM[ch]])


# ---------------------------------------------------------------------------
# Quatro variantes
# ---------------------------------------------------------------------------

def gerar_stone():
    img = helpers.nova_img(16, 16)
    gerar_matriz_stone(img)
    return img


def gerar_smooth_stone():
    """Mais homogeneo que stone + moldura escura fina (marca de cocao)."""
    p = PALETA_STONE
    img = helpers.nova_img(16, 16)

    # base uniforme em meio
    helpers.fill(img, p['meio'])

    # leves variacoes (~10% pixels) — mantem cara de pedra cozida
    suaves = {
        2:  {'M': [3, 11],            'm': [7]},
        5:  {'M': [1, 14],            'm': [6, 9]},
        8:  {'M': [4],                'm': [2, 11, 13]},
        11: {'M': [7, 12],            'm': [3, 9]},
        13: {'M': [5],                'm': [11]},
    }
    for y, marcas in suaves.items():
        for x in marcas.get('M', []):
            helpers.px(img, x, y, p['meio_claro'])
        for x in marcas.get('m', []):
            helpers.px(img, x, y, p['meio_escuro'])

    # moldura escura de 1 px nos 4 lados
    for k in range(16):
        helpers.px(img, k,  0,  p['moldura'])
        helpers.px(img, k,  15, p['moldura'])
        helpers.px(img, 0,  k,  p['moldura'])
        helpers.px(img, 15, k,  p['moldura'])

    return img


# Layout das 9 pedras do cobblestone — coordenadas (x0, y0, x1, y1).
# Bordas esq/dir/topo/base ficam todas em argamassa (col 0, col 15,
# row 0, row 15) — assim a textura tilea sem costura.
_COBBLE_RECTS = [
    # Fileira A (y=1..5), 3 pedras de larguras 3/5/4
    ((1,  1, 3,  5), 'meio'),         # A1 3x5
    ((5,  1, 9,  5), 'meio_claro'),   # A2 5x5
    ((11, 1, 14, 5), 'meio_escuro'),  # A3 4x5
    # Fileira B (y=7..9), 3 pedras 4/3/5
    ((1,  7, 4,  9),  'meio_escuro'),
    ((6,  7, 8,  9),  'meio'),
    ((10, 7, 14, 9),  'meio_claro'),
    # Fileira C (y=11..14), 3 pedras 5/4/3
    ((1,  11, 5,  14), 'meio_claro'),
    ((7,  11, 10, 14), 'meio_escuro'),
    ((12, 11, 14, 14), 'meio'),
]

# Sombras (canto inferior-direito) e highlights (canto superior-esquerdo)
# por pedra. Posicoes calculadas em runtime — vide gerar_cobblestone.


def gerar_cobblestone():
    p = PALETA_STONE
    img = helpers.nova_img(16, 16)
    helpers.fill(img, p['argamassa'])

    for (x0, y0, x1, y1), tom_chave in _COBBLE_RECTS:
        cor_base = p[tom_chave]
        # preenche corpo da pedra
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                helpers.px(img, xx, yy, cor_base)
        # highlight na linha superior (1 px do topo)
        for xx in range(x0, x1):
            helpers.px(img, xx, y0, p['claro'])
        # sombra na linha inferior + coluna direita
        for xx in range(x0 + 1, x1 + 1):
            helpers.px(img, xx, y1, p['escuro'])
        for yy in range(y0 + 1, y1 + 1):
            helpers.px(img, x1, yy, p['escuro'])

    return img


# Posicoes fixas de manchas de musgo (~30% area). Cada tupla = (x, y, tom)
# onde tom in {'musgo', 'musgo_claro', 'musgo_escuro'}.
_MUSGO_POSICOES = [
    # Cluster superior-esquerdo (em torno de pedra A1)
    (1, 1, 'musgo'),  (2, 1, 'musgo_claro'),  (3, 2, 'musgo'),
    (1, 3, 'musgo_escuro'), (2, 4, 'musgo'),  (3, 5, 'musgo_claro'),
    # Cluster topo-centro (em torno de A2)
    (6, 1, 'musgo'),  (7, 2, 'musgo_claro'),  (8, 1, 'musgo'),
    (9, 3, 'musgo_escuro'),
    # Cluster topo-direito (A3)
    (12, 2, 'musgo_claro'), (13, 3, 'musgo'), (14, 4, 'musgo_escuro'),
    # Cluster centro-esquerdo (B1)
    (1, 8, 'musgo'),  (2, 7, 'musgo_claro'),  (3, 9, 'musgo_escuro'),
    # Cluster centro-direito (B3)
    (11, 7, 'musgo'), (12, 8, 'musgo_claro'), (13, 9, 'musgo'),
    (14, 7, 'musgo_escuro'),
    # Cluster inferior-esquerdo (C1)
    (2, 12, 'musgo_claro'), (3, 13, 'musgo'), (1, 14, 'musgo_escuro'),
    (4, 11, 'musgo'),
    # Cluster inferior-centro (C2)
    (7, 12, 'musgo'), (8, 13, 'musgo_claro'), (9, 14, 'musgo_escuro'),
    # Cluster inferior-direito (C3)
    (12, 12, 'musgo'), (13, 13, 'musgo_claro'),
]


def gerar_mossy_cobblestone():
    img = gerar_cobblestone()
    p = PALETA_STONE
    for x, y, tom in _MUSGO_POSICOES:
        helpers.px(img, x, y, p[tom])
    return img


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'stone.png':             gerar_stone(),
        'smooth_stone.png':      gerar_smooth_stone(),
        'cobblestone.png':       gerar_cobblestone(),
        'mossy_cobblestone.png': gerar_mossy_cobblestone(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
