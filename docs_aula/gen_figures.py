# -*- coding: utf-8 -*-
"""Gerador de figuras para o Plano de Aula do Block Round.

Renderiza 2D circles/ellipses e 3D voxels com texturas reais de
Minecraft. Em 3D usa perspective warp para projetar a textura
em cada uma das tres faces visiveis do voxel (top, lit side, dark side).
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
TEX_DIR = HERE.parent.parent.parent.parent / "textures"
IMG_DIR = HERE / "img"
IMG_DIR.mkdir(parents=True, exist_ok=True)

BG = (251, 246, 233, 255)
OVERLAY = (0, 0, 0, 200)

def load_tex(name):
    return Image.open(TEX_DIR / f"{name}.png").convert("RGBA")

# ===========================================================================
# 2D rasterizers (identicos ao app)
# ===========================================================================
def euclidean_2d(D):
    R = D / 2.0
    cells = set()
    for j in range(D):
        for i in range(D):
            dx = (i + 0.5) - R; dy = (j + 0.5) - R
            if dx*dx + dy*dy <= R*R:
                cells.add((i, j))
    return cells

def bresenham_2d(D):
    R = int(round(D / 2.0))
    contour = set()
    x, y, d = 0, R, 1 - R
    while x <= y:
        offset = 0 if D % 2 else 0
        for sx in (-1, 1):
            for sy in (-1, 1):
                contour.add((R + sx*x - (1 if sx < 0 else 0), R + sy*y - (1 if sy < 0 else 0)))
                contour.add((R + sx*y - (1 if sx < 0 else 0), R + sy*x - (1 if sy < 0 else 0)))
        if d < 0: d += 2*x + 3
        else:    d += 2*(x - y) + 5; y -= 1
        x += 1
    cells = set()
    by_row = {}
    for (i, j) in contour:
        if 0 <= i < D and 0 <= j < D:
            by_row.setdefault(j, []).append(i)
    for j, xs in by_row.items():
        for i in range(min(xs), max(xs)+1):
            cells.add((i, j))
    return cells

def threshold_2d(D):
    R = D / 2.0
    cells = set()
    for j in range(D):
        for i in range(D):
            nx = max(i, min(R, i+1))
            ny = max(j, min(R, j+1))
            dx, dy = nx - R, ny - R
            if (dx*dx + dy*dy) / (R*R) <= 0.94:
                cells.add((i, j))
    return cells

def ellipse_2d(W, H):
    rx, ry = W/2.0, H/2.0
    cells = set()
    for j in range(H):
        for i in range(W):
            dx = ((i + 0.5) - rx) / rx
            dy = ((j + 0.5) - ry) / ry
            if dx*dx + dy*dy <= 1.0:
                cells.add((i, j))
    return cells

def shell_2d(cells):
    out = set()
    for (i, j) in cells:
        if any((i+di, j+dj) not in cells for (di, dj) in ((1,0),(-1,0),(0,1),(0,-1))):
            out.add((i, j))
    return out

def thick_2d(cells):
    shell = shell_2d(cells)
    bridges = set()
    for (i, j) in cells:
        if (i, j) in shell: continue
        hH = (i-1, j) in shell or (i+1, j) in shell
        hV = (i, j-1) in shell or (i, j+1) in shell
        if hH and hV: bridges.add((i, j))
    return shell | bridges

# ===========================================================================
# 2D rendering: tile texture into marked cells
# ===========================================================================
def render_2d(cells, W, H, tex, cell_px=48):
    out = Image.new("RGBA", (W*cell_px, H*cell_px), BG)
    tex_scaled = tex.resize((cell_px, cell_px), Image.NEAREST)
    for (i, j) in cells:
        out.paste(tex_scaled, (i*cell_px, j*cell_px), tex_scaled)
    draw = ImageDraw.Draw(out)
    for (i, j) in cells:
        x0, y0 = i*cell_px, j*cell_px
        x1, y1 = x0+cell_px-1, y0+cell_px-1
        if (i-1, j) not in cells: draw.line([(x0, y0), (x0, y1)], fill=OVERLAY, width=2)
        if (i+1, j) not in cells: draw.line([(x1, y0), (x1, y1)], fill=OVERLAY, width=2)
        if (i, j-1) not in cells: draw.line([(x0, y0), (x1, y0)], fill=OVERLAY, width=2)
        if (i, j+1) not in cells: draw.line([(x0, y1), (x1, y1)], fill=OVERLAY, width=2)
    return out

# ===========================================================================
# 3D voxelization
# ===========================================================================
def sphere_3d(D):
    R = D / 2.0
    v = set()
    for k in range(D):
        for j in range(D):
            for i in range(D):
                dx = ((i+0.5)-R)/R; dy = ((j+0.5)-R)/R; dz = ((k+0.5)-R)/R
                if dx*dx + dy*dy + dz*dz <= 1.0:
                    v.add((i,j,k))
    return v

def ellipsoid_3d(W, H, D):
    rx, ry, rz = W/2.0, H/2.0, D/2.0
    v = set()
    for k in range(D):
        for j in range(H):
            for i in range(W):
                dx = ((i+0.5)-rx)/rx; dy = ((j+0.5)-ry)/ry; dz = ((k+0.5)-rz)/rz
                if dx*dx + dy*dy + dz*dz <= 1.0:
                    v.add((i,j,k))
    return v

def cut_y(v, frac=0.5):
    if not v: return v
    Dy = max(j for (_,j,_) in v) + 1
    return {p for p in v if p[1] < frac*Dy}

def cut_x(v, frac=0.5):
    if not v: return v
    Dx = max(i for (i,_,_) in v) + 1
    return {p for p in v if p[0] < frac*Dx}

def cut_diag(v, frac=0.5):
    if not v: return v
    Dx = max(i for (i,_,_) in v) + 1
    Dy = max(j for (_,j,_) in v) + 1
    return {p for p in v if (p[0]+p[1]) < frac*(Dx+Dy)}

# ===========================================================================
# 3D isometric rendering with perspective-warped textures
# ===========================================================================
# Isometric vectors (in pixels per voxel-unit):
#   +i (right-back):   (+dx,  +dy/2)
#   +k (right-front):  (+dx,  -dy/2)   we use -k instead -> (-dx, +dy/2)
#   +j (up):           (0,    -dy)
# Actually use: x = (i - k) * dx_iso, y = (i + k) * dy_iso/2 - j * dy_iso
# So +i moves right; +k moves left; +j moves up.

def render_iso(voxels, tex_top, tex_side, tex_front=None,
               canvas_w=900, canvas_h=750, draw_overlay=True):
    """Render with perspective-warped texture for top + 2 side faces."""
    if tex_front is None:
        tex_front = tex_side
    if not voxels:
        return Image.new("RGBA", (canvas_w, canvas_h), BG)

    DX, DY = 26, 13   # half-width and half-height of voxel diamond
    # Project voxel (i,j,k) (j-up, i to right-back, k to right-front)
    # to screen coords (px, py).
    def proj(i, j, k):
        # camera looks at center; i increases up-right, k increases up-left
        px = (i - k) * DX
        py = (i + k) * DY - j * 2 * DY
        return px, py

    # Compute bounding box and scale to fit canvas with margin
    pts = []
    for (i, j, k) in voxels:
        # corners of voxel
        for di in (0, 1):
            for dj in (0, 1):
                for dk in (0, 1):
                    pts.append(proj(i+di, j+dj, k+dk))
    minx = min(p[0] for p in pts)
    maxx = max(p[0] for p in pts)
    miny = min(p[1] for p in pts)
    maxy = max(p[1] for p in pts)
    cw = maxx - minx
    ch = maxy - miny
    margin = 30
    scale = min((canvas_w - 2*margin) / cw, (canvas_h - 2*margin) / ch)
    if scale > 1.5: scale = 1.5
    offx = (canvas_w - cw*scale) / 2 - minx*scale
    offy = (canvas_h - ch*scale) / 2 - miny*scale

    out = Image.new("RGBA", (canvas_w, canvas_h), BG)

    # Sort voxels back-to-front (painter's algorithm)
    # In our isometric: voxels far away have smaller (i + j + k) actually no:
    # Camera direction such that nearer = smaller (-i - k + j)?
    # Simplest: sort by (j ascending, then i+k descending) — bottom layers first,
    # back voxels first within a layer.
    # We want voxels with bigger projection y drawn LATER (in front).
    # py = (i+k)*DY - j*2*DY. Bigger py = (i+k) larger or j smaller.
    # Painter's: paint layer by layer from bottom (j=0) up; within a layer
    # paint farthest from camera first. With camera at (+i, +j, +k) the
    # farthest-in-layer voxel has smallest (i+k). So sort by (j asc, i+k asc).
    sorted_v = sorted(voxels, key=lambda v: (v[1], v[0] + v[2]))

    # Pre-scale textures
    base_size = max(8, int(2 * DX * scale))
    tex_t = tex_top.resize((base_size, base_size), Image.NEAREST)
    tex_l = tex_side.resize((base_size, base_size), Image.NEAREST)
    tex_r = tex_front.resize((base_size, base_size), Image.NEAREST)

    # Helper: warp a square texture into a quad on the destination using
    # PIL's PERSPECTIVE transform.
    def warp_quad(src, dst_quad):
        """src: square RGBA; dst_quad: 4 (x,y) tuples in order: TL,TR,BR,BL.
        Pastes warped onto out."""
        w, h = src.size
        # Compute coefficients for QUAD transform (PIL needs source quad as
        # 4 pairs in order: top-left, top-right, bottom-right, bottom-left).
        # Easiest: use Image.transform on a temporary canvas sized to the
        # bounding box of dst_quad and then paste.
        xs = [p[0] for p in dst_quad]
        ys = [p[1] for p in dst_quad]
        min_x = int(math.floor(min(xs)))
        min_y = int(math.floor(min(ys)))
        max_x = int(math.ceil(max(xs)))
        max_y = int(math.ceil(max(ys)))
        bw = max(1, max_x - min_x)
        bh = max(1, max_y - min_y)
        # Translate dst_quad to local
        local_quad = [(p[0]-min_x, p[1]-min_y) for p in dst_quad]
        # PIL QUAD: data = (x0,y0, x1,y1, x2,y2, x3,y3) where the order is
        # UPPER-LEFT, LOWER-LEFT, LOWER-RIGHT, UPPER-RIGHT (counterclockwise)
        # and the source coordinates are in source image (4 corner)
        # Map dst TL,TR,BR,BL -> source corners
        # source: (0,0)=TL, (w,0)=TR, (w,h)=BR, (0,h)=BL
        # We want destination[i] to sample source[i]
        # PIL transform Image.QUAD takes 8 floats describing UL, LL, LR, UR
        # of the SOURCE quadrilateral, mapped to the corners of the OUTPUT.
        # Output corners are: (0,0)-(0,h_out)-(w_out,h_out)-(w_out,0)
        # We want output corner (0,0) to come from dst_quad[0] (TL)... no.
        # Actually: we are *generating* an output image of size (bw, bh).
        # For each output pixel, we map back to source. We want pixel at
        # local_quad[i] of the output to come from source corner i.
        # That means: define a source quad (in source coords) and let PIL
        # warp it to fill the OUTPUT IMAGE's full rectangle. So we need to
        # construct an output image whose own rectangle (0,0)-(bw,bh) maps
        # back to source's 4 corners via the inverse of local_quad.
        # Simpler: use bilinear by sampling.
        # We'll do manual bilinear warp.
        warped = Image.new("RGBA", (bw, bh), (0,0,0,0))
        pxw = warped.load()
        srcload = src.load()
        for py in range(bh):
            for px in range(bw):
                # Compute barycentric-ish weights for the quad
                # Use bilinear: find (u, v) in [0,1]^2 such that
                # (1-u)(1-v)*TL + u(1-v)*TR + u*v*BR + (1-u)*v*BL = (px, py)
                tl, tr, br, bl = local_quad
                # Approximate by inverting quad: iterative or linear interp on diag
                # For an isometric face that is a parallelogram or trapezoid,
                # the affine transform suffices because three points define it.
                # Affine map: P = TL + u*(TR-TL) + v*(BL-TL) when BR = TL + u*(TR-TL) + v*(BL-TL)|u=v=1
                # That assumes parallelogram (BR = TR + BL - TL). Iso faces ARE parallelograms.
                # So solve: px = TL.x + u*(TR.x-TL.x) + v*(BL.x-TL.x)
                #            py = TL.y + u*(TR.y-TL.y) + v*(BL.y-TL.y)
                ax = tr[0] - tl[0]; ay = tr[1] - tl[1]
                bx_ = bl[0] - tl[0]; by_ = bl[1] - tl[1]
                det = ax*by_ - ay*bx_
                if det == 0: continue
                rx = px - tl[0]; ry = py - tl[1]
                u = (rx*by_ - ry*bx_) / det
                v = (ry*ax - rx*ay) / det
                if 0 <= u <= 1 and 0 <= v <= 1:
                    sx = int(u*(w-1)); sy = int(v*(h-1))
                    pxw[px, py] = srcload[sx, sy]
        out.alpha_composite(warped, (min_x, min_y))

    def shade(img, factor):
        """Multiply RGB by factor, keep alpha."""
        r, g, b, a = img.split()
        r = r.point(lambda x: max(0, min(255, int(x*factor))))
        g = g.point(lambda x: max(0, min(255, int(x*factor))))
        b = b.point(lambda x: max(0, min(255, int(x*factor))))
        return Image.merge("RGBA", (r, g, b, a))

    tex_t_s = tex_t
    tex_l_s = shade(tex_l, 0.78)
    tex_r_s = shade(tex_r, 0.58)

    for (i, j, k) in sorted_v:
        # Compute 8 corners projected
        def P(di, dj, dk):
            x, y = proj(i+di, j+dj, k+dk)
            return (x*scale + offx, y*scale + offy)
        # Top face corners: ABCD (CCW seen from above):
        # A = (i, j+1, k+1) front-left
        # B = (i+1, j+1, k+1) front-right
        # C = (i+1, j+1, k)   back-right
        # D = (i, j+1, k)     back-left
        # In screen, "front" = larger py, so reorder to TL/TR/BR/BL of top diamond:
        top_v = (P(0,1,0), P(1,1,0), P(1,1,1), P(0,1,1))
        # That's: back-left, back-right, front-right, front-left
        # As a quad TL=back-left, TR=back-right, BR=front-right, BL=front-left
        # That defines orientation.
        # Right face (visible when looking at +i side): rectangle in
        # (i+1, j, k) — (i+1, j+1, k) — (i+1, j+1, k+1) — (i+1, j, k+1)
        # But camera shows the +i face on the upper-right side. Project corners:
        # right face TL: top-back = (i+1, j+1, k)
        # right face TR: top-front = (i+1, j+1, k+1)
        # right face BR: bot-front = (i+1, j, k+1)
        # right face BL: bot-back = (i+1, j, k)
        right_v = (P(1,1,0), P(1,1,1), P(1,0,1), P(1,0,0))
        # Left face (+k or front face) corresponds to camera-front:
        # face k=k+1 -> seen when k+1 = k_max. Use the +k face:
        # TL: top-front-left = (i, j+1, k+1)
        # TR: top-front-right= (i+1, j+1, k+1)
        # BR: bot-front-right= (i+1, j, k+1)
        # BL: bot-front-left = (i, j, k+1)
        front_v = (P(0,1,1), P(1,1,1), P(1,0,1), P(0,0,1))

        # Cull hidden faces: skip if neighbour voxel exists
        if (i, j+1, k) not in voxels:
            warp_quad(tex_t_s, top_v)
        if (i+1, j, k) not in voxels:
            warp_quad(tex_r_s, right_v)
        if (i, j, k+1) not in voxels:
            warp_quad(tex_l_s, front_v)

    # Overlay: draw cube edges of exposed faces
    if draw_overlay:
        draw = ImageDraw.Draw(out)
        edges_drawn = set()
        for (i, j, k) in sorted_v:
            def P(di, dj, dk):
                x, y = proj(i+di, j+dj, k+dk)
                return (x*scale + offx, y*scale + offy)
            # For each exposed face, draw its 4 edges
            faces = []
            if (i, j+1, k) not in voxels:
                faces.append((P(0,1,0), P(1,1,0), P(1,1,1), P(0,1,1)))
            if (i+1, j, k) not in voxels:
                faces.append((P(1,1,0), P(1,1,1), P(1,0,1), P(1,0,0)))
            if (i, j, k+1) not in voxels:
                faces.append((P(0,1,1), P(1,1,1), P(1,0,1), P(0,0,1)))
            for face in faces:
                for a, b in zip(face, face[1:] + (face[0],)):
                    key = (round(a[0]), round(a[1]), round(b[0]), round(b[1]))
                    key2 = (round(b[0]), round(b[1]), round(a[0]), round(a[1]))
                    if key in edges_drawn or key2 in edges_drawn:
                        continue
                    edges_drawn.add(key)
                    draw.line([a, b], fill=OVERLAY, width=1)
    return out

# ===========================================================================
# Crop + padding helpers
# ===========================================================================
def crop_to_content(im, bg_rgba=BG):
    """Find tight bbox of non-bg pixels."""
    px = im.load()
    W, H = im.size
    # Sample by stride for speed
    min_x, min_y, max_x, max_y = W, H, 0, 0
    for y in range(H):
        for x in range(W):
            if px[x, y] != bg_rgba:
                if x < min_x: min_x = x
                if y < min_y: min_y = y
                if x > max_x: max_x = x
                if y > max_y: max_y = y
    if min_x > max_x: return im
    pad = 14
    return im.crop((max(0,min_x-pad), max(0,min_y-pad),
                    min(W,max_x+1+pad), min(H,max_y+1+pad)))

def save(im, name):
    p = IMG_DIR / name
    im.save(p, "PNG")
    print(f"  {name}: {im.size}")

# ===========================================================================
# Main
# ===========================================================================
def main():
    cobble = load_tex("cobblestone")
    stone = load_tex("stone")
    oak = load_tex("oak_planks")
    grass_top = load_tex("grass_block_top")
    grass_side = load_tex("grass_block_side")
    diamond = load_tex("diamond_block")
    quartz = load_tex("quartz_block_side")
    sandstone = load_tex("sandstone")

    # 2D D=10
    for label, fn in (("euclidean", euclidean_2d),
                      ("bresenham", bresenham_2d),
                      ("threshold", threshold_2d)):
        cells = fn(10)
        im = render_2d(cells, 10, 10, cobble, cell_px=56)
        im = crop_to_content(im)
        save(im, {"euclidean":"fig01_2d_d10_euclidean.png",
                  "bresenham":"fig02_2d_d10_bresenham.png",
                  "threshold":"fig03_2d_d10_threshold.png"}[label])

    # 2D D=20
    for label, fn in (("euclidean", euclidean_2d),
                      ("bresenham", bresenham_2d),
                      ("threshold", threshold_2d)):
        cells = fn(20)
        im = render_2d(cells, 20, 20, cobble, cell_px=30)
        im = crop_to_content(im)
        save(im, {"euclidean":"fig04_2d_d20_euclidean.png",
                  "bresenham":"fig05_2d_d20_bresenham.png",
                  "threshold":"fig06_2d_d20_threshold.png"}[label])

    # Ellipse 24x12
    cells = ellipse_2d(24, 12)
    im = render_2d(cells, 24, 12, cobble, cell_px=28)
    im = crop_to_content(im)
    save(im, "fig07_2d_ellipse_24x12.png")

    # Thin / Thick
    base = euclidean_2d(20)
    im = render_2d(shell_2d(base), 20, 20, cobble, cell_px=30)
    save(crop_to_content(im), "fig08_2d_d20_thin.png")
    im = render_2d(thick_2d(base), 20, 20, cobble, cell_px=30)
    save(crop_to_content(im), "fig09_2d_d20_thick.png")

    # 3D sphere D=10 (full solid; face culling handles oclusion)
    sph = sphere_3d(10)
    im = render_iso(sph, cobble, cobble)
    save(crop_to_content(im), "fig10_3d_sphere_d12.png")  # name kept for refs

    # Ellipsoid 20x10x12
    ell = ellipsoid_3d(20, 10, 12)
    im = render_iso(ell, cobble, cobble)
    save(crop_to_content(im), "fig11_3d_ellipsoid.png")

    # Cuts on D=16 sphere
    sph16 = sphere_3d(16)
    im = render_iso(cut_y(sph16, 0.5), cobble, cobble)
    save(crop_to_content(im), "fig12_3d_cut_y50.png")
    im = render_iso(cut_x(sph16, 0.5), cobble, cobble)
    save(crop_to_content(im), "fig13_3d_cut_x50.png")
    im = render_iso(cut_diag(sph16, 0.5), cobble, cobble)
    save(crop_to_content(im), "fig14_3d_cut_diag50.png")

    # Same sphere, 6 different block textures (DIFERENCIAL Block Round)
    sph10 = sphere_3d(10)  # menor para acelerar e ficar mais legivel
    for fname, tex in (("fig15_3d_sphere_cobblestone.png", cobble),
                       ("fig16_3d_sphere_stone.png", stone),
                       ("fig17_3d_sphere_oak.png", oak),
                       ("fig18_3d_sphere_diamond.png", diamond),
                       ("fig19_3d_sphere_quartz.png", quartz),
                       ("fig20_3d_sphere_sandstone.png", sandstone)):
        im = render_iso(sph10, tex, tex)
        save(crop_to_content(im), fname)

    # Grass block (multi-face)
    sph10b = sphere_3d(10)
    im = render_iso(sph10b, grass_top, grass_side)
    save(crop_to_content(im), "fig21_3d_sphere_grass.png")

    print("\nDone.")

if __name__ == "__main__":
    main()
