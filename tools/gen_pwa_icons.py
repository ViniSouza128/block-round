"""Generate PWA PNG icons from the favicon hexagon design.

Outputs (in ./icons/):
    icon-192.png            192x192 any-purpose (transparent bg)
    icon-512.png            512x512 any-purpose (transparent bg)
    icon-192-maskable.png   192x192 maskable (full bleed + safe zone)
    icon-512-maskable.png   512x512 maskable (full bleed + safe zone)
    apple-touch-icon.png    180x180 iOS home-screen icon (opaque bg)

Run from project root:
    python tools/gen_pwa_icons.py
"""

from __future__ import annotations
import pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT  = ROOT / 'icons'

YELLOW = (0xFF, 0xEC, 0x4F, 0xFF)
DARK   = (0x1A, 0x0E, 0x04, 0xFF)
BG     = (0x1A, 0x12, 0x08, 0xFF)

# Hexagon vertices in a 24x24 viewBox (matches favicon.svg).
HEX = [(12, 3), (21, 8), (21, 17), (12, 22), (3, 17), (3, 8)]
MID = (12, 13)   # back-center of the 3D-perspective hexagon


SS = 4   # supersample factor: render at 4x then LANCZOS-downscale for clean
         # anti-aliased edges and seamless line-joins at sharp vertices.


def draw_icon(size: int, *, opaque: bool, fill_ratio: float = 1.0) -> Image.Image:
    """Render the hexagon mark at `size`x`size`.

    fill_ratio < 1.0 shrinks the mark to leave a margin (used for maskable
    icons so launcher cropping never touches the logo). opaque draws the
    brand background underneath; transparent otherwise.
    """
    big = size * SS
    img = Image.new('RGBA', (big, big), BG if opaque else (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)

    # Map 24-unit viewBox → pixel space, then scale to fill_ratio and center.
    pad = (1 - fill_ratio) * big / 2
    scale = (big - 2 * pad) / 24
    def p(x, y):
        return (pad + x * scale, pad + y * scale)

    sw = max(2, int(round(2 * scale)))   # stroke width tracks viewBox "2"

    hex_px = [p(*v) for v in HEX]
    mid_px = p(*MID)

    # 1) yellow fill
    d.polygon(hex_px, fill=YELLOW)
    # 2) perspective folds inside (endpoints overshoot the border)
    d.line([p(3, 8), mid_px, p(21, 8)], fill=DARK, width=sw, joint='curve')
    d.line([mid_px, p(12, 22)],         fill=DARK, width=sw)
    # 3) hexagon outline LAST, mitred via Pillow 10+ width param — covers
    #    the overshoot from step 2 and gives every vertex a clean join.
    d.polygon(hex_px, fill=None, outline=DARK, width=sw)

    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    OUT.mkdir(exist_ok=True)

    specs = [
        ('icon-192.png',           192, False, 0.92),
        ('icon-512.png',           512, False, 0.92),
        # Maskable: full bleed background + mark inside the W3C safe zone
        # (content kept within a 80% diameter, so launcher crops never cut
        # the logo). 0.72 leaves ~14% padding on every side.
        ('icon-192-maskable.png',  192, True,  0.72),
        ('icon-512-maskable.png',  512, True,  0.72),
        # iOS home-screen icon — opaque, mark sized like the manifest "any".
        ('apple-touch-icon.png',   180, True,  0.86),
    ]

    for name, size, opaque, ratio in specs:
        img = draw_icon(size, opaque=opaque, fill_ratio=ratio)
        img.save(OUT / name, 'PNG', optimize=True)
        print(f'  wrote {OUT / name}  ({size}x{size}, opaque={opaque})')


if __name__ == '__main__':
    main()
