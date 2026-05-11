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

  function ensure(){
    if (ctx) return ctx;
    try { ctx = new (window.AudioContext || window.webkitAudioContext)(); }
    catch(_) { ctx = null; }
    return ctx;
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
    // Easter egg — TNT fuse hiss + crackle. Layered short noise bursts
    // with rising lowpass create the sizzling sound of a freshly-lit
    // fuse, ramping in over ~1.4 s. Fired the moment the user picks the
    // TNT tile in the block list.
    tnt: () => {
      if (!on) return;
      const c = ensure(); if (!c) return;
      // Hiss bed: filtered white noise rising in cutoff.
      const len = Math.floor(c.sampleRate * 1.4);
      const buf = c.createBuffer(1, len, c.sampleRate);
      const d = buf.getChannelData(0);
      for (let i = 0; i < len; i++) d[i] = (Math.random()*2 - 1);
      const src = c.createBufferSource(); src.buffer = buf;
      const lp = c.createBiquadFilter(); lp.type = 'bandpass';
      lp.frequency.setValueAtTime(900, c.currentTime);
      lp.frequency.exponentialRampToValueAtTime(2400, c.currentTime + 1.4);
      lp.Q.value = 1.4;
      const g = c.createGain();
      g.gain.setValueAtTime(0.025, c.currentTime);
      g.gain.exponentialRampToValueAtTime(0.055, c.currentTime + 1.2);
      g.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + 1.4);
      src.connect(lp); lp.connect(g); g.connect(c.destination);
      src.start(); src.stop(c.currentTime + 1.4);
      // Crackle taps — irregular short noise pops layered on top.
      const taps = [80, 180, 310, 470, 640, 820, 1000, 1190];
      for (const ms of taps){
        setTimeout(() => noiseBurst({ dur: .035, gain: .025, lowpass: 2200 }), ms);
      }
    },
  };
})();
