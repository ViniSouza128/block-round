# Pixel-art pack — texturas 16×16 originais

Pack alternativo de texturas para o Block Round, desenhado pixel-a-pixel
em Python+PIL. Objetivo: **substituir o conjunto Mojang em `textures/`**
por arte original com a mesma identidade visual de cada bloco, livre do
copyright das texturas vanilla.

## Estrutura

```
scripts/pixelart_pack/
  __init__.py        — marca o pacote
  palette.py         — dicts de cores RGBA por familia
  helpers.py         — primitivas reutilizaveis (fill, granulado, glifo, etc)
  gen_tnt.py         — gerador da familia TNT (POC)
  gen_*.py           — um modulo por familia (rodadas 1-4)
  verify.py          — CLI de validacao + grid comparativo
  _qa/               — saidas de QA (grids, previews) — descartavel
  README.md          — este arquivo
```

```
textures-pixelart/   — destino final: mesma arvore que textures/
                       (pasta unica e plana; nenhum subdiretorio)
```

## Estrategia

1. **Identidade preservada, pixels originais.** Pra cada PNG da pasta
   `textures/` o gerador correspondente desenha um sprite 16×16 (ou strip
   16×N para animacoes) que um jogador de Minecraft reconheceria
   imediatamente como o mesmo bloco — mas sem reproduzir os pixels da
   Mojang. As descricoes em `TEXTURE_VARIATION_PROMPTS.md` definem o que
   e a identidade de cada bloco; usamos esse texto como spec, nao a
   imagem original.

2. **Paletas por familia.** Famílias relacionadas (todos os `*_ore`, as
   6 tabuas, os 8 wools, os 5 deepslate) compartilham cores-base. Ajustar
   uma paleta cascateia para todas as texturas da familia.

3. **Helpers compartilhados.** As primitivas (`fill`, `granulado`,
   `mosaico`, `desenhar_glifo_3x5`, `faixa_horizontal`) sao genericas
   o suficiente para servir varias familias. Geradores especificos so
   precisam compor essas primitivas.

4. **Validacao automatica.** `verify.py` exige dimensao identica ao
   original, preserva alpha quando presente, e checa tileabilidade
   (bordas opostas casam).

5. **QA visual.** `comparar_grid` empilha original x novo lado-a-lado
   ampliado 8× — facil dar um olhada e batucar com a lista de famílias.

## Como rodar

### Pre-requisitos

```bash
pip install Pillow
```

### Gerar uma familia

```bash
# do repo root
python -m scripts.pixelart_pack.gen_tnt
# ou (estilo script)
python scripts/pixelart_pack/gen_tnt.py
```

### Validar tudo o que ja foi gerado

```bash
python scripts/pixelart_pack/verify.py
```

### Validar + gerar grid comparativo

```bash
python scripts/pixelart_pack/verify.py --qa
```

Resultado em `scripts/pixelart_pack/_qa/compare.png`.

### Validar so um subconjunto

```bash
python scripts/pixelart_pack/verify.py --apenas tnt_side tnt_top tnt_bottom
```

## Plano de rodadas

Total: **118 PNGs em 22 familias** (todas em `textures/`, pasta unica).
Alem das 115 imagens 16×16, ha 3 strips de animacao:
`magma.png` (16×48 = 3 frames), `prismarine_rough.png` (16×64 = 4
frames), `sea_lantern.png` (16×80 = 5 frames).

### Rodada 0 — POC (`gen_tnt.py`) — 3 PNGs

Familia 20_tnt: `tnt_side.png`, `tnt_top.png`, `tnt_bottom.png`. Serve
para validar paleta + helpers + verify antes de escalar.

### Rodada 1 — Mineral / stone (~28 PNGs)

| Familia | Qt | Texturas |
|---|---:|---|
| 05_stone_family | 4 | cobblestone, mossy_cobblestone, smooth_stone, stone |
| 06_igneous | 4 | andesite, diorite, granite, polished_andesite |
| 07_ores | 7 | coal/diamond/emerald/gold/iron/lapis/redstone_ore |
| 08_deepslate | 5 | deepslate + 4 deepslate_*_ore |
| 09_metal_gem | 5 | copper/diamond/emerald/gold/iron_block |
| 22 (parcial) | 3 | bedrock, bricks, gravel |

### Rodada 2 — Wood / organic plant (~31 PNGs)

| Familia | Qt | Texturas |
|---|---:|---|
| 01_planks | 6 | acacia/birch/dark_oak/jungle/oak/spruce_planks |
| 02_logs | 15 | 6 madeiras × {side, top} + variantes legadas |
| 03_leaves | 1 | leaves_oak |
| 17_crops_organic | 7 | hay, melon, pumpkin (side/top/front) |
| 18 (parcial) | 2 | mushroom_block_skin_brown, mushroom_block_skin_red |

### Rodada 3 — Terrain / surfaces / nether / ice / end (~29 PNGs)

| Familia | Qt | Texturas |
|---|---:|---|
| 10_sand_sandstone | 5 | sand + sandstone (top/bottom/side) + red_sandstone_top |
| 11_ice_snow | 4 | ice, ice_packed, blue_ice, snow |
| 12_dirt_grass_surfaces | 8 | dirt, podzol (side/top), grass (side/top), moss, mycelium (side/top) |
| 13_nether | 6 | netherrack, nether_bricks, magma**(strip)**, soul_sand, shroomlight, crying_obsidian |
| 14_end_obsidian | 2 | end_stone, obsidian |
| 18 (parcial) | 2 | bone_block_side, bone_block_top |
| 22 (parcial) | 2 | glowstone, sponge |

### Rodada 4 — Crafted / colored / translucent / quartz / prismarine (~30 PNGs)

| Familia | Qt | Texturas |
|---|---:|---|
| 04_wools | 8 | 8 cores |
| 15_prismarine_sea | 4 | prismarine_bricks, prismarine_dark, prismarine_rough**(strip)**, sea_lantern**(strip)** |
| 16_quartz | 3 | quartz_block (bottom/side/top) |
| 19_crafted_workstations | 7 | bookshelf, crafting_table (front/side/top), furnace (front_off/side/top) |
| 20_tnt | 3 | (POC; ja na rodada 0) |
| 21_translucent | 5 | glass, slime, honey (top/side/bottom) |

## Legenda das paletas

As paletas em `palette.py` seguem a convencao de chaves abaixo. Nem todas
as familias usam todas as chaves — sao guias para os geradores.

| Chave | Significado |
|---|---|
| `topo_escuro` / `topo_claro` | faixa de borda superior/inferior |
| `corpo_base` | cor mais frequente no miolo |
| `corpo_sombra` / `corpo_brilho` | variacoes para granulado/ruido |
| `label_*` | quadro/borda/fundo de texto (TNT, sponge) |
| `texto` | cor da glifagem |
| `pavio_*` | familia de pavio (TNT top) |
| `rejunte` | linha de separacao entre tijolos |
| `tijolo_a` / `tijolo_b` | tons alternantes para mosaicos |
| `cristal_*` | nucleos de mineral em ores |
| `gel_*` / `gel_borda` | translucidos (slime, honey, glass) |

## Checklist de validacao

Antes de fechar uma rodada:

- [ ] Todos os PNGs da rodada passam `verify.py` sem falha.
- [ ] Strips de animacao tem altura multipla de 16 (3/4/5 frames).
- [ ] PNGs translucidos (glass, slime, honey, leaves) preservam alpha.
- [ ] Grid comparativo aberto e cada par "le" como o mesmo bloco.
- [ ] Paletas de uma familia compartilham as chaves principais (ajuste
      em massa via `palette.py` deve ser viavel).
- [ ] Nenhum gerador usa literais RGB; tudo vem de `palette.py`.

## Aviso de licenca

Este pack e **codigo original**, distribuido sob os mesmos termos de
"ALL RIGHTS RESERVED" do repositorio (ver `LICENSE`). As PNGs em
`textures-pixelart/` NAO sao derivadas pixel-a-pixel das texturas
Mojang em `textures/` — sao composicoes pixel-a-pixel novas guiadas
pelas descricoes textuais de identidade em
`TEXTURE_VARIATION_PROMPTS.md`. Veja `NOTICE.md` para o status das
texturas em `textures/` (propriedade da Mojang/Microsoft).
