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
# Rodada 1 — Mineral / Stone (placeholders)
# ---------------------------------------------------------------------------

# PALETA_STONE = { ... }            # 05_stone_family
# PALETA_IGNEOUS_ANDESITE = { ... } # 06_igneous (cinza-medio)
# PALETA_IGNEOUS_DIORITE  = { ... } # 06_igneous (branco-cinza)
# PALETA_IGNEOUS_GRANITE  = { ... } # 06_igneous (rosa-terracota)
# PALETA_ORE_MATRIX_STONE = { ... } # 07_ores — base = stone
# PALETA_DEEPSLATE        = { ... } # 08_deepslate (cinza-azulado escuro)
# PALETA_METAL_COPPER     = { ... } # 09_metal_gem
# PALETA_METAL_IRON       = { ... }
# PALETA_METAL_GOLD       = { ... }
# PALETA_GEM_DIAMOND      = { ... }
# PALETA_GEM_EMERALD      = { ... }
# PALETA_BEDROCK          = { ... } # 22_misc parcial
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
