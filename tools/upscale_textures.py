"""Upscale every 16x16 PNG in textures/ to 1024x1024 with NEAREST-neighbor
so the pixel grid stays perfectly crisp (no antialiasing, no blur).

Animated frame strips (16xN where N is a multiple of 16) are split into
individual frames, each upscaled to 1024x1024 separately. This avoids
sending a tall strip to image-gen models that drift off the grid on
long aspect ratios.

Output goes to textures-1024/. Each pixel of the original becomes a solid
64x64 block in the output, so the simulated pixel-art resolution is
unambiguous when the file is fed to an image-gen model for variation.

Run from the project root:
    python tools/upscale_textures.py
"""

from __future__ import annotations
import pathlib
import sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "textures"
DST = ROOT / "textures-1024"
TARGET = 1024  # output dimension for one 16x16 face

def main() -> int:
    if not SRC.is_dir():
        print(f"ERROR: source folder not found: {SRC}", file=sys.stderr)
        return 1
    DST.mkdir(exist_ok=True)

    standard = 0
    strips = 0
    irregular = 0
    frames_total = 0

    for png in sorted(SRC.glob("*.png")):
        img = Image.open(png).convert("RGBA")
        w, h = img.size

        if w == 16 and h == 16:
            big = img.resize((TARGET, TARGET), Image.NEAREST)
            big.save(DST / png.name, optimize=True)
            standard += 1
            print(f"  {png.name:34s}  16x16 -> 1024x1024")
        elif w == 16 and h > 16 and h % 16 == 0:
            n = h // 16
            for i in range(n):
                frame = img.crop((0, i * 16, 16, (i + 1) * 16))
                big = frame.resize((TARGET, TARGET), Image.NEAREST)
                out = DST / f"{png.stem}_frame{i}.png"
                big.save(out, optimize=True)
            strips += 1
            frames_total += n
            print(f"  {png.name:34s}  16x{h} -> {n} frames @ 1024x1024")
        else:
            # Unexpected aspect — keep proportional, scale long side to TARGET.
            scale = TARGET / max(w, h)
            new_w = max(1, int(round(w * scale)))
            new_h = max(1, int(round(h * scale)))
            big = img.resize((new_w, new_h), Image.NEAREST)
            big.save(DST / png.name, optimize=True)
            irregular += 1
            print(f"  {png.name:34s}  {w}x{h} -> {new_w}x{new_h} (irregular)")

    print()
    print(f"Done. {standard} standard textures, {strips} animated strips "
          f"({frames_total} frames total), {irregular} irregular.")
    print(f"Output: {DST}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
