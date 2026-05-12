"""Familia 08_deepslate — deepslate + 4 ores deepslate.

A matriz deepslate (rocha cinza-azul escura com estratificacao vertical
sutil) e gerada por `gerar_matriz_deepslate(img)` — funcao reutilizada
pelos ores. Os 4 ores compartilham os mesmos clusters/shapes de
gen_ores.py para coerencia: a mesma "geometria" de inclusao aparece em
stone e em deepslate, so muda a matriz de fundo.

Ores deepslate existentes em textures/: diamond, emerald, gold, iron.
Nao ha deepslate_coal/lapis/redstone na Mojang vanilla portada aqui.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.gen_ores import (
    ORE_CLUSTERS,
    _aplicar_clusters,
)
from scripts.pixelart_pack.palette import (
    PALETA_DEEPSLATE,
    PALETA_ORE_DIAMOND,
    PALETA_ORE_EMERALD,
    PALETA_ORE_GOLD,
    PALETA_ORE_IRON,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Padrao de ruido deepslate — estratificacao vertical sutil. Diferente
# do stone: predominam VERTICAIS de tons proximos, sugerindo camadas
# sedimentares. Cada coluna tem um tom "dominante" + variacao em y.
# Legenda:
#   . = meio       m = meio_escuro     M = meio_claro
#   d = escuro     b = claro           v = veio (estria mais escura)
DEEPSLATE_PATTERN = [
    '.m.M..m..M.m.M..',  # 0   (rows 0 e 15 identicas pra tilear topo/base)
    '.m..M.mM..m.M.m.',  # 1
    'vmM.M.dm.M.m.Md.',  # 2
    '.m.M.bm..M.dmM..',  # 3
    '.mM..M.mb.m.M.m.',  # 4
    '.dmM..m..Mvm.M.m',  # 5
    '.m..Md.m.M.m.M.b',  # 6
    'b.mM.m.M.mM.dm.M',  # 7
    '.m.M..vm.M.m.M.m',  # 8
    '.m.Md.m..M.bm.M.',  # 9
    '.mM..m.dM..m.Mv.',  # 10
    'vm..M.b.m.M.m.M.',  # 11
    '.mM..m..M.dm.M.m',  # 12
    '.m.M..mb.M.m.M..',  # 13
    '.mvM..d..M.m.Mm.',  # 14
    '.m.M..m..M.m.M..',  # 15
]

_CH_TO_TOM = {
    '.': 'meio',
    'm': 'meio_escuro',
    'M': 'meio_claro',
    'd': 'escuro',
    'b': 'claro',
    'v': 'veio',
}


# ---------------------------------------------------------------------------
# Matriz reutilizavel
# ---------------------------------------------------------------------------

def gerar_matriz_deepslate(img) -> None:
    """Preenche `img` (16x16 RGBA) com a matriz deepslate padrao."""
    p = PALETA_DEEPSLATE
    for y, row in enumerate(DEEPSLATE_PATTERN):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_CH_TO_TOM[ch]])


def _deepslate_ore(clusters_key: str, paleta_ore: dict):
    img = helpers.nova_img(16, 16)
    gerar_matriz_deepslate(img)
    _aplicar_clusters(img, ORE_CLUSTERS[clusters_key], paleta_ore)
    return img


# ---------------------------------------------------------------------------
# Variantes
# ---------------------------------------------------------------------------

def gerar_deepslate():
    img = helpers.nova_img(16, 16)
    gerar_matriz_deepslate(img)
    return img


def gerar_deepslate_diamond_ore(): return _deepslate_ore('diamond', PALETA_ORE_DIAMOND)
def gerar_deepslate_emerald_ore(): return _deepslate_ore('emerald', PALETA_ORE_EMERALD)
def gerar_deepslate_gold_ore():    return _deepslate_ore('gold',    PALETA_ORE_GOLD)
def gerar_deepslate_iron_ore():    return _deepslate_ore('iron',    PALETA_ORE_IRON)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'deepslate.png':              gerar_deepslate(),
        'deepslate_diamond_ore.png':  gerar_deepslate_diamond_ore(),
        'deepslate_emerald_ore.png':  gerar_deepslate_emerald_ore(),
        'deepslate_gold_ore.png':     gerar_deepslate_gold_ore(),
        'deepslate_iron_ore.png':     gerar_deepslate_iron_ore(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
