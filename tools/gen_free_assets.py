"""Generate js/textures_free.js and js/sounds_free.js from CC0 assets.

Textures:  OpenGameArt CC0 block set  (_tmp_oga_blocks/blocks/)
Sounds:    Kenney Impact Sounds CC0   (_tmp_kenney_sounds/Audio/)

Run from project root:
    python tools/gen_free_assets.py
"""

from __future__ import annotations
import base64
import io
import json
import pathlib
from PIL import Image

ROOT   = pathlib.Path(__file__).resolve().parent.parent
OGA    = ROOT / '_tmp_oga_blocks'  / 'blocks'
KENNY  = ROOT / '_tmp_kenney_sounds' / 'Audio'
OUT_TX = ROOT / 'js' / 'textures_free.js'
OUT_SX = ROOT / 'js' / 'sounds_free.js'

# ── helpers ───────────────────────────────────────────────────────────────────

def png_b64(path: pathlib.Path) -> str:
    """Return a data:image/png;base64,… URI from a PNG file."""
    img = Image.open(path).convert('RGBA')
    buf = io.BytesIO()
    img.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

def ogg_b64(path: pathlib.Path) -> str:
    return 'data:audio/ogg;base64,' + base64.b64encode(path.read_bytes()).decode()

def oga(name: str) -> str:
    """base64 URI for an OGA texture by filename stem."""
    return png_b64(OGA / (name + '.png'))

# ── OGA → MC_TEX key mappings ─────────────────────────────────────────────────
# Each entry: OGA_stem → list of MC_TEX keys it covers.

OGA_MAP: dict[str, list[str]] = {
    'stone_generic':       ['stone', 'smooth_stone', 'polished_andesite'],
    'cobblestone':         ['cobblestone'],
    'cobblestone_mossy':   ['mossy_cobblestone'],
    'dirt':                ['dirt'],
    'grass_top':           ['grass_block_top'],
    'grass_side':          ['grass_block_side'],
    'gravel':              ['gravel'],
    'sand_ugly_2':         ['sand'],
    'sandstone':           ['sandstone', 'sandstone_bottom'],
    'sandstone_carved':    ['sandstone_top', 'red_sandstone_top'],
    'glass':               ['glass'],
    'obsidian':            ['obsidian'],
    'oak_planks':          ['oak_planks'],
    'oak_log_side':        ['oak_log'],
    'oak_log_top':         ['oak_log_top'],
    'diorite':             ['diorite', 'andesite'],
    'marble':              ['quartz_block_top', 'quartz_block_bottom', 'ice_packed'],
    'marble_bricks2':      ['quartz_block_side'],
    'granite':             ['granite'],
    'snow':                ['snow'],
    'ice_glacier':         ['ice', 'blue_ice'],
    'hay_side':            ['hay_block_side'],
    'hay_top':             ['hay_block_top'],
    'beech_planks':        ['birch_planks'],
    'maple_planks':        ['spruce_planks', 'jungle_planks'],
    'pine_planks':         ['dark_oak_planks'],
    'eucalyptus_planks':   ['acacia_planks'],
    'beech_log_side':      ['log_birch', 'birch_log'],
    'pine_log_side':       ['log_spruce', 'log_big_oak', 'dark_oak_log', 'spruce_log'],
    'eucalyptus_log_side': ['log_acacia', 'log_jungle'],
    'beech_log_top':       ['log_birch_top', 'log_spruce_top',
                            'log_acacia_top', 'log_big_oak_top', 'log_jungle_top'],
    'oak_leaves':          ['leaves_oak'],
    'maple_leaves':        ['leaves_oak'],      # fallback if needed
    'slate':               ['deepslate'],
    'gabbro':              ['bedrock'],
    'rhyolite':            ['netherrack'],
    'mud':                 ['soul_sand'],
    'limestone':           ['end_stone'],
    'limestone_bricks':    ['bricks'],
    'granite_bricks':      ['nether_bricks'],
    'serpentine':          ['moss_block'],
    'amethyst':            ['crying_obsidian'],
    'mud_bricks':          ['bone_block_side', 'bone_block_top'],
    'diorite_dirty':       ['mycelium_side', 'mycelium_top'],
    'farmland':            ['dirt_podzol_side', 'dirt_podzol_top'],
    'schist':              ['deepslate_diamond_ore', 'deepslate_emerald_ore',
                            'deepslate_gold_ore', 'deepslate_iron_ore'],
    'basalt':              ['prismarine_dark'],
    'coral_block_brain':   ['prismarine_bricks'],
    'coral_block_pore':    ['prismarine_rough'],
    'mushroom_block_skin_red':   ['mushroom_block_skin_red'],   # will be proc
    'mushroom_block_skin_brown': ['mushroom_block_skin_brown'], # will be proc
}

# Pre-collect: OGA filename → URI (compute once)
_oga_cache: dict[str, str] = {}
def _oga(name: str) -> str | None:
    if name not in _oga_cache:
        p = OGA / (name + '.png')
        if not p.exists():
            return None
        _oga_cache[name] = png_b64(p)
    return _oga_cache[name]

# Build forward map: mc_key → URI
mc_tex_from_oga: dict[str, str] = {}
for oga_stem, mc_keys in OGA_MAP.items():
    uri = _oga(oga_stem)
    if uri:
        for k in mc_keys:
            if k not in mc_tex_from_oga:   # first mapping wins
                mc_tex_from_oga[k] = uri

# Mushroom caps: procedural (OGA doesn't have them)
# They'll be handled by JS procedural below.
mc_tex_from_oga.pop('mushroom_block_skin_red',   None)
mc_tex_from_oga.pop('mushroom_block_skin_brown', None)

# ── Kenney sound mappings ─────────────────────────────────────────────────────
SOUND_MAP: dict[str, str] = {
    'place_stone':  'impactMining_000',
    'place_wood':   'footstep_wood_000',
    'place_grass':  'footstep_grass_000',
    'place_gravel': 'impactGeneric_light_000',
    'place_sand':   'impactSoft_medium_000',
    'place_snow':   'footstep_snow_000',
    'place_cloth':  'footstep_carpet_000',
    'place_glass':  'impactGlass_medium_000',
    # tnt_fuse and slime_jump are synthesized in audio.js — not embedded here.
}

# ── Build sounds dict ─────────────────────────────────────────────────────────
sounds: dict[str, str] = {}
for key, fname in SOUND_MAP.items():
    p = KENNY / (fname + '.ogg')
    if p.exists():
        sounds[key] = ogg_b64(p)
    else:
        print(f'WARNING: missing Kenney sound {p}')

# ── JS helpers (procedural texture generators) ────────────────────────────────
# Written as JS source strings; emitted verbatim into textures_free.js.
PROC_JS = r"""
  /* ── procedural texture helpers ── */
  function _c16(fn){
    const c=document.createElement('canvas'); c.width=c.height=16;
    fn(c.getContext('2d'),c); return c.toDataURL('image/png');
  }

  /* Deterministic per-pixel hash (same family as gravel in textures.js) */
  function _h(x,y){ let h=(x*374761393+y*668265263)|0; h=((h^(h>>>13))*1274126177)|0; return((h^(h>>>16))>>>0)/0x100000000; }

  /* Solid fill with subtle noise */
  function _solid(r,g,b,noise=12){
    return _c16((ctx)=>{
      const img=ctx.createImageData(16,16);
      for(let y=0;y<16;y++) for(let x=0;x<16;x++){
        const v=(_h(x,y)*noise)|0;
        const i=(y*16+x)*4;
        img.data[i]=Math.min(255,r+v-noise/2);
        img.data[i+1]=Math.min(255,g+v-noise/2);
        img.data[i+2]=Math.min(255,b+v-noise/2);
        img.data[i+3]=255;
      }
      ctx.putImageData(img,0,0);
    });
  }

  /* Stone-like base with two-tone hash */
  function _stone_like(r,g,b,dark=18,bright=14){
    return _c16((ctx)=>{
      const img=ctx.createImageData(16,16);
      for(let y=0;y<16;y++) for(let x=0;x<16;x++){
        const h=_h(x,y), hh=_h(x+7,y+3);
        let v= h<0.22 ? -(dark+(_h(x+1,y+1)*6)|0)
              : h>0.78 ? (bright+(_h(x+2,y+2)*5)|0)
              : ((_h(x+3,y+5)*8)|0)-4;
        const i=(y*16+x)*4;
        img.data[i]=Math.max(0,Math.min(255,r+v));
        img.data[i+1]=Math.max(0,Math.min(255,g+v));
        img.data[i+2]=Math.max(0,Math.min(255,b+v));
        img.data[i+3]=255;
      }
      ctx.putImageData(img,0,0);
    });
  }

  /* Stone + ore patches */
  function _ore(sr,sg,sb, or_,og,ob, thresh=0.82){
    return _c16((ctx)=>{
      const img=ctx.createImageData(16,16);
      for(let y=0;y<16;y++) for(let x=0;x<16;x++){
        const h=_h(x,y), hh=_h(x+9,y+11), hh2=_h(x+4,y+7);
        let r,g,b;
        if(h>thresh && hh>0.45){
          const t=_h(x+2,y+13);
          r=or_+((t*20)|0)-10; g=og+((t*20)|0)-10; b=ob+((t*20)|0)-10;
        } else {
          const v=h<0.22?-18:h>0.78?14:((_h(x+3,y+5)*8)|0)-4;
          r=sr+v; g=sg+v; b=sb+v;
        }
        const i=(y*16+x)*4;
        img.data[i]=Math.max(0,Math.min(255,r));
        img.data[i+1]=Math.max(0,Math.min(255,g));
        img.data[i+2]=Math.max(0,Math.min(255,b));
        img.data[i+3]=255;
      }
      ctx.putImageData(img,0,0);
    });
  }

  /* Plank-like horizontal bands */
  function _planks(r,g,b,stripe=4){
    return _c16((ctx)=>{
      const img=ctx.createImageData(16,16);
      for(let y=0;y<16;y++) for(let x=0;x<16;x++){
        const band=Math.floor(y/stripe), offset=(band%2)*7;
        const n=(_h(x+offset,y)*14)|0;
        const dark=y%stripe===0?-14:0;
        const i=(y*16+x)*4;
        img.data[i]  =Math.max(0,Math.min(255,r+n-7+dark));
        img.data[i+1]=Math.max(0,Math.min(255,g+n-7+dark));
        img.data[i+2]=Math.max(0,Math.min(255,b+n-7+dark));
        img.data[i+3]=255;
      }
      ctx.putImageData(img,0,0);
    });
  }

  /* Wool: flat solid tint with subtle cross-hatch */
  function _wool(r,g,b){
    return _c16((ctx)=>{
      const img=ctx.createImageData(16,16);
      for(let y=0;y<16;y++) for(let x=0;x<16;x++){
        const cross=(x%2===0||y%2===0)?-8:0;
        const n=(_h(x,y)*10)|0;
        const i=(y*16+x)*4;
        img.data[i]  =Math.max(0,Math.min(255,r+n+cross));
        img.data[i+1]=Math.max(0,Math.min(255,g+n+cross));
        img.data[i+2]=Math.max(0,Math.min(255,b+n+cross));
        img.data[i+3]=255;
      }
      ctx.putImageData(img,0,0);
    });
  }

  /* Brick pattern */
  function _bricks(wr,wg,wb, mr,mg,mb){
    return _c16((ctx)=>{
      const img=ctx.createImageData(16,16);
      for(let y=0;y<16;y++) for(let x=0;x<16;x++){
        const row=Math.floor(y/4); const offset=(row%2)*8;
        const mortar=(y%4===0)||(((x+offset)%8===0));
        const n=(_h(x,y)*10)|0;
        const [r,g,b]=mortar?[mr,mg,mb]:[wr+n-5,wg+n-5,wb+n-5];
        const i=(y*16+x)*4;
        img.data[i]=r; img.data[i+1]=g; img.data[i+2]=b; img.data[i+3]=255;
      }
      ctx.putImageData(img,0,0);
    });
  }

  /* Log: bark on sides row 0-15, ring on ends */
  function _log_side(r,g,b){ return _planks(r,g,b,2); }
  function _log_top(r,g,b){
    return _c16((ctx)=>{
      ctx.fillStyle=`rgb(${r},${g},${b})`;
      ctx.fillRect(0,0,16,16);
      ctx.strokeStyle=`rgba(0,0,0,0.35)`;
      ctx.lineWidth=1;
      // concentric rings
      for(let i=2;i<8;i+=2){
        ctx.beginPath(); ctx.arc(8,8,i,0,Math.PI*2); ctx.stroke();
      }
    });
  }
"""

# ── All procedural keys (blocks without OGA direct mapping) ───────────────────
# Format: key: JS_expression (will be emitted as _t.key = <expr>;)
PROC_DEFS: dict[str, str] = {
    # Ores — stone_generic (130,130,135) + colored patches
    'coal_ore':        '_ore(130,130,135, 45,45,45)',
    'iron_ore':        '_ore(130,130,135, 200,155,110)',
    'gold_ore':        '_ore(130,130,135, 220,185,40)',
    'redstone_ore':    '_ore(130,130,135, 200,50,50)',
    'lapis_ore':       '_ore(130,130,135, 40,80,200)',
    'diamond_ore':     '_ore(130,130,135, 80,215,210)',
    'emerald_ore':     '_ore(130,130,135, 40,180,60)',
    # Deepslate ores — slate base (88,88,95) + ore patches
    'deepslate_coal_ore':    '_ore(88,88,95, 45,45,45)',
    'deepslate_diamond_ore': '_ore(88,88,95, 80,215,210)',
    'deepslate_emerald_ore': '_ore(88,88,95, 40,180,60)',
    'deepslate_gold_ore':    '_ore(88,88,95, 220,185,40)',
    'deepslate_iron_ore':    '_ore(88,88,95, 200,155,110)',
    'deepslate_lapis_ore':   '_ore(88,88,95, 40,80,200)',
    'deepslate_redstone_ore':'_ore(88,88,95, 200,50,50)',
    # Refined blocks
    'iron_block':      '_solid(190,190,195,8)',
    'gold_block':      '_solid(235,195,40,12)',
    'diamond_block':   '_solid(75,210,205,12)',
    'emerald_block':   '_solid(35,175,55,12)',
    'copper_block':    '_solid(185,95,65,14)',
    'lapis_block':     '_solid(35,65,175,10)',
    # Special/light
    'glowstone':       '_solid(240,195,80,20)',
    'sea_lantern':     '_solid(210,228,235,18)',
    'magma':           '_stone_like(190,75,30,25,20)',
    'shroomlight':     '_solid(235,155,50,18)',
    'slime':           '_solid(105,175,80,12)',
    'honey_top':       '_solid(215,140,40,14)',
    'honey_side':      '_solid(200,125,35,14)',
    'honey_bottom':    '_solid(185,110,30,14)',
    'sponge':          '_stone_like(215,200,85,16,14)',
    # End/Nether
    'end_stone_bricks':'_stone_like(210,200,150,14,12)',
    'soul_sand':       '_stone_like(80,68,55,14,10)',
    # Prismarine
    'prismarine_bricks':'_stone_like(80,155,145,18,14)',
    'prismarine_rough': '_stone_like(70,140,130,20,16)',
    'prismarine_dark':  '_stone_like(50,105,95,18,14)',
    # Mushroom caps
    'mushroom_block_skin_red':   '_solid(185,40,35,16)',
    'mushroom_block_skin_brown': '_solid(145,100,65,14)',
    # Specialty
    'tnt_side':   '_bricks(195,50,45, 30,30,30)',
    'tnt_top':    '_solid(100,175,60,14)',
    'tnt_bottom': '_stone_like(175,175,175,14,12)',
    'pumpkin_side':    '_planks(205,115,40,8)',
    'pumpkin_top':     '_stone_like(190,105,35,18,14)',
    'pumpkin_face_off':'_stone_like(190,105,35,18,14)',
    'melon_side':      '_planks(70,140,55,8)',
    'melon_top':       '_solid(55,120,45,14)',
    'crafting_table_top':   '_bricks(155,115,75, 80,60,40)',
    'crafting_table_front': '_planks(155,115,75,4)',
    'crafting_table_side':  '_planks(155,115,75,4)',
    'furnace_top':     '_stone_like(140,130,120,16,12)',
    'furnace_side':    '_stone_like(140,130,120,16,12)',
    'furnace_front_off':'_stone_like(130,120,110,16,12)',
    'bookshelf':       '_bricks(155,115,75, 60,40,20)',
    'mycelium_side':   '_stone_like(120,95,125,18,14)',
    'mycelium_top':    '_stone_like(100,70,110,20,15)',
    'dirt_podzol_side':'_stone_like(100,80,55,18,14)',
    'dirt_podzol_top': '_stone_like(90,105,60,18,14)',
    # Wools
    'white_wool':      '_wool(220,220,220)',
    'light_blue_wool': '_wool(100,165,210)',
    'blue_wool':       '_wool(55,80,175)',
    'green_wool':      '_wool(60,145,50)',
    'yellow_wool':     '_wool(235,210,55)',
    'orange_wool':     '_wool(225,130,45)',
    'red_wool':        '_wool(185,45,40)',
    'black_wool':      '_wool(35,35,35)',
    # Ice
    'ice':             '_solid(150,185,220,18)',
    'blue_ice':        '_solid(100,145,205,14)',
    'ice_packed':      '_solid(130,165,215,16)',
}

# ── Write textures_free.js ────────────────────────────────────────────────────
lines: list[str] = []
lines.append('/* Auto-generated — CC0 OGA block textures + procedural fills.')
lines.append(' * OGA source: https://opengameart.org/content/16x16-block-textures (CC0)')
lines.append(' * Kenney sounds: https://kenney.nl/assets/impact-sounds (CC0)')
lines.append(' * Procedural fills: original code, no third-party IP.')
lines.append(' * Run tools/gen_free_assets.py to regenerate. */')
lines.append('window.FREE_TEX = {};')
lines.append('(function(){')
lines.append('  const _t = window.FREE_TEX;')
lines.append('')
lines.append('  /* === CC0 OGA embedded textures === */')

for key, uri in sorted(mc_tex_from_oga.items()):
    lines.append(f"  _t['{key}'] = '{uri}';")

lines.append('')
lines.append('  /* === Procedural fills === */')
lines.append(PROC_JS)

for key, expr in sorted(PROC_DEFS.items()):
    if key not in mc_tex_from_oga:  # don't overwrite OGA textures
        lines.append(f"  _t['{key}'] = {expr};")

lines.append('})();')

OUT_TX.write_text('\n'.join(lines), encoding='utf-8')
print(f'Wrote {OUT_TX}  ({OUT_TX.stat().st_size//1024} KB)')
print(f'  OGA-mapped keys: {len(mc_tex_from_oga)}')
print(f'  Procedural keys: {sum(1 for k in PROC_DEFS if k not in mc_tex_from_oga)}')

# ── Write sounds_free.js ──────────────────────────────────────────────────────
slines: list[str] = []
slines.append('/* Auto-generated — CC0 Kenney Impact Sounds embedded as base64.')
slines.append(' * Source: https://kenney.nl/assets/impact-sounds (CC0)')
slines.append(' * tnt_fuse and slime_jump are synthesised via Web Audio in audio.js.')
slines.append(' * Run tools/gen_free_assets.py to regenerate. */')
slines.append('window.FREE_SFX = {')
for key, uri in sounds.items():
    slines.append(f"  {key}: '{uri}',")
slines.append('};')

OUT_SX.write_text('\n'.join(slines), encoding='utf-8')
print(f'Wrote {OUT_SX}  ({OUT_SX.stat().st_size//1024} KB)')
print(f'  Sound keys: {list(sounds.keys())}')
print('Done.')
