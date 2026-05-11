# Block Round

A pixel-perfect generator for **circles, ellipses, spheres and
ellipsoids** rendered with **Minecraft block textures**. Browser-based,
no installation, no account, no backend. Exports as PNG.

> **Block Round is not affiliated with, endorsed by, or sponsored by
> Mojang Studios or Microsoft.** "Minecraft" is a trademark of Mojang
> Synergies AB. See `LICENSE` for the full disclaimer.

**Live:** *(GitHub Pages URL — set after deployment)*

## What it does

| Mode        | Shape     | Inputs              |
| ----------- | --------- | ------------------- |
| 2D · Circle    | Round     | Size                |
| 2D · Ellipse   | Oval      | Width + Height      |
| 3D · Sphere    | Voxel     | Size + Cut          |
| 3D · Ellipsoid | Voxel     | Width + Height + Depth + Cut |

Pick a Minecraft block from the picker (Grass Block, Dirt, Stone,
Oak, Diamond, **Sand**, **Gravel**, etc., plus a Random mix) and the
generator renders the shape using that block's texture. Three 2D
algorithms (Euclidean, Bresenham, Threshold) are available.

### Special block behaviours

| Block | What's different |
| --- | --- |
| **Grass Block** | Top voxel of each column uses the grass texture (multi-face in 3D: green top, grass-side, dirt bottom); the rest is plain dirt. |
| **Dirt** | Plain dirt everywhere — no grass cap. |
| **Glass / Ice** | MC-style rendering: faces between two adjacent same-material voxels are culled, so the figure reads as one big pane (no doubled internal frames). `alphaTest:0.5` keeps the frame solid and the panes see-through. |
| **Multi-face blocks** | Pumpkin · Hay · Melon · Quartz · Bone · Sandstone · Crafting Table · Furnace · Bookshelf · TNT · Mycelium · Podzol · all wood Logs (Oak / Birch / Spruce / Jungle / Acacia / Dark Oak) render distinct textures on top, sides and bottom — matching the real Minecraft block. |
| **Filled vs. Thin (transparent)** | For Glass and Ice in Filled mode the renderer emits every voxel of the solid volume (not just the outer shell), so the user can see the dense interior of cubes through the front panes. Thin still draws a hollow merged shell. |
| **Sand / Gravel** | After a 500 ms hold the cells fall onto an invisible floor under gravity, mirroring Minecraft physics. Works in 2D and 3D. Edge overlay opacity is reduced to 25 % on these blocks so the grain reads cleanly. **Soul Sand** doesn't fall (matches MC). |
| **Random** | Procedurally tiered: grass on top of each column, dirt beneath, stone with sparse ores (coal, iron, redstone, gold, lapis, diamond, emerald, cobble), deepslate above bedrock — band boundaries wavy per column. |

## Controls

- Toolbar toggles: **2D / 3D** and **Circle / Ellipse** (or Sphere /
  Ellipsoid in 3D)
- Block picker strip below the canvas — **mouse wheel** scrolls
  horizontally, **click + drag** also scrolls. Order is curated: the
  most iconic Minecraft blocks (Grass Block, Dirt, Stone, Cobblestone,
  Oak Planks, Oak Log, Sand, Gravel, Glass) come first.
- **Mouse wheel** on the canvas zooms; **drag** rotates in 3D;
  **double-click** resets the camera (3D) or zoom (2D)
- **Double-click any slider** to snap it back to its default value
- Cut is **proportional** to size — 50% stays 50%.
  Default axis = **Y**.
- **Grid corner button** in 3D toggles a black **edge overlay** on
  every voxel (default ON, makes counting blocks easier). In 2D it
  toggles the cell grid.
- **Center guides** in 3D draw a translucent yellow cross along all
  three axes; bars are **1 block thick** for odd-sized axes and
  **2 blocks thick** for even, so they always shine through the
  figure's true center voxel(s).
- Clicking a tool toggle while on **Info** or **Settings** returns
  to the canvas automatically
- Keyboard: `G` grid · `C` center guides · `D` download · `I` info ·
  `M` 2D/3D · `S` sound

## Session-only state

Block Round does **not** persist any setting across reloads — every
visit starts at the defaults.

## Tech

Vanilla JavaScript + Canvas 2D + three.js. No framework, no build
step. Loads as a single static HTML file. Works offline (PWA).

## License & notices

- **Code, layout, design system, sound engine:** All Rights Reserved
  — see `LICENSE`
- **Minecraft block textures:** property of Mojang Studios /
  Microsoft Corporation, used here under a non-commercial fan-project
  rationale. Block Round asserts no rights over them and provides no
  license to redistribute them. See `LICENSE` and `NOTICE.md`.

## Companion project

A clean, non-Minecraft version of this tool lives at
[Pixel Round](https://github.com/ViniSouza128/pixel-round) — same
algorithms, neutral pixel-art look.
