/* =============================================================================
   Block Round — service-worker.js
   All Rights Reserved on code.

   Offline-first service worker. Caches the app shell plus the MC block
   textures referenced by the picker. Bumping CACHE invalidates everything
   on next activation. Texture files are big-ish collectively (~66 PNGs);
   we ship them lazily via the runtime fetch handler (cache-on-fetch) to
   keep the install step small.
   ============================================================================ */
/* Bump CACHE whenever any SHELL file changes. The activate handler deletes
   stale caches on the next visit, so a single-character bump here is what
   ships fixes to repeat visitors. */
const CACHE = 'block-round-v9';
const SHELL = [
  './',
  './index.html',
  './style.css',
  './manifest.json',
  './favicon.svg',
  './js/flipbook.js',
  './js/i18n.js',
  './js/state.js',
  './js/algorithms.js',
  './js/audio.js',
  './js/canvas2d.js',
  './js/canvas3d.js',
  './js/schematic.js',
  './js/sounds.js',
  './js/textures.js',
  './js/ui.js',
  './js/main.js',
];

self.addEventListener('install', e => {
  /* Fetch each shell URL with `cache: 'reload'` so the install step
     bypasses the browser HTTP cache. Without this, bumping CACHE only
     replaces the cache map; the same stale files come back via the
     browser's disk cache (Python http.server ETags), and bumps become
     no-ops until the user hard-refreshes. */
  e.waitUntil(
    caches.open(CACHE).then(c =>
      Promise.all(SHELL.map(url =>
        fetch(new Request(url, { cache: 'reload' })).then(res => c.put(url, res))
      ))
    ).then(() => self.skipWaiting())
  );
});
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith((async () => {
    const cached = await caches.match(e.request);
    if (cached) return cached;
    try {
      const res = await fetch(e.request);
      // Cache PNG textures lazily so subsequent loads are offline-safe.
      if (res.ok && /\.png$/i.test(new URL(e.request.url).pathname)){
        const cache = await caches.open(CACHE);
        cache.put(e.request, res.clone());
      }
      return res;
    } catch(_){
      return cached || Response.error();
    }
  })());
});
