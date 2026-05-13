"""Familia 12 (resto) — superficies dirt/grass/podzol/mycelium/moss.

Inclui:
  - grass_block_top, grass_block_side
  - mycelium_top, mycelium_side
  - dirt_podzol_top, dirt_podzol_side  (note prefixo `dirt_` em textures/)
  - moss_block

Coerencia critica: a metade inferior (y=8..15) de TODOS os blocos
*_side e PIXEL-PERFECT igual a dirt.png — `gen_dirt.gerar_dirt(img,
y_inicio=8, y_fim=15)` faz isso.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.gen_dirt import gerar_dirt
from scripts.pixelart_pack.palette import (
    PALETA_GRASS,
    PALETA_MOSS,
    PALETA_MYCELIUM,
    PALETA_PODZOL,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# ---------------------------------------------------------------------------
# Padrao de "topo" — pontilhado uniforme tileavel
# ---------------------------------------------------------------------------

# Distribuicao 16x16 padrao: ~70% base, ~15% claro, ~12% escuro, ~3% destaque.
# Legenda comum: . = base, M = claro, e = escuro, d = destaque (agulha/ponto).
TOPO_PATTERN = [
    '.M..d..eM...e.M.',  # 0
    '.M.e..M..d..M.e.',  # 1
    'd.M.e..M..M.e..d',  # 2
    '..M.e.dM.e..M..M',  # 3
    'M..e.M..M.e..d.M',  # 4
    '.d..M..e.M..M..e',  # 5
    'M.e.M.dM.e..M..M',  # 6
    '..M.e..M..d.M.e.',  # 7
    'd..M..e.M..e.M..',  # 8
    '.M.e..M.dM..e..M',  # 9
    'M..e.M..M.e..M.d',  # 10
    '..M.e..d.M..M.e.',  # 11
    'M.e..M.eM..d.M..',  # 12
    '..M..e.dM.e..M.M',  # 13
    'd.M.e..M..M.e..d',  # 14
    '.M..d..eM...e.M.',  # 15  — identica a row 0
]
_KEY_TOP = {'.': 'base', 'M': 'claro', 'e': 'escuro', 'd': 'destaque'}


def _gerar_topo(paleta: dict, destaque_chave: str = 'claro'):
    """Pinta superficie tileavel com o padrao TOPO_PATTERN.

    `destaque_chave` define qual chave da paleta usar para 'd' — 'agulha'
    em podzol, 'ponto' em mycelium, etc. Famílias sem destaque proprio
    caem em 'claro'.
    """
    img = helpers.nova_img(16, 16)
    for y, row in enumerate(TOPO_PATTERN):
        for x, ch in enumerate(row):
            if ch == 'd':
                cor_chave = destaque_chave
            else:
                cor_chave = _KEY_TOP[ch]
            helpers.px(img, x, y, paleta[cor_chave])
    return img


# ---------------------------------------------------------------------------
# Side: metade superior surface + metade inferior dirt + transicao irregular
# ---------------------------------------------------------------------------

# Encroachments na transicao y=7 -> y=8. Listas de x onde:
#   - o "topo" desce 1 px (verde em y=8)
#   - o "dirt" sobe 1 px (marrom em y=7)
# Identicas pra todas as superficies pra que a "linha de transicao" seja
# visualmente coerente entre grass/podzol/mycelium.
_TOPO_DESCE_X = [1, 4, 9, 13]   # surface invade y=8
_DIRT_SOBE_X  = [2, 7, 11, 14]  # dirt invade y=7


def _gerar_side(paleta_topo: dict, destaque_chave: str = 'claro'):
    """Side block: surface em y=0..7 + dirt em y=8..15 + transicao."""
    img = helpers.nova_img(16, 16)

    # metade superior — replica TOPO_PATTERN apenas nas linhas 0..7
    for y in range(8):
        row = TOPO_PATTERN[y]
        for x, ch in enumerate(row):
            if ch == 'd':
                cor_chave = destaque_chave
            else:
                cor_chave = _KEY_TOP[ch]
            helpers.px(img, x, y, paleta_topo[cor_chave])

    # metade inferior — dirt pixel-perfect
    gerar_dirt(img, y_inicio=8, y_fim=15)

    # transicao irregular em y=7 / y=8
    cor_borda = paleta_topo.get('borda', paleta_topo['escuro'])
    # surface invade y=8
    for x in _TOPO_DESCE_X:
        helpers.px(img, x, 8, cor_borda)
    # linha y=7 ganha leve sombra escurecida (sugere "raiz" do gramado)
    for x in _DIRT_SOBE_X:
        # pixel marrom-escuro (importa de dirt.PALETA via paleta_topo? nao —
        # uso o tom escuro do topo invertido pro escuro)
        helpers.px(img, x, 7, cor_borda)

    return img


# ---------------------------------------------------------------------------
# Variantes
# ---------------------------------------------------------------------------

def gerar_grass_block_top():    return _gerar_topo(PALETA_GRASS)
def gerar_grass_block_side():   return _gerar_side(PALETA_GRASS)
def gerar_mycelium_top():       return _gerar_topo(PALETA_MYCELIUM, destaque_chave='ponto')
def gerar_mycelium_side():      return _gerar_side(PALETA_MYCELIUM, destaque_chave='ponto')
def gerar_dirt_podzol_top():    return _gerar_topo(PALETA_PODZOL,   destaque_chave='agulha')
def gerar_dirt_podzol_side():   return _gerar_side(PALETA_PODZOL,   destaque_chave='agulha')
def gerar_moss_block():         return _gerar_topo(PALETA_MOSS)


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'grass_block_top.png':   gerar_grass_block_top(),
        'grass_block_side.png':  gerar_grass_block_side(),
        'mycelium_top.png':      gerar_mycelium_top(),
        'mycelium_side.png':     gerar_mycelium_side(),
        'dirt_podzol_top.png':   gerar_dirt_podzol_top(),
        'dirt_podzol_side.png':  gerar_dirt_podzol_side(),
        'moss_block.png':        gerar_moss_block(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
