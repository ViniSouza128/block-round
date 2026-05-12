"""Familia 07_ores_stone_matrix — 7 minerios em matriz de stone.

Cada ore = matriz cinza padrao (gerada por gen_stone.gerar_matriz_stone)
+ inclusoes especificas. A matriz de fundo e PIXEL-PERFECT identica
entre stone.png e qualquer ore_*.png — so a camada de inclusoes muda.

Estrutura: as inclusoes sao definidas como "shapes" (lista de offsets
relativos + role) instanciadas em "clusters" (centro + shape). Cada
ore lista seus clusters em ORE_CLUSTERS.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.gen_stone import gerar_matriz_stone
from scripts.pixelart_pack.palette import (
    PALETA_ORE_COAL,
    PALETA_ORE_DIAMOND,
    PALETA_ORE_EMERALD,
    PALETA_ORE_GOLD,
    PALETA_ORE_IRON,
    PALETA_ORE_LAPIS,
    PALETA_ORE_REDSTONE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# ---------------------------------------------------------------------------
# Shapes de inclusao — (dx, dy, role)
# ---------------------------------------------------------------------------

# Mancha amorfa grande (~9 pixels) — coal usa
AMOEBA_GRANDE = [
    (-1, -1, 'sombra'), (0, -1, 'base'),  (1, -1, 'base'),
    (-2, 0,  'base'),   (-1, 0,  'base'), (0, 0,  'sombra'),
    (1, 0,  'base'),    (2, 0,  'base'),
    (-1, 1,  'base'),   (0, 1,  'base'),  (1, 1,  'base'),
    (0, 2,  'base'),
]

# Mancha amorfa media (~6 pixels) — iron/gold usam
AMOEBA_MEDIO = [
    (0, -1, 'base'),  (1, -1, 'base'),
    (-1, 0, 'base'),  (0, 0,  'sombra'), (1, 0,  'base'),
    (0, 1,  'base'),  (1, 1,  'base'),
]

# Cristal angular (~5 pixels com brilho central) — diamond/emerald usam
CRISTAL_ANGULAR = [
    (0, -1, 'base'),
    (-1, 0, 'base'), (0, 0, 'brilho'), (1, 0, 'sombra'),
    (0, 1,  'base'),
]

# Cristal pequeno mas com pirita — lapis usa
CRISTAL_LAPIS = [
    (-1, -1, 'base'),  (0, -1, 'base'),
    (-1, 0,  'brilho'),(0, 0,  'base'), (1, 0, 'sombra'),
    (0, 1,   'base'),
]

# Pontos pequenos (~3 pixels) — redstone usa (gemas espalhadas)
PONTO_BRILHANTE = [
    (0, 0, 'base'),
    (1, 0, 'sombra'),
    (0, 1, 'sombra'),
    (-1, 0, 'brilho'),
]


# ---------------------------------------------------------------------------
# Posicoes de clusters por ore. (cx, cy, shape).
# Escolhidos para:
#   - cobrir ~20-30% da area (coal mais; cristais menos)
#   - distribuir bem (evitar empilhar todos no mesmo canto)
#   - tilear (clusters perto da borda repetem do outro lado)
# ---------------------------------------------------------------------------

ORE_CLUSTERS = {
    'coal': [
        (3,  3,  AMOEBA_GRANDE),
        (11, 5,  AMOEBA_GRANDE),
        (5,  11, AMOEBA_GRANDE),
        (13, 13, AMOEBA_GRANDE),
    ],
    'iron': [
        (3,  3,  AMOEBA_MEDIO),
        (10, 4,  AMOEBA_MEDIO),
        (5,  10, AMOEBA_MEDIO),
        (12, 12, AMOEBA_MEDIO),
        (8,  7,  AMOEBA_MEDIO),
    ],
    'gold': [
        (3,  3,  AMOEBA_MEDIO),
        (11, 4,  AMOEBA_MEDIO),
        (4,  10, AMOEBA_MEDIO),
        (12, 11, AMOEBA_MEDIO),
        (7,  7,  AMOEBA_MEDIO),
    ],
    'diamond': [
        (3,  3,  CRISTAL_ANGULAR),
        (11, 4,  CRISTAL_ANGULAR),
        (6,  8,  CRISTAL_ANGULAR),
        (12, 12, CRISTAL_ANGULAR),
        (3,  12, CRISTAL_ANGULAR),
    ],
    'emerald': [
        (3,  3,  CRISTAL_ANGULAR),
        (12, 4,  CRISTAL_ANGULAR),
        (7,  8,  CRISTAL_ANGULAR),
        (3,  11, CRISTAL_ANGULAR),
        (12, 12, CRISTAL_ANGULAR),
    ],
    'lapis': [
        (3,  3,  CRISTAL_LAPIS),
        (11, 4,  CRISTAL_LAPIS),
        (5,  9,  CRISTAL_LAPIS),
        (12, 11, CRISTAL_LAPIS),
    ],
    'redstone': [
        # redstone tem MAIS clusters (poeira espalhada)
        (2,  2,  PONTO_BRILHANTE),
        (6,  3,  PONTO_BRILHANTE),
        (11, 3,  PONTO_BRILHANTE),
        (14, 6,  PONTO_BRILHANTE),
        (4,  7,  PONTO_BRILHANTE),
        (9,  8,  PONTO_BRILHANTE),
        (2,  10, PONTO_BRILHANTE),
        (7,  11, PONTO_BRILHANTE),
        (12, 12, PONTO_BRILHANTE),
        (5,  14, PONTO_BRILHANTE),
    ],
}

# Para lapis, alguns clusters tem pontos de pirita amarelos sobrepostos
LAPIS_PIRITA_EXTRA = [
    (4, 2),
    (12, 5),
    (5, 11),
    (13, 10),
]


def _aplicar_clusters(img, clusters: list, paleta: dict) -> None:
    """Pinta cada (cx, cy, shape) na imagem usando a paleta dada."""
    for cx, cy, shape in clusters:
        for dx, dy, role in shape:
            helpers.px(img, cx + dx, cy + dy, paleta[role])


# ---------------------------------------------------------------------------
# Geradores por ore
# ---------------------------------------------------------------------------

def _ore_base(clusters_key: str, paleta: dict):
    img = helpers.nova_img(16, 16)
    gerar_matriz_stone(img)
    _aplicar_clusters(img, ORE_CLUSTERS[clusters_key], paleta)
    return img


def gerar_coal_ore():     return _ore_base('coal',     PALETA_ORE_COAL)
def gerar_iron_ore():     return _ore_base('iron',     PALETA_ORE_IRON)
def gerar_gold_ore():     return _ore_base('gold',     PALETA_ORE_GOLD)
def gerar_diamond_ore():  return _ore_base('diamond',  PALETA_ORE_DIAMOND)
def gerar_emerald_ore():  return _ore_base('emerald',  PALETA_ORE_EMERALD)
def gerar_redstone_ore(): return _ore_base('redstone', PALETA_ORE_REDSTONE)


def gerar_lapis_ore():
    img = _ore_base('lapis', PALETA_ORE_LAPIS)
    # pontos extras de pirita (amarelo dourado pontual)
    for x, y in LAPIS_PIRITA_EXTRA:
        helpers.px(img, x, y, PALETA_ORE_LAPIS['pirita'])
    return img


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'coal_ore.png':     gerar_coal_ore(),
        'iron_ore.png':     gerar_iron_ore(),
        'gold_ore.png':     gerar_gold_ore(),
        'diamond_ore.png':  gerar_diamond_ore(),
        'emerald_ore.png':  gerar_emerald_ore(),
        'lapis_ore.png':    gerar_lapis_ore(),
        'redstone_ore.png': gerar_redstone_ore(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
