"""Familia 12 (parcial) — dirt.png + funcao reutilizavel para a "metade dirt"
dos blocos side (grass_block_side, mycelium_side, dirt_podzol_side).

Exporta `gerar_dirt(img, y_inicio=0, y_fim=15)` — pinta o intervalo
vertical [y_inicio..y_fim] com o padrao dirt deterministico, EXATAMENTE
identico ao que `dirt.png` recebe na faixa correspondente. Assim a
metade inferior dos *_side blocks e pixel-perfect igual a dirt.png
naquela faixa.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import PALETA_DIRT


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Padrao 16x16 deterministico. Legenda:
#   . = base    M = claro    e = escuro    p = pedrinha    r = raiz_clara
# Distribuicao: ~60% base, ~15% claro, ~15% escuro, ~7% pedrinha, ~3% raiz.
# Tileavel: row 0 == row 15 (identicas) e luma_dist controlado nas col 0/15.
DIRT_PATTERN = [
    '.M.e..p..M..e.M.',  # 0
    'e.M..M..p.e.M..r',  # 1
    '.M..p.M..e..M..e',  # 2
    'M.e.M.p..M.e..M.',  # 3
    '.p..M.e.M..p..e.',  # 4
    'M.M.e..M.r.M.e.M',  # 5
    '..p.M..e..M..M.p',  # 6
    'M.e..p.M..e.M..M',  # 7
    '.M.M..e..p..M.e.',  # 8
    'e..M.p..M.e..M.M',  # 9
    '.p.M.e..M..p.M..',  # 10
    'M.e..M.p..M.e..p',  # 11
    '.M..p.e..M.r.M.M',  # 12
    'e.M..M.e..p..e.M',  # 13
    '.M.p..M..e..M.M.',  # 14
    '.M.e..p..M..e.M.',  # 15  — identica a row 0
]

_CH_TO_TOM = {
    '.': 'base',
    'M': 'claro',
    'e': 'escuro',
    'p': 'pedrinha',
    'r': 'raiz_clara',
}


def gerar_dirt(img, y_inicio: int = 0, y_fim: int = 15) -> None:
    """Pinta a faixa [y_inicio..y_fim] de `img` com o padrao dirt padrao.

    Usado por:
      - gen_dirt.gerar_dirt_full() (faixa completa 0..15)
      - gen_surfaces.gerar_grass_side / mycelium_side / podzol_side
        (faixa 8..15 — metade inferior)
    A regiao fora da faixa nao e tocada.
    """
    p = PALETA_DIRT
    for y in range(max(0, y_inicio), min(15, y_fim) + 1):
        row = DIRT_PATTERN[y]
        for x, ch in enumerate(row):
            helpers.px(img, x, y, p[_CH_TO_TOM[ch]])


def gerar_dirt_full():
    img = helpers.nova_img(16, 16)
    gerar_dirt(img, 0, 15)
    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    img = gerar_dirt_full()
    out = DST_DIR / 'dirt.png'
    img.save(out)
    print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
