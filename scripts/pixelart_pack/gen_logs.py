"""Familia 02_logs — 15 arquivos = 6 especies x {side, top} +
duplicatas de naming antigo (`log_*` == `*_log`).

Funcoes compartilhadas:
- `gerar_casca_log(paleta)` — vista lateral, grao VERTICAL.
- `gerar_anel_log(paleta)` — corte transversal, aneis concentricos.

Para birch, `paleta['bandas']` lista as linhas y onde desenhar listras
pretas horizontais (icone visual da bidoeira).

Mapeamento de nomes (textures/ tem 15 arquivos por causa de 2 convencoes
de naming legadas):

  oak       side: oak_log.png
            top:  oak_log_top.png
  birch     side: birch_log.png == log_birch.png
            top:  log_birch_top.png
  spruce    side: spruce_log.png == log_spruce.png
            top:  log_spruce_top.png
  acacia    side: log_acacia.png
            top:  log_acacia_top.png
  jungle    side: log_jungle.png
            top:  log_jungle_top.png
  dark_oak  side: dark_oak_log.png == log_big_oak.png
            top:  log_big_oak_top.png

Os arquivos com 2 nomes recebem bytes IDENTICOS.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_LOG_ACACIA,
    PALETA_LOG_BIRCH,
    PALETA_LOG_DARK_OAK,
    PALETA_LOG_JUNGLE,
    PALETA_LOG_OAK,
    PALETA_LOG_SPRUCE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# ---------------------------------------------------------------------------
# CASCA (side) — grao vertical
# ---------------------------------------------------------------------------

# Tones por coluna. 'b' = casca_base, 'C' = casca_claro, 'e' = casca_escuro.
# Distribuicao escolhida pra parecer estriacao vertical natural.
_CASCA_COLUNAS = 'bCbeb.bCbe.bCbeb'
_KEY_CASCA = {
    'b': 'casca_base',
    '.': 'casca_base',
    'C': 'casca_claro',
    'e': 'casca_escuro',
}

# Nos (knots) — pixels escuros isolados em posicoes fixas.
_CASCA_NOS = [(2, 4), (10, 11), (14, 7)]

# Variacoes por linha — 'patch' onde uma coluna troca temporariamente
# pra outro tom (sugere irregularidade do grao).
_CASCA_VARIACOES = {
    1:  [(7, 'C'), (12, 'e')],
    3:  [(4, 'C')],
    5:  [(0, 'C'), (9, 'e')],
    7:  [(5, 'C')],
    9:  [(1, 'e'), (13, 'C')],
    11: [(7, 'C')],
    13: [(3, 'e'), (10, 'C')],
}


def gerar_casca_log(paleta: dict):
    """Vista lateral do log — grao vertical + nos opcionais + bandas (birch)."""
    p = paleta
    img = helpers.nova_img(16, 16)

    # base por coluna
    for x, ch in enumerate(_CASCA_COLUNAS):
        cor = p[_KEY_CASCA[ch]]
        for y in range(16):
            helpers.px(img, x, y, cor)

    # variacoes por linha
    for y, perturb in _CASCA_VARIACOES.items():
        for x, ch in perturb:
            helpers.px(img, x, y, p[_KEY_CASCA[ch]])

    # nos
    for nx, ny in _CASCA_NOS:
        helpers.px(img, nx, ny, p['casca_no'])
        # halo ao redor (1 px diagonal claro)
        if nx + 1 < 16 and ny + 1 < 16:
            helpers.px(img, nx + 1, ny + 1, p['casca_escuro'])

    # bandas horizontais — apenas birch (paleta tem chave 'bandas')
    bandas = p.get('bandas')
    if bandas:
        for y in bandas:
            for x in range(16):
                helpers.px(img, x, y, p['casca_no'])

    return img


# ---------------------------------------------------------------------------
# TOP (anel) — corte transversal, aneis concentricos
# ---------------------------------------------------------------------------

def gerar_anel_log(paleta: dict):
    """Corte transversal — aneis concentricos centrados em (7.5, 7.5)."""
    p = paleta
    img = helpers.nova_img(16, 16)

    # paleta de aneis em ordem de fora pra dentro
    cores_aneis = [
        p['miolo_borda'],   # borda externa (casca)
        p['miolo_escuro'],  # anel escuro
        p['miolo_anel'],    # anel base
        p['miolo_centro'],  # centro claro
        p['miolo_anel'],    # anel base novamente (centro tem 1 anel a mais)
        p['miolo_centro'],
    ]

    # distancia chebyshev a (7.5, 7.5) define qual anel cada pixel pertence
    for y in range(16):
        for x in range(16):
            dx = abs(x - 7.5)
            dy = abs(y - 7.5)
            d = max(dx, dy)
            # mapeia distancia pra indice de anel
            if d >= 7.5:
                idx = 0  # borda
            elif d >= 5.5:
                idx = 1
            elif d >= 3.5:
                idx = 2
            elif d >= 2.5:
                idx = 3
            elif d >= 1.5:
                idx = 4
            else:
                idx = 5
            helpers.px(img, x, y, cores_aneis[idx])

    # Adiciona um "pith" central (o ponto central da arvore) — 1 pixel
    # mais escuro no centro pra dar referencia visual.
    helpers.px(img, 7, 7, p['miolo_escuro'])
    helpers.px(img, 8, 8, p['miolo_escuro'])

    return img


# ---------------------------------------------------------------------------
# Mapeamento especie -> arquivos
# ---------------------------------------------------------------------------

# (paleta, side_filenames, top_filenames)
_ESPECIES = [
    (PALETA_LOG_OAK,      ['oak_log.png'],                         ['oak_log_top.png']),
    (PALETA_LOG_BIRCH,    ['birch_log.png', 'log_birch.png'],      ['log_birch_top.png']),
    (PALETA_LOG_SPRUCE,   ['spruce_log.png', 'log_spruce.png'],    ['log_spruce_top.png']),
    (PALETA_LOG_ACACIA,   ['log_acacia.png'],                       ['log_acacia_top.png']),
    (PALETA_LOG_JUNGLE,   ['log_jungle.png'],                       ['log_jungle_top.png']),
    (PALETA_LOG_DARK_OAK, ['dark_oak_log.png', 'log_big_oak.png'], ['log_big_oak_top.png']),
]


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for paleta, side_files, top_files in _ESPECIES:
        img_side = gerar_casca_log(paleta)
        img_top = gerar_anel_log(paleta)
        for nome in side_files:
            out = DST_DIR / nome
            img_side.save(out)
            print(f'  gerado {out.relative_to(REPO_ROOT)}')
            total += 1
        for nome in top_files:
            out = DST_DIR / nome
            img_top.save(out)
            print(f'  gerado {out.relative_to(REPO_ROOT)}')
            total += 1
    print(f'  total: {total} arquivos')
    return 0


if __name__ == '__main__':
    sys.exit(main())
