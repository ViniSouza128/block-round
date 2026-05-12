# Block Round — Math documents

Localized PDFs documenting the mathematical foundations of the project,
one file per locale supported by the app:

| Locale  | File                              |
|---------|-----------------------------------|
| en-US   | `Block_Round_Math_en-US.pdf`      |
| es-ES   | `Block_Round_Math_es-ES.pdf`      |
| pt-BR   | `Block_Round_Math_pt-BR.pdf`      |
| fr-FR   | `Block_Round_Math_fr-FR.pdf`      |
| de-DE   | `Block_Round_Math_de-DE.pdf`      |
| zh-CN   | `Block_Round_Math_zh-CN.pdf`      |
| ja-JP   | `Block_Round_Math_ja-JP.pdf`      |
| ru-RU   | `Block_Round_Math_ru-RU.pdf`      |
| ko-KR   | `Block_Round_Math_ko-KR.pdf`      |

Each PDF is at least 25 pages and covers the same 22 sections plus an
appendix in its respective language:

- Sections 1–15 share the continuous-to-discrete rasterization pipeline
  with the sibling project Pixel Round: coordinate system, the implicit
  ellipse equation, the three 2D rasterization algorithms (Euclidean,
  Bresenham, threshold), rendering modes, discrete-area computation, the
  ellipsoid equation, voxel volume, cutting planes (including the 45°
  diagonal), thick-3D slice composition, the 3D camera in spherical
  coordinates, auto-zoom via bounding sphere and FOV, and shading as a
  Lambertian approximation.
- Sections 17–21 are **specific to Block Round** and develop five new
  mathematical concerns introduced by the Minecraft-block layer:
  inventory arithmetic (packs of 64 and double chests of 3,456 items),
  highlight-overlay exposed-face counting, layer-by-layer horizontal
  decomposition for floor-by-floor construction, octahedral-symmetry
  optimization via `/clone`, and block-texture UV mapping with
  family/tone classification.
- Section 22 is the conclusion; Appendix A consolidates the key
  numerical tables, command references, worked example, keyboard
  shortcut listing, glossary, outlook and external references.

## Rebuilding

The PDFs are typeset with XeLaTeX. Requires a TeX distribution (e.g. MiKTeX)
with `unicode-math`, `polyglossia`, `xeCJK`, `tcolorbox`, `needspace`,
`booktabs` and `csquotes`. Non-Latin locales additionally require the
system fonts **Microsoft YaHei** (zh-CN), **Yu Gothic** (ja-JP),
**Malgun Gothic** (ko-KR) and **Cambria** (ru-RU).

```bash
cd docs_math
python build.py
```

The builder script is `build.py`; all translations live in
`translations.py` plus four appended modules (`translations_es_fr.py`,
`translations_de_zh.py`, `translations_ja_ru.py`, `translations_ko.py`).
Math content is shared across locales — only the prose varies.
