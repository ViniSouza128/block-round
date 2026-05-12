/* =============================================================================
   Block Round — js/asset_toggle.js
   All Rights Reserved on code.

   Temporary A/B test toggle: switches between the original Minecraft textures
   (MC pack — Mojang property) and the CC0 free asset pack (OGA textures +
   Kenney sounds + procedural fills).

   Depends on (loaded before this file):
     js/textures.js    → window.MC_TEX
     js/sounds.js      → window.MC_SFX
     js/textures_free.js → window.FREE_TEX
     js/sounds_free.js   → window.FREE_SFX
     js/state.js       → MC_BLOCKS, clearImgCache()
     js/canvas3d.js    → clearTexCache3D()
   ============================================================================ */

window.ASSET_PACK = 'mc';   // 'mc' | 'free'

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

/* Rebuild MC_BLOCKS[k].src and update picker tile background-images. */
function _refreshPickerTiles(){
  Object.entries(_BLOCK_SRC_MAP).forEach(([blockKey, texKey]) => {
    const uri = (window.MC_TEX && window.MC_TEX[texKey]) || null;
    if (window.MC_BLOCKS && window.MC_BLOCKS[blockKey]){
      window.MC_BLOCKS[blockKey].src = uri;
    }
    if (blockKey !== 'random' && uri){
      const tile = document.querySelector(`.mc-block[data-block="${blockKey}"]`);
      if (tile) tile.style.backgroundImage = `url('${uri}')`;
    }
  });
}

/* Main switch function — called by the toggle button. */
function switchAssetPack(pack){
  if (pack === window.ASSET_PACK) return;
  window.ASSET_PACK = pack;

  _saveOriginals();

  if (pack === 'free'){
    _applyTexPack(window.FREE_TEX || {});
    // Overwrite MC_SFX place keys with Kenney sounds
    const freeSfx = window.FREE_SFX || {};
    Object.keys(freeSfx).forEach(k => { window.MC_SFX[k] = freeSfx[k]; });
  } else {
    _restoreTexPack(_mcTexOrig);
    Object.keys(_mcSfxOrig).forEach(k => { window.MC_SFX[k] = _mcSfxOrig[k]; });
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

/* Toggle button click handler — wired by index.html data-act="asset-pack" */
function onAssetPackToggle(){
  const next = window.ASSET_PACK === 'mc' ? 'free' : 'mc';
  switchAssetPack(next);

  // Update button label / aria
  document.querySelectorAll('[data-act="asset-pack"]').forEach(btn => {
    const isFree = window.ASSET_PACK === 'free';
    btn.classList.toggle('asset-free', isFree);
    btn.title       = isFree ? 'Switch to MC assets (Mojang)' : 'Switch to Free CC0 assets (test)';
    btn.setAttribute('aria-pressed', String(isFree));
  });
}
