/* =============================================================================
   Block Round — js/audio.js
   All Rights Reserved.

   MC-flavoured sound palette. Noise bursts with aggressive lowpass produce
   the "block-place" thud; low sines fill in. Synthesized at runtime via
   WebAudio — no external audio assets, no sampling from Minecraft.
   ============================================================================ */

const Sfx = (() => {
  let ctx = null;
  let on  = true;
  // Decoded sample cache (key -> AudioBuffer) plus the currently-playing
  // long sample's source node so we can stop it on demand. Used by the TNT
  // fuse easter egg, which must cut off the moment the user picks another
  // tile instead of letting the 1.5 s+ fuse play to completion.
  const _sampleBuffers = new Map();
  let _tntSource = null;

  function ensure(){
    if (ctx) return ctx;
    try { ctx = new (window.AudioContext || window.webkitAudioContext)(); }
    catch(_) { ctx = null; }
    return ctx;
  }

  function loadSample(key, dataUri){
    if (_sampleBuffers.has(key)) return Promise.resolve(_sampleBuffers.get(key));
    const c = ensure(); if (!c) return Promise.reject();
    return fetch(dataUri)
      .then(r => r.arrayBuffer())
      .then(buf => c.decodeAudioData(buf))
      .then(decoded => { _sampleBuffers.set(key, decoded); return decoded; });
  }

  function tone({freq=600, dur=.06, type='sine', gain=.025} = {}){
    if (!on) return;
    const c = ensure(); if (!c) return;
    const o = c.createOscillator();
    const g = c.createGain();
    o.type = type;
    o.frequency.value = freq;
    g.gain.value = gain;
    g.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + dur);
    o.connect(g); g.connect(c.destination);
    o.start();
    o.stop(c.currentTime + dur);
  }

  function noiseBurst({dur=.05, gain=.035, lowpass=900} = {}){
    if (!on) return;
    const c = ensure(); if (!c) return;
    const len = Math.floor(c.sampleRate * dur);
    const buf = c.createBuffer(1, len, c.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = (Math.random()*2 - 1) * Math.exp(-i/len * 5);
    const src = c.createBufferSource(); src.buffer = buf;
    const lp = c.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = lowpass;
    const g = c.createGain(); g.gain.value = gain;
    src.connect(lp); lp.connect(g); g.connect(c.destination);
    src.start();
    src.stop(c.currentTime + dur);
  }

  return {
    setEnabled(v){ on = !!v; },
    isEnabled(){ return on; },
    loadPref(){ /* session-only — no persistence */ },

    click:  () => noiseBurst({dur:.045, gain:.035, lowpass:900}),
    hover:  () => tone({freq:240, dur:.02, gain:.012}),
    open:   () => { noiseBurst({dur:.035, gain:.028, lowpass:700}); setTimeout(() => tone({freq:220, dur:.06, gain:.028}), 35); },
    close:  () => { tone({freq:220, dur:.06, gain:.028}); setTimeout(() => noiseBurst({dur:.035, gain:.025, lowpass:600}), 55); },
    ok:     () => { tone({freq:380, dur:.07, gain:.03}); setTimeout(() => tone({freq:560, dur:.09, gain:.028}), 55); },
    error:  () => tone({freq:120, dur:.20, gain:.04}),
    pop:    () => noiseBurst({dur:.05, gain:.04, lowpass:1400}),
    tick:   () => tone({freq:480, dur:.018, gain:.012}),
    // Easter egg — plays the real Minecraft TNT fuse sample
    // (random/fuse.ogg) embedded as a data URI by js/sounds.js. The sample
    // is decoded once on first use and cached. Calling stopTnt() (e.g. on
    // block change) cuts the playback off immediately, so the fuse can't
    // out-last the user's attention span.
    tnt: () => {
      if (!on) return;
      // Free pack: synthesise a fuse hiss with filtered noise + pitch sweep.
      if (window.ASSET_PACK === 'free'){
        const c = ensure(); if (!c) return;
        try { _tntSource && _tntSource.stop(); } catch(_) {}
        const dur = 3.5;
        const len = Math.floor(c.sampleRate * dur);
        const buf = c.createBuffer(1, len, c.sampleRate);
        const d = buf.getChannelData(0);
        for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.exp(-i / len * 1.2);
        const src2 = c.createBufferSource(); src2.buffer = buf;
        const lp = c.createBiquadFilter(); lp.type = 'bandpass';
        lp.frequency.setValueAtTime(900, c.currentTime);
        lp.frequency.linearRampToValueAtTime(300, c.currentTime + dur);
        lp.Q.value = 0.8;
        const g2 = c.createGain(); g2.gain.value = 0.45;
        src2.connect(lp); lp.connect(g2); g2.connect(c.destination);
        src2.onended = () => { if (_tntSource === src2) _tntSource = null; };
        _tntSource = src2;
        src2.start();
        return;
      }
      const c = ensure(); if (!c) return;
      const src = window.MC_SFX && window.MC_SFX.tnt_fuse;
      if (!src) return;
      loadSample('tnt_fuse', src).then(buffer => {
        if (!on) return;  // user disabled audio during the decode
        // Stop any previous fuse so re-clicks don't stack.
        try { _tntSource && _tntSource.stop(); } catch(_) {}
        const node = c.createBufferSource();
        node.buffer = buffer;
        const g = c.createGain();
        g.gain.value = 0.55;
        node.connect(g); g.connect(c.destination);
        node.onended = () => { if (_tntSource === node) _tntSource = null; };
        _tntSource = node;
        node.start();
      }).catch(() => {});
    },
    stopTnt: () => {
      if (!_tntSource) return;
      try { _tntSource.stop(); } catch(_) {}
      _tntSource = null;
    },
    // Easter egg — plays the real vanilla slime jump sound when the
    // user picks the Slime Block tile. Short squelchy boing, ~0.5 s.
    // Honey reuses this sample since MC's actual honey-block "bounce"
    // sound is just a re-pitched slime jump anyway.
    slime: () => {
      if (!on) return;
      // Free pack: synthesise a springy boing (pitch-descending tone burst).
      if (window.ASSET_PACK === 'free'){
        const c = ensure(); if (!c) return;
        const o = c.createOscillator();
        const g2 = c.createGain();
        o.type = 'sine';
        o.frequency.setValueAtTime(520, c.currentTime);
        o.frequency.exponentialRampToValueAtTime(80, c.currentTime + 0.45);
        g2.gain.setValueAtTime(0.35, c.currentTime);
        g2.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + 0.5);
        o.connect(g2); g2.connect(c.destination);
        o.start(); o.stop(c.currentTime + 0.5);
        return;
      }
      const c = ensure(); if (!c) return;
      const src = window.MC_SFX && window.MC_SFX.slime_jump;
      if (!src) return;
      loadSample('slime_jump', src).then(buffer => {
        if (!on) return;
        const node = c.createBufferSource();
        node.buffer = buffer;
        const g = c.createGain();
        g.gain.value = 0.7;
        node.connect(g); g.connect(c.destination);
        node.start();
      }).catch(() => {});
    },
    // Per-category MC place sound. category ∈ {stone, wood, grass, gravel,
    // sand, cloth, glass, snow}. Plays the vanilla dig sample so each
    // block category gets its own distinct picker-click thunk.
    place: (category) => {
      if (!on) return;
      const c = ensure(); if (!c) return;
      const key = 'place_' + category;
      const src = window.MC_SFX && window.MC_SFX[key];
      if (!src) return;
      loadSample(key, src).then(buffer => {
        if (!on) return;
        const node = c.createBufferSource();
        node.buffer = buffer;
        const g = c.createGain();
        g.gain.value = 0.55;
        node.connect(g); g.connect(c.destination);
        node.start();
      }).catch(() => {});
    },
  };
})();
