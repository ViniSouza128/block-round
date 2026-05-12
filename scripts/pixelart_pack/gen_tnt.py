"""Gera as 3 faces do TNT em textures-pixelart/ (rodada 0 — POC).

Modelo:
  - SIDE   16x16 : faixas marrom (y=0, y=15) + corpo vermelho granulado
                   (y=1..4 e y=11..14) + faixa creme central (y=5..10)
                   com texto "TNT" 4x5 centralizado em y=6..10.
  - TOP    16x16 : faixas marrom + corpo vermelho granulado em y=1..14 +
                   pavio em forma de losango/estrela com faisca laranja
                   no centro (area ~8x8 em x=4..11, y=4..11).
  - BOTTOM 16x16 : padrao de tijolinhos 3x2 alternando 2 tons de vermelho,
                   com rejunte vermelho-escuro de 1 px entre tijolos.

Sem aleatoriedade: todos os padroes sao listas fixas pra que rodar duas
vezes produza PNGs identicos.
"""

from __future__ import annotations

import sys
from pathlib import Path

# permite execucao direta como script
if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import PALETA_TNT


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


# ---------------------------------------------------------------------------
# Padroes fixos de granulado
# ---------------------------------------------------------------------------

# Cada chave e a linha y; 's' = pixels sombreados, 'b' = pixels brilhantes.
# Cobrem y=1..4 (sob a faixa marrom superior) e y=11..14 (sob a inferior).
GRANULADO_SIDE = {
    1:  {'s': [2, 7, 13],         'b': [4, 10]},
    2:  {'s': [0, 5, 9, 14],      'b': [1, 7, 12]},
    3:  {'s': [3, 8, 11],         'b': [5, 13]},
    4:  {'s': [1, 6, 10, 15],     'b': [0, 8, 14]},
    11: {'s': [2, 6, 12],         'b': [4, 9, 14]},
    12: {'s': [0, 8, 13],         'b': [1, 5, 11]},
    13: {'s': [4, 9, 15],         'b': [2, 7, 12]},
    14: {'s': [1, 6, 10],         'b': [0, 3, 8, 14]},
}

# TOP — granulado em toda a area entre as faixas (y=1..14).
GRANULADO_TOP = {
    1:  {'s': [2, 7, 13],     'b': [4, 10, 15]},
    2:  {'s': [0, 5, 9, 14],  'b': [1, 7, 12]},
    3:  {'s': [3, 8, 11],     'b': [5, 13]},
    4:  {'s': [1, 6, 15],     'b': [0, 9, 14]},
    5:  {'s': [4, 12],        'b': [2, 7, 14]},
    6:  {'s': [0, 8, 13],     'b': [3, 10, 15]},
    7:  {'s': [5, 9, 14],     'b': [1, 12]},
    8:  {'s': [1, 6, 11],     'b': [3, 9, 14]},
    9:  {'s': [4, 8, 15],     'b': [2, 10, 13]},
    10: {'s': [0, 7, 12],     'b': [5, 11, 14]},
    11: {'s': [3, 9, 15],     'b': [1, 6, 13]},
    12: {'s': [5, 10, 14],    'b': [0, 8, 12]},
    13: {'s': [2, 7, 11],     'b': [4, 9, 15]},
    14: {'s': [0, 6, 13],     'b': [1, 8, 14]},
}


# ---------------------------------------------------------------------------
# Faces
# ---------------------------------------------------------------------------

def gerar_side() -> 'object':
    """SIDE: corpo vermelho com faixas marrom + label creme com TNT."""
    p = PALETA_TNT
    img = helpers.nova_img(16, 16)

    # faixas marrom topo (y=0) e base (y=15)
    helpers.faixa_horizontal(img, 0,  p['topo_escuro'], p['topo_claro'], [1, 3, 6, 9, 12, 14])
    helpers.faixa_horizontal(img, 15, p['topo_escuro'], p['topo_claro'], [0, 2, 5, 8, 11, 13])

    # corpo vermelho granulado em y=1..4 e y=11..14
    helpers.granulado(img, GRANULADO_SIDE, p['corpo_base'], p['corpo_sombra'], p['corpo_brilho'])

    # faixa creme central (y=5..10) — fundo do "label"
    for y in range(5, 11):
        helpers.linha_h(img, y, p['label_fundo'])

    # borda do label (linhas y=5 e y=10 com pixels de borda)
    for x in range(16):
        helpers.px(img, x, 5,  p['label_borda'])
        helpers.px(img, x, 10, p['label_borda'])

    # texto "TNT" em glifo 4x5, centralizado em y=6..10
    # 3 letras de 4px + 2 espacos de 1px = 14px -> margem 1px cada lado
    helpers.desenhar_glifo_3x5(img, helpers.GLIFOS_4x5['T'],  1, 6, p['texto'])
    helpers.desenhar_glifo_3x5(img, helpers.GLIFOS_4x5['N'],  6, 6, p['texto'])
    helpers.desenhar_glifo_3x5(img, helpers.GLIFOS_4x5['T'], 11, 6, p['texto'])

    return img


def gerar_top() -> 'object':
    """TOP: corpo vermelho granulado + pavio em losango/estrela no centro."""
    p = PALETA_TNT
    img = helpers.nova_img(16, 16)

    # faixas marrom em y=0 e y=15 (mesmo padrao do side pra coerencia visual)
    helpers.faixa_horizontal(img, 0,  p['topo_escuro'], p['topo_claro'], [1, 3, 6, 9, 12, 14])
    helpers.faixa_horizontal(img, 15, p['topo_escuro'], p['topo_claro'], [0, 2, 5, 8, 11, 13])

    # corpo vermelho granulado em y=1..14
    helpers.granulado(img, GRANULADO_TOP, p['corpo_base'], p['corpo_sombra'], p['corpo_brilho'])

    # pavio: losango/estrela em x=4..11, y=4..11, com faisca no centro
    # forma de losango (estrela de 4 pontas) + cruz central
    losango = {
        4:  [7, 8],
        5:  [6, 7, 8, 9],
        6:  [5, 6, 9, 10],
        7:  [4, 5, 10, 11],
        8:  [4, 5, 10, 11],
        9:  [5, 6, 9, 10],
        10: [6, 7, 8, 9],
        11: [7, 8],
    }
    for y, xs in losango.items():
        for x in xs:
            helpers.px(img, x, y, p['pavio_meio'])

    # contorno escuro (1px externo do losango) — sombra na ponta direita/baixo
    contorno = {
        4:  [9],
        5:  [10],
        6:  [11],
        7:  [12],
        8:  [12],
        9:  [11],
        10: [10],
        11: [9],
    }
    for y, xs in contorno.items():
        for x in xs:
            helpers.px(img, x, y, p['pavio_escuro'])

    # faisca laranja no centro (~3x3 cruzado)
    helpers.px(img, 7, 7, p['pavio_brilho'])
    helpers.px(img, 8, 7, p['pavio_brilho'])
    helpers.px(img, 7, 8, p['pavio_brilho'])
    helpers.px(img, 8, 8, p['pavio_brilho'])
    helpers.px(img, 6, 7, p['corpo_brilho'])  # halo
    helpers.px(img, 9, 8, p['corpo_brilho'])

    return img


def gerar_bottom() -> 'object':
    """BOTTOM: padrao de tijolinhos 3x2 alternando 2 tons de vermelho."""
    p = PALETA_TNT
    img = helpers.nova_img(16, 16)

    # tijolos 3px largura x 2px altura (mais rejunte de 1px). Linhas
    # alternam offset pra dar o classico padrao "bricks running bond".
    rejunte = p['corpo_sombra']
    a = p['corpo_base']
    b = p['corpo_brilho']

    tijolos: list[tuple[int, int, int, int]] = []
    cores: list[tuple] = []

    # 5 fileiras de tijolos com altura 3, separadas por rejunte de 1px:
    # y in [0..2], [3..5], [6..8], [9..11], [12..14], rejunte em 15
    # offset alternado nas fileiras pares vs impares
    for row, y in enumerate(range(0, 15, 3)):
        offset = 0 if row % 2 == 0 else 2
        # gera tijolos de 4px de largura + 1px rejunte = 5px de passo
        x = -offset
        idx = 0
        while x < 16:
            x0 = max(x, 0)
            x1 = min(x + 3, 15)
            if x1 >= x0:
                tijolos.append((x0, y, x1, y + 2))
                cores.append(a if (row + idx) % 2 == 0 else b)
            x += 5
            idx += 1

    helpers.mosaico(img, rejunte, tijolos, cores)

    # faixa marrom no rodape (y=15) — assinatura da "base de TNT"
    helpers.faixa_horizontal(img, 15, p['topo_escuro'], p['topo_claro'], [1, 4, 7, 10, 13])

    return img


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    faces = {
        'tnt_side.png':   gerar_side(),
        'tnt_top.png':    gerar_top(),
        'tnt_bottom.png': gerar_bottom(),
    }
    for nome, img in faces.items():
        out = DST_DIR / nome
        img.save(out)
        print(f'  gerado {out.relative_to(REPO_ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
