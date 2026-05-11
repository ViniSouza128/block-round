/* =============================================================================
   Block Round — js/state.js
   All Rights Reserved on code. MC textures are Mojang property.

   Loaded AFTER js/textures.js so window.MC_TEX is available. The block
   catalog (MC_BLOCKS) pulls its `src` from MC_TEX[key] base64 data URIs,
   which sidesteps file:// CORS limits when the page is opened from disk.
   ============================================================================ */

let state = {
  route: 'tool',
  mode:  '2d',
  shape: 'circle',
  render: 'filled',
  algo:   'euclidean',
  size:  16, width: 20, height: 12, depth: 14,
  cut:   16, cutPct: 1.0, axis: 'y',
  edges3d: true,        // Grid btn in 3D toggles a black edge overlay on
                        // every voxel; default ON so the user can count
                        // blocks when copying into Minecraft.
  grid:    false,     // OFF by default — textures already give visual structure
  center:  false,
  overlay: false,
  zoomBtn: false,
  info:    false,
  zoom2D:  1,
  mcBlock: 'random',
};

/* Session-only — no persistence. App always starts at defaults. */
function loadPrefs(){ /* no-op */ }
function savePrefs(){ /* no-op */ }

/* Theme helpers — Block Round is single-theme but kept for API parity */
function getTheme(){ return 'minecraft'; }
function setTheme(){ /* no-op */ }

let dom = {};
function captureDom(){
  dom = {
    app:        document.querySelector('.app'),
    canvas2D:   document.getElementById('c2d'),
    canvas3D:   document.getElementById('c3d'),
    canvasFrame:document.querySelector('.canvas-frame'),
    toolGrid:   document.querySelector('.tool-grid'),
    infoChip:   document.querySelector('.info-chip'),
    toastHost:  document.querySelector('.toast-host'),
    mcList:     document.querySelector('.mc-list'),
  };
}

function setSliderPct(input){
  const min = +input.min || 0, max = +input.max || 64, v = +input.value;
  const pct = max === min ? 0 : ((v - min) / (max - min)) * 100;
  input.style.setProperty('--pct', pct + '%');
}

const SHAPE_LABELS = {
  circle:  { '2d':'Circle',  '3d':'Sphere' },
  ellipse: { '2d':'Ellipse', '3d':'Ellipsoid' },
};
const ALGO_FULL_NAME = {
  euclidean: 'Euclidean',
  bresenham: 'Bresenham',
  threshold: 'Threshold',
};

/* ---------- MC BLOCK CATALOG -------------------------------------------- */
/* Wide catalog drawing from window.MC_TEX (base64 data URIs from
   js/textures.js, which is loaded before this file). The `src` for each
   block is a data URI so loading works on file:// without CORS issues. */
function _tex(key){ return (window.MC_TEX && window.MC_TEX[key]) || null; }
const MC_BLOCKS = {
  random:        { src: null, name: 'Random' },

  // ===== TOP TIER ========================================================
  // Iconic / most-used Minecraft blocks. Picker shows these first so the
  // most useful options aren't buried under stone variants and ores.
  //
  //   • grass_block — real MC "Grass Block": grass_top on +Y, grass_side
  //     on the four sides, dirt on -Y. The renderer stamps this on the
  //     top voxel of each column and uses plain dirt below.
  //   • dirt        — plain dirt, no grass cap.
  //   • grass / grass_side / oak_log_top — internal-only face textures
  //     for multi-face materials; hidden from the picker.
  grass_block:   { src: _tex('grass_block_side'),  name: 'Grass Block' },
  dirt:          { src: _tex('dirt'),              name: 'Dirt' },
  stone:         { src: _tex('stone'),             name: 'Stone' },
  cobble:        { src: _tex('cobblestone'),       name: 'Cobblestone' },
  oak:           { src: _tex('oak_planks'),        name: 'Oak Planks' },
  oak_log:       { src: _tex('oak_log'),           name: 'Oak Log' },
  sand:          { src: _tex('sand'),              name: 'Sand' },
  gravel:        { src: _tex('gravel'),            name: 'Gravel' },
  glass:         { src: _tex('glass'),             name: 'Glass' },

  // ===== ORES =============================================================
  coal:          { src: _tex('coal_ore'),          name: 'Coal Ore' },
  iron_ore:      { src: _tex('iron_ore'),          name: 'Iron Ore' },
  gold_ore:      { src: _tex('gold_ore'),          name: 'Gold Ore' },
  redstone:      { src: _tex('redstone_ore'),      name: 'Redstone Ore' },
  lapis:         { src: _tex('lapis_ore'),         name: 'Lapis Ore' },
  diamond_ore:   { src: _tex('diamond_ore'),       name: 'Diamond Ore' },
  emerald_ore:   { src: _tex('emerald_ore'),       name: 'Emerald Ore' },

  // ===== REFINED METAL / GEM BLOCKS ======================================
  iron:          { src: _tex('iron_block'),        name: 'Iron Block' },
  gold:          { src: _tex('gold_block'),        name: 'Gold Block' },
  diamond:       { src: _tex('diamond_block'),     name: 'Diamond Block' },
  emerald:       { src: _tex('emerald_block'),     name: 'Emerald Block' },
  copper:        { src: _tex('copper_block'),      name: 'Copper Block' },

  // ===== STONE VARIANTS ===================================================
  granite:           { src: _tex('granite'),           name: 'Granite' },
  andesite:          { src: _tex('andesite'),          name: 'Andesite' },
  polished_andesite: { src: _tex('polished_andesite'), name: 'Polished Andesite' },
  diorite:           { src: _tex('diorite'),           name: 'Diorite' },
  smooth_stone:      { src: _tex('smooth_stone'),      name: 'Smooth Stone' },
  mossy_cobble:      { src: _tex('mossy_cobblestone'), name: 'Mossy Cobble' },
  deepslate:         { src: _tex('deepslate'),         name: 'Deepslate' },
  bedrock:           { src: _tex('bedrock'),           name: 'Bedrock' },

  // ===== EARTH / DESERT ===================================================
  soul_sand:     { src: _tex('soul_sand'),         name: 'Soul Sand' },
  sandstone:     { src: _tex('sandstone'),         name: 'Sandstone' },
  end_stone:     { src: _tex('end_stone'),         name: 'End Stone' },
  moss:          { src: _tex('moss_block'),        name: 'Moss' },

  // ===== WOOD VARIANTS ===================================================
  // Planks (single-texture, all 6 faces identical).
  darkOak:       { src: _tex('dark_oak_planks'),   name: 'Dark Oak' },
  birch:         { src: _tex('birch_planks'),      name: 'Birch' },
  spruce:        { src: _tex('spruce_planks'),     name: 'Spruce' },
  jungle:        { src: _tex('jungle_planks'),     name: 'Jungle' },
  acacia:        { src: _tex('acacia_planks'),     name: 'Acacia' },
  // Logs — bark on the four sides, end-grain on top and bottom. The
  // 3D renderer wires up the multi-face material in canvas3d.js
  // (getMaterial3D). The picker icon shows the bark texture.
  birch_log:    { src: _tex('log_birch'),         name: 'Birch Log'    },
  spruce_log:   { src: _tex('log_spruce'),        name: 'Spruce Log'   },
  jungle_log:   { src: _tex('log_jungle'),        name: 'Jungle Log'   },
  acacia_log:   { src: _tex('log_acacia'),        name: 'Acacia Log'   },
  dark_oak_log: { src: _tex('log_big_oak'),       name: 'Dark Oak Log' },

  // ===== LIGHT ============================================================
  glowstone:     { src: _tex('glowstone'),         name: 'Glowstone' },
  sea_lantern:   { src: _tex('sea_lantern'),       name: 'Sea Lantern' },
  magma:         { src: _tex('magma'),             name: 'Magma' },

  // ===== DECORATION =======================================================
  bricks:        { src: _tex('bricks'),            name: 'Bricks' },
  nether_bricks: { src: _tex('nether_bricks'),     name: 'Nether Bricks' },
  quartz:        { src: _tex('quartz_block_top'),  name: 'Quartz' },
  obsidian:      { src: _tex('obsidian'),          name: 'Obsidian' },
  ice:           { src: _tex('ice'),               name: 'Ice' },
  packed_ice:    { src: _tex('ice_packed'),        name: 'Packed Ice' },
  blue_ice:      { src: _tex('blue_ice'),          name: 'Blue Ice' },
  snow_block:    { src: _tex('snow'),              name: 'Snow Block' },
  netherrack:    { src: _tex('netherrack'),        name: 'Netherrack' },
  hay:           { src: _tex('hay_block_side'),    name: 'Hay' },
  pumpkin:       { src: _tex('pumpkin_top'),       name: 'Pumpkin' },
  melon:         { src: _tex('melon_side'),        name: 'Melon' },
  bone:          { src: _tex('bone_block_side'),   name: 'Bone' },

  // ===== CRAFTED / UTILITY ================================================
  // Three-face blocks: front, side, top distinct.
  crafting_table: { src: _tex('crafting_table_side'),    name: 'Crafting Table' },
  furnace:        { src: _tex('furnace_side'),           name: 'Furnace' },
  bookshelf:      { src: _tex('bookshelf'),              name: 'Bookshelf' },
  tnt:            { src: _tex('tnt_side'),               name: 'TNT' },

  // ===== EARTH VARIANTS ===================================================
  mycelium:       { src: _tex('mycelium_side'),          name: 'Mycelium' },
  podzol:         { src: _tex('dirt_podzol_side'),       name: 'Podzol' },

  // ===== PRISMARINE / NETHER ==============================================
  prismarine:        { src: _tex('prismarine_rough'),    name: 'Prismarine' },
  prismarine_bricks: { src: _tex('prismarine_bricks'),   name: 'Prismarine Bricks' },
  dark_prismarine:   { src: _tex('prismarine_dark'),     name: 'Dark Prismarine' },

  // ===== MUSHROOM CAPS ====================================================
  red_mushroom:   { src: _tex('mushroom_block_skin_red'),   name: 'Red Mushroom' },
  brown_mushroom: { src: _tex('mushroom_block_skin_brown'), name: 'Brown Mushroom' },

  // ===== WOOL =============================================================
  white_wool:     { src: _tex('white_wool'),       name: 'White Wool' },
  light_blue_wool:{ src: _tex('light_blue_wool'),  name: 'Light Blue Wool' },
  blue_wool:      { src: _tex('blue_wool'),        name: 'Blue Wool' },
  green_wool:     { src: _tex('green_wool'),       name: 'Green Wool' },
  yellow_wool:    { src: _tex('yellow_wool'),      name: 'Yellow Wool' },
  orange_wool:    { src: _tex('orange_wool'),      name: 'Orange Wool' },
  red_wool:       { src: _tex('red_wool'),         name: 'Red Wool' },
  black_wool:     { src: _tex('black_wool'),       name: 'Black Wool' },

  // ===== INTERNAL =========================================================
  // Face textures only — hidden from the picker, used by multi-face
  // materials in canvas3d.js (grass_block, oak_log).
  grass:        { src: _tex('grass_block_top'),  name: 'Grass Top',     internal: true },
  grass_side:   { src: _tex('grass_block_side'), name: 'Grass Side',    internal: true },
  oak_log_top:  { src: _tex('oak_log_top'),      name: 'Oak Log Top',   internal: true },
};
const RANDOM_POOL = ['grass','dirt','stone','cobble','oak','sand'];

/* ---------- IMAGE CACHE -------------------------------------------------- */
/* Lazily loads block textures from MC_TEX data URIs. Cached by key. */
const _imgCache = new Map();
function loadBlockImage(key){
  if (key === 'random') return null;
  if (_imgCache.has(key)) return _imgCache.get(key);
  const b = MC_BLOCKS[key];
  if (!b || !b.src) return null;
  const img = new Image();
  img.src = b.src;
  _imgCache.set(key, img);
  return img;
}
function imageReady(img){ return img && img.complete && img.naturalWidth > 0; }
function preloadAllBlockImages(){
  Object.keys(MC_BLOCKS).forEach(k => { if (k !== 'random') loadBlockImage(k); });
}
