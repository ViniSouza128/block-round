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
# Rodada 2 — Wood / Organic plant (placeholders)
# ---------------------------------------------------------------------------

# PALETA_PLANKS_OAK       = { ... } # 01_planks
# PALETA_PLANKS_BIRCH     = { ... }
# PALETA_PLANKS_SPRUCE    = { ... }
# PALETA_PLANKS_JUNGLE    = { ... }
# PALETA_PLANKS_ACACIA    = { ... }
# PALETA_PLANKS_DARK_OAK  = { ... }
# PALETA_LOG_OAK          = { ... } # 02_logs (side+top variantes)
# PALETA_LOG_BIRCH        = { ... }
# PALETA_LOG_SPRUCE       = { ... }
# PALETA_LOG_JUNGLE       = { ... }
# PALETA_LOG_ACACIA       = { ... }
# PALETA_LOG_DARK_OAK     = { ... }
# PALETA_LEAVES_OAK       = { ... } # 03_leaves
# PALETA_HAY              = { ... } # 17_crops_organic
# PALETA_MELON            = { ... }
# PALETA_PUMPKIN          = { ... }
# PALETA_MUSHROOM_BROWN   = { ... } # 18_mushroom_bone parcial
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
