"""glass.png — vidro com moldura clara + interior transparente.

Critico: a maior parte da textura e (0,0,0,0). So a moldura externa
(perimetro) e algumas linhas internas tem pixels visiveis. O original
da Mojang tem 191 pixels com alpha < 255 (quase 75% transparente).
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers
from scripts.pixelart_pack.palette import PALETA_GLASS


REPO_ROOT = Path(__file__).resolve().parents[2]
DST_DIR = REPO_ROOT / 'textures-pixelart'


def gerar_glass():
    p = PALETA_GLASS
    img = helpers.nova_img(16, 16)  # comeca totalmente transparente

    # moldura externa contornando o bloco inteiro (top + bottom + esq + dir)
    for k in range(16):
        helpers.px(img, k,  0,  p['moldura_externa'])
        helpers.px(img, k,  15, p['moldura_externa'])
        helpers.px(img, 0,  k,  p['moldura_externa'])
        helpers.px(img, 15, k,  p['moldura_externa'])

    # 2 linhas internas (vertical + horizontal) sugerindo "corte" no meio
    # — semi-transparentes (alpha 220 via moldura_interna)
    for k in range(2, 14):
        helpers.px(img, k, 7, p['moldura_interna'])
        helpers.px(img, 7, k, p['moldura_interna'])

    # 4 highlights nos cantos internos (sugerem reflexo)
    for cx, cy in ((1, 1), (14, 1), (1, 14), (14, 14)):
        helpers.px(img, cx, cy, p['highlight'])

    # 2 highlights extras na moldura sugerem brilho (visual de vidro)
    helpers.px(img, 4, 0,  p['highlight'])
    helpers.px(img, 0, 4,  p['highlight'])
    helpers.px(img, 11, 15, p['highlight'])
    helpers.px(img, 15, 11, p['highlight'])

    return img


def main() -> int:
    DST_DIR.mkdir(parents=True, exist_ok=True)
    img = gerar_glass()
    out = DST_DIR / 'glass.png'
    img.save(out)
    n_alpha = sum(1 for px in img.getdata() if px[3] < 255)
    print(f'  gerado {out.relative_to(REPO_ROOT)} (alpha_px={n_alpha})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
