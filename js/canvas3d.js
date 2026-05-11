/* =============================================================================
   Block Round — js/canvas3d.js
   All Rights Reserved on code. MC textures are Mojang property.

   Three.js voxel renderer using real MC block textures (base64 data URIs
   from textures.js → MC_TEX[key], piped through THREE.TextureLoader).

   Render mode (state.render) chooses which voxels are emitted via the
   shared voxelShell(). state.edges3d (toggled by the canvas Grid button,
   ON by default in 3D) overlays black line segments tracing the 12
   edges of every voxel — this replaces the old "wireframe" style.

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
  const b = MC_BLOCKS[key];
  if (!b || !b.src) return null;
  const tex = new THREE.TextureLoader().load(b.src, (t) => {
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
/* Returns either a single material or an array of six materials so a single
   BoxGeometry can use distinct textures per face. The face order Three.js
   expects is [+X, -X, +Y, -Y, +Z, -Z] — i.e. right, left, top, bottom,
   front, back. Multi-face blocks (grass, oak_log, …) plus alpha blocks
   (glass, ice) get their own cached entries. */
function getMaterial3D(key){
  if (_matCache.has(key)) return _matCache.get(key);

  // Grass block: green on top, dirt on bottom, mossy side on the four sides
  if (key === 'grass'){
    const top    = new THREE.MeshLambertMaterial({ map: getTexture3D('grass') });
    const side   = new THREE.MeshLambertMaterial({ map: getTexture3D('grass_side') });
    const bottom = new THREE.MeshLambertMaterial({ map: getTexture3D('dirt') });
    const mats = [side, side, top, bottom, side, side];
    _matCache.set(key, mats);
    return mats;
  }

  // Oak log: bark on the 4 sides, end-grain on top & bottom
  if (key === 'oak_log'){
    const side = new THREE.MeshLambertMaterial({ map: getTexture3D('oak_log') });
    const end  = new THREE.MeshLambertMaterial({ map: getTexture3D('oak_log_top') });
    const mats = [side, side, end, end, side, side];
    _matCache.set(key, mats);
    return mats;
  }

  // Alpha-channel blocks: keep transparency so panes/cracks show through.
  if (key === 'glass' || key === 'ice'){
    const tex = getTexture3D(key);
    const mat = new THREE.MeshLambertMaterial({
      map: tex, transparent: true, alphaTest: 0.5, depthWrite: true,
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

function updateCamera3D(){
  if (!camera3D) return;
  camera3D.position.x = distance3D * Math.sin(phi3D) * Math.cos(theta3D);
  camera3D.position.y = distance3D * Math.cos(phi3D);
  camera3D.position.z = distance3D * Math.sin(phi3D) * Math.sin(theta3D);
  camera3D.lookAt(0, 0, 0);
  scheduleRender3D();
}
function resetCamera3D(){ theta3D = Math.PI / 4; phi3D = Math.PI / 3; autoZoom3D(); }
/* Fit the figure's bounding sphere into the camera frustum with a small
   margin. The bounding-sphere radius is half the box-diagonal; needed
   distance is R / sin(fov/2). Use the more-constrained of vertical and
   horizontal FOV so wide aspect-ratio frames don't crop tall ellipsoids. */
function autoZoom3D(){
  if (!camera3D) return;
  const isEllipse = state.shape === 'ellipse';
  const Dx = isEllipse ? state.width : state.size;
  const Dy = isEllipse ? state.height : state.size;
  const Dz = isEllipse ? state.depth : state.size;

  const R = 0.5 * Math.sqrt(Dx*Dx + Dy*Dy + Dz*Dz);
  const vFov = camera3D.fov * Math.PI / 180;
  const hFov = 2 * Math.atan(Math.tan(vFov / 2) * camera3D.aspect);
  const distV = R / Math.sin(vFov / 2);
  const distH = R / Math.sin(hFov / 2);
  // No artificial floor — small ellipsoids should let the camera get
  // genuinely close so the figure fills the frame proportionally.
  distance3D = Math.max(2, Math.max(distV, distH) * 1.10);
  updateCamera3D();
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
  const mat = new THREE.LineBasicMaterial({
    color: 0x1a0e04, transparent: true, opacity: 0.55,
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
  disposeVoxelGroup();
  disposeCenterCross();
  _fall3DReset();

  const isEllipse = state.shape === 'ellipse';
  const Dx = isEllipse ? state.width     : state.size;
  const Dy = isEllipse ? state.height     : state.size;
  const Dz = isEllipse ? state.depth : state.size;

  const maxAxis = state.axis === 'x' ? Dx : Dy;
  const cutLimit = state.cut < maxAxis ? state.cut : maxAxis + 1;
  const voxels = voxelShell(Dx, Dy, Dz, state.render, state.axis, cutLimit);
  if (voxels.length === 0){ scheduleRender3D(); return; }

  voxelGroup3D = new THREE.Group();
  const geom = new THREE.BoxGeometry(1, 1, 1);
  const cx = (Dx - 1) / 2, cy = (Dy - 1) / 2, cz = (Dz - 1) / 2;

  // Per-voxel mesh with the block's textured material. Wireframe is no
  // longer a render style — the Grid corner button toggles the
  // edges-overlay LineSegments below.
  const ext = computeVoxelColumnExtremes(voxels, Dx, Dz);
  const meshes = [];
  for (let i = 0; i < voxels.length; i++){
    const v = voxels[i];
    const mat = getMaterial3D(pickBlockForVoxel(v, ext, Dz));
    const mesh = new THREE.Mesh(geom, mat);
    mesh.position.set(v.x - cx, v.y - cy, v.z - cz);
    voxelGroup3D.add(mesh);
    meshes.push(mesh);
  }
  if (FALL3D_BLOCKS.has(state.mcBlock)){
    _fall3DStart(voxels, meshes, 'mesh');
    _fall3DRaf = requestAnimationFrame(() => _fall3DTick(cx, cy, cz));
  }

  _lastVoxels3D = voxels;
  _lastDims3D   = { cx, cy, cz };

  if (state.edges3d){
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
  if (state.edges3d){
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
