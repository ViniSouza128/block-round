# Plano de propagação — `Block_Round_Math_*.pdf` em 8 locales

Este documento descreve **todas as decisões e regras iteradas** durante a revisão do `Block_Round_Math_pt-BR.pdf`, para que num próximo prompt o assistente reproduza tudo nos 8 locales restantes: `en-US`, `es-ES`, `fr-FR`, `de-DE`, `zh-CN`, `ja-JP`, `ru-RU`, `ko-KR`.

> **Importante:** este plano é o input do próximo prompt. Ele NÃO deve ser executado agora — só serve como playbook. Leia, ajuste se precisar, e mande "execute o plano" quando estiver satisfeito.

---

## 1 · Estado atual (referência)

`Block_Round_Math_pt-BR.pdf` (36 páginas, ~1.7 MB) é o **gold standard**. Possui:

- Links coloridos (verde escuro `linkc = #2D5A1F`) clicáveis em URLs, TOC e bookmarks
- Underscores em `\code{path_com_underscore}` corretamente escapados como `\code{path\_with\_underscore}`
- Texto factualmente correto sobre o comportamento Minecraft (não fala "vazamento por frestas geométricas")
- 8 figuras geradas pelo Python (`gen_figures.py`) inseridas em pontos estratégicos das seções §3, §7, §9, §11, §15, §18, §20, §21
- Tabela §17.3 com `tabularx` (auto-wrap)
- Seção de Referências bibliográficas com 17 entradas em 4 categorias (técnicas, Minecraft, geometria/álgebra/grupos, algoritmos), além de recursos online

Os 8 outros locales (~25–31 páginas cada) atualmente:
- Já têm links coloridos (template-wide)
- Já têm underscore escapado em `\code{docs\_math/}` (corrigido nos 9)
- Já têm tabela §17.3 com tabularx (template-wide)
- Ainda **não** têm figuras (recebem string vazia em `FIG_*`)
- Ainda **não** têm bibliografia (recebem string vazia em `BIBLIOGRAPHY`)
- Ainda têm **claim incorreto** sobre vazamento de luz/água por frestas (precisam revisar factualmente)

---

## 2 · Lista de mudanças factuais (texto)

### 2.1 · "Frestas diagonais" → "células diagonais vazias"

O comportamento real do Minecraft: **luz e água propagam-se apenas por blocos de ar**, não por "fendas geométricas". O modo Fino deixa células diagonais vazias (que SÃO blocos de ar) — esse é o caminho do vazamento. Trechos a revisar em **cada** locale:

| Chave | Local (linha aprox.) |
|-------|----------------------|
| `S7_P5` | translations.py (en-US linha 107, outros nos arquivos satellite) |
| `S7_MC_EXAMPLE` | id. |
| `S12_P1` | id. (en-US linha 163) |
| `S12_P2` | id. |
| `S12_MC_EXAMPLE` | id. (en-US linha 166) |
| `APX_A_P2` | id. (en-US linha 318) |

**Termos a substituir em cada locale** (manter o equivalente idiomático em cada idioma):

| de | para |
|----|------|
| "diagonal cracks/gaps" "frestas diagonais" "rachaduras diagonais" "diagonale Risse" "fissures diagonales" "rendijas diagonales" "対角の隙間" "对角缝隙" "диагональные щели" "대각선 균열" | "empty diagonal cells" "células diagonais vazias" "celdas diagonales vacías" "leere Diagonalzellen" "cellules diagonales vides" "対角に空いたセル" "对角线上空着的方格" "пустые диагональные ячейки" "비어 있는 대각 셀들" |
| "leaking light/water through diagonal gaps" | "propagation of light/water through the empty diagonal cells" (locale-idiomatic) |
| "watertight"/"sealed" | "continuous" / "closed" (locale-idiomatic) |
| "vedar"/"selar"/"sellar"/"abdichten" | "preencher"/"fechar"/"close"/"fill" |

**Estado atual:** já corrigido em pt-BR e en-US (5 trechos cada). Faltam os 7 demais.

### 2.2 · `\code{...}` com underscore

**Já corrigido nos 9 locales.** Nenhuma ação necessária. (Quando criar texto novo, lembrar de escapar.)

### 2.3 · Bibliografia

Cada locale precisa adicionar uma entrada `BIBLIOGRAPHY` ao seu dict de traduções com a estrutura de 4 categorias. O conteúdo da bibliografia pt-BR está em `build.py` linhas 1077+ (`FIG_BLOCKS_PT_BR["BIBLIOGRAPHY"]`). Para cada locale precisamos:

1. **Mover** o `BIBLIOGRAPHY` de `FIG_BLOCKS_PT_BR` para uma estrutura geral `FIG_BLOCKS[locale]` em `build.py`;
2. **Traduzir** os títulos das 4 subseções + os comentários após cada referência ("— artigo original...", "— mod do Minecraft..."), mantendo os títulos das obras em inglês (e.g. "Algorithm for computer control of a digital plotter" não vira "Algoritmo para...").

### Esqueleto comum a manter em todos os locales

```latex
\section*{\color{accent}<<Bibliografia | Bibliography | Bibliographie | ...>>}
\addcontentsline{toc}{section}{<<Bibliografia>>}
\label{sec:bib}

\subsection*{<<Referências técnicas (rasterização e topologia digital)>>}
  - Bresenham, J. E. (1965)
  - Pitteway, M. L. V. (1967)
  - Kappel, A. (1985)
  - Klette, R.; Rosenfeld, A. (2004)
  - Foley et al. (2014)

\subsection*{<<Especificações e ferramentas Minecraft referenciadas>>}
  - Sponge Project — Schematic v2
  - EngineHub — WorldEdit
  - Mojang Wiki — Inventory, /fill, /clone
  - Masady — Litematica

\subsection*{<<Geometria, álgebra linear e teoria de grupos>>}
  - Lima, E. L. (2014)   [ou equivalente local]
  - Armstrong, M. A. (1988)
  - Coxeter, H. S. M. (1973)
  - Hilbert; Cohn-Vossen (1932)

\subsection*{<<Algoritmos e estruturas de dados>>}
  - Cormen et al. (2022)
  - Wirth (1976)

\subsection*{<<Recursos online complementares>>}
  - URLs Block Round, Pixel Round, plano de aula
```

### Substituições por locale (livro de geometria nacional)

A entrada "Lima, E. L. (2014)" é específica do Brasil. Cada locale recebe uma referência equivalente:

| locale | substituir Lima por |
|--------|---------------------|
| en-US  | Strang, G. *Linear Algebra and Its Applications*, 4th ed., Cengage, 2006 |
| es-ES  | Vinuesa, J. *Geometría Analítica*, Pirámide, 2009 |
| fr-FR  | Audin, M. *Géométrie*, EDP Sciences, 2006 |
| de-DE  | Fischer, G. *Analytische Geometrie*, Vieweg, 1985 |
| zh-CN  | 王萼芳, 石生明 (eds.). 《高等代数》, 北京: 高等教育出版社, 2003 |
| ja-JP  | 齋藤正彦. 《線型代数入門》, 東京大学出版会, 1966 |
| ru-RU  | Кострикин А. И., Манин Ю. И. *Линейная алгебра и геометрия*, Наука, 1986 |
| ko-KR  | 김홍중. 《선형대수와 그 응용》, 경문사, 2012 |

---

## 3 · Lista de blocos `FIG_*` a popular em cada locale

Os 21 PNGs em `docs_math/img/` são **comuns aos 9 locales**. O que muda é a legenda em LaTeX.

Cada locale precisa **adicionar 8 chaves** no seu dict (atualmente recebem `""` via `setdefault`):

| Chave | Conteúdo | Apêndice |
|-------|----------|----------|
| `FIG_3ALG` | 3 esferas D=10 (Euclidiano/Bresenham/Limiar) | aparece após §3 |
| `FIG_MODES` | 3 esferas D=20 (Preenchido/Fino/Grosso) | após §7 |
| `FIG_3D` | esfera D=10 + elipsóide 20×10×12 | após §9 |
| `FIG_CUTS` | 3 cortes 50% em D=16 (Y/X/diag) | após §11 |
| `FIG_SHADING` | 3 multiplicadores (Classic/Blocks/Smooth) | após §15 |
| `FIG_OVERLAY` | edge overlay ON vs OFF | após §18 |
| `FIG_OCTANTS` | octante destacado verde | após §20 (width 0.45) |
| `FIG_TEXTURES` | esfera D=8 em 3 texturas (cobble/oak/quartz) | DENTRO §21.1 (após S21_P3, não no final) |

Estrutura do LaTeX dentro de cada FIG_* (igual em todos os locales, só legenda muda):

```latex
\begin{figure}[!htbp]   % nao usar [H] — figura orfã na proxima pagina
\centering
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d10_eucl.png}
  \caption{\emph{<<Euclidean | Euclidien | Euclidiano | ...>>}}
\end{subfigure}\hfill
... (subfig × 3)
\caption{<<legenda traduzida>>}
\label{fig:comp-d10}   % manter labels iguais entre locales para refs cruzadas
\end{figure}
```

**Para `FIG_OCTANTS` usar `width=0.45\linewidth`** (não 0.55 como original).
**Para `FIG_TEXTURES` inserir no template ENTRE `«S21_P3»` e `\subsection{«S21_SUB2»}`** — atualmente está dentro de §21.1, não no final de §21.

---

## 4 · Mudanças template (build.py) — já aplicadas, NÃO refazer

As seguintes mudanças no template já estão presentes e afetam todos os locales:

```latex
% 1. Pacotes adicionados
\usepackage{subcaption}
\usepackage{caption}
\usepackage{float}
\graphicspath{{img/}}

% 2. Cor para links
\definecolor{linkc}{HTML}{2D5A1F}

% 3. Hyperref com colorlinks (substituido hidelinks)
\usepackage[colorlinks=true,
            linkcolor=linkc,
            urlcolor=linkc,
            citecolor=linkc,
            bookmarks=true,bookmarksopen=true,
            pdftitle={Block Round — «PDF_TITLE»},
            pdfauthor={Vinícius Rodrigues de Souza}]{hyperref}

% 4. Tabela S17.3: tabular -> tabularx
\begin{center}
\small
\begin{tabularx}{\textwidth}{@{}lrrlX@{}}
...
\end{tabularx}
\end{center}

% 5. Placeholders inseridos no template (cada um vira "" se locale != pt-BR atual)
«FIG_3ALG»     após o exemplo Minecraft de §3
«FIG_MODES»    após o exemplo Minecraft de §7
«FIG_3D»       após o exemplo Minecraft de §9
«FIG_CUTS»     após o exemplo Minecraft de §11
«FIG_SHADING»  após o §15 (15.3 último parágrafo)
«FIG_OVERLAY»  após §18 (18.3 último parágrafo)
«FIG_OCTANTS»  após §20 (20.2 último parágrafo)
«FIG_TEXTURES» dentro de §21, após S21_P3 (NÃO no final)
«BIBLIOGRAPHY» antes do `\clearpage` que precede o apêndice
```

A função `build(loc)` faz `cfg.setdefault(k, "")` para todas as chaves `FIG_*` + `BIBLIOGRAPHY`. Se o locale fornece a chave, ela é usada; senão, vira string vazia.

---

## 5 · Implementação proposta (próximo prompt deve executar)

### Passo 1 · Refatorar `FIG_BLOCKS_PT_BR` para `FIG_BLOCKS[locale]`

Trocar:
```python
FIG_BLOCKS_PT_BR = {...}

def build(loc):
    ...
    if loc == "pt-BR":
        cfg.update(FIG_BLOCKS_PT_BR)
```

Por:
```python
FIG_BLOCKS = {
    "pt-BR": {...},
    "en-US": {...},
    "es-ES": {...},
    # ... 9 locales
}

def build(loc):
    ...
    cfg.update(FIG_BLOCKS.get(loc, {}))
```

### Passo 2 · Para cada um dos 8 locales restantes, criar o dict completo

Cada dict tem 9 chaves: `FIG_3ALG`, `FIG_MODES`, `FIG_3D`, `FIG_CUTS`, `FIG_SHADING`, `FIG_OVERLAY`, `FIG_OCTANTS`, `FIG_TEXTURES`, `BIBLIOGRAPHY`.

Como modelo, copiar a versão pt-BR e:
1. Traduzir só o conteúdo de cada `\caption{...}` e os títulos `\subsection*{...}` da bibliografia
2. Traduzir só os comentários das referências (textos pós `---`)
3. **Manter** títulos de obras (inglês), nomes de autores, DOIs/URLs, labels `\label{fig:...}`
4. **Manter** o `\label{fig:comp-d10}`, `\label{fig:modes}`, etc — devem ser idênticos para que cross-refs funcionem se forem adicionadas
5. **Trocar** a referência "Lima, E. L." pela equivalente local da tabela em §2.3

### Passo 3 · Aplicar revisão factual

Para cada locale, abrir `translations*.py` e editar as 5 chaves indicadas em §2.1 substituindo o claim incorreto. Aproveitar o trabalho já feito em pt-BR/en-US como guia.

### Passo 4 · Recompilar tudo

```bash
cd docs_math && python build.py
```

Esperado:
- 9 PDFs gerados sem erros
- Cada PDF ≥ 25 páginas (pt-BR já tem 36, outros devem subir uns 4–6 pelos figuras)
- Sem `WARN chaves nao substituidas` no log
- Tabela §17.3 sem overflow lateral
- Figuras inseridas nos pontos esperados (visual check em 2-3 locales)

### Passo 5 · Limpar e commitar

```bash
cd docs_math
rm -f *.aux *.log *.toc *.out *_review*.png
cd ..
git add docs_math/
git commit -m "docs_math: replica revisao pt-BR para 8 locales (figuras, bibliografia, fix factual)"
git push origin main
```

Mensagem do commit deve listar:
- 8 locales propagados (en-US, es-ES, fr-FR, de-DE, zh-CN, ja-JP, ru-RU, ko-KR)
- Figuras (8 blocos × 8 locales = 64 entries traduzidos)
- Bibliografia (5 subseções × 8 locales)
- Revisão factual sobre frestas/células diagonais
- Páginas finais por locale

---

## 6 · Validações esperadas

| Item | Critério |
|------|----------|
| Páginas | Cada locale ≥ 25 |
| Sem `WARN chaves nao substituidas` | log de build limpo |
| Sem overfull \hbox > 100pt | warning aceitável até 100pt |
| Tabela §17.3 sem overflow lateral | "cúpula de catedral, arena de world-boss" quebra naturalmente |
| Bookmarks PDF | clique em "5. Bresenham" no leitor PDF deve saltar para a seção |
| URLs externas clicáveis | URLs em verde abrem o site |
| Sem menção a IA/Claude | em todos os arquivos |
| Commit autor `vinisouza128` | sem `Co-Authored-By` |
| Push para `main` por fast-forward | sem force-push |

---

## 7 · Tempo estimado

- Refatoração `FIG_BLOCKS_PT_BR` → `FIG_BLOCKS[locale]`: 5 min
- Cada locale (legendas + bibliografia + revisão factual): 15 min × 8 = 2h
- Build + validação: 20 min
- Commit + push: 5 min

**Total estimado:** ~2h30min

---

## 8 · Lista de checagem rápida (próximo prompt)

- [ ] Ler este plano por completo
- [ ] Confirmar que as 8 entradas de bibliografia em §2.3 batem com o que o usuário espera (livro de geometria nacional)
- [ ] Confirmar se quer cross-refs `\ref{sec:N}` em texto (exigiria adicionar `\label` em cada seção do template + reescrever textos pt-BR/en-US — não está incluído neste plano)
- [ ] Executar: refatoração + 8 traduções + build + commit + push

---

## 9 · O que NÃO está no escopo

- Adicionar `\label{}` em cada seção e converter "§5" textual em `\ref{sec:5}` clicável (invasivo demais)
- Mudar a paleta de cores ou layout
- Adicionar mais figuras além das 8 já planejadas
- Alterar conteúdo matemático (apenas correção factual)
- Criar mais locales além dos 9 existentes
- Modificar `docs_aula/` (escopo é apenas `docs_math/`)
