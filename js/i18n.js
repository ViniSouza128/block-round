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
      sub: 'A Minecraft-flavoured pixel-perfect generator for rounded shapes — circles, ellipses, spheres and ellipsoids rendered with real block textures.',
      sections: [
        { h3: '1. Quick start', items: [
          { p: '<b>1.</b> Pick a mode at the top — <b>2D / 3D</b> — then a shape (<b>Circle / Ellipse</b> or <b>Sphere / Ellipsoid</b>). <br><b>2.</b> Choose a block from the picker strip below the canvas. <br><b>3.</b> Drag the sliders to set the integer dimensions and hit the corner buttons to download a PNG or a Sponge Schematic (<code>.schem</code>).' },
        ]},
        { h3: '2. Documents', items: [
          { h: 'Math companion (PDF)',       p: 'Full derivation of the implicit ellipse / ellipsoid equations, the three rasterization algorithms, voxelization, planar cuts, Lambertian shading and five Minecraft-specific extensions (inventory packs, exposed faces, layer construction, <code>/clone</code> symmetry, texture UVs). <a href="docs_math/Block_Round_Math_en-US.pdf" target="_blank" rel="noopener">Open Block_Round_Math_en-US.pdf →</a>' },
          { h: 'Classroom lesson plan (PDF)',p: 'Five-period instructional sequence aligned to the Brazilian curriculum (BNCC / ENEM / OBMEP), with five regional adaptations and a Litematica build tutorial. <a href="docs_aula/Plano_de_Aula_pt-BR.pdf" target="_blank" rel="noopener">Open Plano_de_Aula_pt-BR.pdf →</a>' },
          { h: 'All documents',              p: 'The math companion ships in 9 languages — browse <a href="docs_math/" target="_blank" rel="noopener">docs_math/</a> (math, 9 locales) and <a href="docs_aula/" target="_blank" rel="noopener">docs_aula/</a> (lesson plan).' },
        ]},
        { h3: '3. Modes & shapes', items: [
          { h: '2D · Circle / Ellipse',   p: 'Circle uses one <b>Size</b>; Ellipse uses <b>Width</b> + <b>Height</b>. The canvas tiles the chosen block texture into every cell of the rasterized shape.' },
          { h: '3D · Sphere / Ellipsoid', p: 'Sphere uses one <b>Size</b>; Ellipsoid uses <b>W</b> + <b>H</b> + <b>D</b>. Each visible voxel is rendered as a textured Minecraft block.' },
          { h: 'Cut (3D)',                p: 'Slice along <b>X</b>, <b>Y</b> or <b>⟋</b> (45° diagonal). Switching axis restores the full figure — only one cut at a time. The slider max scales to the chosen axis.' },
        ]},
        { h3: '4. Algorithms (2D)', items: [
          { h: 'Euclidean', p: 'Distance test at pixel centres. Smoothest contour.' },
          { h: 'Bresenham', p: 'Integer midpoint algorithm. Stair-stepped pixel-art look.' },
          { h: 'Threshold', p: 'Corner-coverage test. Chunkiest silhouette — any cell with a corner inside fills.' },
        ]},
        { h3: '5. Controls', items: [
          { h: 'Pinch & rotate', p: 'Two fingers zoom (in 3D the midpoint also rotates). Mouse wheel zooms; in 3D click-drag rotates. Double-click resets the camera (3D) or zoom (2D).' },
          { h: 'Grid & edges',   p: 'The grid corner button toggles a cell grid in 2D and a per-voxel edge overlay in 3D. The default is OFF for transparent blocks (Glass / Ice) and ON otherwise.' },
          { h: 'Exports',        p: 'Top-right corner has <b>PNG</b> (current canvas) and <b>.schem</b> (Sponge Schematic v2, gzipped NBT). The schematic opens directly in WorldEdit, Litematica and MCEdit.' },
          { h: 'Easter eggs',    p: 'An oak <b>tree</b> grows on top of the figure when a size slider hits <b>15</b> with Grass Block / Dirt / Random selected. A <b>creeper</b> takes its place with <b>TNT</b> selected — it slowly turns to face the camera every ~16 s, glowing primed-white as it lights the fuse.' },
          { h: 'Keyboard',       p: '<span class="key">G</span> Grid &nbsp; <span class="key">C</span> Center &nbsp; <span class="key">D</span> Download PNG &nbsp; <span class="key">I</span> Info chip &nbsp; <span class="key">M</span> 2D/3D &nbsp; <span class="key">S</span> Sound &nbsp; <span class="key">T</span> Night &nbsp; <span class="key">Ctrl+Z</span> Undo &nbsp; <span class="key">Ctrl+Y</span> Redo' },
        ]},
        { h3: '6. About', items: [
          { h: 'Stack & offline',  p: 'Vanilla JavaScript + Canvas 2D + three.js. No framework, no build step. PWA-installable — works offline once visited. Only the chosen locale persists in <code>localStorage</code>.' },
          { h: 'Not affiliated',   p: '<b>Block Round is not affiliated with, endorsed by, or sponsored by Mojang Studios or Microsoft.</b> "Minecraft" is a trademark of Mojang Synergies AB. Block textures remain property of Mojang/Microsoft — see <code>LICENSE</code> &amp; <code>NOTICE.md</code>.' },
          { h: 'License & source', p: 'All Rights Reserved on code. Repository: <a href="https://github.com/ViniSouza128/block-round" target="_blank" rel="noopener">github.com/ViniSouza128/block-round</a>. Sibling project (texture-free pixel art): <a href="https://github.com/ViniSouza128/pixel-round" target="_blank" rel="noopener">Pixel Round</a>.' },
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
      sub: 'Gerador pixel-perfeito de formas arredondadas com estética Minecraft — círculos, elipses, esferas e elipsoides renderizados com texturas reais de bloco.',
      sections: [
        { h3: '1. Início rápido', items: [
          { p: '<b>1.</b> Escolha um modo no topo — <b>2D / 3D</b> — e uma forma (<b>Círculo / Elipse</b> ou <b>Esfera / Elipsoide</b>). <br><b>2.</b> Selecione um bloco no seletor abaixo do canvas. <br><b>3.</b> Ajuste os sliders e use os botões de canto pra baixar PNG ou Sponge Schematic (<code>.schem</code>).' },
        ]},
        { h3: '2. Documentos', items: [
          { h: 'Documento matemático (PDF)', p: 'Derivação completa das equações implícitas da elipse e do elipsóide, dos três algoritmos de rasterização, voxelização, cortes, sombreamento Lambertiano e das cinco extensões específicas do Minecraft (packs de inventário, faces expostas, construção por camadas, simetria via <code>/clone</code>, mapeamento UV). <a href="docs_math/Block_Round_Math_pt-BR.pdf" target="_blank" rel="noopener">Abrir Block_Round_Math_pt-BR.pdf →</a>' },
          { h: 'Plano de aula (PDF)',        p: 'Sequência didática de 5 aulas pro 3.º ano do EM brasileiro, alinhada à BNCC / ENEM / OBMEP, com cinco adaptações regionais e tutorial Litematica pra construção real. <a href="docs_aula/Plano_de_Aula_pt-BR.pdf" target="_blank" rel="noopener">Abrir Plano_de_Aula_pt-BR.pdf →</a>' },
          { h: 'Todos os documentos',        p: 'O documento matemático está disponível em 9 idiomas — navegue por <a href="docs_math/" target="_blank" rel="noopener">docs_math/</a> (matemática, 9 locales) e <a href="docs_aula/" target="_blank" rel="noopener">docs_aula/</a> (plano de aula).' },
        ]},
        { h3: '3. Modos & formas', items: [
          { h: '2D · Círculo / Elipse',   p: 'Círculo usa só <b>Tamanho</b>; Elipse usa <b>Largura</b> + <b>Altura</b>. O canvas preenche cada célula da forma rasterizada com a textura do bloco escolhido.' },
          { h: '3D · Esfera / Elipsoide', p: 'Esfera usa só <b>Tamanho</b>; Elipsoide usa <b>L</b> + <b>A</b> + <b>P</b>. Cada voxel visível é renderizado como um bloco texturizado.' },
          { h: 'Corte (3D)',              p: 'Corte ao longo de <b>X</b>, <b>Y</b> ou <b>⟋</b> (diagonal 45°). Trocar o eixo restaura a figura inteira — só um corte por vez. O máximo do slider se ajusta ao eixo escolhido.' },
        ]},
        { h3: '4. Algoritmos (2D)', items: [
          { h: 'Euclidiano', p: 'Teste de distância no centro do pixel. Contorno mais suave.' },
          { h: 'Bresenham',  p: 'Algoritmo do ponto médio inteiro. Visual escadinha pixel-art.' },
          { h: 'Limiar',     p: 'Cobertura por canto. Silhueta mais "blocada" — qualquer célula com canto dentro é preenchida.' },
        ]},
        { h3: '5. Controles', items: [
          { h: 'Pinçar & rotacionar', p: 'Dois dedos dão zoom (em 3D o ponto médio também rotaciona). A roda do mouse dá zoom; em 3D clique-arraste rotaciona. Duplo clique reseta a câmera (3D) ou o zoom (2D).' },
          { h: 'Grade & arestas',     p: 'O botão de grade alterna a grade de células em 2D e o overlay de arestas por voxel em 3D. Padrão OFF para blocos transparentes (Vidro / Gelo) e ON pro resto.' },
          { h: 'Exportações',         p: 'O canto superior direito tem <b>PNG</b> (canvas atual) e <b>.schem</b> (Sponge Schematic v2, NBT compactado). O schematic abre direto no WorldEdit, Litematica e MCEdit.' },
          { h: 'Easter eggs',         p: 'Uma <b>árvore</b> de carvalho nasce em cima da figura quando um slider chega em <b>15</b> com Grama / Terra / Aleatório selecionado. Um <b>creeper</b> ocupa o lugar com <b>TNT</b> selecionado — vira devagar pra fitar a câmera a cada ~16 s, brilhando branco quando acende o pavio.' },
          { h: 'Teclado',             p: '<span class="key">G</span> Grade &nbsp; <span class="key">C</span> Centro &nbsp; <span class="key">D</span> Baixar PNG &nbsp; <span class="key">I</span> Chip de info &nbsp; <span class="key">M</span> 2D/3D &nbsp; <span class="key">S</span> Som &nbsp; <span class="key">T</span> Noite &nbsp; <span class="key">Ctrl+Z</span> Desfazer &nbsp; <span class="key">Ctrl+Y</span> Refazer' },
        ]},
        { h3: '6. Sobre', items: [
          { h: 'Stack & offline',     p: 'JavaScript puro + Canvas 2D + three.js. Sem framework, sem build step. Instalável como PWA — funciona offline depois da primeira visita. Só a locale escolhida fica em <code>localStorage</code>.' },
          { h: 'Sem afiliação',       p: '<b>Block Round não é afiliado, endossado ou patrocinado pela Mojang Studios ou pela Microsoft.</b> "Minecraft" é marca registrada da Mojang Synergies AB. Texturas de bloco continuam sendo propriedade da Mojang/Microsoft — veja <code>LICENSE</code> &amp; <code>NOTICE.md</code>.' },
          { h: 'Licença & código',    p: 'Todos os direitos reservados sobre o código. Repositório: <a href="https://github.com/ViniSouza128/block-round" target="_blank" rel="noopener">github.com/ViniSouza128/block-round</a>. Projeto irmão (pixel art sem texturas): <a href="https://github.com/ViniSouza128/pixel-round" target="_blank" rel="noopener">Pixel Round</a>.' },
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
