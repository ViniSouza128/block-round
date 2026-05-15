/* =============================================================================
   Block Round — js/asset_toggle.js
   All Rights Reserved on code.

   Three-way toggle: original Minecraft textures (MC), CC0 free asset pack
   (FREE), and CC0 pixel-art pack (PIX).

   Depends on (loaded before this file):
     js/textures.js         → window.MC_TEX
     js/sounds.js           → window.MC_SFX
     js/textures_free.js    → window.FREE_TEX
     js/textures_pixelart.js → window.PIXELART_TEX
     js/sounds_free.js      → window.FREE_SFX
     js/state.js            → MC_BLOCKS, clearImgCache()
     js/canvas3d.js         → clearTexCache3D()
   ============================================================================ */

window.ASSET_PACK = 'mc';   // 'mc' | 'free' | 'pixelart'

/* Maps each MC_BLOCKS picker key to the primary MC_TEX key used for its
   background-image / 2D canvas source.  Must stay in sync with state.js. */
const _BLOCK_SRC_MAP = {
  grass_block:      'grass_block_side',
  dirt:             'dirt',
  stone:            'stone',
  cobble:           'cobblestone',
  oak:              'oak_planks',
  oak_log:          'oak_log',
  sand:             'sand',
  gravel:           'gravel',
  glass:            'glass',
  coal:             'coal_ore',
  iron_ore:         'iron_ore',
  gold_ore:         'gold_ore',
  redstone:         'redstone_ore',
  lapis:            'lapis_ore',
  diamond_ore:      'diamond_ore',
  emerald_ore:      'emerald_ore',
  iron:             'iron_block',
  gold:             'gold_block',
  diamond:          'diamond_block',
  emerald:          'emerald_block',
  copper:           'copper_block',
  granite:          'granite',
  andesite:         'andesite',
  polished_andesite:'polished_andesite',
  diorite:          'diorite',
  smooth_stone:     'smooth_stone',
  mossy_cobble:     'mossy_cobblestone',
  deepslate:        'deepslate',
  bedrock:          'bedrock',
  soul_sand:        'soul_sand',
  sandstone:        'sandstone',
  end_stone:        'end_stone',
  moss:             'moss_block',
  darkOak:          'dark_oak_planks',
  birch:            'birch_planks',
  spruce:           'spruce_planks',
  jungle:           'jungle_planks',
  acacia:           'acacia_planks',
  birch_log:        'log_birch',
  spruce_log:       'log_spruce',
  jungle_log:       'log_jungle',
  acacia_log:       'log_acacia',
  dark_oak_log:     'log_big_oak',
  glowstone:        'glowstone',
  sea_lantern:      'sea_lantern',
  magma:            'magma',
  bricks:           'bricks',
  nether_bricks:    'nether_bricks',
  quartz:           'quartz_block_top',
  obsidian:         'obsidian',
  ice:              'ice',
  packed_ice:       'ice_packed',
  blue_ice:         'blue_ice',
  snow_block:       'snow',
  netherrack:       'netherrack',
  hay:              'hay_block_side',
  pumpkin:          'pumpkin_top',
  melon:            'melon_side',
  bone:             'bone_block_side',
  crafting_table:   'crafting_table_top',
  furnace:          'furnace_front_off',
  bookshelf:        'bookshelf',
  tnt:              'tnt_side',
  mycelium:         'mycelium_side',
  podzol:           'dirt_podzol_side',
  prismarine:       'prismarine_rough',
  prismarine_bricks:'prismarine_bricks',
  dark_prismarine:  'prismarine_dark',
  red_mushroom:     'mushroom_block_skin_red',
  brown_mushroom:   'mushroom_block_skin_brown',
  slime:            'slime',
  honey:            'honey_top',
  sponge:           'sponge',
  shroomlight:      'shroomlight',
  crying_obsidian:  'crying_obsidian',
  white_wool:       'white_wool',
  light_blue_wool:  'light_blue_wool',
  blue_wool:        'blue_wool',
  green_wool:       'green_wool',
  yellow_wool:      'yellow_wool',
  orange_wool:      'orange_wool',
  red_wool:         'red_wool',
  black_wool:       'black_wool',
  // internal face textures
  grass:            'grass_block_top',
  grass_side:       'grass_block_side',
  oak_log_top:      'oak_log_top',
  oak_leaves:       'leaves_oak',
};

/* Snapshot of the original MC assets (taken once on first switch). */
let _mcTexOrig = null;
let _mcSfxOrig = null;

function _saveOriginals(){
  if (!_mcTexOrig) _mcTexOrig = Object.assign({}, window.MC_TEX);
  if (!_mcSfxOrig) _mcSfxOrig = Object.assign({}, window.MC_SFX);
}

/* style.css references `textures/<name>.png` directly for the UI background,
   panels, and buttons. Inject a high-specificity override stylesheet using
   the active pack's data URIs so the UI swaps along with block textures.

   NOTE: keys here name the *FREE* texture to pull (via MC_TEX[k] after the
   swap), NOT necessarily the same texture style.css uses for MC. The OGA
   `stone` is much noisier than Mojang's — yellow titles and cream body
   text bled into the speckled grey on the help/settings/info cards.
   We replace it with `iron_block` for the FREE pack only (a smooth light
   silvery fill) so legibility stays high. MC mode is untouched — it
   keeps the original style.css `textures/stone.png` background. */
const _UI_OVERRIDE_MAP = {
  dirt: [
    'body.asset-free',
  ],
  oak_planks: [
    'body.asset-free .topbar',
    'body.asset-free .icon-btn.active',
    'body.asset-free .c-btn.active',
    'body.asset-free .btn',
    'body.asset-free .toast',
  ],
  // Iron block (smooth, light) — replaces the speckled OGA stone for any
  // surface that hosts text. Buttons (icon-btn, c-btn) and panel cards
  // (info-chip, slider-box, cut-row, help-item, setting-row, pill-row).
  iron_block: [
    'body.asset-free .icon-btn',
    'body.asset-free .c-btn',
    'body.asset-free .info-chip',
    'body.asset-free .pill-row',
    'body.asset-free .slider-box',
    'body.asset-free .cut-row',
    'body.asset-free .help-item',
    'body.asset-free .setting-row',
  ],
  cobblestone: [
    'body.asset-free .mc-list',
    'body.asset-free .btn.ghost',
  ],
};
const _UI_STYLE_ID = 'asset-pack-ui-override';

function _applyUiOverride(pack){
  let el = document.getElementById(_UI_STYLE_ID);
  if (!el){
    el = document.createElement('style');
    el.id = _UI_STYLE_ID;
    document.head.appendChild(el);
  }
  // For pixelart pack, remap selectors to body.asset-pixelart
  const bodyClass = pack === 'pixelart' ? 'asset-pixelart' : 'asset-free';
  const lines = [];
  Object.entries(_UI_OVERRIDE_MAP).forEach(([texKey, sels]) => {
    const uri = (window.MC_TEX && window.MC_TEX[texKey]) || '';
    if (!uri) return;
    sels.forEach(sel => {
      const remapped = sel.replace('body.asset-free', `body.${bodyClass}`);
      lines.push(`${remapped} { background-image: url('${uri}') !important; }`);
    });
  });
  el.textContent = lines.join('\n');
}

function _removeUiOverride(){
  const el = document.getElementById(_UI_STYLE_ID);
  if (el) el.remove();
}

/* Overwrite MC_TEX in-place from the provided source dict.
   Keys absent in src stay as-is (so MC-only keys still render). */
function _applyTexPack(src){
  const keys = Object.keys(src);
  for (const k of keys) window.MC_TEX[k] = src[k];
}

/* Restore MC_TEX from snapshot for any key present in snapshot. */
function _restoreTexPack(snapshot){
  const keys = Object.keys(snapshot);
  for (const k of keys) window.MC_TEX[k] = snapshot[k];
}

/* Rebuild MC_BLOCKS[k].src and update picker tile background-images.
   NOTE: state.js declares MC_BLOCKS as `const`, which is *script-scope*
   (shared across all <script> tags) but NOT a window property. The
   previous `window.MC_BLOCKS` guard was always false so MC_BLOCKS[k].src
   never updated — leaving the 2D image cache and the 3D multi-face
   fallback (canvas3d.js's `MC_BLOCKS[key].src` path for `grass`,
   `grass_side`, `oak_log_top`, `oak_leaves`) frozen on Mojang data
   URIs even while window.MC_TEX got swapped. Reference MC_BLOCKS bare
   here so every picker key — including the internal-face aliases —
   gets its src rebuilt on every toggle. */
function _refreshPickerTiles(){
  const blocks = (typeof MC_BLOCKS !== 'undefined') ? MC_BLOCKS : null;
  Object.entries(_BLOCK_SRC_MAP).forEach(([blockKey, texKey]) => {
    const uri = (window.MC_TEX && window.MC_TEX[texKey]) || null;
    if (blocks && blocks[blockKey] && uri){
      blocks[blockKey].src = uri;
    }
    if (blockKey !== 'random' && uri){
      const tile = document.querySelector(`.mc-block[data-block="${blockKey}"]`);
      if (tile) tile.style.backgroundImage = `url('${uri}')`;
    }
  });
}

/* Performs the in-place swap of textures, sounds, picker tiles, caches,
   and triggers a re-render. Split out from switchAssetPack so we can
   wrap it in a smooth crossfade transition. */
function _doAssetSwap(pack){
  window.ASSET_PACK = pack;
  _saveOriginals();

  // Reflect the new active pack on the toggle button itself. Done here
  // (synchronous with window.ASSET_PACK) so the label inside the View
  // Transition's "after" snapshot already shows the correct active pack
  // — i.e. when FREE is active, the button reads "FREE", when MC is
  // active, it reads "MC". Previously this was set in onAssetPackToggle
  // AFTER the async swap fired, which meant the label could lag by one
  // click in the VT capture.
  document.querySelectorAll('[data-act="asset-pack"]').forEach(btn => {
    btn.classList.toggle('asset-free',     pack === 'free');
    btn.classList.toggle('asset-pixelart', pack === 'pixelart');
    const titles = {
      mc:       'Switch to Free CC0 assets (test)',
      free:     'Switch to Pixel-Art CC0 assets (test)',
      pixelart: 'Switch to MC assets (Mojang)',
    };
    btn.title = titles[pack] || titles.mc;
    btn.setAttribute('aria-pressed', String(pack !== 'mc'));
  });

  if (pack === 'free'){
    _applyTexPack(window.FREE_TEX || {});
    const freeSfx = window.FREE_SFX || {};
    Object.keys(freeSfx).forEach(k => { window.MC_SFX[k] = freeSfx[k]; });
    document.body.classList.add('asset-free');
    document.body.classList.remove('asset-pixelart');
    _applyUiOverride('free');
  } else if (pack === 'pixelart'){
    _applyTexPack(window.PIXELART_TEX || {});
    const freeSfx = window.FREE_SFX || {};
    Object.keys(freeSfx).forEach(k => { window.MC_SFX[k] = freeSfx[k]; });
    document.body.classList.remove('asset-free');
    document.body.classList.add('asset-pixelart');
    _applyUiOverride('pixelart');
  } else {
    _restoreTexPack(_mcTexOrig);
    Object.keys(_mcSfxOrig).forEach(k => { window.MC_SFX[k] = _mcSfxOrig[k]; });
    document.body.classList.remove('asset-free');
    document.body.classList.remove('asset-pixelart');
    _removeUiOverride();
  }

  // Clear 3-D texture / material cache so Three.js re-loads from new URIs
  if (typeof clearTexCache3D === 'function') clearTexCache3D();
  // Clear 2-D image cache
  if (typeof clearImgCache === 'function') clearImgCache();
  // Rebuild MC_BLOCKS.src + picker backgrounds
  _refreshPickerTiles();
  // Reload all block images for 2D canvas
  if (typeof preloadAllBlockImages === 'function') preloadAllBlockImages();
  // Re-render whichever canvas is active
  if (state.mode === '3d'){
    if (typeof update3D === 'function') update3D();
  } else {
    if (typeof redraw === 'function') redraw();
  }
}

/* Smooth crossfade transition. Two strategies in priority order:
   1. Native View Transitions API (Chrome 111+) — auto-captures the page
      snapshot, runs our swap callback, crossfades old → new at 220 ms.
      Best result; works on background, panels, picker, AND canvas.
   2. Fallback: overlay a fixed snapshot div that holds the body's current
      background CSS, fade it out while the swap happens underneath. The
      <canvas> snapshot isn't captured (would need html-to-image lib), so
      the canvas itself updates instantly — but the UI shell (background,
      topbar, panels, buttons) gets a clean crossfade. */
const _ASSET_SWAP_DURATION = 240;  // ms — fast but not abrupt
function _withCrossfade(swapFn){
  // Path 1: native View Transitions
  if (document.startViewTransition){
    document.documentElement.style.setProperty('--asset-vt-dur', _ASSET_SWAP_DURATION + 'ms');
    const t = document.startViewTransition(() => swapFn());
    // Clean up the custom property after the transition completes
    t.finished.finally(() => {
      document.documentElement.style.removeProperty('--asset-vt-dur');
    });
    return;
  }
  // Path 2: snapshot-overlay fallback
  const overlay = document.createElement('div');
  overlay.id = 'asset-pack-fade-overlay';
  // Mirror the entire viewport so the overlay reads as the current frame.
  // We capture every property that contributes to the body's painted look
  // (background-image + the dirt fill colour behind it).
  const body = document.body;
  const cs = getComputedStyle(body);
  Object.assign(overlay.style, {
    position: 'fixed', inset: '0', zIndex: '9999', pointerEvents: 'none',
    background: cs.background,
    backgroundColor: cs.backgroundColor,
    backgroundImage: cs.backgroundImage,
    backgroundSize: cs.backgroundSize,
    backgroundPosition: cs.backgroundPosition,
    backgroundRepeat: cs.backgroundRepeat,
    opacity: '1',
    transition: `opacity ${_ASSET_SWAP_DURATION}ms ease`,
    imageRendering: 'pixelated',
  });
  document.body.appendChild(overlay);
  // Force a layout flush so the overlay paints at opacity 1 BEFORE we swap.
  void overlay.offsetWidth;
  // Now do the swap behind the overlay
  swapFn();
  // Next frame, start the fade-out
  requestAnimationFrame(() => {
    overlay.style.opacity = '0';
    setTimeout(() => overlay.remove(), _ASSET_SWAP_DURATION + 40);
  });
}

/* Main switch function — called by the toggle button. */
function switchAssetPack(pack){
  if (pack === window.ASSET_PACK) return;
  _withCrossfade(() => _doAssetSwap(pack));
}

/* Toggle button click handler — wired by index.html data-act="asset-pack".
   Just kicks the swap; the button label / aria-pressed state is updated
   inside _doAssetSwap so it stays in lock-step with window.ASSET_PACK
   (and gets captured correctly by the View Transition snapshot). */
function onAssetPackToggle(){
  const cycle = { mc: 'free', free: 'pixelart', pixelart: 'mc' };
  switchAssetPack(cycle[window.ASSET_PACK] || 'free');
}
