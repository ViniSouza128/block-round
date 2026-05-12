"""
Generate og-image.png — the link-preview image embedded via Open Graph /
Twitter Card meta tags in index.html. Regenerate by running:

    python scripts/generate_og_image.py

The output is committed to the repo root as og-image.png (referenced by
absolute URL in the meta tags, since WhatsApp won't fetch relative URLs).
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "og-image.png"

W, H = 1200, 630
# Block Round palette (matches style.css :root)
BG       = (26, 18, 8)        # --bg
SURFACE  = (42, 24, 8)        # --surface
BORDER   = (58, 36, 16)       # --border
TEXT     = (255, 244, 208)    # --text
MUTED    = (255, 232, 168)    # --text-muted
ACCENT   = (255, 236, 79)     # --accent
GRID     = (255, 236, 79, 28) # grid lines (translucent yellow)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")


def font(size, bold=True):
    name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


# --- LEFT PANEL: pixel circle preview ---------------------------------------
# 16x16 Euclidean filled circle — the canonical Block Round output.
GRID_N = 16
PANEL_X, PANEL_Y = 80, 95
PANEL_SIZE = 440
CELL = PANEL_SIZE // GRID_N

# panel background (canvas-like)
draw.rounded_rectangle(
    [PANEL_X - 14, PANEL_Y - 14,
     PANEL_X + PANEL_SIZE + 14, PANEL_Y + PANEL_SIZE + 14],
    radius=20, fill=SURFACE, outline=BORDER, width=2,
)

# grid
for i in range(GRID_N + 1):
    x = PANEL_X + i * CELL
    y = PANEL_Y + i * CELL
    draw.line([(x, PANEL_Y), (x, PANEL_Y + PANEL_SIZE)], fill=GRID, width=1)
    draw.line([(PANEL_X, y), (PANEL_X + PANEL_SIZE, y)], fill=GRID, width=1)

# Euclidean filled circle, diameter 16 → radius 8, center at (8,8)
cx = cy = GRID_N / 2.0
r = GRID_N / 2.0
for gy in range(GRID_N):
    for gx in range(GRID_N):
        dx = (gx + 0.5) - cx
        dy = (gy + 0.5) - cy
        if dx * dx + dy * dy <= r * r:
            x0 = PANEL_X + gx * CELL
            y0 = PANEL_Y + gy * CELL
            draw.rectangle(
                [x0 + 1, y0 + 1, x0 + CELL - 1, y0 + CELL - 1],
                fill=ACCENT,
            )

# --- RIGHT PANEL: title + tagline + url -------------------------------------
RX = 600

# small brand chip (hex logo mark + name) — matches the Block Round topbar SVG.
mark_cx, mark_cy, mark_r = RX + 22, 130, 20
hex_pts = []
for k in range(6):
    ang = math.pi / 3 * k - math.pi / 2
    hex_pts.append(
        (mark_cx + mark_r * math.cos(ang),
         mark_cy + mark_r * math.sin(ang))
    )
draw.polygon(hex_pts, fill=ACCENT, outline=(26, 14, 4))
# the Y-shape inside the hex
draw.line([hex_pts[5], (mark_cx, mark_cy)], fill=(26, 14, 4), width=2)
draw.line([hex_pts[1], (mark_cx, mark_cy)], fill=(26, 14, 4), width=2)
draw.line([(mark_cx, mark_cy), hex_pts[3]], fill=(26, 14, 4), width=2)

draw.text((mark_cx + mark_r + 14, mark_cy - 18), "BLOCK ROUND",
          font=font(22), fill=MUTED)

# Title — two lines for impact.
draw.text((RX, 185), "Pixel & voxel", font=font(66), fill=TEXT)
draw.text((RX, 265), "rounded shapes.", font=font(66), fill=ACCENT)

# Tagline
tagline = "Minecraft-flavoured 2D & 3D generator\nfor pixel-perfect circles and spheres."
draw.multiline_text((RX, 395), tagline, font=font(28, bold=False),
                    fill=MUTED, spacing=10)

# URL pill at bottom
url = "vinisouza128.github.io/block-round"
url_font = font(24)
bbox = draw.textbbox((0, 0), url, font=url_font)
url_w = bbox[2] - bbox[0]
url_h = bbox[3] - bbox[1]
pill_pad_x, pill_pad_y = 18, 12
pill_x, pill_y = RX, 520
draw.rounded_rectangle(
    [pill_x, pill_y,
     pill_x + url_w + pill_pad_x * 2,
     pill_y + url_h + pill_pad_y * 2],
    radius=999, fill=SURFACE, outline=BORDER, width=2,
)
draw.text((pill_x + pill_pad_x, pill_y + pill_pad_y - 4), url,
          font=url_font, fill=TEXT)

img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.1f} KB)")
