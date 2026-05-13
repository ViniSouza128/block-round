"""Paletas RGBA por familia de bloco.

Cada paleta e um dict {nome_logico: (r, g, b, a)}. Familias relacionadas
compartilham cores-base (ex: PALETA_STONE serve de matriz pra todos os
*_ore.png). Os geradores em scripts/pixelart_pack/gen_*.py importam essas
paletas e nao usam literais RGB diretamente — assim ajustar a familia
inteira e trocar uma paleta so.
"""

# ---------------------------------------------------------------------------
# Rodada 0 — POC (TNT)
# ---------------------------------------------------------------------------

PALETA_TNT = {
    'topo_escuro':   (45, 30, 25, 255),
    'topo_claro':    (80, 55, 40, 255),
    'corpo_base':    (180, 35, 25, 255),
    'corpo_sombra':  (130, 20, 15, 255),
    'corpo_brilho':  (220, 75, 50, 255),
    'label_fundo':   (245, 235, 220, 255),
    'label_borda':   (200, 180, 160, 255),
    'texto':         (150, 25, 20, 255),
    'pavio_escuro':  (35, 25, 18, 255),
    'pavio_meio':    (75, 50, 30, 255),
    'pavio_brilho':  (165, 120, 60, 255),
}

# ---------------------------------------------------------------------------
# Rodada 1 — Mineral / Stone
# ---------------------------------------------------------------------------

# 05_stone_family — paleta cinza neutra compartilhada por stone,
# smooth_stone, cobblestone e mossy_cobblestone. A mesma paleta tambem
# alimenta a matriz dos ores em 07.
PALETA_STONE = {
    'escuro':       (78,  78,  82,  255),  # sombras profundas / pedrinhas escuras
    'meio_escuro':  (108, 108, 112, 255),  # tom abaixo da media
    'meio':         (132, 132, 136, 255),  # cor mais frequente
    'meio_claro':   (156, 156, 160, 255),  # tom acima da media
    'claro':        (182, 182, 186, 255),  # highlights
    'argamassa':    (54,  54,  58,  255),  # rejunte cobble
    'musgo':        (74,  118, 56,  255),  # mossy — verde-oliva
    'musgo_claro':  (108, 158, 78,  255),  # mossy — verde-claro
    'musgo_escuro': (52,  88,  38,  255),  # mossy — verde profundo
    'moldura':      (62,  62,  66,  255),  # borda escura smooth_stone
}

# 06_igneous — 3 rochas + 1 polida. Cada uma tem paleta propria, mas
# o conceito de "speckled" e identico (3 tons base + 2 pontos contrastantes).
PALETA_IGNEOUS_ANDESITE = {
    'base':         (134, 134, 138, 255),
    'meio':         (114, 114, 118, 255),
    'claro':        (158, 158, 162, 255),
    'ponto_preto':  (52,  52,  56,  255),
    'ponto_branco': (206, 206, 210, 255),
    'moldura':      (88,  88,  92,  255),  # polished_andesite
}

PALETA_IGNEOUS_DIORITE = {
    'base':         (202, 202, 204, 255),  # branco-cinza dominante
    'meio':         (180, 180, 184, 255),
    'claro':        (228, 228, 230, 255),
    'ponto_preto':  (60,  60,  64,  255),
    'ponto_branco': (244, 244, 246, 255),
}

PALETA_IGNEOUS_GRANITE = {
    'base':         (168, 110, 92,  255),  # rosa-terracota
    'meio':         (138, 86,  70,  255),
    'claro':        (196, 144, 124, 255),
    'ponto_preto':  (62,  46,  40,  255),
    'ponto_branco': (218, 196, 178, 255),
    'ponto_cinza':  (118, 100, 92,  255),
}

# 07_ores — reutilizam PALETA_STONE como matriz. Cada ore so adiciona
# uma "tint" de inclusao (base + sombra + brilho).
PALETA_ORE_COAL = {
    'base':   (34,  32,  34,  255),
    'sombra': (16,  16,  18,  255),
    'brilho': (62,  60,  62,  255),
}
PALETA_ORE_IRON = {
    'base':   (210, 168, 132, 255),  # salmao palido
    'sombra': (164, 124, 96,  255),
    'brilho': (236, 200, 168, 255),
}
PALETA_ORE_GOLD = {
    'base':   (228, 196, 78,  255),  # dourado vivo
    'sombra': (180, 148, 36,  255),
    'brilho': (252, 228, 130, 255),
}
PALETA_ORE_DIAMOND = {
    'base':   (108, 218, 220, 255),  # ciano cristalino
    'sombra': (66,  168, 184, 255),
    'brilho': (200, 246, 244, 255),
}
PALETA_ORE_EMERALD = {
    'base':   (62,  198, 96,  255),  # verde vivo
    'sombra': (32,  144, 62,  255),
    'brilho': (140, 232, 152, 255),
}
PALETA_ORE_LAPIS = {
    'base':   (48,  82,  186, 255),  # azul profundo
    'sombra': (28,  52,  130, 255),
    'brilho': (136, 168, 232, 255),
    'pirita': (224, 196, 92,  255),  # leves pontos dourados
}
PALETA_ORE_REDSTONE = {
    'base':   (202, 38,  30,  255),  # vermelho vivo
    'sombra': (142, 22,  18,  255),
    'brilho': (240, 96,  76,  255),
}

# 08_deepslate — matriz escura azul-cinza com estratificacao vertical.
# Os 4 ores deepslate reusam as paletas PALETA_ORE_* acima.
PALETA_DEEPSLATE = {
    'escuro':       (28,  30,  36,  255),
    'meio_escuro':  (42,  44,  50,  255),
    'meio':         (58,  60,  66,  255),  # cor mais frequente
    'meio_claro':   (76,  78,  84,  255),
    'claro':        (94,  96,  102, 255),
    'veio':         (22,  24,  28,  255),  # estratificacao vertical
}

# 09_metal_gem_blocks — grade 3x3. Diamond/emerald reusam paletas dos ores.
PALETA_METAL_COPPER = {
    'base':   (190, 110, 72,  255),
    'sombra': (148, 78,  46,  255),
    'brilho': (228, 152, 108, 255),
    'borda':  (102, 50,  30,  255),
}
PALETA_METAL_IRON = {
    'base':   (216, 216, 220, 255),
    'sombra': (172, 172, 176, 255),
    'brilho': (240, 240, 244, 255),
    'borda':  (128, 128, 132, 255),
}
PALETA_METAL_GOLD = {
    'base':   (232, 200, 74,  255),
    'sombra': (184, 152, 36,  255),
    'brilho': (252, 232, 134, 255),
    'borda':  (140, 110, 24,  255),
}
PALETA_GEM_DIAMOND = {
    'base':   PALETA_ORE_DIAMOND['base'],
    'sombra': PALETA_ORE_DIAMOND['sombra'],
    'brilho': PALETA_ORE_DIAMOND['brilho'],
    'borda':  (40,  108, 130, 255),
}
PALETA_GEM_EMERALD = {
    'base':   PALETA_ORE_EMERALD['base'],
    'sombra': PALETA_ORE_EMERALD['sombra'],
    'brilho': PALETA_ORE_EMERALD['brilho'],
    'borda':  (18,  82,  36,  255),
}

# PALETA_BEDROCK          = { ... } # 22_misc parcial — rodada 3+
# PALETA_BRICKS           = { ... }
# PALETA_GRAVEL           = { ... }

# ---------------------------------------------------------------------------
# Rodada 2 — Wood / Organic plant
# ---------------------------------------------------------------------------

# 01_planks — 6 madeiras. Convencao de chaves identica entre todas para
# que `gerar_planks_base(paleta)` em gen_planks.py funcione com qualquer
# uma. Tons: claro (highlight) > base > escuro (sombra) > separador.
# 'no_escuro' = nucleo do no; 'no_claro' = halo do no.
PALETA_PLANKS_OAK = {
    'claro':     (196, 158, 108, 255),
    'base':      (172, 132, 86,  255),  # marrom-mel
    'escuro':    (132, 96,  56,  255),
    'separador': (88,  60,  34,  255),
    'no_escuro': (104, 70,  38,  255),
    'no_claro':  (140, 102, 64,  255),
}
PALETA_PLANKS_BIRCH = {
    'claro':     (236, 222, 178, 255),
    'base':      (216, 198, 152, 255),  # creme palido
    'escuro':    (180, 158, 110, 255),
    'separador': (132, 110, 72,  255),
    'no_escuro': (140, 116, 76,  255),
    'no_claro':  (190, 168, 122, 255),
}
PALETA_PLANKS_SPRUCE = {
    'claro':     (134, 102, 70,  255),
    'base':      (108, 80,  54,  255),  # marrom escuro frio
    'escuro':    (74,  54,  36,  255),
    'separador': (52,  36,  24,  255),
    'no_escuro': (62,  44,  28,  255),
    'no_claro':  (88,  64,  44,  255),
}
PALETA_PLANKS_JUNGLE = {
    'claro':     (192, 144, 102, 255),
    'base':      (166, 118, 80,  255),  # russet quente
    'escuro':    (130, 86,  56,  255),
    'separador': (90,  58,  36,  255),
    'no_escuro': (102, 68,  42,  255),
    'no_claro':  (140, 96,  62,  255),
}
PALETA_PLANKS_ACACIA = {
    'claro':     (220, 130, 88,  255),
    'base':      (188, 104, 66,  255),  # terracota laranja-vermelho
    'escuro':    (148, 76,  46,  255),
    'separador': (104, 50,  28,  255),
    'no_escuro': (118, 60,  34,  255),
    'no_claro':  (160, 86,  54,  255),
}
PALETA_PLANKS_DARK_OAK = {
    'claro':     (94,  72,  50,  255),
    'base':      (70,  52,  34,  255),  # marrom frio profundo
    'escuro':    (44,  32,  20,  255),
    'separador': (24,  16,  10,  255),
    'no_escuro': (32,  22,  14,  255),
    'no_claro':  (54,  40,  26,  255),
}

# 02_logs — cada paleta tem chaves para casca (lateral) e miolo (top).
# Casca: cor_externa estriada verticalmente. Miolo: aneis concentricos
# que reusam os tons da paleta de planks da mesma especie.
# 'banda' (opcional): list de y onde desenhar listras escuras (so birch).
PALETA_LOG_OAK = {
    'casca_base':   (104, 78,  48,  255),
    'casca_claro':  (134, 104, 68,  255),
    'casca_escuro': (72,  52,  32,  255),
    'casca_no':     (52,  36,  22,  255),
    # miolo (top) reusa planks oak
    'miolo_centro': PALETA_PLANKS_OAK['claro'],
    'miolo_anel':   PALETA_PLANKS_OAK['base'],
    'miolo_escuro': PALETA_PLANKS_OAK['escuro'],
    'miolo_borda':  PALETA_PLANKS_OAK['separador'],
}
PALETA_LOG_BIRCH = {
    'casca_base':   (224, 218, 200, 255),  # branco icone
    'casca_claro':  (244, 240, 224, 255),
    'casca_escuro': (180, 172, 152, 255),
    'casca_no':     (40,  38,  34,  255),  # listras pretas birch
    'bandas':       [2, 6, 10, 13],         # y das listras pretas
    'miolo_centro': PALETA_PLANKS_BIRCH['claro'],
    'miolo_anel':   PALETA_PLANKS_BIRCH['base'],
    'miolo_escuro': PALETA_PLANKS_BIRCH['escuro'],
    'miolo_borda':  PALETA_PLANKS_BIRCH['separador'],
}
PALETA_LOG_SPRUCE = {
    'casca_base':   (62,  44,  28,  255),
    'casca_claro':  (88,  66,  46,  255),
    'casca_escuro': (40,  28,  18,  255),
    'casca_no':     (28,  20,  12,  255),
    'miolo_centro': PALETA_PLANKS_SPRUCE['claro'],
    'miolo_anel':   PALETA_PLANKS_SPRUCE['base'],
    'miolo_escuro': PALETA_PLANKS_SPRUCE['escuro'],
    'miolo_borda':  PALETA_PLANKS_SPRUCE['separador'],
}
PALETA_LOG_JUNGLE = {
    'casca_base':   (108, 88,  56,  255),
    'casca_claro':  (138, 116, 76,  255),
    'casca_escuro': (76,  60,  38,  255),
    'casca_no':     (48,  38,  24,  255),
    'miolo_centro': PALETA_PLANKS_JUNGLE['claro'],
    'miolo_anel':   PALETA_PLANKS_JUNGLE['base'],
    'miolo_escuro': PALETA_PLANKS_JUNGLE['escuro'],
    'miolo_borda':  PALETA_PLANKS_JUNGLE['separador'],
}
PALETA_LOG_ACACIA = {
    'casca_base':   (108, 96,  86,  255),  # acacia tem casca cinza
    'casca_claro':  (140, 124, 110, 255),
    'casca_escuro': (74,  64,  56,  255),
    'casca_no':     (44,  36,  30,  255),
    'miolo_centro': PALETA_PLANKS_ACACIA['claro'],
    'miolo_anel':   PALETA_PLANKS_ACACIA['base'],
    'miolo_escuro': PALETA_PLANKS_ACACIA['escuro'],
    'miolo_borda':  PALETA_PLANKS_ACACIA['separador'],
}
PALETA_LOG_DARK_OAK = {
    'casca_base':   (52,  38,  24,  255),
    'casca_claro':  (74,  56,  36,  255),
    'casca_escuro': (32,  22,  14,  255),
    'casca_no':     (16,  10,  6,   255),
    'miolo_centro': PALETA_PLANKS_DARK_OAK['claro'],
    'miolo_anel':   PALETA_PLANKS_DARK_OAK['base'],
    'miolo_escuro': PALETA_PLANKS_DARK_OAK['escuro'],
    'miolo_borda':  PALETA_PLANKS_DARK_OAK['separador'],
}

# 03_leaves — verde-medio cluster com folhas claras + alpha nas bordas.
PALETA_LEAVES_OAK = {
    'base':       (62,  118, 50,  255),
    'claro':      (96,  158, 72,  255),
    'escuro':     (40,  84,  34,  255),
    'borda':      (32,  68,  28,  255),
    'transparente': (0, 0, 0, 0),
}

# 12_dirt_grass_surfaces
PALETA_DIRT = {
    'base':       (130, 90,  58,  255),  # marrom dominante
    'claro':      (162, 116, 78,  255),
    'escuro':     (96,  66,  42,  255),
    'pedrinha':   (74,  52,  34,  255),  # raizes/pedrinhas escuras
    'raiz_clara': (188, 142, 96,  255),  # ocasional toque mais claro
}
PALETA_GRASS = {
    'base':       (90,  158, 60,  255),  # verde puro grama
    'claro':      (122, 196, 78,  255),
    'escuro':     (62,  124, 44,  255),
    'borda':      (52,  100, 38,  255),  # transicao com dirt no side
}
PALETA_PODZOL = {
    'base':       (138, 92,  52,  255),  # laranja escuro
    'claro':      (174, 132, 82,  255),
    'escuro':     (96,  60,  32,  255),
    'agulha':     (216, 180, 132, 255),  # agulhas claras esparsas
}
PALETA_MYCELIUM = {
    'base':       (108, 92,  112, 255),  # roxo escuro
    'claro':      (142, 122, 148, 255),
    'escuro':     (76,  62,  86,  255),
    'ponto':      (180, 168, 180, 255),  # pontinhos cinza-claros
}
PALETA_MOSS = {
    'base':       (66,  112, 50,  255),  # verde musgo
    'claro':      (102, 152, 76,  255),
    'escuro':     (44,  82,  36,  255),
    'borda':      (32,  62,  28,  255),
}

# PALETA_HAY              = { ... } # 17_crops_organic — rodada 4
# PALETA_MELON            = { ... }
# PALETA_PUMPKIN          = { ... }
# PALETA_MUSHROOM_BROWN   = { ... } # 18_mushroom_bone parcial — rodada 4
# PALETA_MUSHROOM_RED     = { ... }

# ---------------------------------------------------------------------------
# Rodada 3 — Terrain / Surfaces / Nether / Ice / End (placeholders)
# ---------------------------------------------------------------------------

# PALETA_SAND             = { ... } # 10_sand_sandstone
# PALETA_SANDSTONE        = { ... }
# PALETA_RED_SANDSTONE    = { ... }
# PALETA_ICE              = { ... } # 11_ice_snow
# PALETA_ICE_BLUE         = { ... }
# PALETA_SNOW             = { ... }
# PALETA_DIRT             = { ... } # 12_dirt_grass_surfaces
# PALETA_GRASS            = { ... }
# PALETA_PODZOL           = { ... }
# PALETA_MYCELIUM         = { ... }
# PALETA_MOSS             = { ... }
# PALETA_NETHER_RACK      = { ... } # 13_nether
# PALETA_NETHER_BRICKS    = { ... }
# PALETA_MAGMA            = { ... } # strip 16x48
# PALETA_SOUL_SAND        = { ... }
# PALETA_SHROOMLIGHT      = { ... }
# PALETA_CRYING_OBSIDIAN  = { ... }
# PALETA_END_STONE        = { ... } # 14_end_obsidian
# PALETA_OBSIDIAN         = { ... }
# PALETA_BONE             = { ... } # 18_mushroom_bone parcial
# PALETA_GLOWSTONE        = { ... } # 22_misc parcial
# PALETA_SPONGE           = { ... }

# ---------------------------------------------------------------------------
# Rodada 4 — Crafted / Colored / Translucent / Quartz / Prismarine
# ---------------------------------------------------------------------------

# PALETA_WOOL_WHITE       = { ... } # 04_wools (8 cores)
# PALETA_WOOL_BLACK       = { ... }
# PALETA_WOOL_RED         = { ... }
# PALETA_WOOL_ORANGE      = { ... }
# PALETA_WOOL_YELLOW      = { ... }
# PALETA_WOOL_GREEN       = { ... }
# PALETA_WOOL_BLUE        = { ... }
# PALETA_WOOL_LIGHT_BLUE  = { ... }
# PALETA_PRISMARINE       = { ... } # 15_prismarine_sea (incl strips)
# PALETA_SEA_LANTERN      = { ... } # strip 16x80
# PALETA_QUARTZ           = { ... } # 16_quartz
# PALETA_BOOKSHELF        = { ... } # 19_crafted_workstations
# PALETA_CRAFTING_TABLE   = { ... }
# PALETA_FURNACE          = { ... }
# PALETA_GLASS            = { ... } # 21_translucent (com alpha!)
# PALETA_SLIME            = { ... }
# PALETA_HONEY            = { ... }
