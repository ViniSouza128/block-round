/* =============================================================================
   Block Round — js/i18n.js
   All Rights Reserved.

   Minimal i18n: two locales (en / pt), data-i18n attribute walker, and a
   t() helper for strings generated in JS (toasts, dynamic labels).

   Usage
     • HTML:  <span data-i18n="key">fallback</span>
              <button data-i18n-title="key" title="fallback">
     • JS:    toast(t('grid_on'))
     • Init:  setLocale('en')  or  setLocale('pt')
   ============================================================================ */

(function(){

/* ---------- TRANSLATION TABLE --------------------------------------------- */
const _TR = {
  en: {
    /* topbar */
    lang_toggle_title: 'Switch to Portuguese (PT)',
    sound_title: 'Toggle sound (S)',
    theme_title: 'Toggle day / night (T)',
    info_title:  'Info',
    settings_title: 'Settings',

    /* mode / shape buttons */
    mode_2d: '2D', mode_3d: '3D',
    shape_circle:    'Circle',
    shape_ellipse:   'Ellipse',
    shape_sphere:    'Sphere',
    shape_ellipsoid: 'Ellipsoid',

    /* render pills */
    render_filled: 'Filled',
    render_thin:   'Thin',
    render_thick:  'Thick',

    /* algo pills */
    algo_euclidean: 'Euclidean',
    algo_bresenham: 'Bresenham',
    algo_threshold: 'Threshold',

    /* slider labels */
    lbl_size:   'Size',
    lbl_width:  'Width',
    lbl_height: 'Height',
    lbl_depth:  'Depth',
    lbl_cut:    'Cut',

    /* canvas corner button titles */
    title_grid:     'Grid / Wireframe (G)',
    title_download: 'Download PNG (D)',
    title_schem:    'Export Minecraft schematic (.schem)',
    title_center:   'Center guides (C)',
    title_overlay:  'Perfect overlay',
    title_zoom:     'Zoom top-left quadrant',
    title_infochip: 'Info chip (I)',

    /* info chip labels */
    chip_d:      'D',
    chip_r:      'R',
    chip_vol:    'Vol',
    chip_blocks: 'Blocks',
    chip_block:  'Block',

    /* cut-axis titles */
    title_cut_x:    'Cut along X axis',
    title_cut_y:    'Cut along Y axis',
    title_cut_diag: 'Diagonal 45° cut (x+y plane)',

    /* toasts */
    night_on:   'Night on',
    night_off:  'Night off',
    sounds_on:  'Sounds on',
    sounds_off: 'Sounds off',
    grid_on:    'Grid on',
    grid_off:   'Grid off',
    edges_on:   'Edges on',
    edges_off:  'Edges off',
    reset:      'Reset',
    undo:       'Undo',
    redo:       'Redo',
    png_saved:  'PNG saved',

    /* settings page */
    settings_h2:          'Settings',
    settings_sub:         'Session-only — every reload starts at the defaults.',
    setting_sounds_lbl:   'Sounds',
    setting_sounds_desc:  'Sound feedback on interactions',
    setting_grid_lbl:     'Canvas grid',
    setting_grid_desc:    'Background helper lines (full canvas)',
    setting_center_lbl:   'Center guides',
    setting_center_desc:  'X/Y lines through the figure center',
    setting_reset_lbl:    'Reset',
    setting_reset_desc:   'Restore all settings to defaults',
    btn_reset:            'Reset',
  },

  pt: {
    /* topbar */
    lang_toggle_title: 'Mudar para inglês (EN)',
    sound_title: 'Alternar som (S)',
    theme_title: 'Alternar dia / noite (T)',
    info_title:  'Informações',
    settings_title: 'Configurações',

    /* mode / shape buttons */
    mode_2d: '2D', mode_3d: '3D',
    shape_circle:    'Círculo',
    shape_ellipse:   'Elipse',
    shape_sphere:    'Esfera',
    shape_ellipsoid: 'Elipsoide',

    /* render pills */
    render_filled: 'Preenchido',
    render_thin:   'Fino',
    render_thick:  'Grosso',

    /* algo pills */
    algo_euclidean: 'Euclidiano',
    algo_bresenham: 'Bresenham',
    algo_threshold: 'Limiar',

    /* slider labels */
    lbl_size:   'Tamanho',
    lbl_width:  'Largura',
    lbl_height: 'Altura',
    lbl_depth:  'Profundidade',
    lbl_cut:    'Corte',

    /* canvas corner button titles */
    title_grid:     'Grade / Wireframe (G)',
    title_download: 'Baixar PNG (D)',
    title_schem:    'Exportar esquemático Minecraft (.schem)',
    title_center:   'Guias de centro (C)',
    title_overlay:  'Sobreposição perfeita',
    title_zoom:     'Zoom no quadrante superior esquerdo',
    title_infochip: 'Chip de informações (I)',

    /* info chip labels */
    chip_d:      'D',
    chip_r:      'R',
    chip_vol:    'Vol',
    chip_blocks: 'Blocos',
    chip_block:  'Bloco',

    /* cut-axis titles */
    title_cut_x:    'Cortar ao longo do eixo X',
    title_cut_y:    'Cortar ao longo do eixo Y',
    title_cut_diag: 'Corte diagonal 45° (plano x+y)',

    /* toasts */
    night_on:   'Noite ativada',
    night_off:  'Noite desativada',
    sounds_on:  'Sons ativados',
    sounds_off: 'Sons desativados',
    grid_on:    'Grade ativada',
    grid_off:   'Grade desativada',
    edges_on:   'Arestas ativadas',
    edges_off:  'Arestas desativadas',
    reset:      'Reiniciar',
    undo:       'Desfazer',
    redo:       'Refazer',
    png_saved:  'PNG salvo',

    /* settings page */
    settings_h2:          'Configurações',
    settings_sub:         'Apenas para esta sessão — cada recarga volta ao padrão.',
    setting_sounds_lbl:   'Sons',
    setting_sounds_desc:  'Feedback sonoro nas interações',
    setting_grid_lbl:     'Grade do canvas',
    setting_grid_desc:    'Linhas auxiliares de fundo (canvas completo)',
    setting_center_lbl:   'Guias de centro',
    setting_center_desc:  'Linhas X/Y pelo centro da figura',
    setting_reset_lbl:    'Reiniciar',
    setting_reset_desc:   'Restaurar todas as configurações ao padrão',
    btn_reset:            'Reiniciar',
  },
};

/* ---------- STATE ---------------------------------------------------------- */
let _locale = (navigator.language || 'en').startsWith('pt') ? 'pt' : 'en';

/* ---------- PUBLIC API ----------------------------------------------------- */
window.t = function(key){
  return (_TR[_locale] && _TR[_locale][key]) || (_TR.en[key]) || key;
};

window.setLocale = function(lang){
  _locale = (lang === 'pt') ? 'pt' : 'en';
  _applyLocale();
  _syncLangBtn();
  /* Re-run shape button labels, which are generated dynamically in ui.js */
  if (typeof syncShape === 'function') syncShape();
};

window.getLocale = function(){ return _locale; };

/* ---------- DOM WALKER ----------------------------------------------------- */
function _applyLocale(){
  /* textContent targets */
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    const v = t(key);
    if (v) el.textContent = v;
  });
  /* title / aria-label targets */
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.dataset.i18nTitle;
    const v = t(key);
    if (v) el.title = v;
  });
}

function _syncLangBtn(){
  const btn = document.querySelector('[data-act=lang]');
  if (!btn) return;
  /* swap label text */
  const lbl = btn.querySelector('[data-i18n=lang_label]');
  if (lbl) lbl.textContent = _locale === 'pt' ? 'EN' : 'PT';
  btn.title = t('lang_toggle_title');
}

/* ---------- SHAPE LABELS (locale-aware) ------------------------------------ */
/* Overrides SHAPE_LABELS in state.js so syncShape() in ui.js picks up
   translated names without needing changes in that file. */
function _patchShapeLabels(){
  if (typeof window.SHAPE_LABELS === 'undefined') return;
  window.SHAPE_LABELS.circle['2d']  = t('shape_circle');
  window.SHAPE_LABELS.circle['3d']  = t('shape_sphere');
  window.SHAPE_LABELS.ellipse['2d'] = t('shape_ellipse');
  window.SHAPE_LABELS.ellipse['3d'] = t('shape_ellipsoid');
}

/* ---------- INIT ----------------------------------------------------------- */
/* Run once after DOM is ready (DOMContentLoaded or equivalent). */
window.initI18N = function(){
  _patchShapeLabels();
  _applyLocale();
  _syncLangBtn();
};

})();
