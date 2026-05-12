"""Helpers reutilizaveis para gerar PNGs pixel-a-pixel.

Convencao: todas as funcoes operam sobre PIL.Image em modo RGBA.
Cores sao tuplas (r, g, b, a). Coordenadas seguem (x, y) com origem
no canto superior esquerdo.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw


# ---------------------------------------------------------------------------
# Primitivas
# ---------------------------------------------------------------------------

def nova_img(w: int = 16, h: int = 16) -> Image.Image:
    """Cria uma imagem RGBA totalmente transparente."""
    return Image.new('RGBA', (w, h), (0, 0, 0, 0))


def fill(img: Image.Image, cor: tuple) -> None:
    """Preenche a imagem inteira com a cor dada."""
    ImageDraw.Draw(img).rectangle([0, 0, img.width - 1, img.height - 1], fill=cor)


def px(img: Image.Image, x: int, y: int, cor: tuple) -> None:
    """Acende um unico pixel — versao defensiva (ignora fora-de-bordas)."""
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), cor)


def linha_h(img: Image.Image, y: int, cor: tuple) -> None:
    """Pinta uma linha horizontal cheia em y."""
    for x in range(img.width):
        img.putpixel((x, y), cor)


# ---------------------------------------------------------------------------
# Padroes
# ---------------------------------------------------------------------------

def faixa_horizontal(
    img: Image.Image,
    y: int,
    cor_base: tuple,
    cor_textura: tuple,
    posicoes: Iterable[int],
) -> None:
    """Pinta a linha y inteira de cor_base e troca pixels listados por cor_textura."""
    linha_h(img, y, cor_base)
    for x in posicoes:
        px(img, x, y, cor_textura)


def granulado(
    img: Image.Image,
    padroes: dict,
    cor_base: tuple,
    cor_sombra: tuple,
    cor_brilho: tuple,
) -> None:
    """Pinta um corpo granulado a partir de um dict {linha: {'s':[...], 'b':[...]}}.

    Para cada linha y do dict, primeiro preenche com cor_base; depois marca
    os pixels listados em 's' (sombra) e 'b' (brilho). Padroes fixos
    garantem reprodutibilidade (sem RNG).
    """
    for y, marca in padroes.items():
        linha_h(img, y, cor_base)
        for x in marca.get('s', []):
            px(img, x, y, cor_sombra)
        for x in marca.get('b', []):
            px(img, x, y, cor_brilho)


def desenhar_glifo_3x5(
    img: Image.Image,
    glifo: list,
    x: int,
    y: int,
    cor: tuple,
) -> None:
    """Pinta um glifo descrito como lista de strings ('#' e '.') a partir de (x, y).

    Funciona com qualquer tamanho — o nome '3x5' e nominal. A largura
    do glifo e max(len(linha)); a altura e len(glifo).
    """
    for dy, linha in enumerate(glifo):
        for dx, ch in enumerate(linha):
            if ch == '#':
                px(img, x + dx, y + dy, cor)


# Glifos minimos para o POC do TNT — 4x5 funcionam melhor pra caber 3 letras
# em 16px (12px de letras + 2px de margem cada lado, mais 1px de espaco).
GLIFOS_4x5 = {
    'T': [
        '####',
        '.##.',
        '.##.',
        '.##.',
        '.##.',
    ],
    'N': [
        '#..#',
        '##.#',
        '#.##',
        '#..#',
        '#..#',
    ],
}


def mosaico(
    img: Image.Image,
    cor_rejunte: tuple,
    tijolos: list,
    cores_alternadas: list,
) -> None:
    """Pinta padrao de tijolinhos.

    `tijolos` e uma lista de retangulos [(x0, y0, x1, y1), ...]. A cor de
    cada tijolo vem de `cores_alternadas` ciclicamente. Antes de qualquer
    tijolo, a imagem inteira e preenchida com `cor_rejunte` — assim os
    espacos entre tijolos viram rejunte automaticamente.
    """
    fill(img, cor_rejunte)
    draw = ImageDraw.Draw(img)
    for i, (x0, y0, x1, y1) in enumerate(tijolos):
        draw.rectangle([x0, y0, x1, y1], fill=cores_alternadas[i % len(cores_alternadas)])


# ---------------------------------------------------------------------------
# Validacao / QA
# ---------------------------------------------------------------------------

def tile_check(img: Image.Image) -> list:
    """Valida tileabilidade. Retorna lista de erros (vazia = ok).

    Critica: a textura sera repetida no jogo, entao a coluna esquerda
    deve casar com a direita E a linha superior com a inferior — mas o
    padrao precisa fluir, nao ser identico pixel-a-pixel. Aqui exigimos
    apenas que NAO existam descontinuidades visuais grandes: comparamos
    os pixels da borda oposta como referencia e contamos diferencas.
    """
    erros = []
    w, h = img.width, img.height

    diff_hv = sum(
        1 for y in range(h)
        if img.getpixel((0, y)) != img.getpixel((w - 1, y)) and
           _luma_dist(img.getpixel((0, y)), img.getpixel((w - 1, y))) > 60
    )
    diff_vh = sum(
        1 for x in range(w)
        if img.getpixel((x, 0)) != img.getpixel((x, h - 1)) and
           _luma_dist(img.getpixel((x, 0)), img.getpixel((x, h - 1))) > 60
    )

    if diff_hv > h // 3:
        erros.append(f'borda esq/dir descasada em {diff_hv}/{h} linhas (limite {h // 3})')
    if diff_vh > w // 3:
        erros.append(f'borda topo/base descasada em {diff_vh}/{w} colunas (limite {w // 3})')

    return erros


def _luma_dist(c1: tuple, c2: tuple) -> float:
    """Distancia perceptual aproximada entre duas cores RGBA."""
    return abs(c1[0] - c2[0]) * 0.3 + abs(c1[1] - c2[1]) * 0.59 + abs(c1[2] - c2[2]) * 0.11


def preview_4x(input_path: str, output_path: str, escala: int = 4) -> None:
    """Salva uma versao ampliada (nearest-neighbor) do PNG para visualizacao humana."""
    src = Image.open(input_path)
    big = src.resize((src.width * escala, src.height * escala), Image.NEAREST)
    big.save(output_path)


def comparar_grid(
    originais: list,
    novas: list,
    output_path: str,
    cols: int = 8,
    escala: int = 8,
    pad: int = 4,
    rotulos: list | None = None,
) -> None:
    """Cria grid antes/depois ampliado lado-a-lado.

    originais e novas sao listas paralelas de caminhos. Cada par vira uma
    celula com a textura original a esquerda e a nova a direita.
    """
    assert len(originais) == len(novas), 'listas precisam ter o mesmo tamanho'
    n = len(originais)
    if rotulos is None:
        rotulos = [Path(p).stem for p in novas]

    cell_tex = 16 * escala
    cell_w = cell_tex * 2 + pad * 3
    cell_h = cell_tex + pad * 2 + 14
    rows = (n + cols - 1) // cols
    grid_w = cell_w * min(n, cols) + pad
    grid_h = cell_h * rows + pad

    out = Image.new('RGBA', (grid_w, grid_h), (24, 18, 12, 255))
    draw = ImageDraw.Draw(out)

    for i, (orig_p, nova_p) in enumerate(zip(originais, novas)):
        row, col = divmod(i, cols)
        x0 = pad + col * cell_w
        y0 = pad + row * cell_h

        for k, p in enumerate((orig_p, nova_p)):
            img = Image.open(p).convert('RGBA')
            # se for strip vertical 16xN, recorta apenas o frame 0 (top 16x16)
            if img.width == 16 and img.height > 16:
                img = img.crop((0, 0, 16, 16))
            big = img.resize((cell_tex, cell_tex), Image.NEAREST)
            out.paste(big, (x0 + pad + k * (cell_tex + pad), y0 + pad), big)

        draw.text((x0 + pad, y0 + cell_tex + pad), rotulos[i][:24], fill=(255, 244, 208, 255))

    out.save(output_path)
