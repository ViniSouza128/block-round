# -*- coding: utf-8 -*-
"""Gerador de figuras para o documento matemático do Block Round.

Reusa o gerador de docs_aula/gen_figures.py (importa as funções de
rasterização e renderização) e adiciona variantes específicas do
math doc: 3 estilos de shading, edge overlay on/off, esfera por
octantes coloridos.

Saída: docs_math/img/math_*.png (18 figuras).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# import docs_aula/gen_figures.py
sys.path.insert(0, str(ROOT / "docs_aula"))
import gen_figures as ga  # noqa: E402

from PIL import Image, ImageDraw  # noqa: E402

IMG_DIR = HERE / "img"
IMG_DIR.mkdir(parents=True, exist_ok=True)
TEX_DIR = ROOT / "textures"

# ----------------------------------------------------------------------------
# Wrapper: render_iso with optional shading multipliers and overlay toggle.
# We monkey-patch render_iso to accept extra kwargs.
# ----------------------------------------------------------------------------
_orig_render = ga.render_iso

def render_iso_styled(voxels, tex_top, tex_side, tex_front=None,
                     canvas_w=900, canvas_h=750,
                     draw_overlay=True,
                     shade_left=0.78, shade_right=0.58,
                     octant_color=None):
    """Renderiza voxels com controle de shading e (opcional) destaque de octante.

    shade_left  : multiplicador de brilho para a face esquerda (default 0.78).
    shade_right : idem para a face direita (default 0.58).
    octant_color: se dado, voxels com (i>=R, j>=R, k>=R) recebem cor sólida
                  RGBA ao invés de textura — usado para destacar 1 octante.
    """
    if tex_front is None:
        tex_front = tex_side
    if not voxels:
        return Image.new("RGBA", (canvas_w, canvas_h), ga.BG)

    DX, DY = 26, 13

    def proj(i, j, k):
        return ((i - k) * DX, (i + k) * DY - j * 2 * DY)

    pts = []
    for (i, j, k) in voxels:
        for di in (0, 1):
            for dj in (0, 1):
                for dk in (0, 1):
                    pts.append(proj(i+di, j+dj, k+dk))
    minx = min(p[0] for p in pts); maxx = max(p[0] for p in pts)
    miny = min(p[1] for p in pts); maxy = max(p[1] for p in pts)
    cw, ch = maxx - minx, maxy - miny
    margin = 30
    scale = min((canvas_w - 2*margin) / cw, (canvas_h - 2*margin) / ch, 1.5)
    offx = (canvas_w - cw*scale) / 2 - minx*scale
    offy = (canvas_h - ch*scale) / 2 - miny*scale

    out = Image.new("RGBA", (canvas_w, canvas_h), ga.BG)
    sorted_v = sorted(voxels, key=lambda v: (v[1], v[0] + v[2]))

    base_size = max(8, int(2 * DX * scale))
    tex_t = tex_top.resize((base_size, base_size), Image.NEAREST)
    tex_l = tex_side.resize((base_size, base_size), Image.NEAREST)
    tex_r = tex_front.resize((base_size, base_size), Image.NEAREST)

    def shade(img, factor):
        r, g, b, a = img.split()
        r = r.point(lambda x: max(0, min(255, int(x*factor))))
        g = g.point(lambda x: max(0, min(255, int(x*factor))))
        b = b.point(lambda x: max(0, min(255, int(x*factor))))
        return Image.merge("RGBA", (r, g, b, a))

    tex_t_s = tex_t
    tex_l_s = shade(tex_l, shade_left)
    tex_r_s = shade(tex_r, shade_right)

    # Octante highlight: pre-render a single solid tile per face
    octant_tiles = None
    if octant_color is not None:
        sz = base_size
        oc_t = Image.new("RGBA", (sz, sz), octant_color)
        oc_l = shade(oc_t, shade_left)
        oc_r = shade(oc_t, shade_right)
        octant_tiles = (oc_t, oc_l, oc_r)

    # Determine octant boundary (>= midpoint = positive octant)
    if octant_tiles is not None:
        max_i = max(v[0] for v in voxels)
        max_j = max(v[1] for v in voxels)
        max_k = max(v[2] for v in voxels)
        mid_i, mid_j, mid_k = max_i / 2, max_j / 2, max_k / 2

    for (i, j, k) in sorted_v:
        def P(di, dj, dk):
            x, y = proj(i+di, j+dj, k+dk)
            return (x*scale + offx, y*scale + offy)
        top_v = (P(0,1,0), P(1,1,0), P(1,1,1), P(0,1,1))
        right_v = (P(1,1,0), P(1,1,1), P(1,0,1), P(1,0,0))
        front_v = (P(0,1,1), P(1,1,1), P(1,0,1), P(0,0,1))

        # Choose textures for this voxel
        if octant_tiles is not None and i >= mid_i and j >= mid_j and k >= mid_k:
            t_top, t_left, t_right = octant_tiles
        else:
            t_top, t_left, t_right = tex_t_s, tex_l_s, tex_r_s

        if (i, j+1, k) not in voxels:
            ga.render_iso.__globals__["_warp_into"] = lambda *a, **kw: None  # no-op shadow
            warp_to_out(out, t_top, top_v)
        if (i+1, j, k) not in voxels:
            warp_to_out(out, t_right, right_v)
        if (i, j, k+1) not in voxels:
            warp_to_out(out, t_left, front_v)

    if draw_overlay:
        draw = ImageDraw.Draw(out)
        edges_drawn = set()
        for (i, j, k) in sorted_v:
            def P(di, dj, dk):
                x, y = proj(i+di, j+dj, k+dk)
                return (x*scale + offx, y*scale + offy)
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
                    draw.line([a, b], fill=ga.OVERLAY, width=1)
    return out


def warp_to_out(out, src, dst_quad):
    """Warp a textured square into a quad of the output canvas (affine for parallelogram)."""
    import math as _m
    w, h = src.size
    xs = [p[0] for p in dst_quad]; ys = [p[1] for p in dst_quad]
    min_x = int(_m.floor(min(xs))); min_y = int(_m.floor(min(ys)))
    max_x = int(_m.ceil(max(xs)));  max_y = int(_m.ceil(max(ys)))
    bw = max(1, max_x - min_x); bh = max(1, max_y - min_y)
    local_quad = [(p[0]-min_x, p[1]-min_y) for p in dst_quad]
    warped = Image.new("RGBA", (bw, bh), (0,0,0,0))
    pxw = warped.load(); srcload = src.load()
    tl, tr, br, bl = local_quad
    ax = tr[0] - tl[0]; ay = tr[1] - tl[1]
    bx_ = bl[0] - tl[0]; by_ = bl[1] - tl[1]
    det = ax*by_ - ay*bx_
    if det == 0: return
    for py in range(bh):
        for px in range(bw):
            rx = px - tl[0]; ry = py - tl[1]
            u = (rx*by_ - ry*bx_) / det
            v = (ry*ax - rx*ay) / det
            if 0 <= u <= 1 and 0 <= v <= 1:
                sx = int(u*(w-1)); sy = int(v*(h-1))
                pxw[px, py] = srcload[sx, sy]
    out.alpha_composite(warped, (min_x, min_y))


# ----------------------------------------------------------------------------
# Build the 18 figures
# ----------------------------------------------------------------------------
def save(im, name):
    p = IMG_DIR / name
    im.save(p, "PNG")
    print(f"  {name}: {im.size}")


def main():
    cobble = ga.load_tex("cobblestone")
    stone = ga.load_tex("stone")
    oak = ga.load_tex("oak_planks")
    diamond = ga.load_tex("diamond_block")
    quartz = ga.load_tex("quartz_block_side")

    # --- 2D D=10, 3 algoritmos ---
    for name, fn in (("eucl", ga.euclidean_2d),
                     ("bres", ga.bresenham_2d),
                     ("thr",  ga.threshold_2d)):
        cells = fn(10)
        im = ga.render_2d(cells, 10, 10, cobble, cell_px=56)
        im = ga.crop_to_content(im)
        save(im, f"math_2d_d10_{name}.png")

    # --- 2D D=20, modos render ---
    base = ga.euclidean_2d(20)
    im = ga.render_2d(base, 20, 20, cobble, cell_px=30)
    save(ga.crop_to_content(im), "math_2d_d20_filled.png")
    im = ga.render_2d(ga.shell_2d(base), 20, 20, cobble, cell_px=30)
    save(ga.crop_to_content(im), "math_2d_d20_thin.png")
    im = ga.render_2d(ga.thick_2d(base), 20, 20, cobble, cell_px=30)
    save(ga.crop_to_content(im), "math_2d_d20_thick.png")

    # --- Ellipse ---
    cells = ga.ellipse_2d(24, 12)
    im = ga.render_2d(cells, 24, 12, cobble, cell_px=28)
    save(ga.crop_to_content(im), "math_2d_ellipse.png")

    # --- 3D sphere & ellipsoid ---
    sph10 = ga.sphere_3d(10)
    save(ga.crop_to_content(render_iso_styled(sph10, cobble, cobble)),
         "math_3d_sphere_d10.png")

    ell = ga.ellipsoid_3d(20, 10, 12)
    save(ga.crop_to_content(render_iso_styled(ell, cobble, cobble)),
         "math_3d_ellipsoid.png")

    # --- Cuts on D=16 ---
    sph16 = ga.sphere_3d(16)
    save(ga.crop_to_content(render_iso_styled(ga.cut_y(sph16, 0.5), cobble, cobble)),
         "math_3d_cut_y.png")
    save(ga.crop_to_content(render_iso_styled(ga.cut_x(sph16, 0.5), cobble, cobble)),
         "math_3d_cut_x.png")
    save(ga.crop_to_content(render_iso_styled(ga.cut_diag(sph16, 0.5), cobble, cobble)),
         "math_3d_cut_diag.png")

    # --- Shading styles: D=10 cobble, três multiplicadores ---
    sph10v = ga.sphere_3d(10)
    save(ga.crop_to_content(render_iso_styled(sph10v, cobble, cobble,
        shade_left=0.62, shade_right=0.42)),
        "math_3d_shading_classic.png")    # forte contraste
    save(ga.crop_to_content(render_iso_styled(sph10v, cobble, cobble,
        shade_left=0.88, shade_right=0.75)),
        "math_3d_shading_smooth.png")     # suave
    save(ga.crop_to_content(render_iso_styled(sph10v, cobble, cobble,
        shade_left=0.78, shade_right=0.58)),
        "math_3d_shading_blocks.png")     # padrão (medio)

    # --- Edge overlay on / off ---
    save(ga.crop_to_content(render_iso_styled(sph10v, cobble, cobble,
        draw_overlay=False)),
        "math_3d_overlay_off.png")
    save(ga.crop_to_content(render_iso_styled(sph10v, cobble, cobble,
        draw_overlay=True)),
        "math_3d_overlay_on.png")

    # --- Octantes: esfera com octante +,+,+ destacado em verde ---
    accent_rgba = (91, 142, 63, 255)  # #5B8E3F = block-round green
    save(ga.crop_to_content(render_iso_styled(sph10v, cobble, cobble,
        octant_color=accent_rgba)),
        "math_3d_octants.png")

    # --- Bonus: 3 texturas diferentes lado a lado (each saved as its own file) ---
    sph8 = ga.sphere_3d(8)
    save(ga.crop_to_content(render_iso_styled(sph8, cobble, cobble)),
        "math_3d_tex_cobble.png")
    save(ga.crop_to_content(render_iso_styled(sph8, oak, oak)),
        "math_3d_tex_oak.png")
    save(ga.crop_to_content(render_iso_styled(sph8, quartz, quartz)),
        "math_3d_tex_quartz.png")

    print("\nDone.")


if __name__ == "__main__":
    main()
