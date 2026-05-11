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
Oak, Diamond, **Sand**, **Gravel**, etc., plus a Random mix and a
handful of curiosity blocks — Slime, Honey, Sponge, Shroomlight,
Crying Obsidian) and the generator renders the shape using that
block's texture. Three 2D algorithms (Euclidean, Bresenham,
Threshold) are available.

### Special block behaviours

| Block | What's different |
| --- | --- |
| **Grass Block** | Top voxel of each column uses the grass texture (multi-face in 3D: green top, grass-side, dirt bottom); the rest is plain dirt. |
| **Dirt** | Plain dirt everywhere — no grass cap. |
| **Glass / Ice** | MC-style rendering: faces between two adjacent same-material voxels are culled, so the figure reads as one big pane (no doubled internal frames). `alphaTest:0.5` keeps the frame solid and the panes see-through. |
| **Slime / Honey** | Shell-and-core rendering matching real Minecraft: each voxel is a translucent outer cube wrapping a smaller opaque inner core. Inner-core sizes are pulled straight from the vanilla block models (slime = 10/16 ≈ 0.625, honey = 14/16 ≈ 0.875). Adjacent shells merge via same-material face cull. Picking the tile plays the vanilla slime jump sound. |
| **Emissive blocks** | Glowstone, Sea Lantern, Shroomlight, Magma and Crying Obsidian render with `emissive + emissiveMap` at intensities scaled to their MC light level, so they self-illuminate the texture independent of scene shadows. |
| **Multi-face blocks** | Pumpkin · Hay · Melon · Quartz · Bone · Sandstone · Crafting Table · Furnace · Bookshelf · TNT · Mycelium · Podzol · all wood Logs (Oak / Birch / Spruce / Jungle / Acacia / Dark Oak) render distinct textures on top, sides and bottom — matching the real Minecraft block. |
| **Filled vs. Thin (transparent)** | For Glass and Ice in Filled mode the renderer emits every voxel of the solid volume (not just the outer shell), so the user can see the dense interior of cubes through the front panes. Thin still draws a hollow merged shell. |
| **Sand / Gravel** | After a 500 ms hold the cells fall onto an invisible floor under gravity, mirroring Minecraft physics. Works in 2D and 3D. Edge overlay opacity is reduced to 25 % on these blocks so the grain reads cleanly. **Soul Sand** doesn't fall (matches MC). Re-clicking the currently-selected Sand / Gravel tile resets the figure and replays the fall. |
| **TNT** | Picking the TNT tile in the block list plays a sizzling fuse sound (synthesised noise + bandpass-rising crackle). |
| **Edges on transparent blocks** | Glass and Ice default to **edge overlay OFF** since the outlines compete with the alpha-blended frames. Toggling the Grid corner button while on Glass / Ice only flips the transparent preference — opaque blocks keep their own preference, so leaving Glass → Stone restores the previous Stone setting automatically. |
| **Random** | Procedurally tiered: grass on top of each column, dirt beneath, stone with sparse ores (coal, iron, redstone, gold, lapis, diamond, emerald, cobble), deepslate above bedrock — band boundaries wavy per column. |

### Easter eggs

- **Oak tree on slider value 15** — plants a small oak tree (4-block
  trunk + 4-layer green-tinted oak-leaves canopy, leaves with proper
  alpha cutouts) directly on top of the figure. Works in **2D and 3D**.
  - Sphere mode triggers on `state.size === 15`.
  - Ellipsoid / Ellipse mode triggers on any of
    `state.width / state.height / state.depth === 15` (the `size`
    slider is ignored there since the user can't edit it in that mode).
  - Block must be **Grass Block**, **Dirt** or **Random** (random's
    top cell is always grass-stamped). Other blocks do not trigger.
  - 3D cuts: **X** and **diagonal** slice the tree block-by-block in
    sync with the figure (lateral trim), while **Y** clears it entirely
    (its base sits above the figure top — any vertical trim erases it).
    The camera recenters so the tree never crops at the top — autoZoom
    adds the tree's height to the bounding-box AND lifts the lookAt.
  - 2D: extra rows are reserved above the figure so the tree fits
    with breathing room; the figure shifts downward accordingly.
- **TNT creeper on slider value 15** — spawns a Minecraft creeper
  standing on top of the figure. **3D only.**
  - Built as a proper Minecraft entity model — six box parts (head,
    body, 4 legs) with per-face UV mapping into a shared 64×32 skin
    atlas. **The atlas is procedurally drawn** at first activation,
    not a copy of Mojang's `creeper.png` binary (we'd need a
    redistribution licence we don't have). The pattern reconstructs
    the visual character of the real texture from primitives:
    a 7-shade green palette matching Mojang's range, a weighted
    per-pixel speckle pass, a chunky-patch overlay pass, and the
    canonical black eye-and-mouth painted into the head-front
    region. Atlas regions are the canonical ones from the entity
    model (head rows 0–15; body rows 16–31, x 16–39; leg rows 16–31,
    x 0–15) so each cube face samples the right slice.
  - True Minecraft entity proportions (16 px = 1 block): head
    8×8×8 px, body 4×12×8 px, four legs at 4×6×4 px each.
    Total height 1.625 blocks, footprint 0.5 × 0.5 block — sits
    centred on the figure's top face.
  - **Eye-contact cycle** — every 6 seconds the creeper slowly turns
    its whole body to face the camera, holds the gaze for ~2 s, and
    eases back to neutral, all on cubic ease-in-out so the motion
    feels organic. During the gaze the head/leg micro-sway damps
    down (the creeper looks locked-on, not paused), and the
    camera-tracking is continuous — if the user orbits the camera
    while the creeper is staring, the gaze follows. Cycle plan:
    1.5 s rise · 2 s hold · 1.5 s fall · 1 s breather.
  - **Idle micro-motion** — between gazes, the head sways ±6°
    around Y (~0.18 Hz) and the legs rock ±4° around X in
    alternating front-back pairs (~0.5 Hz), via pivot groups so the
    head turns around its centre and legs swing from the hip joint.
  - **TNT fuse sound** — the creeper plays the real Minecraft TNT
    fuse the moment it appears on screen (slider transition into 15
    with TNT already selected). The double-trigger case — clicking
    the TNT tile *while* slider is at 15 — is suppressed, because
    the tile-click handler already fires the same fuse.
  - Sphere mode triggers on `state.size === 15`.
  - Ellipsoid mode triggers on any of `state.width / state.height /
    state.depth === 15`. Coexists with the oak-tree easter egg
    (same slider value, different trigger blocks).
  - Block must be **TNT**.
  - 3D cuts: all-or-nothing rule (the creeper is too small to slice
    meaningfully) — Y cut < Dy, X cut ≤ Dx/2, or Diag cut ≤ Dx/2 +
    Dy − 1 hides it. AutoZoom lifts the bounding box by 2 blocks so
    the head never grazes the canvas edge.
  - Creeper is intentionally **excluded from the info-chip block
    count**, mirroring the tree's convention.
- **TNT fuse sound** — picking the TNT tile plays the real Minecraft
  fuse sample (vanilla `random/fuse.ogg`, embedded as a base64 OGG
  data URI in `js/sounds.js`). Switching to any other block before
  the fuse ends stops it immediately.
- **Slime jump sound** — picking the Slime Block or Honey Block tile
  plays the vanilla `mob/slime/small1.ogg` boing.
- **Per-category place sounds** — every other tile plays the right
  Minecraft "dig" sample for its material (stone, wood, grass, sand,
  gravel, cloth, glass, snow). Eight vanilla OGGs (~52 KB raw) are
  embedded as data URIs in `js/sounds.js`.
- **Day / night mood (selective dimming)** — the topbar sun/moon
  button (and the `T` shortcut) tints the background surfaces only
  — text, slider thumbs, the topbar's yellow icons, and the block
  picker tiles all stay at full brightness so they remain readable
  and pickable. Implementation: rather than a global `filter:` on
  body (which used to darken everything, including text and tiles),
  each texture-backed surface (`.topbar`, `.pill-row`, `.slider-box`,
  `.cut-row`, `.mc-list`, `.info-chip`) gets an `inset 0 0 0 9999px`
  translucent navy `box-shadow` — the inset shadow paints inside the
  panel above its texture but **behind** any child content, so the
  texture darkens while children stay 100% bright. The canvas frame
  swaps its bright sky gradient for a deep-navy one. Emissive blocks
  (glowstone, sea lantern, shroomlight, magma, crying obsidian)
  really pop against the night canvas.

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
  Default axis = **Y**. The cut row now has three options:
  **X** (slice perpendicular to X), **Y** (slice perpendicular to Y),
  and **⟋** (45° diagonal slice through the X + Y plane).
- **Undo / Redo** via `Ctrl+Z` for undo and any of `Ctrl+Y`,
  `Ctrl+Shift+Z` or `Ctrl+Alt+Z` for redo (three bindings so muscle
  memory from any host app works). Walks every figure-changing edit —
  sliders, render mode, algorithm, shape, axis, block, mode toggle.
  Slider drags are debounced so one Ctrl+Z undoes one move, not one
  pixel. Visual-only toggles (camera, edges overlay, center cross,
  theme) are NOT tracked.
- **`.schem` export** — the second icon in the top-right canvas
  corner downloads a Sponge schematic v2 file (gzipped NBT) of the
  current figure. WorldEdit (`//schem load`), Litematica and MCEdit
  can all import it. The exported palette covers every block in the
  picker, mapping each one to its MC namespaced block state.
- **Grid corner button** in 3D toggles a black **edge overlay** on
  every voxel (default ON for opaque blocks; default OFF for Glass /
  Ice and remembered separately so the two preferences don't trample
  each other). In 2D it toggles the cell grid.
- **Keyboard arrows** (← / →) move through the block picker after
  you've selected any tile, skipping the internal-only entries.
- **Info chip block count** — the `i` corner button shows a Blocks
  row formatted as `total (stacks × 64 + remainder)`, exactly the
  way Minecraft inventory stacks work. Easter-egg blocks (oak tree,
  TNT creeper) are excluded so the number reflects what the user
  actually needs to collect to build the figure. The chip itself
  **floats above the button**: opening or closing it does not shift
  the `i` button up or down, so the button stays anchored to the
  bottom-left of the canvas.
- **Toast messages overlay the canvas** — the floating "Night on /
  off", "Undo", "Redo" etc. labels are positioned absolutely over
  the bottom of the canvas frame, not below the page. They never
  push layout (so responsive flow stays stable) and they sit in a
  place the user is already looking at.
- **PNG export** of a 2D figure now includes the oak-tree easter
  egg when it's active (when one of the size sliders sits at 15).
- **Center guides** in 3D draw a translucent yellow cross along all
  three axes; bars are **1 block thick** for odd-sized axes and
  **2 blocks thick** for even, so they always shine through the
  figure's true center voxel(s).
- **Camera follows the cut** — the auto-fit camera tracks the
  bounding box of the actually-visible portion of the figure, not
  the full pre-cut figure. Sliding the cut down recenters the
  remaining slice on the canvas instead of letting it drift toward
  one edge.
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
