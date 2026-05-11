/* =============================================================================
   Block Round — js/canvas2d.js
   All Rights Reserved on code. MC textures are Mojang property.

   2D renderer that paints each filled cell with a slice of an MC block
   texture. Uses the shared algorithms (Euclidean/Bresenham/Threshold)
   plus applyRenderMode (filled/thin/thick) from algorithms.js.

   Block selection rules (see pickBlockFor):
     • random       → terrain-tiered cross-section. grass_side on the
                      top-most cell of each column, then dirt, stone
                      with sparse ores (coal/iron/redstone/gold/lapis/
                      diamond/emerald/cobble) via _pickOreForStone,
                      deepslate, bedrock on the very bottom row. Band
                      boundaries are wavy per column via _hash01.
     • grass_block  → grass_side cap on top, dirt below.
     • dirt         → dirt everywhere (no cap).
     • <any other>  → that single block, full figure.

   Sand / gravel fall animation:
     After 500 ms hold, every cell falls onto an invisible floor at the
     figure's bottom-most row, stacked per column from the floor up.
     The animation captures the f-grid at start and is driven by
     _fallStart / _fallCurrentDist / requestAnimationFrame loops. The
     state survives cosmetic redraws (grid/center/overlay) so the user
     never has to re-watch the fall just because they changed a toggle.
   ============================================================================ */

function getAccentColor(){ return '#FFEC4F'; }
function getOverlayColor(){ return '#FFFFFF'; } /* white reads well over textures */
function getGridColor(){ return 'rgba(0,0,0,.32)'; }
function getCenterColor(){ return 'rgba(255,236,79,.30)'; }

function snap(v){ return Math.floor(v) + 0.5; }

function drawFullGrid(ctx, ps, ox, oy, cW, cH){
  ctx.save();
  ctx.strokeStyle = getGridColor();
  ctx.lineWidth = 1;
  ctx.beginPath();
  const sx = ((ox % ps) + ps) % ps - ps;
  const sy = ((oy % ps) + ps) % ps - ps;
  for (let x = sx; x <= cW + ps; x += ps){
    const v = snap(x);
    ctx.moveTo(v, 0); ctx.lineTo(v, cH);
  }
  for (let y = sy; y <= cH + ps; y += ps){
    const v = snap(y);
    ctx.moveTo(0, v); ctx.lineTo(cW, v);
  }
  ctx.stroke();
  ctx.restore();
}

function drawCenterGuides(ctx, cx, cy, ps, ox, oy, cW, cH){
  const isEX = (cx === Math.floor(cx));
  const isEY = (cy === Math.floor(cy));
  ctx.save();
  ctx.fillStyle = getCenterColor();
  const pw = Math.ceil(ps), ph = Math.ceil(ps);
  if (isEX){
    ctx.fillRect(Math.floor(ox + (Math.floor(cx) - 1) * ps), 0, pw, cH);
    ctx.fillRect(Math.floor(ox + Math.floor(cx) * ps), 0, pw, cH);
  } else {
    ctx.fillRect(Math.floor(ox + Math.floor(cx) * ps), 0, pw, cH);
  }
  const drawRow = (ry) => {
    if (isEX){
      const c1 = Math.floor(ox + (Math.floor(cx) - 1) * ps);
      const c2 = Math.floor(ox + Math.floor(cx) * ps);
      ctx.fillRect(0, ry, c1, ph);
      ctx.fillRect(c1 + pw, ry, c2 - c1 - pw, ph);
      ctx.fillRect(c2 + pw, ry, cW - c2 - pw, ph);
    } else {
      const c1 = Math.floor(ox + Math.floor(cx) * ps);
      ctx.fillRect(0, ry, c1, ph);
      ctx.fillRect(c1 + pw, ry, cW - c1 - pw, ph);
    }
  };
  if (isEY){
    drawRow(Math.floor(oy + (Math.floor(cy) - 1) * ps));
    drawRow(Math.floor(oy + Math.floor(cy) * ps));
  } else {
    drawRow(Math.floor(oy + Math.floor(cy) * ps));
  }
  ctx.restore();
}

function drawPerfectOverlay(ctx, cx, cy, rx, ry, ps, ox, oy){
  const scrCX = ox + cx * ps, scrCY = oy + cy * ps;
  const srX = rx * ps, srY = ry * ps;
  if (srX < 1 || srY < 1) return;
  const steps = Math.ceil(2 * Math.PI * Math.max(srX, srY) * 8);
  const seen = new Set();
  ctx.fillStyle = getOverlayColor();
  for (let s = 0; s < steps; s++){
    const a = (s / steps) * Math.PI * 2;
    const sx = Math.floor(scrCX + Math.cos(a) * srX);
    const sy = Math.floor(scrCY + Math.sin(a) * srY);
    const k = sx * 65536 + sy;
    if (!seen.has(k)){ seen.add(k); ctx.fillRect(sx, sy, 1, 1); }
  }
}

/* Pre-computed per-column top/bottom row indices so we can stamp grass on
   the silhouette top and dirt below for terrain-style picks. */
function computeColumnExtremes(f, Gx, Gy){
  const top = new Int32Array(Gx).fill(-1);
  const bot = new Int32Array(Gx).fill(-1);
  let gTop = -1, gBot = -1;
  for (let i = 0; i < Gx; i++){
    for (let j = 0; j < Gy; j++)       if (f[j][i]){ top[i] = j; break; }
    for (let j = Gy - 1; j >= 0; j--)  if (f[j][i]){ bot[i] = j; break; }
    if (top[i] >= 0 && (gTop === -1 || top[i] < gTop)) gTop = top[i];
    if (bot[i] >= 0 && bot[i] > gBot) gBot = bot[i];
  }
  return { top, bot, gTop, gBot };
}

/* Deterministic small jitter for natural variety in tiered random. */
/* xxhash-style mixer — drops the visible diagonal stripes the previous
   `% 100` hash produced (which read as a coal "staircase" in the screenshot). */
function _hash01(i, j){
  let h = (i * 2654435761) ^ (j * 40503);
  h = Math.imul(h ^ (h >>> 16), 0x21f0aaad);
  h = Math.imul(h ^ (h >>> 15), 0x735a2d97);
  h = h ^ (h >>> 15);
  return (h >>> 0) / 0x100000000;
}

/* For animated textures (magma, sea_lantern, prismarine) the PNG is a vertical
   strip of 16×16 frames. Draw only the top frame so blocks don't squash. */
function drawBlockImage(ctx, img, dx, dy, dw, dh){
  const sw = img.naturalWidth;
  const sh = img.naturalHeight;
  if (sh > sw * 1.5){
    ctx.drawImage(img, 0, 0, sw, sw, dx, dy, dw, dh);
  } else {
    ctx.drawImage(img, dx, dy, dw, dh);
  }
}

/* Ore pool sampled inside the stone band. Probabilities ordered roughly by
   Minecraft rarity so the cross-section reads naturally. */
function _pickOreForStone(r){
  if (r < 0.06)  return 'coal';
  if (r < 0.10)  return 'iron_ore';
  if (r < 0.125) return 'redstone';
  if (r < 0.14)  return 'gold_ore';
  if (r < 0.15)  return 'lapis';
  if (r < 0.157) return 'diamond_ore';
  if (r < 0.162) return 'emerald_ore';
  if (r < 0.18)  return 'cobble';
  return 'stone';
}

function pickBlockFor(i, j, ext){
  const block = state.mcBlock;

  if (block === 'random' && ext){
    const top = ext.gTop, bot = ext.gBot;
    const span = bot - top;
    if (span <= 0) return 'grass';
    const t = (j - top) / span;
    const r = _hash01(i, j);
    // Add per-column jitter so the layer borders are wavy, not perfect
    // straight lines crossing the whole figure.
    const dirtCut = 0.20 + (_hash01(i, 17) - 0.5) * 0.10;
    const deepCut = 0.80 + (_hash01(i, 113) - 0.5) * 0.12;
    // 2D is a side view, so the top voxels show the grass-block SIDE
    // texture (grass band + dirt body) — not the green grass_top.
    if (j === ext.top[i])       return 'grass_side';
    if (j === bot && span > 4)  return 'bedrock';
    if (t < dirtCut)            return 'dirt';
    if (t < deepCut)            return _pickOreForStone(r);
    return 'deepslate';
  }

  if (block === 'random'){
    return RANDOM_POOL[(i * 7 + j * 3) % RANDOM_POOL.length];
  }

  // Grass Block: top row uses grass_side (grass strip + dirt body — the
  // canonical Minecraft side texture); everything below is dirt.
  // Plain Dirt: no grass-on-top stamping, entire figure is dirt.
  if (block === 'grass_block' && ext){
    const topJ = ext.top[i];
    if (topJ >= 0 && j === topJ) return 'grass_side';
    return 'dirt';
  }
  return block;
}

/* ---------- 2D SAND / GRAVEL FALL ANIMATION ----------------------------- */
/* After 500 ms the cells of a fallable column collapse onto an invisible
   floor at the bottom of the figure, simulating Minecraft gravity. State
   is per-figure: start time, the original f-grid, and per-cell startJ/endJ
   so the same shape stacks at the bottom in a single pass. */
/* Only blocks that obey Minecraft gravity. soul_sand stays put in MC. */
const FALL_BLOCKS = new Set(['sand', 'gravel']);
const FALL_HOLD_MS = 500;
const FALL_G       = 21;       // squares per second² (~20% slower than g=30)
let _fallState = null;
let _fallRaf = null;

function _fallReset(){
  _fallState = null;
  if (_fallRaf){ cancelAnimationFrame(_fallRaf); _fallRaf = null; }
}

function _fallStart(f, Gx, Gy){
  let floorJ = -1;
  for (let j = Gy - 1; j >= 0; j--){
    for (let i = 0; i < Gx; i++) if (f[j][i]){ floorJ = j; break; }
    if (floorJ >= 0) break;
  }
  if (floorJ < 0) return;
  const columns = new Map();
  for (let j = 0; j < Gy; j++){
    for (let i = 0; i < Gx; i++){
      if (!f[j][i]) continue;
      if (!columns.has(i)) columns.set(i, []);
      columns.get(i).push({ i, startJ: j, endJ: j });
    }
  }
  let maxFall = 0;
  columns.forEach(col => {
    col.sort((a, b) => a.startJ - b.startJ);
    col.forEach((c, idx) => {
      c.endJ = floorJ - (col.length - 1 - idx);
      const d = c.endJ - c.startJ;
      if (d > maxFall) maxFall = d;
    });
  });
  const cells = [];
  columns.forEach(col => col.forEach(c => cells.push(c)));
  _fallState = { cells, maxFall, startTime: performance.now() };
}

function _fallCurrentDist(){
  if (!_fallState) return 0;
  const elapsed = performance.now() - _fallState.startTime;
  if (elapsed < FALL_HOLD_MS) return 0;
  const t = (elapsed - FALL_HOLD_MS) / 1000;
  return 0.5 * FALL_G * t * t;
}

const BLOCK_FALLBACK_COLOR = {
  grass:'#7BB04F', dirt:'#8B6F47', stone:'#A0A0A0', cobble:'#7d7d7d',
  oak:'#a87a4a', darkOak:'#4a2c14', sand:'#d8c896', bricks:'#bc7a4f',
  diamond:'#5dd3d3', gold:'#ffe14a', redstone:'#9a3030', emerald:'#3ec06d',
  moss:'#5b8b40', quartz:'#ece6d6', obsidian:'#1a1028', ice:'#a7d8ff',
  nether_bricks:'#3a1818', iron:'#dcdcdc',
};

function draw2D(canvas){
  if (!canvas) return;
  const cw = canvas.clientWidth  || 300;
  const ch = canvas.clientHeight || 220;
  const dpr = window.devicePixelRatio || 1;
  canvas.width  = Math.max(1, Math.floor(cw * dpr));
  canvas.height = Math.max(1, Math.floor(ch * dpr));
  const ctx = canvas.getContext('2d');
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.imageSmoothingEnabled = false;
  ctx.clearRect(0, 0, cw, ch);

  const isEllipse = state.shape === 'ellipse';
  const D  = state.size;
  const Wd = isEllipse ? state.width : D;
  const Hd = isEllipse ? state.height : D;
  const pad = 2;
  const Gx = Wd + pad * 2;
  const Gy = Hd + pad * 2;
  const cx = Gx / 2, cy = Gy / 2;
  const rx = Wd / 2, ry = Hd / 2;

  const zoom = state.zoom2D || 1;
  let ps = Math.min(cw / Gx, ch / Gy) * zoom;
  let ox = (cw - Gx * ps) / 2;
  let oy = (ch - Gy * ps) / 2;

  if (state.zoomBtn && !isEllipse){
    const m = 1;
    const srcSpan = Math.max((cx + m) - (pad - m), (cy + m) - (pad - m));
    const zps = Math.min(cw, ch) / srcSpan;
    ps = zps;
    ox = -(pad - m) * zps;
    oy = -(pad - m) * zps;
  }

  const fRaw = computeFilled(Gx, Gy, cx, cy, rx, ry, state.algo);
  const f    = applyRenderMode(fRaw, Gx, Gy, state.render);
  const ext  = computeColumnExtremes(f, Gx, Gy);

  // Drive sand/gravel collapse animation by replacing per-cell j with an
  // interpolated y for cells with a non-zero fall distance.
  const fallActive = _fallState && FALL_BLOCKS.has(state.mcBlock);
  const fd = fallActive ? _fallCurrentDist() : 0;

  if (fallActive){
    const img = loadBlockImage(state.mcBlock);
    for (const c of _fallState.cells){
      const dCol = c.endJ - c.startJ;
      const cur = Math.min(c.startJ + fd, c.endJ);
      const x = Math.floor(ox + c.i * ps);
      const y = Math.floor(oy + cur * ps);
      const w = Math.floor(ox + (c.i + 1) * ps) - x;
      const h = Math.floor(oy + (cur + 1) * ps) - y;
      if (imageReady(img)){
        drawBlockImage(ctx, img, x, y, w, h);
      } else {
        ctx.fillStyle = BLOCK_FALLBACK_COLOR[state.mcBlock] || '#d8c896';
        ctx.fillRect(x, y, w, h);
      }
    }
    // Schedule next frame until the animation finishes.
    if (fd < _fallState.maxFall){
      if (_fallRaf) cancelAnimationFrame(_fallRaf);
      _fallRaf = requestAnimationFrame(() => { _fallRaf = null; draw2D(canvas); });
    }
  } else {
    for (let j = 0; j < Gy; j++){
      for (let i = 0; i < Gx; i++){
        if (!f[j][i]) continue;
        const x = Math.floor(ox + i * ps);
        const y = Math.floor(oy + j * ps);
        const w = Math.floor(ox + (i + 1) * ps) - x;
        const h = Math.floor(oy + (j + 1) * ps) - y;
        const blockKey = pickBlockFor(i, j, ext);
        const img = loadBlockImage(blockKey);
        if (imageReady(img)){
          drawBlockImage(ctx, img, x, y, w, h);
        } else {
          ctx.fillStyle = BLOCK_FALLBACK_COLOR[blockKey] || '#888';
          ctx.fillRect(x, y, w, h);
          if (img && !img.__bound){
            img.__bound = true;
            img.addEventListener('load', () => {
              if (typeof redraw === 'function') redraw();
            }, { once: true });
          }
        }
      }
    }
    // If the user just switched to a fallable block, arm the fall state.
    if (FALL_BLOCKS.has(state.mcBlock) && !_fallState){
      _fallStart(f, Gx, Gy);
      if (_fallRaf) cancelAnimationFrame(_fallRaf);
      _fallRaf = requestAnimationFrame(() => { _fallRaf = null; draw2D(canvas); });
    }
  }

  if (state.center) drawCenterGuides(ctx, cx, cy, ps, ox, oy, cw, ch);
  if (state.grid) drawFullGrid(ctx, ps, ox, oy, cw, ch);
  if (state.overlay) drawPerfectOverlay(ctx, cx, cy, rx, ry, ps, ox, oy);
}

function updateInfoChip(){
  const host = dom.canvasFrame;
  if (!host) return;
  const diamEl = host.querySelector('[data-info-diam]');
  const radEl  = host.querySelector('[data-info-rad]');
  const areaEl = host.querySelector('[data-info-area]');
  const algoEl = host.querySelector('[data-info-algo]');
  if (!diamEl) return;

  const isEllipse = state.shape === 'ellipse';
  if (state.mode === '2d'){
    if (isEllipse){
      diamEl.textContent = `${state.width}×${state.height}`;
      radEl.textContent  = `${(state.width/2)}×${(state.height/2)}`;
    } else {
      diamEl.textContent = state.size;
      radEl.textContent  = (state.size / 2);
    }
    areaEl.textContent = area2D(state.size, state.width, state.height, isEllipse, state.algo);
  } else {
    if (isEllipse){
      diamEl.textContent = `${state.width}×${state.height}×${state.depth}`;
      radEl.textContent  = `${state.width/2}×${state.height/2}×${state.depth/2}`;
    } else {
      diamEl.textContent = state.size;
      radEl.textContent  = (state.size / 2);
    }
    const Dx = isEllipse ? state.width : state.size;
    const Dy = isEllipse ? state.height : state.size;
    const Dz = isEllipse ? state.depth : state.size;
    areaEl.textContent = voxelVolume(Dx, Dy, Dz);
  }
  algoEl.textContent = state.mcBlock === 'random' ? 'Random' :
                       (MC_BLOCKS[state.mcBlock]?.name || state.mcBlock);
}

function downloadPNG(){
  const isEllipse = state.shape === 'ellipse';

  if (state.mode === '2d'){
    // High-res PNG: each cell at 16px (= 1 MC block in actual game scale)
    const Wd = isEllipse ? state.width : state.size;
    const Hd = isEllipse ? state.height : state.size;
    const Gx = Wd + 2, Gy = Hd + 2;
    const TILE = 16;
    const off = document.createElement('canvas');
    off.width = Gx * TILE; off.height = Gy * TILE;
    const ctx = off.getContext('2d');
    ctx.imageSmoothingEnabled = false;
    const cx = Gx / 2, cy = Gy / 2;
    const rx = Wd / 2, ry = Hd / 2;
    const fRaw = computeFilled(Gx, Gy, cx, cy, rx, ry, state.algo);
    const f    = applyRenderMode(fRaw, Gx, Gy, state.render);
    const ext  = computeColumnExtremes(f, Gx, Gy);
    for (let j = 0; j < Gy; j++)
      for (let i = 0; i < Gx; i++){
        if (!f[j][i]) continue;
        const blockKey = pickBlockFor(i, j, ext);
        const img = loadBlockImage(blockKey);
        if (imageReady(img)){
          drawBlockImage(ctx, img, i * TILE, j * TILE, TILE, TILE);
        } else {
          ctx.fillStyle = BLOCK_FALLBACK_COLOR[blockKey] || '#888';
          ctx.fillRect(i * TILE, j * TILE, TILE, TILE);
        }
      }
    off.toBlob(blob => {
      if (!blob) return;
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      const name = isEllipse
        ? `block-round-ellipse-${state.width}x${state.height}-${state.mcBlock}-${state.render}.png`
        : `block-round-circle-d${state.size}-${state.mcBlock}-${state.render}.png`;
      a.href = url; a.download = name;
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }, 'image/png');
  } else {
    if (!dom.canvas3D || !renderer3D) return;
    if (scene3D && camera3D) renderer3D.render(scene3D, camera3D);
    const name = state.shape === 'ellipse'
      ? `block-round-ellipsoid-${state.width}x${state.height}x${state.depth}-${state.mcBlock}.png`
      : `block-round-sphere-d${state.size}-${state.mcBlock}.png`;
    dom.canvas3D.toBlob(blob => {
      if (!blob) return;
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = name;
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }, 'image/png');
  }
}
