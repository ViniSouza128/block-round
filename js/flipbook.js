/* =============================================================================
   Block Round — js/flipbook.js
   All Rights Reserved on code. MC textures are Mojang property.

   Bedrock-style flipbook animation for vertical texture strips.

   Several Mojang block textures ship as a vertical stack of 16x16 frames
   (height = N * width). Bedrock's `flipbook_textures.json` advances them
   on the world tick (50 ms = 1 game tick); we mirror those canonical
   defaults here so magma pulses, sea_lantern shimmers and prismarine
   ripples on screen instead of being frozen on frame 0.

     • magma            — 16x48,  3 frames, 10 ticks/frame (500 ms)
     • sea_lantern      — 16x80,  5 frames,  5 ticks/frame (250 ms)
     • prismarine_rough — 16x64,  4 frames, custom 22-step sequence

   The module exposes three pieces:
     1. window.MC_FLIPBOOK         — per-key timing + frame-order metadata
                                      (matches bedrock-samples canon).
     2. window.flipbookFrameCount  — derive N from a loaded HTMLImageElement.
     3. window.flipbookCurrentFrame — int frame index at a given epoch.
     4. window.registerFlipbook     — subscribe an apply(frameIdx) callback;
                                      the global rAF ticker calls it only
                                      when the integer frame index changes.

   Renderers wire in like this:
     • canvas2d.js — drawBlockImage() blits frame i via a sub-rect
                     ctx.drawImage(img, 0, i*16, 16, 16, ...). draw2D
                     subscribes once for each animated MC_BLOCKS key and
                     calls redraw() on change, gated by state.mode === '2d'.
     • canvas3d.js — getTexture3D() sets repeat.y = 1/N once on load, then
                     subscribes a callback that updates offset.y per frame
                     and calls scheduleRender3D(). flipY:true on THREE
                     textures inverts row order, so frame 0 (top of PNG)
                     lives at offset.y = (N-1)/N.

   To add a new animated block:
     • Drop a tall PNG into js/textures.js (16x{16*N}).
     • Add an MC_FLIPBOOK entry below if you want non-default timing.
     • If the picker key differs from the MC_TEX key, alias it in
       MC_FLIPBOOK_ALIASES so the 2D path can resolve picker→texture.
   ============================================================================ */

window.MC_TICK_MS = 50;

/* Canonical Bedrock timings from
   github.com/Mojang/bedrock-samples → resource_pack/textures/flipbook_textures.json
   Keys mirror MC_TEX entries (so they apply directly in the 3D path).
   `ticks_per_frame` defaults to 8 if omitted; `frames` is an optional
   non-linear sequence (used by prismarine_rough — the classic 22-step
   ripple that flickers back through frame 0).

   All three match the in-game Bedrock animation exactly:
     • magma            — 10 ticks/frame  ( 500 ms ) ×  3 frames =  1.5 s loop
     • sea_lantern      —  5 ticks/frame  ( 250 ms ) ×  5 frames =  1.25 s loop
     • prismarine_rough — 300 ticks/frame (15.0 s ) × 22-step seq = 5.5 min loop

   Prismarine looks "frozen" most of the time — that's the actual game
   behaviour. The flicker is meant to be a subtle surprise, not an
   obvious animation. */
window.MC_FLIPBOOK = {
  magma:            { ticks_per_frame: 10 },
  sea_lantern:      { ticks_per_frame: 5  },
  prismarine_rough: {
    ticks_per_frame: 300,
    frames: [0, 1, 0, 2, 0, 3, 0, 1, 2, 1, 3, 1, 0, 2, 1, 2, 3, 2, 0, 3, 1, 3],
  },
};

/* MC_BLOCKS keys can differ from their underlying MC_TEX key (e.g. the
   picker shows "Prismarine" → tex `prismarine_rough`). The 2D path looks
   up flipbook config by picker key, so we map any mismatched pairs here. */
window.MC_FLIPBOOK_ALIASES = {
  prismarine: 'prismarine_rough',
};

function _resolveFlipbookKey(key){
  if (!key) return null;
  if (window.MC_FLIPBOOK[key]) return key;
  const alias = window.MC_FLIPBOOK_ALIASES[key];
  if (alias && window.MC_FLIPBOOK[alias]) return alias;
  return null;
}
window.resolveFlipbookKey = _resolveFlipbookKey;

/* Returns the number of vertically-stacked 16x16 frames in `img`, or 1
   when the image isn't a flipbook strip. Requires the image to already
   be loaded (naturalWidth > 0). */
window.flipbookFrameCount = function(img){
  if (!img || !img.naturalWidth || !img.naturalHeight) return 1;
  const w = img.naturalWidth, h = img.naturalHeight;
  if (h <= w) return 1;
  const ratio = h / w;
  const N = Math.round(ratio);
  if (Math.abs(ratio - N) > 0.01) return 1;
  return Math.max(1, N);
};

/* Frame index for `key` at epoch `nowMs`. Honours custom `frames`
   sequences and clamps to the actual frame count of the loaded image. */
window.flipbookCurrentFrame = function(key, frameCount, nowMs){
  if (frameCount <= 1) return 0;
  const cfg = (key && window.MC_FLIPBOOK[key]) || null;
  const ticks = (cfg && cfg.ticks_per_frame) || 8;
  const periodMs = ticks * window.MC_TICK_MS;
  const step = Math.floor(nowMs / periodMs);
  if (cfg && Array.isArray(cfg.frames) && cfg.frames.length){
    const raw = cfg.frames[step % cfg.frames.length] | 0;
    return Math.min(Math.max(0, raw), frameCount - 1);
  }
  return step % frameCount;
};

/* Single shared rAF ticker. Subscribers fire only when their integer frame
   index changes — so a sea_lantern callback runs 4x/s, not 60x/s. The
   ticker idles itself once the subscriber set is empty. */
(function setupFlipbookTicker(){
  const subs = new Set();
  let raf = null;

  function tick(){
    raf = null;
    const now = performance.now();
    subs.forEach(s => {
      const next = window.flipbookCurrentFrame(s.key, s.frameCount, now);
      if (next !== s.lastIdx){
        s.lastIdx = next;
        try { s.apply(next); } catch(_) {}
      }
    });
    if (subs.size > 0) raf = requestAnimationFrame(tick);
  }

  /* Register a flipbook subscriber.
     - `key`        : MC_FLIPBOOK key (or any value; falls back to default timing).
     - `frameCount` : N derived from the image; skip if N <= 1.
     - `apply(idx)` : invoked once immediately with the current frame and
                      again on every frame change.
     Returns an unregister function. */
  window.registerFlipbook = function(key, frameCount, apply){
    if (frameCount <= 1 || typeof apply !== 'function') return () => {};
    const now = performance.now();
    const idx0 = window.flipbookCurrentFrame(key, frameCount, now);
    const s = { key, frameCount, apply, lastIdx: idx0 };
    apply(idx0);
    subs.add(s);
    if (raf == null) raf = requestAnimationFrame(tick);
    return () => subs.delete(s);
  };
})();
