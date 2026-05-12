# Prompts de variação de textura — `textures-1024/`

Um prompt por PNG, agrupado por pasta na mesma ordem do explorador de arquivos. Use a estratégia que faz sentido pro seu fluxo:

- **Por grupo inteiro**: abra um chat por pasta, faça upload de TODOS os PNGs da pasta, cole o **intro do grupo** + **base de estilo** uma vez, e depois cole cada prompt individual conforme rodar.
- **Por arquivo isolado**: cada prompt já é auto-suficiente — base de estilo + intro do grupo + identidade do bloco — então funciona em chat virgem também.

> ⚠️ Sempre faça upload do PNG **original 1024×1024** anexado ao prompt. O modelo vai usar a imagem como referência visual; o texto só descreve o que preservar e o que variar.

---

## Base de estilo (idêntica para todas as variações)

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


---

## `01_planks/`

**Intro do grupo (cole 1× no início do chat):** Os 6 arquivos desta pasta são **tábuas de madeira** — uma textura única por tipo de madeira. Para coerência da família, mantenha o **padrão das tábuas idêntico em todas** (mesma largura de tábua horizontal — 4 pixels —, mesma densidade de nós, mesma direção de grão). O que muda entre arquivos é **só a cor da madeira**.

### `acacia_planks.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: tábuas de **acácia** — tom laranja-avermelhado quente / terracota, saturação média. Tábuas horizontais de 4 px, alguns nós pequenos.

Restrição da família a que pertence: Os 6 arquivos desta pasta são **tábuas de madeira** — uma textura única por tipo de madeira. Para coerência da família, mantenha o **padrão das tábuas idêntico em todas** (mesma largura de tábua horizontal — 4 pixels —, mesma densidade de nós, mesma direção de grão). O que muda entre arquivos é **só a cor da madeira**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `birch_planks.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: tábuas de **bétula** — tom creme-pálido com sutil aquecimento. As mais claras da família. Nós escuros pequenos visíveis.

Restrição da família a que pertence: Os 6 arquivos desta pasta são **tábuas de madeira** — uma textura única por tipo de madeira. Para coerência da família, mantenha o **padrão das tábuas idêntico em todas** (mesma largura de tábua horizontal — 4 pixels —, mesma densidade de nós, mesma direção de grão). O que muda entre arquivos é **só a cor da madeira**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `dark_oak_planks.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: tábuas de **carvalho escuro** — marrom frio profundo, quase preto nos nós. Tom mais pesado da família.

Restrição da família a que pertence: Os 6 arquivos desta pasta são **tábuas de madeira** — uma textura única por tipo de madeira. Para coerência da família, mantenha o **padrão das tábuas idêntico em todas** (mesma largura de tábua horizontal — 4 pixels —, mesma densidade de nós, mesma direção de grão). O que muda entre arquivos é **só a cor da madeira**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `jungle_planks.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: tábuas de **selva** — marrom-russet quente saturado, tom "madeira tropical".

Restrição da família a que pertence: Os 6 arquivos desta pasta são **tábuas de madeira** — uma textura única por tipo de madeira. Para coerência da família, mantenha o **padrão das tábuas idêntico em todas** (mesma largura de tábua horizontal — 4 pixels —, mesma densidade de nós, mesma direção de grão). O que muda entre arquivos é **só a cor da madeira**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `oak_planks.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: tábuas de **carvalho** — marrom-mel clássico (a referência da família).

Restrição da família a que pertence: Os 6 arquivos desta pasta são **tábuas de madeira** — uma textura única por tipo de madeira. Para coerência da família, mantenha o **padrão das tábuas idêntico em todas** (mesma largura de tábua horizontal — 4 pixels —, mesma densidade de nós, mesma direção de grão). O que muda entre arquivos é **só a cor da madeira**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `spruce_planks.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: tábuas de **abeto** — marrom escuro frio levemente acinzentado.

Restrição da família a que pertence: Os 6 arquivos desta pasta são **tábuas de madeira** — uma textura única por tipo de madeira. Para coerência da família, mantenha o **padrão das tábuas idêntico em todas** (mesma largura de tábua horizontal — 4 pixels —, mesma densidade de nós, mesma direção de grão). O que muda entre arquivos é **só a cor da madeira**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `02_logs/`

**Intro do grupo (cole 1× no início do chat):** Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

### `birch_log.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: variante alternativa da casca lateral de tronco de **bétula** — mesma identidade (branca + estrias pretas) mas pode diferir levemente em distribuição/rugosidade.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `dark_oak_log.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: variante alternativa de casca de **carvalho escuro** — mesma identidade.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `log_acacia.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: casca lateral de tronco de **acácia** — cinza-marrom esverdeado/oliva, grão vertical sutil.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `log_acacia_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: corte transversal de tronco de **acácia** — anéis em tom oliva-bege.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `log_big_oak.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: casca lateral de tronco de **carvalho escuro** ("big oak" no nome interno) — marrom muito escuro quase preto.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `log_big_oak_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: corte transversal de tronco de **carvalho escuro** — anéis muito escuros, centro quase preto.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `log_birch.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: casca lateral de tronco de **bétula**. Branca com estrias horizontais pretas curtas (marca registrada da bétula).

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `log_birch_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: corte transversal de tronco de **bétula**. Anéis claros, casca branca na borda externa, centro levemente mais escuro.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `log_jungle.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: casca lateral de tronco de **selva** — marrom-russet quente, grão menos pronunciado que abeto.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `log_jungle_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: corte transversal de tronco de **selva** — anéis em russet quente.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `log_spruce.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: casca lateral de tronco de **abeto** — marrom escuro frio, grão vertical mais pronunciado, sulcos mais profundos.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `log_spruce_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: corte transversal de tronco de **abeto** — anéis mais escuros, paleta marrom frio.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `oak_log.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **casca lateral** de tronco de carvalho. Grão vertical, marrom-bege uniforme, com nervuras finas verticais (não tábua horizontal!).

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `oak_log_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **corte transversal** (topo) de tronco de **carvalho**. Anéis concêntricos visíveis, centro levemente off-center. Marrom-mel.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `spruce_log.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: variante alternativa de casca de **abeto** — mesma identidade.

Restrição da família a que pertence: Pasta dos **troncos**. Cada tipo de madeira tem **side** (casca, grão vertical) e **top** (corte transversal com anéis concêntricos). Side e top do MESMO tipo precisam combinar (mesma cor de casca / mesmo tom interno dos anéis). Entre tipos, **anatomia uniforme** — mesma quantidade de anéis no top, mesma rugosidade da casca no side — só muda a paleta.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `03_leaves/`

**Intro do grupo (cole 1× no início do chat):** Só folhas de carvalho neste catálogo. Densidade de aglomerado de folhas e tom verde devem permanecer reconhecíveis.

### `leaves_oak.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **folhas de carvalho** — aglomerado denso de pequenas folhas verde-médio. Algumas folhas mais claras espalhadas. Padrão deve dar sensação de massa folhada vista de fora.

Restrição da família a que pertence: Só folhas de carvalho neste catálogo. Densidade de aglomerado de folhas e tom verde devem permanecer reconhecíveis.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `04_wools/`

**Intro do grupo (cole 1× no início do chat):** **Lãs coloridas**. As 8 cores DEVEM compartilhar o mesmo padrão de tricô / fibra — exatamente a mesma trama, mesmo espaçamento, mesmo ângulo. O ÚNICO eixo de variação entre os arquivos é a **cor base**.

### `black_wool.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: lã **preta** — quase preto, com a trama de tricô ainda perceptível em um tom levemente mais quente.

Restrição da família a que pertence: **Lãs coloridas**. As 8 cores DEVEM compartilhar o mesmo padrão de tricô / fibra — exatamente a mesma trama, mesmo espaçamento, mesmo ângulo. O ÚNICO eixo de variação entre os arquivos é a **cor base**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `blue_wool.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: lã **azul** — azul médio saturado, levemente frio.

Restrição da família a que pertence: **Lãs coloridas**. As 8 cores DEVEM compartilhar o mesmo padrão de tricô / fibra — exatamente a mesma trama, mesmo espaçamento, mesmo ângulo. O ÚNICO eixo de variação entre os arquivos é a **cor base**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `green_wool.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: lã **verde** — verde-folha médio levemente dessaturado.

Restrição da família a que pertence: **Lãs coloridas**. As 8 cores DEVEM compartilhar o mesmo padrão de tricô / fibra — exatamente a mesma trama, mesmo espaçamento, mesmo ângulo. O ÚNICO eixo de variação entre os arquivos é a **cor base**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `light_blue_wool.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: lã **azul-claro** — azul-céu suave, baixa saturação. Mesma trama da white_wool, só muda a cor.

Restrição da família a que pertence: **Lãs coloridas**. As 8 cores DEVEM compartilhar o mesmo padrão de tricô / fibra — exatamente a mesma trama, mesmo espaçamento, mesmo ângulo. O ÚNICO eixo de variação entre os arquivos é a **cor base**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `orange_wool.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: lã **laranja** — laranja saturado, entre amarelo e vermelho.

Restrição da família a que pertence: **Lãs coloridas**. As 8 cores DEVEM compartilhar o mesmo padrão de tricô / fibra — exatamente a mesma trama, mesmo espaçamento, mesmo ângulo. O ÚNICO eixo de variação entre os arquivos é a **cor base**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `red_wool.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: lã **vermelha** — vermelho quente levemente abafado (não escarlate puro).

Restrição da família a que pertence: **Lãs coloridas**. As 8 cores DEVEM compartilhar o mesmo padrão de tricô / fibra — exatamente a mesma trama, mesmo espaçamento, mesmo ângulo. O ÚNICO eixo de variação entre os arquivos é a **cor base**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `white_wool.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: lã **branca** — branco-creme nevado levemente off-white. Trama de tricô visível em toda a textura.

Restrição da família a que pertence: **Lãs coloridas**. As 8 cores DEVEM compartilhar o mesmo padrão de tricô / fibra — exatamente a mesma trama, mesmo espaçamento, mesmo ângulo. O ÚNICO eixo de variação entre os arquivos é a **cor base**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `yellow_wool.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: lã **amarela** — amarelo saturado quente, leve toque alaranjado.

Restrição da família a que pertence: **Lãs coloridas**. As 8 cores DEVEM compartilhar o mesmo padrão de tricô / fibra — exatamente a mesma trama, mesmo espaçamento, mesmo ângulo. O ÚNICO eixo de variação entre os arquivos é a **cor base**.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `05_stone_family/`

**Intro do grupo (cole 1× no início do chat):** Família da **pedra cinza**. `stone` é a base lisa-rugosa, `smooth_stone` é mais homogênea (pedra cozida), `cobblestone` tem pedrinhas individuais visíveis, `mossy_cobblestone` é cobble com manchas verdes de musgo. Paleta cinza neutra unificada entre os 4.

### `cobblestone.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **paralelepípedo (cobble)** — pedrinhas individuais empilhadas com argamassa cinza-escura entre elas. Tons de cinza variados entre as pedras.

Restrição da família a que pertence: Família da **pedra cinza**. `stone` é a base lisa-rugosa, `smooth_stone` é mais homogênea (pedra cozida), `cobblestone` tem pedrinhas individuais visíveis, `mossy_cobblestone` é cobble com manchas verdes de musgo. Paleta cinza neutra unificada entre os 4.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `mossy_cobblestone.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **cobble musgoso** — mesma estrutura do cobble, mas com manchas verdes irregulares de musgo cobrindo ~30% da superfície. O musgo deve parecer crescido, não pintado.

Restrição da família a que pertence: Família da **pedra cinza**. `stone` é a base lisa-rugosa, `smooth_stone` é mais homogênea (pedra cozida), `cobblestone` tem pedrinhas individuais visíveis, `mossy_cobblestone` é cobble com manchas verdes de musgo. Paleta cinza neutra unificada entre os 4.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `smooth_stone.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **pedra lisa** (pedra cozida) — cinza médio mais homogêneo que `stone.png`, com uma fina moldura escura na borda do bloco (marca de cocção). Sem pedras individuais visíveis.

Restrição da família a que pertence: Família da **pedra cinza**. `stone` é a base lisa-rugosa, `smooth_stone` é mais homogênea (pedra cozida), `cobblestone` tem pedrinhas individuais visíveis, `mossy_cobblestone` é cobble com manchas verdes de musgo. Paleta cinza neutra unificada entre os 4.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `stone.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **pedra** Minecraft clássica — cinza médio levemente rugoso, manchas claras/escuras sutis, sem elementos dominantes. Essa é a matriz de referência para todos os arquivos de `07_ores_stone_matrix/`.

Restrição da família a que pertence: Família da **pedra cinza**. `stone` é a base lisa-rugosa, `smooth_stone` é mais homogênea (pedra cozida), `cobblestone` tem pedrinhas individuais visíveis, `mossy_cobblestone` é cobble com manchas verdes de musgo. Paleta cinza neutra unificada entre os 4.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `06_igneous/`

**Intro do grupo (cole 1× no início do chat):** **Rochas ígneas**. Andesite (cinza), granite (rosado), diorite (branco com pontos pretos). Versões polidas são as mesmas mas com superfície lisa em vez de speckled. Mesma escala de mancha entre versões rugosa e polida do mesmo material.

### `andesite.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **andesito** — cinza médio com pequenas inclusões pretas e brancas espalhadas (textura speckled fina).

Restrição da família a que pertence: **Rochas ígneas**. Andesite (cinza), granite (rosado), diorite (branco com pontos pretos). Versões polidas são as mesmas mas com superfície lisa em vez de speckled. Mesma escala de mancha entre versões rugosa e polida do mesmo material.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `diorite.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **diorito** — base branca/clara dominante com pontos pretos espalhados ("granito invertido").

Restrição da família a que pertence: **Rochas ígneas**. Andesite (cinza), granite (rosado), diorite (branco com pontos pretos). Versões polidas são as mesmas mas com superfície lisa em vez de speckled. Mesma escala de mancha entre versões rugosa e polida do mesmo material.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `granite.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **granito** — base rosada-bege com pequenos pontos pretos, brancos e cinza espalhados.

Restrição da família a que pertence: **Rochas ígneas**. Andesite (cinza), granite (rosado), diorite (branco com pontos pretos). Versões polidas são as mesmas mas com superfície lisa em vez de speckled. Mesma escala de mancha entre versões rugosa e polida do mesmo material.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `polished_andesite.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: andesito **polido** — superfície lisa cinza médio uniforme, com uma sutil grade clara/escura sugerindo blocos cortados.

Restrição da família a que pertence: **Rochas ígneas**. Andesite (cinza), granite (rosado), diorite (branco com pontos pretos). Versões polidas são as mesmas mas com superfície lisa em vez de speckled. Mesma escala de mancha entre versões rugosa e polida do mesmo material.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `07_ores_stone_matrix/`

**Intro do grupo (cole 1× no início do chat):** **Minérios em matriz de pedra cinza comum**. A matriz cinza deve ser EXATAMENTE igual à `stone.png` (gere `stone.png` primeiro, depois aplique as inclusões de minério por cima). O que varia é só a cor e forma dos cristais/grãos do minério.

### `coal_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **carvão em pedra**. Matriz idêntica à `stone.png`. Por cima, manchas pretas amorfas (carvão) ocupando ~30% da área, formato irregular.

Restrição da família a que pertence: **Minérios em matriz de pedra cinza comum**. A matriz cinza deve ser EXATAMENTE igual à `stone.png` (gere `stone.png` primeiro, depois aplique as inclusões de minério por cima). O que varia é só a cor e forma dos cristais/grãos do minério.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `diamond_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **diamante em pedra**. Matriz `stone.png`. Inclusões **ciano-pálido cristalinas** com pequeno toque de geometria angular (sugerindo gemas).

Restrição da família a que pertence: **Minérios em matriz de pedra cinza comum**. A matriz cinza deve ser EXATAMENTE igual à `stone.png` (gere `stone.png` primeiro, depois aplique as inclusões de minério por cima). O que varia é só a cor e forma dos cristais/grãos do minério.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `emerald_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **esmeralda em pedra**. Matriz `stone.png`. Inclusões **verde-vivo cristalinas** angulares.

Restrição da família a que pertence: **Minérios em matriz de pedra cinza comum**. A matriz cinza deve ser EXATAMENTE igual à `stone.png` (gere `stone.png` primeiro, depois aplique as inclusões de minério por cima). O que varia é só a cor e forma dos cristais/grãos do minério.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `gold_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **ouro em pedra**. Matriz `stone.png`. Inclusões amarelo-dourado vivo.

Restrição da família a que pertence: **Minérios em matriz de pedra cinza comum**. A matriz cinza deve ser EXATAMENTE igual à `stone.png` (gere `stone.png` primeiro, depois aplique as inclusões de minério por cima). O que varia é só a cor e forma dos cristais/grãos do minério.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `iron_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **ferro em pedra**. Matriz idêntica à `stone.png`. Inclusões em tom **rosa-alaranjado/salmon** pálido, irregulares.

Restrição da família a que pertence: **Minérios em matriz de pedra cinza comum**. A matriz cinza deve ser EXATAMENTE igual à `stone.png` (gere `stone.png` primeiro, depois aplique as inclusões de minério por cima). O que varia é só a cor e forma dos cristais/grãos do minério.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `lapis_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lápis-lazúli em pedra**. Matriz `stone.png`. Inclusões **azul-profundo** com leves pontos brancos/dourados (calcita+pirita).

Restrição da família a que pertence: **Minérios em matriz de pedra cinza comum**. A matriz cinza deve ser EXATAMENTE igual à `stone.png` (gere `stone.png` primeiro, depois aplique as inclusões de minério por cima). O que varia é só a cor e forma dos cristais/grãos do minério.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `redstone_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **redstone em pedra**. Matriz `stone.png`. Pontos pequenos vermelho-vivos espalhados (sugerindo poeira vermelha brilhante).

Restrição da família a que pertence: **Minérios em matriz de pedra cinza comum**. A matriz cinza deve ser EXATAMENTE igual à `stone.png` (gere `stone.png` primeiro, depois aplique as inclusões de minério por cima). O que varia é só a cor e forma dos cristais/grãos do minério.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `08_deepslate/`

**Intro do grupo (cole 1× no início do chat):** **Deepslate e seus minérios**. Mesma lógica do grupo de pedra: a matriz escura precisa ser idêntica à `deepslate.png` (rocha azul-cinza escura, estratificada). Os ores deepslate substituem só as inclusões; a matriz cinza-escuro permanece igual.

### `deepslate.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **deepslate** — rocha cinza-azulada escura, com estratificação vertical sutil (linhas verticais paralelas). MUITO escura mas com variação interna. Essa é a matriz de referência para os ores deepslate.

Restrição da família a que pertence: **Deepslate e seus minérios**. Mesma lógica do grupo de pedra: a matriz escura precisa ser idêntica à `deepslate.png` (rocha azul-cinza escura, estratificada). Os ores deepslate substituem só as inclusões; a matriz cinza-escuro permanece igual.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `deepslate_diamond_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **diamante em deepslate**. Matriz idêntica à `deepslate.png`. Inclusões ciano-cristalinas com mais luminosidade aparente (contraste com o fundo escuro).

Restrição da família a que pertence: **Deepslate e seus minérios**. Mesma lógica do grupo de pedra: a matriz escura precisa ser idêntica à `deepslate.png` (rocha azul-cinza escura, estratificada). Os ores deepslate substituem só as inclusões; a matriz cinza-escuro permanece igual.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `deepslate_emerald_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **esmeralda em deepslate**. Matriz `deepslate.png`. Inclusões verde-vivo cristalinas.

Restrição da família a que pertence: **Deepslate e seus minérios**. Mesma lógica do grupo de pedra: a matriz escura precisa ser idêntica à `deepslate.png` (rocha azul-cinza escura, estratificada). Os ores deepslate substituem só as inclusões; a matriz cinza-escuro permanece igual.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `deepslate_gold_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **ouro em deepslate**. Matriz `deepslate.png`. Inclusões dourado-vivo, alto contraste com fundo escuro.

Restrição da família a que pertence: **Deepslate e seus minérios**. Mesma lógica do grupo de pedra: a matriz escura precisa ser idêntica à `deepslate.png` (rocha azul-cinza escura, estratificada). Os ores deepslate substituem só as inclusões; a matriz cinza-escuro permanece igual.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `deepslate_iron_ore.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **ferro em deepslate**. Matriz `deepslate.png`. Inclusões rosa-alaranjado pálido.

Restrição da família a que pertence: **Deepslate e seus minérios**. Mesma lógica do grupo de pedra: a matriz escura precisa ser idêntica à `deepslate.png` (rocha azul-cinza escura, estratificada). Os ores deepslate substituem só as inclusões; a matriz cinza-escuro permanece igual.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `09_metal_gem_blocks/`

**Intro do grupo (cole 1× no início do chat):** **Blocos sólidos de metal/gema** (a versão refinada/empilhada do minério). Todos compartilham o mesmo **layout de grade 3×3** (parece 9 lingotes/gemas dispostos em quadrado). Só muda a cor e o material visual (metal polido vs gema cristalina).

### `copper_block.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **bloco de cobre** — grade 3×3 em laranja-marrom polido (cobre não-oxidado, sem patina verde).

Restrição da família a que pertence: **Blocos sólidos de metal/gema** (a versão refinada/empilhada do minério). Todos compartilham o mesmo **layout de grade 3×3** (parece 9 lingotes/gemas dispostos em quadrado). Só muda a cor e o material visual (metal polido vs gema cristalina).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `diamond_block.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **bloco de diamante** — grade 3×3 ciano-pálido cristalino, faces facetadas levemente angulares.

Restrição da família a que pertence: **Blocos sólidos de metal/gema** (a versão refinada/empilhada do minério). Todos compartilham o mesmo **layout de grade 3×3** (parece 9 lingotes/gemas dispostos em quadrado). Só muda a cor e o material visual (metal polido vs gema cristalina).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `emerald_block.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **bloco de esmeralda** — grade 3×3 verde-vivo cristalino, facetas semelhantes ao diamante.

Restrição da família a que pertence: **Blocos sólidos de metal/gema** (a versão refinada/empilhada do minério). Todos compartilham o mesmo **layout de grade 3×3** (parece 9 lingotes/gemas dispostos em quadrado). Só muda a cor e o material visual (metal polido vs gema cristalina).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `gold_block.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **bloco de ouro** — grade 3×3 amarelo-dourado polido.

Restrição da família a que pertence: **Blocos sólidos de metal/gema** (a versão refinada/empilhada do minério). Todos compartilham o mesmo **layout de grade 3×3** (parece 9 lingotes/gemas dispostos em quadrado). Só muda a cor e o material visual (metal polido vs gema cristalina).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `iron_block.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **bloco de ferro** — grade 3×3 de lingotes em tom prateado/cinza-claro polido, com sutil contorno mais escuro entre cada lingote.

Restrição da família a que pertence: **Blocos sólidos de metal/gema** (a versão refinada/empilhada do minério). Todos compartilham o mesmo **layout de grade 3×3** (parece 9 lingotes/gemas dispostos em quadrado). Só muda a cor e o material visual (metal polido vs gema cristalina).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `10_sand_sandstone/`

**Intro do grupo (cole 1× no início do chat):** **Areia e arenito**. `sand` é areia solta (grãos finos). `sandstone` é o bloco esculpido — lateral tem ranhuras verticais de erosão. `sandstone_top/bottom` são tampas lisas. `red_sandstone_top` é a versão vermelha/laranja da tampa lisa.

### `red_sandstone_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **arenito vermelho (topo)** — versão laranja-avermelhada da tampa sandstone_top. Mesma estrutura, paleta quente.

Restrição da família a que pertence: **Areia e arenito**. `sand` é areia solta (grãos finos). `sandstone` é o bloco esculpido — lateral tem ranhuras verticais de erosão. `sandstone_top/bottom` são tampas lisas. `red_sandstone_top` é a versão vermelha/laranja da tampa lisa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `sand.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **areia** — grãos finos cor de areia clara (beige claro), ligeiramente granulada, uniforme.

Restrição da família a que pertence: **Areia e arenito**. `sand` é areia solta (grãos finos). `sandstone` é o bloco esculpido — lateral tem ranhuras verticais de erosão. `sandstone_top/bottom` são tampas lisas. `red_sandstone_top` é a versão vermelha/laranja da tampa lisa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `sandstone.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **arenito (lateral)** — bege/beige médio com **ranhuras verticais** sutis (erosão). Identidade da face lateral do bloco arenito.

Restrição da família a que pertence: **Areia e arenito**. `sand` é areia solta (grãos finos). `sandstone` é o bloco esculpido — lateral tem ranhuras verticais de erosão. `sandstone_top/bottom` são tampas lisas. `red_sandstone_top` é a versão vermelha/laranja da tampa lisa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `sandstone_bottom.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **arenito (base)** — tampa inferior, similar ao top mas sem moldura escura.

Restrição da família a que pertence: **Areia e arenito**. `sand` é areia solta (grãos finos). `sandstone` é o bloco esculpido — lateral tem ranhuras verticais de erosão. `sandstone_top/bottom` são tampas lisas. `red_sandstone_top` é a versão vermelha/laranja da tampa lisa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `sandstone_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **arenito (topo)** — tampa lisa do bloco arenito, sem ranhuras verticais. Beige mais uniforme, com uma fina linha de moldura escura ao redor.

Restrição da família a que pertence: **Areia e arenito**. `sand` é areia solta (grãos finos). `sandstone` é o bloco esculpido — lateral tem ranhuras verticais de erosão. `sandstone_top/bottom` são tampas lisas. `red_sandstone_top` é a versão vermelha/laranja da tampa lisa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `11_ice_snow/`

**Intro do grupo (cole 1× no início do chat):** **Gelo e neve** — paleta fria. `ice` translúcido com rachaduras, `ice_packed` opaco branco-azulado, `blue_ice` saturado azul-vidro, `snow` neve fofa branca pura. Mantenha a sensação de frio/úmido.

### `blue_ice.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **gelo azul** — saturação maior, azul-vidro brilhante, superfície quase espelhada (mas mantendo aspecto pixelado).

Restrição da família a que pertence: **Gelo e neve** — paleta fria. `ice` translúcido com rachaduras, `ice_packed` opaco branco-azulado, `blue_ice` saturado azul-vidro, `snow` neve fofa branca pura. Mantenha a sensação de frio/úmido.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `ice.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **gelo** — branco-azulado translúcido com **rachaduras finas** irregulares espalhadas. Sugestão de transparência (mas é PNG opaco — usar tom claro para sugerir).

Restrição da família a que pertence: **Gelo e neve** — paleta fria. `ice` translúcido com rachaduras, `ice_packed` opaco branco-azulado, `blue_ice` saturado azul-vidro, `snow` neve fofa branca pura. Mantenha a sensação de frio/úmido.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `ice_packed.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **gelo compacto** — branco-azulado mais opaco, **sem rachaduras**, superfície mais lisa que `ice`.

Restrição da família a que pertence: **Gelo e neve** — paleta fria. `ice` translúcido com rachaduras, `ice_packed` opaco branco-azulado, `blue_ice` saturado azul-vidro, `snow` neve fofa branca pura. Mantenha a sensação de frio/úmido.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `snow.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **neve** — branco puro com leve variação azulada (sombras suaves entre flocos), aspecto fofo/grumoso.

Restrição da família a que pertence: **Gelo e neve** — paleta fria. `ice` translúcido com rachaduras, `ice_packed` opaco branco-azulado, `blue_ice` saturado azul-vidro, `snow` neve fofa branca pura. Mantenha a sensação de frio/úmido.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `12_dirt_grass_surfaces/`

**Intro do grupo (cole 1× no início do chat):** **Superfícies de chão / cobertura vegetal**. Todas que terminam em `_side` têm **dirt na metade inferior e a cobertura específica na superior** (grama verde no topo, mycelium roxo no topo, podzol com agulhas claras no topo). A parte dirt deve ser idêntica à `dirt.png` em todos os _side.

### `dirt.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **terra** — marrom escuro com pequenos pontos mais claros (pedrinhas/raízes). Sem grama. Essa é a referência para a metade inferior de todos os `_side` deste grupo.

Restrição da família a que pertence: **Superfícies de chão / cobertura vegetal**. Todas que terminam em `_side` têm **dirt na metade inferior e a cobertura específica na superior** (grama verde no topo, mycelium roxo no topo, podzol com agulhas claras no topo). A parte dirt deve ser idêntica à `dirt.png` em todos os _side.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `dirt_podzol_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de bloco de podzol** — metade inferior `dirt.png`, metade superior tem borda de podzol (terra com agulhas claras) caindo sobre a terra.

Restrição da família a que pertence: **Superfícies de chão / cobertura vegetal**. Todas que terminam em `_side` têm **dirt na metade inferior e a cobertura específica na superior** (grama verde no topo, mycelium roxo no topo, podzol com agulhas claras no topo). A parte dirt deve ser idêntica à `dirt.png` em todos os _side.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `dirt_podzol_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de bloco de podzol** — superfície marrom-escura coberta de **agulhas claras** (pinheiro), pontos esparsos.

Restrição da família a que pertence: **Superfícies de chão / cobertura vegetal**. Todas que terminam em `_side` têm **dirt na metade inferior e a cobertura específica na superior** (grama verde no topo, mycelium roxo no topo, podzol com agulhas claras no topo). A parte dirt deve ser idêntica à `dirt.png` em todos os _side.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `grass_block_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de bloco de grama** — metade inferior é `dirt.png`, metade superior tem **a borda de grama caindo sobre a terra** (linha irregular onde a grama termina). Borda de grama verde-médio.

Restrição da família a que pertence: **Superfícies de chão / cobertura vegetal**. Todas que terminam em `_side` têm **dirt na metade inferior e a cobertura específica na superior** (grama verde no topo, mycelium roxo no topo, podzol com agulhas claras no topo). A parte dirt deve ser idêntica à `dirt.png` em todos os _side.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `grass_block_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de bloco de grama** — manto de grama verde-médio com variação sutil (folhinhas mais claras e mais escuras). Sem terra visível.

Restrição da família a que pertence: **Superfícies de chão / cobertura vegetal**. Todas que terminam em `_side` têm **dirt na metade inferior e a cobertura específica na superior** (grama verde no topo, mycelium roxo no topo, podzol com agulhas claras no topo). A parte dirt deve ser idêntica à `dirt.png` em todos os _side.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `moss_block.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **bloco de musgo** — superfície verde-lustroso uniforme, mais densa e úmida que grama, sem nada de terra exposta.

Restrição da família a que pertence: **Superfícies de chão / cobertura vegetal**. Todas que terminam em `_side` têm **dirt na metade inferior e a cobertura específica na superior** (grama verde no topo, mycelium roxo no topo, podzol com agulhas claras no topo). A parte dirt deve ser idêntica à `dirt.png` em todos os _side.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `mycelium_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de bloco de micélio** — metade inferior `dirt.png`, metade superior tem borda de micélio roxo-acinzentado caindo sobre a terra.

Restrição da família a que pertence: **Superfícies de chão / cobertura vegetal**. Todas que terminam em `_side` têm **dirt na metade inferior e a cobertura específica na superior** (grama verde no topo, mycelium roxo no topo, podzol com agulhas claras no topo). A parte dirt deve ser idêntica à `dirt.png` em todos os _side.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `mycelium_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de bloco de micélio** — superfície roxo-acinzentada fungal com pequenos pontos brancos (esporos) espalhados.

Restrição da família a que pertence: **Superfícies de chão / cobertura vegetal**. Todas que terminam em `_side` têm **dirt na metade inferior e a cobertura específica na superior** (grama verde no topo, mycelium roxo no topo, podzol com agulhas claras no topo). A parte dirt deve ser idêntica à `dirt.png` em todos os _side.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `13_nether/`

**Intro do grupo (cole 1× no início do chat):** **Dimensão Nether** — paleta vermelha/escura. `netherrack` é a rocha vermelha base do bioma. `magma_frame0/1/2` são **3 frames de uma animação** — geram em sequência, frame N flui para N+1 (cracks de lava se movendo lentamente). `crying_obsidian` tem lágrimas magenta vivas no obsidian roxo escuro.

### `crying_obsidian.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **obsidian chorando** — base obsidian roxo-escuro quase preto, com **lágrimas/cristais magenta-vivo** verticais escorrendo (4-6 lágrimas verticais).

Restrição da família a que pertence: **Dimensão Nether** — paleta vermelha/escura. `netherrack` é a rocha vermelha base do bioma. `magma_frame0/1/2` são **3 frames de uma animação** — geram em sequência, frame N flui para N+1 (cracks de lava se movendo lentamente). `crying_obsidian` tem lágrimas magenta vivas no obsidian roxo escuro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `magma_frame0.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **magma — frame 0/3** de animação. Superfície de pedra preta com **rachaduras de lava laranja-amarelo** brilhante. Frame inicial: rachaduras mais finas/quietas.

Restrição da família a que pertence: **Dimensão Nether** — paleta vermelha/escura. `netherrack` é a rocha vermelha base do bioma. `magma_frame0/1/2` são **3 frames de uma animação** — geram em sequência, frame N flui para N+1 (cracks de lava se movendo lentamente). `crying_obsidian` tem lágrimas magenta vivas no obsidian roxo escuro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `magma_frame1.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **magma — frame 1/3** de animação. Mesma identidade, rachaduras um pouco mais grossas/brilhantes que frame 0 (lava se movendo).

Restrição da família a que pertence: **Dimensão Nether** — paleta vermelha/escura. `netherrack` é a rocha vermelha base do bioma. `magma_frame0/1/2` são **3 frames de uma animação** — geram em sequência, frame N flui para N+1 (cracks de lava se movendo lentamente). `crying_obsidian` tem lágrimas magenta vivas no obsidian roxo escuro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `magma_frame2.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **magma — frame 2/3** de animação. Rachaduras mais luminosas, prestes a voltar para o frame 0 (loop).

Restrição da família a que pertence: **Dimensão Nether** — paleta vermelha/escura. `netherrack` é a rocha vermelha base do bioma. `magma_frame0/1/2` são **3 frames de uma animação** — geram em sequência, frame N flui para N+1 (cracks de lava se movendo lentamente). `crying_obsidian` tem lágrimas magenta vivas no obsidian roxo escuro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `nether_bricks.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **tijolos do Nether** — padrão de parede de tijolos pequenos em marrom muito escuro, com argamassa preta entre eles.

Restrição da família a que pertence: **Dimensão Nether** — paleta vermelha/escura. `netherrack` é a rocha vermelha base do bioma. `magma_frame0/1/2` são **3 frames de uma animação** — geram em sequência, frame N flui para N+1 (cracks de lava se movendo lentamente). `crying_obsidian` tem lágrimas magenta vivas no obsidian roxo escuro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `netherrack.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **netherrack** — rocha vermelha-bordô do Nether, com **veias mais escuras** e padrão irregular tipo "carne" fibrosa.

Restrição da família a que pertence: **Dimensão Nether** — paleta vermelha/escura. `netherrack` é a rocha vermelha base do bioma. `magma_frame0/1/2` são **3 frames de uma animação** — geram em sequência, frame N flui para N+1 (cracks de lava se movendo lentamente). `crying_obsidian` tem lágrimas magenta vivas no obsidian roxo escuro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `shroomlight.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **shroomlight** — cogumelo luminoso laranja-dourado do Nether. Superfície bumpy/orgânica com tom emissivo dourado vivo.

Restrição da família a que pertence: **Dimensão Nether** — paleta vermelha/escura. `netherrack` é a rocha vermelha base do bioma. `magma_frame0/1/2` são **3 frames de uma animação** — geram em sequência, frame N flui para N+1 (cracks de lava se movendo lentamente). `crying_obsidian` tem lágrimas magenta vivas no obsidian roxo escuro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `soul_sand.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **areia das almas** — areia marrom-escura com **3 marcas de rosto/face fantasmagórico** sutis cavadas na superfície. Identidade do bloco vem dessas faces.

Restrição da família a que pertence: **Dimensão Nether** — paleta vermelha/escura. `netherrack` é a rocha vermelha base do bioma. `magma_frame0/1/2` são **3 frames de uma animação** — geram em sequência, frame N flui para N+1 (cracks de lava se movendo lentamente). `crying_obsidian` tem lágrimas magenta vivas no obsidian roxo escuro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `14_end_obsidian/`

**Intro do grupo (cole 1× no início do chat):** **End Stone** e **Obsidian** — visualmente opostas mas agrupadas por raridade/peso. End stone é beige claro speckled; obsidian é roxo muito escuro quase preto, com reflexos magenta sutis.

### `end_stone.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **end stone** — pedra do End. Beige-amarelado claro com **pequenas inclusões pretas densas** (pontos amorfos espalhados).

Restrição da família a que pertence: **End Stone** e **Obsidian** — visualmente opostas mas agrupadas por raridade/peso. End stone é beige claro speckled; obsidian é roxo muito escuro quase preto, com reflexos magenta sutis.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `obsidian.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **obsidian** — vidro vulcânico **roxo muito escuro, quase preto**, com **reflexos magenta sutis** em algumas áreas (sugerindo brilho vítreo).

Restrição da família a que pertence: **End Stone** e **Obsidian** — visualmente opostas mas agrupadas por raridade/peso. End stone é beige claro speckled; obsidian é roxo muito escuro quase preto, com reflexos magenta sutis.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `15_prismarine_sea/`

**Intro do grupo (cole 1× no início do chat):** **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

### `prismarine_bricks.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **prismarine bricks** — padrão de tijolos pequenos em ciano-turquesa, com argamassa azul-escura entre eles.

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `prismarine_dark.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **prismarine escuro** — variante escura, padrão carved/esculpido com tom teal muito escuro quase preto.

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `prismarine_rough_frame0.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **prismarine rough — frame 0/4** de animação. Superfície turquesa-ciano com padrão de **ondulações suaves**. Frame inicial da onda.

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `prismarine_rough_frame1.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: prismarine rough — **frame 1/4**. Ondulações deslocadas um pouco para um lado em relação ao frame 0.

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `prismarine_rough_frame2.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: prismarine rough — **frame 2/4**. Ondulações no ponto médio do ciclo.

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `prismarine_rough_frame3.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: prismarine rough — **frame 3/4**. Ondulações prestes a voltar ao frame 0 (loop).

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `sea_lantern_frame0.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **sea lantern — frame 0/5** de animação luminosa. Superfície ciano-claro com **cristais brilhantes** dispostos em padrão. Frame inicial: brilho mais sutil.

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `sea_lantern_frame1.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: sea lantern — **frame 1/5**. Brilho aumentando levemente em alguns cristais.

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `sea_lantern_frame2.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: sea lantern — **frame 2/5**. Pico de brilho — máximo de luminosidade nos cristais.

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `sea_lantern_frame3.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: sea lantern — **frame 3/5**. Brilho diminuindo, voltando ao estado mais sutil.

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `sea_lantern_frame4.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: sea lantern — **frame 4/5**. Frame mais sutil, prestes a fazer loop com frame 0.

Restrição da família a que pertence: **Família prismarine** (monumento submarino). `prismarine_rough_*` é uma **animação de 4 frames** (água rippling). `sea_lantern_*` é uma **animação de 5 frames** (luz pulsante). Os frames devem fluir suavemente um para o outro. Paleta turquesa-ciano luminosa.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `16_quartz/`

**Intro do grupo (cole 1× no início do chat):** **Bloco de quartzo** com 3 faces distintas. Top tem tampa lisa com borda fina. Side tem colunas verticais estriadas. Bottom é uma base lisa. As 3 faces compartilham o branco quartz puro.

### `quartz_block_bottom.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **base de bloco de quartzo** — branca quartz lisa, sem moldura escura ao redor (mais limpa que o top).

Restrição da família a que pertence: **Bloco de quartzo** com 3 faces distintas. Top tem tampa lisa com borda fina. Side tem colunas verticais estriadas. Bottom é uma base lisa. As 3 faces compartilham o branco quartz puro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `quartz_block_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de bloco de quartzo** — colunas verticais estriadas (3-4 colunas paralelas), brancas quartz com sombras finas entre as colunas.

Restrição da família a que pertence: **Bloco de quartzo** com 3 faces distintas. Top tem tampa lisa com borda fina. Side tem colunas verticais estriadas. Bottom é uma base lisa. As 3 faces compartilham o branco quartz puro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `quartz_block_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de bloco de quartzo** — tampa lisa branca quartz puro, com uma **fina moldura escura** ao redor (sulco na borda).

Restrição da família a que pertence: **Bloco de quartzo** com 3 faces distintas. Top tem tampa lisa com borda fina. Side tem colunas verticais estriadas. Bottom é uma base lisa. As 3 faces compartilham o branco quartz puro.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `17_crops_organic/`

**Intro do grupo (cole 1× no início do chat):** **Plantações e alimentos** — blocos com side+top distintos. Hay (palha): side mostra feixes verticais amarrados, top mostra o corte transversal dos feixes. Melon (melancia): side verde listrado, top mostra a polpa rosa. Pumpkin (abóbora): side laranja com gomos verticais, top com talo/cabo central.

### `hay_block_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de fardo de feno** — feixes verticais de palha dourada amarrados por uma **corda horizontal** no meio. Tons dourado-amarelo.

Restrição da família a que pertence: **Plantações e alimentos** — blocos com side+top distintos. Hay (palha): side mostra feixes verticais amarrados, top mostra o corte transversal dos feixes. Melon (melancia): side verde listrado, top mostra a polpa rosa. Pumpkin (abóbora): side laranja com gomos verticais, top com talo/cabo central.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `hay_block_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de fardo de feno** — corte transversal dos feixes, mostrando os caules amarrados em padrão circular concêntrico (dourado).

Restrição da família a que pertence: **Plantações e alimentos** — blocos com side+top distintos. Hay (palha): side mostra feixes verticais amarrados, top mostra o corte transversal dos feixes. Melon (melancia): side verde listrado, top mostra a polpa rosa. Pumpkin (abóbora): side laranja com gomos verticais, top com talo/cabo central.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `melon_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de melancia** — exterior **verde com listras verticais** (claras e escuras alternadas).

Restrição da família a que pertence: **Plantações e alimentos** — blocos com side+top distintos. Hay (palha): side mostra feixes verticais amarrados, top mostra o corte transversal dos feixes. Melon (melancia): side verde listrado, top mostra a polpa rosa. Pumpkin (abóbora): side laranja com gomos verticais, top com talo/cabo central.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `melon_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de melancia** — corte transversal mostrando a **polpa rosa-avermelhada** com sementes pretas pequenas espalhadas, borda fina verde.

Restrição da família a que pertence: **Plantações e alimentos** — blocos com side+top distintos. Hay (palha): side mostra feixes verticais amarrados, top mostra o corte transversal dos feixes. Melon (melancia): side verde listrado, top mostra a polpa rosa. Pumpkin (abóbora): side laranja com gomos verticais, top com talo/cabo central.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `pumpkin_face_off.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de abóbora não esculpida** — exterior laranja com **gomos verticais** (cristas verticais paralelas), sem face esculpida.

Restrição da família a que pertence: **Plantações e alimentos** — blocos com side+top distintos. Hay (palha): side mostra feixes verticais amarrados, top mostra o corte transversal dos feixes. Melon (melancia): side verde listrado, top mostra a polpa rosa. Pumpkin (abóbora): side laranja com gomos verticais, top com talo/cabo central.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `pumpkin_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de abóbora padrão** — versão padrão (similar ao face_off mas pode ter variação sutil de cor).

Restrição da família a que pertence: **Plantações e alimentos** — blocos com side+top distintos. Hay (palha): side mostra feixes verticais amarrados, top mostra o corte transversal dos feixes. Melon (melancia): side verde listrado, top mostra a polpa rosa. Pumpkin (abóbora): side laranja com gomos verticais, top com talo/cabo central.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `pumpkin_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de abóbora** — laranja com **cabo/talo central** verde-marrom no centro.

Restrição da família a que pertence: **Plantações e alimentos** — blocos com side+top distintos. Hay (palha): side mostra feixes verticais amarrados, top mostra o corte transversal dos feixes. Melon (melancia): side verde listrado, top mostra a polpa rosa. Pumpkin (abóbora): side laranja com gomos verticais, top com talo/cabo central.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `18_mushroom_bone/`

**Intro do grupo (cole 1× no início do chat):** **Cogumelos gigantes e bloco de osso**. Bone block tem fibras verticais na side e end-grain no top (parece um osso longo cortado). Mushroom red é cogumelo vermelho com pontos brancos (amanita). Mushroom brown é mais terroso, sem pontos.

### `bone_block_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de bloco de osso** — fibras verticais cremes/brancas (como osso longo cortado).

Restrição da família a que pertence: **Cogumelos gigantes e bloco de osso**. Bone block tem fibras verticais na side e end-grain no top (parece um osso longo cortado). Mushroom red é cogumelo vermelho com pontos brancos (amanita). Mushroom brown é mais terroso, sem pontos.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `bone_block_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de bloco de osso** — corte transversal mostrando estriações concêntricas em creme/branco.

Restrição da família a que pertence: **Cogumelos gigantes e bloco de osso**. Bone block tem fibras verticais na side e end-grain no top (parece um osso longo cortado). Mushroom red é cogumelo vermelho com pontos brancos (amanita). Mushroom brown é mais terroso, sem pontos.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `mushroom_block_skin_brown.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **pele de cogumelo gigante marrom** — superfície marrom-canela uniforme, sem pontos (mais terrosa que a vermelha).

Restrição da família a que pertence: **Cogumelos gigantes e bloco de osso**. Bone block tem fibras verticais na side e end-grain no top (parece um osso longo cortado). Mushroom red é cogumelo vermelho com pontos brancos (amanita). Mushroom brown é mais terroso, sem pontos.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `mushroom_block_skin_red.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **pele de cogumelo gigante vermelho** — superfície vermelha vibrante com **pontos brancos circulares** espalhados (amanita clássica).

Restrição da família a que pertence: **Cogumelos gigantes e bloco de osso**. Bone block tem fibras verticais na side e end-grain no top (parece um osso longo cortado). Mushroom red é cogumelo vermelho com pontos brancos (amanita). Mushroom brown é mais terroso, sem pontos.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `19_crafted_workstations/`

**Intro do grupo (cole 1× no início do chat):** **Blocos de bancada**. Crafting table: top mostra grade 3×3 de receita, side mostra tábuas+ferramentas, front tem motivo de martelo/serra. Furnace: top liso, side com sulcos sutis, front tem a abertura retangular escura (apagada/off). Bookshelf: lombadas de livros enfileiradas com cores variadas.

### `bookshelf.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **estante de livros** — fileira horizontal de **lombadas de livros coloridas** (vermelhas, azuis, marrons, amarelas, espessuras variadas) sobre prateleira de madeira em cima e embaixo.

Restrição da família a que pertence: **Blocos de bancada**. Crafting table: top mostra grade 3×3 de receita, side mostra tábuas+ferramentas, front tem motivo de martelo/serra. Furnace: top liso, side com sulcos sutis, front tem a abertura retangular escura (apagada/off). Bookshelf: lombadas de livros enfileiradas com cores variadas.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `crafting_table_front.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **frente de bancada de trabalho** — tábuas com motivo central de **martelo+serra** cruzados.

Restrição da família a que pertence: **Blocos de bancada**. Crafting table: top mostra grade 3×3 de receita, side mostra tábuas+ferramentas, front tem motivo de martelo/serra. Furnace: top liso, side com sulcos sutis, front tem a abertura retangular escura (apagada/off). Bookshelf: lombadas de livros enfileiradas com cores variadas.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `crafting_table_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de bancada de trabalho** — tábuas de madeira com silhuetas escuras de **ferramentas** (serra, martelo).

Restrição da família a que pertence: **Blocos de bancada**. Crafting table: top mostra grade 3×3 de receita, side mostra tábuas+ferramentas, front tem motivo de martelo/serra. Furnace: top liso, side com sulcos sutis, front tem a abertura retangular escura (apagada/off). Bookshelf: lombadas de livros enfileiradas com cores variadas.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `crafting_table_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de bancada de trabalho** — superfície de madeira com **grade 3×3 cavada** (linhas claras formando 9 quadrados).

Restrição da família a que pertence: **Blocos de bancada**. Crafting table: top mostra grade 3×3 de receita, side mostra tábuas+ferramentas, front tem motivo de martelo/serra. Furnace: top liso, side com sulcos sutis, front tem a abertura retangular escura (apagada/off). Bookshelf: lombadas de livros enfileiradas com cores variadas.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `furnace_front_off.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **frente de fornalha (desligada)** — pedra cinza com **abertura retangular escura central** (entrada de combustão, vazia).

Restrição da família a que pertence: **Blocos de bancada**. Crafting table: top mostra grade 3×3 de receita, side mostra tábuas+ferramentas, front tem motivo de martelo/serra. Furnace: top liso, side com sulcos sutis, front tem a abertura retangular escura (apagada/off). Bookshelf: lombadas de livros enfileiradas com cores variadas.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `furnace_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de fornalha** — pedra cinza com **sulcos verticais sutis** (rebites/painéis).

Restrição da família a que pertence: **Blocos de bancada**. Crafting table: top mostra grade 3×3 de receita, side mostra tábuas+ferramentas, front tem motivo de martelo/serra. Furnace: top liso, side com sulcos sutis, front tem a abertura retangular escura (apagada/off). Bookshelf: lombadas de livros enfileiradas com cores variadas.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `furnace_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de fornalha** — superfície de pedra cinza lisa, idêntica à `smooth_stone` (sem nada por cima).

Restrição da família a que pertence: **Blocos de bancada**. Crafting table: top mostra grade 3×3 de receita, side mostra tábuas+ferramentas, front tem motivo de martelo/serra. Furnace: top liso, side com sulcos sutis, front tem a abertura retangular escura (apagada/off). Bookshelf: lombadas de livros enfileiradas com cores variadas.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `20_tnt/`

**Intro do grupo (cole 1× no início do chat):** **TNT** — 3 faces de um único cubo. Top: pavio enrolado no centro. Side: caixa vermelha com **"TNT" em letras brancas visíveis** e listras diagonais amarelas/pretas de aviso (esse texto e o padrão de aviso DEVEM permanecer legíveis). Bottom: vermelho liso (base da carga explosiva).

### `tnt_bottom.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **base de TNT** — vermelho liso, mais uniforme que o top (sem pavio).

Restrição da família a que pertence: **TNT** — 3 faces de um único cubo. Top: pavio enrolado no centro. Side: caixa vermelha com **"TNT" em letras brancas visíveis** e listras diagonais amarelas/pretas de aviso (esse texto e o padrão de aviso DEVEM permanecer legíveis). Bottom: vermelho liso (base da carga explosiva).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `tnt_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de TNT** — caixa vermelha com **as letras "TNT"** em branco no centro (LEGÍVEIS, NÃO DISTORÇA O TEXTO) e listras diagonais amarelas+pretas de aviso nas bordas superior e inferior.

Restrição da família a que pertence: **TNT** — 3 faces de um único cubo. Top: pavio enrolado no centro. Side: caixa vermelha com **"TNT" em letras brancas visíveis** e listras diagonais amarelas/pretas de aviso (esse texto e o padrão de aviso DEVEM permanecer legíveis). Bottom: vermelho liso (base da carga explosiva).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `tnt_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de TNT** — superfície vermelha com **pavio enrolado em espiral** preto/cinza no centro.

Restrição da família a que pertence: **TNT** — 3 faces de um único cubo. Top: pavio enrolado no centro. Side: caixa vermelha com **"TNT" em letras brancas visíveis** e listras diagonais amarelas/pretas de aviso (esse texto e o padrão de aviso DEVEM permanecer legíveis). Bottom: vermelho liso (base da carga explosiva).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `21_translucent/`

**Intro do grupo (cole 1× no início do chat):** **Blocos translúcidos / gelatinosos**. Glass tem só uma fina borda de moldura, miolo praticamente vazio (transparência sugerida com leve tom azul-claro). Slime é gel verde com padrão de favo de mel sutil. Honey é gel âmbar — top/side/bottom têm tonalidades levemente diferentes.

### `glass.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **vidro** — predominantemente **transparente / claro** (cor de fundo neutra clara), com apenas uma **fina moldura azul-claro/branco** ao redor sugerindo a borda da vidraça. Centro praticamente vazio.

Restrição da família a que pertence: **Blocos translúcidos / gelatinosos**. Glass tem só uma fina borda de moldura, miolo praticamente vazio (transparência sugerida com leve tom azul-claro). Slime é gel verde com padrão de favo de mel sutil. Honey é gel âmbar — top/side/bottom têm tonalidades levemente diferentes.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `honey_bottom.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **base de mel** — âmbar uniforme similar ao top, mas levemente mais escuro.

Restrição da família a que pertence: **Blocos translúcidos / gelatinosos**. Glass tem só uma fina borda de moldura, miolo praticamente vazio (transparência sugerida com leve tom azul-claro). Slime é gel verde com padrão de favo de mel sutil. Honey é gel âmbar — top/side/bottom têm tonalidades levemente diferentes.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `honey_side.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **lateral de mel** — âmbar mais escuro que o top, com **gotas/escorrimento** sutil descendo.

Restrição da família a que pertence: **Blocos translúcidos / gelatinosos**. Glass tem só uma fina borda de moldura, miolo praticamente vazio (transparência sugerida com leve tom azul-claro). Slime é gel verde com padrão de favo de mel sutil. Honey é gel âmbar — top/side/bottom têm tonalidades levemente diferentes.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `honey_top.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **topo de mel** — superfície âmbar dourada brilhante, com sugestão sutil de viscosidade (gradiente leve mas mantendo pixel-art).

Restrição da família a que pertence: **Blocos translúcidos / gelatinosos**. Glass tem só uma fina borda de moldura, miolo praticamente vazio (transparência sugerida com leve tom azul-claro). Slime é gel verde com padrão de favo de mel sutil. Honey é gel âmbar — top/side/bottom têm tonalidades levemente diferentes.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `slime.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **slime** — verde-claro translúcido com padrão de **favo de mel/escamas hexagonais** sutil. Cor de gel.

Restrição da família a que pertence: **Blocos translúcidos / gelatinosos**. Glass tem só uma fina borda de moldura, miolo praticamente vazio (transparência sugerida com leve tom azul-claro). Slime é gel verde com padrão de favo de mel sutil. Honey é gel âmbar — top/side/bottom têm tonalidades levemente diferentes.

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---

## `22_misc_solids/`

**Intro do grupo (cole 1× no início do chat):** **Sólidos diversos** que não pertencem a nenhuma família específica. Bedrock (rocha quase preta, irregular, fissuras). Bricks (parede de tijolos vermelhos com argamassa). Glowstone (aglomerado luminoso dourado-amarelado). Gravel (cascalho solto, pedrinhas redondas cinza). Sponge (espuma porosa amarela).

### `bedrock.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **bedrock** — rocha **quase preta** com fissuras irregulares cinza-escuro. Aspecto inquebrável/imune. Padrão caótico, sem geometria reconhecível.

Restrição da família a que pertence: **Sólidos diversos** que não pertencem a nenhuma família específica. Bedrock (rocha quase preta, irregular, fissuras). Bricks (parede de tijolos vermelhos com argamassa). Glowstone (aglomerado luminoso dourado-amarelado). Gravel (cascalho solto, pedrinhas redondas cinza). Sponge (espuma porosa amarela).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `bricks.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **tijolos** clássicos — parede de tijolos pequenos **vermelho-terracota** com **argamassa cinza-clara** entre eles. Padrão de fiada deslocada (offset entre fiadas).

Restrição da família a que pertence: **Sólidos diversos** que não pertencem a nenhuma família específica. Bedrock (rocha quase preta, irregular, fissuras). Bricks (parede de tijolos vermelhos com argamassa). Glowstone (aglomerado luminoso dourado-amarelado). Gravel (cascalho solto, pedrinhas redondas cinza). Sponge (espuma porosa amarela).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `glowstone.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **glowstone** — aglomerado de **bolinhas/cristais dourado-amarelo luminosos** (cluster orgânico), com aparência emissiva.

Restrição da família a que pertence: **Sólidos diversos** que não pertencem a nenhuma família específica. Bedrock (rocha quase preta, irregular, fissuras). Bricks (parede de tijolos vermelhos com argamassa). Glowstone (aglomerado luminoso dourado-amarelado). Gravel (cascalho solto, pedrinhas redondas cinza). Sponge (espuma porosa amarela).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `gravel.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **cascalho** — **pedrinhas redondas pequenas** cinza claras e escuras misturadas, distribuição aleatória.

Restrição da família a que pertence: **Sólidos diversos** que não pertencem a nenhuma família específica. Bedrock (rocha quase preta, irregular, fissuras). Bricks (parede de tijolos vermelhos com argamassa). Glowstone (aglomerado luminoso dourado-amarelado). Gravel (cascalho solto, pedrinhas redondas cinza). Sponge (espuma porosa amarela).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

### `sponge.png`

```
Faça uma variação da textura anexada (PNG 1024×1024,
estilo Minecraft, pixel-art preservado).

O que é esta textura: **esponja** — superfície **amarelo-mostarda porosa** com **buracos pequenos circulares** espalhados (poros da esponja).

Restrição da família a que pertence: **Sólidos diversos** que não pertencem a nenhuma família específica. Bedrock (rocha quase preta, irregular, fissuras). Bricks (parede de tijolos vermelhos com argamassa). Glowstone (aglomerado luminoso dourado-amarelado). Gravel (cascalho solto, pedrinhas redondas cinza). Sponge (espuma porosa amarela).

Restrições gerais de estilo:
- Saída 1024×1024 PNG, quadrado, sem padding/moldura/texto/marca d'água.
- Pixel-art com bordas duras de pixel: ZERO antialiasing, ZERO desfoque,
  ZERO gradiente suave. Cada "pixel" original = bloco 64×64 sólido.
- Tileável sem costura (borda esquerda casa com direita, topo com base).
- Paleta dentro da família — não muda a identidade de cor do bloco.
- O bloco precisa continuar reconhecível como o mesmo tipo de bloco.
```

---
