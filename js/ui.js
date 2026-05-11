/* =============================================================================
   Block Round — js/ui.js
   All Rights Reserved.

   Mirrors Pixel Round's ui.js but:
     - NO theme switch (single MC theme)
     - NO style3d pills (Block Round doesn't have them)
     - MC block picker (.mc-list) is built dynamically from MC_BLOCKS
     - Grid button toggles 2D cell grid OR 3D wireframe
   ============================================================================ */

/* ---------- ROUTE NAVIGATION ---------------------------------------------- */
function goRoute(route){
  state.route = route;
  document.querySelectorAll('.route').forEach(r => {
    r.hidden = (r.dataset.route !== route);
  });
  document.querySelectorAll('.icon-btn[data-route]').forEach(b => {
    b.classList.toggle('active', b.dataset.route === route);
  });
  if (route === 'tool') requestAnimationFrame(() => { resize3D(); redraw(); });
  Sfx.click();
}

/* ---------- BUILD MC PICKER ---------------------------------------------- */
/* Dynamically populates .mc-list from MC_BLOCKS so the picker reflects
   whatever block catalog state.js declares. Random tile is special-cased. */
function buildMCList(){
  const host = dom.mcList;
  if (!host) return;
  host.innerHTML = '';
  Object.keys(MC_BLOCKS).forEach(key => {
    const b = MC_BLOCKS[key];
    // Internal-only entries (grass_top / grass_side / oak_log_top) exist
    // for face-stamping in 3D, but they shouldn't show up in the picker.
    if (b.internal) return;
    const tile = document.createElement('div');
    tile.className = 'mc-block' + (key === 'random' ? ' random' : '')
                    + (key === state.mcBlock ? ' active' : '');
    tile.dataset.block = key;
    tile.title = b.name;
    if (key !== 'random' && b.src) tile.style.backgroundImage = `url('${b.src}')`;
    host.appendChild(tile);
  });

  // Wheel → horizontal scroll (most MC pickers live in a narrow horizontal
  // strip; users expect scroll-wheel to slide it sideways).
  host.addEventListener('wheel', e => {
    if (host.scrollWidth <= host.clientWidth) return;
    e.preventDefault();
    host.scrollLeft += (e.deltaY !== 0 ? e.deltaY : e.deltaX);
  }, { passive: false });

  // Click + drag horizontally (a la image gallery).
  let dragging = false, startX = 0, startScroll = 0, hasMoved = false;
  host.addEventListener('mousedown', e => {
    dragging = true; hasMoved = false;
    startX = e.clientX; startScroll = host.scrollLeft;
    host.classList.add('dragging');
  });
  window.addEventListener('mousemove', e => {
    if (!dragging) return;
    const dx = e.clientX - startX;
    if (Math.abs(dx) > 3) hasMoved = true;
    host.scrollLeft = startScroll - dx;
  });
  window.addEventListener('mouseup', () => {
    host.classList.remove('dragging');
    if (dragging && hasMoved){
      // Swallow the click that follows a drag so we don't pick the tile we
      // ended up over. Listener self-removes.
      const swallow = ev => { ev.stopPropagation(); ev.preventDefault(); };
      host.addEventListener('click', swallow, { capture: true, once: true });
    }
    dragging = false;
  });
}

/* ---------- SYNCSHAPE ----------------------------------------------------- */
function syncShape(){
  const showSize  = state.shape === 'circle';
  const showW     = state.shape === 'ellipse';
  const showH     = state.shape === 'ellipse';
  const showDepth = state.shape === 'ellipse' && state.mode === '3d';
  document.querySelector('[data-dim=size]').hidden   = !showSize;
  document.querySelector('[data-dim=width]').hidden  = !showW;
  document.querySelector('[data-dim=height]').hidden = !showH;
  document.querySelector('[data-dim=depth]').hidden  = !showDepth;

  // Algorithms only matter in 2D. Block Round has no style3d pills, so the
  // right pill row hides entirely in 3D.
  document.querySelectorAll('.algo-pill').forEach(b => b.hidden = state.mode === '3d');
  const rightRow = document.querySelector('.pill-row.right');
  if (rightRow) rightRow.hidden = state.mode === '3d';

  document.querySelector('.tool-grid').classList.toggle('has-cut', state.mode === '3d');

  syncCutMax();

  document.querySelectorAll('.mode-btn').forEach(b => b.classList.toggle('active', b.dataset.mode === state.mode));
  document.querySelectorAll('.shape-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.shape === state.shape);
    const lbl = SHAPE_LABELS[b.dataset.shape]?.[state.mode];
    if (lbl) b.textContent = lbl;
  });

  const overlayBtn = document.querySelector('[data-act=overlay]');
  const zoomBtn    = document.querySelector('[data-act=zoom]');
  if (overlayBtn) overlayBtn.hidden = state.mode === '3d';
  if (zoomBtn)    zoomBtn.hidden    = state.mode === '3d';

  document.body.classList.toggle('mode3d', state.mode === '3d');
}

function syncCutMax(){
  const cs = document.querySelector('[data-slider=cut]');
  if (!cs) return;
  const isEllipse = state.shape === 'ellipse';
  const Dx = isEllipse ? state.width : state.size;
  const Dy = isEllipse ? state.height : state.size;
  // Diagonal cut uses (x + y) <= cut, so it ranges 0..(Dx+Dy).
  // Straight cuts (X or Y) range 0..max-of-that-axis.
  const maxVal = state.axis === 'x'    ? Dx
               : state.axis === 'y'    ? Dy
               : /* 'diag' */            (Dx + Dy);
  cs.max = maxVal;
  cs.min = 0;
  const pct = (state.cutPct == null) ? 1 : state.cutPct;
  const absVal = Math.round(pct * maxVal);
  cs.value = Math.max(0, Math.min(maxVal, absVal));
  state.cut = +cs.value;
  setSliderPct(cs);
  const cv = document.querySelector('[data-val=cut]');
  if (cv) cv.textContent = cs.value;
}

/* ---------- UNDO / REDO HISTORY ------------------------------------------
   Lightweight time-travel for the user's state edits. We snapshot only
   the fields that change the FIGURE (size/shape/render/algo/cut/block/
   etc.) — camera angle, edge overlay toggle, theme and other purely
   visual flags are deliberately left out.

   Two stacks: undo and redo. Snapshots are JSON strings of the snapshot
   shape so we can compare cheaply and detect duplicate consecutive
   pushes (which slider drags would otherwise generate by the dozen).
   Slider input uses pushHistoryDebounced (commits 250 ms after the
   last input event), while discrete clicks (block/render/algo/mode/
   shape/axis) call pushHistory immediately. Capped at 50 entries. */
const HIST_FIELDS = [
  'mode', 'shape', 'render', 'algo',
  'size', 'width', 'height', 'depth',
  'cut', 'cutPct', 'axis',
  'mcBlock',
];
const HIST_MAX = 50;
let _histStack = [];
let _histPos = -1;
let _histDebounce = null;
let _histApplying = false;     // re-entrancy guard during applyHistory()

function _histSnap(){
  const o = {};
  HIST_FIELDS.forEach(k => o[k] = state[k]);
  return JSON.stringify(o);
}
function pushHistory(){
  if (_histApplying) return;
  const snap = _histSnap();
  if (_histPos >= 0 && _histStack[_histPos] === snap) return;
  // Drop everything after current pos (redo branch is invalidated).
  _histStack = _histStack.slice(0, _histPos + 1);
  _histStack.push(snap);
  _histPos = _histStack.length - 1;
  if (_histStack.length > HIST_MAX){
    _histStack.shift();
    _histPos--;
  }
}
function pushHistoryDebounced(){
  if (_histDebounce) clearTimeout(_histDebounce);
  _histDebounce = setTimeout(() => { _histDebounce = null; pushHistory(); }, 250);
}
function _applyHistory(snap){
  _histApplying = true;
  const o = JSON.parse(snap);
  Object.assign(state, o);
  // Rehydrate the UI controls to match the restored state.
  document.querySelectorAll('input[type=range]').forEach(s => {
    const k = s.dataset.slider;
    if (k && (k in state)) s.value = state[k];
    setSliderPct(s);
  });
  ['render','algo'].forEach(k =>
    document.querySelectorAll(`[data-${k}]`).forEach(p => p.classList.toggle('active', p.dataset[k] === state[k]))
  );
  document.querySelectorAll('[data-axis]').forEach(b => b.classList.toggle('active', b.dataset.axis === state.axis));
  document.querySelectorAll('[data-block]').forEach(b => b.classList.toggle('active', b.dataset.block === state.mcBlock));
  document.querySelectorAll('[data-val]').forEach(v => {
    const k = v.dataset.val;
    if (k && k in state) v.textContent = state[k];
  });
  syncShape();
  if (typeof _fallReset === 'function') _fallReset();
  if (typeof _fall3DReset === 'function') _fall3DReset();
  if (state.mode === '3d' && typeof autoZoom3D === 'function') autoZoom3D();
  redraw();
  _histApplying = false;
}
function undo(){
  if (_histPos <= 0) return false;
  _histPos--;
  _applyHistory(_histStack[_histPos]);
  return true;
}
function redo(){
  if (_histPos >= _histStack.length - 1) return false;
  _histPos++;
  _applyHistory(_histStack[_histPos]);
  return true;
}

/* ---------- REDRAW ------------------------------------------------------- */
let _redrawRaf = null;
function redraw(){
  if (_redrawRaf) cancelAnimationFrame(_redrawRaf);
  _redrawRaf = requestAnimationFrame(() => {
    _redrawRaf = null;
    if (state.mode === '2d'){
      draw2D(dom.canvas2D);
    } else {
      if (init3D(dom.canvas3D)) update3D();
    }
    updateInfoChip();
    savePrefs();
  });
}

/* ---------- CANVAS PULSE -------------------------------------------------- */
let _pulseTimer = null;
function pulseCanvas(){
  if (!dom.canvasFrame) return;
  dom.canvasFrame.classList.remove('pulse');
  void dom.canvasFrame.offsetWidth;
  dom.canvasFrame.classList.add('pulse');
  clearTimeout(_pulseTimer);
  _pulseTimer = setTimeout(() => dom.canvasFrame.classList.remove('pulse'), 200);
}

/* ---------- TOAST -------------------------------------------------------- */
function toast(msg, kind = ''){
  if (!dom.toastHost) return;
  const el = document.createElement('div');
  el.className = 'toast ' + (kind || '');
  el.textContent = msg;
  dom.toastHost.appendChild(el);
  setTimeout(() => {
    el.classList.add('out');
    setTimeout(() => el.remove(), 250);
  }, 1700);
}

/* ---------- RESET -------------------------------------------------------- */
function resetState(){
  Object.assign(state, {
    mode:'2d', shape:'circle', render:'filled', algo:'euclidean',
    size:16, width:20, height:12, depth:14, cut:16, cutPct:1.0, axis:'y',
    grid:false, center:false, overlay:false, zoomBtn:false, info:false,
    zoom2D:1, mcBlock:'random', edges3d:true, edges3dTransparent:false,
  });
  document.querySelectorAll('input[type=range]').forEach(s => {
    const k = s.dataset.slider;
    if (k && (k in state)) s.value = state[k];
    setSliderPct(s);
  });
  document.querySelectorAll('[data-pref]').forEach(p => {
    if (p.dataset.pref in state) p.checked = !!state[p.dataset.pref];
  });
  ['render','algo'].forEach(k =>
    document.querySelectorAll(`[data-${k}]`).forEach(p => p.classList.toggle('active', p.dataset[k] === state[k]))
  );
  document.querySelectorAll('[data-axis]').forEach(b => b.classList.toggle('active', b.dataset.axis === state.axis));
  document.querySelectorAll('[data-block]').forEach(b => b.classList.toggle('active', b.dataset.block === state.mcBlock));
  document.querySelectorAll('[data-val]').forEach(v => {
    const k = v.dataset.val;
    if (k && k in state) v.textContent = state[k];
  });
  document.querySelectorAll('[data-act=grid],[data-act=center],[data-act=overlay],[data-act=zoom]').forEach(b => {
    const act = b.dataset.act === 'zoom' ? 'zoomBtn' : b.dataset.act;
    b.classList.toggle('active', !!state[act]);
  });
  state.zoom2D = 1;
  syncShape();
  if (state.mode === '3d') resetCamera3D();
  redraw();
  // Record the reset as one history entry so Ctrl+Z brings the user
  // straight back to whatever they had before clicking Reset.
  if (typeof pushHistory === 'function') pushHistory();
  Sfx.ok();
  toast('Reset', 'ok');
}

/* Map each picker block to one of the MC sound categories so the tile-
   click plays the right "dig" / "place" sample. Blocks not listed here
   fall back to the generic Sfx.click() noise. Categories: stone, wood,
   grass, sand, gravel, cloth, glass, snow. Blocks with their own
   dedicated sound (tnt fuse, slime jump) skip this map. */
const BLOCK_SOUND_CATEGORY = {
  stone:'stone', cobble:'stone', mossy_cobble:'stone', smooth_stone:'stone',
  granite:'stone', andesite:'stone', polished_andesite:'stone', diorite:'stone',
  deepslate:'stone', bedrock:'stone', end_stone:'stone', sandstone:'stone',
  bricks:'stone', nether_bricks:'stone', netherrack:'stone',
  prismarine:'stone', prismarine_bricks:'stone', dark_prismarine:'stone',
  obsidian:'stone', crying_obsidian:'stone', quartz:'stone',
  glowstone:'stone', sea_lantern:'stone', shroomlight:'stone',
  magma:'stone', bone:'stone',
  iron:'stone', gold:'stone', diamond:'stone', emerald:'stone', copper:'stone',
  coal:'stone', iron_ore:'stone', gold_ore:'stone',
  diamond_ore:'stone', emerald_ore:'stone', redstone:'stone', lapis:'stone',
  furnace:'stone',
  oak:'wood', darkOak:'wood', birch:'wood', spruce:'wood', jungle:'wood', acacia:'wood',
  oak_log:'wood', birch_log:'wood', spruce_log:'wood',
  jungle_log:'wood', acacia_log:'wood', dark_oak_log:'wood',
  bookshelf:'wood', crafting_table:'wood',
  pumpkin:'wood', melon:'wood',
  red_mushroom:'wood', brown_mushroom:'wood',
  grass_block:'grass', dirt:'grass', mycelium:'grass', podzol:'grass', moss:'grass',
  sand:'sand', soul_sand:'sand',
  gravel:'gravel',
  glass:'glass', ice:'glass', packed_ice:'glass', blue_ice:'glass',
  white_wool:'cloth', black_wool:'cloth', red_wool:'cloth', green_wool:'cloth',
  blue_wool:'cloth', yellow_wool:'cloth', orange_wool:'cloth', light_blue_wool:'cloth',
  sponge:'cloth', hay:'cloth',
  snow_block:'snow',
};

/* Non-navigation tool toggle. Used to auto-return to the canvas when the
   user clicks any of these while on Info or Settings. */
function isToolToggle(el){
  if (!el) return false;
  if (el.dataset.route || el.dataset.act === 'logo') return false;
  if (el.dataset.act === 'info-chip' || el.dataset.act === 'theme') return false;
  return !!(el.dataset.render || el.dataset.algo
         || el.dataset.mode   || el.dataset.shape || el.dataset.axis
         || el.dataset.block  || el.dataset.act);
}

/* ---------- CLICK DELEGATION --------------------------------------------- */
let prevStyle3D = 'classic'; // for wireframe toggle (only relevant for grid btn)
function setupClickDelegation(){
  document.body.addEventListener('click', e => {
    const t = e.target.closest('[data-act],[data-route],[data-render],[data-algo],[data-mode],[data-shape],[data-axis],[data-block]');
    if (!t) return;

    if (t.dataset.route){
      const next = (state.route === t.dataset.route && t.dataset.route !== 'tool') ? 'tool' : t.dataset.route;
      goRoute(next);
      return;
    }

    if (state.route !== 'tool' && isToolToggle(t)){
      goRoute('tool');
    }

    const a = t.dataset.act;
    if (a === 'logo'){ goRoute('tool'); return; }
    // Day / night canvas mood toggle. Stored in state.theme and reflected
    // on document.body via the .theme-night class — CSS handles the
    // canvas-frame background gradient swap. Session-only; nothing
    // persists across reloads.
    if (a === 'theme'){
      state.theme = (state.theme === 'night') ? 'day' : 'night';
      document.body.classList.toggle('theme-night', state.theme === 'night');
      t.classList.toggle('active', state.theme === 'night');
      Sfx.click();
      toast(`Night ${state.theme === 'night' ? 'on' : 'off'}`);
      return;
    }

    if (a === 'info-chip'){
      document.querySelector('.info-chip')?.classList.toggle('open');
      Sfx.hover();
      return;
    }

    if (a === 'grid'){
      if (state.mode === '3d'){
        // Transparent and opaque blocks each have their own edge-overlay
        // preference so moving glass <-> stone doesn't surprise the user.
        // (slime / honey are translucent too — share the transparent preference.)
        const isTransparent = ['glass', 'ice', 'slime', 'honey'].includes(state.mcBlock);
        if (isTransparent) state.edges3dTransparent = !state.edges3dTransparent;
        else               state.edges3d           = !state.edges3d;
        const eff = isTransparent ? state.edges3dTransparent : state.edges3d;
        t.classList.toggle('active', eff);
        Sfx.click();
        if (typeof toggleEdges3D === 'function') toggleEdges3D();
        else update3D();
        toast(`Edges ${eff ? 'on' : 'off'}`);
      } else {
        state.grid = !state.grid;
        t.classList.toggle('active', state.grid);
        const inp = document.querySelector('[data-pref=grid]');
        if (inp) inp.checked = state.grid;
        Sfx.click(); redraw();
        toast(`Grid ${state.grid ? 'on' : 'off'}`);
      }
      return;
    }
    if (a === 'center'){
      state.center = !state.center;
      t.classList.toggle('active', state.center);
      const inp = document.querySelector('[data-pref=center]');
      if (inp) inp.checked = state.center;
      Sfx.click();
      // 3D: toggle only the center cross without rebuilding the voxel mesh
      // so any in-progress sand/gravel fall keeps animating.
      if (state.mode === '3d'){
        if (typeof toggleCenter3D === 'function') toggleCenter3D();
        else update3D();
      } else {
        redraw();
      }
      return;
    }
    if (a === 'overlay'){
      state.overlay = !state.overlay;
      t.classList.toggle('active', state.overlay);
      Sfx.click(); redraw(); return;
    }
    if (a === 'zoom'){
      state.zoomBtn = !state.zoomBtn;
      t.classList.toggle('active', state.zoomBtn);
      Sfx.click(); redraw(); return;
    }
    if (a === 'download'){ downloadPNG(); Sfx.ok(); toast('PNG saved', 'ok'); return; }
    if (a === 'schem'){
      // Sponge-format .schem (gzipped NBT) for WorldEdit / Litematica.
      if (typeof downloadSchematic === 'function'){ downloadSchematic(); Sfx.ok(); }
      return;
    }
    if (a === 'reset'){ resetState(); return; }

    if (t.dataset.render){
      state.render = t.dataset.render;
      document.querySelectorAll('[data-render]').forEach(p => p.classList.toggle('active', p === t));
      if (typeof _fallReset === 'function') _fallReset();
      Sfx.click(); redraw(); pushHistory(); return;
    }
    if (t.dataset.algo){
      state.algo = t.dataset.algo;
      document.querySelectorAll('[data-algo]').forEach(p => p.classList.toggle('active', p === t));
      if (typeof _fallReset === 'function') _fallReset();
      Sfx.click(); redraw(); pushHistory(); return;
    }
    if (t.dataset.mode){
      if (state.mode === t.dataset.mode) return;
      state.mode = t.dataset.mode;
      const gridBtn = document.querySelector('[data-act=grid]');
      if (gridBtn) gridBtn.classList.toggle('active',
        state.mode === '3d'
          ? (typeof effectiveEdges3D === 'function' ? effectiveEdges3D() : !!state.edges3d)
          : state.grid);
      syncShape();
      if (state.mode === '3d'){
        if (init3D(dom.canvas3D)){ resize3D(); autoZoom3D(); update3D(); }
      } else { redraw(); }
      Sfx.pop(); pushHistory(); return;
    }
    if (t.dataset.shape){
      if (state.shape === t.dataset.shape) return;
      state.shape = t.dataset.shape;
      syncShape();
      if (state.mode === '3d'){ autoZoom3D(); update3D(); }
      else { redraw(); }
      Sfx.pop(); pushHistory(); return;
    }
    if (t.dataset.axis){
      if (state.axis === t.dataset.axis) return;
      state.axis = t.dataset.axis;
      syncCutMax();
      document.querySelectorAll('[data-axis]').forEach(b => b.classList.toggle('active', b === t));
      // Switching the cut axis changes which side of the figure is
      // trimmed — re-fit the camera so the visible portion stays
      // centred on the canvas.
      Sfx.click(); autoZoom3D(); update3D(); pushHistory(); return;
    }
    if (t.dataset.block){
      const FALLABLE = new Set(['sand', 'gravel']);
      const reclick = state.mcBlock === t.dataset.block;
      // Re-clicking the SAME tile is normally a no-op, but for sand /
      // gravel it explicitly resets the figure so the fall replays.
      // For everything else, ignore the duplicate click.
      if (reclick && !FALLABLE.has(state.mcBlock)) return;
      const prevBlock = state.mcBlock;
      state.mcBlock = t.dataset.block;
      if (typeof _fallReset === 'function') _fallReset();
      if (typeof _fall3DReset === 'function') _fall3DReset();
      // Re-arm the geometry signature so update3D rebuilds the mesh even
      // though state didn't change — this is what restarts the fall.
      if (reclick && typeof _lastGeomSig3D !== 'undefined') _lastGeomSig3D = null;
      document.querySelectorAll('[data-block]').forEach(b => b.classList.toggle('active', b === t));
      // Choose per-block click sound. Slime/Honey play their dedicated
      // jump sample; everything else plays the right MC "place" sample
      // for its material category; anything outside the map (e.g.
      // 'random') falls back to the generic UI click. TNT used to play
      // the fuse sample here, but the fuse now belongs to the creeper
      // easter egg's stare cycle — picking the TNT tile is silent
      // except for the place click that the category map provides.
      if (prevBlock === 'tnt' && state.mcBlock !== 'tnt' && typeof Sfx.stopTnt === 'function') Sfx.stopTnt();
      if ((state.mcBlock === 'slime' || state.mcBlock === 'honey') && typeof Sfx.slime === 'function'){
        Sfx.slime();
      } else {
        const cat = BLOCK_SOUND_CATEGORY[state.mcBlock];
        if (cat && typeof Sfx.place === 'function') Sfx.place(cat);
        else Sfx.click();
      }
      if (state.mcBlock !== 'random') loadBlockImage(state.mcBlock);
      // Refresh the Grid corner button to reflect the new effective edges
      // preference (different default for transparent vs opaque blocks).
      if (state.mode === '3d' && typeof effectiveEdges3D === 'function'){
        const eff = effectiveEdges3D();
        document.querySelector('[data-act=grid]')?.classList.toggle('active', eff);
      }
      // Re-fit the camera so the tree easter egg fits when toggling on/off.
      if (state.mode === '3d' && typeof autoZoom3D === 'function') autoZoom3D();
      redraw();
      pushHistory();
      return;
    }
  });
}

/* ---------- SLIDERS ------------------------------------------------------ */
/* Double-click any slider → reset to its HTML baseline. For Cut that means
   the "no-cut" position (cutPct = 1.0); for the others it's the value="…"
   attribute the input was authored with. */
function setupSliders(){
  document.querySelectorAll('input[type=range]').forEach(sl => {
    sl.addEventListener('dblclick', () => {
      const k = sl.dataset.slider;
      if (k === 'cut'){
        state.cutPct = 1.0;
        sl.value = sl.max;
      } else {
        sl.value = sl.defaultValue;
      }
      sl.dispatchEvent(new Event('input', { bubbles: true }));
      Sfx.pop();
    });
    sl.addEventListener('input', () => {
      const k = sl.dataset.slider;
      if (!k) return;
      if (state.route !== 'tool') goRoute('tool');
      state[k] = +sl.value;
      const valEl = document.querySelector(`[data-val=${k}]`);
      if (valEl) valEl.textContent = sl.value;
      setSliderPct(sl);
      if (k === 'cut'){
        const max = +sl.max || 1;
        state.cutPct = max > 0 ? (+sl.value / max) : 1;
        // Recenter the camera every time the cut moves — the visible
        // bounding box shifts as voxels disappear, and without an
        // autoZoom call the model drifts toward the bottom-left of
        // the canvas.
        if (state.mode === '3d'){ autoZoom3D(); update3D(); }
      } else {
        // Geometry changed → restart any sand/gravel fall from scratch.
        if (typeof _fallReset === 'function') _fallReset();
        if (typeof _fall3DReset === 'function') _fall3DReset();
        syncCutMax();
        if (state.mode === '3d'){ autoZoom3D(); update3D(); }
        else { redraw(); pulseCanvas(); }
      }
      if (+sl.value % 4 === 0) Sfx.tick();
      // Slider drag fires many input events — debounce the snapshot
      // so an undo step ≈ a deliberate move, not every micro-pixel.
      pushHistoryDebounced();
    });
  });
}

/* ---------- PREFS -------------------------------------------------------- */
function setupPrefs(){
  document.querySelectorAll('[data-pref]').forEach(t => {
    t.addEventListener('change', () => {
      const k = t.dataset.pref;
      if (k === 'sound'){
        Sfx.setEnabled(t.checked);
        toast(`Sounds ${t.checked ? 'on' : 'off'}`);
      } else if (k in state){
        state[k] = t.checked;
        const btn = document.querySelector(`[data-act=${k}]`);
        if (btn) btn.classList.toggle('active', t.checked);
        redraw();
        toast(`${k} ${t.checked ? 'on' : 'off'}`);
      }
      Sfx.click();
      savePrefs();
    });
  });
}

/* ---------- 3D POINTER + PINCH + KEYBOARD (same as Pixel Round) --------- */
let _drag = null;
function setup3DPointer(){
  const frame = dom.canvasFrame;
  if (!frame) return;
  frame.addEventListener('wheel', e => {
    e.preventDefault();
    if (state.mode === '3d'){
      distance3D *= e.deltaY > 0 ? 1.08 : 0.93;
      distance3D = Math.max(20, Math.min(400, distance3D));
      updateCamera3D();
    } else {
      const nz = (state.zoom2D || 1) * (e.deltaY > 0 ? 0.92 : 1.09);
      state.zoom2D = Math.max(0.5, Math.min(8, nz));
      redraw();
    }
  }, { passive: false });
  frame.addEventListener('dblclick', () => {
    if (state.mode === '3d'){ resetCamera3D(); }
    else { state.zoom2D = 1; redraw(); }
  });
  frame.addEventListener('mousedown', e => { if (state.mode === '3d') _drag = { x: e.clientX, y: e.clientY }; });
  window.addEventListener('mousemove', e => {
    if (!_drag) return;
    const dx = e.clientX - _drag.x, dy = e.clientY - _drag.y;
    _drag.x = e.clientX; _drag.y = e.clientY;
    theta3D += dx * 0.005;
    phi3D   -= dy * 0.005;
    phi3D = Math.max(0.05, Math.min(Math.PI - 0.05, phi3D));
    // Rotation only — never re-fit during a drag. User zoom (wheel /
    // pinch) must persist; double-click resets the camera explicitly.
    updateCamera3D();
  });
  window.addEventListener('mouseup',   () => { _drag = null; });
  window.addEventListener('mouseleave',() => { _drag = null; });
  frame.addEventListener('touchstart', e => {
    if (state.mode !== '3d') return;
    if (e.touches.length === 1) _drag = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  }, { passive: true });
  frame.addEventListener('touchmove', e => {
    if (!_drag || e.touches.length !== 1) return;
    const dx = e.touches[0].clientX - _drag.x, dy = e.touches[0].clientY - _drag.y;
    _drag.x = e.touches[0].clientX; _drag.y = e.touches[0].clientY;
    theta3D += dx * 0.005;
    phi3D   -= dy * 0.005;
    phi3D = Math.max(0.05, Math.min(Math.PI - 0.05, phi3D));
    // Rotation only — preserves user zoom across drags.
    updateCamera3D();
  }, { passive: true });
  frame.addEventListener('touchend',  () => { _drag = null; });
  frame.addEventListener('touchcancel',() => { _drag = null; });
}

function setupPinch(){
  const frame = dom.canvasFrame;
  if (!frame) return;
  let pinchStartDist = 0, pinchStart3D = 70, pinchStart2DZoom = 1;
  let pinchPrevMid = { x:0, y:0 };
  let isPinching = false;
  const dist = (a, b) => Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);
  const mid  = (a, b) => ({ x:(a.clientX + b.clientX)/2, y:(a.clientY + b.clientY)/2 });
  frame.addEventListener('touchstart', e => {
    if (e.touches.length === 2){
      isPinching = true;
      pinchStartDist = dist(e.touches[0], e.touches[1]);
      pinchStart3D = distance3D;
      pinchStart2DZoom = state.zoom2D || 1;
      pinchPrevMid = mid(e.touches[0], e.touches[1]);
      _drag = null;
      e.preventDefault();
    }
  }, { passive: false });
  frame.addEventListener('touchmove', e => {
    if (!isPinching || e.touches.length !== 2) return;
    e.preventDefault();
    const d = dist(e.touches[0], e.touches[1]);
    if (pinchStartDist <= 0) return;
    const ratio = d / pinchStartDist;
    const m = mid(e.touches[0], e.touches[1]);
    const dx = m.x - pinchPrevMid.x, dy = m.y - pinchPrevMid.y;
    pinchPrevMid = m;
    if (state.mode === '3d'){
      let nd = pinchStart3D / ratio;
      nd = Math.max(20, Math.min(400, nd));
      distance3D = nd;
      theta3D += dx * 0.005;
      phi3D   -= dy * 0.005;
      phi3D = Math.max(0.05, Math.min(Math.PI - 0.05, phi3D));
      updateCamera3D();
    } else {
      let nz = pinchStart2DZoom * ratio;
      nz = Math.max(0.5, Math.min(8, nz));
      state.zoom2D = nz;
      redraw();
    }
  }, { passive: false });
  const endPinch = e => { if (e.touches.length < 2){ isPinching = false; pinchStartDist = 0; } };
  frame.addEventListener('touchend', endPinch);
  frame.addEventListener('touchcancel', endPinch);
}

function setupKeyboard(){
  document.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    const k = e.key.toLowerCase();
    // Undo / Redo. Three redo bindings so muscle memory from any host
    // app works: Ctrl+Y (Word, Excel, most Windows apps), Ctrl+Shift+Z
    // (Photoshop / web editors), Ctrl+Alt+Z (some Linux DEs / IDEs).
    // Plain Ctrl+Z is always undo.
    if ((e.ctrlKey || e.metaKey) && (k === 'z' || k === 'y')){
      e.preventDefault();
      const wantRedo = (k === 'y') || (k === 'z' && (e.shiftKey || e.altKey));
      const did = wantRedo ? redo() : undo();
      if (did) toast(wantRedo ? 'Redo' : 'Undo');
      return;
    }
    if (k === 'g'){ document.querySelector('[data-act=grid]')?.click(); }
    else if (k === 'c'){
      state.center = !state.center;
      document.querySelector('[data-act=center]')?.classList.toggle('active', state.center);
      const inp = document.querySelector('[data-pref=center]');
      if (inp) inp.checked = state.center;
      redraw();
    }
    else if (k === 'd'){ downloadPNG(); toast('PNG saved', 'ok'); }
    else if (k === 'i'){ document.querySelector('.info-chip')?.classList.toggle('open'); }
    else if (k === 'm'){
      state.mode = state.mode === '2d' ? '3d' : '2d';
      syncShape();
      if (state.mode === '3d'){ if (init3D(dom.canvas3D)){ resize3D(); autoZoom3D(); update3D(); } }
      else redraw();
      Sfx.pop();
    }
    else if (k === 's'){
      Sfx.setEnabled(!Sfx.isEnabled());
      const inp = document.querySelector('[data-pref=sound]');
      if (inp) inp.checked = Sfx.isEnabled();
      toast(`Sounds ${Sfx.isEnabled() ? 'on' : 'off'}`);
    }
    else if (k === 't'){
      document.querySelector('[data-act=theme]')?.click();
    }
    // Arrow keys walk the block picker. Disabled when the user is typing
    // (handled at the top of this listener) and when the picker doesn't
    // contain the current selection (e.g. brand-new session — falls back
    // to the first tile).
    else if (k === 'arrowleft' || k === 'arrowright'){
      const tiles = Array.from(document.querySelectorAll('.mc-block[data-block]'));
      if (!tiles.length) return;
      const cur = tiles.findIndex(t => t.dataset.block === state.mcBlock);
      const dir = (k === 'arrowright') ? 1 : -1;
      const next = (cur < 0 ? 0 : (cur + dir + tiles.length) % tiles.length);
      tiles[next].click();
      // Keep the active tile in view inside the horizontally-scrolling strip.
      tiles[next].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
      e.preventDefault();
    }
  });
}

function setupUI(){
  buildMCList();
  setupClickDelegation();
  setupSliders();
  setupPrefs();
  setup3DPointer();
  setupPinch();
  setupKeyboard();
  // Seed the undo stack with the initial state so the user can undo
  // all the way back to the moment they opened the page.
  pushHistory();
}
