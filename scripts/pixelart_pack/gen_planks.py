"""Familia 01_planks — 6 madeiras, mesma estrutura de tabuas, so a cor muda.

Layout 16x16:
- 4 fileiras de tabuas, cada uma com 4 px de altura.
- Linha y=3, y=7, y=11, y=15 = SEPARADOR HORIZONTAL (escuro entre tabuas).
- Cada fileira tem UM separador vertical de 1 px em x distinto (offset
  staggered 4/8/12/4 entre fileiras), simulando emendas entre 2 tabuas
  no mesmo nivel.
- 1-2 nos pequenos por fileira em posicoes fixas.

Tileabilidade: separadores horizontais ficam em y=15 (e y=3,7,11 internos);
quando tilear, y=15 do tile atual encosta em y=0 do proximo, que e madeira
base — luma_dist controlado dentro do limite.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_PLANKS_ACACIA,
    PALETA_PLANKS_BIRCH,
    PALETA_PLANKS_DARK_OAK,
    PALETA_PLANKS_JUNGLE,
    PALETA_PLANKS_OAK,
    PALETA_PLANKS_SPRUCE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Definicao das 4 fileiras de tabuas. Cada tupla:
#   (y0, y1, separador_x, [(no_x, no_y), ...])
# y0..y1 inclusive (3px de madeira), separador horizontal em y1+1.
# Layout escolhido para tilear topo/base: separadores horizontais ficam
# em y={3, 7, 11} (apenas internos); y=0 e y=15 sao madeira. Tabua 1 e
# Tabua 4 sao verticalmente "metades" — quando o tile e empilhado
# verticalmente, a tabua 4 (y=12..15) encontra a tabua 1 (y=0..2) do
# tile de cima e juntas formam a tabua de 4-px completa.
_FILEIRAS = [
    (0,  2,  4,  [(2, 1), (10, 0)]),    # tabua 1 — 3 px
    (4,  6,  8,  [(3, 5), (13, 4)]),    # tabua 2
    (8,  10, 12, [(2, 9), (6, 8)]),     # tabua 3
    (12, 15, 4,  [(9, 13), (14, 12)]),  # tabua 4 — 4 px (ate borda)
]

# Padroes de "veias" claros/escuros dentro de cada tabua, por linha relativa.
# rel_y in {0,1,2}; valor = lista de (x, tom) onde tom in {'M','e'}.
_VEIAS = {
    0: [(1, 'M'), (5, 'e'), (7, 'M'), (11, 'e'), (15, 'M')],
    1: [(0, 'e'), (3, 'M'), (6, 'e'), (9, 'M'), (12, 'e')],
    2: [(2, 'e'), (5, 'M'), (8, 'e'), (11, 'M'), (14, 'e')],
}

_TOM_KEY = {'M': 'claro', 'e': 'escuro'}


def gerar_planks_base(paleta: dict):
    """Funcao reutilizada pelas 6 variantes — so a paleta muda."""
    p = paleta
    img = helpers.nova_img(16, 16)
    helpers.fill(img, p['base'])

    for y0, y1, sep_x, nos in _FILEIRAS:
        # veias claras e escuras dentro da tabua
        for rel_y in range(y1 - y0 + 1):
            yy = y0 + rel_y
            for x, ch in _VEIAS.get(rel_y, []):
                helpers.px(img, x, yy, p[_TOM_KEY[ch]])

        # separador vertical (emenda) — 1 px na largura
        for yy in range(y0, y1 + 1):
            helpers.px(img, sep_x, yy, p['separador'])

        # linha separadora horizontal abaixo (y1+1)
        for x in range(16):
            helpers.px(img, x, y1 + 1, p['separador'])

        # nos: pixel central escuro + halo claro ao redor
        for nx, ny in nos:
            helpers.px(img, nx, ny, p['no_escuro'])
            # halo: 1 pixel a direita ou abaixo (se ainda dentro da tabua)
            if nx + 1 < 16 and nx + 1 != sep_x:
                helpers.px(img, nx + 1, ny, p['no_claro'])

    return img


# ---------------------------------------------------------------------------
# Variantes
# ---------------------------------------------------------------------------

def gerar_oak_planks():      return gerar_planks_base(PALETA_PLANKS_OAK)
def gerar_birch_planks():    return gerar_planks_base(PALETA_PLANKS_BIRCH)
def gerar_spruce_planks():   return gerar_planks_base(PALETA_PLANKS_SPRUCE)
def gerar_jungle_planks():   return gerar_planks_base(PALETA_PLANKS_JUNGLE)
def gerar_acacia_planks():   return gerar_planks_base(PALETA_PLANKS_ACACIA)
def gerar_dark_oak_planks(): return gerar_planks_base(PALETA_PLANKS_DARK_OAK)


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'oak_planks.png':      gerar_oak_planks(),
        'birch_planks.png':    gerar_birch_planks(),
        'spruce_planks.png':   gerar_spruce_planks(),
        'jungle_planks.png':   gerar_jungle_planks(),
        'acacia_planks.png':   gerar_acacia_planks(),
        'dark_oak_planks.png': gerar_dark_oak_planks(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
