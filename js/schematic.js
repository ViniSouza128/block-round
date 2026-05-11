/* =============================================================================
   Block Round — js/schematic.js
   All Rights Reserved on code. MC textures + block names are Mojang property.

   Sponge Schematic v2 (.schem) writer. Generates a gzipped NBT file
   matching the spec at:
     https://github.com/SpongePowered/Schematic-Specification/blob/master/versions/schematic-2.md

   Pipeline:
     1. Walk every voxel of the current Block Round figure (respecting
        render mode + cut + per-voxel block pick).
     2. Build a palette (block state string → small integer index).
     3. Serialise the 3D voxel grid as a flat array of VarInts referencing
        the palette.
     4. Wrap in NBT.
     5. GZIP-compress via the browser-native CompressionStream('gzip').
     6. Trigger a download as block-round-<dims>-<block>-<render>.schem.

   The resulting file imports cleanly into WorldEdit (//schem load),
   Litematica (Schematic Manager -> load) and MCEdit Unified.

   No external libs — NBT writer is implemented from scratch (~120 lines).
   ============================================================================ */

/* ---------- BLOCK NAME → MC BLOCK STATE ----------------------------------
   Maps Block Round's internal keys to the full namespaced MC block-state
   strings the Sponge schematic palette expects. Anything not mapped here
   falls back to "minecraft:stone" so the file is still valid even for
   exotic / placeholder picks. */
const SCHEM_BLOCK_STATES = {
  // Earth
  grass_block:    'minecraft:grass_block[snowy=false]',
  dirt:           'minecraft:dirt',
  mycelium:       'minecraft:mycelium[snowy=false]',
  podzol:         'minecraft:podzol[snowy=false]',
  moss:           'minecraft:moss_block',
  // Stone family
  stone:          'minecraft:stone',
  cobble:         'minecraft:cobblestone',
  mossy_cobble:   'minecraft:mossy_cobblestone',
  smooth_stone:   'minecraft:smooth_stone',
  granite:        'minecraft:granite',
  andesite:       'minecraft:andesite',
  polished_andesite: 'minecraft:polished_andesite',
  diorite:        'minecraft:diorite',
  deepslate:      'minecraft:deepslate[axis=y]',
  bedrock:        'minecraft:bedrock',
  sandstone:      'minecraft:sandstone',
  end_stone:      'minecraft:end_stone',
  bricks:         'minecraft:bricks',
  nether_bricks:  'minecraft:nether_bricks',
  netherrack:     'minecraft:netherrack',
  prismarine:     'minecraft:prismarine',
  prismarine_bricks: 'minecraft:prismarine_bricks',
  dark_prismarine:'minecraft:dark_prismarine',
  obsidian:       'minecraft:obsidian',
  crying_obsidian:'minecraft:crying_obsidian',
  quartz:         'minecraft:quartz_block',
  magma:          'minecraft:magma_block',
  glowstone:      'minecraft:glowstone',
  sea_lantern:    'minecraft:sea_lantern',
  shroomlight:    'minecraft:shroomlight',
  bone:           'minecraft:bone_block[axis=y]',
  // Ores
  coal:           'minecraft:coal_ore',
  iron_ore:       'minecraft:iron_ore',
  gold_ore:       'minecraft:gold_ore',
  diamond_ore:    'minecraft:diamond_ore',
  emerald_ore:    'minecraft:emerald_ore',
  redstone:       'minecraft:redstone_ore[lit=false]',
  lapis:          'minecraft:lapis_ore',
  // Refined metal/gem blocks
  iron:           'minecraft:iron_block',
  gold:           'minecraft:gold_block',
  diamond:        'minecraft:diamond_block',
  emerald:        'minecraft:emerald_block',
  copper:         'minecraft:copper_block',
  // Wood — planks
  oak:            'minecraft:oak_planks',
  darkOak:        'minecraft:dark_oak_planks',
  birch:          'minecraft:birch_planks',
  spruce:         'minecraft:spruce_planks',
  jungle:         'minecraft:jungle_planks',
  acacia:         'minecraft:acacia_planks',
  // Wood — logs (default y-axis = standing upright)
  oak_log:        'minecraft:oak_log[axis=y]',
  birch_log:      'minecraft:birch_log[axis=y]',
  spruce_log:     'minecraft:spruce_log[axis=y]',
  jungle_log:     'minecraft:jungle_log[axis=y]',
  acacia_log:     'minecraft:acacia_log[axis=y]',
  dark_oak_log:   'minecraft:dark_oak_log[axis=y]',
  // Crafted / utility
  crafting_table: 'minecraft:crafting_table',
  furnace:        'minecraft:furnace[facing=north,lit=false]',
  bookshelf:      'minecraft:bookshelf',
  tnt:            'minecraft:tnt[unstable=false]',
  // Desert / soul
  sand:           'minecraft:sand',
  gravel:         'minecraft:gravel',
  soul_sand:      'minecraft:soul_sand',
  hay:            'minecraft:hay_block[axis=y]',
  // Glass / ice / snow
  glass:          'minecraft:glass',
  ice:            'minecraft:ice',
  packed_ice:     'minecraft:packed_ice',
  blue_ice:       'minecraft:blue_ice',
  snow_block:     'minecraft:snow_block',
  // Mushroom / sponge / honey / slime
  pumpkin:        'minecraft:pumpkin',
  melon:          'minecraft:melon',
  red_mushroom:   'minecraft:red_mushroom_block[down=false,east=false,north=false,south=false,up=true,west=false]',
  brown_mushroom: 'minecraft:brown_mushroom_block[down=false,east=false,north=false,south=false,up=true,west=false]',
  sponge:         'minecraft:sponge',
  slime:          'minecraft:slime_block',
  honey:          'minecraft:honey_block',
  // Wool
  white_wool:     'minecraft:white_wool',
  black_wool:     'minecraft:black_wool',
  red_wool:       'minecraft:red_wool',
  green_wool:     'minecraft:green_wool',
  blue_wool:      'minecraft:blue_wool',
  yellow_wool:    'minecraft:yellow_wool',
  orange_wool:    'minecraft:orange_wool',
  light_blue_wool:'minecraft:light_blue_wool',
};

function _schemBlockState(key){
  return SCHEM_BLOCK_STATES[key] || 'minecraft:stone';
}

/* ---------- VARINT ENCODING ----------------------------------------------
   Sponge schematic block data is a packed byte array of unsigned VarInts
   (7 bits per byte, MSB = "more bytes follow"). Same encoding used by
   Minecraft's network protocol. */
function _writeVarInt(out, n){
  n = n >>> 0;
  while ((n & ~0x7F) !== 0){
    out.push((n & 0x7F) | 0x80);
    n >>>= 7;
  }
  out.push(n & 0x7F);
}

/* ---------- NBT WRITER ---------------------------------------------------
   Tiny Notch NBT writer. Supports the tag types this schematic needs:
   Byte, Short, Int, String, ByteArray, IntArray, List, Compound. Numbers
   are written big-endian per the NBT spec. */
function _utf8(s){
  return new TextEncoder().encode(s);
}
class _NBTWriter {
  constructor(){ this.bytes = []; }
  byte(v){ this.bytes.push(v & 0xFF); }
  short(v){ this.bytes.push((v >> 8) & 0xFF, v & 0xFF); }
  int(v){
    this.bytes.push((v >>> 24) & 0xFF, (v >>> 16) & 0xFF, (v >>> 8) & 0xFF, v & 0xFF);
  }
  string(s){
    const u = _utf8(s);
    this.short(u.length);
    for (const b of u) this.bytes.push(b);
  }
  byteArrayPayload(arr){
    this.int(arr.length);
    for (const b of arr) this.bytes.push(b & 0xFF);
  }
  intArrayPayload(arr){
    this.int(arr.length);
    for (const v of arr) this.int(v);
  }
  // Named tag wrappers (top-level tags inside a compound).
  tagByte(name, v){ this.byte(1); this.string(name); this.byte(v); }
  tagShort(name, v){ this.byte(2); this.string(name); this.short(v); }
  tagInt(name, v){ this.byte(3); this.string(name); this.int(v); }
  tagString(name, v){ this.byte(8); this.string(name); this.string(v); }
  tagByteArray(name, arr){ this.byte(7); this.string(name); this.byteArrayPayload(arr); }
  tagIntArray(name, arr){ this.byte(11); this.string(name); this.intArrayPayload(arr); }
  /* Compound: caller passes a function that emits tagged children. */
  tagCompound(name, fn){
    this.byte(10); this.string(name);
    fn(this);
    this.byte(0); // TAG_End closes the compound
  }
  /* List of compounds — used for the empty BlockEntities list. */
  tagListEmpty(name, elementType){
    this.byte(9); this.string(name);
    this.byte(elementType);
    this.int(0);
  }
  toUint8Array(){ return new Uint8Array(this.bytes); }
}

/* ---------- GZIP --------------------------------------------------------- */
async function _gzip(data){
  const cs = new CompressionStream('gzip');
  const writer = cs.writable.getWriter();
  writer.write(data);
  writer.close();
  const reader = cs.readable.getReader();
  const chunks = [];
  while (true){
    const { value, done } = await reader.read();
    if (done) break;
    chunks.push(value);
  }
  const total = chunks.reduce((s, c) => s + c.length, 0);
  const out = new Uint8Array(total);
  let off = 0;
  for (const c of chunks){ out.set(c, off); off += c.length; }
  return out;
}

/* ---------- SCHEM BUILDER ------------------------------------------------
   buildSpongeSchematic returns the gzipped .schem bytes for the current
   figure (state.size / shape / render / cut / mcBlock all read from
   global state). The voxel set comes straight from voxelShell with the
   block-key picking logic shared with the live renderer. */
function buildSpongeSchematic(){
  const isEllipse = state.shape === 'ellipse';
  const Dx = isEllipse ? state.width  : state.size;
  const Dy = isEllipse ? state.height : state.size;
  const Dz = isEllipse ? state.depth  : state.size;
  if (Dx <= 0 || Dy <= 0 || Dz <= 0) return null;

  const maxAxis = state.axis === 'x'    ? Dx
                : state.axis === 'y'    ? Dy
                : /* 'diag' */            (Dx + Dy);
  const cutLimit = state.cut < maxAxis ? state.cut : maxAxis + 1;

  // Use the same voxel pipeline the renderer uses, so what you see is
  // what you export. Transparent + filled goes through voxelKeptAll to
  // preserve the dense interior.
  const isTransparentFilled =
    state.render === 'filled' && (state.mcBlock === 'glass' || state.mcBlock === 'ice'
                                  || state.mcBlock === 'slime' || state.mcBlock === 'honey');
  const voxels = isTransparentFilled
    ? voxelKeptAll(Dx, Dy, Dz, state.axis, cutLimit)
    : voxelShell(Dx, Dy, Dz, state.render, state.axis, cutLimit);
  if (!voxels.length) return null;

  // Per-(x,z) column extremes for the random-pattern grass cap.
  const ext = (typeof computeVoxelColumnExtremes === 'function')
    ? computeVoxelColumnExtremes(voxels, Dx, Dz)
    : null;

  // Build a 3D grid initialised to "minecraft:air" so empty cells are
  // properly encoded. Sponge format = flat array indexed by
  //   index = (y * Length + z) * Width + x  (Y-Z-X traversal)
  const W = Dx, H = Dy, L = Dz;
  const total = W * H * L;
  const palette = new Map();
  let nextPaletteIdx = 0;
  function paletteAdd(name){
    let idx = palette.get(name);
    if (idx === undefined){ idx = nextPaletteIdx++; palette.set(name, idx); }
    return idx;
  }
  const airIdx = paletteAdd('minecraft:air');
  const cells = new Uint32Array(total).fill(airIdx);

  for (const v of voxels){
    const blockKey = (typeof pickBlockForVoxel === 'function')
      ? pickBlockForVoxel(v, ext, Dz)
      : state.mcBlock;
    const bs = _schemBlockState(blockKey);
    const idx = paletteAdd(bs);
    const arrayIdx = (v.y * L + v.z) * W + v.x;
    cells[arrayIdx] = idx;
  }

  // BlockData = VarInt-encoded flat list, one VarInt per cell.
  const blockData = [];
  for (let i = 0; i < total; i++) _writeVarInt(blockData, cells[i]);

  // Build the NBT tree. Root is an UNNAMED compound named "Schematic"
  // (older WorldEdit), or top-level name "" with a single "Schematic"
  // child. We use the simpler convention: outer compound named "".
  const w = new _NBTWriter();
  w.tagCompound('Schematic', s => {
    s.tagInt('Version', 2);
    s.tagInt('DataVersion', 3120);          // 1.19.3 — broad reader compat
    s.tagShort('Width',  W);
    s.tagShort('Height', H);
    s.tagShort('Length', L);
    s.tagIntArray('Offset', [0, 0, 0]);
    s.tagInt('PaletteMax', nextPaletteIdx);
    s.tagCompound('Palette', p => {
      for (const [name, idx] of palette){
        p.tagInt(name, idx);
      }
    });
    s.tagByteArray('BlockData', blockData);
    s.tagListEmpty('BlockEntities', 10 /* TAG_Compound */);
    s.tagCompound('Metadata', m => {
      m.tagString('Name', 'Block Round figure');
      m.tagString('Author', 'block-round');
    });
  });

  return _gzip(w.toUint8Array());
}

/* ---------- DOWNLOAD TRIGGER ---------------------------------------------
   Public entry point — called by the canvas-corner "schem" button. Builds
   the file in memory and triggers a browser download. */
async function downloadSchematic(){
  try {
    const bytes = await buildSpongeSchematic();
    if (!bytes){
      if (typeof toast === 'function') toast('Empty figure — nothing to export', 'error');
      return;
    }
    const blob = new Blob([bytes], { type: 'application/octet-stream' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const isEllipse = state.shape === 'ellipse';
    const name = isEllipse
      ? `block-round-ellipsoid-${state.width}x${state.height}x${state.depth}-${state.mcBlock}-${state.render}.schem`
      : `block-round-sphere-d${state.size}-${state.mcBlock}-${state.render}.schem`;
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    if (typeof toast === 'function') toast('.schem saved', 'ok');
  } catch (err){
    console.error('Schematic export failed:', err);
    if (typeof toast === 'function') toast('Export failed — see console', 'error');
  }
}
