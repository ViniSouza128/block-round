#!/usr/bin/env python3
"""
Generate TEXTURE_VARIATION_PROMPTS.md — one ChatGPT prompt per PNG in
textures-1024/, grouped by folder so visually-related blocks (all
planks, all wools, all log pairs, all ores-in-deepslate…) appear next
to each other and share their context paragraph.

Re-run after adding/removing textures. Idempotent (full rewrite each
run, so the .md never drifts from the actual folder layout).

    python tools/gen_variation_prompts.py
"""

from pathlib import Path
from collections import OrderedDict
import sys

ROOT = Path(__file__).resolve().parent.parent
TEX_DIR = ROOT / "textures-1024"
OUT = ROOT / "TEXTURE_VARIATION_PROMPTS.md"

# ---------------------------------------------------------------------------
# Base style block shared by every prompt. Pulled out so a tweak to one
# constraint propagates to all 127 prompts in one place.
# ---------------------------------------------------------------------------
BASE_STYLE = """\
**Pedido**: gerar uma **variação** da textura anexada para uso em um bloco
estilo Minecraft.

**Restrições de estilo (valem para toda variação):**
- **Saída**: PNG quadrado **1024×1024**, sem padding, sem moldura, sem texto,
  sem assinatura, sem marca d'água.
- **Estética pixel-art preservada**: a imagem original é um sprite 16×16
  ampliado com nearest-neighbor (cada pixel original = bloco 64×64 sólido).
  A saída deve manter exatamente esse aspecto — **bordas de pixel duras**,
  **sem antialiasing**, **sem gradientes suaves**, **sem desfoque**. Nada
  deve parecer "pintura digital" — tem que parecer um sprite 16×16 esticado.
- **Tileável sem costura**: a textura é repetida em várias faces do bloco
  no jogo. **A borda esquerda precisa casar com a direita**, e a **superior
  com a inferior**. Evite elementos visuais que toquem só uma borda.
- **Paleta dentro da família**: não mudar a identidade de cor do bloco
  (ver a "identidade" abaixo). Variação é em padrão, distribuição, ângulo
  dos elementos — não em cor base.
- **Reconhecibilidade**: um jogador olhando a textura deve dizer "isso é
  X" (o mesmo bloco do input), não "isso é um bloco diferente".
"""

# ---------------------------------------------------------------------------
# Per-group context paragraph. Added once at the top of each folder section
# so the user can paste it as the "system intro" when generating the whole
# group in one chat session.
# ---------------------------------------------------------------------------
GROUP_INTRO = {
    "01_planks": (
        "Os 6 arquivos desta pasta são **tábuas de madeira** — uma textura "
        "única por tipo de madeira. Para coerência da família, mantenha o "
        "**padrão das tábuas idêntico em todas** (mesma largura de tábua "
        "horizontal — 4 pixels —, mesma densidade de nós, mesma direção de "
        "grão). O que muda entre arquivos é **só a cor da madeira**."
    ),
    "02_logs": (
        "Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, "
        "grão vertical) e **top** (corte transversal com anéis concêntricos). "
        "Side e top do MESMO tipo precisam combinar (mesma cor de casca / "
        "mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — "
        "mesma quantidade de anéis no top, mesma rugosidade da casca no "
        "side — só muda a paleta."
    ),
    "03_leaves": (
        "Só folhas de carvalho neste catálogo. Densidade de aglomerado de "
        "folhas e tom verde devem permanecer reconhecíveis."
    ),
    "04_wools": (
        "**Lãs coloridas**. As 8 cores DEVEM compartilhar o mesmo padrão de "
        "tricô / fibra — exatamente a mesma trama, mesmo espaçamento, mesmo "
        "ângulo. O ÚNICO eixo de variação entre os arquivos é a **cor base**."
    ),
    "05_stone_family": (
        "Família da **pedra cinza**. `stone` é a base lisa-rugosa, "
        "`smooth_stone` é mais homogênea (pedra cozida), `cobblestone` tem "
        "pedrinhas individuais visíveis, `mossy_cobblestone` é cobble com "
        "manchas verdes de musgo. Paleta cinza neutra unificada entre os 4."
    ),
    "06_igneous": (
        "**Rochas ígneas**. Andesite (cinza), granite (rosado), diorite "
        "(branco com pontos pretos). Versões polidas são as mesmas mas "
        "com superfície lisa em vez de speckled. Mesma escala de mancha "
        "entre versões rugosa e polida do mesmo material."
    ),
    "07_ores_stone_matrix": (
        "**Minérios em matriz de pedra cinza comum**. A matriz cinza deve "
        "ser EXATAMENTE igual à `stone.png` (gere `stone.png` primeiro, "
        "depois aplique as inclusões de minério por cima). O que varia é "
        "só a cor e forma dos cristais/grãos do minério."
    ),
    "08_deepslate": (
        "**Deepslate e seus minérios**. Mesma lógica do grupo de pedra: "
        "a matriz escura precisa ser idêntica à `deepslate.png` (rocha "
        "azul-cinza escura, estratificada). Os ores deepslate substituem "
        "só as inclusões; a matriz cinza-escuro permanece igual."
    ),
    "09_metal_gem_blocks": (
        "**Blocos sólidos de metal/gema** (a versão refinada/empilhada do "
        "minério). Todos compartilham o mesmo **layout de grade 3×3** "
        "(parece 9 lingotes/gemas dispostos em quadrado). Só muda a cor "
        "e o material visual (metal polido vs gema cristalina)."
    ),
    "10_sand_sandstone": (
        "**Areia e arenito**. `sand` é areia solta (grãos finos). "
        "`sandstone` é o bloco esculpido — lateral tem ranhuras verticais "
        "de erosão. `sandstone_top/bottom` são tampas lisas. "
        "`red_sandstone_top` é a versão vermelha/laranja da tampa lisa."
    ),
    "11_ice_snow": (
        "**Gelo e neve** — paleta fria. `ice` translúcido com rachaduras, "
        "`ice_packed` opaco branco-azulado, `blue_ice` saturado azul-vidro, "
        "`snow` neve fofa branca pura. Mantenha a sensação de frio/úmido."
    ),
    "12_dirt_grass_surfaces": (
        "**Superfícies de chão / cobertura vegetal**. Todas que terminam em "
        "`_side` têm **dirt na metade inferior e a cobertura específica na "
        "superior** (grama verde no topo, mycelium roxo no topo, podzol com "
        "agulhas claras no topo). A parte dirt deve ser idêntica à `dirt.png` "
        "em todos os _side."
    ),
    "13_nether": (
        "**Dimensão Nether** — paleta vermelha/escura. `netherrack` é a rocha "
        "vermelha base do bioma. `magma_frame0/1/2` são **3 frames de uma "
        "animação** — geram em sequência, frame N flui para N+1 (cracks de "
        "lava se movendo lentamente). `crying_obsidian` tem lágrimas magenta "
        "vivas no obsidian roxo escuro."
    ),
    "14_end_obsidian": (
        "**End Stone** e **Obsidian** — visualmente opostas mas agrupadas por "
        "raridade/peso. End stone é beige claro speckled; obsidian é roxo "
        "muito escuro quase preto, com reflexos magenta sutis."
    ),
    "15_prismarine_sea": (
        "**Família prismarine** (monumento submarino). `prismarine_rough_*` "
        "é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é "
        "uma **animação de 5 frames** (luz pulsante). Os frames devem fluir "
        "suavemente um para o outro. Paleta turquesa-ciano luminosa."
    ),
    "16_quartz": (
        "**Bloco de quartzo** com 3 faces distintas. Top tem tampa lisa "
        "com borda fina. Side tem colunas verticais estriadas. Bottom é "
        "uma base lisa. As 3 faces compartilham o branco quartz puro."
    ),
    "17_crops_organic": (
        "**Plantações e alimentos** — blocos com side+top distintos. "
        "Hay (palha): side mostra feixes verticais amarrados, top mostra "
        "o corte transversal dos feixes. Melon (melancia): side verde "
        "listrado, top mostra a polpa rosa. Pumpkin (abóbora): side "
        "laranja com gomos verticais, top com talo/cabo central."
    ),
    "18_mushroom_bone": (
        "**Cogumelos gigantes e bloco de osso**. Bone block tem fibras "
        "verticais na side e end-grain no top (parece um osso longo "
        "cortado). Mushroom red é cogumelo vermelho com pontos brancos "
        "(amanita). Mushroom brown é mais terroso, sem pontos."
    ),
    "19_crafted_workstations": (
        "**Blocos de bancada**. Crafting table: top mostra grade 3×3 de "
        "receita, side mostra tábuas+ferramentas, front tem motivo de "
        "martelo/serra. Furnace: top liso, side com sulcos sutis, front "
        "tem a abertura retangular escura (apagada/off). Bookshelf: "
        "lombadas de livros enfileiradas com cores variadas."
    ),
    "20_tnt": (
        "**TNT** — 3 faces de um único cubo. Top: pavio enrolado no "
        "centro. Side: caixa vermelha com **\"TNT\" em letras brancas "
        "visíveis** e listras diagonais amarelas/pretas de aviso (esse "
        "texto e o padrão de aviso DEVEM permanecer legíveis). Bottom: "
        "vermelho liso (base da carga explosiva)."
    ),
    "21_translucent": (
        "**Blocos translúcidos / gelatinosos**. Glass tem só uma fina "
        "borda de moldura, miolo praticamente vazio (transparência "
        "sugerida com leve tom azul-claro). Slime é gel verde com "
        "padrão de favo de mel sutil. Honey é gel âmbar — top/side/"
        "bottom têm tonalidades levemente diferentes."
    ),
    "22_misc_solids": (
        "**Sólidos diversos** que não pertencem a nenhuma família "
        "específica. Bedrock (rocha quase preta, irregular, fissuras). "
        "Bricks (parede de tijolos vermelhos com argamassa). Glowstone "
        "(aglomerado luminoso dourado-amarelado). Gravel (cascalho solto, "
        "pedrinhas redondas cinza). Sponge (espuma porosa amarela)."
    ),
}

# ---------------------------------------------------------------------------
# Per-PNG identity line. Stems with sub-faces (_top, _side, _bottom, _front)
# or animation frames (_frame0..N) carry their face/frame note here too.
#
# Keep each entry to 1–2 lines — the BASE_STYLE block already covers
# generic constraints. Don't repeat them.
# ---------------------------------------------------------------------------
IDENTITY = {
    # 01 planks
    "acacia_planks": "tábuas de **acácia** — tom laranja-avermelhado quente / terracota, saturação média. Tábuas horizontais de 4 px, alguns nós pequenos.",
    "birch_planks": "tábuas de **bétula** — tom creme-pálido com sutil aquecimento. As mais claras da família. Nós escuros pequenos visíveis.",
    "dark_oak_planks": "tábuas de **carvalho escuro** — marrom frio profundo, quase preto nos nós. Tom mais pesado da família.",
    "jungle_planks": "tábuas de **selva** — marrom-russet quente saturado, tom \"madeira tropical\".",
    "oak_planks": "tábuas de **carvalho** — marrom-mel clássico (a referência da família).",
    "spruce_planks": "tábuas de **abeto** — marrom escuro frio levemente acinzentado.",

    # 02 logs — bark / side variants
    "oak_log":        "**casca lateral** de tronco de carvalho. Grão vertical, marrom-bege uniforme, com nervuras finas verticais (não tábua horizontal!).",
    "log_birch":      "casca lateral de tronco de **bétula**. Branca com estrias horizontais pretas curtas (marca registrada da bétula).",
    "birch_log":      "variante alternativa da casca lateral de tronco de **bétula** — mesma identidade (branca + estrias pretas) mas pode diferir levemente em distribuição/rugosidade.",
    "log_spruce":     "casca lateral de tronco de **abeto** — marrom escuro frio, grão vertical mais pronunciado, sulcos mais profundos.",
    "spruce_log":     "variante alternativa de casca de **abeto** — mesma identidade.",
    "log_jungle":     "casca lateral de tronco de **selva** — marrom-russet quente, grão menos pronunciado que abeto.",
    "log_acacia":     "casca lateral de tronco de **acácia** — cinza-marrom esverdeado/oliva, grão vertical sutil.",
    "log_big_oak":    "casca lateral de tronco de **carvalho escuro** (\"big oak\" no nome interno) — marrom muito escuro quase preto.",
    "dark_oak_log":   "variante alternativa de casca de **carvalho escuro** — mesma identidade.",

    # 02 logs — top / end-cut variants
    "oak_log_top":      "**corte transversal** (topo) de tronco de **carvalho**. Anéis concêntricos visíveis, centro levemente off-center. Marrom-mel.",
    "log_birch_top":    "corte transversal de tronco de **bétula**. Anéis claros, casca branca na borda externa, centro levemente mais escuro.",
    "log_spruce_top":   "corte transversal de tronco de **abeto** — anéis mais escuros, paleta marrom frio.",
    "log_jungle_top":   "corte transversal de tronco de **selva** — anéis em russet quente.",
    "log_acacia_top":   "corte transversal de tronco de **acácia** — anéis em tom oliva-bege.",
    "log_big_oak_top":  "corte transversal de tronco de **carvalho escuro** — anéis muito escuros, centro quase preto.",

    # 03 leaves
    "leaves_oak": "**folhas de carvalho** — aglomerado denso de pequenas folhas verde-médio. Algumas folhas mais claras espalhadas. Padrão deve dar sensação de massa folhada vista de fora.",

    # 04 wools (same knit, different hue)
    "white_wool":      "lã **branca** — branco-creme nevado levemente off-white. Trama de tricô visível em toda a textura.",
    "light_blue_wool": "lã **azul-claro** — azul-céu suave, baixa saturação. Mesma trama da white_wool, só muda a cor.",
    "blue_wool":       "lã **azul** — azul médio saturado, levemente frio.",
    "green_wool":      "lã **verde** — verde-folha médio levemente dessaturado.",
    "yellow_wool":     "lã **amarela** — amarelo saturado quente, leve toque alaranjado.",
    "orange_wool":     "lã **laranja** — laranja saturado, entre amarelo e vermelho.",
    "red_wool":        "lã **vermelha** — vermelho quente levemente abafado (não escarlate puro).",
    "black_wool":      "lã **preta** — quase preto, com a trama de tricô ainda perceptível em um tom levemente mais quente.",

    # 05 stone family
    "stone":              "**pedra** Minecraft clássica — cinza médio levemente rugoso, manchas claras/escuras sutis, sem elementos dominantes. Essa é a matriz de referência para todos os arquivos de `07_ores_stone_matrix/`.",
    "smooth_stone":       "**pedra lisa** (pedra cozida) — cinza médio mais homogêneo que `stone.png`, com uma fina moldura escura na borda do bloco (marca de cocção). Sem pedras individuais visíveis.",
    "cobblestone":        "**paralelepípedo (cobble)** — pedrinhas individuais empilhadas com argamassa cinza-escura entre elas. Tons de cinza variados entre as pedras.",
    "mossy_cobblestone":  "**cobble musgoso** — mesma estrutura do cobble, mas com manchas verdes irregulares de musgo cobrindo ~30% da superfície. O musgo deve parecer crescido, não pintado.",

    # 06 igneous
    "andesite":          "**andesito** — cinza médio com pequenas inclusões pretas e brancas espalhadas (textura speckled fina).",
    "polished_andesite": "andesito **polido** — superfície lisa cinza médio uniforme, com uma sutil grade clara/escura sugerindo blocos cortados.",
    "granite":           "**granito** — base rosada-bege com pequenos pontos pretos, brancos e cinza espalhados.",
    "diorite":           "**diorito** — base branca/clara dominante com pontos pretos espalhados (\"granito invertido\").",

    # 07 ores in stone matrix
    "coal_ore":      "**carvão em pedra**. Matriz idêntica à `stone.png`. Por cima, manchas pretas amorfas (carvão) ocupando ~30% da área, formato irregular.",
    "iron_ore":      "**ferro em pedra**. Matriz idêntica à `stone.png`. Inclusões em tom **rosa-alaranjado/salmon** pálido, irregulares.",
    "gold_ore":      "**ouro em pedra**. Matriz `stone.png`. Inclusões amarelo-dourado vivo.",
    "diamond_ore":   "**diamante em pedra**. Matriz `stone.png`. Inclusões **ciano-pálido cristalinas** com pequeno toque de geometria angular (sugerindo gemas).",
    "emerald_ore":   "**esmeralda em pedra**. Matriz `stone.png`. Inclusões **verde-vivo cristalinas** angulares.",
    "redstone_ore":  "**redstone em pedra**. Matriz `stone.png`. Pontos pequenos vermelho-vivos espalhados (sugerindo poeira vermelha brilhante).",
    "lapis_ore":     "**lápis-lazúli em pedra**. Matriz `stone.png`. Inclusões **azul-profundo** com leves pontos brancos/dourados (calcita+pirita).",

    # 08 deepslate
    "deepslate":              "**deepslate** — rocha cinza-azulada escura, com estratificação vertical sutil (linhas verticais paralelas). MUITO escura mas com variação interna. Essa é a matriz de referência para os ores deepslate.",
    "deepslate_diamond_ore":  "**diamante em deepslate**. Matriz idêntica à `deepslate.png`. Inclusões ciano-cristalinas com mais luminosidade aparente (contraste com o fundo escuro).",
    "deepslate_emerald_ore":  "**esmeralda em deepslate**. Matriz `deepslate.png`. Inclusões verde-vivo cristalinas.",
    "deepslate_gold_ore":     "**ouro em deepslate**. Matriz `deepslate.png`. Inclusões dourado-vivo, alto contraste com fundo escuro.",
    "deepslate_iron_ore":     "**ferro em deepslate**. Matriz `deepslate.png`. Inclusões rosa-alaranjado pálido.",

    # 09 metal/gem blocks
    "iron_block":    "**bloco de ferro** — grade 3×3 de lingotes em tom prateado/cinza-claro polido, com sutil contorno mais escuro entre cada lingote.",
    "gold_block":    "**bloco de ouro** — grade 3×3 amarelo-dourado polido.",
    "diamond_block": "**bloco de diamante** — grade 3×3 ciano-pálido cristalino, faces facetadas levemente angulares.",
    "emerald_block": "**bloco de esmeralda** — grade 3×3 verde-vivo cristalino, facetas semelhantes ao diamante.",
    "copper_block":  "**bloco de cobre** — grade 3×3 em laranja-marrom polido (cobre não-oxidado, sem patina verde).",

    # 10 sand
    "sand":               "**areia** — grãos finos cor de areia clara (beige claro), ligeiramente granulada, uniforme.",
    "sandstone":          "**arenito (lateral)** — bege/beige médio com **ranhuras verticais** sutis (erosão). Identidade da face lateral do bloco arenito.",
    "sandstone_top":      "**arenito (topo)** — tampa lisa do bloco arenito, sem ranhuras verticais. Beige mais uniforme, com uma fina linha de moldura escura ao redor.",
    "sandstone_bottom":   "**arenito (base)** — tampa inferior, similar ao top mas sem moldura escura.",
    "red_sandstone_top":  "**arenito vermelho (topo)** — versão laranja-avermelhada da tampa sandstone_top. Mesma estrutura, paleta quente.",

    # 11 ice/snow
    "ice":         "**gelo** — branco-azulado translúcido com **rachaduras finas** irregulares espalhadas. Sugestão de transparência (mas é PNG opaco — usar tom claro para sugerir).",
    "ice_packed":  "**gelo compacto** — branco-azulado mais opaco, **sem rachaduras**, superfície mais lisa que `ice`.",
    "blue_ice":    "**gelo azul** — saturação maior, azul-vidro brilhante, superfície quase espelhada (mas mantendo aspecto pixelado).",
    "snow":        "**neve** — branco puro com leve variação azulada (sombras suaves entre flocos), aspecto fofo/grumoso.",

    # 12 dirt/grass surfaces
    "dirt":              "**terra** — marrom escuro com pequenos pontos mais claros (pedrinhas/raízes). Sem grama. Essa é a referência para a metade inferior de todos os `_side` deste grupo.",
    "grass_block_top":   "**topo de bloco de grama** — manto de grama verde-médio com variação sutil (folhinhas mais claras e mais escuras). Sem terra visível.",
    "grass_block_side":  "**lateral de bloco de grama** — metade inferior é `dirt.png`, metade superior tem **a borda de grama caindo sobre a terra** (linha irregular onde a grama termina). Borda de grama verde-médio.",
    "moss_block":        "**bloco de musgo** — superfície verde-lustroso uniforme, mais densa e úmida que grama, sem nada de terra exposta.",
    "mycelium_top":      "**topo de bloco de micélio** — superfície roxo-acinzentada fungal com pequenos pontos brancos (esporos) espalhados.",
    "mycelium_side":     "**lateral de bloco de micélio** — metade inferior `dirt.png`, metade superior tem borda de micélio roxo-acinzentado caindo sobre a terra.",
    "dirt_podzol_top":   "**topo de bloco de podzol** — superfície marrom-escura coberta de **agulhas claras** (pinheiro), pontos esparsos.",
    "dirt_podzol_side":  "**lateral de bloco de podzol** — metade inferior `dirt.png`, metade superior tem borda de podzol (terra com agulhas claras) caindo sobre a terra.",

    # 13 nether
    "netherrack":      "**netherrack** — rocha vermelha-bordô do Nether, com **veias mais escuras** e padrão irregular tipo \"carne\" fibrosa.",
    "nether_bricks":   "**tijolos do Nether** — padrão de parede de tijolos pequenos em marrom muito escuro, com argamassa preta entre eles.",
    "soul_sand":       "**areia das almas** — areia marrom-escura com **3 marcas de rosto/face fantasmagórico** sutis cavadas na superfície. Identidade do bloco vem dessas faces.",
    "magma_frame0":    "**magma — frame 0/3** de animação. Superfície de pedra preta com **rachaduras de lava laranja-amarelo** brilhante. Frame inicial: rachaduras mais finas/quietas.",
    "magma_frame1":    "**magma — frame 1/3** de animação. Mesma identidade, rachaduras um pouco mais grossas/brilhantes que frame 0 (lava se movendo).",
    "magma_frame2":    "**magma — frame 2/3** de animação. Rachaduras mais luminosas, prestes a voltar para o frame 0 (loop).",
    "shroomlight":     "**shroomlight** — cogumelo luminoso laranja-dourado do Nether. Superfície bumpy/orgânica com tom emissivo dourado vivo.",
    "crying_obsidian": "**obsidian chorando** — base obsidian roxo-escuro quase preto, com **lágrimas/cristais magenta-vivo** verticais escorrendo (4-6 lágrimas verticais).",

    # 14 end/obsidian
    "end_stone": "**end stone** — pedra do End. Beige-amarelado claro com **pequenas inclusões pretas densas** (pontos amorfos espalhados).",
    "obsidian":  "**obsidian** — vidro vulcânico **roxo muito escuro, quase preto**, com **reflexos magenta sutis** em algumas áreas (sugerindo brilho vítreo).",

    # 15 prismarine / sea
    "prismarine_bricks":         "**prismarine bricks** — padrão de tijolos pequenos em ciano-turquesa, com argamassa azul-escura entre eles.",
    "prismarine_dark":           "**prismarine escuro** — variante escura, padrão carved/esculpido com tom teal muito escuro quase preto.",
    "prismarine_rough_frame0":   "**prismarine rough — frame 0/4** de animação. Superfície turquesa-ciano com padrão de **ondulações suaves**. Frame inicial da onda.",
    "prismarine_rough_frame1":   "prismarine rough — **frame 1/4**. Ondulações deslocadas um pouco para um lado em relação ao frame 0.",
    "prismarine_rough_frame2":   "prismarine rough — **frame 2/4**. Ondulações no ponto médio do ciclo.",
    "prismarine_rough_frame3":   "prismarine rough — **frame 3/4**. Ondulações prestes a voltar ao frame 0 (loop).",
    "sea_lantern_frame0":        "**sea lantern — frame 0/5** de animação luminosa. Superfície ciano-claro com **cristais brilhantes** dispostos em padrão. Frame inicial: brilho mais sutil.",
    "sea_lantern_frame1":        "sea lantern — **frame 1/5**. Brilho aumentando levemente em alguns cristais.",
    "sea_lantern_frame2":        "sea lantern — **frame 2/5**. Pico de brilho — máximo de luminosidade nos cristais.",
    "sea_lantern_frame3":        "sea lantern — **frame 3/5**. Brilho diminuindo, voltando ao estado mais sutil.",
    "sea_lantern_frame4":        "sea lantern — **frame 4/5**. Frame mais sutil, prestes a fazer loop com frame 0.",

    # 16 quartz
    "quartz_block_top":     "**topo de bloco de quartzo** — tampa lisa branca quartz puro, com uma **fina moldura escura** ao redor (sulco na borda).",
    "quartz_block_side":    "**lateral de bloco de quartzo** — colunas verticais estriadas (3-4 colunas paralelas), brancas quartz com sombras finas entre as colunas.",
    "quartz_block_bottom":  "**base de bloco de quartzo** — branca quartz lisa, sem moldura escura ao redor (mais limpa que o top).",

    # 17 crops / organic
    "hay_block_side":   "**lateral de fardo de feno** — feixes verticais de palha dourada amarrados por uma **corda horizontal** no meio. Tons dourado-amarelo.",
    "hay_block_top":    "**topo de fardo de feno** — corte transversal dos feixes, mostrando os caules amarrados em padrão circular concêntrico (dourado).",
    "melon_side":       "**lateral de melancia** — exterior **verde com listras verticais** (claras e escuras alternadas).",
    "melon_top":        "**topo de melancia** — corte transversal mostrando a **polpa rosa-avermelhada** com sementes pretas pequenas espalhadas, borda fina verde.",
    "pumpkin_face_off": "**lateral de abóbora não esculpida** — exterior laranja com **gomos verticais** (cristas verticais paralelas), sem face esculpida.",
    "pumpkin_side":     "**lateral de abóbora padrão** — versão padrão (similar ao face_off mas pode ter variação sutil de cor).",
    "pumpkin_top":      "**topo de abóbora** — laranja com **cabo/talo central** verde-marrom no centro.",

    # 18 mushroom / bone
    "bone_block_side":              "**lateral de bloco de osso** — fibras verticais cremes/brancas (como osso longo cortado).",
    "bone_block_top":               "**topo de bloco de osso** — corte transversal mostrando estriações concêntricas em creme/branco.",
    "mushroom_block_skin_red":      "**pele de cogumelo gigante vermelho** — superfície vermelha vibrante com **pontos brancos circulares** espalhados (amanita clássica).",
    "mushroom_block_skin_brown":    "**pele de cogumelo gigante marrom** — superfície marrom-canela uniforme, sem pontos (mais terrosa que a vermelha).",

    # 19 crafted workstations
    "crafting_table_top":     "**topo de bancada de trabalho** — superfície de madeira com **grade 3×3 cavada** (linhas claras formando 9 quadrados).",
    "crafting_table_side":    "**lateral de bancada de trabalho** — tábuas de madeira com silhuetas escuras de **ferramentas** (serra, martelo).",
    "crafting_table_front":   "**frente de bancada de trabalho** — tábuas com motivo central de **martelo+serra** cruzados.",
    "furnace_top":            "**topo de fornalha** — superfície de pedra cinza lisa, idêntica à `smooth_stone` (sem nada por cima).",
    "furnace_side":           "**lateral de fornalha** — pedra cinza com **sulcos verticais sutis** (rebites/painéis).",
    "furnace_front_off":      "**frente de fornalha (desligada)** — pedra cinza com **abertura retangular escura central** (entrada de combustão, vazia).",
    "bookshelf":              "**estante de livros** — fileira horizontal de **lombadas de livros coloridas** (vermelhas, azuis, marrons, amarelas, espessuras variadas) sobre prateleira de madeira em cima e embaixo.",

    # 20 tnt
    "tnt_top":    "**topo de TNT** — superfície vermelha com **pavio enrolado em espiral** preto/cinza no centro.",
    "tnt_side":   "**lateral de TNT** — caixa vermelha com **as letras \"TNT\"** em branco no centro (LEGÍVEIS, NÃO DISTORÇA O TEXTO) e listras diagonais amarelas+pretas de aviso nas bordas superior e inferior.",
    "tnt_bottom": "**base de TNT** — vermelho liso, mais uniforme que o top (sem pavio).",

    # 21 translucent
    "glass":       "**vidro** — predominantemente **transparente / claro** (cor de fundo neutra clara), com apenas uma **fina moldura azul-claro/branco** ao redor sugerindo a borda da vidraça. Centro praticamente vazio.",
    "slime":       "**slime** — verde-claro translúcido com padrão de **favo de mel/escamas hexagonais** sutil. Cor de gel.",
    "honey_top":   "**topo de mel** — superfície âmbar dourada brilhante, com sugestão sutil de viscosidade (gradiente leve mas mantendo pixel-art).",
    "honey_side":  "**lateral de mel** — âmbar mais escuro que o top, com **gotas/escorrimento** sutil descendo.",
    "honey_bottom":"**base de mel** — âmbar uniforme similar ao top, mas levemente mais escuro.",

    # 22 misc
    "bedrock":   "**bedrock** — rocha **quase preta** com fissuras irregulares cinza-escuro. Aspecto inquebrável/imune. Padrão caótico, sem geometria reconhecível.",
    "bricks":    "**tijolos** clássicos — parede de tijolos pequenos **vermelho-terracota** com **argamassa cinza-clara** entre eles. Padrão de fiada deslocada (offset entre fiadas).",
    "glowstone": "**glowstone** — aglomerado de **bolinhas/cristais dourado-amarelo luminosos** (cluster orgânico), com aparência emissiva.",
    "gravel":    "**cascalho** — **pedrinhas redondas pequenas** cinza claras e escuras misturadas, distribuição aleatória.",
    "sponge":    "**esponja** — superfície **amarelo-mostarda porosa** com **buracos pequenos circulares** espalhados (poros da esponja).",
}

# ---------------------------------------------------------------------------
# Build the .md
# ---------------------------------------------------------------------------

def main():
    if not TEX_DIR.exists():
        print(f"error: {TEX_DIR} not found", file=sys.stderr)
        return 1

    # Discover groups (subfolders) in numeric order.
    groups = sorted(
        [p for p in TEX_DIR.iterdir() if p.is_dir() and not p.name.startswith("_")],
        key=lambda p: p.name,
    )

    missing = []
    out = []
    out.append("# Prompts de variação de textura — `textures-1024/`")
    out.append("")
    out.append(
        "Um prompt por PNG, agrupado por pasta na mesma ordem do explorador "
        "de arquivos. Use a estratégia que faz sentido pro seu fluxo:"
    )
    out.append("")
    out.append(
        "- **Por grupo inteiro**: abra um chat por pasta, faça upload de "
        "TODOS os PNGs da pasta, cole o **intro do grupo** + **base de estilo** "
        "uma vez, e depois cole cada prompt individual conforme rodar."
    )
    out.append(
        "- **Por arquivo isolado**: cada prompt já é auto-suficiente — base "
        "de estilo + intro do grupo + identidade do bloco — então funciona "
        "em chat virgem também."
    )
    out.append("")
    out.append(
        "> ⚠️ Sempre faça upload do PNG **original 1024×1024** anexado ao "
        "prompt. O modelo vai usar a imagem como referência visual; o texto "
        "só descreve o que preservar e o que variar."
    )
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Base de estilo (idêntica para todas as variações)")
    out.append("")
    out.append(BASE_STYLE)
    out.append("")
    out.append("---")
    out.append("")

    for grp in groups:
        intro = GROUP_INTRO.get(grp.name, "")
        out.append(f"## `{grp.name}/`")
        out.append("")
        if intro:
            out.append(f"**Intro do grupo (cole 1× no início do chat):** {intro}")
            out.append("")
        pngs = sorted([p for p in grp.iterdir() if p.suffix == ".png"], key=lambda p: p.name)
        for png in pngs:
            stem = png.stem
            ident = IDENTITY.get(stem)
            out.append(f"### `{png.name}`")
            out.append("")
            if not ident:
                missing.append(f"{grp.name}/{png.name}")
                out.append(
                    "> ⚠️ **Sem identidade definida** — adicione em "
                    "`tools/gen_variation_prompts.py` (dict `IDENTITY`)."
                )
                out.append("")
                continue
            out.append("```")
            out.append("Faça uma variação da textura anexada (PNG 1024×1024,")
            out.append("estilo Minecraft, pixel-art preservado).")
            out.append("")
            out.append(f"O que é esta textura: {ident}")
            if intro:
                out.append("")
                out.append(f"Restrição da família a que pertence: {intro}")
            out.append("")
            out.append("Restrições gerais de estilo:")
            out.append("- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.")
            out.append("- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,")
            out.append("  ZERO gradiente suave. Cada \"pixel\" original = bloco 64×64 sólido.")
            out.append("- Tileável sem costura (borda esquerda casa com direita, topo com base).")
            out.append("- Paleta dentro da família — não muda a identidade de cor do bloco.")
            out.append("- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.")
            out.append("```")
            out.append("")
        out.append("---")
        out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    if missing:
        print(f"\n⚠️ {len(missing)} file(s) without IDENTITY entry:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
