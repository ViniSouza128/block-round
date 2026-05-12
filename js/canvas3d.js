/* =============================================================================
   Block Round — js/canvas3d.js
   All Rights Reserved on code. MC textures are Mojang property.

   Three.js voxel renderer using real MC block textures (base64 data URIs
   from textures.js → MC_TEX[key], piped through THREE.TextureLoader).

   Render mode (state.render) chooses which voxels are emitted via the
   shared voxelShell(). The edge-overlay preference is a pair of flags:
     • state.edges3d           — applied to opaque blocks; default ON.
     • state.edges3dTransparent — applied to Glass / Ice;   default OFF.
   effectiveEdges3D() picks the right one for the currently-selected
   block. The Grid corner button toggles whichever flag applies, so
   leaving a transparent block returns the user to their last opaque
   preference automatically.

   Special-case block behaviours wired up here:
     • grass_block   → multi-face material via getMaterial3D: grass_top
                       on +Y, grass_block_side on the four sides, dirt
                       on -Y. Random pattern uses the same key when
                       stamping the top voxel of each (x,z) column.
     • glass / ice   → MeshLambertMaterial with alphaTest:0.5 so the
                       inner panes drop out, mirroring MC's translucent
                       look without depth-sort artefacts.
     • magma / sea_lantern / prismarine (animated vertical sprite strips)
                       → texture window is locked to one 16x16 frame via
                       repeat.y = 1/N, and offset.y is driven on the
                       Bedrock tick by js/flipbook.js so the block pulses
                       on screen instead of being frozen on frame 0.
     • sand / gravel → after a 500 ms hold the voxels fall under
                       gravity onto an invisible floor at the figure's
                       bottom-most Y. Animation supports both the
                       textured-mesh path and the InstancedMesh
                       wireframe path. Driven by _fall3DStart /
                       _fall3DTick.
     • center toggle → toggleCenter3D() adds/removes the cross WITHOUT
                       rebuilding the voxel mesh, so an in-progress
                       fall animation isn't interrupted.
   ============================================================================ */

let scene3D = null, camera3D = null, renderer3D = null, voxelGroup3D = null;
let centerCross3D = null;
let voxelEdges3D  = null;
/* Snapshot of the last build's voxels + figure-center offsets so
   toggleEdges3D() can flip the edge overlay without rebuilding the
   voxel mesh (and therefore without restarting any sand/gravel fall). */
let _lastVoxels3D = null, _lastDims3D = null;

/* Geometry signature — concatenation of every state field that, if changed,
   forces a fresh voxel mesh. Anything not in this list (camera ops, edge
   overlay, center cross, 2D-only flags, focus state, …) MUST NOT rebuild,
   otherwise an in-progress sand/gravel fall gets erased. */
let _lastGeomSig3D = null;
function _geomSig3D(){
  return [
    state.shape, state.size, state.width, state.height, state.depth,
    state.cut, state.axis, state.render, state.algo, state.mcBlock, state.mode
  ].join('|');
}

/* Effective edge-overlay preference. Transparent blocks (glass, ice,
   slime, honey) read state.edges3dTransparent (default OFF — the
   outlines compete with the alpha rendering); everything else reads
   state.edges3d. */
const _TRANSPARENT_BLOCK_SET = new Set(['glass', 'ice', 'slime', 'honey']);
function effectiveEdges3D(){
  if (_TRANSPARENT_BLOCK_SET.has(state.mcBlock)){
    return !!state.edges3dTransparent;
  }
  return !!state.edges3d;
}
let distance3D = 70;
let theta3D = Math.PI / 4;
let phi3D = Math.PI / 3;
let _frame3DReady = false;
let _animPending = false;
const _texCache = new Map();  // key → THREE.Texture
const _matCache = new Map();  // key → THREE.MeshLambertMaterial
let _wireMat = null;

/* Called by asset_toggle.js when the active texture pack changes. */
function clearTexCache3D(){
  _texCache.forEach(t => t.dispose());
  _texCache.clear();
  _matCache.forEach(m => { if (Array.isArray(m)) m.forEach(x => x.dispose()); else m.dispose(); });
  _matCache.clear();
  if (_wireMat){ _wireMat.dispose(); _wireMat = null; }
}

function getTexture3D(key){
  if (_texCache.has(key)) return _texCache.get(key);
  // Look up by raw MC_TEX key FIRST — the multi-face tables here reference
  // face textures (hay_block_top, log_birch_top, …) that live only in
  // MC_TEX, not in MC_BLOCKS. Fall back to the picker catalog so the
  // single-texture path still works.
  let src = (window.MC_TEX && window.MC_TEX[key]) || null;
  if (!src){
    const b = MC_BLOCKS[key];
    if (b && b.src) src = b.src;
  }
  if (!src) return null;
  const tex = new THREE.TextureLoader().load(src, (t) => {
    // Animated MC textures are vertical strips of 16×16 frames. Lock
    // repeat.y to 1/N so each face shows exactly one frame, then drive
    // offset.y per Bedrock tick via the shared flipbook ticker. flipY
    // defaults to true on THREE textures, so the *top* PNG row sits at
    // v = 1 — i.e. frame i lives at offset.y = (N - 1 - i) / N.
    const im = t.image;
    const N = (window.flipbookFrameCount ? window.flipbookFrameCount(im) : 1);
    if (N > 1){
      t.repeat.set(1, 1 / N);
      t.offset.set(0, (N - 1) / N);
      t.needsUpdate = true;
      const fbKey = (window.resolveFlipbookKey && window.resolveFlipbookKey(key)) || key;
      window.registerFlipbook(fbKey, N, (frameIdx) => {
        t.offset.y = (N - 1 - frameIdx) / N;
        if (state && state.mode === '3d') scheduleRender3D();
      });
    }
    scheduleRender3D();
  });
  tex.magFilter = THREE.NearestFilter;
  tex.minFilter = THREE.NearestFilter;
  tex.generateMipmaps = false;
  _texCache.set(key, tex);
  return tex;
}
/* Multi-face blocks. In real Minecraft a lot of blocks render different
   textures on top/sides/bottom — these are the ones we wire up here.
   The face order Three.js expects on a BoxGeometry is
       [+X, -X, +Y, -Y, +Z, -Z]
   i.e. [right, left, top, bottom, front, back]. For most "natural"
   blocks we want [side, side, top, bottom, side, side]. Textures come
   straight from the Mojang bedrock-samples drop into textures.js. */
const MULTI_FACE_3D = {
  // [+X, -X, +Y, -Y, +Z, -Z] keyed against MC_TEX entries.
  grass:        ['grass_side', 'grass_side', 'grass', 'dirt', 'grass_side', 'grass_side'],
  oak_log:      ['oak_log', 'oak_log', 'oak_log_top', 'oak_log_top', 'oak_log', 'oak_log'],
  birch_log:    ['log_birch', 'log_birch', 'log_birch_top', 'log_birch_top', 'log_birch', 'log_birch'],
  spruce_log:   ['log_spruce', 'log_spruce', 'log_spruce_top', 'log_spruce_top', 'log_spruce', 'log_spruce'],
  jungle_log:   ['log_jungle', 'log_jungle', 'log_jungle_top', 'log_jungle_top', 'log_jungle', 'log_jungle'],
  acacia_log:   ['log_acacia', 'log_acacia', 'log_acacia_top', 'log_acacia_top', 'log_acacia', 'log_acacia'],
  dark_oak_log: ['log_big_oak', 'log_big_oak', 'log_big_oak_top', 'log_big_oak_top', 'log_big_oak', 'log_big_oak'],
  // Pumpkin: stem on top, plain-side on the 4 sides, stem on bottom too.
  // (Carved-pumpkin face is `pumpkin_face_off`; we use the plain side here
  // since the picker shows just "pumpkin" without a directional face.)
  pumpkin:      ['pumpkin_side', 'pumpkin_side', 'pumpkin_top', 'pumpkin_top', 'pumpkin_side', 'pumpkin_side'],
  // Hay & Bone: end-grain on top/bottom, bark-like side on the 4 sides.
  hay:          ['hay_block_side', 'hay_block_side', 'hay_block_top', 'hay_block_top', 'hay_block_side', 'hay_block_side'],
  bone:         ['bone_block_side', 'bone_block_side', 'bone_block_top', 'bone_block_top', 'bone_block_side', 'bone_block_side'],
  // Melon: striped top/bottom, plain green side around.
  melon:        ['melon_side', 'melon_side', 'melon_top', 'melon_top', 'melon_side', 'melon_side'],
  // Quartz: smooth top, fluted side, smooth bottom (different from top).
  quartz:       ['quartz_block_side', 'quartz_block_side', 'quartz_block_top', 'quartz_block_bottom', 'quartz_block_side', 'quartz_block_side'],
  // Sandstone: smooth cap on top, chiselled side, smooth base on bottom.
  sandstone:    ['sandstone', 'sandstone', 'sandstone_top', 'sandstone_bottom', 'sandstone', 'sandstone'],
  // Crafted blocks. Crafting table has a recipe-grid top, planks-and-saw
  // sides, with an alternate front face. Furnace is similar: hot front,
  // generic side, bare top.
  crafting_table: ['crafting_table_side', 'crafting_table_front',
                   'crafting_table_top', 'oak_planks',
                   'crafting_table_front', 'crafting_table_side'],
  furnace:        ['furnace_side', 'furnace_front_off',
                   'furnace_top', 'furnace_top',
                   'furnace_front_off', 'furnace_side'],
  // Bookshelf: book spines on the 4 sides, plain planks on top and bottom.
  bookshelf:      ['bookshelf', 'bookshelf', 'oak_planks', 'oak_planks',
                   'bookshelf', 'bookshelf'],
  // TNT: red side with diagonal lines, fuse top, plain bottom.
  tnt:            ['tnt_side', 'tnt_side', 'tnt_top', 'tnt_bottom',
                   'tnt_side', 'tnt_side'],
  // Mycelium: purple cap, brown side (dirt-mossy), plain dirt bottom.
  mycelium:       ['mycelium_side', 'mycelium_side',
                   'mycelium_top', 'dirt',
                   'mycelium_side', 'mycelium_side'],
  // Podzol: spruce-litter cap, dirt-with-needles side, plain dirt bottom.
  podzol:         ['dirt_podzol_side', 'dirt_podzol_side',
                   'dirt_podzol_top', 'dirt',
                   'dirt_podzol_side', 'dirt_podzol_side'],
  // Honey Block is handled separately (shell + inner core), since it needs
  // multi-face uvs on the translucent outer and a single-tex opaque core.
};

/* Returns either a single material or an array of six materials so a single
   BoxGeometry can render distinct textures per face. Multi-face entries
   come from MULTI_FACE_3D above; alpha blocks (glass, ice) get an alphaTest
   material; everything else gets a plain single-texture Lambert. */
function getMaterial3D(key){
  if (_matCache.has(key)) return _matCache.get(key);

  if (MULTI_FACE_3D[key]){
    const faceTextures = MULTI_FACE_3D[key];
    const mats = faceTextures.map(texKey => new THREE.MeshLambertMaterial({
      map: getTexture3D(texKey),
    }));
    _matCache.set(key, mats);
    return mats;
  }

  // Light-emitting blocks pick up an emissive map at intensity scaled
  // by the in-game light level (max 15). The base map stays so the
  // shadow side still reads, but the texture also shines on its own
  // — independent of scene lighting — exactly like MC's luminance.
  const EMISSIVE_BLOCKS = {
    glowstone:        0.75,  // light 15
    sea_lantern:      0.70,
    shroomlight:      0.65,
    magma:            0.45,
    crying_obsidian:  0.35,  // light 10
  };
  if (EMISSIVE_BLOCKS[key] !== undefined){
    const tex = getTexture3D(key);
    const mat = new THREE.MeshLambertMaterial({
      map: tex,
      emissive: 0xffffff,
      emissiveMap: tex,
      emissiveIntensity: EMISSIVE_BLOCKS[key],
    });
    _matCache.set(key, mat);
    return mat;
  }

  // Glass / Ice — alphaTest keeps panes see-through while the frame stays
  // solid. The actual same-material face culling for "MC-style" rendering
  // happens in buildTransparentMesh() in update3D.
  if (key === 'glass' || key === 'ice'){
    const tex = getTexture3D(key);
    const mat = new THREE.MeshLambertMaterial({
      map: tex, transparent: true, alphaTest: 0.5, depthWrite: true,
    });
    _matCache.set(key, mat);
    return mat;
  }

  // Slime / Honey — alpha-BLENDED translucent shell (no alphaTest). In
  // real Minecraft these blocks are a uniformly translucent jelly cube
  // wrapping an opaque inner core. depthWrite:false so the core
  // (rendered before, as a smaller solid cube via buildInnerCore3D) is
  // visible through the shell; DoubleSide so the inner faces of the
  // shell are also drawn when looking at the figure from inside a cut.
  if (key === 'slime' || key === 'honey'){
    const texKey = key === 'slime' ? 'slime' : 'honey_side';
    const tex = getTexture3D(texKey);
    const mat = new THREE.MeshLambertMaterial({
      map: tex, transparent: true, depthWrite: false,
      side: THREE.DoubleSide,
    });
    _matCache.set(key, mat);
    return mat;
  }

  // Oak leaves (tree easter egg) — alphaTest carves the gaps between the
  // leaf clusters out of the cube, so neighbouring leaf blocks read as a
  // proper sparse canopy rather than a solid green box. DoubleSide so the
  // inner faces of each leaf cube are visible at oblique angles.
  if (key === 'oak_leaves'){
    const tex = getTexture3D(key);
    const mat = new THREE.MeshLambertMaterial({
      map: tex, transparent: true, alphaTest: 0.5, depthWrite: true,
      side: THREE.DoubleSide,
    });
    _matCache.set(key, mat);
    return mat;
  }

  const tex = getTexture3D(key);
  const mat = new THREE.MeshLambertMaterial({ map: tex });
  _matCache.set(key, mat);
  return mat;
}
/* Inner-core material for the shell-and-core look on Slime / Honey
   blocks. Same texture as the shell, but with no alpha blending — so
   each voxel gets a solid smaller cube visible through the translucent
   outer wrap, matching real Minecraft. Cached separately from the
   outer material (which is the regular getMaterial3D entry). */
function getInnerCoreMaterial3D(key){
  const cacheKey = '_core_' + key;
  if (_matCache.has(cacheKey)) return _matCache.get(cacheKey);
  const texKey = key === 'slime' ? 'slime' : 'honey_side';
  const tex = getTexture3D(texKey);
  const mat = new THREE.MeshLambertMaterial({ map: tex });
  _matCache.set(cacheKey, mat);
  return mat;
}

function getWireMat(){
  if (_wireMat) return _wireMat;
  _wireMat = new THREE.MeshBasicMaterial({ color: 0xFFEC4F, wireframe: true });
  return _wireMat;
}

function init3D(canvas){
  if (_frame3DReady) return true;
  if (typeof THREE === 'undefined' || !canvas) return false;

  const rect = canvas.parentElement.getBoundingClientRect();
  const w = Math.max(1, Math.floor(rect.width));
  const h = Math.max(1, Math.floor(rect.height));

  renderer3D = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer3D.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer3D.setSize(w, h, false);

  scene3D = new THREE.Scene();
  scene3D.background = null; // MC sky gradient shows through via CSS

  camera3D = new THREE.PerspectiveCamera(35, w / h, 0.1, 2000);
  updateCamera3D();

  const key = new THREE.DirectionalLight(0xffffff, 0.95);
  key.position.set(50, 80, 50);
  scene3D.add(key);
  const fill = new THREE.DirectionalLight(0xffffff, 0.40);
  fill.position.set(-40, 20, -30);
  scene3D.add(fill);
  scene3D.add(new THREE.AmbientLight(0xffffff, 0.35));

  _frame3DReady = true;
  scheduleRender3D();
  return true;
}

/* Bounding box of the CURRENTLY-VISIBLE part of the figure, in world
   coords (where the full figure is centred on origin). Takes the active
   cut into account so the camera reframes when the user trims the
   figure — without this the model drifts toward the bottom-left of
   the canvas as the right/top is sliced away.

   For each axis the kept range:
     X:   [0, min(Dx, cut)-1]    when cutAxis === 'x'
     Y:   [0, min(Dy, cut)-1]    when cutAxis === 'y'
     diag: same as X+Y but bounded by the (x+y < cut) diagonal, which
          we approximate via the bbox max(x) ≤ cut-1, max(y) ≤ cut-1
          for camera-fit purposes (slight over-allocation is fine —
          worst case the camera leaves a little extra margin).
   Returns center + half-extent of the kept bbox in world units, plus
   the tree's vertical extension when the easter egg is on. */
function _visibleBounds3D(){
  const isEllipse = state.shape === 'ellipse';
  const Dx = isEllipse ? state.width  : state.size;
  const Dy = isEllipse ? state.height : state.size;
  const Dz = isEllipse ? state.depth  : state.size;

  let xMax = Dx, yMax = Dy;
  if (state.axis === 'x' && state.cut < Dx)        xMax = state.cut;
  else if (state.axis === 'y' && state.cut < Dy)   yMax = state.cut;
  else if (state.axis === 'diag' && state.cut < (Dx + Dy)){
    // Diagonal slice in (x, y). Both axes get clipped to (cut-something).
    // For the bbox we use min(D, cut) on each axis, which is a tight
    // bound when cut < min(Dx, Dy) and a loose bound when cut > one
    // axis's dim. Either way it never under-frames.
    xMax = Math.min(Dx, state.cut);
    yMax = Math.min(Dy, state.cut);
  }

  // Half-extent in each direction.
  const hx = xMax / 2;
  const hy = yMax / 2;
  const hz = Dz   / 2;

  // Kept voxels: x ∈ [0, xMax-1] in figure coords. Each voxel renders
  // at (x - (Dx-1)/2) in world coords. So kept voxels' world x ∈
  // [-(Dx-1)/2, xMax-1-(Dx-1)/2]. Midpoint = (xMax - Dx)/2.
  const cxW = (xMax - Dx) / 2;
  const cyW = (yMax - Dy) / 2;
  const czW = 0;

  // Easter-egg extensions (tree, creeper) only extend upward (in +Y).
  // Add whichever is active to the +Y side of the bbox so the camera
  // pulls back AND looks higher. Only one easter egg can be active at
  // a time (their trigger blocks differ — Grass/Dirt/Random vs TNT),
  // so a plain max() correctly picks the active one.
  const treeExtra    = (typeof treeBoundsExtraY    === 'function') ? treeBoundsExtraY()    : 0;
  const creeperExtra = (typeof creeperBoundsExtraY === 'function') ? creeperBoundsExtraY() : 0;
  const eggExtra = Math.max(treeExtra, creeperExtra);
  const yTop = cyW + hy + eggExtra;
  const yBot = cyW - hy;
  const finalCy = (yTop + yBot) / 2;
  const finalHy = (yTop - yBot) / 2;

  /* Creeper override: when the creeper easter egg is on, the geometric
     centre of figure+creeper sits halfway up the figure — far below the
     creeper itself. We instead orbit/lookAt the creeper's FEET (= world
     Y of the figure's top face) so the creeper stays roughly centred on
     screen. `hy` is recomputed as the max distance from feet to any
     bbox edge so the bounding-sphere autoZoom still fits everything
     (figure body extends downward, creeper extends upward). */
  if (typeof creeperIsActive === 'function' && creeperIsActive()){
    const feetY = cyW + hy;                       // world Y of figure top face
    const hyFromFeet = Math.max(feetY - yBot,     // downward (whole figure)
                                yTop  - feetY);   // upward   (creeper)
    return { cx: cxW, cy: feetY, cz: czW, hx, hy: hyFromFeet, hz };
  }

  return { cx: cxW, cy: finalCy, cz: czW, hx, hy: finalHy, hz };
}

/* Camera orbits AND looks at the figure's visible centre, so cuts AND
   the tree easter egg both keep the model framed properly. */
function updateCamera3D(){
  if (!camera3D) return;
  const b = _visibleBounds3D();
  camera3D.position.x = b.cx + distance3D * Math.sin(phi3D) * Math.cos(theta3D);
  camera3D.position.y = b.cy + distance3D * Math.cos(phi3D);
  camera3D.position.z = b.cz + distance3D * Math.sin(phi3D) * Math.sin(theta3D);
  camera3D.lookAt(b.cx, b.cy, b.cz);
  scheduleRender3D();
}
function resetCamera3D(){ theta3D = Math.PI / 4; phi3D = Math.PI / 3; autoZoom3D(); }

/* autoZoom3D — fit the cut-adjusted visible bounding box into the
   viewport. The bounding sphere of that bbox guarantees no clipping
   at any rotation angle. Called on figure changes and double-click
   reset only — user wheel/pinch zoom is preserved across drags. */
function autoZoom3D(){
  if (!camera3D) return;
  const b = _visibleBounds3D();
  const R = Math.sqrt(b.hx*b.hx + b.hy*b.hy + b.hz*b.hz);
  const vFov = camera3D.fov * Math.PI / 180;
  const hFov = 2 * Math.atan(Math.tan(vFov / 2) * camera3D.aspect);
  const distV = R / Math.tan(vFov / 2);
  const distH = R / Math.tan(hFov / 2);
  // 1.20× margin keeps a visible gap between model and canvas edges.
  distance3D = Math.max(2, Math.max(distV, distH) * 1.20);
  updateCamera3D();
}

/* ---------- EASTER EGG: OAK TREE ----------------------------------------
   Plants a small oak tree (4-block trunk + 4-layer leaf canopy with the
   bottom two canopy layers overlapping the upper two trunk blocks)
   directly on top of the 3D figure.

   Trigger rules:
     • Sphere    → state.size === 15.
     • Ellipsoid → any of state.width / state.height / state.depth === 15.
       The sphere `state.size` is intentionally NOT a trigger when in
       ellipsoid shape, since the value is not visible/editable there.
     • Block must be Grass Block, Dirt or Random (random's top voxel is
       always grass). No tree on stone, glass, wool, etc.

   Cut behaviours:
     • X cut → tree slices laterally with the figure (voxels at x ≥ cut
       are skipped, just like figure voxels).
     • Y cut < Dy → tree disappears entirely (its base sits above the
       figure's top, so any vertical trim should erase it).

   Together with treeBoundsExtraY() / treeBoundsXRange(), the 3D
   autoZoom uses these dimensions to keep the whole composition framed. */
function treeIsActive(){
  if (!isTreeBlock(state.mcBlock)) return false;
  if (state.shape === 'circle')  return state.size === 15;
  /* ellipsoid */                return state.width === 15 || state.height === 15 || state.depth === 15;
}

function isTreeBlock(key){
  // The block on top of the figure must be soil-like for the tree to
  // make sense. Random qualifies because the random pattern always
  // stamps grass on the topmost voxel of every column.
  return key === 'grass_block' || key === 'dirt' || key === 'random';
}

const TREE_TRUNK_H = 4;
const TREE_CANOPY_TOP_OFFSET = TREE_TRUNK_H - 2 + 3;  // top y above figure
function treeBoundsExtraY(){
  // Tree's top voxel is at y = Dy + TREE_TRUNK_H + 1 (layer3) = Dy + 5
  // relative to figure-local coords. So tree adds (5 + 1) cells of
  // height above the figure's topmost cell.
  return treeIsActive() ? (TREE_TRUNK_H + 2) : 0;
}

function buildEasterEggTree(Dx, Dy, Dz, cx, cy, cz, geom){
  if (!treeIsActive()) return;
  // Y cut active → tree disappears (its base is above the figure).
  // Y cut active → tree disappears wholesale (its base sits ABOVE the
  // figure top, so any vertical trim erases it). X and Diag cuts let
  // the tree survive but slice individual blocks like the figure does.
  if (state.axis === 'y' && state.cut < Dy) return;

  // Per-block slice limits. Each tree voxel is dropped if it falls past
  // the active cut, matching how the figure itself is sliced:
  //   X cut    → drop tree voxels at lx >= cutXLimit
  //   diag cut → drop tree voxels at lx + ly >= cutDiagLimit
  const cutXLimit    = state.axis === 'x'    ? state.cut : Dx;
  const cutDiagLimit = state.axis === 'diag' ? state.cut : Infinity;
  const treeCX = Math.floor((Dx - 1) / 2);
  const treeCZ = Math.floor((Dz - 1) / 2);
  const baseY  = Dy;  // first voxel above the topmost figure voxel

  const addBlock = (lx, ly, lz, matKey) => {
    if (lx < 0 || lx >= cutXLimit)  return;   // X cut
    if (lx + ly >= cutDiagLimit)    return;   // diag cut
    const mat = getMaterial3D(matKey);
    const mesh = new THREE.Mesh(geom, mat);
    mesh.position.set(lx - cx, ly - cy, lz - cz);
    voxelGroup3D.add(mesh);
  };

  // Trunk: 4 oak_log stacked dead-centre.
  for (let i = 0; i < TREE_TRUNK_H; i++){
    addBlock(treeCX, baseY + i, treeCZ, 'oak_log');
  }

  // Canopy — 4 ascending layers. Bottom two overlap the top two logs.
  const layer0base = baseY + TREE_TRUNK_H - 2;
  const SQ5 = [];
  for (let dz = -2; dz <= 2; dz++)
    for (let dx = -2; dx <= 2; dx++)
      if (!(Math.abs(dx) === 2 && Math.abs(dz) === 2)) SQ5.push([dx, dz]);
  const SQ3 = [];
  for (let dz = -1; dz <= 1; dz++)
    for (let dx = -1; dx <= 1; dx++) SQ3.push([dx, dz]);
  const CROSS = [[0,0], [-1,0], [1,0], [0,-1], [0,1]];

  const LAYERS = [
    { dy: 0, pat: SQ5   },
    { dy: 1, pat: SQ5   },
    { dy: 2, pat: SQ3   },
    { dy: 3, pat: CROSS },
  ];
  for (const L of LAYERS){
    for (const [dx, dz] of L.pat){
      addBlock(treeCX + dx, layer0base + L.dy, treeCZ + dz, 'oak_leaves');
    }
  }
}

/* ---------- EASTER EGG: TNT CREEPER -------------------------------------
   Spawns a real Minecraft creeper standing on top of the 3D figure when
   the user builds an iconic Minecraft moment: a TNT figure with a "15"
   on any active size slider. The creeper itself is rendered with its
   own green-mottled "creeper.png"-style skin (procedurally drawn on a
   canvas so we don't ship a binary asset) and the iconic black face
   on the front of the head — not built out of TNT cubes.

   Trigger rules (mirrors the oak-tree easter egg's structure):
     • Block must be TNT (no creeper on stone, grass, etc).
     • Sphere    → state.size === 15.
     • Ellipsoid → any of state.width / state.height / state.depth === 15.

   Geometry — sub-block scale, using real Minecraft entity proportions
   (16 px = 1 block). Six box parts:
     head   8×8×8  px  → 0.500 × 0.500 × 0.500 blocks
     body   4×12×8 px  → 0.250 × 0.750 × 0.500 blocks
     leg×4  4×6×4  px  → 0.250 × 0.375 × 0.250 blocks
   Total height = 0.375 (legs) + 0.750 (body) + 0.500 (head) = 1.625 blocks.
   The creeper sits centred on the figure top, facing +z so the face is
   visible at the default camera angle (theta = π/4, looking from +x+z).

   Cut behaviours (since the creeper is small and centred we use a
   simple all-or-nothing rule — the body never crosses a cut plane):
     • Y cut < Dy                     → hide.
     • X cut <= floor(Dx/2)           → hide.
     • Diag cut <= floor(Dx/2)+Dy-1   → hide.

   Info-chip block count: the creeper is added after the count is
   locked, just like the tree, so the displayed total stays as
   "blocks needed to build the figure". */
const CREEPER_TOTAL_H = 1.625;   // 0.375 legs + 0.75 body + 0.5 head
const CREEPER_LEG_H   = 0.375;
const CREEPER_BODY_H  = 0.75;
const CREEPER_HEAD_H  = 0.5;

function creeperIsActive(){
  if (state.mcBlock !== 'tnt') return false;
  if (state.shape === 'circle')  return state.size === 15;
  /* ellipsoid */                return state.width === 15 || state.height === 15 || state.depth === 15;
}

function creeperBoundsExtraY(){
  return creeperIsActive() ? Math.ceil(CREEPER_TOTAL_H) : 0;
}

/* Creeper skin atlas (64×32 px) — PROCEDURALLY drawn, not a copy of the
   real Mojang creeper.png binary. We don't ship the actual entity file
   (we'd need a redistribution licence we don't have); instead, the
   pattern below reconstructs the visual character of the real texture
   from primitives:
     • a 7-shade green palette spanning the same range as Mojang's
       (from #2E641D very dark up to #74D654 highlight)
     • a base mid-green wash, then per-pixel speckles weighted toward
       darker shades (matches the speckly look real creeper.png has)
     • larger 2-px chunks of contrasting shade scattered on top
       (matches the patchy clusters visible on the real model)
     • the canonical black eye-and-mouth pattern painted into the
       head-front region (atlas coords 8..15, 8..15)
   The visual result is close enough that a casual viewer reads it as
   "a real creeper"; the model proportions and UV layout below are
   pixel-exact replicas of the entity model.

   Atlas layout matches the canonical Minecraft creeper.png:
     HEAD  top (8,0,8,8)   bottom (16,0,8,8)
           right (0,8,8,8) front (8,8,8,8) left (16,8,8,8) back (24,8,8,8)
     BODY  top (20,16,4,8) bottom (24,16,4,8)
           left (16,20,8,12) front (24,20,4,12)
           right (28,20,8,12) back (36,20,4,12)
     LEG   top (4,16,4,4)  bottom (8,16,4,4)
           right (0,20,4,6) front (4,20,4,6)
           left (8,20,4,6) back (12,20,4,6)
   Built once, cached for the session. */
const CREEPER_ATLAS_W = 64;
const CREEPER_ATLAS_H = 32;
let _creeperAtlasMat = null;
function _getCreeperAtlasMat(){
  if (_creeperAtlasMat) return _creeperAtlasMat;

  const c = document.createElement('canvas');
  c.width = CREEPER_ATLAS_W; c.height = CREEPER_ATLAS_H;
  const ctx = c.getContext('2d');

  // 7-shade palette: very-dark → dark → mid-dark → BASE → mid-light →
  // light → highlight. Indices align with the weighted distribution
  // used below in the speckle pass.
  const PALETTE = [
    '#2e641d',  // 0 very dark   (rare, deep shadows)
    '#3a7d22',  // 1 dark
    '#43912a',  // 2 mid-dark
    '#54ad37',  // 3 BASE
    '#5fbe3f',  // 4 mid-light
    '#6acc48',  // 5 light
    '#74d654',  // 6 highlight   (rare, brightest pops)
  ];
  // Hash → palette index with a distribution centred on BASE so the
  // skin reads as "mostly-green-with-speckles" rather than uniform noise.
  //   00..0F (~6%)  →  0  very dark
  //   10..2F (~12%) →  1  dark
  //   30..5F (~19%) →  2  mid-dark
  //   60..9F (~25%) →  3  base
  //   A0..C7 (~16%) →  4  mid-light
  //   C8..EF (~16%) →  5  light
  //   F0..FF (~6%)  →  6  highlight
  const shadeFor = (h) => {
    if (h < 0x10) return 0;
    if (h < 0x30) return 1;
    if (h < 0x60) return 2;
    if (h < 0xA0) return 3;
    if (h < 0xC8) return 4;
    if (h < 0xF0) return 5;
    return 6;
  };

  // Pass 1 — wash the whole atlas in the base shade so any thin
  // anti-aliasing artefacts at face boundaries fall back to a sensible
  // green rather than transparent.
  ctx.fillStyle = PALETTE[3];
  ctx.fillRect(0, 0, CREEPER_ATLAS_W, CREEPER_ATLAS_H);

  // Pass 2 — per-pixel speckle, deterministic hash. Same input → same
  // texture every reload, so the creeper looks identical session over
  // session. Two prime-mix hashes XORed to spread the bits well.
  for (let y = 0; y < CREEPER_ATLAS_H; y++){
    for (let x = 0; x < CREEPER_ATLAS_W; x++){
      const h = (((x * 374761393) ^ (y * 668265263) ^ ((x * y + 1) * 2246822519)) >>> 0) & 0xff;
      ctx.fillStyle = PALETTE[shadeFor(h)];
      ctx.fillRect(x, y, 1, 1);
    }
  }

  // Pass 3 — chunky 2×1 / 1×2 / 2×2 patches that mimic the larger
  // dark-green blobs visible on the real creeper.png. A second hash
  // decides patch size and shade independently of pass 2.
  for (let y = 0; y < CREEPER_ATLAS_H; y += 2){
    for (let x = 0; x < CREEPER_ATLAS_W; x += 2){
      const h = (((x * 1597) ^ (y * 31397) ^ ((x + y) * 6151)) >>> 0) & 0xff;
      // Only ~30 % of cells get a patch; the rest keep their speckle
      // values from pass 2.
      if (h > 0x4D) continue;
      // Patch shape from low bits, patch shade from high bits.
      const shape = h & 0x3;        // 0..3
      const shade = ((h >> 2) & 0x7);
      ctx.fillStyle = PALETTE[shade > 6 ? 6 : shade];
      if      (shape === 0) ctx.fillRect(x,   y,   2, 1);
      else if (shape === 1) ctx.fillRect(x,   y,   1, 2);
      else if (shape === 2) ctx.fillRect(x,   y,   2, 2);
      else                  ctx.fillRect(x+1, y+1, 1, 1);  // tiny accent
    }
  }

  // Iconic creeper face — painted over the head-front region (8,8)-(16,16).
  const FACE = [
    '........',
    '.##..##.',
    '.##..##.',
    '...##...',
    '..####..',
    '..####..',
    '..#..#..',
    '........',
  ];
  ctx.fillStyle = '#0a1a0a';
  for (let fy = 0; fy < 8; fy++){
    for (let fx = 0; fx < 8; fx++){
      if (FACE[fy][fx] === '#') ctx.fillRect(8 + fx, 8 + fy, 1, 1);
    }
  }

  const tex = new THREE.CanvasTexture(c);
  tex.magFilter = THREE.NearestFilter;
  tex.minFilter = THREE.NearestFilter;
  tex.generateMipmaps = false;
  // The emissive channel is what drives the "primed swell" white pulse
  // every cycle — we lock the colour to white at construction time and
  // animate only the intensity from the rAF tick. Starts at 0 so the
  // creeper looks normal until the first stare ignites.
  _creeperAtlasMat = new THREE.MeshLambertMaterial({
    map: tex,
    emissive: 0xffffff,
    emissiveIntensity: 0,
  });
  return _creeperAtlasMat;
}

/* Remap a BoxGeometry's UV attribute so each of its six faces samples
   a specific rectangle of the creeper atlas. `regions` is an array in
   BoxGeometry face order [+X, -X, +Y, -Y, +Z, -Z], each entry an
   [atlasX, atlasY, atlasW, atlasH] tuple in pixels (atlas origin
   top-left). Three.js textures use bottom-left origin, so we flip V. */
function _setBoxAtlasUVs(geom, regions){
  const uv = geom.attributes.uv;
  for (let f = 0; f < 6; f++){
    const [x, y, w, h] = regions[f];
    const u1 = x / CREEPER_ATLAS_W;
    const u2 = (x + w) / CREEPER_ATLAS_W;
    const v1 = 1 - (y + h) / CREEPER_ATLAS_H;
    const v2 = 1 - y / CREEPER_ATLAS_H;
    const i = f * 4;
    uv.setXY(i + 0, u1, v2);   // top-left vertex of the face
    uv.setXY(i + 1, u2, v2);   // top-right
    uv.setXY(i + 2, u1, v1);   // bottom-left
    uv.setXY(i + 3, u2, v1);   // bottom-right
  }
  uv.needsUpdate = true;
}

// Atlas regions per part — face order is [+X, -X, +Y, -Y, +Z, -Z].
const CREEPER_HEAD_UV = [
  [16, 8, 8, 8],   // +X right
  [ 0, 8, 8, 8],   // -X left  (atlas "right" region renders on the model's left side; symmetric mottle hides the mirror)
  [ 8, 0, 8, 8],   // +Y top
  [16, 0, 8, 8],   // -Y bottom
  [ 8, 8, 8, 8],   // +Z front  (FACE)
  [24, 8, 8, 8],   // -Z back
];
const CREEPER_BODY_UV = [
  [28, 20, 8, 12], // +X right
  [16, 20, 8, 12], // -X left
  [20, 16, 4, 8],  // +Y top
  [24, 16, 4, 8],  // -Y bottom
  [24, 20, 4, 12], // +Z front
  [36, 20, 4, 12], // -Z back
];
const CREEPER_LEG_UV = [
  [ 0, 20, 4, 6],  // +X
  [ 8, 20, 4, 6],  // -X
  [ 4, 16, 4, 4],  // +Y top
  [ 8, 16, 4, 4],  // -Y bottom
  [ 4, 20, 4, 6],  // +Z front
  [12, 20, 4, 6],  // -Z back
];

/* Animation — two layered behaviours running off the same rAF:
     • Idle micro-motion: very slow head Y-sway and gentle leg X-sway
       so the creeper never looks frozen.
     • Eye-contact cycle (every 6 s): the creeper smoothly turns its
       whole body toward the camera, holds the gaze, then eases back to
       neutral. The body rotation is what pivots the head + legs as one
       unit (Y around the creeper's own axis), so the user perceives an
       intentional "the creeper just looked at me" beat.

   Pivot groups: the head and each leg are wrapped in their own
   THREE.Group so we can rotate them around their joints (legs around
   their tops, head around its centre) instead of their geometric
   origins. The body root group's rotation drives the look-at-camera
   turn. */
// Cycle = rise + hold + fall + breather. The breather is intentionally
// long so the creeper "forgets" the user for a long stretch between
// stares. The fall back to neutral is deliberately the LONGEST phase
// of the stare arc — a slow drift away from the user rather than an
// abrupt snap back — which mirrors how an animal slowly looks off
// after eye contact rather than reverting instantly.
const CREEPER_RISE_S     = 0.75;  // ease into camera-gaze (fast lock-on)
const CREEPER_HOLD_S     = 1.0;   // dwell at the gaze
const CREEPER_FALL_S     = 2.25;  // slow, natural return — 3× the rise
const CREEPER_BREATHER_S = 12.6;  // idle pause before the next stare (was 7 s, +80 %)
const CREEPER_CYCLE_S    = CREEPER_RISE_S + CREEPER_HOLD_S
                         + CREEPER_FALL_S + CREEPER_BREATHER_S;  // 16.6 s
// Grace period after the creeper first appears before its very first
// stare. The user spawns the easter egg; we let them admire the model
// for a beat before the creeper "notices" them. Implemented by
// pre-aging the animation clock so the first tick lands inside the
// breather phase with this many seconds remaining until the rise.
const CREEPER_INITIAL_DELAY_S = 6.0;

// White brightness pulse — the "primed/swell flash" the real creeper
// fires when it locks onto a player and starts its detonation
// countdown. Fast attack to peak (~50 ms — looks like a sudden bloom),
// then a long exponential decay so the residual glow lingers and
// fades naturally instead of cliff-edging to off. Peak emissive 0.375
// keeps the underlying creeper texture clearly readable through the
// bloom (was 0.75 — halved per visual feedback that the model was
// going too white).
const CREEPER_FLASH_S        = 2.9;   // total flash window (0.05 attack + 2.85 decay)
const CREEPER_FLASH_ATTACK_S = 0.05;
const CREEPER_FLASH_PEAK     = 0.375; // half of the previous 0.75
const CREEPER_FLASH_DECAY_K  = 3.0;   // exp(-k·u) coefficient, u in [0..1]

// Head pitch clamp during the stare. Real MC creepers can pitch up to
// ±90°, but at extreme angles the cube head looks like it's bent on a
// hinge rather than tracking a tall/short player. ±60° (= π/3) covers
// every realistic camera elevation in this app's orbit while keeping
// the cube head visually plausible.
const CREEPER_PITCH_CLAMP = Math.PI / 3;

// Random-walk parameters — the creeper wanders within a 3×3 grid
// centred on its original spawn cell (so ±WALK_RANGE blocks in X
// and Z). The walk advances only during the breather phase of the
// stare cycle (blend ≈ 0); the moment the creeper starts looking
// at the user, the walk state machine freezes. After the stare
// ends, the walk resumes with a brief pause before the next step
// — feels like the creeper "catches its breath" after eye contact.
// Grid radius (in cell indices) and cell pitch in world units. The grid
// is still 3×3 cells, but each cell is only CELL_SIZE = 0.6 blocks
// wide — so the footprint shrinks from a ±1-block square to ±0.6-block
// square. That kills the "creeper sliding too fast for its legs" feel
// reported visually: per leg cycle the body now covers 60 % of the
// world distance it used to.
//
// Speed is intentionally co-scaled with cell size (0.4 → 0.24 b/s)
// so the cardinal step duration stays at the previous 2.5 s:
//     duration = distance / speed = 0.6 / 0.24 = 2.5 s
// The leg gait is synced to step progress (one sine cycle per step),
// so equal step duration means EQUAL leg-animation speed — exactly
// the constraint the user asked for.
const CREEPER_WALK_RANGE        = 1;     // ±1 cell indices → 3×3 grid
const CREEPER_WALK_CELL_SIZE    = 0.6;   // world units per cell (was implicitly 1)
const CREEPER_WALK_SPEED_BPS    = 0.24;  // co-scaled so duration is unchanged
const CREEPER_WALK_PAUSE_MIN_S  = 0.4;   // shortest dwell at a cell
const CREEPER_WALK_PAUSE_MAX_S  = 1.0;   // longest dwell at a cell
const CREEPER_WALK_LEG_AMP_DEG  = 18;    // ±° leg swing while a step is in flight
const CREEPER_WALK_BLEND_THRESH = 0.01;  // below this, treat blend as "idle"

let _creeperGroup    = null;   // current creeper THREE.Group (or null)
let _creeperParts    = null;   // { head, legs:[fl,fr,bl,br] } pivot groups
let _creeperAnimRaf  = null;
let _creeperAnimT0   = 0;
let _creeperLastCyc  = -1;     // last completed look-cycle index (for fuse trigger)
let _creeperWasShown = false;  // tracks creeperIsActive() across update3D

// Random-walk state. _creeperPosX/Z is the smoothly interpolated world
// offset (relative to the spawn-centre cell); during 'walk' phase it
// lerps from origin → target, during 'pause' it equals the target
// (i.e. an integer cell in the 3×3). _creeperWalkYaw is the facing
// direction the body holds while the current step is in flight; it
// also serves as the BASE yaw the stare-yaw lerps away from.
let _creeperPosX            = 0;
let _creeperPosZ            = 0;
let _creeperOriginX         = 0;
let _creeperOriginZ         = 0;
let _creeperTargetX         = 0;
let _creeperTargetZ         = 0;
let _creeperWalkPhase       = 'pause';   // 'walk' | 'pause'
let _creeperWalkPhaseStartT = 0;
let _creeperWalkPhaseDur    = 0;
let _creeperWalkYaw         = 0;
let _creeperPrevBlend       = 0;         // detect stare → idle transition each tick

/* Pick a random neighbour cell of (cx, cz) inside the 3×3 grid.
   Skips the current cell and any cell outside ±CREEPER_WALK_RANGE.
   Corner cells have 3 neighbours, edges 5, centre 8 — uniform
   sampling within the valid set gives the corners less time and
   keeps the wander biased toward the middle, which looks natural. */
function _pickCreeperNeighbour(cx, cz){
  const options = [];
  for (let dx = -1; dx <= 1; dx++){
    for (let dz = -1; dz <= 1; dz++){
      if (dx === 0 && dz === 0) continue;
      const nx = cx + dx, nz = cz + dz;
      if (nx < -CREEPER_WALK_RANGE || nx > CREEPER_WALK_RANGE) continue;
      if (nz < -CREEPER_WALK_RANGE || nz > CREEPER_WALK_RANGE) continue;
      options.push([nx, nz]);
    }
  }
  return options[Math.floor(Math.random() * options.length)];
}

/* Wrap a signed angle into [-π, π] so we lerp along the shortest
   arc between two yaws. Without this, a transition from yaw +170°
   to yaw -170° would take the long way around (340°) instead of
   the short 20° flip across the −180/+180 boundary. */
function _shortestAngle(a){
  while (a >  Math.PI) a -= 2 * Math.PI;
  while (a < -Math.PI) a += 2 * Math.PI;
  return a;
}

function _randomCreeperPause(){
  return CREEPER_WALK_PAUSE_MIN_S
       + Math.random() * (CREEPER_WALK_PAUSE_MAX_S - CREEPER_WALK_PAUSE_MIN_S);
}

/* Cubic ease-in-out so the body acceleration into and out of the gaze
   feels organic — no abrupt linear ramp. */
function _easeInOut(x){
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
}

/* Look-blend in [0..1] given the cycle-local time t.
   Phase plan (one 6 s cycle):
     0.0 .. 1.5   rise from 0 → 1  (turning to face the camera)
     1.5 .. 3.5   hold at 1        (locked gaze; the "stare" beat)
     3.5 .. 5.0   fall from 1 → 0  (turning back to neutral)
     5.0 .. 6.0   idle at 0        (one-second breather between cycles) */
function _creeperLookBlend(t){
  const ct = ((t % CREEPER_CYCLE_S) + CREEPER_CYCLE_S) % CREEPER_CYCLE_S;
  if (ct < CREEPER_RISE_S){
    return _easeInOut(ct / CREEPER_RISE_S);
  }
  if (ct < CREEPER_RISE_S + CREEPER_HOLD_S){
    return 1;
  }
  if (ct < CREEPER_RISE_S + CREEPER_HOLD_S + CREEPER_FALL_S){
    const ft = (ct - CREEPER_RISE_S - CREEPER_HOLD_S) / CREEPER_FALL_S;
    return 1 - _easeInOut(ft);
  }
  return 0;  // idle tail
}

function _creeperAnimTick(){
  if (!_creeperGroup || !_creeperGroup.parent){
    _creeperAnimRaf = null;
    return;
  }
  const t = (performance.now() - _creeperAnimT0) * 0.001;

  // Stare-synced TNT fuse — fires once per cycle, exactly when the
  // rise phase begins. The fuse sample (~4 s) overruns the 2.5 s
  // stare, which mirrors the real game: the hiss starts before the
  // explosion and trails off after. Sfx.tnt() internally stops any
  // previous fuse before starting, so re-entering the cycle never
  // stacks.
  const cycleIdx = Math.floor(t / CREEPER_CYCLE_S);
  if (cycleIdx > _creeperLastCyc){
    _creeperLastCyc = cycleIdx;
    if (typeof Sfx !== 'undefined' && Sfx && typeof Sfx.tnt === 'function'){
      Sfx.tnt();
    }
  }

  // White "primed-swell" pulse — fires from the same moment as the
  // fuse and the rise. Real MC overlays a brightness multiplier on
  // the creeper texture as the detonation countdown approaches; we
  // do the same with the material's emissive channel:
  //   0 .. ATTACK_S         linear ramp 0 → PEAK   (sudden bloom)
  //   ATTACK_S .. FLASH_S   exp(-k·u) tail to 0    (slow fade)
  // Outside that window the pulse is hard-cleared to 0 so the
  // residual emissive can't leak into the long breather phase.
  const cycleLocalT = ((t % CREEPER_CYCLE_S) + CREEPER_CYCLE_S) % CREEPER_CYCLE_S;
  let flashI = 0;
  if (cycleLocalT < CREEPER_FLASH_ATTACK_S){
    flashI = (cycleLocalT / CREEPER_FLASH_ATTACK_S) * CREEPER_FLASH_PEAK;
  } else if (cycleLocalT < CREEPER_FLASH_S){
    const u = (cycleLocalT - CREEPER_FLASH_ATTACK_S)
            / (CREEPER_FLASH_S - CREEPER_FLASH_ATTACK_S);  // u in [0..1]
    flashI = Math.exp(-CREEPER_FLASH_DECAY_K * u) * CREEPER_FLASH_PEAK;
  }
  if (_creeperAtlasMat) _creeperAtlasMat.emissiveIntensity = flashI;

  const blend = _creeperLookBlend(t);
  const now = performance.now();

  // -------------------- WALK STATE MACHINE --------------------------
  // The creeper only advances its random walk while the look-blend is
  // essentially zero (breather phase). During the stare arc the state
  // machine is frozen and the body holds its last walk position +
  // facing. The instant the blend drops back to zero (stare → idle
  // transition) we reset to a brief 'pause' so the creeper "catches
  // its breath" before the next step instead of teleporting forward.
  const stareEnded = (_creeperPrevBlend >= CREEPER_WALK_BLEND_THRESH
                  && blend < CREEPER_WALK_BLEND_THRESH);
  if (stareEnded){
    _creeperWalkPhase       = 'pause';
    _creeperWalkPhaseStartT = now;
    _creeperWalkPhaseDur    = _randomCreeperPause() * 1000;
  }
  _creeperPrevBlend = blend;

  if (blend < CREEPER_WALK_BLEND_THRESH){
    const phaseT = now - _creeperWalkPhaseStartT;
    if (_creeperWalkPhase === 'pause'){
      // Sit at the target cell. When the pause window expires, pick a
      // random neighbour of the rounded current cell as the next
      // target and switch to 'walk'.
      if (phaseT >= _creeperWalkPhaseDur){
        // Convert the current world-space position to the nearest cell
        // INDEX so the neighbour-pick stays in integer-grid logic; the
        // returned indices are converted back to world units via
        // CELL_SIZE for the lerp endpoints. This split lets us keep
        // _pickCreeperNeighbour purely combinatorial (validates ±RANGE
        // on integer cells) while the actual rendered displacement
        // shrinks with CELL_SIZE.
        const cxIdx = Math.round(_creeperPosX / CREEPER_WALK_CELL_SIZE);
        const czIdx = Math.round(_creeperPosZ / CREEPER_WALK_CELL_SIZE);
        const [tiIdx, tjIdx] = _pickCreeperNeighbour(cxIdx, czIdx);
        _creeperOriginX = _creeperPosX;  // start the lerp from the actual position
        _creeperOriginZ = _creeperPosZ;  // (may not be a grid cell after a stare)
        _creeperTargetX = tiIdx * CREEPER_WALK_CELL_SIZE;
        _creeperTargetZ = tjIdx * CREEPER_WALK_CELL_SIZE;
        const dx = _creeperTargetX - _creeperOriginX;
        const dz = _creeperTargetZ - _creeperOriginZ;
        _creeperWalkYaw      = Math.atan2(dx, dz);
        _creeperWalkPhase    = 'walk';
        _creeperWalkPhaseStartT = now;
        _creeperWalkPhaseDur    = (Math.hypot(dx, dz) / CREEPER_WALK_SPEED_BPS) * 1000;
      }
    } else { /* 'walk' */
      const p = Math.min(1, phaseT / _creeperWalkPhaseDur);
      _creeperPosX = _creeperOriginX + (_creeperTargetX - _creeperOriginX) * p;
      _creeperPosZ = _creeperOriginZ + (_creeperTargetZ - _creeperOriginZ) * p;
      if (p >= 1){
        // Arrived — clamp to the target cell and dwell.
        _creeperPosX = _creeperTargetX;
        _creeperPosZ = _creeperTargetZ;
        _creeperWalkPhase       = 'pause';
        _creeperWalkPhaseStartT = now;
        _creeperWalkPhaseDur    = _randomCreeperPause() * 1000;
      }
    }
  }
  // Apply the walking position (Y is set once at build to Dy/2 and
  // never changes — the creeper walks on the figure-top plane).
  _creeperGroup.position.x = _creeperPosX;
  _creeperGroup.position.z = _creeperPosZ;

  // -------------------- STARE-AWARE YAW + PITCH ---------------------
  // Body YAW — interpolates between the walking facing direction and
  // the camera-facing direction using the look-blend. atan2(dx, dz) is
  // correct because a rotation.y of θ maps local +Z to world
  // (sinθ, 0, cosθ); for the body's +Z to point at the camera, solving
  // sinθ = camDX/|d|, cosθ = camDZ/|d| gives θ = atan2(camDX, camDZ).
  // The stare yaw is computed relative to the creeper's CURRENT
  // position (not the spawn origin) so the gaze is correct even when
  // the creeper has wandered to an edge of the 3×3.
  let stareYaw = _creeperWalkYaw;
  if (camera3D){
    const dxC = camera3D.position.x - _creeperPosX;
    const dzC = camera3D.position.z - _creeperPosZ;
    if (Math.hypot(dxC, dzC) > 1e-4) stareYaw = Math.atan2(dxC, dzC);
  }
  // Shortest-arc lerp between walk yaw and stare yaw so the body
  // never spins the long way round at the −π/+π wrap-around.
  const yawDelta = _shortestAngle(stareYaw - _creeperWalkYaw);
  _creeperGroup.rotation.y = _creeperWalkYaw + yawDelta * blend;

  // Head PITCH — tilts the face up/down to track tall or short camera
  // angles. Computed from the head's CURRENT world position (walks
  // with the body), then clamped so an extreme overhead camera can't
  // bend the cube head into a hinge. In three.js Rx(+θ) maps +Z toward
  // −Y (DOWN), so we negate the target to lift the face up when the
  // camera is above.
  let targetPitch = 0;
  if (camera3D){
    const headWorldX = _creeperPosX;
    const headWorldZ = _creeperPosZ;
    const headWorldY = _creeperGroup.position.y
                     + (CREEPER_LEG_H + CREEPER_BODY_H + CREEPER_HEAD_H / 2);
    const dy  = camera3D.position.y - headWorldY;
    const dxz = Math.hypot(camera3D.position.x - headWorldX,
                           camera3D.position.z - headWorldZ);
    targetPitch = Math.atan2(dy, dxz);
    if (targetPitch >  CREEPER_PITCH_CLAMP) targetPitch =  CREEPER_PITCH_CLAMP;
    if (targetPitch < -CREEPER_PITCH_CLAMP) targetPitch = -CREEPER_PITCH_CLAMP;
  }

  // Head idle Y-sway — plays during the breather, damps as the gaze
  // intensifies. Pitch and sway live on different axes (X vs Y) so
  // they never fight; their blend factors are reciprocal so the head
  // smoothly hands off between "looking at the user" and "idle bob".
  const idleSway = Math.sin(t * 2 * Math.PI * 0.18) * (6 * Math.PI / 180);
  _creeperParts.head.rotation.x = -blend * targetPitch;
  _creeperParts.head.rotation.y = idleSway * (1 - blend);

  // -------------------- LEGS: WALKING GAIT vs IDLE ------------------
  // While a step is in flight (blend ≈ 0 AND phase === 'walk'), legs
  // run a full-amplitude gait: one sine cycle per step, alternating
  // pairs in opposite phase. Sync to step progress (not wall-clock)
  // so the legs visibly "finish their stride" exactly when the body
  // arrives at the target cell — that's what kills the slide effect.
  //
  // Otherwise (paused, staring, or transitioning) the legs play the
  // tiny idle sway, damped by the stare blend so a locked-in gaze
  // reads as "locked on" rather than "paused mid-bob".
  const [fl, fr, bl, br] = _creeperParts.legs;
  if (blend < CREEPER_WALK_BLEND_THRESH && _creeperWalkPhase === 'walk'){
    const phaseT = now - _creeperWalkPhaseStartT;
    const p = Math.min(1, phaseT / _creeperWalkPhaseDur);
    const gaitPhase = p * 2 * Math.PI;
    const swing = Math.sin(gaitPhase) * (CREEPER_WALK_LEG_AMP_DEG * Math.PI / 180);
    fl.rotation.x =  swing;
    br.rotation.x =  swing;
    fr.rotation.x = -swing;
    bl.rotation.x = -swing;
  } else {
    const legSway = Math.sin(t * 2 * Math.PI * 0.5) * (4 * Math.PI / 180);
    const legAmp  = 1 - 0.7 * blend;
    fl.rotation.x =  legSway * legAmp;
    br.rotation.x =  legSway * legAmp;
    fr.rotation.x = -legSway * legAmp;
    bl.rotation.x = -legSway * legAmp;
  }

  scheduleRender3D();
  _creeperAnimRaf = requestAnimationFrame(_creeperAnimTick);
}

function buildEasterEggCreeper(Dx, Dy, Dz, cx, cy, cz){
  // Reset module-scope creeper handles each rebuild — the previous
  // group was destroyed when voxelGroup3D was disposed.
  _creeperGroup = null;
  _creeperParts = null;
  if (_creeperAnimRaf){ cancelAnimationFrame(_creeperAnimRaf); _creeperAnimRaf = null; }

  const nowActive = creeperIsActive();
  // The fuse is no longer played on spawn — it's now tied to the
  // every-12-s stare cycle in _creeperAnimTick. But if the creeper
  // *was* on screen and just left (slider stepped off 15, or block
  // changed) we cut any in-flight fuse so it can't outlive the
  // creeper that was making the noise.
  if (!nowActive && _creeperWasShown){
    if (typeof Sfx !== 'undefined' && Sfx && typeof Sfx.stopTnt === 'function'){
      Sfx.stopTnt();
    }
    // Clear any in-flight primed-flash so the cached material doesn't
    // re-mount the next creeper mid-pulse.
    if (_creeperAtlasMat) _creeperAtlasMat.emissiveIntensity = 0;
  }
  _creeperWasShown = nowActive;

  if (!nowActive) return;

  // All-or-nothing cut rules — the creeper occupies the top-centre of
  // the figure, so if that voxel is cut away there's nothing to stand
  // on and we hide the entire creeper.
  const centerX = Math.floor(Dx / 2);
  if (state.axis === 'y'    && state.cut <  Dy)                return;
  if (state.axis === 'x'    && state.cut <= centerX)           return;
  if (state.axis === 'diag' && state.cut <= centerX + Dy - 1)  return;

  const mat = _getCreeperAtlasMat();

  // Root group sits at the figure-top centre. The figure spans world
  // y ∈ [-Dy/2, +Dy/2] (the -cy offset is already baked into each
  // voxel's mesh.position), so y = +Dy/2 is the figure's top face.
  const root = new THREE.Group();
  root.position.set(0, Dy / 2, 0);

  // Helper — build a Box with custom UV atlas regions, optionally
  // wrapping it in a pivot group so rotations happen around a joint
  // rather than the mesh's geometric centre.
  const buildPart = (wPx, hPx, dPx, uvRegions) => {
    const g = new THREE.BoxGeometry(wPx / 16, hPx / 16, dPx / 16);
    _setBoxAtlasUVs(g, uvRegions);
    return new THREE.Mesh(g, mat);
  };

  // --- Legs --------------------------------------------------------
  // Each leg is wrapped in a pivot Group at the hip joint (top of the
  // leg). The leg mesh hangs below the pivot so rotating the pivot
  // around X sways the foot.
  const legXZ = 0.125;                       // ±2 px from centre
  const hipY  = CREEPER_LEG_H;               // joint is at top of leg
  const legs = [];
  const mkLeg = (sx, sz) => {
    const pivot = new THREE.Group();
    pivot.position.set(sx * legXZ, hipY, sz * legXZ);
    const mesh = buildPart(4, 6, 4, CREEPER_LEG_UV);
    mesh.position.set(0, -CREEPER_LEG_H / 2, 0); // hang below joint
    pivot.add(mesh);
    root.add(pivot);
    legs.push(pivot);
    return pivot;
  };
  mkLeg(-1, +1);  // front-left  (front = +z in our convention)
  mkLeg(+1, +1);  // front-right
  mkLeg(-1, -1);  // back-left
  mkLeg(+1, -1);  // back-right

  // --- Body --------------------------------------------------------
  const bodyMesh = buildPart(4, 12, 8, CREEPER_BODY_UV);
  bodyMesh.position.set(0, CREEPER_LEG_H + CREEPER_BODY_H / 2, 0);
  root.add(bodyMesh);

  // --- Head --------------------------------------------------------
  // Wrap the head in a pivot so we can rotate it around its own centre
  // without moving the body. Pivot Y is at the head's centre.
  const headY = CREEPER_LEG_H + CREEPER_BODY_H + CREEPER_HEAD_H / 2;
  const headPivot = new THREE.Group();
  headPivot.position.set(0, headY, 0);
  const headMesh = buildPart(8, 8, 8, CREEPER_HEAD_UV);
  headPivot.add(headMesh);
  root.add(headPivot);

  voxelGroup3D.add(root);

  // Wire the animation loop. Stored module-scope so the rAF tick can
  // mutate the right parts and stop when the group is removed.
  _creeperGroup  = root;
  _creeperParts  = { head: headPivot, legs };
  // Pre-age the clock so the first tick sits inside the breather phase
  // with exactly CREEPER_INITIAL_DELAY_S seconds left before the very
  // first rise. At wall-clock t=0 the cycleLocalT is (CYCLE - DELAY) —
  // deep in the idle tail — so no fuse, no flash, no body rotation
  // happens for the grace period. The first stare lands at t = DELAY.
  _creeperAnimT0  = performance.now()
                  - (CREEPER_CYCLE_S - CREEPER_INITIAL_DELAY_S) * 1000;
  // Cycle index 0 has effectively "already happened" during pre-age,
  // so the fuse trigger waits for the transition to cycle 1 (which
  // lines up with the end of the grace period — exactly when the
  // first rise begins).
  _creeperLastCyc = 0;

  // Reset the random-walk state machine so a fresh creeper always
  // starts at the centre cell, facing +Z (the spawn-default), and
  // begins with a short pause before its first step.
  _creeperPosX            = 0;
  _creeperPosZ            = 0;
  _creeperOriginX         = 0;
  _creeperOriginZ         = 0;
  _creeperTargetX         = 0;
  _creeperTargetZ         = 0;
  _creeperWalkYaw         = 0;
  _creeperWalkPhase       = 'pause';
  _creeperWalkPhaseStartT = performance.now();
  _creeperWalkPhaseDur    = _randomCreeperPause() * 1000;
  _creeperPrevBlend       = 0;

  _creeperAnimRaf = requestAnimationFrame(_creeperAnimTick);
}

function disposeVoxelGroup(){
  if (!voxelGroup3D) return;
  scene3D.remove(voxelGroup3D);
  voxelGroup3D.traverse(obj => {
    if (obj.geometry) obj.geometry.dispose();
    // Materials are cached in _matCache / _wireMat — don't dispose per rebuild
  });
  voxelGroup3D = null;
}

/* Minecraft-style transparent block rendering. For glass / ice voxels we
   build ONE merged BufferGeometry per material containing only the faces
   that are NOT shared with another voxel of the same material:
     • Two adjacent glass blocks share an internal face — both faces
       culled, so the boundary between them disappears (just like MC).
     • A glass voxel with air on one side keeps that face — you can see
       the pane / frame.
     • Air-separated glass blocks still each keep their facing faces, so
       the user sees through the front pane to the back one's surface,
       not into a hollow interior.
   alphaTest:0.5 in the material then discards the panes inside the
   frame texture, leaving the frame solid and the panes see-through. */
function buildTransparentMesh(voxels, blockKey, cx, cy, cz){
  if (!voxels.length) return null;
  const set = new Set();
  const sk = (x, y, z) => x + ',' + y + ',' + z;
  for (const v of voxels) set.add(sk(v.x, v.y, v.z));

  // Per face: normal, then four quad corners in CCW order seen from
  // outside the cube. We emit two triangles per face below.
  const FACES = [
    { n:[ 1, 0, 0], q:[[ .5,-.5, .5],[ .5, .5, .5],[ .5, .5,-.5],[ .5,-.5,-.5]] }, // +X
    { n:[-1, 0, 0], q:[[-.5,-.5,-.5],[-.5, .5,-.5],[-.5, .5, .5],[-.5,-.5, .5]] }, // -X
    { n:[ 0, 1, 0], q:[[-.5, .5,-.5],[ .5, .5,-.5],[ .5, .5, .5],[-.5, .5, .5]] }, // +Y
    { n:[ 0,-1, 0], q:[[-.5,-.5, .5],[ .5,-.5, .5],[ .5,-.5,-.5],[-.5,-.5,-.5]] }, // -Y
    { n:[ 0, 0, 1], q:[[-.5,-.5, .5],[-.5, .5, .5],[ .5, .5, .5],[ .5,-.5, .5]] }, // +Z
    { n:[ 0, 0,-1], q:[[ .5,-.5,-.5],[ .5, .5,-.5],[-.5, .5,-.5],[-.5,-.5,-.5]] }, // -Z
  ];
  const UV = [[0,0],[0,1],[1,1],[1,0]];

  const positions = [];
  const uvs = [];
  const normals = [];
  for (const v of voxels){
    for (const f of FACES){
      const nx = v.x + f.n[0], ny = v.y + f.n[1], nz = v.z + f.n[2];
      if (set.has(sk(nx, ny, nz))) continue; // shared internal face — cull
      // Triangulate as (0,2,1) + (0,3,2). The reversed order is what gives
      // each triangle a CCW winding when viewed from outside the cube;
      // [0,1,2,0,2,3] produces inward-facing normals, which Three.js's
      // backface cull then drops — exactly what made the glass spheres
      // disappear from outside view in the previous build.
      const tri = [0,2,1, 0,3,2];
      for (let i = 0; i < 6; i++){
        const idx = tri[i];
        const c = f.q[idx];
        positions.push(v.x + c[0] - cx, v.y + c[1] - cy, v.z + c[2] - cz);
        uvs.push(UV[idx][0], UV[idx][1]);
        normals.push(f.n[0], f.n[1], f.n[2]);
      }
    }
  }
  if (!positions.length) return null;

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geo.setAttribute('uv',       new THREE.Float32BufferAttribute(uvs, 2));
  geo.setAttribute('normal',   new THREE.Float32BufferAttribute(normals, 3));
  return new THREE.Mesh(geo, getMaterial3D(blockKey));
}

/* Returns a single LineSegments containing the 12 cube edges of every
   voxel. Toggled by state.edges3d via the canvas Grid button — gives the
   user crisp block outlines on top of the textured faces so they can
   count cells when copying the figure into Minecraft. */
function buildVoxelEdges3D(voxels, cx, cy, cz){
  const E = [
    [-.5,-.5,-.5,  .5,-.5,-.5], [-.5,-.5, .5,  .5,-.5, .5],
    [-.5,-.5,-.5, -.5,-.5, .5], [ .5,-.5,-.5,  .5,-.5, .5],
    [-.5, .5,-.5,  .5, .5,-.5], [-.5, .5, .5,  .5, .5, .5],
    [-.5, .5,-.5, -.5, .5, .5], [ .5, .5,-.5,  .5, .5, .5],
    [-.5,-.5,-.5, -.5, .5,-.5], [ .5,-.5,-.5,  .5, .5,-.5],
    [-.5,-.5, .5, -.5, .5, .5], [ .5,-.5, .5,  .5, .5, .5],
  ];
  const positions = new Float32Array(voxels.length * 12 * 2 * 3);
  let p = 0;
  for (const v of voxels){
    const ox = v.x - cx, oy = v.y - cy, oz = v.z - cz;
    for (const e of E){
      positions[p++] = e[0] + ox; positions[p++] = e[1] + oy; positions[p++] = e[2] + oz;
      positions[p++] = e[3] + ox; positions[p++] = e[4] + oy; positions[p++] = e[5] + oz;
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  // Sand/gravel get a much fainter outline (25 % of the usual opacity)
  // because the falling animation reads better when the cubes don't
  // carry strong outlines — the grain texture itself sells the look.
  // baseOpacity halved (was 0.55 → now 0.275) so the edge overlay
  // stays a hint, not a competing layer over the textured cubes.
  const fadeBlocks = new Set(['sand', 'gravel']);
  const baseOpacity = 0.275;
  const opacity = fadeBlocks.has(state.mcBlock) ? baseOpacity * 0.25 : baseOpacity;
  const mat = new THREE.LineBasicMaterial({
    color: 0x1a0e04, transparent: true, opacity,
  });
  return new THREE.LineSegments(geo, mat);
}

function disposeCenterCross(){
  if (!centerCross3D) return;
  scene3D.remove(centerCross3D);
  centerCross3D.traverse(o => { o.geometry?.dispose?.(); o.material?.dispose?.(); });
  centerCross3D = null;
}

/* Side door for the Center toggle — adds or removes the cross without
   rebuilding the voxel mesh, so an in-progress sand/gravel fall isn't
   interrupted. Reads the current figure dims directly from state. */
function toggleCenter3D(){
  if (!_frame3DReady) return;
  if (state.center){
    const isEllipse = state.shape === 'ellipse';
    const Dx = isEllipse ? state.width : state.size;
    const Dy = isEllipse ? state.height : state.size;
    const Dz = isEllipse ? state.depth : state.size;
    buildCenterCross3D(Dx, Dy, Dz);
  } else {
    disposeCenterCross();
  }
  scheduleRender3D();
}

/* Bars are 1 cube thick when the perpendicular dim is odd, 2 cubes thick
   when it's even (so an even-size sphere shines through the four central
   blocks). Length is huge so axes read as "infinite". */
function buildCenterCross3D(Dx, Dy, Dz){
  disposeCenterCross();
  centerCross3D = new THREE.Group();
  const L = 1500;
  const mat = new THREE.MeshBasicMaterial({
    color: 0xFFEC4F, transparent: true, opacity: 0.30, depthWrite: false,
  });
  const wx = (Dx % 2 === 0) ? 2 : 1;
  const wy = (Dy % 2 === 0) ? 2 : 1;
  const wz = (Dz % 2 === 0) ? 2 : 1;
  const barX = new THREE.Mesh(new THREE.BoxGeometry(L,  wy, wz), mat);
  const barY = new THREE.Mesh(new THREE.BoxGeometry(wx, L,  wz), mat);
  const barZ = new THREE.Mesh(new THREE.BoxGeometry(wx, wy, L ), mat);
  centerCross3D.add(barX, barY, barZ);
  scene3D.add(centerCross3D);
}

function _hash01_3D(x, y, z){
  let h = (x * 2654435761) ^ (y * 40503) ^ (z * 16777619);
  h = Math.imul(h ^ (h >>> 16), 0x21f0aaad);
  h = Math.imul(h ^ (h >>> 15), 0x735a2d97);
  h = h ^ (h >>> 15);
  return (h >>> 0) / 0x100000000;
}

function _pickOre3D(r){
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

function pickBlockForVoxel(v, ext, Dz){
  const block = state.mcBlock;
  const k = v.x * Dz + v.z;
  const topY = ext ? ext.top[k] : -1;
  const botY = ext ? ext.bot[k] : -1;

  if (block === 'random'){
    const gTop = ext.gTop, gBot = ext.gBot;
    const span = gTop - gBot;
    if (span <= 0) return 'grass';
    const t = (gTop - v.y) / span;        // 0 = top, 1 = bottom
    const r = _hash01_3D(v.x, v.y, v.z);
    // Wavy layer boundaries — column-based jitter so the figure cross-section
    // doesn't look like sharp horizontal bands.
    const dirtCut = 0.20 + (_hash01_3D(v.x, 17, v.z) - 0.5) * 0.10;
    const deepCut = 0.80 + (_hash01_3D(v.x, 113, v.z) - 0.5) * 0.12;
    if (v.y === topY)             return 'grass';
    if (v.y === gBot && span > 4) return 'bedrock';
    if (t < dirtCut)              return 'dirt';
    if (t < deepCut)              return _pickOre3D(r);
    return 'deepslate';
  }
  // Grass Block: top voxel of each (x,z) column gets the multi-face grass
  // material (top=grass_top, sides=grass_side, bottom=dirt); voxels
  // below are plain dirt. Plain Dirt selection skips the stamping.
  if (block === 'grass_block' && topY >= 0){
    return v.y === topY ? 'grass' : 'dirt';
  }
  return block;
}

function computeVoxelColumnExtremes(voxels, Dx, Dz){
  const top = new Int32Array(Dx * Dz).fill(-1);
  const bot = new Int32Array(Dx * Dz).fill(Number.MAX_SAFE_INTEGER);
  let gTop = -1, gBot = Number.MAX_SAFE_INTEGER;
  for (let i = 0; i < voxels.length; i++){
    const v = voxels[i];
    const k = v.x * Dz + v.z;
    if (v.y > top[k]) top[k] = v.y;
    if (v.y < bot[k]) bot[k] = v.y;
    if (v.y > gTop) gTop = v.y;
    if (v.y < gBot) gBot = v.y;
  }
  return { top, bot, gTop, gBot };
}

/* ---------- 3D FALL ANIMATION ------------------------------------------- */
const FALL3D_BLOCKS = new Set(['sand', 'gravel']);
const FALL3D_HOLD_MS = 500;
const FALL3D_G = 21;     // ~20% slower than g=30 (matches 2D)
let _fall3DState = null;
let _fall3DRaf = null;

function _fall3DReset(){
  _fall3DState = null;
  if (_fall3DRaf){ cancelAnimationFrame(_fall3DRaf); _fall3DRaf = null; }
}

/* Build the fall plan for a list of voxels. Each cell tracks its starting Y
   plus a target Y (stacked from the figure-wide bottom up). Works for both
   render modes — the caller supplies either:
     • mode='mesh': per-voxel Mesh refs (textured blocks path)
     • mode='inst': a single InstancedMesh + matrix indices (wireframe path)
*/
function _fall3DStart(voxels, payload, mode){
  let floorY = Number.MAX_SAFE_INTEGER;
  for (const v of voxels) if (v.y < floorY) floorY = v.y;
  if (floorY === Number.MAX_SAFE_INTEGER) return;

  const columns = new Map();
  for (let i = 0; i < voxels.length; i++){
    const v = voxels[i];
    const k = v.x * 4096 + v.z;
    if (!columns.has(k)) columns.set(k, []);
    if (mode === 'mesh') columns.get(k).push({ v, mesh: payload[i] });
    else                 columns.get(k).push({ v, idx: i });
  }
  let maxFall = 0;
  const cells = [];
  columns.forEach(col => {
    col.sort((a, b) => a.v.y - b.v.y);
    col.forEach((c, idx) => {
      c.startY = c.v.y;
      c.endY   = floorY + idx;
      const d = c.startY - c.endY;
      if (d > maxFall) maxFall = d;
      cells.push(c);
    });
  });
  _fall3DState = { cells, maxFall, startTime: performance.now(), mode, inst: mode === 'inst' ? payload : null };
}

function _fall3DTick(cx, cy, cz){
  if (!_fall3DState) return;
  const elapsed = performance.now() - _fall3DState.startTime;
  const fd = elapsed < FALL3D_HOLD_MS ? 0 : 0.5 * FALL3D_G * Math.pow((elapsed - FALL3D_HOLD_MS) / 1000, 2);

  if (_fall3DState.mode === 'mesh'){
    for (const c of _fall3DState.cells){
      const drop = Math.min(fd, c.startY - c.endY);
      c.mesh.position.y = (c.startY - drop) - cy;
    }
  } else {
    const dummy = new THREE.Object3D();
    const inst = _fall3DState.inst;
    for (const c of _fall3DState.cells){
      const drop = Math.min(fd, c.startY - c.endY);
      dummy.position.set(c.v.x - cx, (c.startY - drop) - cy, c.v.z - cz);
      dummy.updateMatrix();
      inst.setMatrixAt(c.idx, dummy.matrix);
    }
    inst.instanceMatrix.needsUpdate = true;
  }
  scheduleRender3D();
  if (fd < _fall3DState.maxFall){
    _fall3DRaf = requestAnimationFrame(() => _fall3DTick(cx, cy, cz));
  } else {
    _fall3DRaf = null;
  }
}

function update3D(){
  if (!_frame3DReady) return;
  // DEFINITIVE sand-fall guard. update3D() is the only call path that
  // tears down + rebuilds the voxel mesh. If the geometry signature
  // hasn't actually changed, we short-circuit before the rebuild, so
  // any click/drag/dblclick interaction can never accidentally erase
  // an in-progress (or already-completed) sand or gravel fall.
  const sig = _geomSig3D();
  if (_lastGeomSig3D === sig && voxelGroup3D){
    scheduleRender3D();
    return;
  }
  _lastGeomSig3D = sig;

  disposeVoxelGroup();
  disposeCenterCross();
  _fall3DReset();

  const isEllipse = state.shape === 'ellipse';
  const Dx = isEllipse ? state.width     : state.size;
  const Dy = isEllipse ? state.height     : state.size;
  const Dz = isEllipse ? state.depth : state.size;

  // Cut max depends on the axis: X→Dx, Y→Dy, diag→Dx+Dy (since the
  // diagonal cut uses (x+y) ≥ cut as the exclusion test).
  const maxAxis = state.axis === 'x'    ? Dx
                : state.axis === 'y'    ? Dy
                : /* 'diag' */            (Dx + Dy);
  const cutLimit = state.cut < maxAxis ? state.cut : maxAxis + 1;
  // Filled + transparent is the one case where the cheap "shell-only"
  // voxel set is wrong: the user can SEE through the front panes and
  // would expect to see the dense interior of cubes behind. Use the
  // full solid volume instead. Thin / Thick still go through the
  // regular voxelShell paths so a hollow shell stays a shell.
  // Applies to Glass, Ice, Slime and Honey — all our translucent blocks.
  const TRANSPARENT_BLOCKS = new Set(['glass', 'ice', 'slime', 'honey']);
  const isTransparentFilled =
    state.render === 'filled' && TRANSPARENT_BLOCKS.has(state.mcBlock);
  const voxels = isTransparentFilled
    ? voxelKeptAll(Dx, Dy, Dz, state.axis, cutLimit)
    : voxelShell(Dx, Dy, Dz, state.render, state.axis, cutLimit);
  if (voxels.length === 0){ window._lastBlockCount = 0; scheduleRender3D(); return; }
  // Info-chip block counter — figure voxels only. Tree easter-egg
  // voxels are added later (buildEasterEggTree) and are intentionally
  // not counted here, so the chip reflects what the user would actually
  // need to gather in Minecraft to build the figure.
  window._lastBlockCount = voxels.length;

  voxelGroup3D = new THREE.Group();
  const geom = new THREE.BoxGeometry(1, 1, 1);
  const cx = (Dx - 1) / 2, cy = (Dy - 1) / 2, cz = (Dz - 1) / 2;

  const ext = computeVoxelColumnExtremes(voxels, Dx, Dz);

  // Two render passes:
  //   1. Transparent voxels (glass / ice) — ALWAYS go through the merged
  //      same-material face-cull path, matching how Minecraft renders
  //      transparent blocks. The visual difference between Filled and
  //      Thin comes from the voxel set itself (full solid vs hollow
  //      shell), NOT from per-cube outlining: a filled mass of glass
  //      reads as one solid block in MC because every internal face is
  //      glass-on-glass and gets culled, while a hollow shell still
  //      shows BOTH the outer hull (glass-vs-outside-air) and the inner
  //      hull (glass-vs-interior-air) through the see-through panes.
  //   2. Everything opaque — per-voxel Mesh as before, also collected
  //      so the sand/gravel fall animation can mutate their positions.
  // All four translucent blocks go through the merged-with-same-material-
  // face-culling path. Slime and Honey additionally get a smaller opaque
  // inner core per voxel — matching real Minecraft, where the jelly cube
  // has a darker solid bead visible through the translucent skin.
  // Core sizes come straight from the vanilla block models:
  //   slime  → 10/16 = 0.625 (inner element [3,3,3]..[13,13,13])
  //   honey  → 14/16 = 0.875 (inner element [1,1,1]..[15,15,15])
  const transparentKeys = TRANSPARENT_BLOCKS;
  const coreKeys = new Set(['slime', 'honey']);
  const transparentVoxels = new Map();   // key → voxels[]
  const meshes = [];
  const slimeCoreGeom = new THREE.BoxGeometry(0.625, 0.625, 0.625);
  const honeyCoreGeom = new THREE.BoxGeometry(0.875, 0.875, 0.875);
  for (let i = 0; i < voxels.length; i++){
    const v = voxels[i];
    const blockKey = pickBlockForVoxel(v, ext, Dz);
    if (transparentKeys.has(blockKey)){
      if (!transparentVoxels.has(blockKey)) transparentVoxels.set(blockKey, []);
      transparentVoxels.get(blockKey).push(v);
      if (coreKeys.has(blockKey)){
        const coreGeom = blockKey === 'slime' ? slimeCoreGeom : honeyCoreGeom;
        const core = new THREE.Mesh(coreGeom, getInnerCoreMaterial3D(blockKey));
        core.position.set(v.x - cx, v.y - cy, v.z - cz);
        voxelGroup3D.add(core);
      }
      continue;
    }
    const mat = getMaterial3D(blockKey);
    const mesh = new THREE.Mesh(geom, mat);
    mesh.position.set(v.x - cx, v.y - cy, v.z - cz);
    voxelGroup3D.add(mesh);
    meshes.push(mesh);
  }
  transparentVoxels.forEach((vs, key) => {
    const m = buildTransparentMesh(vs, key, cx, cy, cz);
    if (m) voxelGroup3D.add(m);
  });
  if (FALL3D_BLOCKS.has(state.mcBlock)){
    _fall3DStart(voxels, meshes, 'mesh');
    _fall3DRaf = requestAnimationFrame(() => _fall3DTick(cx, cy, cz));
  }

  _lastVoxels3D = voxels;
  _lastDims3D   = { cx, cy, cz };

  // Easter egg: slider value 15 → small oak tree on top of the figure.
  buildEasterEggTree(Dx, Dy, Dz, cx, cy, cz, geom);
  // Easter egg: TNT block + slider value 15 → real creeper on top.
  buildEasterEggCreeper(Dx, Dy, Dz, cx, cy, cz);

  if (effectiveEdges3D()){
    voxelEdges3D = buildVoxelEdges3D(voxels, cx, cy, cz);
    voxelGroup3D.add(voxelEdges3D);
  }

  scene3D.add(voxelGroup3D);
  if (state.center) buildCenterCross3D(Dx, Dy, Dz);
  scheduleRender3D();
}

/* Add or remove the edges overlay without rebuilding the voxel mesh, so
   the Grid button doesn't restart an in-progress sand/gravel fall. */
function toggleEdges3D(){
  if (!_frame3DReady || !_lastVoxels3D || !voxelGroup3D) return;
  if (voxelEdges3D){
    voxelGroup3D.remove(voxelEdges3D);
    voxelEdges3D.geometry?.dispose?.();
    voxelEdges3D.material?.dispose?.();
    voxelEdges3D = null;
  }
  if (effectiveEdges3D()){
    const { cx, cy, cz } = _lastDims3D;
    voxelEdges3D = buildVoxelEdges3D(_lastVoxels3D, cx, cy, cz);
    voxelGroup3D.add(voxelEdges3D);
  }
  scheduleRender3D();
}

function scheduleRender3D(){
  if (_animPending || !_frame3DReady) return;
  _animPending = true;
  requestAnimationFrame(() => {
    _animPending = false;
    if (renderer3D && scene3D && camera3D) renderer3D.render(scene3D, camera3D);
  });
}

function resize3D(){
  if (!_frame3DReady || !renderer3D || !camera3D) return;
  const canvas = renderer3D.domElement;
  const rect = canvas.parentElement.getBoundingClientRect();
  const w = Math.max(1, Math.floor(rect.width));
  const h = Math.max(1, Math.floor(rect.height));
  renderer3D.setSize(w, h, false);
  camera3D.aspect = w / h;
  camera3D.updateProjectionMatrix();
  scheduleRender3D();
}

function destroy3D(){
  disposeVoxelGroup();
  _matCache.forEach(m => m.dispose()); _matCache.clear();
  _texCache.forEach(t => t.dispose()); _texCache.clear();
  _wireMat?.dispose?.(); _wireMat = null;
  renderer3D?.dispose?.();
  renderer3D = null; scene3D = null; camera3D = null;
  _frame3DReady = false;
}
