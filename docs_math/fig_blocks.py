# -*- coding: utf-8 -*-
"""Blocos de figura + bibliografia para cada locale do Block_Round_Math.

A versao pt-BR contem todas as 8 figuras + bibliografia completa (texto
longo). Os 8 demais locales seguem o mesmo template LaTeX mas com legendas
e bibliografia ligeiramente mais concisas, traduzidas em cada idioma.

Estrutura:
  _FIG_TPLS   -- 8 templates LaTeX de figura, com <<KEY>> placeholders
  _BIB_TPL    -- template LaTeX da bibliografia
  _materialize(strings) -- substitui <<KEY>> pelas strings traduzidas
  _FIG_TRANS  -- dict {locale: {KEY: traducao}} (~50 strings por locale)
  FIG_BLOCKS  -- dict {locale: {FIG_3ALG: latex, ..., BIBLIOGRAPHY: latex}}
"""

# ============================================================================
# TEMPLATES — esqueleto LaTeX com <<KEY>> a substituir
# ============================================================================

_FIG_TPLS = {
    "FIG_3ALG": r"""\begin{figure}[!ht]
\centering
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d10_eucl.png}
  \caption{\emph{<<EUCL>>}}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d10_bres.png}
  \caption{\emph{<<BRES>>}}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d10_thr.png}
  \caption{\emph{<<THR>>}}
\end{subfigure}
\caption{<<CAP_3ALG>>}
\label{fig:comp-d10}
\end{figure}""",

    "FIG_MODES": r"""\begin{figure}[!ht]
\centering
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d20_filled.png}
  \caption{\emph{<<FILLED>>}}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d20_thin.png}
  \caption{\emph{<<THIN>>}}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d20_thick.png}
  \caption{\emph{<<THICK>>}}
\end{subfigure}
\caption{<<CAP_MODES>>}
\label{fig:modes}
\end{figure}""",

    "FIG_3D": r"""\begin{figure}[!ht]
\centering
\begin{subfigure}[t]{0.46\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_sphere_d10.png}
  \caption{<<SPHERE_D10>>}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.46\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_ellipsoid.png}
  \caption{<<ELLIPSOID>>}
\end{subfigure}
\caption{<<CAP_3D>>}
\label{fig:3d-shapes}
\end{figure}""",

    "FIG_CUTS": r"""\begin{figure}[!ht]
\centering
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_cut_y.png}
  \caption{<<CUT_Y>>}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_cut_x.png}
  \caption{<<CUT_X>>}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_cut_diag.png}
  \caption{<<CUT_DIAG>>}
\end{subfigure}
\caption{<<CAP_CUTS>>}
\label{fig:cuts}
\end{figure}""",

    "FIG_SHADING": r"""\begin{figure}[!ht]
\centering
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_shading_classic.png}
  \caption{\emph{Classic} <<SHADING_CLASSIC>>}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_shading_blocks.png}
  \caption{\emph{Blocks} <<SHADING_BLOCKS>>}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_shading_smooth.png}
  \caption{\emph{Smooth} <<SHADING_SMOOTH>>}
\end{subfigure}
\caption{<<CAP_SHADING>>}
\label{fig:shading}
\end{figure}""",

    "FIG_OVERLAY": r"""\begin{figure}[!ht]
\centering
\begin{subfigure}[t]{0.40\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_overlay_off.png}
  \caption{<<OVERLAY_OFF>>}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.40\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_overlay_on.png}
  \caption{<<OVERLAY_ON>>}
\end{subfigure}
\caption{<<CAP_OVERLAY>>}
\label{fig:overlay}
\end{figure}""",

    "FIG_OCTANTS": r"""\begin{figure}[!ht]
\centering
\includegraphics[width=0.45\linewidth]{math_3d_octants.png}
\caption{<<CAP_OCTANTS>>}
\label{fig:octants}
\end{figure}""",

    "FIG_TEXTURES": r"""\begin{figure}[!ht]
\centering
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_tex_cobble.png}
  \caption{\emph{Cobblestone}}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_tex_oak.png}
  \caption{\emph{Oak Planks}}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_tex_quartz.png}
  \caption{\emph{Quartz Block}}
\end{subfigure}
\caption{<<CAP_TEXTURES>>}
\label{fig:textures}
\end{figure}""",
}

# Bibliography template: 18 referencias em 5 subsecoes + 4 recursos online.
# Os campos estaticos (autores, titulos no idioma original, DOIs/URLs) sao
# comuns; <<KEY>> sao apenas titulos de secao + comentarios por referencia +
# entrada do livro de geometria local (Lima/Strang/Audin/...).
_BIB_TPL = r"""\section*{\color{accent}<<BIB_TITLE>>}
\addcontentsline{toc}{section}{<<BIB_TITLE>>}
\label{sec:bib}

\subsection*{<<BIB_SUB1>>}

\begin{itemize}[leftmargin=1.4em,itemsep=0.3em,topsep=0.3em]
  \item \textbf{Bresenham, J. E.} \emph{Algorithm for computer control of a digital plotter}.
        IBM Systems Journal, vol.~4, n.~1, p.~25--30, 1965.
        <<BIB_AVAILABLE_AT>> \biblink{https://doi.org/10.1147/sj.41.0025}{doi:10.1147/sj.41.0025}.
        --- <<BIB_C_BRESENHAM>>

  \item \textbf{Pitteway, M.~L.~V.} \emph{Algorithm for drawing ellipses or hyperbolae
        with a digital plotter}. The Computer Journal, vol.~10, n.~3, p.~282--289, 1967.
        <<BIB_AVAILABLE_AT>> \biblink{https://doi.org/10.1093/comjnl/10.3.282}{doi:10.1093/comjnl/10.3.282}.
        --- <<BIB_C_PITTEWAY>>

  \item \textbf{Kappel, A.} \emph{An ellipse-drawing algorithm for raster displays}.
        <<BIB_KAPPEL_IN>> \emph{Fundamental Algorithms for Computer Graphics} (R.~A.~Earnshaw, ed.),
        NATO ASI Series F-17, Springer, 1985, p.~257--280.
        --- <<BIB_C_KAPPEL>>

  \item \textbf{Klette, R.; Rosenfeld, A.} \emph{Digital Geometry: Geometric Methods
        for Digital Picture Analysis}. Morgan Kaufmann, 2004. 656 <<BIB_PAGES>>.
        --- <<BIB_C_KLETTE>>

  \item \textbf{Foley, J.~D.; van Dam, A.; Feiner, S.~K.; Hughes, J.~F.}
        \emph{Computer Graphics: Principles and Practice}. <<BIB_3RD_ED>>, Addison-Wesley, 2014.
        --- <<BIB_C_FOLEY>>
\end{itemize}

\subsection*{<<BIB_SUB2>>}

\begin{itemize}[leftmargin=1.4em,itemsep=0.3em,topsep=0.3em]
  \item \textbf{Sponge Project.} \emph{Sponge Schematic Specification, version~2}.
        \biblink{https://github.com/SpongePowered/Schematic-Specification}{github.com/SpongePowered/Schematic-Specification}.
        --- <<BIB_C_SPONGE>>

  \item \textbf{EngineHub.} \emph{WorldEdit Documentation}.
        \biblink{https://worldedit.enginehub.org/}{worldedit.enginehub.org}.
        --- <<BIB_C_WORLDEDIT>>

  \item \textbf{Mojang AB.} \emph{Minecraft Wiki --- Inventory}.
        \biblink{https://minecraft.wiki/w/Inventory}{minecraft.wiki/w/Inventory}.
        --- <<BIB_C_MCINVENTORY>>

  \item \textbf{Mojang AB.} \emph{Minecraft Wiki --- Commands/fill, /clone}.
        \biblink{https://minecraft.wiki/w/Commands/fill}{minecraft.wiki/w/Commands/fill},
        \biblink{https://minecraft.wiki/w/Commands/clone}{minecraft.wiki/w/Commands/clone}.
        --- <<BIB_C_MCCOMMANDS>>

  \item \textbf{Masady} (\emph{Litematica} mod).
        \biblink{https://github.com/maruohon/litematica}{github.com/maruohon/litematica}.
        --- <<BIB_C_LITEMATICA>>
\end{itemize}

\subsection*{<<BIB_SUB3>>}

\begin{itemize}[leftmargin=1.4em,itemsep=0.3em,topsep=0.3em]
  <<BIB_LIMA_ENTRY>>

  \item \textbf{Armstrong, M.~A.} \emph{Groups and Symmetry}. Undergraduate Texts in
        Mathematics, Springer, 1988.
        --- <<BIB_C_ARMSTRONG>>

  \item \textbf{Coxeter, H.~S.~M.} \emph{Regular Polytopes}. <<BIB_3RD_ED>>, Dover, 1973.
        --- <<BIB_C_COXETER>>

  \item \textbf{Hilbert, D.; Cohn-Vossen, S.} \emph{Geometry and the Imagination}.
        AMS Chelsea, 1990 [orig.~1932].
        --- <<BIB_C_HILBERT>>
\end{itemize}

\subsection*{<<BIB_SUB4>>}

\begin{itemize}[leftmargin=1.4em,itemsep=0.3em,topsep=0.3em]
  \item \textbf{Cormen, T.~H.; Leiserson, C.~E.; Rivest, R.~L.; Stein, C.}
        \emph{Introduction to Algorithms}. <<BIB_4TH_ED>>, MIT Press, 2022.
        --- <<BIB_C_CORMEN>>

  \item \textbf{Wirth, N.} \emph{Algorithms + Data Structures = Programs}.
        Prentice-Hall, 1976.
        --- <<BIB_C_WIRTH>>
\end{itemize}

\subsection*{<<BIB_SUB5>>}

\begin{itemize}[leftmargin=1.4em,itemsep=0.3em,topsep=0.3em]
  \item <<BIB_ONLINE_APP>>: \biblink{https://vinisouza128.github.io/block-round/}{vinisouza128.github.io/block-round/}.
  \item <<BIB_ONLINE_REPO>>: \biblink{https://github.com/ViniSouza128/block-round}{github.com/ViniSouza128/block-round}.
  \item <<BIB_ONLINE_PIXELROUND>>:
        \biblink{https://github.com/ViniSouza128/pixel-round}{github.com/ViniSouza128/pixel-round}.
  \item <<BIB_ONLINE_AULA>>
\end{itemize}
"""


def _materialize(strings):
    """Substitui <<KEY>> nos templates pelas strings do locale."""
    out = {}
    for k, tpl in _FIG_TPLS.items():
        s = tpl
        for kk, vv in strings.items():
            s = s.replace("<<" + kk + ">>", vv)
        out[k] = s
    bib = _BIB_TPL
    for kk, vv in strings.items():
        bib = bib.replace("<<" + kk + ">>", vv)
    out["BIBLIOGRAPHY"] = bib
    return out


# ============================================================================
# TRADUCOES POR LOCALE
# ============================================================================

_FIG_TRANS = {}


# ----------------------------------------------------------------------------
# pt-BR — versao detalhada/longa (corresponde ao FIG_BLOCKS_PT_BR original)
# ----------------------------------------------------------------------------
_FIG_TRANS["pt-BR"] = dict(
    EUCL="Euclidiano",
    BRES="Bresenham",
    THR="Limiar",
    FILLED="Preenchido",
    THIN=r"Fino (\emph{1 voxel})",
    THICK="Grosso",
    SPHERE_D10=r"Esfera $D=10$, $r_x=r_y=r_z=5$.",
    ELLIPSOID=r"Elipsóide $W=20,\,H=10,\,D=12$.",
    CUT_Y=r"Corte $Y$ 50\% (cúpula)",
    CUT_X=r"Corte $X$ 50\%",
    CUT_DIAG=r"Diagonal 50\%",
    SHADING_CLASSIC=r"(contraste forte)",
    SHADING_BLOCKS=r"(default)",
    SHADING_SMOOTH=r"(faces parecidas)",
    OVERLAY_OFF=r"Overlay \emph{OFF}",
    OVERLAY_ON=r"Overlay \emph{ON} (default)",
    CAP_3ALG=r"Mesma circunferência de diâmetro $D=10$ sob os três critérios. Cada figura é o conjunto de células marcadas pela respectiva versão da desigualdade $d_x^2+d_y^2\leq 1$, renderizada com a textura \emph{cobblestone} do Minecraft. Note como a transição entre filas, as células de quina e os pontos cardeais variam --- três respostas matematicamente corretas sob critérios distintos.",
    CAP_MODES=r"Os três modos de renderização para a mesma circunferência euclidiana de $D=20$. O modo \emph{Fino} corresponde ao bordo discreto topológico ($\partial F$); o modo \emph{Grosso} adiciona blocos diagonais para fechar buracos a $45^\circ$, essencial para construções estanques (cúpulas de Vidro/Gelo subaquáticas).",
    CAP_3D=r"Voxelização em $\mathbb{R}^3$. Cada cubo é um voxel; sua coordenada $(i,j,k)$ no centro é testada na equação implícita $a_x^2+a_y^2+a_z^2\leq 1$. As escadarias visíveis na superfície são consequência matemática da discretização --- exatamente o aspecto que dá ao Minecraft sua identidade visual.",
    CAP_CUTS=r"Três cortes na mesma esfera $D=16$, todos preservando 50\% do volume. O corte $Y$ produz a cúpula clássica $V_{\mathrm{cúpula}}=\tfrac{2}{3}\pi r^3$; o diagonal expõe a hipotenusa $x+y=k$ característica desse plano de corte.",
    CAP_SHADING=r"Três multiplicadores de luz aplicados às mesmas três faces visíveis. \emph{Classic} dá o aspecto canônico Minecraft vanilla; \emph{Smooth} reduz o contraste para superfícies suaves; \emph{Blocks} é o intermediário com inset geométrico que revela fronteiras entre voxels mesmo quando a textura é a mesma.",
    CAP_OVERLAY=r"Mesmo conjunto de voxels com e sem o contorno preto nas arestas expostas. Com o \emph{highlight overlay} ON, um bloco faltante na casca produz uma descontinuidade no padrão que o olho detecta de relance --- ferramenta de validação rápida durante a construção em survival.",
    CAP_OCTANTS=r"Esfera $D=10$ com o octante positivo $(+x,+y,+z)$ destacado em verde. Sob a ação do subgrupo $\mathbb{Z}_2^3 \leq O_h$ (ordem 8, gerado pelas três reflexões coordenadas), esse octante determina toda a esfera --- as outras sete regiões são obtidas por uma sequência de \cmd{/clone} com \emph{mode:masked} aplicadas sobre o octante construído manualmente.",
    CAP_TEXTURES=r"A mesma esfera de diâmetro $D=8$ renderizada com três blocos diferentes. A silhueta voxelizada (matemática) é idêntica nas três: o algoritmo escolhe os voxels, a textura é uma camada estética posterior que não altera nem o volume nem a topologia.",
    BIB_TITLE="Referências bibliográficas",
    BIB_SUB1="Referências técnicas (rasterização e topologia digital)",
    BIB_SUB2="Especificações e ferramentas Minecraft referenciadas",
    BIB_SUB3="Geometria, álgebra linear e teoria de grupos",
    BIB_SUB4="Algoritmos, estruturas de dados, complexidade",
    BIB_SUB5="Recursos online complementares",
    BIB_AVAILABLE_AT="Disponível em",
    BIB_PAGES="páginas",
    BIB_3RD_ED=r"3.\textordmasculine{} ed.",
    BIB_4TH_ED=r"4.\textordmasculine{} ed.",
    BIB_KAPPEL_IN="Em",
    BIB_C_BRESENHAM=r"artigo original do algoritmo de meio-ponto inteiro tratado na §5 deste documento.",
    BIB_C_PITTEWAY=r"generalização do algoritmo de Bresenham para cônicas arbitrárias, base da extensão para elipses descrita na §5.",
    BIB_C_KAPPEL=r"formulação por duas regiões usada na implementação de elipses.",
    BIB_C_KLETTE=r"referência padrão para topologia digital, operadores de bordo ($\partial F$), 4-/6-/26-conectividade. Usada nas §7, §12 e §18.",
    BIB_C_FOLEY=r"tratamento clássico de rasterização, modelos de iluminação, projeção perspectiva. Relevante para as §13--15.",
    BIB_C_SPONGE=r"formato de arquivo \code{.schem} (gzip + NBT) que o Block Round exporta. Carregável por WorldEdit, Litematica e MCEdit.",
    BIB_C_WORLDEDIT=r"referência oficial para os comandos \cmd{//sphere}, \cmd{//hsphere}, \cmd{//ellipsoid}, \cmd{//cyl}, \cmd{//schem load} citados ao longo do documento.",
    BIB_C_MCINVENTORY=r"referência sobre slots, stacks, baús simples (27 slots) e baús duplos (54 slots) usados na §17.",
    BIB_C_MCCOMMANDS=r"comandos vanilla \cmd{/fill} e \cmd{/clone} citados nas §17 e §20.",
    BIB_C_LITEMATICA=r"mod do Minecraft Java Edition que importa schematics e exibe um fantasma translúcido da construção a executar.",
    BIB_LIMA_ENTRY=r"""\item \textbf{Lima, E.~L.} \emph{Geometria Analítica e Álgebra Linear}. Coleção
        Matemática Universitária, IMPA, 2.\textordmasculine{} ed., 2014.
        --- equação implícita da elipse, álgebra de planos no $\mathbb{R}^3$,
        coordenadas esféricas. Base do conteúdo das §3, §9 e §13.""",
    BIB_C_ARMSTRONG=r"exposição introdutória ao grupo octaédrico $O_h$ e seus subgrupos, usada na §20.",
    BIB_C_COXETER=r"referência canônica para os grupos de simetria dos sólidos regulares, incluindo o tratamento detalhado de $O_h$ de ordem 48 mencionado na §20.",
    BIB_C_HILBERT=r"tratamento clássico de quádricas e visualização geométrica, base intuitiva da §9.",
    BIB_C_CORMEN=r"análise de complexidade dos três algoritmos da §4--6, divisão com teto da §17.",
    BIB_C_WIRTH=r"exposição clássica do algoritmo de Bresenham para retas e sua extensão para circunferências.",
    BIB_ONLINE_APP="Block Round --- aplicativo",
    BIB_ONLINE_REPO="Block Round --- repositório",
    BIB_ONLINE_PIXELROUND="Projeto irmão Pixel Round (versão sem texturas Minecraft)",
    BIB_ONLINE_AULA=r"""Plano de aula em pt-BR (3.\textordmasculine{} ano EM):
        \biblink{https://vinisouza128.github.io/block-round/docs_aula/Plano_de_Aula_pt-BR.pdf}{docs\_aula/Plano\_de\_Aula\_pt-BR.pdf}.""",
)


# ----------------------------------------------------------------------------
# en-US — English (US)
# ----------------------------------------------------------------------------
_FIG_TRANS["en-US"] = dict(
    EUCL="Euclidean",
    BRES="Bresenham",
    THR="Threshold",
    FILLED="Filled",
    THIN=r"Thin (\emph{1 voxel})",
    THICK="Thick",
    SPHERE_D10=r"Sphere $D=10$, $r_x=r_y=r_z=5$.",
    ELLIPSOID=r"Ellipsoid $W=20,\,H=10,\,D=12$.",
    CUT_Y=r"$Y$ cut 50\% (dome)",
    CUT_X=r"$X$ cut 50\%",
    CUT_DIAG=r"Diagonal 50\%",
    SHADING_CLASSIC=r"(strong contrast)",
    SHADING_BLOCKS=r"(default)",
    SHADING_SMOOTH=r"(similar faces)",
    OVERLAY_OFF=r"Overlay \emph{OFF}",
    OVERLAY_ON=r"Overlay \emph{ON} (default)",
    CAP_3ALG=r"Same circumference of diameter $D=10$ under the three criteria. Each figure shows the set of cells marked by the corresponding version of $d_x^2+d_y^2\leq 1$, rendered with Minecraft \emph{cobblestone}. Notice how the row transitions, corner cells and cardinal points differ --- three mathematically correct answers under distinct criteria.",
    CAP_MODES=r"The three rendering modes for the same Euclidean circumference of $D=20$. The \emph{Thin} mode corresponds to the discrete topological boundary ($\partial F$); the \emph{Thick} mode adds diagonal cells to seal $45^\circ$ holes, essential for watertight builds (underwater Glass/Ice domes).",
    CAP_3D=r"Voxelisation in $\mathbb{R}^3$. Each cube is a voxel; its centre coordinate $(i,j,k)$ is tested against the implicit equation $a_x^2+a_y^2+a_z^2\leq 1$. The visible surface staircases are a mathematical consequence of discretisation --- the very property that gives Minecraft its visual identity.",
    CAP_CUTS=r"Three cuts on the same $D=16$ sphere, each preserving 50\% of the volume. The $Y$ cut produces the classical dome $V_{\mathrm{dome}}=\tfrac{2}{3}\pi r^3$; the diagonal exposes the hypotenuse $x+y=k$ characteristic of that cutting plane.",
    CAP_SHADING=r"Three light multipliers applied to the same three visible faces. \emph{Classic} yields the canonical Minecraft vanilla look; \emph{Smooth} reduces contrast for smooth surfaces; \emph{Blocks} is the intermediate default with geometric inset that reveals voxel boundaries even when the texture is the same.",
    CAP_OVERLAY=r"Same voxel set with and without the black outline on exposed edges. With the \emph{highlight overlay} ON, a missing block in the shell yields a pattern discontinuity that the eye catches at a glance --- a quick validation tool during survival construction.",
    CAP_OCTANTS=r"$D=10$ sphere with positive octant $(+x,+y,+z)$ highlighted in green. Under the action of the subgroup $\mathbb{Z}_2^3 \leq O_h$ (order 8, generated by the three coordinate reflections), this octant determines the entire sphere --- the other seven regions are obtained via a sequence of \cmd{/clone} calls with \emph{mode:masked} applied to the manually built octant.",
    CAP_TEXTURES=r"The same $D=8$ sphere rendered with three different blocks. The voxelised silhouette (mathematics) is identical across all three: the algorithm picks the voxels; the texture is a purely aesthetic layer applied afterwards that changes neither volume nor topology.",
    BIB_TITLE="Bibliography",
    BIB_SUB1="Technical references (rasterisation and digital topology)",
    BIB_SUB2="Minecraft specifications and tools referenced",
    BIB_SUB3="Geometry, linear algebra and group theory",
    BIB_SUB4="Algorithms, data structures, complexity",
    BIB_SUB5="Complementary online resources",
    BIB_AVAILABLE_AT="Available at",
    BIB_PAGES="pages",
    BIB_3RD_ED="3rd ed.",
    BIB_4TH_ED="4th ed.",
    BIB_KAPPEL_IN="In",
    BIB_C_BRESENHAM=r"original paper of the integer mid-point algorithm covered in §5.",
    BIB_C_PITTEWAY=r"generalisation of the Bresenham algorithm to arbitrary conics, the basis of the ellipse extension described in §5.",
    BIB_C_KAPPEL=r"two-region formulation used in the ellipse implementation.",
    BIB_C_KLETTE=r"standard reference for digital topology, boundary operators ($\partial F$), 4-/6-/26-connectivity. Used in §7, §12 and §18.",
    BIB_C_FOLEY=r"classical treatment of rasterisation, lighting models, perspective projection. Relevant to §13--15.",
    BIB_C_SPONGE=r"file format \code{.schem} (gzip + NBT) that Block Round exports. Loadable by WorldEdit, Litematica and MCEdit.",
    BIB_C_WORLDEDIT=r"official reference for the \cmd{//sphere}, \cmd{//hsphere}, \cmd{//ellipsoid}, \cmd{//cyl}, \cmd{//schem load} commands cited throughout this document.",
    BIB_C_MCINVENTORY=r"reference on slots, stacks, single chests (27 slots) and double chests (54 slots) used in §17.",
    BIB_C_MCCOMMANDS=r"vanilla commands \cmd{/fill} and \cmd{/clone} cited in §17 and §20.",
    BIB_C_LITEMATICA=r"Minecraft Java Edition mod that imports schematics and displays a translucent ghost of the build to execute.",
    BIB_LIMA_ENTRY=r"""\item \textbf{Strang, G.} \emph{Linear Algebra and Its Applications}. 4th ed.,
        Cengage Learning, 2006.
        --- implicit equation of the ellipse, plane algebra in $\mathbb{R}^3$,
        spherical coordinates. Basis for the content of §3, §9 and §13.""",
    BIB_C_ARMSTRONG=r"introductory exposition of the octahedral group $O_h$ and its subgroups, used in §20.",
    BIB_C_COXETER=r"canonical reference for the symmetry groups of regular solids, including the detailed treatment of $O_h$ of order 48 mentioned in §20.",
    BIB_C_HILBERT=r"classical treatment of quadrics and geometric visualisation, intuitive basis for §9.",
    BIB_C_CORMEN=r"complexity analysis of the three algorithms in §4--6, ceiling division in §17.",
    BIB_C_WIRTH=r"classical exposition of the Bresenham algorithm for lines and its extension to circumferences.",
    BIB_ONLINE_APP="Block Round --- app",
    BIB_ONLINE_REPO="Block Round --- repository",
    BIB_ONLINE_PIXELROUND="Sibling project Pixel Round (Minecraft-texture-free variant)",
    BIB_ONLINE_AULA=r"""Lesson plan in pt-BR (3rd year of secondary school):
        \biblink{https://vinisouza128.github.io/block-round/docs_aula/Plano_de_Aula_pt-BR.pdf}{docs\_aula/Plano\_de\_Aula\_pt-BR.pdf}.""",
)


# ----------------------------------------------------------------------------
# es-ES — Espanol (Espana)
# ----------------------------------------------------------------------------
_FIG_TRANS["es-ES"] = dict(
    EUCL="Euclidiano",
    BRES="Bresenham",
    THR="Umbral",
    FILLED="Relleno",
    THIN=r"Fino (\emph{1 vóxel})",
    THICK="Grueso",
    SPHERE_D10=r"Esfera $D=10$, $r_x=r_y=r_z=5$.",
    ELLIPSOID=r"Elipsoide $W=20,\,H=10,\,D=12$.",
    CUT_Y=r"Corte $Y$ 50\% (cúpula)",
    CUT_X=r"Corte $X$ 50\%",
    CUT_DIAG=r"Diagonal 50\%",
    SHADING_CLASSIC=r"(contraste fuerte)",
    SHADING_BLOCKS=r"(por defecto)",
    SHADING_SMOOTH=r"(caras parecidas)",
    OVERLAY_OFF=r"Superposición \emph{OFF}",
    OVERLAY_ON=r"Superposición \emph{ON} (por defecto)",
    CAP_3ALG=r"Misma circunferencia de diámetro $D=10$ bajo los tres criterios. Cada figura muestra el conjunto de celdas marcadas por la versión correspondiente de $d_x^2+d_y^2\leq 1$, renderizada con la textura \emph{cobblestone} de Minecraft. Observa cómo varían las transiciones entre filas, las celdas de esquina y los puntos cardinales: tres respuestas matemáticamente correctas bajo criterios distintos.",
    CAP_MODES=r"Los tres modos de renderizado para la misma circunferencia euclidiana de $D=20$. El modo \emph{Fino} corresponde al borde discreto topológico ($\partial F$); el modo \emph{Grueso} añade celdas diagonales para sellar los huecos a $45^\circ$, esencial para construcciones estancas (cúpulas de Vidrio/Hielo bajo el agua).",
    CAP_3D=r"Voxelización en $\mathbb{R}^3$. Cada cubo es un vóxel; su coordenada del centro $(i,j,k)$ se evalúa en la ecuación implícita $a_x^2+a_y^2+a_z^2\leq 1$. Las escaleras visibles en la superficie son consecuencia matemática de la discretización: precisamente el rasgo que da a Minecraft su identidad visual.",
    CAP_CUTS=r"Tres cortes sobre la misma esfera de $D=16$, cada uno conservando el 50\% del volumen. El corte $Y$ produce la cúpula clásica $V_{\mathrm{cúpula}}=\tfrac{2}{3}\pi r^3$; el diagonal expone la hipotenusa $x+y=k$ característica de ese plano de corte.",
    CAP_SHADING=r"Tres multiplicadores de luz aplicados a las mismas tres caras visibles. \emph{Classic} ofrece el aspecto canónico de Minecraft vanilla; \emph{Smooth} reduce el contraste para superficies suaves; \emph{Blocks} es el intermedio por defecto con un retranqueo geométrico que revela las fronteras entre vóxeles aunque la textura sea la misma.",
    CAP_OVERLAY=r"Mismo conjunto de vóxeles con y sin el contorno negro en las aristas expuestas. Con el \emph{highlight overlay} ON, un bloque que falte en la cáscara produce una discontinuidad en el patrón que el ojo detecta de un vistazo: una herramienta de validación rápida durante la construcción en supervivencia.",
    CAP_OCTANTS=r"Esfera $D=10$ con el octante positivo $(+x,+y,+z)$ resaltado en verde. Bajo la acción del subgrupo $\mathbb{Z}_2^3 \leq O_h$ (orden 8, generado por las tres reflexiones coordenadas), este octante determina toda la esfera: las otras siete regiones se obtienen mediante una secuencia de \cmd{/clone} con \emph{mode:masked} aplicada sobre el octante construido manualmente.",
    CAP_TEXTURES=r"La misma esfera de diámetro $D=8$ renderizada con tres bloques distintos. La silueta voxelizada (la matemática) es idéntica en las tres: el algoritmo elige los vóxeles; la textura es una capa puramente estética aplicada después que no altera ni el volumen ni la topología.",
    BIB_TITLE="Bibliografía",
    BIB_SUB1="Referencias técnicas (rasterización y topología digital)",
    BIB_SUB2="Especificaciones y herramientas de Minecraft referenciadas",
    BIB_SUB3="Geometría, álgebra lineal y teoría de grupos",
    BIB_SUB4="Algoritmos, estructuras de datos, complejidad",
    BIB_SUB5="Recursos en línea complementarios",
    BIB_AVAILABLE_AT="Disponible en",
    BIB_PAGES="páginas",
    BIB_3RD_ED=r"3.\textsuperscript{a} ed.",
    BIB_4TH_ED=r"4.\textsuperscript{a} ed.",
    BIB_KAPPEL_IN="En",
    BIB_C_BRESENHAM=r"artículo original del algoritmo del punto medio entero tratado en §5.",
    BIB_C_PITTEWAY=r"generalización del algoritmo de Bresenham a cónicas arbitrarias, base de la extensión a elipses descrita en §5.",
    BIB_C_KAPPEL=r"formulación por dos regiones empleada en la implementación de elipses.",
    BIB_C_KLETTE=r"referencia estándar para topología digital, operadores de borde ($\partial F$), 4-/6-/26-conectividad. Usada en §7, §12 y §18.",
    BIB_C_FOLEY=r"tratamiento clásico de rasterización, modelos de iluminación, proyección en perspectiva. Relevante para §13--15.",
    BIB_C_SPONGE=r"formato de archivo \code{.schem} (gzip + NBT) que exporta Block Round. Cargable por WorldEdit, Litematica y MCEdit.",
    BIB_C_WORLDEDIT=r"referencia oficial para los comandos \cmd{//sphere}, \cmd{//hsphere}, \cmd{//ellipsoid}, \cmd{//cyl}, \cmd{//schem load} citados a lo largo del documento.",
    BIB_C_MCINVENTORY=r"referencia sobre ranuras, pilas, cofres simples (27 ranuras) y cofres dobles (54 ranuras) usados en §17.",
    BIB_C_MCCOMMANDS=r"comandos vanilla \cmd{/fill} y \cmd{/clone} citados en §17 y §20.",
    BIB_C_LITEMATICA=r"mod de Minecraft Java Edition que importa schematics y muestra un fantasma translúcido de la construcción a ejecutar.",
    BIB_LIMA_ENTRY=r"""\item \textbf{Vinuesa, J.} \emph{Geometría Analítica}. Pirámide, 2009.
        --- ecuación implícita de la elipse, álgebra de planos en $\mathbb{R}^3$,
        coordenadas esféricas. Base del contenido de §3, §9 y §13.""",
    BIB_C_ARMSTRONG=r"exposición introductoria al grupo octaédrico $O_h$ y sus subgrupos, usada en §20.",
    BIB_C_COXETER=r"referencia canónica para los grupos de simetría de los sólidos regulares, incluyendo el tratamiento detallado de $O_h$ de orden 48 mencionado en §20.",
    BIB_C_HILBERT=r"tratamiento clásico de cuádricas y visualización geométrica, base intuitiva de §9.",
    BIB_C_CORMEN=r"análisis de complejidad de los tres algoritmos de §4--6, división con techo de §17.",
    BIB_C_WIRTH=r"exposición clásica del algoritmo de Bresenham para rectas y su extensión a circunferencias.",
    BIB_ONLINE_APP="Block Round --- aplicación",
    BIB_ONLINE_REPO="Block Round --- repositorio",
    BIB_ONLINE_PIXELROUND="Proyecto hermano Pixel Round (variante sin texturas de Minecraft)",
    BIB_ONLINE_AULA=r"""Plan de clase en pt-BR (3.\textsuperscript{er} año de bachillerato):
        \biblink{https://vinisouza128.github.io/block-round/docs_aula/Plano_de_Aula_pt-BR.pdf}{docs\_aula/Plano\_de\_Aula\_pt-BR.pdf}.""",
)


# ----------------------------------------------------------------------------
# fr-FR — Francais (France)
# ----------------------------------------------------------------------------
_FIG_TRANS["fr-FR"] = dict(
    EUCL="Euclidien",
    BRES="Bresenham",
    THR="Seuil",
    FILLED="Rempli",
    THIN=r"Fin (\emph{1 voxel})",
    THICK="Épais",
    SPHERE_D10=r"Sphère $D=10$, $r_x=r_y=r_z=5$.",
    ELLIPSOID=r"Ellipsoïde $W=20,\,H=10,\,D=12$.",
    CUT_Y=r"Coupe $Y$ 50\% (dôme)",
    CUT_X=r"Coupe $X$ 50\%",
    CUT_DIAG=r"Diagonale 50\%",
    SHADING_CLASSIC=r"(contraste fort)",
    SHADING_BLOCKS=r"(par défaut)",
    SHADING_SMOOTH=r"(faces similaires)",
    OVERLAY_OFF=r"Surimpression \emph{OFF}",
    OVERLAY_ON=r"Surimpression \emph{ON} (par défaut)",
    CAP_3ALG=r"Même circonférence de diamètre $D=10$ sous les trois critères. Chaque figure montre l'ensemble des cellules marquées par la version correspondante de $d_x^2+d_y^2\leq 1$, rendue avec la texture \emph{cobblestone} de Minecraft. Observez comment varient les transitions entre rangées, les cellules de coin et les points cardinaux : trois réponses mathématiquement correctes sous des critères distincts.",
    CAP_MODES=r"Les trois modes de rendu pour la même circonférence euclidienne de $D=20$. Le mode \emph{Fin} correspond au bord discret topologique ($\partial F$) ; le mode \emph{Épais} ajoute des cellules diagonales pour combler les trous à $45^\circ$, essentiel pour les constructions étanches (dômes de Verre/Glace sous l'eau).",
    CAP_3D=r"Voxélisation dans $\mathbb{R}^3$. Chaque cube est un voxel ; sa coordonnée centrale $(i,j,k)$ est testée dans l'équation implicite $a_x^2+a_y^2+a_z^2\leq 1$. Les escaliers visibles à la surface sont une conséquence mathématique de la discrétisation --- précisément la propriété qui donne à Minecraft son identité visuelle.",
    CAP_CUTS=r"Trois coupes sur la même sphère $D=16$, chacune préservant 50\% du volume. La coupe $Y$ produit le dôme classique $V_{\mathrm{dôme}}=\tfrac{2}{3}\pi r^3$ ; la diagonale expose l'hypoténuse $x+y=k$ caractéristique de ce plan de coupe.",
    CAP_SHADING=r"Trois multiplicateurs de lumière appliqués aux mêmes trois faces visibles. \emph{Classic} donne l'aspect canonique de Minecraft vanilla ; \emph{Smooth} réduit le contraste pour des surfaces lisses ; \emph{Blocks} est l'intermédiaire par défaut avec un retrait géométrique qui révèle les frontières entre voxels même lorsque la texture est identique.",
    CAP_OVERLAY=r"Même ensemble de voxels avec et sans le contour noir sur les arêtes exposées. Avec le \emph{highlight overlay} ON, un bloc manquant dans la coque produit une discontinuité dans le motif que l'œil détecte d'un coup d'œil --- un outil de validation rapide lors de la construction en survie.",
    CAP_OCTANTS=r"Sphère $D=10$ avec l'octant positif $(+x,+y,+z)$ mis en évidence en vert. Sous l'action du sous-groupe $\mathbb{Z}_2^3 \leq O_h$ (ordre 8, engendré par les trois réflexions coordonnées), cet octant détermine toute la sphère --- les sept autres régions sont obtenues par une suite de \cmd{/clone} avec \emph{mode:masked} appliquée à l'octant construit manuellement.",
    CAP_TEXTURES=r"La même sphère de diamètre $D=8$ rendue avec trois blocs différents. La silhouette voxélisée (la mathématique) est identique dans les trois : l'algorithme choisit les voxels ; la texture est une couche purement esthétique appliquée ensuite qui ne modifie ni le volume ni la topologie.",
    BIB_TITLE="Bibliographie",
    BIB_SUB1="Références techniques (rastérisation et topologie numérique)",
    BIB_SUB2="Spécifications et outils Minecraft référencés",
    BIB_SUB3="Géométrie, algèbre linéaire et théorie des groupes",
    BIB_SUB4="Algorithmes, structures de données, complexité",
    BIB_SUB5="Ressources en ligne complémentaires",
    BIB_AVAILABLE_AT="Disponible sur",
    BIB_PAGES="pages",
    BIB_3RD_ED=r"3\textsuperscript{e} éd.",
    BIB_4TH_ED=r"4\textsuperscript{e} éd.",
    BIB_KAPPEL_IN="Dans",
    BIB_C_BRESENHAM=r"article original de l'algorithme du point médian entier traité au §5.",
    BIB_C_PITTEWAY=r"généralisation de l'algorithme de Bresenham aux coniques arbitraires, base de l'extension aux ellipses décrite au §5.",
    BIB_C_KAPPEL=r"formulation à deux régions utilisée dans l'implémentation des ellipses.",
    BIB_C_KLETTE=r"référence standard pour la topologie numérique, opérateurs de bord ($\partial F$), 4-/6-/26-connexité. Utilisée aux §7, §12 et §18.",
    BIB_C_FOLEY=r"traitement classique de la rastérisation, des modèles d'éclairage, de la projection en perspective. Pertinent pour les §13--15.",
    BIB_C_SPONGE=r"format de fichier \code{.schem} (gzip + NBT) exporté par Block Round. Chargeable par WorldEdit, Litematica et MCEdit.",
    BIB_C_WORLDEDIT=r"référence officielle pour les commandes \cmd{//sphere}, \cmd{//hsphere}, \cmd{//ellipsoid}, \cmd{//cyl}, \cmd{//schem load} citées tout au long du document.",
    BIB_C_MCINVENTORY=r"référence sur les emplacements, piles, coffres simples (27 emplacements) et coffres doubles (54 emplacements) utilisés au §17.",
    BIB_C_MCCOMMANDS=r"commandes vanilla \cmd{/fill} et \cmd{/clone} citées aux §17 et §20.",
    BIB_C_LITEMATICA=r"mod de Minecraft Java Edition qui importe des schematics et affiche un fantôme translucide de la construction à exécuter.",
    BIB_LIMA_ENTRY=r"""\item \textbf{Audin, M.} \emph{Géométrie}. EDP Sciences, 2006.
        --- équation implicite de l'ellipse, algèbre des plans dans $\mathbb{R}^3$,
        coordonnées sphériques. Base du contenu des §3, §9 et §13.""",
    BIB_C_ARMSTRONG=r"exposition introductive au groupe octaédrique $O_h$ et à ses sous-groupes, utilisée au §20.",
    BIB_C_COXETER=r"référence canonique pour les groupes de symétrie des solides réguliers, incluant le traitement détaillé de $O_h$ d'ordre 48 mentionné au §20.",
    BIB_C_HILBERT=r"traitement classique des quadriques et de la visualisation géométrique, base intuitive du §9.",
    BIB_C_CORMEN=r"analyse de complexité des trois algorithmes des §4--6, division avec plafond du §17.",
    BIB_C_WIRTH=r"exposition classique de l'algorithme de Bresenham pour les droites et son extension aux circonférences.",
    BIB_ONLINE_APP="Block Round --- application",
    BIB_ONLINE_REPO="Block Round --- dépôt",
    BIB_ONLINE_PIXELROUND="Projet frère Pixel Round (variante sans textures Minecraft)",
    BIB_ONLINE_AULA=r"""Plan de cours en pt-BR (3\textsuperscript{e} année de lycée) :
        \biblink{https://vinisouza128.github.io/block-round/docs_aula/Plano_de_Aula_pt-BR.pdf}{docs\_aula/Plano\_de\_Aula\_pt-BR.pdf}.""",
)


# ----------------------------------------------------------------------------
# de-DE — Deutsch (Deutschland)
# ----------------------------------------------------------------------------
_FIG_TRANS["de-DE"] = dict(
    EUCL="Euklidisch",
    BRES="Bresenham",
    THR="Schwellenwert",
    FILLED="Gefüllt",
    THIN=r"Dünn (\emph{1 Voxel})",
    THICK="Dick",
    SPHERE_D10=r"Kugel $D=10$, $r_x=r_y=r_z=5$.",
    ELLIPSOID=r"Ellipsoid $W=20,\,H=10,\,D=12$.",
    CUT_Y=r"$Y$-Schnitt 50\% (Kuppel)",
    CUT_X=r"$X$-Schnitt 50\%",
    CUT_DIAG=r"Diagonal 50\%",
    SHADING_CLASSIC=r"(starker Kontrast)",
    SHADING_BLOCKS=r"(Standard)",
    SHADING_SMOOTH=r"(ähnliche Flächen)",
    OVERLAY_OFF=r"Overlay \emph{OFF}",
    OVERLAY_ON=r"Overlay \emph{ON} (Standard)",
    CAP_3ALG=r"Derselbe Kreis mit Durchmesser $D=10$ unter den drei Kriterien. Jede Abbildung zeigt die Menge der Zellen, die von der jeweiligen Version der Ungleichung $d_x^2+d_y^2\leq 1$ markiert werden, gerendert mit der Minecraft-Textur \emph{Cobblestone}. Man beachte, wie sich die Reihenübergänge, die Eckzellen und die Kardinalpunkte unterscheiden --- drei mathematisch korrekte Antworten unter verschiedenen Kriterien.",
    CAP_MODES=r"Die drei Renderingmodi für denselben euklidischen Kreis mit $D=20$. Der Modus \emph{Dünn} entspricht dem diskreten topologischen Rand ($\partial F$); der Modus \emph{Dick} fügt diagonale Blöcke hinzu, um $45^\circ$-Löcher zu schließen, was für wasserdichte Bauten (Unterwasserkuppeln aus Glas/Eis) unerlässlich ist.",
    CAP_3D=r"Voxelisierung im $\mathbb{R}^3$. Jeder Würfel ist ein Voxel; seine Mittelpunktskoordinate $(i,j,k)$ wird gegen die implizite Gleichung $a_x^2+a_y^2+a_z^2\leq 1$ geprüft. Die sichtbaren Treppenstufen auf der Oberfläche sind eine mathematische Folge der Diskretisierung --- genau die Eigenschaft, die Minecraft seine visuelle Identität verleiht.",
    CAP_CUTS=r"Drei Schnitte durch dieselbe Kugel $D=16$, jeder erhält 50\% des Volumens. Der $Y$-Schnitt erzeugt die klassische Kuppel $V_{\mathrm{Kuppel}}=\tfrac{2}{3}\pi r^3$; der diagonale Schnitt legt die Hypotenuse $x+y=k$ frei, die für diese Schnittebene charakteristisch ist.",
    CAP_SHADING=r"Drei Lichtmultiplikatoren, die auf dieselben drei sichtbaren Flächen angewendet werden. \emph{Classic} ergibt das kanonische Minecraft-Vanilla-Aussehen; \emph{Smooth} reduziert den Kontrast für glatte Oberflächen; \emph{Blocks} ist der mittlere Standard mit geometrischem Einsatz, der Voxelgrenzen auch dann sichtbar macht, wenn die Textur gleich ist.",
    CAP_OVERLAY=r"Dieselbe Voxelmenge mit und ohne schwarze Umrandung an den freiliegenden Kanten. Bei aktiviertem \emph{Highlight-Overlay} erzeugt ein fehlender Block in der Schale eine Diskontinuität im Muster, die das Auge sofort erkennt --- ein schnelles Validierungswerkzeug während des Bauens im Survival-Modus.",
    CAP_OCTANTS=r"Kugel $D=10$ mit dem positiven Oktanten $(+x,+y,+z)$ grün hervorgehoben. Unter der Wirkung der Untergruppe $\mathbb{Z}_2^3 \leq O_h$ (Ordnung 8, erzeugt durch die drei Koordinatenspiegelungen) bestimmt dieser Oktant die gesamte Kugel --- die anderen sieben Bereiche werden durch eine Folge von \cmd{/clone}-Aufrufen mit \emph{mode:masked} aus dem manuell gebauten Oktanten gewonnen.",
    CAP_TEXTURES=r"Dieselbe Kugel mit Durchmesser $D=8$, gerendert mit drei verschiedenen Blöcken. Die voxelisierte Silhouette (Mathematik) ist in allen drei Fällen identisch: Der Algorithmus wählt die Voxel aus, die Textur ist eine rein ästhetische Schicht, die nachträglich aufgebracht wird und weder Volumen noch Topologie verändert.",
    BIB_TITLE="Literaturverzeichnis",
    BIB_SUB1="Technische Referenzen (Rasterisierung und digitale Topologie)",
    BIB_SUB2="Referenzierte Minecraft-Spezifikationen und Werkzeuge",
    BIB_SUB3="Geometrie, lineare Algebra und Gruppentheorie",
    BIB_SUB4="Algorithmen, Datenstrukturen, Komplexität",
    BIB_SUB5="Ergänzende Online-Ressourcen",
    BIB_AVAILABLE_AT="Verfügbar unter",
    BIB_PAGES="Seiten",
    BIB_3RD_ED="3. Aufl.",
    BIB_4TH_ED="4. Aufl.",
    BIB_KAPPEL_IN="In",
    BIB_C_BRESENHAM=r"Originalartikel des ganzzahligen Mittelpunkt-Algorithmus, behandelt in §5.",
    BIB_C_PITTEWAY=r"Verallgemeinerung des Bresenham-Algorithmus auf beliebige Kegelschnitte, Grundlage der in §5 beschriebenen Ellipsenerweiterung.",
    BIB_C_KAPPEL=r"Zwei-Regionen-Formulierung, die in der Ellipsenimplementierung verwendet wird.",
    BIB_C_KLETTE=r"Standardreferenz für digitale Topologie, Randoperatoren ($\partial F$), 4-/6-/26-Nachbarschaft. Verwendet in §7, §12 und §18.",
    BIB_C_FOLEY=r"Klassische Behandlung von Rasterisierung, Beleuchtungsmodellen und perspektivischer Projektion. Relevant für §13--15.",
    BIB_C_SPONGE=r"Dateiformat \code{.schem} (gzip + NBT), das Block Round exportiert. Ladbar mit WorldEdit, Litematica und MCEdit.",
    BIB_C_WORLDEDIT=r"Offizielle Referenz für die Befehle \cmd{//sphere}, \cmd{//hsphere}, \cmd{//ellipsoid}, \cmd{//cyl}, \cmd{//schem load}, die in diesem Dokument zitiert werden.",
    BIB_C_MCINVENTORY=r"Referenz zu Slots, Stacks, einfachen Truhen (27 Slots) und Doppeltruhen (54 Slots), verwendet in §17.",
    BIB_C_MCCOMMANDS=r"Vanilla-Befehle \cmd{/fill} und \cmd{/clone}, zitiert in §17 und §20.",
    BIB_C_LITEMATICA=r"Minecraft-Java-Edition-Mod, der Schematics importiert und einen durchscheinenden Geist des auszuführenden Bauwerks anzeigt.",
    BIB_LIMA_ENTRY=r"""\item \textbf{Fischer, G.} \emph{Analytische Geometrie}. Vieweg, 1985.
        --- implizite Gleichung der Ellipse, Algebra von Ebenen im $\mathbb{R}^3$,
        Kugelkoordinaten. Basis für den Inhalt von §3, §9 und §13.""",
    BIB_C_ARMSTRONG=r"einführende Darstellung der oktaedrischen Gruppe $O_h$ und ihrer Untergruppen, verwendet in §20.",
    BIB_C_COXETER=r"kanonische Referenz für die Symmetriegruppen regulärer Körper, einschließlich der detaillierten Behandlung von $O_h$ der Ordnung 48, die in §20 erwähnt wird.",
    BIB_C_HILBERT=r"klassische Behandlung von Quadriken und geometrischer Visualisierung, intuitive Grundlage für §9.",
    BIB_C_CORMEN=r"Komplexitätsanalyse der drei Algorithmen aus §4--6, Aufrundungsdivision aus §17.",
    BIB_C_WIRTH=r"klassische Darstellung des Bresenham-Algorithmus für Geraden und seiner Erweiterung auf Kreise.",
    BIB_ONLINE_APP="Block Round --- Anwendung",
    BIB_ONLINE_REPO="Block Round --- Repository",
    BIB_ONLINE_PIXELROUND="Schwesterprojekt Pixel Round (Variante ohne Minecraft-Texturen)",
    BIB_ONLINE_AULA=r"""Unterrichtsplan auf pt-BR (3. Jahr der Sekundarstufe):
        \biblink{https://vinisouza128.github.io/block-round/docs_aula/Plano_de_Aula_pt-BR.pdf}{docs\_aula/Plano\_de\_Aula\_pt-BR.pdf}.""",
)


# ----------------------------------------------------------------------------
# zh-CN — 简体中文
# ----------------------------------------------------------------------------
_FIG_TRANS["zh-CN"] = dict(
    EUCL="欧几里得",
    BRES="Bresenham",
    THR="阈值",
    FILLED="填充",
    THIN=r"细 (\emph{1 体素})",
    THICK="粗",
    SPHERE_D10=r"球体 $D=10$, $r_x=r_y=r_z=5$.",
    ELLIPSOID=r"椭球体 $W=20,\,H=10,\,D=12$.",
    CUT_Y=r"$Y$ 切 50\%(穹顶)",
    CUT_X=r"$X$ 切 50\%",
    CUT_DIAG=r"对角 50\%",
    SHADING_CLASSIC=r"(强对比)",
    SHADING_BLOCKS=r"(默认)",
    SHADING_SMOOTH=r"(面相近)",
    OVERLAY_OFF=r"叠加 \emph{OFF}",
    OVERLAY_ON=r"叠加 \emph{ON}(默认)",
    CAP_3ALG=r"在三种判定下直径 $D=10$ 的同一圆周。每幅图显示对应版本的不等式 $d_x^2+d_y^2\leq 1$ 所标记的单元集合,使用 Minecraft 的 \emph{cobblestone} 材质渲染。注意行间过渡、角点单元和基本方位的差异——三种在不同判定下都数学正确的答案。",
    CAP_MODES=r"同一 $D=20$ 欧几里得圆周的三种渲染模式。\emph{细}模式对应离散拓扑边界 ($\partial F$);\emph{粗}模式增加对角块以封闭 $45^\circ$ 的孔洞,这对密封构造(水下玻璃/冰穹顶)至关重要。",
    CAP_3D=r"$\mathbb{R}^3$ 中的体素化。每个立方体是一个体素;以其中心坐标 $(i,j,k)$ 代入隐式方程 $a_x^2+a_y^2+a_z^2\leq 1$ 进行检验。表面上可见的阶梯是离散化的数学必然结果——正是赋予 Minecraft 视觉标识的特性。",
    CAP_CUTS=r"对同一 $D=16$ 球体的三种切法,均保留 50\% 体积。$Y$ 切产生经典穹顶 $V_{\mathrm{穹顶}}=\tfrac{2}{3}\pi r^3$;对角切暴露出该切割平面特有的斜边 $x+y=k$。",
    CAP_SHADING=r"对同样三个可见面应用三种光照倍数。\emph{Classic} 给出标志性的 Minecraft 原版外观;\emph{Smooth} 降低对比度以呈现平滑表面;\emph{Blocks} 为中间默认值,其几何内嵌即使在材质相同时也能显露体素边界。",
    CAP_OVERLAY=r"同一体素集合在外露棱上有/无黑色轮廓的对比。开启 \emph{highlight overlay} 时,外壳上缺失的方块会产生肉眼一瞥即可察觉的图案不连续——生存建造中的快速验证工具。",
    CAP_OCTANTS=r"$D=10$ 球体,正八分卦象 $(+x,+y,+z)$ 以绿色高亮。在子群 $\mathbb{Z}_2^3 \leq O_h$(阶 8,由三个坐标反射生成)的作用下,该八分卦象决定整个球——其余七个区域通过对手工构建的八分卦象施加一系列带 \emph{mode:masked} 的 \cmd{/clone} 调用得到。",
    CAP_TEXTURES=r"同一 $D=8$ 球体使用三种不同方块渲染。体素化轮廓(数学)在三者中完全相同:算法选定体素;材质是事后施加的纯粹美学层,既不改变体积也不改变拓扑。",
    BIB_TITLE="参考文献",
    BIB_SUB1="技术参考(光栅化与数字拓扑)",
    BIB_SUB2="所引用的 Minecraft 规范与工具",
    BIB_SUB3="几何、线性代数与群论",
    BIB_SUB4="算法、数据结构、复杂度",
    BIB_SUB5="补充在线资源",
    BIB_AVAILABLE_AT="可获取于",
    BIB_PAGES="页",
    BIB_3RD_ED="第3版",
    BIB_4TH_ED="第4版",
    BIB_KAPPEL_IN="收录于",
    BIB_C_BRESENHAM=r"本文档第 §5 节所讨论的整数中点算法的原始论文。",
    BIB_C_PITTEWAY=r"将 Bresenham 算法推广至任意圆锥曲线,是第 §5 节中椭圆扩展的基础。",
    BIB_C_KAPPEL=r"椭圆实现中所采用的两区域公式。",
    BIB_C_KLETTE=r"数字拓扑、边界算子 ($\partial F$)、4-/6-/26-连通性的标准参考。用于 §7、§12 和 §18。",
    BIB_C_FOLEY=r"光栅化、光照模型、透视投影的经典论述。与 §13--15 相关。",
    BIB_C_SPONGE=r"Block Round 导出的 \code{.schem} 文件格式(gzip + NBT)。可由 WorldEdit、Litematica 和 MCEdit 加载。",
    BIB_C_WORLDEDIT=r"全文中引用的 \cmd{//sphere}、\cmd{//hsphere}、\cmd{//ellipsoid}、\cmd{//cyl}、\cmd{//schem load} 命令的官方参考。",
    BIB_C_MCINVENTORY=r"§17 中所用关于槽位、堆叠、单箱(27 槽)和双箱(54 槽)的参考资料。",
    BIB_C_MCCOMMANDS=r"§17 与 §20 中引用的原版命令 \cmd{/fill} 与 \cmd{/clone}。",
    BIB_C_LITEMATICA=r"导入示意图并以半透明幽灵显示待施工建筑的 Minecraft Java 版模组。",
    BIB_LIMA_ENTRY=r"""\item \textbf{王萼芳, 石生明 (编)} \emph{高等代数}. 高等教育出版社, 北京, 2003.
        --- 椭圆的隐式方程、$\mathbb{R}^3$ 中的平面代数、球坐标。
        §3、§9 与 §13 内容的基础。""",
    BIB_C_ARMSTRONG=r"八面体群 $O_h$ 及其子群的入门论述,用于 §20。",
    BIB_C_COXETER=r"正多面体对称群的经典参考,包含 §20 中提及的 48 阶 $O_h$ 的详细处理。",
    BIB_C_HILBERT=r"二次曲面与几何可视化的经典论述,§9 的直观基础。",
    BIB_C_CORMEN=r"§4--6 三种算法的复杂度分析,§17 的向上取整除法。",
    BIB_C_WIRTH=r"Bresenham 直线算法及其向圆周推广的经典论述。",
    BIB_ONLINE_APP="Block Round --- 应用程序",
    BIB_ONLINE_REPO="Block Round --- 代码仓库",
    BIB_ONLINE_PIXELROUND="姊妹项目 Pixel Round(无 Minecraft 材质版本)",
    BIB_ONLINE_AULA=r"""pt-BR 教案(高中3年级):
        \biblink{https://vinisouza128.github.io/block-round/docs_aula/Plano_de_Aula_pt-BR.pdf}{docs\_aula/Plano\_de\_Aula\_pt-BR.pdf}.""",
)


# ----------------------------------------------------------------------------
# ja-JP — 日本語
# ----------------------------------------------------------------------------
_FIG_TRANS["ja-JP"] = dict(
    EUCL="ユークリッド",
    BRES="Bresenham",
    THR="しきい値",
    FILLED="塗りつぶし",
    THIN=r"細 (\emph{1 ボクセル})",
    THICK="太",
    SPHERE_D10=r"球 $D=10$, $r_x=r_y=r_z=5$.",
    ELLIPSOID=r"楕円体 $W=20,\,H=10,\,D=12$.",
    CUT_Y=r"$Y$ カット 50\%(ドーム)",
    CUT_X=r"$X$ カット 50\%",
    CUT_DIAG=r"対角 50\%",
    SHADING_CLASSIC=r"(強コントラスト)",
    SHADING_BLOCKS=r"(デフォルト)",
    SHADING_SMOOTH=r"(面が近似)",
    OVERLAY_OFF=r"オーバーレイ \emph{OFF}",
    OVERLAY_ON=r"オーバーレイ \emph{ON}(デフォルト)",
    CAP_3ALG=r"3 つの基準による直径 $D=10$ の同一円周。各図は対応する不等式 $d_x^2+d_y^2\leq 1$ により選ばれたセル集合を示し,Minecraft の \emph{cobblestone} テクスチャで描画されている。行間の遷移,角セル,基本方位の違いに注目——いずれも異なる基準のもとで数学的に正しい 3 つの答えである。",
    CAP_MODES=r"同一の $D=20$ ユークリッド円周に対する 3 つの描画モード。\emph{細}モードは離散位相境界 ($\partial F$) に対応し,\emph{太}モードは $45^\circ$ の穴を塞ぐ対角ブロックを追加する——水中のガラス/氷ドームなど密閉構造には必須である。",
    CAP_3D=r"$\mathbb{R}^3$ におけるボクセル化。各立方体が 1 ボクセルで,その中心座標 $(i,j,k)$ を陰関数 $a_x^2+a_y^2+a_z^2\leq 1$ に代入して判定する。表面に見える階段状は離散化の数学的帰結である——まさに Minecraft に視覚的アイデンティティを与えている特性に他ならない。",
    CAP_CUTS=r"同一の $D=16$ 球に対する 3 通りの切断で,いずれも体積の 50\% を保持する。$Y$ 切断は古典的なドーム $V_{\mathrm{dome}}=\tfrac{2}{3}\pi r^3$ を与え,対角切断はその切断面に特徴的な斜辺 $x+y=k$ を露出させる。",
    CAP_SHADING=r"同じ 3 つの可視面に対する 3 種類の光乗数。\emph{Classic} は Minecraft バニラの定番外観,\emph{Smooth} は滑らかな表面のためにコントラストを下げ,\emph{Blocks} は同一テクスチャでもボクセル境界を浮き上がらせる幾何的インセットを伴う中間デフォルトである。",
    CAP_OVERLAY=r"露出辺の黒い輪郭の有無による同一ボクセル集合の対比。\emph{highlight overlay} を ON にすると,殻に欠けたブロックがあると一目でわかるパターンの不連続が生じる——サバイバル建築中の素早い検証手段である。",
    CAP_OCTANTS=r"$D=10$ の球で,正の八分象限 $(+x,+y,+z)$ を緑で強調表示。部分群 $\mathbb{Z}_2^3 \leq O_h$(位数 8,3 つの座標反射で生成)の作用のもと,この八分象限が球全体を決定する——他の 7 領域は手作業で構築した八分象限に対し \emph{mode:masked} 付きの \cmd{/clone} を順に適用して得られる。",
    CAP_TEXTURES=r"同一の $D=8$ 球を 3 種類の異なるブロックで描画。ボクセル化されたシルエット(数学)は 3 つとも同一であり,アルゴリズムがボクセルを選び,テクスチャは体積も位相も変えない後付けの純粋に美的なレイヤーに過ぎない。",
    BIB_TITLE="参考文献",
    BIB_SUB1="技術文献(ラスタライズと離散位相)",
    BIB_SUB2="参照した Minecraft の仕様とツール",
    BIB_SUB3="幾何学,線形代数,群論",
    BIB_SUB4="アルゴリズム,データ構造,計算量",
    BIB_SUB5="補足オンライン資料",
    BIB_AVAILABLE_AT="入手先",
    BIB_PAGES="ページ",
    BIB_3RD_ED="第3版",
    BIB_4TH_ED="第4版",
    BIB_KAPPEL_IN="所収",
    BIB_C_BRESENHAM=r"本書 §5 で扱う整数ミッドポイント・アルゴリズムの原論文。",
    BIB_C_PITTEWAY=r"Bresenham アルゴリズムの任意の円錐曲線への一般化で,§5 で述べる楕円拡張の基礎。",
    BIB_C_KAPPEL=r"楕円実装で用いる二領域定式化。",
    BIB_C_KLETTE=r"離散位相,境界作用素 ($\partial F$),4-/6-/26-連結性の標準参考。§7,§12,§18 で使用。",
    BIB_C_FOLEY=r"ラスタライズ,照明モデル,透視投影の古典的論述。§13--15 に関連。",
    BIB_C_SPONGE=r"Block Round が出力する \code{.schem} 形式(gzip + NBT)。WorldEdit,Litematica,MCEdit で読み込み可能。",
    BIB_C_WORLDEDIT=r"本書全体で引用される \cmd{//sphere},\cmd{//hsphere},\cmd{//ellipsoid},\cmd{//cyl},\cmd{//schem load} コマンドの公式リファレンス。",
    BIB_C_MCINVENTORY=r"§17 で用いるスロット,スタック,単一チェスト(27 スロット)および二連チェスト(54 スロット)の参考。",
    BIB_C_MCCOMMANDS=r"§17 および §20 で引用するバニラコマンド \cmd{/fill} と \cmd{/clone}。",
    BIB_C_LITEMATICA=r"スキーマティックを読み込み,施工対象の半透明なゴーストを表示する Minecraft Java Edition の mod。",
    BIB_LIMA_ENTRY=r"""\item \textbf{齋藤正彦} \emph{線型代数入門}. 東京大学出版会, 1966.
        --- 楕円の陰関数表示,$\mathbb{R}^3$ における平面の代数,
        球面座標。§3,§9,§13 の内容の基礎。""",
    BIB_C_ARMSTRONG=r"八面体群 $O_h$ とその部分群の入門的解説,§20 で使用。",
    BIB_C_COXETER=r"正多面体の対称群の標準的参考。§20 で言及される位数 48 の $O_h$ の詳細な扱いを含む。",
    BIB_C_HILBERT=r"二次曲面と幾何学的可視化の古典的論述,§9 の直観的基礎。",
    BIB_C_CORMEN=r"§4--6 の 3 アルゴリズムの計算量解析と,§17 の天井除算。",
    BIB_C_WIRTH=r"Bresenham の直線アルゴリズムとその円周への拡張についての古典的論述。",
    BIB_ONLINE_APP="Block Round --- アプリ",
    BIB_ONLINE_REPO="Block Round --- リポジトリ",
    BIB_ONLINE_PIXELROUND="姉妹プロジェクト Pixel Round(Minecraft テクスチャ非使用版)",
    BIB_ONLINE_AULA=r"""pt-BR の指導案(高校3年生):
        \biblink{https://vinisouza128.github.io/block-round/docs_aula/Plano_de_Aula_pt-BR.pdf}{docs\_aula/Plano\_de\_Aula\_pt-BR.pdf}.""",
)


# ----------------------------------------------------------------------------
# ru-RU — Русский
# ----------------------------------------------------------------------------
_FIG_TRANS["ru-RU"] = dict(
    EUCL="Евклидово",
    BRES="Брезенхэм",
    THR="Пороговое",
    FILLED="Заполненный",
    THIN=r"Тонкий (\emph{1 воксель})",
    THICK="Толстый",
    SPHERE_D10=r"Сфера $D=10$, $r_x=r_y=r_z=5$.",
    ELLIPSOID=r"Эллипсоид $W=20,\,H=10,\,D=12$.",
    CUT_Y=r"Сечение $Y$ 50\% (купол)",
    CUT_X=r"Сечение $X$ 50\%",
    CUT_DIAG=r"Диагональ 50\%",
    SHADING_CLASSIC=r"(сильный контраст)",
    SHADING_BLOCKS=r"(по умолчанию)",
    SHADING_SMOOTH=r"(схожие грани)",
    OVERLAY_OFF=r"Overlay \emph{OFF}",
    OVERLAY_ON=r"Overlay \emph{ON} (по умолчанию)",
    CAP_3ALG=r"Одна и та же окружность диаметра $D=10$ при трёх различных критериях. Каждая фигура --- это множество клеток, помеченных соответствующей версией неравенства $d_x^2+d_y^2\leq 1$, отрендеренное текстурой \emph{cobblestone} из Minecraft. Обратите внимание на различия в переходах между рядами, угловых клетках и кардинальных точках --- три математически верных ответа при разных критериях.",
    CAP_MODES=r"Три режима рендеринга для одной и той же евклидовой окружности $D=20$. Режим \emph{Тонкий} соответствует дискретной топологической границе ($\partial F$); режим \emph{Толстый} добавляет диагональные блоки для закрытия отверстий под $45^\circ$, что необходимо для герметичных построек (подводные купола из Стекла/Льда).",
    CAP_3D=r"Воксельизация в $\mathbb{R}^3$. Каждый куб --- это воксель; координаты его центра $(i,j,k)$ проверяются по неявному уравнению $a_x^2+a_y^2+a_z^2\leq 1$. Видимые ступеньки на поверхности --- математическое следствие дискретизации, именно та особенность, которая придаёт Minecraft его визуальную идентичность.",
    CAP_CUTS=r"Три сечения одной и той же сферы $D=16$, каждое сохраняет 50\% объёма. Сечение $Y$ даёт классический купол $V_{\mathrm{купол}}=\tfrac{2}{3}\pi r^3$; диагональ обнажает гипотенузу $x+y=k$, характерную для этой секущей плоскости.",
    CAP_SHADING=r"Три множителя освещения, применяемые к одним и тем же трём видимым граням. \emph{Classic} даёт канонический ванильный вид Minecraft; \emph{Smooth} снижает контраст для гладких поверхностей; \emph{Blocks} --- промежуточный вариант по умолчанию с геометрическим отступом, выявляющим границы вокселей даже при одинаковой текстуре.",
    CAP_OVERLAY=r"То же множество вокселей с чёрной обводкой открытых рёбер и без неё. С включённым \emph{highlight overlay} отсутствующий блок в оболочке создаёт разрыв узора, который глаз замечает мгновенно --- инструмент быстрой проверки во время строительства в режиме выживания.",
    CAP_OCTANTS=r"Сфера $D=10$ с положительным октантом $(+x,+y,+z)$, выделенным зелёным. При действии подгруппы $\mathbb{Z}_2^3 \leq O_h$ (порядка 8, порождённой тремя координатными отражениями) этот октант определяет всю сферу --- остальные семь областей получаются последовательностью \cmd{/clone} с \emph{mode:masked}, применённой к октанту, построенному вручную.",
    CAP_TEXTURES=r"Одна и та же сфера диаметра $D=8$, отрендеренная с тремя различными блоками. Воксельный силуэт (математика) идентичен во всех трёх случаях: алгоритм выбирает воксели, а текстура --- это чисто эстетический слой, наносимый позже и не меняющий ни объём, ни топологию.",
    BIB_TITLE="Библиография",
    BIB_SUB1="Технические работы (растеризация и цифровая топология)",
    BIB_SUB2="Спецификации и инструменты Minecraft",
    BIB_SUB3="Геометрия, линейная алгебра и теория групп",
    BIB_SUB4="Алгоритмы, структуры данных, сложность",
    BIB_SUB5="Дополнительные онлайн-ресурсы",
    BIB_AVAILABLE_AT="Доступно по адресу",
    BIB_PAGES="с.",
    BIB_3RD_ED="3-е изд.",
    BIB_4TH_ED="4-е изд.",
    BIB_KAPPEL_IN="В сб.",
    BIB_C_BRESENHAM=r"оригинальная статья о целочисленном алгоритме средней точки, рассматриваемом в §5 данного документа.",
    BIB_C_PITTEWAY=r"обобщение алгоритма Брезенхэма на произвольные конические сечения, основа расширения для эллипсов, описанного в §5.",
    BIB_C_KAPPEL=r"двухобластная формулировка, используемая в реализации эллипсов.",
    BIB_C_KLETTE=r"стандартная работа по цифровой топологии, операторам границы ($\partial F$), 4-/6-/26-связности. Используется в §7, §12 и §18.",
    BIB_C_FOLEY=r"классическое изложение растеризации, моделей освещения, перспективной проекции. Актуально для §13--15.",
    BIB_C_SPONGE=r"формат файла \code{.schem} (gzip + NBT), который экспортирует Block Round. Загружается через WorldEdit, Litematica и MCEdit.",
    BIB_C_WORLDEDIT=r"официальная документация по командам \cmd{//sphere}, \cmd{//hsphere}, \cmd{//ellipsoid}, \cmd{//cyl}, \cmd{//schem load}, упоминаемым в документе.",
    BIB_C_MCINVENTORY=r"справка по слотам, стакам, обычным сундукам (27 слотов) и двойным сундукам (54 слота), используется в §17.",
    BIB_C_MCCOMMANDS=r"ванильные команды \cmd{/fill} и \cmd{/clone}, упоминаемые в §17 и §20.",
    BIB_C_LITEMATICA=r"мод для Minecraft Java Edition, импортирующий схемы и показывающий полупрозрачный призрак постройки.",
    BIB_LIMA_ENTRY=r"""\item \textbf{Кострикин А.~И., Манин Ю.~И.} \emph{Линейная алгебра и геометрия}.
        Наука, 1986.
        --- неявное уравнение эллипса, алгебра плоскостей в $\mathbb{R}^3$,
        сферические координаты. Основа содержания §3, §9 и §13.""",
    BIB_C_ARMSTRONG=r"вводное изложение октаэдрической группы $O_h$ и её подгрупп, используется в §20.",
    BIB_C_COXETER=r"каноническая работа по группам симметрии правильных многогранников, включая детальное рассмотрение $O_h$ порядка 48, упомянутого в §20.",
    BIB_C_HILBERT=r"классическое изложение квадрик и геометрической визуализации, интуитивная основа §9.",
    BIB_C_CORMEN=r"анализ сложности трёх алгоритмов §4--6, деление с округлением вверх в §17.",
    BIB_C_WIRTH=r"классическое изложение алгоритма Брезенхэма для прямых и его расширения на окружности.",
    BIB_ONLINE_APP="Block Round --- приложение",
    BIB_ONLINE_REPO="Block Round --- репозиторий",
    BIB_ONLINE_PIXELROUND="Родственный проект Pixel Round (вариант без текстур Minecraft)",
    BIB_ONLINE_AULA=r"""План урока на pt-BR (3-й год средней школы):
        \biblink{https://vinisouza128.github.io/block-round/docs_aula/Plano_de_Aula_pt-BR.pdf}{docs\_aula/Plano\_de\_Aula\_pt-BR.pdf}.""",
)


# ----------------------------------------------------------------------------
# ko-KR — 한국어
# ----------------------------------------------------------------------------
_FIG_TRANS["ko-KR"] = dict(
    EUCL="유클리드",
    BRES="Bresenham",
    THR="임계",
    FILLED="채움",
    THIN=r"가는 (\emph{1 복셀})",
    THICK="굵은",
    SPHERE_D10=r"구 $D=10$, $r_x=r_y=r_z=5$.",
    ELLIPSOID=r"타원체 $W=20,\,H=10,\,D=12$.",
    CUT_Y=r"$Y$ 절단 50\%(돔)",
    CUT_X=r"$X$ 절단 50\%",
    CUT_DIAG=r"대각 50\%",
    SHADING_CLASSIC=r"(강한 대비)",
    SHADING_BLOCKS=r"(기본)",
    SHADING_SMOOTH=r"(면이 유사)",
    OVERLAY_OFF=r"오버레이 \emph{OFF}",
    OVERLAY_ON=r"오버레이 \emph{ON}(기본)",
    CAP_3ALG=r"세 가지 기준에서의 직경 $D=10$ 인 동일한 원주. 각 그림은 대응되는 부등식 $d_x^2+d_y^2\leq 1$ 에 의해 표시되는 셀 집합을 보여주며, Minecraft 의 \emph{cobblestone} 텍스처로 렌더링되어 있다. 행 사이의 전이, 모서리 셀, 기본 방위가 어떻게 달라지는지 주목하라 --- 서로 다른 기준 아래에서 수학적으로 모두 옳은 세 가지 답이다.",
    CAP_MODES=r"동일한 $D=20$ 유클리드 원주에 대한 세 가지 렌더링 모드. \emph{가는} 모드는 이산 위상 경계 ($\partial F$) 에 대응하고, \emph{굵은} 모드는 $45^\circ$ 의 구멍을 막기 위해 대각 블록을 추가하는데, 이는 밀폐 구조(수중 유리/얼음 돔)에 필수적이다.",
    CAP_3D=r"$\mathbb{R}^3$ 에서의 복셀화. 각 정육면체가 하나의 복셀이며, 그 중심 좌표 $(i,j,k)$ 를 음함수 방정식 $a_x^2+a_y^2+a_z^2\leq 1$ 에 대입해 판정한다. 표면에 보이는 계단 모양은 이산화의 수학적 귀결이며 --- 바로 Minecraft 에 시각적 정체성을 부여하는 그 특성이다.",
    CAP_CUTS=r"동일한 $D=16$ 구에 대한 세 가지 절단으로, 모두 부피의 50\% 를 보존한다. $Y$ 절단은 고전적인 돔 $V_{\mathrm{dome}}=\tfrac{2}{3}\pi r^3$ 을 만들고, 대각 절단은 그 절단면 특유의 빗변 $x+y=k$ 를 드러낸다.",
    CAP_SHADING=r"같은 세 개의 가시면에 적용된 세 가지 빛 배율. \emph{Classic} 은 표준적인 Minecraft 바닐라 외관을 주며, \emph{Smooth} 는 매끈한 표면을 위해 대비를 낮추고, \emph{Blocks} 는 텍스처가 같아도 복셀 경계를 드러내는 기하학적 인셋이 있는 중간 기본값이다.",
    CAP_OVERLAY=r"노출된 모서리의 검은 윤곽선 유무에 따른 동일한 복셀 집합의 비교. \emph{highlight overlay} 가 ON 이면 껍데기에 빠진 블록이 한눈에 알아챌 수 있는 패턴 불연속을 만든다 --- 서바이벌 건축 중의 빠른 검증 도구.",
    CAP_OCTANTS=r"$D=10$ 구에서 양의 팔분공간 $(+x,+y,+z)$ 을 초록으로 강조 표시. 부분군 $\mathbb{Z}_2^3 \leq O_h$(위수 8, 세 좌표 반사로 생성됨)의 작용 아래 이 팔분공간이 구 전체를 결정한다 --- 나머지 일곱 영역은 수작업으로 만든 팔분공간에 \emph{mode:masked} 옵션을 준 \cmd{/clone} 호출을 차례로 적용해 얻는다.",
    CAP_TEXTURES=r"동일한 $D=8$ 구를 세 가지 다른 블록으로 렌더링한 결과. 복셀화된 실루엣(수학)은 세 경우에 모두 동일하다: 알고리즘이 복셀을 선택하고, 텍스처는 이후에 적용되는 순전히 미적인 층으로서 부피도 위상도 바꾸지 않는다.",
    BIB_TITLE="참고문헌",
    BIB_SUB1="기술 참고문헌(래스터화 및 디지털 위상수학)",
    BIB_SUB2="참조한 Minecraft 사양 및 도구",
    BIB_SUB3="기하학, 선형대수, 군론",
    BIB_SUB4="알고리즘, 자료구조, 복잡도",
    BIB_SUB5="보조 온라인 자료",
    BIB_AVAILABLE_AT="이용 가능한 곳",
    BIB_PAGES="쪽",
    BIB_3RD_ED="제3판",
    BIB_4TH_ED="제4판",
    BIB_KAPPEL_IN="수록",
    BIB_C_BRESENHAM=r"본 문서의 §5 에서 다루는 정수 중점 알고리즘의 원논문.",
    BIB_C_PITTEWAY=r"Bresenham 알고리즘을 임의의 원뿔곡선으로 일반화한 것으로, §5 에서 설명한 타원 확장의 기초.",
    BIB_C_KAPPEL=r"타원 구현에서 사용한 두 영역 정식화.",
    BIB_C_KLETTE=r"디지털 위상수학, 경계 작용소 ($\partial F$), 4-/6-/26-연결성의 표준 참고문헌. §7, §12, §18 에서 사용.",
    BIB_C_FOLEY=r"래스터화, 조명 모델, 원근 투영의 고전적 논의. §13--15 와 관련.",
    BIB_C_SPONGE=r"Block Round 가 내보내는 \code{.schem} 파일 형식(gzip + NBT). WorldEdit, Litematica, MCEdit 으로 불러올 수 있다.",
    BIB_C_WORLDEDIT=r"본 문서 전반에서 인용되는 \cmd{//sphere}, \cmd{//hsphere}, \cmd{//ellipsoid}, \cmd{//cyl}, \cmd{//schem load} 명령에 대한 공식 참고문헌.",
    BIB_C_MCINVENTORY=r"§17 에서 사용되는 슬롯, 스택, 단일 상자(27 슬롯) 및 더블 상자(54 슬롯)에 대한 참고자료.",
    BIB_C_MCCOMMANDS=r"§17 과 §20 에서 인용되는 바닐라 명령 \cmd{/fill} 과 \cmd{/clone}.",
    BIB_C_LITEMATICA=r"스키매틱을 불러와 시공할 건축물의 반투명 고스트를 표시하는 Minecraft Java Edition 모드.",
    BIB_LIMA_ENTRY=r"""\item \textbf{김홍중} \emph{선형대수와 그 응용}. 경문사, 2012.
        --- 타원의 음함수 방정식, $\mathbb{R}^3$ 에서의 평면 대수,
        구면 좌표. §3, §9, §13 내용의 기초.""",
    BIB_C_ARMSTRONG=r"팔면체군 $O_h$ 와 그 부분군에 대한 입문적 서술, §20 에서 사용.",
    BIB_C_COXETER=r"정다면체 대칭군의 표준 참고문헌으로, §20 에서 언급된 위수 48 의 $O_h$ 에 대한 자세한 처리를 포함.",
    BIB_C_HILBERT=r"이차곡면과 기하학적 시각화의 고전적 논의, §9 의 직관적 기초.",
    BIB_C_CORMEN=r"§4--6 의 세 알고리즘에 대한 복잡도 분석, §17 의 천장 나눗셈.",
    BIB_C_WIRTH=r"Bresenham 의 직선 알고리즘 및 그 원주로의 확장에 관한 고전적 서술.",
    BIB_ONLINE_APP="Block Round --- 앱",
    BIB_ONLINE_REPO="Block Round --- 저장소",
    BIB_ONLINE_PIXELROUND="자매 프로젝트 Pixel Round(Minecraft 텍스처 없는 버전)",
    BIB_ONLINE_AULA=r"""pt-BR 수업 계획서(고등학교 3학년):
        \biblink{https://vinisouza128.github.io/block-round/docs_aula/Plano_de_Aula_pt-BR.pdf}{docs\_aula/Plano\_de\_Aula\_pt-BR.pdf}.""",
)


# ============================================================================
# COMPUTACAO FINAL
# ============================================================================
FIG_BLOCKS = {loc: _materialize(t) for loc, t in _FIG_TRANS.items()}
