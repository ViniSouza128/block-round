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
     • magma / sea_lantern (animated vertical sprite strips) → texture
                       cropped to the top frame via tex.offset/repeat.
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

/* Effective edge-overlay preference. Transparent blocks (glass / ice)
   read state.edges3dTransparent (default OFF — the outlines compete
   with the alpha rendering); everything else reads state.edges3d. */
function effectiveEdges3D(){
  if (state.mcBlock === 'glass' || state.mcBlock === 'ice'){
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
    // Animated MC textures are vertical strips of 16×16 frames.
    // Crop to the top frame so blocks don't squash vertically in 3D.
    const im = t.image;
    if (im && im.height > im.width * 1.5){
      const frac = im.width / im.height;
      t.repeat.set(1, frac);
      t.offset.set(0, 1 - frac);
      t.needsUpdate = true;
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

// Camera always orbits AND looks at the figure's effective centre. When
// the tree easter egg is active the effective centre rises (the tree
// adds extra cells above the figure), so the camera's lookAt and the
// orbit anchor both shift up by the same amount — keeping the entire
// composition framed instead of pushing the tree off the top of the
// canvas.
function _cameraLookAtY(){
  const extra = (typeof treeBoundsExtraY === 'function') ? treeBoundsExtraY() : 0;
  // Effective half-height of (figure + tree) above origin.
  return extra > 0 ? (extra / 2) : 0;
}

function updateCamera3D(){
  if (!camera3D) return;
  const ly = _cameraLookAtY();
  camera3D.position.x = distance3D * Math.sin(phi3D) * Math.cos(theta3D);
  camera3D.position.y = distance3D * Math.cos(phi3D) + ly;
  camera3D.position.z = distance3D * Math.sin(phi3D) * Math.sin(theta3D);
  camera3D.lookAt(0, ly, 0);
  scheduleRender3D();
}
function resetCamera3D(){ theta3D = Math.PI / 4; phi3D = Math.PI / 3; autoZoom3D(); }
/* autoZoom3D — set distance3D so the bounding sphere of the figure fits
   inside the viewport with a guaranteed margin at every rotation angle.
   When the tree easter egg is active, the bounding box is extended
   vertically to include the tree, so the camera pulls back AND looks
   up to keep the entire figure-plus-tree composition in frame. */
function autoZoom3D(){
  if (!camera3D) return;
  const isEllipse = state.shape === 'ellipse';
  const Dx = isEllipse ? state.width  : state.size;
  const Dy = isEllipse ? state.height : state.size;
  const Dz = isEllipse ? state.depth  : state.size;

  // Effective height grows when the tree easter egg is active. The
  // tree extends upward from the figure top, so the half-height grows
  // and the bounding sphere recenters higher (handled in lookAt).
  const treeExtra = (typeof treeBoundsExtraY === 'function') ? treeBoundsExtraY() : 0;
  const effDy = Dy + treeExtra;

  // Half-diagonal of the effective AABB = radius of the tightest sphere.
  const hx = Dx / 2, hy = effDy / 2, hz = Dz / 2;
  const R = Math.sqrt(hx * hx + hy * hy + hz * hz);

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
  if (state.axis === 'y' && state.cut < Dy) return;

  const cutXLimit = state.axis === 'x' ? state.cut : Dx;
  const treeCX = Math.floor((Dx - 1) / 2);
  const treeCZ = Math.floor((Dz - 1) / 2);
  const baseY  = Dy;  // first voxel above the topmost figure voxel

  const addBlock = (lx, ly, lz, matKey) => {
    if (lx < 0 || lx >= cutXLimit) return;
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

  const maxAxis = state.axis === 'x' ? Dx : Dy;
  const cutLimit = state.cut < maxAxis ? state.cut : maxAxis + 1;
  // Filled + transparent (Glass/Ice) is the one case where the cheap
  // "shell-only" voxel set is wrong: the user can SEE through the front
  // panes and would expect to see the dense interior of cubes behind.
  // Use the full solid volume instead. Thin/Thick still go through the
  // regular voxelShell paths so a hollow shell stays a shell.
  const isTransparentFilled =
    state.render === 'filled' && (state.mcBlock === 'glass' || state.mcBlock === 'ice');
  const voxels = isTransparentFilled
    ? voxelKeptAll(Dx, Dy, Dz, state.axis, cutLimit)
    : voxelShell(Dx, Dy, Dz, state.render, state.axis, cutLimit);
  if (voxels.length === 0){ scheduleRender3D(); return; }

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
  const transparentKeys = new Set(['glass', 'ice']);
  const transparentVoxels = new Map();   // key → voxels[]
  const meshes = [];
  for (let i = 0; i < voxels.length; i++){
    const v = voxels[i];
    const blockKey = pickBlockForVoxel(v, ext, Dz);
    if (transparentKeys.has(blockKey)){
      if (!transparentVoxels.has(blockKey)) transparentVoxels.set(blockKey, []);
      transparentVoxels.get(blockKey).push(v);
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
