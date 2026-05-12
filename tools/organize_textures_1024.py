#!/usr/bin/env python3
"""
Reorganize textures-1024/ (flat 127 PNGs) into thematic subfolders so each
"visual coherence group" can be sent to an image generator together.

Groups are defined by what a human eye reads as one family: a wood type's
side+top must match each other; all wools share a knit pattern but vary
in hue; the ores inside deepslate must use the deepslate matrix; etc.

Re-run any time. Idempotent: files already inside a group folder are
left alone. New textures that don't match any group land in `_unsorted/`.

Usage:
    python tools/organize_textures_1024.py
"""

from pathlib import Path
import shutil
import sys

# Root of textures-1024/ (relative to repo root)
ROOT = Path(__file__).resolve().parent.parent / "textures-1024"

# Group definitions — each subfolder name → list of stems (without .png).
# Order is "user-friendly visual": planks first, then logs, then surfaces,
# then ores, etc. Folder names are prefixed with a number so they sort
# in a sensible order in the file explorer.
GROUPS = {
    "01_planks": [
        # One face per wood type. Plank grain pattern must be consistent
        # across types — generate the whole set as one prompt to keep
        # plank width / knot density / grain direction matching.
        "acacia_planks", "birch_planks", "dark_oak_planks",
        "jungle_planks", "oak_planks", "spruce_planks",
    ],
    "02_logs": [
        # Bark (side) + ring-top pairs. Within a wood type, side+top
        # MUST agree on bark colour and ring colour. Across wood types,
        # the *anatomy* (ring count, bark roughness) should be uniform
        # so a row of logs reads as one family.
        "oak_log", "oak_log_top",
        "log_birch", "log_birch_top", "birch_log",
        "log_spruce", "log_spruce_top", "spruce_log",
        "log_jungle", "log_jungle_top",
        "log_acacia", "log_acacia_top",
        "log_big_oak", "log_big_oak_top", "dark_oak_log",
    ],
    "03_leaves": [
        # Only oak leaves shipped today. If more leaf types arrive, drop
        # them here so they share leaf-cluster density.
        "leaves_oak",
    ],
    "04_wools": [
        # Same knit pattern, different hues. Generate as one batch and
        # ask the model to keep the weave identical across colours.
        "white_wool", "light_blue_wool", "blue_wool", "green_wool",
        "yellow_wool", "orange_wool", "red_wool", "black_wool",
    ],
    "05_stone_family": [
        # Plain stone + its derived surfaces. Smooth stone is what cobble
        # turns into when smelted; mossy cobble is overgrown cobble.
        # Same base grey palette across all four.
        "stone", "smooth_stone", "cobblestone", "mossy_cobblestone",
    ],
    "06_igneous": [
        # Andesite / granite / diorite + their polished forms. All three
        # are igneous rocks; visual coherence = same speckle scale.
        "andesite", "polished_andesite", "granite", "diorite",
    ],
    "07_ores_stone_matrix": [
        # Ores embedded in plain stone. The matrix MUST match stone.png
        # exactly so the ore-spot reads as an inclusion. Generate this
        # group AFTER stone is finalised, locking the matrix as input.
        "coal_ore", "iron_ore", "gold_ore", "diamond_ore",
        "emerald_ore", "redstone_ore", "lapis_ore",
    ],
    "08_deepslate": [
        # Deepslate base + its 4 ore variants. Same constraint as #07:
        # matrix must match deepslate.png. Note: copper and lapis don't
        # have deepslate variants in this catalog.
        "deepslate", "deepslate_diamond_ore", "deepslate_emerald_ore",
        "deepslate_gold_ore", "deepslate_iron_ore",
    ],
    "09_metal_gem_blocks": [
        # Solid blocks of refined metal/gem. They share a "tiled bar"
        # composition — 9 ingot/gem shapes in a grid. Coherence point:
        # same tile geometry, different material colour.
        "iron_block", "gold_block", "diamond_block",
        "emerald_block", "copper_block",
    ],
    "10_sand_sandstone": [
        # Loose sand + carved sandstone (top/side/bottom faces). Side
        # has the vertical erosion lines; top/bottom are smooth caps.
        # Red sandstone top kept here too since it's the same family
        # rotated to a warmer hue.
        "sand", "sandstone", "sandstone_top", "sandstone_bottom",
        "red_sandstone_top",
    ],
    "11_ice_snow": [
        # Ice progression (regular → packed → blue) + snow. All cold
        # surfaces; coherence = colour temperature stays in the cool
        # blue-white range across the four.
        "ice", "ice_packed", "blue_ice", "snow",
    ],
    "12_dirt_grass_surfaces": [
        # Top-of-world ground textures. Grass top (green), grass side
        # (dirt with green cap), plain dirt, moss, mycelium (purple
        # cap on dirt), podzol (spruce litter on dirt). They share the
        # dirt base on the side faces.
        "dirt", "grass_block_top", "grass_block_side", "moss_block",
        "mycelium_top", "mycelium_side",
        "dirt_podzol_top", "dirt_podzol_side",
    ],
    "13_nether": [
        # The Nether dimension's surface palette: red flesh/stone family
        # plus warm glow blocks. magma_frame{0,1,2} are animation frames
        # of one tile — generate together as a sequence.
        "netherrack", "nether_bricks", "soul_sand",
        "magma_frame0", "magma_frame1", "magma_frame2",
        "shroomlight", "crying_obsidian",
    ],
    "14_end_obsidian": [
        # End dimension surfaces + obsidian (technically Overworld but
        # visually it's the same dark-volcanic-glass family).
        "end_stone", "obsidian",
    ],
    "15_prismarine_sea": [
        # Underwater monument family. prismarine_rough is animated
        # (4 frames). sea_lantern is also animated (5 frames). Bricks
        # and dark are static.
        "prismarine_bricks", "prismarine_dark",
        "prismarine_rough_frame0", "prismarine_rough_frame1",
        "prismarine_rough_frame2", "prismarine_rough_frame3",
        "sea_lantern_frame0", "sea_lantern_frame1",
        "sea_lantern_frame2", "sea_lantern_frame3",
        "sea_lantern_frame4",
    ],
    "16_quartz": [
        # Nether quartz block — three distinct faces (top has the
        # smooth cap, side has the fluted column, bottom has the
        # smoother base). All three must share the white quartz hue.
        "quartz_block_top", "quartz_block_side", "quartz_block_bottom",
    ],
    "17_crops_organic": [
        # Living/harvest blocks with distinct side+top anatomy. Hay
        # bale (straw side, end-grain top). Melon (striped top, green
        # side). Pumpkin (orange ridged side, stem top, optional face).
        "hay_block_side", "hay_block_top",
        "melon_side", "melon_top",
        "pumpkin_face_off", "pumpkin_side", "pumpkin_top",
    ],
    "18_mushroom_bone": [
        # Fibrous / fleshy organic surfaces. Bone block (vertical
        # striations on side, end-grain top). Mushroom skin (red /
        # brown — speckled fungal caps).
        "bone_block_side", "bone_block_top",
        "mushroom_block_skin_brown", "mushroom_block_skin_red",
    ],
    "19_crafted_workstations": [
        # Multi-face workstation blocks. Crafting table (recipe-grid
        # top, planks-and-tools side, alternate front). Furnace (hot
        # front, generic side, bare top). Bookshelf (book spines
        # side, planks top).
        "crafting_table_top", "crafting_table_side", "crafting_table_front",
        "furnace_top", "furnace_side", "furnace_front_off",
        "bookshelf",
    ],
    "20_tnt": [
        # TNT — three faces of one block. Side has the diagonal warning
        # stripes, top has the fuse, bottom is plain. Coherence inside
        # the trio is critical (it's literally one cube).
        "tnt_top", "tnt_side", "tnt_bottom",
    ],
    "21_translucent": [
        # Translucent / jelly blocks. Glass is the reference (clean
        # window pane with reflection). Slime is green jelly with
        # honeycomb innards. Honey is amber with three distinct faces.
        "glass", "slime",
        "honey_top", "honey_side", "honey_bottom",
    ],
    "22_misc_solids": [
        # Standalone blocks that don't share a family with anything
        # else here. Bedrock (jagged dark stone). Bricks (clay-fired
        # red brick pattern). Glowstone (golden-pebble luminous).
        # Gravel (loose round stones). Sponge (yellow porous foam).
        "bedrock", "bricks", "glowstone", "gravel", "sponge",
    ],
}


def main():
    if not ROOT.exists():
        print(f"error: {ROOT} not found", file=sys.stderr)
        return 1

    # Build reverse map: stem → group folder
    target = {}
    for folder, stems in GROUPS.items():
        for s in stems:
            if s in target:
                print(f"error: '{s}' listed twice ({target[s]} and {folder})",
                      file=sys.stderr)
                return 1
            target[s] = folder

    # Walk every PNG currently at the root of textures-1024
    flat_pngs = [p for p in ROOT.iterdir() if p.is_file() and p.suffix == ".png"]
    if not flat_pngs:
        print("Nothing at root of textures-1024/ — already organised? "
              "Re-run is a no-op.")
    moved = 0
    skipped = 0
    unsorted = []
    for png in flat_pngs:
        stem = png.stem
        group = target.get(stem)
        if not group:
            unsorted.append(stem)
            group = "_unsorted"
        dest_dir = ROOT / group
        dest_dir.mkdir(exist_ok=True)
        dest = dest_dir / png.name
        if dest.exists():
            print(f"  skip (already in {group}/): {png.name}")
            skipped += 1
            continue
        shutil.move(str(png), str(dest))
        moved += 1
    print(f"\nMoved {moved} file(s); skipped {skipped}; unsorted {len(unsorted)}")
    if unsorted:
        print("Unsorted (added to _unsorted/):")
        for s in sorted(unsorted):
            print(f"  - {s}")

    # Generate a README inside textures-1024/ listing every folder + the
    # rationale so it's discoverable when the user opens the folder.
    readme = ROOT / "README.md"
    lines = [
        "# textures-1024/",
        "",
        "1024×1024 nearest-neighbor upscales of `../textures/*.png`,",
        "generated by `tools/upscale_textures.py`. Pure derivative — local",
        "only, gitignored.",
        "",
        "Organised by **visual coherence group** so each subfolder can be",
        "sent to an image generator as one batch and the variations come",
        "back stylistically consistent.",
        "",
        "## Groups",
        "",
    ]
    for folder, stems in GROUPS.items():
        # Pull the comment line from the source — strip leading `# `.
        # Simpler: hard-code short blurbs here. Read GROUPS dict above for
        # the long-form reasoning in the code comments.
        lines.append(f"### `{folder}/` ({len(stems)} files)")
        lines.append("")
        for s in sorted(stems):
            lines.append(f"- `{s}.png`")
        lines.append("")
    lines.append("## Adding new textures")
    lines.append("")
    lines.append("1. Regenerate the flat set with `python tools/upscale_textures.py`.")
    lines.append("2. Re-run `python tools/organize_textures_1024.py`.")
    lines.append("3. Anything new and uncategorised lands in `_unsorted/` —")
    lines.append("   add it to `GROUPS` in the script, then re-run.")
    lines.append("")
    readme.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {readme.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
