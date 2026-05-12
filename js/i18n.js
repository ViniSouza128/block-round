/* =============================================================================
   Block Round — js/i18n.js
   All Rights Reserved.

   Four locales ship in this file (≈817 M native speakers combined):
     en-US  English (US)         — base / fallback for missing keys
     pt-BR  Português (Brasil)   — ~210 M speakers
     ru-RU  Русский              — ~150 M speakers
     ko-KR  한국어                — ~77 M speakers

   How to add a new locale:
     1. Add an entry to AVAILABLE_LOCALES with code (BCP-47), label, and
        the htmlLang attribute to set on <html lang>.
     2. Add a full translation block under TRANSLATIONS[code] mirroring
        the keys present in 'en-US'.
     3. Add a `name_<blockKey>` entry under blocks for every MC_BLOCKS
        catalog key (otherwise the English fallback is used).
     4. Add the locale option in the Settings select via i18n.applyLocale
        (it auto-rebuilds the picker from AVAILABLE_LOCALES).

   Architecture
     • AVAILABLE_LOCALES — declarative list of all supported locales.
     • TRANSLATIONS      — keyed by locale code; each entry is a flat key
                           map plus a structured `info` tree (rendered to
                           the Info page) and a `blocks` block-name map.
     • t(key)            — returns the current-locale string for a key
                           (English fallback, then the key itself).
     • setLocale(code)   — switches, persists to localStorage, applies
                           DOM updates, refits page metadata, rebuilds
                           the Info page and Settings language picker.
     • applyLocale()     — walks data-i18n / data-i18n-title attributes
                           and refreshes them all.
     • initI18N()        — called from main.js on DOMContentLoaded.
   ============================================================================ */

(function(){

/* ---------- LOCALE REGISTRY ----------------------------------------------- */
const AVAILABLE_LOCALES = [
  { code: 'en-US', label: 'EN-US', name: 'English (US)',       htmlLang: 'en'    },
  { code: 'pt-BR', label: 'PT-BR', name: 'Português (Brasil)', htmlLang: 'pt-BR' },
  { code: 'ru-RU', label: 'RU-RU', name: 'Русский',            htmlLang: 'ru'    },
  { code: 'ko-KR', label: 'KO-KR', name: '한국어',              htmlLang: 'ko'    },
];
const DEFAULT_LOCALE = 'en-US';
const STORAGE_KEY = 'br_locale';

/* ---------- TRANSLATION TABLES -------------------------------------------- */
/* Each locale must mirror the keys in 'en-US'. Missing keys fall back to
   English; missing English keys return the literal key (so untranslated
   strings surface visibly during development). */
const TR = {
  'en-US': {
    /* ---- meta ---- */
    doc_title:   'Block Round — pixel-perfect rounded shape generator',
    meta_desc:   'Block Round — Minecraft-flavoured pixel-perfect generator. Not affiliated with Mojang/Microsoft.',
    brand:       'Block Round',
    brand_aria:  'Block Round home',

    /* ---- topbar buttons ---- */
    lang_toggle_title: 'Change language',
    sound_title:       'Toggle sound (S)',
    theme_title:       'Toggle day / night (T)',
    info_title:        'Info',
    settings_title:    'Settings',
    brand_title:       'Block Round',

    /* ---- mode / shape buttons ---- */
    mode_2d: '2D', mode_3d: '3D',
    shape_circle:    'Circle',
    shape_ellipse:   'Ellipse',
    shape_sphere:    'Sphere',
    shape_ellipsoid: 'Ellipsoid',

    /* ---- render pills ---- */
    render_filled: 'Filled',
    render_thin:   'Thin',
    render_thick:  'Thick',

    /* ---- algo pills ---- */
    algo_euclidean: 'Euclidean',
    algo_bresenham: 'Bresenham',
    algo_threshold: 'Threshold',

    /* ---- slider labels ---- */
    lbl_size:   'Size',
    lbl_width:  'Width',
    lbl_height: 'Height',
    lbl_depth:  'Depth',
    lbl_cut:    'Cut',

    /* ---- canvas corner button titles ---- */
    title_grid:     'Grid / Wireframe (G)',
    title_download: 'Download PNG (D)',
    title_schem:    'Export Minecraft schematic (.schem)',
    title_center:   'Center guides (C)',
    title_overlay:  'Perfect overlay',
    title_zoom:     'Zoom top-left quadrant',
    title_infochip: 'Info chip (I)',

    /* ---- info chip labels ---- */
    chip_d:      'D',
    chip_r:      'R',
    chip_vol:    'Vol',
    chip_blocks: 'Blocks',
    chip_block:  'Block',

    /* ---- cut-axis titles ---- */
    title_cut_x:    'Cut along X axis',
    title_cut_y:    'Cut along Y axis',
    title_cut_diag: 'Diagonal 45° cut (x+y plane)',

    /* ---- toasts ---- */
    night_on:   'Night on',
    night_off:  'Night off',
    sounds_on:  'Sounds on',
    sounds_off: 'Sounds off',
    grid_on:    'Grid on',
    grid_off:   'Grid off',
    center_on:  'center on',
    center_off: 'center off',
    edges_on:   'Edges on',
    edges_off:  'Edges off',
    reset:      'Reset',
    undo:       'Undo',
    redo:       'Redo',
    png_saved:  'PNG saved',
    lang_changed: 'Language: English (US)',

    /* ---- settings page ---- */
    settings_h2:          'Settings',
    settings_sub:         'Session-only — every reload starts at the defaults.',
    setting_lang_lbl:     'Language',
    setting_lang_desc:    'Interface language',
    setting_sounds_lbl:   'Sounds',
    setting_sounds_desc:  'Sound feedback on interactions',
    setting_grid_lbl:     'Canvas grid',
    setting_grid_desc:    'Background helper lines (full canvas)',
    setting_center_lbl:   'Center guides',
    setting_center_desc:  'X/Y lines through the figure center',
    setting_reset_lbl:    'Reset',
    setting_reset_desc:   'Restore all settings to defaults',
    btn_reset:            'Reset',

    /* ---- info page (structured) ---- */
    info: {
      h2:  'Info',
      sub: 'A Minecraft-flavoured pixel-perfect generator for rounded shapes.',
      sections: [
        { h3: '1. What it is', items: [
          { p: 'Browser-based generator for pixel shapes (2D) and voxel shapes (3D) rendered with Minecraft block textures. Pick a block, dial in a size, get a PNG. No installation, no account, no backend.' },
        ]},
        { h3: '2. Modes & shapes', items: [
          { h: '2D · Circle / Ellipse',   p: 'Circle (single <b>Size</b>) or Ellipse (<b>Width</b> + <b>Height</b>) tiled with the chosen block texture.' },
          { h: '3D · Sphere / Ellipsoid', p: 'Voxel sphere (single <b>Size</b>) or Ellipsoid (<b>W</b> + <b>H</b> + <b>D</b>). Each visible voxel is textured.' },
          { h: 'Cut (3D)',                p: 'Slice along the <b>X</b>, <b>Y</b> or <b>⟋</b> (45° diagonal) axis. Switching axis restores the full figure — only one cuts at a time. Slider max scales to the chosen axis.' },
        ]},
        { h3: '3. Algorithms (2D)', items: [
          { h: 'Euclidean', p: 'Distance test at pixel centres. Smoothest contour.' },
          { h: 'Bresenham', p: 'Classic midpoint algorithm. Stair-stepped pixel-art look.' },
          { h: 'Threshold', p: 'Corner-coverage. Chunkier silhouette at the same size.' },
        ]},
        { h3: '4. Controls', items: [
          { h: 'Mode & shape',     p: '<b>2D / 3D</b> and <b>Circle / Ellipse</b> (Sphere / Ellipsoid in 3D) toggles at the top.' },
          { h: 'Block picker',     p: 'Click any block tile in the picker strip below the canvas. <b>Random</b> mixes natural blocks across cells. Arrow keys walk the picker after selection.' },
          { h: 'Pinch & rotate',   p: 'Two fingers zoom; in 3D the midpoint also rotates. Mouse wheel zooms; in 3D click-drag rotates. Double-click resets the camera (3D) or zoom (2D).' },
          { h: 'Grid & wireframe', p: 'The grid corner button toggles a cell grid in 2D and a per-voxel edge overlay in 3D. Default is OFF for transparent blocks (Glass / Ice) and ON for everything else — preferences are kept separately.' },
          { h: 'Sound & theme',    p: 'The <b>speaker</b> button in the topbar mutes all sounds (placement clicks, fuse, easter-egg samples). The <b>sun / moon</b> button toggles a night mood that dims background panels only — text and block tiles stay bright.' },
          { h: 'Language',         p: 'The <b>language</b> button at the right side of the topbar (and the picker in Settings) swaps the interface between supported locales. Choice is remembered across reloads.' },
          { h: 'Undo / Redo',      p: '<span class="key">Ctrl+Z</span> undoes the last figure-changing edit; any of <span class="key">Ctrl+Y</span> / <span class="key">Ctrl+Shift+Z</span> / <span class="key">Ctrl+Alt+Z</span> redoes. Visual-only toggles (camera, edges, theme, sound) are not tracked.' },
          { h: 'Exports',          p: 'The top-right corner has <b>PNG</b> (current canvas) and <b>.schem</b> (Sponge Schematic v2, gzipped NBT) — the latter loads in WorldEdit, Litematica and MCEdit.' },
          { h: 'Easter eggs',      p: 'An oak <b>tree</b> grows on top of the figure when any size slider hits <b>15</b> with Grass Block / Dirt / Random selected. A <b>creeper</b> stands on top instead when the slider is at 15 with <b>TNT</b> selected — and slowly turns to lock eyes with the camera every ~16 s, glowing primed-white as it fires the TNT fuse.' },
          { h: 'Keyboard',         p: '<span class="key">G</span> Grid &nbsp; <span class="key">C</span> Center &nbsp; <span class="key">D</span> Download PNG &nbsp; <span class="key">I</span> Info chip &nbsp; <span class="key">M</span> 2D/3D &nbsp; <span class="key">S</span> Sound &nbsp; <span class="key">T</span> Night &nbsp; <span class="key">Ctrl+Z</span> Undo &nbsp; <span class="key">Ctrl+Y</span> Redo' },
        ]},
        { h3: '5. Trademarks & credits', items: [
          { h: 'Not affiliated',   p: '<b>Block Round is not affiliated with, endorsed by, or sponsored by Mojang Studios or Microsoft.</b> "Minecraft" is a trademark of Mojang Synergies AB.' },
          { h: 'Block textures',   p: 'Block textures are property of Mojang/Microsoft. See <code>LICENSE</code> &amp; <code>NOTICE.md</code>.' },
          { h: 'Source',           p: 'All Rights Reserved on code. Repository: <code>github.com/ViniSouza128/block-round</code>.' },
        ]},
      ],
    },

    /* ---- block names (picker tile tooltip + info chip "Block:" value) ---- */
    blocks: {
      random: 'Random',
      grass_block: 'Grass Block', dirt: 'Dirt', stone: 'Stone', cobble: 'Cobblestone',
      oak: 'Oak Planks', oak_log: 'Oak Log', sand: 'Sand', gravel: 'Gravel', glass: 'Glass',
      coal: 'Coal Ore', iron_ore: 'Iron Ore', gold_ore: 'Gold Ore', redstone: 'Redstone Ore',
      lapis: 'Lapis Ore', diamond_ore: 'Diamond Ore', emerald_ore: 'Emerald Ore',
      iron: 'Iron Block', gold: 'Gold Block', diamond: 'Diamond Block', emerald: 'Emerald Block',
      copper: 'Copper Block',
      granite: 'Granite', andesite: 'Andesite', polished_andesite: 'Polished Andesite',
      diorite: 'Diorite', smooth_stone: 'Smooth Stone', mossy_cobble: 'Mossy Cobble',
      deepslate: 'Deepslate', bedrock: 'Bedrock',
      soul_sand: 'Soul Sand', sandstone: 'Sandstone', end_stone: 'End Stone', moss: 'Moss',
      darkOak: 'Dark Oak', birch: 'Birch', spruce: 'Spruce', jungle: 'Jungle', acacia: 'Acacia',
      birch_log: 'Birch Log', spruce_log: 'Spruce Log', jungle_log: 'Jungle Log',
      acacia_log: 'Acacia Log', dark_oak_log: 'Dark Oak Log',
      glowstone: 'Glowstone', sea_lantern: 'Sea Lantern', magma: 'Magma',
      bricks: 'Bricks', nether_bricks: 'Nether Bricks', quartz: 'Quartz', obsidian: 'Obsidian',
      ice: 'Ice', packed_ice: 'Packed Ice', blue_ice: 'Blue Ice', snow_block: 'Snow Block',
      netherrack: 'Netherrack', hay: 'Hay', pumpkin: 'Pumpkin', melon: 'Melon', bone: 'Bone',
      crafting_table: 'Crafting Table', furnace: 'Furnace', bookshelf: 'Bookshelf', tnt: 'TNT',
      mycelium: 'Mycelium', podzol: 'Podzol',
      prismarine: 'Prismarine', prismarine_bricks: 'Prismarine Bricks', dark_prismarine: 'Dark Prismarine',
      red_mushroom: 'Red Mushroom', brown_mushroom: 'Brown Mushroom',
      slime: 'Slime Block', honey: 'Honey Block', sponge: 'Sponge',
      shroomlight: 'Shroomlight', crying_obsidian: 'Crying Obsidian',
      white_wool: 'White Wool', light_blue_wool: 'Light Blue Wool', blue_wool: 'Blue Wool',
      green_wool: 'Green Wool', yellow_wool: 'Yellow Wool', orange_wool: 'Orange Wool',
      red_wool: 'Red Wool', black_wool: 'Black Wool',
    },
  },

  'pt-BR': {
    /* ---- meta ---- */
    doc_title:   'Block Round — gerador pixel-perfeito de formas arredondadas',
    meta_desc:   'Block Round — gerador pixel-perfeito com estética Minecraft. Não afiliado à Mojang/Microsoft.',
    brand:       'Block Round',
    brand_aria:  'Página inicial do Block Round',

    /* ---- topbar buttons ---- */
    lang_toggle_title: 'Mudar idioma',
    sound_title:       'Alternar som (S)',
    theme_title:       'Alternar dia / noite (T)',
    info_title:        'Informações',
    settings_title:    'Configurações',
    brand_title:       'Block Round',

    /* ---- mode / shape buttons ---- */
    mode_2d: '2D', mode_3d: '3D',
    shape_circle:    'Círculo',
    shape_ellipse:   'Elipse',
    shape_sphere:    'Esfera',
    shape_ellipsoid: 'Elipsoide',

    /* ---- render pills ---- */
    render_filled: 'Preenchido',
    render_thin:   'Fino',
    render_thick:  'Grosso',

    /* ---- algo pills ---- */
    algo_euclidean: 'Euclidiano',
    algo_bresenham: 'Bresenham',
    algo_threshold: 'Limiar',

    /* ---- slider labels ---- */
    lbl_size:   'Tamanho',
    lbl_width:  'Largura',
    lbl_height: 'Altura',
    lbl_depth:  'Profundidade',
    lbl_cut:    'Corte',

    /* ---- canvas corner button titles ---- */
    title_grid:     'Grade / Wireframe (G)',
    title_download: 'Baixar PNG (D)',
    title_schem:    'Exportar esquemático Minecraft (.schem)',
    title_center:   'Guias de centro (C)',
    title_overlay:  'Sobreposição perfeita',
    title_zoom:     'Zoom no quadrante superior esquerdo',
    title_infochip: 'Chip de informações (I)',

    /* ---- info chip labels ---- */
    chip_d:      'D',
    chip_r:      'R',
    chip_vol:    'Vol',
    chip_blocks: 'Blocos',
    chip_block:  'Bloco',

    /* ---- cut-axis titles ---- */
    title_cut_x:    'Cortar ao longo do eixo X',
    title_cut_y:    'Cortar ao longo do eixo Y',
    title_cut_diag: 'Corte diagonal 45° (plano x+y)',

    /* ---- toasts ---- */
    night_on:   'Noite ativada',
    night_off:  'Noite desativada',
    sounds_on:  'Sons ativados',
    sounds_off: 'Sons desativados',
    grid_on:    'Grade ativada',
    grid_off:   'Grade desativada',
    center_on:  'guias centrais ativadas',
    center_off: 'guias centrais desativadas',
    edges_on:   'Arestas ativadas',
    edges_off:  'Arestas desativadas',
    reset:      'Reiniciado',
    undo:       'Desfazer',
    redo:       'Refazer',
    png_saved:  'PNG salvo',
    lang_changed: 'Idioma: Português (Brasil)',

    /* ---- settings page ---- */
    settings_h2:          'Configurações',
    settings_sub:         'Apenas para esta sessão — cada recarga volta ao padrão (exceto o idioma).',
    setting_lang_lbl:     'Idioma',
    setting_lang_desc:    'Idioma da interface',
    setting_sounds_lbl:   'Sons',
    setting_sounds_desc:  'Feedback sonoro nas interações',
    setting_grid_lbl:     'Grade do canvas',
    setting_grid_desc:    'Linhas auxiliares de fundo (canvas completo)',
    setting_center_lbl:   'Guias de centro',
    setting_center_desc:  'Linhas X/Y pelo centro da figura',
    setting_reset_lbl:    'Reiniciar',
    setting_reset_desc:   'Restaurar todas as configurações ao padrão',
    btn_reset:            'Reiniciar',

    /* ---- info page (structured) ---- */
    info: {
      h2:  'Informações',
      sub: 'Um gerador pixel-perfeito de formas arredondadas com estética Minecraft.',
      sections: [
        { h3: '1. O que é', items: [
          { p: 'Gerador no navegador para formas em pixels (2D) e em voxels (3D) com texturas de blocos do Minecraft. Escolha um bloco, ajuste o tamanho e baixe um PNG. Sem instalação, sem cadastro e sem backend.' },
        ]},
        { h3: '2. Modos & formas', items: [
          { h: '2D · Círculo / Elipse',      p: 'Círculo (apenas <b>Tamanho</b>) ou Elipse (<b>Largura</b> + <b>Altura</b>) preenchidos com a textura do bloco escolhido.' },
          { h: '3D · Esfera / Elipsoide',    p: 'Esfera de voxels (apenas <b>Tamanho</b>) ou Elipsoide (<b>L</b> + <b>A</b> + <b>P</b>). Cada voxel visível recebe textura.' },
          { h: 'Corte (3D)',                 p: 'Corte ao longo do eixo <b>X</b>, <b>Y</b> ou <b>⟋</b> (diagonal 45°). Trocar o eixo restaura a figura — apenas um corte por vez. O máximo do slider se ajusta ao eixo escolhido.' },
        ]},
        { h3: '3. Algoritmos (2D)', items: [
          { h: 'Euclidiano', p: 'Teste de distância no centro de cada pixel. Contorno mais suave.' },
          { h: 'Bresenham',  p: 'Algoritmo clássico do ponto médio. Visual escadinha em pixel-art.' },
          { h: 'Limiar',     p: 'Cobertura por canto. Silhueta mais "blocada" no mesmo tamanho.' },
        ]},
        { h3: '4. Controles', items: [
          { h: 'Modo & forma',       p: 'Botões <b>2D / 3D</b> e <b>Círculo / Elipse</b> (Esfera / Elipsoide em 3D) no topo.' },
          { h: 'Seletor de blocos',  p: 'Clique em qualquer bloco na faixa abaixo do canvas. <b>Aleatório</b> mistura blocos naturais entre as células. As setas do teclado percorrem o seletor depois da seleção.' },
          { h: 'Pinçar & rotacionar',p: 'Dois dedos dão zoom; em 3D o ponto médio também rotaciona. A roda do mouse dá zoom; em 3D clique-arraste rotaciona. Duplo clique reseta a câmera (3D) ou o zoom (2D).' },
          { h: 'Grade & wireframe',  p: 'O botão de grade alterna a grade de células em 2D e a sobreposição de arestas por voxel em 3D. O padrão é OFF para blocos transparentes (Vidro / Gelo) e ON para o resto — as preferências são separadas.' },
          { h: 'Som & tema',         p: 'O botão de <b>alto-falante</b> no topo silencia todos os sons (cliques de posicionamento, pavio, easter-eggs). O botão de <b>sol / lua</b> alterna um modo noturno que escurece apenas os painéis de fundo — texto e blocos seguem nítidos.' },
          { h: 'Idioma',             p: 'O botão de <b>idioma</b> à direita do topo (e o seletor em Configurações) troca o idioma da interface entre os disponíveis. A escolha fica salva entre as recargas.' },
          { h: 'Desfazer / Refazer', p: '<span class="key">Ctrl+Z</span> desfaz a última alteração da figura; <span class="key">Ctrl+Y</span> / <span class="key">Ctrl+Shift+Z</span> / <span class="key">Ctrl+Alt+Z</span> refaz. Toggles visuais (câmera, arestas, tema, som) não entram no histórico.' },
          { h: 'Exportações',        p: 'O canto superior direito tem <b>PNG</b> (canvas atual) e <b>.schem</b> (Sponge Schematic v2, NBT compactado) — o segundo abre no WorldEdit, Litematica e MCEdit.' },
          { h: 'Easter eggs',        p: 'Uma <b>árvore</b> de carvalho nasce em cima da figura quando qualquer slider de tamanho chega a <b>15</b> com Grama / Terra / Aleatório selecionado. Um <b>creeper</b> aparece no lugar com <b>TNT</b> selecionado em 15 — ele vira lentamente para fitar a câmera a cada ~16 s, brilhando de branco quando aciona o pavio.' },
          { h: 'Teclado',            p: '<span class="key">G</span> Grade &nbsp; <span class="key">C</span> Centro &nbsp; <span class="key">D</span> Baixar PNG &nbsp; <span class="key">I</span> Chip de info &nbsp; <span class="key">M</span> 2D/3D &nbsp; <span class="key">S</span> Som &nbsp; <span class="key">T</span> Noite &nbsp; <span class="key">Ctrl+Z</span> Desfazer &nbsp; <span class="key">Ctrl+Y</span> Refazer' },
        ]},
        { h3: '5. Marcas & créditos', items: [
          { h: 'Sem afiliação',  p: '<b>Block Round não é afiliado, endossado ou patrocinado pela Mojang Studios ou pela Microsoft.</b> "Minecraft" é uma marca registrada da Mojang Synergies AB.' },
          { h: 'Texturas',       p: 'As texturas dos blocos são propriedade da Mojang/Microsoft. Veja <code>LICENSE</code> &amp; <code>NOTICE.md</code>.' },
          { h: 'Código-fonte',   p: 'Todos os direitos reservados sobre o código. Repositório: <code>github.com/ViniSouza128/block-round</code>.' },
        ]},
      ],
    },

    /* ---- block names ---- */
    blocks: {
      random: 'Aleatório',
      grass_block: 'Bloco de Grama', dirt: 'Terra', stone: 'Pedra', cobble: 'Pedregulho',
      oak: 'Tábuas de Carvalho', oak_log: 'Tronco de Carvalho', sand: 'Areia', gravel: 'Cascalho', glass: 'Vidro',
      coal: 'Minério de Carvão', iron_ore: 'Minério de Ferro', gold_ore: 'Minério de Ouro',
      redstone: 'Minério de Redstone', lapis: 'Minério de Lápis-Lazúli',
      diamond_ore: 'Minério de Diamante', emerald_ore: 'Minério de Esmeralda',
      iron: 'Bloco de Ferro', gold: 'Bloco de Ouro', diamond: 'Bloco de Diamante',
      emerald: 'Bloco de Esmeralda', copper: 'Bloco de Cobre',
      granite: 'Granito', andesite: 'Andesito', polished_andesite: 'Andesito Polido',
      diorite: 'Diorito', smooth_stone: 'Pedra Lisa', mossy_cobble: 'Pedregulho Musgoso',
      deepslate: 'Ardósia Profunda', bedrock: 'Bedrock',
      soul_sand: 'Areia das Almas', sandstone: 'Arenito', end_stone: 'Pedra do End', moss: 'Musgo',
      darkOak: 'Carvalho Escuro', birch: 'Bétula', spruce: 'Pinheiro', jungle: 'Selva', acacia: 'Acácia',
      birch_log: 'Tronco de Bétula', spruce_log: 'Tronco de Pinheiro',
      jungle_log: 'Tronco de Selva', acacia_log: 'Tronco de Acácia',
      dark_oak_log: 'Tronco de Carvalho Escuro',
      glowstone: 'Glowstone', sea_lantern: 'Lanterna Marinha', magma: 'Magma',
      bricks: 'Tijolos', nether_bricks: 'Tijolos do Nether', quartz: 'Quartzo',
      obsidian: 'Obsidiana', ice: 'Gelo', packed_ice: 'Gelo Compactado',
      blue_ice: 'Gelo Azul', snow_block: 'Bloco de Neve',
      netherrack: 'Pedra do Nether', hay: 'Feno', pumpkin: 'Abóbora', melon: 'Melancia', bone: 'Osso',
      crafting_table: 'Bancada de Trabalho', furnace: 'Fornalha', bookshelf: 'Estante de Livros', tnt: 'TNT',
      mycelium: 'Micélio', podzol: 'Podzol',
      prismarine: 'Prismarinho', prismarine_bricks: 'Tijolos de Prismarinho', dark_prismarine: 'Prismarinho Escuro',
      red_mushroom: 'Cogumelo Vermelho', brown_mushroom: 'Cogumelo Marrom',
      slime: 'Bloco de Slime', honey: 'Bloco de Mel', sponge: 'Esponja',
      shroomlight: 'Cogucândela', crying_obsidian: 'Obsidiana Chorona',
      white_wool: 'Lã Branca', light_blue_wool: 'Lã Azul Clara', blue_wool: 'Lã Azul',
      green_wool: 'Lã Verde', yellow_wool: 'Lã Amarela', orange_wool: 'Lã Laranja',
      red_wool: 'Lã Vermelha', black_wool: 'Lã Preta',
    },
  },

  'ru-RU': {
    /* ---- meta ---- */
    doc_title:   'Block Round — пиксельно-точный генератор закруглённых фигур',
    meta_desc:   'Block Round — пиксельно-точный генератор с эстетикой Minecraft. Не аффилирован с Mojang/Microsoft.',
    brand:       'Block Round',
    brand_aria:  'Домашняя страница Block Round',

    /* ---- topbar buttons ---- */
    lang_toggle_title: 'Сменить язык',
    sound_title:       'Звук (S)',
    theme_title:       'День / ночь (T)',
    info_title:        'Инфо',
    settings_title:    'Настройки',
    brand_title:       'Block Round',

    /* ---- mode / shape buttons ---- */
    mode_2d: '2D', mode_3d: '3D',
    shape_circle:    'Круг',
    shape_ellipse:   'Эллипс',
    shape_sphere:    'Сфера',
    shape_ellipsoid: 'Эллипсоид',

    /* ---- render pills ---- */
    render_filled: 'Заливка',
    render_thin:   'Тонкий',
    render_thick:  'Толстый',

    /* ---- algo pills ---- */
    algo_euclidean: 'Евклидов',
    algo_bresenham: 'Брезенхэм',
    algo_threshold: 'Порог',

    /* ---- slider labels ---- */
    lbl_size:   'Размер',
    lbl_width:  'Ширина',
    lbl_height: 'Высота',
    lbl_depth:  'Глубина',
    lbl_cut:    'Срез',

    /* ---- canvas corner button titles ---- */
    title_grid:     'Сетка / Рёбра (G)',
    title_download: 'Скачать PNG (D)',
    title_schem:    'Экспорт схематика Minecraft (.schem)',
    title_center:   'Осевые линии (C)',
    title_overlay:  'Идеальный контур',
    title_zoom:     'Увеличить верхний левый квадрант',
    title_infochip: 'Инфо-чип (I)',

    /* ---- info chip labels ---- */
    chip_d:      'D',
    chip_r:      'R',
    chip_vol:    'Объём',
    chip_blocks: 'Блоки',
    chip_block:  'Блок',

    /* ---- cut-axis titles ---- */
    title_cut_x:    'Срез по оси X',
    title_cut_y:    'Срез по оси Y',
    title_cut_diag: 'Диагональный срез 45° (плоскость x+y)',

    /* ---- toasts ---- */
    night_on:   'Ночь включена',
    night_off:  'Ночь выключена',
    sounds_on:  'Звук включён',
    sounds_off: 'Звук выключен',
    grid_on:    'Сетка включена',
    grid_off:   'Сетка выключена',
    center_on:  'осевые линии включены',
    center_off: 'осевые линии выключены',
    edges_on:   'Рёбра включены',
    edges_off:  'Рёбра выключены',
    reset:      'Сброс',
    undo:       'Отменить',
    redo:       'Повторить',
    png_saved:  'PNG сохранён',
    lang_changed: 'Язык: Русский',

    /* ---- settings page ---- */
    settings_h2:          'Настройки',
    settings_sub:         'Только для этой сессии — каждая перезагрузка начинает с настроек по умолчанию.',
    setting_lang_lbl:     'Язык',
    setting_lang_desc:    'Язык интерфейса',
    setting_sounds_lbl:   'Звуки',
    setting_sounds_desc:  'Звуковой отклик на действия',
    setting_grid_lbl:     'Сетка холста',
    setting_grid_desc:    'Вспомогательные линии фона (весь холст)',
    setting_center_lbl:   'Осевые линии',
    setting_center_desc:  'Линии X/Y через центр фигуры',
    setting_reset_lbl:    'Сброс',
    setting_reset_desc:   'Восстановить все настройки по умолчанию',
    btn_reset:            'Сбросить',

    /* ---- info page (structured) ---- */
    info: {
      h2:  'Инфо',
      sub: 'Пиксельно-точный генератор закруглённых фигур с эстетикой Minecraft.',
      sections: [
        { h3: '1. Что это', items: [
          { p: 'Браузерный генератор пиксельных фигур (2D) и воксельных фигур (3D) с текстурами блоков Minecraft. Выберите блок, задайте размер, получите PNG. Без установки, без аккаунта, без бэкенда.' },
        ]},
        { h3: '2. Режимы и фигуры', items: [
          { h: '2D · Круг / Эллипс',     p: 'Круг (только <b>Размер</b>) или Эллипс (<b>Ширина</b> + <b>Высота</b>) с выбранной текстурой блока.' },
          { h: '3D · Сфера / Эллипсоид', p: 'Воксельная сфера (только <b>Размер</b>) или Эллипсоид (<b>Ш</b> + <b>В</b> + <b>Г</b>). Каждый видимый воксел получает текстуру.' },
          { h: 'Срез (3D)',              p: 'Срез по оси <b>X</b>, <b>Y</b> или <b>⟋</b> (диагональ 45°). Смена оси восстанавливает фигуру — одновременно режет только одна ось. Максимум слайдера масштабируется под выбранную ось.' },
        ]},
        { h3: '3. Алгоритмы (только 2D)', items: [
          { h: 'Евклидов',  p: 'Тест расстояния в центре пикселя. Самый плавный контур.' },
          { h: 'Брезенхэм', p: 'Классический алгоритм средней точки. Ступенчатый вид пиксель-арта.' },
          { h: 'Порог',     p: 'Тест покрытия угла. Более «блочный» силуэт при том же размере.' },
        ]},
        { h3: '4. Управление', items: [
          { h: 'Режим и форма',        p: 'Кнопки <b>2D / 3D</b> и <b>Круг / Эллипс</b> (Сфера / Эллипсоид в 3D) вверху.' },
          { h: 'Выбор блока',          p: 'Щёлкните любой блок на панели ниже холста. <b>Случайный</b> смешивает природные блоки. Стрелки клавиатуры перемещаются по панели после выбора.' },
          { h: 'Щипок и поворот',      p: 'Два пальца дают зум; в 3D средняя точка также вращает. Колёсико мыши — зум; в 3D перетаскивание — поворот. Двойной клик сбрасывает камеру (3D) или зум (2D).' },
          { h: 'Сетка и рёбра',        p: 'Кнопка сетки переключает сетку ячеек в 2D и наложение рёбер на воксел в 3D. По умолчанию ВЫКЛ для прозрачных блоков (Стекло / Лёд) и ВКЛ для остальных — настройки хранятся раздельно.' },
          { h: 'Звук и тема',          p: 'Кнопка <b>динамика</b> вверху отключает все звуки (щелчки размещения, фитиль, пасхалки). Кнопка <b>солнце / луна</b> включает ночной режим, затемняющий только фоновые панели — текст и блоки остаются яркими.' },
          { h: 'Язык',                 p: 'Кнопка <b>язык</b> справа вверху (и выбор в Настройках) переключает язык интерфейса. Выбор сохраняется между перезагрузками.' },
          { h: 'Отменить / Повторить', p: '<span class="key">Ctrl+Z</span> отменяет последнее изменение фигуры; <span class="key">Ctrl+Y</span> / <span class="key">Ctrl+Shift+Z</span> / <span class="key">Ctrl+Alt+Z</span> — повтор. Визуальные переключатели (камера, рёбра, тема, звук) не отслеживаются.' },
          { h: 'Экспорт',              p: 'В правом верхнем углу — <b>PNG</b> (текущий холст) и <b>.schem</b> (Sponge Schematic v2, сжатый NBT) — второй открывается в WorldEdit, Litematica и MCEdit.' },
          { h: 'Пасхалки',            p: 'Дуб <b>растёт</b> на фигуре, когда любой слайдер размера достигает <b>15</b> с выбранным Блоком Травы / Землёй / Случайным. <b>Крипер</b> появляется вместо него при <b>TNT</b> — медленно поворачивается к камере каждые ~16 с, мигая белым при воспламенении фитиля.' },
          { h: 'Клавиши',             p: '<span class="key">G</span> Сетка &nbsp; <span class="key">C</span> Центр &nbsp; <span class="key">D</span> Скачать PNG &nbsp; <span class="key">I</span> Инфо-чип &nbsp; <span class="key">M</span> 2D/3D &nbsp; <span class="key">S</span> Звук &nbsp; <span class="key">T</span> Ночь &nbsp; <span class="key">Ctrl+Z</span> Отменить &nbsp; <span class="key">Ctrl+Y</span> Повторить' },
        ]},
        { h3: '5. Марки и авторы', items: [
          { h: 'Без аффиляции',   p: '<b>Block Round не аффилирован, не одобрен и не спонсируется Mojang Studios или Microsoft.</b> «Minecraft» — товарный знак Mojang Synergies AB.' },
          { h: 'Текстуры блоков', p: 'Текстуры блоков являются собственностью Mojang/Microsoft. См. <code>LICENSE</code> &amp; <code>NOTICE.md</code>.' },
          { h: 'Исходный код',    p: 'Все права на код защищены. Репозиторий: <code>github.com/ViniSouza128/block-round</code>.' },
        ]},
      ],
    },

    /* ---- block names ---- */
    blocks: {
      random: 'Случайный',
      grass_block: 'Блок Травы', dirt: 'Земля', stone: 'Камень', cobble: 'Булыжник',
      oak: 'Доски Дуба', oak_log: 'Ствол Дуба', sand: 'Песок', gravel: 'Гравий', glass: 'Стекло',
      coal: 'Уголь (руда)', iron_ore: 'Железная руда', gold_ore: 'Золотая руда',
      redstone: 'Красная руда', lapis: 'Лазурит (руда)',
      diamond_ore: 'Алмаз (руда)', emerald_ore: 'Изумруд (руда)',
      iron: 'Железный блок', gold: 'Золотой блок', diamond: 'Алмазный блок',
      emerald: 'Изумрудный блок', copper: 'Медный блок',
      granite: 'Гранит', andesite: 'Андезит', polished_andesite: 'Полированный андезит',
      diorite: 'Диорит', smooth_stone: 'Гладкий камень', mossy_cobble: 'Замшелый булыжник',
      deepslate: 'Глубинный сланец', bedrock: 'Бедрок',
      soul_sand: 'Душевой песок', sandstone: 'Песчаник', end_stone: 'Камень Края', moss: 'Мох',
      darkOak: 'Тёмный дуб', birch: 'Берёза', spruce: 'Ель', jungle: 'Джунгли', acacia: 'Акация',
      birch_log: 'Ствол берёзы', spruce_log: 'Ствол ели',
      jungle_log: 'Ствол джунглей', acacia_log: 'Ствол акации',
      dark_oak_log: 'Ствол тёмного дуба',
      glowstone: 'Светокамень', sea_lantern: 'Морской фонарь', magma: 'Магма',
      bricks: 'Кирпич', nether_bricks: 'Адский кирпич', quartz: 'Кварц', obsidian: 'Обсидиан',
      ice: 'Лёд', packed_ice: 'Плотный лёд', blue_ice: 'Синий лёд', snow_block: 'Снежный блок',
      netherrack: 'Незерак', hay: 'Сено', pumpkin: 'Тыква', melon: 'Арбуз', bone: 'Кость',
      crafting_table: 'Верстак', furnace: 'Печь', bookshelf: 'Книжная полка', tnt: 'ТНТ',
      mycelium: 'Мицелий', podzol: 'Подзол',
      prismarine: 'Призмарин', prismarine_bricks: 'Призмариновые кирпичи', dark_prismarine: 'Тёмный призмарин',
      red_mushroom: 'Красный гриб', brown_mushroom: 'Коричневый гриб',
      slime: 'Блок слизи', honey: 'Медовый блок', sponge: 'Губка',
      shroomlight: 'Грибосвет', crying_obsidian: 'Плачущий обсидиан',
      white_wool: 'Белая шерсть', light_blue_wool: 'Голубая шерсть', blue_wool: 'Синяя шерсть',
      green_wool: 'Зелёная шерсть', yellow_wool: 'Жёлтая шерсть', orange_wool: 'Оранжевая шерсть',
      red_wool: 'Красная шерсть', black_wool: 'Чёрная шерсть',
    },
  },

  'ko-KR': {
    /* ---- meta ---- */
    doc_title:   'Block Round — 픽셀 정밀 둥근 도형 생성기',
    meta_desc:   'Block Round — 마인크래프트 스타일 픽셀 정밀 생성기. Mojang/Microsoft와 무관.',
    brand:       'Block Round',
    brand_aria:  'Block Round 홈',

    /* ---- topbar buttons ---- */
    lang_toggle_title: '언어 변경',
    sound_title:       '소리 (S)',
    theme_title:       '낮 / 밤 (T)',
    info_title:        '정보',
    settings_title:    '설정',
    brand_title:       'Block Round',

    /* ---- mode / shape buttons ---- */
    mode_2d: '2D', mode_3d: '3D',
    shape_circle:    '원',
    shape_ellipse:   '타원',
    shape_sphere:    '구',
    shape_ellipsoid: '타원체',

    /* ---- render pills ---- */
    render_filled: '채우기',
    render_thin:   '얇게',
    render_thick:  '굵게',

    /* ---- algo pills ---- */
    algo_euclidean: '유클리드',
    algo_bresenham: '브레젠험',
    algo_threshold: '임계값',

    /* ---- slider labels ---- */
    lbl_size:   '크기',
    lbl_width:  '너비',
    lbl_height: '높이',
    lbl_depth:  '깊이',
    lbl_cut:    '자르기',

    /* ---- canvas corner button titles ---- */
    title_grid:     '격자 / 모서리 (G)',
    title_download: 'PNG 다운로드 (D)',
    title_schem:    '마인크래프트 스케매틱 내보내기 (.schem)',
    title_center:   '중심 가이드 (C)',
    title_overlay:  '완벽한 오버레이',
    title_zoom:     '왼쪽 상단 사분면 확대',
    title_infochip: '정보 칩 (I)',

    /* ---- info chip labels ---- */
    chip_d:      'D',
    chip_r:      'R',
    chip_vol:    '부피',
    chip_blocks: '블록들',
    chip_block:  '블록',

    /* ---- cut-axis titles ---- */
    title_cut_x:    'X축으로 자르기',
    title_cut_y:    'Y축으로 자르기',
    title_cut_diag: '45° 대각선 자르기 (x+y 평면)',

    /* ---- toasts ---- */
    night_on:   '밤 켜짐',
    night_off:  '밤 꺼짐',
    sounds_on:  '소리 켜짐',
    sounds_off: '소리 꺼짐',
    grid_on:    '격자 켜짐',
    grid_off:   '격자 꺼짐',
    center_on:  '중심 가이드 켜짐',
    center_off: '중심 가이드 꺼짐',
    edges_on:   '모서리 켜짐',
    edges_off:  '모서리 꺼짐',
    reset:      '초기화',
    undo:       '실행 취소',
    redo:       '다시 실행',
    png_saved:  'PNG 저장됨',
    lang_changed: '언어: 한국어',

    /* ---- settings page ---- */
    settings_h2:          '설정',
    settings_sub:         '세션 전용 — 새로 고침 시 기본값으로 시작합니다.',
    setting_lang_lbl:     '언어',
    setting_lang_desc:    '인터페이스 언어',
    setting_sounds_lbl:   '소리',
    setting_sounds_desc:  '인터랙션 소리 피드백',
    setting_grid_lbl:     '캔버스 격자',
    setting_grid_desc:    '배경 보조선 (전체 캔버스)',
    setting_center_lbl:   '중심 가이드',
    setting_center_desc:  '도형 중심을 통과하는 X/Y 선',
    setting_reset_lbl:    '초기화',
    setting_reset_desc:   '모든 설정을 기본값으로 복원',
    btn_reset:            '초기화',

    /* ---- info page (structured) ---- */
    info: {
      h2:  '정보',
      sub: '마인크래프트 블록 텍스처를 사용한 픽셀 정밀 둥근 도형 생성기.',
      sections: [
        { h3: '1. 무엇인가', items: [
          { p: '마인크래프트 블록 텍스처로 렌더링된 픽셀 도형(2D)과 복셀 도형(3D)을 생성하는 브라우저 기반 도구. 블록을 선택하고 크기를 조절하면 PNG가 출력됩니다. 설치 불필요, 계정 불필요, 백엔드 불필요.' },
        ]},
        { h3: '2. 모드 & 도형', items: [
          { h: '2D · 원 / 타원',   p: '원(<b>크기</b>만) 또는 타원(<b>너비</b> + <b>높이</b>)을 선택한 블록 텍스처로 표시합니다.' },
          { h: '3D · 구 / 타원체', p: '복셀 구(<b>크기</b>만) 또는 타원체(<b>너비</b> + <b>높이</b> + <b>깊이</b>). 보이는 모든 복셀에 텍스처가 적용됩니다.' },
          { h: '자르기 (3D)',      p: '<b>X</b>, <b>Y</b> 또는 <b>⟋</b>(45° 대각선) 축으로 자릅니다. 축을 바꾸면 전체 도형이 복원됩니다 — 한 번에 하나의 축만 자릅니다. 슬라이더 최대값이 선택된 축에 맞게 조정됩니다.' },
        ]},
        { h3: '3. 알고리즘 (2D 전용)', items: [
          { h: '유클리드', p: '픽셀 중심에서 거리 테스트. 가장 부드러운 윤곽.' },
          { h: '브레젠험', p: '고전적인 정수 중점 알고리즘. 픽셀 아트 계단 형태.' },
          { h: '임계값',   p: '모서리 커버리지 테스트. 동일 크기에서 더 두꺼운 실루엣.' },
        ]},
        { h3: '4. 조작', items: [
          { h: '모드 & 도형',           p: '상단의 <b>2D / 3D</b> 및 <b>원 / 타원</b>(3D에서는 <b>구 / 타원체</b>) 버튼.' },
          { h: '블록 선택',             p: '캔버스 아래 패널에서 블록 타일을 클릭하세요. <b>랜덤</b>은 자연 블록을 혼합합니다. 선택 후 화살표 키로 이동.' },
          { h: '핀치 & 회전',           p: '두 손가락으로 확대/축소; 3D에서는 중점도 회전합니다. 마우스 휠로 줌; 3D에서 클릭 드래그로 회전. 더블 클릭으로 카메라(3D) 또는 줌(2D) 초기화.' },
          { h: '격자 & 모서리',         p: '격자 버튼은 2D에서는 셀 격자를, 3D에서는 복셀별 모서리 오버레이를 전환합니다. 투명 블록(유리/얼음)은 기본 OFF, 나머지는 기본 ON — 설정은 별도로 유지됩니다.' },
          { h: '소리 & 테마',           p: '상단 <b>스피커</b> 버튼으로 모든 소리(배치 클릭, 도화선, 이스터에그)를 끕니다. <b>해/달</b> 버튼은 배경 패널만 어둡게 하는 야간 모드를 전환합니다 — 텍스트와 블록 타일은 밝게 유지됩니다.' },
          { h: '언어',                  p: '상단 바 오른쪽의 <b>언어</b> 버튼(및 설정의 선택기)으로 인터페이스 언어를 전환합니다. 선택 사항은 새로 고침 후에도 유지됩니다.' },
          { h: '실행 취소 / 다시 실행', p: '<span class="key">Ctrl+Z</span>로 마지막 도형 변경을 취소; <span class="key">Ctrl+Y</span> / <span class="key">Ctrl+Shift+Z</span> / <span class="key">Ctrl+Alt+Z</span>로 다시 실행. 시각적 토글(카메라, 모서리, 테마, 소리)은 추적되지 않습니다.' },
          { h: '내보내기',              p: '오른쪽 상단 모서리에 <b>PNG</b>(현재 캔버스)와 <b>.schem</b>(Sponge Schematic v2, 압축된 NBT) — 후자는 WorldEdit, Litematica, MCEdit에서 불러올 수 있습니다.' },
          { h: '이스터에그',            p: '크기 슬라이더가 <b>15</b>일 때 잔디 블록 / 흙 / 랜덤 선택 시 도형 위에 참나무 <b>나무</b>가 자랍니다. <b>TNT</b> 선택 시 <b>크리퍼</b>가 나타납니다 — 약 16초마다 카메라를 향해 천천히 돌아보며 도화선이 켜질 때 흰색으로 빛납니다.' },
          { h: '키보드',                p: '<span class="key">G</span> 격자 &nbsp; <span class="key">C</span> 중심 &nbsp; <span class="key">D</span> PNG 다운로드 &nbsp; <span class="key">I</span> 정보 칩 &nbsp; <span class="key">M</span> 2D/3D &nbsp; <span class="key">S</span> 소리 &nbsp; <span class="key">T</span> 밤 &nbsp; <span class="key">Ctrl+Z</span> 실행 취소 &nbsp; <span class="key">Ctrl+Y</span> 다시 실행' },
        ]},
        { h3: '5. 상표 & 크레딧', items: [
          { h: '비제휴',      p: '<b>Block Round는 Mojang Studios 또는 Microsoft와 제휴, 보증 또는 후원 관계가 없습니다.</b> "Minecraft"는 Mojang Synergies AB의 상표입니다.' },
          { h: '블록 텍스처', p: '블록 텍스처는 Mojang/Microsoft의 소유입니다. <code>LICENSE</code> &amp; <code>NOTICE.md</code> 참조.' },
          { h: '소스',        p: '코드의 모든 권리 보유. 저장소: <code>github.com/ViniSouza128/block-round</code>.' },
        ]},
      ],
    },

    /* ---- block names ---- */
    blocks: {
      random: '랜덤',
      grass_block: '잔디 블록', dirt: '흙', stone: '돌', cobble: '자갈돌',
      oak: '참나무 판자', oak_log: '참나무 원목', sand: '모래', gravel: '자갈', glass: '유리',
      coal: '석탄 광석', iron_ore: '철 광석', gold_ore: '금 광석',
      redstone: '레드스톤 광석', lapis: '청금석 광석',
      diamond_ore: '다이아몬드 광석', emerald_ore: '에메랄드 광석',
      iron: '철 블록', gold: '금 블록', diamond: '다이아몬드 블록',
      emerald: '에메랄드 블록', copper: '구리 블록',
      granite: '화강암', andesite: '안산암', polished_andesite: '매끈한 안산암',
      diorite: '섬록암', smooth_stone: '매끈한 돌', mossy_cobble: '이끼 낀 자갈돌',
      deepslate: '심층암', bedrock: '기반암',
      soul_sand: '소울 샌드', sandstone: '사암', end_stone: '엔드 돌', moss: '이끼',
      darkOak: '짙은 참나무', birch: '자작나무', spruce: '가문비나무', jungle: '정글나무', acacia: '아카시아',
      birch_log: '자작나무 원목', spruce_log: '가문비나무 원목',
      jungle_log: '정글 원목', acacia_log: '아카시아 원목',
      dark_oak_log: '짙은 참나무 원목',
      glowstone: '글로우스톤', sea_lantern: '바다 랜턴', magma: '마그마',
      bricks: '벽돌', nether_bricks: '네더 벽돌', quartz: '석영', obsidian: '흑요석',
      ice: '얼음', packed_ice: '촘촘한 얼음', blue_ice: '청얼음', snow_block: '눈 블록',
      netherrack: '네더랙', hay: '건초 더미', pumpkin: '호박', melon: '수박', bone: '뼈',
      crafting_table: '조합대', furnace: '화로', bookshelf: '책장', tnt: 'TNT',
      mycelium: '균사체', podzol: '포드졸',
      prismarine: '프리즈머린', prismarine_bricks: '프리즈머린 벽돌', dark_prismarine: '짙은 프리즈머린',
      red_mushroom: '빨간 버섯', brown_mushroom: '갈색 버섯',
      slime: '슬라임 블록', honey: '꿀 블록', sponge: '스펀지',
      shroomlight: '버섯불', crying_obsidian: '울고 있는 흑요석',
      white_wool: '흰 양털', light_blue_wool: '하늘색 양털', blue_wool: '파란 양털',
      green_wool: '초록 양털', yellow_wool: '노란 양털', orange_wool: '주황 양털',
      red_wool: '빨간 양털', black_wool: '검은 양털',
    },
  },
};

/* ---------- STATE --------------------------------------------------------- */
let _locale = _detectLocale();

function _detectLocale(){
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && _isSupported(saved)) return saved;
  } catch(_) {}
  const nav = (navigator.language || navigator.userLanguage || '').toLowerCase();
  if (nav) {
    for (const loc of AVAILABLE_LOCALES) {
      const prefix = loc.code.toLowerCase().split('-')[0];
      if (nav.startsWith(prefix)) return loc.code;
    }
  }
  return DEFAULT_LOCALE;
}

function _isSupported(code){
  return AVAILABLE_LOCALES.some(l => l.code === code);
}

function _meta(code){
  return AVAILABLE_LOCALES.find(l => l.code === code) || AVAILABLE_LOCALES[0];
}

/* ---------- PUBLIC API ---------------------------------------------------- */
window.t = function(key){
  const v = (TR[_locale] && TR[_locale][key]);
  if (v != null) return v;
  const fb = TR[DEFAULT_LOCALE] && TR[DEFAULT_LOCALE][key];
  return (fb != null) ? fb : key;
};

window.tBlock = function(blockKey){
  const dict = (TR[_locale] && TR[_locale].blocks) || {};
  const fb   = (TR[DEFAULT_LOCALE] && TR[DEFAULT_LOCALE].blocks) || {};
  return dict[blockKey] || fb[blockKey] || blockKey;
};

window.getLocale = function(){ return _locale; };
window.getAvailableLocales = function(){ return AVAILABLE_LOCALES.slice(); };

window.setLocale = function(code){
  if (!_isSupported(code)) code = DEFAULT_LOCALE;
  _locale = code;
  try { localStorage.setItem(STORAGE_KEY, code); } catch(_) {}
  _applyAll();
  if (typeof toast === 'function') toast(t('lang_changed'));
};

/* ---------- DOM APPLICATION ----------------------------------------------- */
function _applyAll(){
  _applyDocMeta();
  _applyShapeLabels();
  _applyAttributes();
  _rebuildInfoPage();
  _rebuildLangPicker();
  _syncLangBtn();
  _refreshBlockTitles();
  _refreshInfoChip();
  /* Re-run dynamic relabels (shape buttons) */
  if (typeof syncShape === 'function') syncShape();
}

function _applyDocMeta(){
  const meta = _meta(_locale);
  document.title = t('doc_title');
  const html = document.getElementById('html-root') || document.documentElement;
  if (html) html.setAttribute('lang', meta.htmlLang);
  const desc = document.querySelector('meta[name="description"]');
  if (desc) desc.setAttribute('content', t('meta_desc'));
}

function _applyShapeLabels(){
  if (typeof window.SHAPE_LABELS === 'undefined') return;
  window.SHAPE_LABELS.circle['2d']  = t('shape_circle');
  window.SHAPE_LABELS.circle['3d']  = t('shape_sphere');
  window.SHAPE_LABELS.ellipse['2d'] = t('shape_ellipse');
  window.SHAPE_LABELS.ellipse['3d'] = t('shape_ellipsoid');
}

function _applyAttributes(){
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const v = t(el.dataset.i18n);
    if (v != null) el.textContent = v;
  });
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const v = t(el.dataset.i18nTitle);
    if (v != null){
      el.title = v;
      if (el.hasAttribute('aria-label')) el.setAttribute('aria-label', v);
    }
  });
  document.querySelectorAll('[data-i18n-aria]').forEach(el => {
    const v = t(el.dataset.i18nAria);
    if (v != null) el.setAttribute('aria-label', v);
  });
}

function _esc(s){ return String(s).replace(/[&<>"']/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c])); }

function _rebuildInfoPage(){
  const host = document.querySelector('.route[data-route="info"] .route-pad');
  if (!host) return;
  const info = (TR[_locale] && TR[_locale].info) || TR[DEFAULT_LOCALE].info;
  const parts = [];
  parts.push(`<h2 class="section-title">${_esc(info.h2)}</h2>`);
  parts.push(`<p class="section-sub">${info.sub}</p>`);
  info.sections.forEach((sec, i) => {
    parts.push(`<h3 class="ds-h2" style="margin-top:28px;">${sec.h3}</h3>`);
    parts.push('<div class="help-list">');
    sec.items.forEach(it => {
      parts.push('<div class="help-item">');
      if (it.h) parts.push(`<h3>${it.h}</h3>`);
      if (it.p) parts.push(`<p>${it.p}</p>`);
      parts.push('</div>');
    });
    parts.push('</div>');
  });
  host.innerHTML = parts.join('');
}

function _rebuildLangPicker(){
  const sel = document.querySelector('[data-pref="locale"]');
  if (!sel) return;
  sel.innerHTML = '';
  AVAILABLE_LOCALES.forEach(loc => {
    const opt = document.createElement('option');
    opt.value = loc.code;
    opt.textContent = loc.name;
    if (loc.code === _locale) opt.selected = true;
    sel.appendChild(opt);
  });
}

function _syncLangBtn(){
  const btn = document.querySelector('[data-act=lang]');
  if (!btn) return;
  const meta = _meta(_locale);
  const lbl = btn.querySelector('.lang-lbl');
  if (lbl) lbl.textContent = meta.label;
  btn.title = t('lang_toggle_title');
  btn.setAttribute('aria-label', t('lang_toggle_title'));
}

/* Refreshes the title attribute on every block-picker tile to match the
   current locale's name. Built tiles set their title at buildMCList()
   time, so without this they stay frozen in the boot locale. */
function _refreshBlockTitles(){
  document.querySelectorAll('.mc-block[data-block]').forEach(tile => {
    const k = tile.dataset.block;
    tile.title = window.tBlock(k);
  });
}

/* Info chip displays the currently-selected block name. Re-render so the
   text under "Block:" / "Bloco:" follows the locale. */
function _refreshInfoChip(){
  if (typeof updateInfoChip === 'function') updateInfoChip();
}

/* ---------- LANG BUTTON CLICK CYCLE --------------------------------------- */
/* Single-button cycle: cycles through AVAILABLE_LOCALES in order. */
window.cycleLocale = function(){
  const idx = AVAILABLE_LOCALES.findIndex(l => l.code === _locale);
  const next = AVAILABLE_LOCALES[(idx + 1) % AVAILABLE_LOCALES.length].code;
  setLocale(next);
};

/* ---------- INIT ---------------------------------------------------------- */
window.initI18N = function(){
  _applyAll();
};

})();
