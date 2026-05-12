"""
Block Round — temp/extract_textures.py

Decodes every base64 PNG in js/textures.js and writes upscaled copies to
temp/textures-hires/<key>.png so the user can hand them to GPT (or any
image model) and request stylistic variations.

Upscale rule: nearest-neighbour 16x (so 16x16 -> 256x256, 16x48 magma ->
256x768). Nearest-neighbour preserves the pixel-art look — bilinear
would soften the edges, which defeats the purpose.

Run from the worktree root:

    python temp/extract_textures.py
"""
import base64
import os
import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is required: pip install Pillow", file=sys.stderr)
    sys.exit(1)

# Each source pixel becomes UPSCALE x UPSCALE pixels. 16 → 256 px per
# source pixel-row gives plenty of room for GPT-style edits.
UPSCALE = 16

ROOT = Path(__file__).resolve().parent.parent
TEX_JS = ROOT / "js" / "textures.js"
OUT_DIR = ROOT / "temp" / "textures-hires"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Permissive matcher: <key>: 'data:image/png;base64,<payload>',
PATTERN = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*'data:image/png;base64,([^']+)'",
    re.MULTILINE,
)

def main():
    src = TEX_JS.read_text(encoding="utf-8")
    matches = PATTERN.findall(src)
    if not matches:
        print("No textures found in", TEX_JS, file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(matches)} textures. Writing to {OUT_DIR}")
    written = 0
    skipped = 0
    for key, b64 in matches:
        try:
            raw = base64.b64decode(b64)
        except Exception as e:
            print(f"  [skip] {key}: decode failed ({e})")
            skipped += 1
            continue
        out = OUT_DIR / f"{key}.png"
        try:
            # Pillow can read PNG bytes directly via BytesIO; resize using
            # nearest-neighbour to keep crisp pixel edges.
            import io
            img = Image.open(io.BytesIO(raw))
            img.load()
            w, h = img.size
            big = img.resize((w * UPSCALE, h * UPSCALE), Image.NEAREST)
            big.save(out, "PNG")
            print(f"  {key:<30}  {w}x{h}  -> {w*UPSCALE}x{h*UPSCALE}")
            written += 1
        except Exception as e:
            print(f"  [skip] {key}: {e}")
            skipped += 1

    print(f"\nDone. Wrote {written} files, skipped {skipped}.")

if __name__ == "__main__":
    main()
