# Block Round — Design System

> Living reference. Update whenever a visual or behavioural rule changes.
> All Rights Reserved on code. MC textures are Mojang/Microsoft property.

---

## 1. Brand

- **Name:** Block Round (covers circle, ellipse, sphere, ellipsoid in MC)
- **Tagline:** "Build perfect rounded shapes, one block at a time."
- **Logo:** isometric gold cube outlined in bedrock
- **Voice:** casual, gamer-friendly. MC slang accepted (voxel, mob, biome).
- **Mandatory disclaimer:** "Not affiliated with Mojang/Microsoft."

---

## 2. Colors (single theme)

| Token | Value | Use |
|---|---|---|
| `--bg` | `#1a1208` | dirt texture (24px) for body |
| `--surface` | `#2a1808` | smooth_stone texture (24px) on cards |
| `--border` | `#3a2410` | dark wood 3px outer border |
| `--border-strong` | `#1a0e04` | bedrock 2px inner outline |
| `--accent` | `#FFEC4F` | MC gold — CTAs, active states |
| `--accent-light` | `#FFF4A0` | inset highlight on slider thumbs |
| `--text` | `#FFF4D0` | body copy (cream — 8:1 over stone) |
| `--text-muted` | `#FFE8A8` | labels, sub-copy |
| `--on-accent` | `#1a0e04` | text over gold |

**Critical:** EVERY text element over a texture MUST have
`text-shadow: 1px 1px 0 #1a0e04`. Without it, the texture's noise
overwhelms the glyphs and copy becomes illegible.

---

## 3. Typography

- **Display:** Press Start 2P, 20px (14 on mobile), with 2-3px hard shadow
- **H3 / section title:** Press Start 2P, 11-12px, 1-2px shadow
- **Body:** Inter 500, 13-14px, 1.7 line-height, 1px shadow
- **Labels:** Inter 700 caps, 11-12px, 1px shadow
- **Mono (values):** JetBrains Mono 700, 13-14px

Press Start 2P is used ONLY for display + section titles. Inter handles
body copy because Press Start 2P becomes unreadable below 11px.

Font sizes are ~15% larger than the previous iteration.

---

## 4. Spacing

4px grid. Multiples: 4, 8, 12, 16, 24, 32, 48. Card padding ≥16; gap
between cards 12-16. Border discipline is fixed: ALWAYS 3px wood +
2px bedrock outline at offset -3.

---

## 5. Border radius

**ZERO. Always.** Enforced via catch-all `*{border-radius:0 !important}`.
Rounded corners break the blocky aesthetic.

---

## 6. Unified topbar

Layout:

```
[ logo-icon + Block Round ]   [ 2D|3D · Circle|Ellipse ]   [ ⓘ ⚙ ]
       brand (left)                center (toggles)            actions (right)
```

- **Brand:** clickable, returns to Tool route.
- **Center:** mode toggle (2D/3D) + shape toggle (re-labels to
  Sphere/Ellipsoid in 3D).
- **Actions:** **Info** + **Settings** icon buttons (NO theme button —
  single theme).
- **Mobile (≤640px):** center wraps below.

Background: `textures/oak_planks.png` (24px). Border: 3px wood + 2px
bedrock outline.

---

## 7. Tool layout

### Per-mode visibility

| Mode + Shape | Size | W | H | D | Cut | Algorithm pills |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| 2D Circle    | ✅ |    |    |    |    | ✅ |
| 2D Ellipse   |    | ✅ | ✅ |    |    | ✅ |
| 3D Sphere    | ✅ |    |    |    | ✅ | ❌ (right row hides) |
| 3D Ellipsoid |    | ✅ | ✅ | ✅ | ✅ | ❌ |

Render pills (Filled / Thin / Thick) are ALWAYS visible.

**No 3D-style pills** exist in Block Round (unlike Pixel Round). The right
pill row hides entirely in 3D mode.

### Canvas corner buttons

| Button | 2D | 3D | Notes |
|---|:-:|:-:|---|
| Grid    | ✅ | ✅ | 2D: cell grid · 3D: wireframe toggle |
| Download | ✅ | ✅ | 2D: PNG at 16px/cell · 3D: WebGL framebuffer |
| Center  | ✅ | ❌ | Gold guides at center |
| Overlay | ✅ | ❌ | White perfect-ellipse overlay (contrasts with textures) |
| Zoom    | ✅ | ❌ | Toggle on/off · top-left quadrant |
| Info    | ✅ | ✅ | Info chip with D / R / Vol / Block |

### MC Block picker

- Dynamically built from `MC_BLOCKS` catalog in `js/state.js` (50+ blocks)
- Horizontal strip with scroll-x
- Each tile 38×38, `background-image` from `MC_TEX[key]` (base64)
- Selected tile gets gold border + outline (offset -3)
- **Random** tile: checker pattern gold/brown with "?" centered
- Random distributes from `RANDOM_POOL`:
  grass/dirt/stone/cobble/oak/sand

### Cut row

- Visible only in 3D
- Toggle `X | Y` switches axis. Switching:
  1. Updates slider max to the new axis dim
  2. Resets cut to full (max value)
- At full = no cut.

### Center guides

- 1 cell wide for odd diameters
- 2 cells wide for even diameters
- Color: `rgba(255,236,79,.30)` (gold @30%)
- Full canvas coverage

### Grid

- Optional (OFF by default — textures already provide visual structure)
- Full canvas coverage
- Color: `rgba(0,0,0,.32)` for visibility over textures

---

## 8. Algorithms (2D)

Same three distinct implementations as Pixel Round, sourced from the
shared `js/algorithms.js`:

- **Euclidean** — distance test at pixel centres
- **Bresenham** — integer midpoint, stair-stepped
- **Threshold** — corner coverage, chunkier

Switching algorithm visibly changes the cell pattern.

---

## 9. 3D rendering

Each voxel is a `THREE.Mesh` with `MeshLambertMaterial` whose `map` is a
`THREE.Texture` loaded from the base64 data URI in `MC_TEX[key]`. Texture
filters: `NearestFilter` (no smoothing) + no mipmaps — pixel-perfect MC look.

**Render modes** (state.render) drive which voxels are emitted via
`voxelShell(Dx, Dy, Dz, mode, axis, cut)`:

- **Filled**: every kept voxel with at least one exposed face (cut face
  shows solid interior)
- **Thin**: only ellipsoid surface (1-cell shell)
- **Thick**: ellipsoid surface + 1 inward layer

**Wireframe**: special style toggled by the canvas Grid button in 3D.
Replaces all materials with a single `MeshBasicMaterial({ wireframe: true,
color: gold })`. Restores the previous style when toggled off.

---

## 10. Animations

| Name | Spec | Use |
|---|---|---|
| Micro hover/click | 120ms ease | pills, buttons |
| Canvas pulse | 150ms ease · 1→1.012→1 | slider feedback |
| Splash text pulse (legacy) | 800ms alternate | reserved for drawer (none currently) |
| Pinch zoom/rotate | real-time | 3D camera |

`prefers-reduced-motion` is respected.

---

## 11. Sounds

Synthesized via WebAudio (`js/audio.js`). MC-flavoured palette: noise
burst with aggressive lowpass for the "block-place" thud + low sines.

| Name | Spec | Use |
|---|---|---|
| click | noise burst 45ms · lowpass 900Hz · gain .035 | any button |
| hover | 240Hz sine 20ms gain .012 | desktop only |
| open  | noise + 220Hz sine | (reserved) |
| close | 220Hz sine + noise | (reserved) |
| ok    | 380→560Hz sine sequence | save, download |
| pop   | noise burst lowpass 1400Hz gain .04 | mode/shape toggle |
| tick  | 480Hz sine 18ms gain .012 | every 4th slider step |
| error | 120Hz sine 200ms gain .04 | invalid action |

---

## 12. Keyboard shortcuts

- `G` Grid (or wireframe in 3D)
- `C` Center guides
- `D` Download PNG
- `I` Info chip
- `M` Toggle 2D / 3D
- `S` Sounds on/off

(No `T` — Block Round has no theme switch.)

---

## 13. Accessibility

- Gold over bedrock = 13:1 ✓; cream over stone = ~8:1 ✓
- Visible focus: 3px gold outline + 1px bedrock inner
- EVERY text over texture has `text-shadow 1px 1px 0 #1a0e04`
- `prefers-reduced-motion` clamps animations
- Touch targets ≥ 44px (button heights with borders satisfy this)
- Press Start 2P AVOIDED in body copy (illegible below 11px)

---

## 14. License & trademarks

- **Code:** All Rights Reserved (see `LICENSE`)
- **MC textures:** property of Mojang Studios / Microsoft. Used here
  under a non-commercial, fan-project rationale. The repository
  reproduces them in two forms:
  1. `textures/*.png` for CSS background-image references
  2. base64 data URIs in `js/textures.js` for canvas drawing (sidesteps
     file:// CORS limits)
- **Not affiliated** with Mojang/Microsoft. "Minecraft" is a trademark
  of Mojang Synergies AB.

---

## 15. Don'ts

- DO NOT use border-radius — breaks the blocky aesthetic
- DO NOT use Inter as display font (only for body)
- DO NOT skip text-shadow over textures — text becomes illegible
- DO NOT add a light/dark theme — Block Round is single-theme
- DO NOT use crossOrigin='anonymous' on `<img>` for textures — kills
  loading on `file://`. The base64 data URIs sidestep this entirely.
- DO NOT add 3D-style pills (Classic/Smooth/Blocks) — those belong only
  to Pixel Round; textures already determine the 3D look here
- DO NOT keep the cut slider max at 64 when the axis dim is smaller
- DO NOT use cumulative zoom on the canvas Zoom button — toggle on/off
