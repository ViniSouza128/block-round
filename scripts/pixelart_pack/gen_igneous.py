"""Familia 06_igneous — andesite, diorite, granite, polished_andesite.

Cada uma tem paleta propria (cinza/branco/rosa-bege) mas o conceito
"speckled" e identico: base + 2 tons proximos + 2 pontos contrastantes
(preto + branco) numa distribuicao fina. Polished_andesite usa a paleta
do andesite com superficie lisa + sutil grade de blocos cortados.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import (
    PALETA_IGNEOUS_ANDESITE,
    PALETA_IGNEOUS_DIORITE,
    PALETA_IGNEOUS_GRANITE,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# Mapa de distribuicao "speckled" comum a andesite, diorite e granite.
# Cada caractere indica o tom (so a mapeacao chave->cor muda por familia):
#   . = base       m = meio (tom proximo da base)        M = claro
#   k = ponto_preto                                       w = ponto_branco
#   c = ponto_cinza (so granite usa, demais ignoram convertendo p/ meio)
# Padrao desenhado para parecer rocha speckled de granulometria fina,
# tileavel (col 0 ~= col 15 em luminosidade, idem topo/base).
SPECKLED_PATTERN = [
    '.M.k..w...M..k..',  # 0
    'm....M.k....w...',  # 1
    '..w....m...k....',  # 2
    'M..k...w.m......',  # 3
    '....m....M..k...',  # 4
    '.k....M...m...w.',  # 5
    'M.w...k.....m..M',  # 6
    '...m......w..k..',  # 7
    'k....M.m..w.....',  # 8
    '.w.M....k.....m.',  # 9
    '...k....w...M..k',  # 10
    'M..m...M...w....',  # 11
    '..w...k.m....M..',  # 12
    'k..M.....w....k.',  # 13
    '.m...w....M..m..',  # 14
    '...M.k...m..w...',  # 15
]

# Granite tem distribuicao um pouco diferente — mais densa de pontos
# brancos e cinzas (e nao usa diorite/andesite-style "speckled medio").
GRANITE_PATTERN = [
    '.cM..c.w...M.c..',  # 0  — rows 0/15 identicas pra tilear topo/base
    'M..c..w...kc....',  # 1
    '..k..M...w....cm',  # 2
    'c.M.w....M..k...',  # 3
    '...m..c.k.....c.',  # 4  — w final virou c (col 14 mais calma)
    'c.k....M...c.M..',  # 5  — col 0 w virou c
    '..M..w.c....k...',  # 6
    'c....k....w.M..c',  # 7  — col 15 k virou c
    '.w.M..c....M...c',  # 8  — col 15 w virou c
    '.k.....w.c.k....',  # 9
    'M..c.M....m..c.M',  # 10
    '..w.k....w...M..',  # 11
    'c..M.c.M..c....c',  # 12 — col 0/15 k virou c
    '.c.....k.M.w....',  # 13
    '..M.w....c..k.M.',  # 14
    '.cM..c.w...M.c..',  # 15 — identica a row 0
]


def _paint_speckled(img, pattern, paleta: dict, ch_map: dict) -> None:
    """Pinta o pattern usando o mapeamento de caracteres."""
    for y, row in enumerate(pattern):
        for x, ch in enumerate(row):
            helpers.px(img, x, y, paleta[ch_map[ch]])


# ---------------------------------------------------------------------------
# Variantes
# ---------------------------------------------------------------------------

def gerar_andesite():
    p = PALETA_IGNEOUS_ANDESITE
    img = helpers.nova_img(16, 16)
    helpers.fill(img, p['base'])
    ch_map = {
        '.': 'base',
        'm': 'meio',
        'M': 'claro',
        'k': 'ponto_preto',
        'w': 'ponto_branco',
        'c': 'meio',  # andesite nao usa cinza extra
    }
    _paint_speckled(img, SPECKLED_PATTERN, p, ch_map)
    return img


def gerar_diorite():
    p = PALETA_IGNEOUS_DIORITE
    img = helpers.nova_img(16, 16)
    helpers.fill(img, p['base'])
    ch_map = {
        '.': 'base',
        'm': 'meio',
        'M': 'claro',
        'k': 'ponto_preto',
        'w': 'ponto_branco',
        'c': 'meio',
    }
    _paint_speckled(img, SPECKLED_PATTERN, p, ch_map)
    return img


def gerar_granite():
    p = PALETA_IGNEOUS_GRANITE
    img = helpers.nova_img(16, 16)
    helpers.fill(img, p['base'])
    ch_map = {
        '.': 'base',
        'm': 'meio',
        'M': 'claro',
        'k': 'ponto_preto',
        'w': 'ponto_branco',
        'c': 'ponto_cinza',
    }
    _paint_speckled(img, GRANITE_PATTERN, p, ch_map)
    return img


def gerar_polished_andesite():
    """Andesite polido — base uniforme + grade sutil em formato de blocos cortados."""
    p = PALETA_IGNEOUS_ANDESITE
    img = helpers.nova_img(16, 16)
    helpers.fill(img, p['base'])

    # leve variacao interna pra evitar parecer chapado
    pontilhado = {
        2:  [4, 11],
        5:  [2, 9, 14],
        9:  [3, 12],
        12: [6, 10],
        14: [4, 13],
    }
    for y, xs in pontilhado.items():
        for x in xs:
            helpers.px(img, x, y, p['claro'])

    # grade de blocos cortados — uma linha vertical em x=8 e horizontal em y=8
    # com pixels mais escuros sutis (~moldura) — sugere blocos 8x8
    for k in range(16):
        helpers.px(img, 8, k, p['moldura'])
        helpers.px(img, k, 8, p['moldura'])
    # cruz fica meio chamativa — quebra com 2 highlights de cada lado
    for k in (3, 12):
        helpers.px(img, 8, k, p['meio'])
        helpers.px(img, k, 8, p['meio'])

    return img


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'andesite.png':          gerar_andesite(),
        'diorite.png':           gerar_diorite(),
        'granite.png':           gerar_granite(),
        'polished_andesite.png': gerar_polished_andesite(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
