/* =============================================================================
   Block Round — js/i18n.js
   All Rights Reserved.

   Multi-locale system.

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
  { code: 'en-US', label: 'EN-US', name: 'English (US)',     htmlLang: 'en'    },
  { code: 'pt-BR', label: 'PT-BR', name: 'Português (Brasil)', htmlLang: 'pt-BR' },
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
        { h3: '6. Documents', items: [
          { h: 'Math companion (PDF)',       p: 'In-depth derivation of the implicit ellipse / ellipsoid equations, the three 2D rasterization algorithms, voxelization, cuts, Lambertian shading and the five Minecraft-specific extensions (inventory arithmetic, exposed-face counting, layer-by-layer construction, octahedral-symmetry /clone optimization, block-texture UV mapping). <a href="docs_math/Block_Round_Math_en-US.pdf" target="_blank" rel="noopener">Open Block_Round_Math_en-US.pdf →</a>' },
          { h: 'Math — all locales',         p: 'The math companion is available in 9 languages (each PDF ≥25 pages): <a href="docs_math/" target="_blank" rel="noopener">docs_math/</a>.' },
          { h: 'Classroom lesson plan (PDF)',p: 'Five-period instructional sequence for the 3rd year of Brazilian high school. 58 pages, 21 figures, aligned to BNCC / ENEM / OBMEP, with five regional adaptations. <a href="docs_aula/Plano_de_Aula_pt-BR.pdf" target="_blank" rel="noopener">Open Plano_de_Aula_pt-BR.pdf →</a>' },
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
        { h3: '6. Documentos', items: [
          { h: 'Documento matemático (PDF)', p: 'Desenvolvimento completo das equações implícitas da elipse e do elipsóide, dos três algoritmos 2D de rasterização, voxelização, cortes, sombreamento Lambertiano e das cinco extensões específicas do Minecraft (aritmética de inventário, contagem de faces expostas, construção camada-por-camada, otimização por simetria octaédrica via /clone, mapeamento UV das texturas de bloco). <a href="docs_math/Block_Round_Math_pt-BR.pdf" target="_blank" rel="noopener">Abrir Block_Round_Math_pt-BR.pdf →</a>' },
          { h: 'Documento — outros idiomas', p: 'O documento matemático está disponível em 9 idiomas (cada PDF tem ≥25 páginas): <a href="docs_math/" target="_blank" rel="noopener">docs_math/</a>.' },
          { h: 'Plano de aula (PDF)',        p: 'Sequência didática de 5 aulas para o 3.º ano do Ensino Médio brasileiro. 58 páginas, 21 figuras, alinhado à BNCC (EM13MAT307/308/309/404), ENEM e OBMEP, com adaptações regionais para escolas urbanas/interior/IFs/campo/indígenas-quilombolas/EJA e tutorial Litematica para construção real no Minecraft. <a href="docs_aula/Plano_de_Aula_pt-BR.pdf" target="_blank" rel="noopener">Abrir Plano_de_Aula_pt-BR.pdf →</a>' },
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
};

/* ---------- STATE --------------------------------------------------------- */
let _locale = _detectLocale();

function _detectLocale(){
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && _isSupported(saved)) return saved;
  } catch(_) {}
  const nav = (navigator.language || navigator.userLanguage || '').toLowerCase();
  if (nav.startsWith('pt')) return 'pt-BR';
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
