/* =============================================================================
   Block Round — service-worker.js
   All Rights Reserved on code.

   Offline-first service worker. Caches the app shell plus the MC block
   textures referenced by the picker. Bumping CACHE invalidates everything
   on next activation. Texture files are big-ish collectively (~66 PNGs);
   we ship them lazily via the runtime fetch handler (cache-on-fetch) to
   keep the install step small.
   ============================================================================ */
const CACHE = 'block-round-v1';
const SHELL = [
  './',
  './index.html',
  './style.css',
  './manifest.json',
  './favicon.svg',
  './js/state.js',
  './js/algorithms.js',
  './js/audio.js',
  './js/canvas2d.js',
  './js/canvas3d.js',
  './js/ui.js',
  './js/main.js',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
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
