# -*- coding: utf-8 -*-
"""Gerador multilingue dos PDFs "A Matemática do Projeto" do Block Round.

Compila um PDF por locale (en-US, es-ES, pt-BR, fr-FR, de-DE,
zh-CN, ja-JP, ru-RU, ko-KR) a partir de um único template XeLaTeX
+ tabela de traduções. Conteúdo recontextualizado para construção
em Minecraft (blocos, voxels com textura, /fill, /clone, WorldEdit,
inventário com packs de 64, baús, schematics).

Uso:    python build.py
Saída:  Block_Round_Math_<locale>.pdf  (mesmo diretório, >=25 páginas)
"""
import os, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
XELATEX = r"C:\Users\softk\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"

# ============================================================================
# TEMPLATE (chaves entre «...»)
# ============================================================================
TEX = r"""% !TEX program = xelatex
\documentclass[12pt,a4paper]{scrartcl}

«FONT_SETUP»

\usepackage{amsmath}
\usepackage{mathtools}

\usepackage[a4paper,top=2.8cm,bottom=2.8cm,left=2.6cm,right=2.6cm,
            headheight=16pt]{geometry}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{graphicx}
\usepackage{subcaption}
\usepackage{caption}
\usepackage{float}
\graphicspath{{img/}}
\usepackage{csquotes}
\usepackage{needspace}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\definecolor{accent}{HTML}{5B8E3F}
\definecolor{accentdark}{HTML}{406A2A}
\definecolor{earth}{HTML}{825432}
\definecolor{ink}{HTML}{1F1F23}
\definecolor{muted}{HTML}{4E4E58}
\definecolor{bg}{HTML}{FBF6E9}
\definecolor{rule}{HTML}{D8D1BC}
\definecolor{linkc}{HTML}{2D5A1F}

\usepackage[colorlinks=true,
            linkcolor=linkc,
            urlcolor=linkc,
            citecolor=linkc,
            bookmarks=true,bookmarksopen=true,
            pdftitle={Block Round — «PDF_TITLE»},
            pdfauthor={Vinícius Rodrigues de Souza}]{hyperref}

\color{ink}

\titleformat{\section}
  {\sffamily\Large\bfseries\color{accent}}{\thesection.}{0.6em}{}
\titleformat{\subsection}
  {\sffamily\large\bfseries\color{accent!85!ink}}{\thesubsection}{0.6em}{}
\titlespacing*{\section}{0pt}{1.2\baselineskip}{0.6\baselineskip}
\titlespacing*{\subsection}{0pt}{0.8\baselineskip}{0.3\baselineskip}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\sffamily\bfseries\color{accent}BLOCK ROUND}
\fancyhead[R]{\small\sffamily\color{muted}«HEAD_R»}
\fancyfoot[L]{\small\sffamily\color{muted}«FOOT_L»}
\fancyfoot[R]{\small\sffamily\color{muted}«PAGE_WORD» \thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}
\renewcommand{\headrule}{{\color{rule}\hrule height \headrulewidth}}
\renewcommand{\footrule}{{\color{rule}\vskip-\footrulewidth\hrule height \footrulewidth\vskip-\footrulewidth}}

\newtcolorbox{formula}{
  colback=bg, colframe=rule, boxrule=0.4pt, arc=2pt,
  left=10pt,right=10pt,top=8pt,bottom=8pt,
  before skip=8pt, after skip=8pt,
  fontupper=\color{accentdark}, breakable,
  before={\par\needspace{4\baselineskip}}
}

\newtcolorbox{minec}{
  colback=accent!7, colframe=accent!50!rule, boxrule=0.6pt, arc=2pt,
  left=10pt,right=10pt,top=8pt,bottom=8pt,
  before skip=10pt, after skip=10pt,
  breakable,
  before={\par\needspace{5\baselineskip}}
}

\setlength{\parskip}{0.75em}
\setlength{\parindent}{0pt}
\linespread{1.10}

\newcommand{\code}[1]{\texttt{\small #1}}
\newcommand{\acc}[1]{\textcolor{accent}{\textbf{#1}}}
\newcommand{\cmd}[1]{\textcolor{earth}{\texttt{\small #1}}}

\begin{document}

\begin{titlepage}
  \centering
  \vspace*{3.5cm}
  {\sffamily\bfseries\fontsize{56}{60}\selectfont \color{accent} Block Round\par}
  \vspace{0.7cm}
  {\sffamily\LARGE\color{muted} «COVER_SUBTITLE»\par}
  \vspace{1.4cm}
  {\color{rule}\rule{0.6\textwidth}{0.6pt}\par}
  \vspace{0.9cm}
  \begin{minipage}{0.82\textwidth}
    \centering\color{ink}\large
    «COVER_DESC»
  \end{minipage}
  \vspace{0.9cm}\\
  {\color{rule}\rule{0.6\textwidth}{0.6pt}\par}
  \vspace{2cm}
  \begin{minipage}{0.78\textwidth}
    \centering\sffamily\small\color{muted}
    \textbf{«COVER_AREAS_LABEL»} «COVER_AREAS_LIST»
  \end{minipage}
\end{titlepage}

\renewcommand{\contentsname}{\color{accent}«TOC_TITLE»}
\tableofcontents
\thispagestyle{fancy}
\newpage

% =============================================================================
\section{«S1_TITLE»}

«S1_P1»

«S1_P2»

«S1_P3_INTRO»
\begin{itemize}[leftmargin=1.3em,itemsep=0.15em,topsep=0.3em]
  \item «S1_AREA_1»;
  \item «S1_AREA_2»;
  \item «S1_AREA_3»;
  \item «S1_AREA_4»;
  \item «S1_AREA_5»;
  \item «S1_AREA_6»;
  \item «S1_AREA_7».
\end{itemize}

«S1_MC_NOTE»

% =============================================================================
\section{«S2_TITLE»}

«S2_P1»

\begin{formula}
\centering
$\displaystyle \text{«S2_CENTER_LABEL»}\;=\;\bigl(i+\tfrac{1}{2},\;\; j+\tfrac{1}{2}\bigr)$
\end{formula}

«S2_P2»

\begin{minec}
\textbf{«S2_MC_LABEL»} «S2_MC_EXAMPLE»
\end{minec}

% =============================================================================
\section{«S3_TITLE»}

«S3_P1»

\begin{formula}
\centering
$\displaystyle \left(\dfrac{x}{r_x}\right)^{\!2} + \left(\dfrac{y}{r_y}\right)^{\!2} \;=\; 1$
\end{formula}

«S3_P2»

«S3_P3»

\begin{formula}
\centering
$\displaystyle d_x = \dfrac{i+\tfrac{1}{2}-c_x}{r_x},\qquad
                d_y = \dfrac{j+\tfrac{1}{2}-c_y}{r_y},\qquad
                \text{«S3_INSIDE»}\;\Longleftrightarrow\; d_x^2 + d_y^2 \leq 1$
\end{formula}

\begin{minec}
\textbf{«S3_MC_LABEL»} «S3_MC_EXAMPLE»
\end{minec}

«FIG_3ALG»

% =============================================================================
\section{«S4_TITLE»}

\textbf{«S4_IDEA_LABEL»} «S4_P1»

\begin{formula}
\centering
$\displaystyle x \;=\; c_x \;\pm\; r_x\,\sqrt{\,1 - \left(\dfrac{y-c_y}{r_y}\right)^{\!2}\,}$
\end{formula}

«S4_P2»

\begin{formula}
\centering
$\displaystyle \mathit{dxM} \;=\; r_x\,\sqrt{\,1 - \dfrac{d_y^{\,2}}{r_y^{\,2}}\,}$
\end{formula}

«S4_P3»

\begin{formula}
\centering
$\displaystyle \mathit{lo} = \lceil c_x - \mathit{dxM} - \tfrac{1}{2} \rceil,
                \qquad
                \mathit{hi} = \lfloor c_x + \mathit{dxM} - \tfrac{1}{2} \rfloor$
\end{formula}

\textbf{«S4_JUST_LABEL»} «S4_P4»

\begin{minec}
\textbf{«S4_MC_LABEL»} «S4_MC_EXAMPLE»
\end{minec}

% =============================================================================
\section{«S5_TITLE»}

«S5_P1»

\subsection{«S5_SUB1»}

«S5_P2»
\[
d_0 \;=\; 1 - R
\]

«S5_P3»
\[
\begin{cases}
\text{«S5_IF» } d < 0: & \text{«S5_NEXT» } (x{+}1,\;y), \quad d \mathrel{+}= 2x+3 \\[2pt]
\text{«S5_IF» } d \geq 0: & \text{«S5_NEXT» } (x{+}1,\;y{-}1), \quad d \mathrel{+}= 2(x-y)+5
\end{cases}
\]

\textbf{«S5_JUST_LABEL»} «S5_P4»
\[
F\!\left(x+1,\;y-\tfrac{1}{2}\right) \;=\; (x+1)^2 + \left(y-\tfrac{1}{2}\right)^{\!2} - R^2
\]
«S5_P5»

\subsection{«S5_SUB2»}

«S5_P6»
\[
\text{«S5_REGION» I: } 2b^2 x < 2a^2 y \quad \bigl(|dy/dx| < 1\bigr),
\qquad
\text{«S5_REGION» II: «S5_OTHERWISE»}
\]

«S5_P7»
\begin{align*}
p_1 &= b^2 - a^2 b + \tfrac{a^2}{4}, \\
p_2 &= b^2\!\left(x+\tfrac{1}{2}\right)^{\!2} + a^2\!\left(y-1\right)^{\!2} - a^2 b^2.
\end{align*}

«S5_P8»

\begin{minec}
\textbf{«S5_MC_LABEL»} «S5_MC_EXAMPLE»
\end{minec}

% =============================================================================
\section{«S6_TITLE»}

«S6_P1»

\begin{formula}
\centering
$\displaystyle n_x = \operatorname{clamp}(c_x,\,i,\,i{+}1),\quad
                n_y = \operatorname{clamp}(c_y,\,j,\,j{+}1)$ \\[6pt]
$\displaystyle \text{«S3_INSIDE»}\;\Longleftrightarrow\;
\left(\dfrac{n_x-c_x}{r_x}\right)^{\!2} + \left(\dfrac{n_y-c_y}{r_y}\right)^{\!2} \leq 0{,}94$
\end{formula}

«S6_P2»

«S6_P3»

\begin{minec}
\textbf{«S6_MC_LABEL»} «S6_MC_EXAMPLE»
\end{minec}

% =============================================================================
\section{«S7_TITLE»}

«S7_P1»

\subsection{«S7_SUB1»}
«S7_P2»

\subsection{«S7_SUB2»}
«S7_P3»
\[
b(i,j) \;=\; f(i,j) \;\wedge\;
\bigl(\neg f(i{-}1,j)\,\vee\,\neg f(i{+}1,j)\,\vee\,\neg f(i,j{-}1)\,\vee\,\neg f(i,j{+}1)\bigr)
\]
«S7_P4»

\subsection{«S7_SUB3»}
«S7_P5»
\begin{align*}
t(i,j) &= b(i,j) \;\vee\; \bigl(f(i,j) \,\wedge\, h_H \,\wedge\, h_V\bigr), \\
h_H &= b(i{-}1,j) \;\vee\; b(i{+}1,j), \\
h_V &= b(i,j{-}1) \;\vee\; b(i,j{+}1).
\end{align*}

\begin{minec}
\textbf{«S7_MC_LABEL»} «S7_MC_EXAMPLE»
\end{minec}

«FIG_MODES»

% =============================================================================
\section{«S8_TITLE»}

«S8_P1»
\[
\underset{\text{«S8_CONT»}}{\pi \, r_x \, r_y}
\qquad\longleftrightarrow\qquad
\underset{\text{«S8_DISC»}}{\sum_{j=0}^{G_y-1}\sum_{i=0}^{G_x-1} f(i,j)}
\]
«S8_P2»

\begin{minec}
\textbf{«S8_MC_LABEL»} «S8_MC_EXAMPLE»
\end{minec}

% =============================================================================
\section{«S9_TITLE»}

«S9_P1»
\[
\left(\dfrac{x}{r_x}\right)^{\!2} + \left(\dfrac{y}{r_y}\right)^{\!2} + \left(\dfrac{z}{r_z}\right)^{\!2} \;=\; 1
\]

«S9_P2»
\[
a_\xi = \frac{\xi + \tfrac{1}{2} - c_\xi}{r_\xi}\;\;(\xi \in \{x,y,z\}),
\qquad
\text{«S3_INSIDE»}\;\Longleftrightarrow\;a_x^{\,2} + a_y^{\,2} + a_z^{\,2} \leq 1
\]

\begin{minec}
\textbf{«S9_MC_LABEL»} «S9_MC_EXAMPLE»
\end{minec}

«FIG_3D»

% =============================================================================
\section{«S10_TITLE»}

«S10_P1»
\[
V \;=\; \dfrac{4}{3}\,\pi\, r_x\, r_y\, r_z
\]
«S10_P2»

\textbf{«S10_SHELL_LABEL»} «S10_P3»

\begin{minec}
\textbf{«S10_MC_LABEL»} «S10_MC_EXAMPLE»
\end{minec}

\vspace{0.5em}
\begin{center}
\begin{tabular}{@{}lrrrr@{}}
\toprule
\textbf{«S10_TBL_H1»} & \textbf{«S10_TBL_H2»} & \textbf{«S10_TBL_H3»} & \textbf{«S10_TBL_H4»} & \textbf{«S10_TBL_H5»} \\
\midrule
D=8   &   268 &  5  & 1 & «S10_TBL_NOTE_8»  \\
D=12  &   904 & 15  & 1 & «S10_TBL_NOTE_12» \\
D=16  &  2145 & 34  & 1 & «S10_TBL_NOTE_16» \\
D=20  &  4189 & 66  & 2 & «S10_TBL_NOTE_20» \\
D=24  &  7238 & 114 & 3 & «S10_TBL_NOTE_24» \\
D=32  & 17156 & 269 & 5 & «S10_TBL_NOTE_32» \\
\bottomrule
\end{tabular}
\end{center}

«S10_TBL_CAPTION»

% =============================================================================
\section{«S11_TITLE»}

«S11_P1»
\[
\begin{array}{lcl}
\text{«S11_X»:}    & x \geq \mathit{cut}      & \Rightarrow\; \text{«S11_DISCARD»} \\
\text{«S11_Y»:}    & y \geq \mathit{cut}      & \Rightarrow\; \text{«S11_DISCARD»} \\
\text{«S11_DIAG»:}  & x + y \geq \mathit{cut}  & \Rightarrow\; \text{«S11_DISCARD»}
\end{array}
\]

«S11_P2»
\[
\mathit{cut} \;=\; \mathit{cutPct} \cdot \max_{\text{«S11_AXIS»}}
\]
«S11_P3»

\begin{minec}
\textbf{«S11_MC_LABEL»} «S11_MC_EXAMPLE»
\end{minec}

«FIG_CUTS»

% =============================================================================
\section{«S12_TITLE»}

«S12_P1»
\[
\mathit{thick3D} \;=\;
\bigcup_{z} T\bigl(S_z(z)\bigr) \;\cup\;
\bigcup_{y} T\bigl(S_y(y)\bigr) \;\cup\;
\bigcup_{x} T\bigl(S_x(x)\bigr)
\]
«S12_P2»

\begin{minec}
\textbf{«S12_MC_LABEL»} «S12_MC_EXAMPLE»
\end{minec}

% =============================================================================
\section{«S13_TITLE»}

«S13_P1»
\[
\begin{aligned}
x &= r\,\sin(\varphi)\,\cos(\theta), \\
y &= r\,\cos(\varphi), \\
z &= r\,\sin(\varphi)\,\sin(\theta).
\end{aligned}
\]
«S13_P2»

% =============================================================================
\section{«S14_TITLE»}

«S14_P1»
\[
R \;=\; \sqrt{\,(D_x/2)^2 + (D_y/2)^2 + (D_z/2)^2\,}
\]

«S14_P2»
\[
\mathit{dist}_V \;=\; \dfrac{R}{\tan(\mathit{fov}_V / 2)}
\]
«S14_P3»
\[
\mathit{fov}_H \;=\; 2\,\arctan\!\left(\,\tan(\mathit{fov}_V/2)\cdot \mathit{aspect}\,\right)
\]
«S14_P4»

% =============================================================================
\section{«S15_TITLE»}

«S15_P1»
\[
R' = \mathrm{clamp}(R \cdot f),\quad
G' = \mathrm{clamp}(G \cdot f),\quad
B' = \mathrm{clamp}(B \cdot f)
\]
«S15_P2»
\[
I \;=\; \max\bigl(0,\;\mathbf{n}\cdot\mathbf{l}\bigr)\cdot \mathit{«S15_BASECOLOR»},
\]
«S15_P3»

«FIG_SHADING»

% =============================================================================
\section{«S16_TITLE»}

«S16_P1»

«S16_P2»

\clearpage

% =============================================================================
\section{«S17_TITLE»}

«S17_P1»

\subsection{«S17_SUB1»}
«S17_P2»

\subsection{«S17_SUB2»}
«S17_P3»
\[
\text{«S17_PACKS_LABEL»}:\quad N_{\mathrm{packs}} \;=\; \left\lceil \dfrac{N}{64} \right\rceil
\qquad
\text{«S17_DCHEST_LABEL»}:\quad N_{\mathrm{dc}} \;=\; \left\lceil \dfrac{N}{3456} \right\rceil
\]
«S17_P4»

\subsection{«S17_SUB3»}
«S17_P5»

\vspace{0.4em}
\begin{center}
\small
\begin{tabularx}{\textwidth}{@{}lrrlX@{}}
\toprule
\textbf{«S17_TBL_H1»} & \textbf{«S17_TBL_H2»} & \textbf{«S17_TBL_H3»} & \textbf{«S17_TBL_H4»} & \textbf{«S17_TBL_H5»} \\
\midrule
D=8   &   268 &  5  &  1 «S17_DCHEST_WORD» & «S17_TBL_USE_8»  \\
D=12  &   904 & 15  &  1 «S17_DCHEST_WORD» & «S17_TBL_USE_12» \\
D=16  &  2145 & 34  &  1 «S17_DCHEST_WORD» & «S17_TBL_USE_16» \\
D=20  &  4189 & 66  &  2 «S17_DCHEST_PLURAL» & «S17_TBL_USE_20» \\
D=24  &  7238 & 114 &  3 «S17_DCHEST_PLURAL» & «S17_TBL_USE_24» \\
D=32  & 17156 & 269 &  5 «S17_DCHEST_PLURAL» & «S17_TBL_USE_32» \\
\bottomrule
\end{tabularx}
\end{center}

«S17_P6»

% =============================================================================
\section{«S18_TITLE»}

«S18_P1»

\subsection{«S18_SUB1»}
«S18_P2»

\subsection{«S18_SUB2»}
«S18_P3»
\[
b(i,j,k) \;=\; f(i,j,k) \;\wedge\; \bigl(\neg f(i{\pm}1,j,k)\,\vee\,\neg f(i,j{\pm}1,k)\,\vee\,\neg f(i,j,k{\pm}1)\bigr)
\]
«S18_P4»

\subsection{«S18_SUB3»}
«S18_P5»
\[
F_{\mathrm{exp}} \;=\; \sum_{\mathbf{v}\in V_{\mathrm{solid}}}\;\sum_{\mathbf{n}\in N_6(\mathbf{v})}\!\!\bigl[\mathbf{v}+\mathbf{n}\notin V_{\mathrm{solid}}\bigr]
\]
«S18_P6»

«FIG_OVERLAY»

% =============================================================================
\section{«S19_TITLE»}

«S19_P1»
\[
\text{«S19_LAYER_LABEL»} \;=\; \bigl\{\,(i,j)\;:\;a_x(i)^2 + a_y(j)^2 \leq 1 - a_z(k)^2\,\bigr\}
\]

«S19_P2»
\[
r_x(k) \;=\; r_x\,\sqrt{\,1 - \left(\dfrac{k}{r_z}\right)^{\!2}\,},
\qquad
r_y(k) \;=\; r_y\,\sqrt{\,1 - \left(\dfrac{k}{r_z}\right)^{\!2}\,}
\]
«S19_P3»

\begin{minec}
\textbf{«S19_MC_LABEL»} «S19_MC_EXAMPLE»
\end{minec}

«S19_P4»

% =============================================================================
\section{«S20_TITLE»}

«S20_P1»
\[
V_{\mathrm{total}} \;\approx\; 8\,V_{\mathrm{octant}}\;\;\Longrightarrow\;\;
\text{«S20_REDUCTION_LABEL»}\;=\;\frac{N - N/8}{N} \;=\; 87{,}5\%
\]

«S20_P2»

\subsection{«S20_SUB1»}
«S20_P3»

\begin{minec}
«S20_CMD_EXAMPLE»
\end{minec}

«S20_P4»

\subsection{«S20_SUB2»}
«S20_P5»
\[
T_{\mathrm{octant}} \;+\; 7\,T_{\mathrm{clone}}
\quad\ll\quad
T_{\mathrm{full}}
\]
«S20_P6»

«FIG_OCTANTS»

% =============================================================================
\section{«S21_TITLE»}

«S21_P1»

\subsection{«S21_SUB1»}
«S21_P2»
\[
\text{«S21_FACE_LABEL»}\;\in\;\{\,\text{«S21_FACE_TOP»},\;\text{«S21_FACE_SIDE»},\;\text{«S21_FACE_BOT»}\,\}
\qquad
\mathrm{UV}: [0,1]^2 \to \text{pixels}
\]

«S21_P3»

«FIG_TEXTURES»

\subsection{«S21_SUB2»}
«S21_P4»

\vspace{0.4em}
\begin{center}
\begin{tabular}{@{}llll@{}}
\toprule
\textbf{«S21_TBL_H1»} & \textbf{«S21_TBL_H2»} & \textbf{«S21_TBL_H3»} & \textbf{«S21_TBL_H4»} \\
\midrule
cobblestone        & «S21_BLK_FAMILY_STONE»  & «S21_BLK_TONE_GRAY»  & «S21_BLK_USE_1» \\
stone              & «S21_BLK_FAMILY_STONE»  & «S21_BLK_TONE_GRAY»  & «S21_BLK_USE_2» \\
oak\_planks        & «S21_BLK_FAMILY_WOOD»   & «S21_BLK_TONE_TAN»   & «S21_BLK_USE_3» \\
quartz\_block      & «S21_BLK_FAMILY_QTZ»    & «S21_BLK_TONE_WHT»   & «S21_BLK_USE_4» \\
sandstone          & «S21_BLK_FAMILY_SAND»   & «S21_BLK_TONE_TAN»   & «S21_BLK_USE_5» \\
deepslate          & «S21_BLK_FAMILY_STONE»  & «S21_BLK_TONE_DARK»  & «S21_BLK_USE_6» \\
\bottomrule
\end{tabular}
\end{center}

\subsection{«S21_SUB3»}
«S21_P5»

% =============================================================================
\section{«S22_TITLE»}

«S22_P1»

\begin{itemize}[leftmargin=1.3em,itemsep=0.25em,topsep=0.4em]
  \item \acc{«S22_AREA1_NAME»}: «S22_AREA1_DESC»
  \item \acc{«S22_AREA2_NAME»}: «S22_AREA2_DESC»
  \item \acc{«S22_AREA3_NAME»}: «S22_AREA3_DESC»
  \item \acc{«S22_AREA4_NAME»}: «S22_AREA4_DESC»
  \item \acc{«S22_AREA5_NAME»}: «S22_AREA5_DESC»
  \item \acc{«S22_AREA6_NAME»}: «S22_AREA6_DESC»
  \item \acc{«S22_AREA7_NAME»}: «S22_AREA7_DESC»
  \item \acc{«S22_AREA8_NAME»}: «S22_AREA8_DESC»
\end{itemize}

«S22_P2»

«S22_P3»

% =============================================================================
«BIBLIOGRAPHY»

\clearpage

% =============================================================================
\section*{\color{accent}«APX_A_TITLE»}
\addcontentsline{toc}{section}{«APX_A_TITLE»}

«APX_A_P1»

\subsection*{«APX_A_SUB1»}
«APX_A_P2»

\vspace{0.4em}
\begin{center}
\begin{tabular}{@{}lrrrr@{}}
\toprule
\textbf{D} & \textbf{«APX_A_TBL_FILLED»} & \textbf{«APX_A_TBL_HOLLOW»} & \textbf{«APX_A_TBL_PACKS_F»} & \textbf{«APX_A_TBL_PACKS_H»} \\
\midrule
8   &   268 &   170 &  5  &  3  \\
10  &   523 &   316 &  9  &  5  \\
12  &   904 &   500 & 15  &  8  \\
14  &  1437 &   744 & 23  & 12  \\
16  &  2145 &  1042 & 34  & 17  \\
18  &  3052 &  1338 & 48  & 21  \\
20  &  4189 &  1648 & 66  & 26  \\
24  &  7238 &  2400 & 114 & 38  \\
28  & 11494 &  3296 & 180 & 52  \\
32  & 17156 &  4332 & 269 & 68  \\
\bottomrule
\end{tabular}
\end{center}

«APX_A_P3»

\subsection*{«APX_A_SUB2»}
«APX_A_P4»

\vspace{0.4em}
\begin{center}
\begin{tabular}{@{}lll@{}}
\toprule
\textbf{«APX_A_CMD_H1»} & \textbf{«APX_A_CMD_H2»} & \textbf{«APX_A_CMD_H3»} \\
\midrule
\cmd{//sphere stone 8}     & «APX_A_CMD_DESC_1» & «APX_A_CMD_RESULT_1»  \\
\cmd{//hsphere stone 8}    & «APX_A_CMD_DESC_2» & «APX_A_CMD_RESULT_2»  \\
\cmd{//cyl stone 8 16}     & «APX_A_CMD_DESC_3» & «APX_A_CMD_RESULT_3»  \\
\cmd{//ellipsoid st. 10 5 10} & «APX_A_CMD_DESC_4» & «APX_A_CMD_RESULT_4»  \\
\cmd{/fill ... stone}      & «APX_A_CMD_DESC_5» & «APX_A_CMD_RESULT_5»  \\
\cmd{/clone ... mode:masked} & «APX_A_CMD_DESC_6» & «APX_A_CMD_RESULT_6»  \\
\bottomrule
\end{tabular}
\end{center}

«APX_A_P5»

\subsection*{«APX_A_SUB3»}
«APX_A_P6»

\begin{enumerate}[leftmargin=1.6em,itemsep=0.3em,topsep=0.3em]
  \item «APX_A_STEP_1»
  \item «APX_A_STEP_2»
  \item «APX_A_STEP_3»
  \item «APX_A_STEP_4»
  \item «APX_A_STEP_5»
  \item «APX_A_STEP_6»
\end{enumerate}

«APX_A_P7»

\subsection*{«APX_A_SUB4»}

«APX_A_P8»

\vspace{0.4em}
\begin{center}
\begin{tabular}{@{}lll@{}}
\toprule
\textbf{«APX_A_KEY_H1»} & \textbf{«APX_A_KEY_H2»} & \textbf{«APX_A_KEY_H3»} \\
\midrule
\code{G} & «APX_A_KEY_DESC_G»  & «APX_A_KEY_USE_G» \\
\code{C} & «APX_A_KEY_DESC_C»  & «APX_A_KEY_USE_C» \\
\code{D} & «APX_A_KEY_DESC_D»  & «APX_A_KEY_USE_D» \\
\code{I} & «APX_A_KEY_DESC_I»  & «APX_A_KEY_USE_I» \\
\code{M} & «APX_A_KEY_DESC_M»  & «APX_A_KEY_USE_M» \\
\code{S} & «APX_A_KEY_DESC_S»  & «APX_A_KEY_USE_S» \\
\code{T} & «APX_A_KEY_DESC_T»  & «APX_A_KEY_USE_T» \\
\code{Ctrl+Z / Y} & «APX_A_KEY_DESC_Z»  & «APX_A_KEY_USE_Z» \\
\bottomrule
\end{tabular}
\end{center}

«APX_A_P9»

«APX_A_P10»

\subsection*{«APX_A_SUB5»}

«APX_A_P11»

\begin{itemize}[leftmargin=1.4em,itemsep=0.18em,topsep=0.3em]
  \item \textbf{«GLOS_T1»} --- «GLOS_D1»
  \item \textbf{«GLOS_T2»} --- «GLOS_D2»
  \item \textbf{«GLOS_T3»} --- «GLOS_D3»
  \item \textbf{«GLOS_T4»} --- «GLOS_D4»
  \item \textbf{«GLOS_T5»} --- «GLOS_D5»
  \item \textbf{«GLOS_T6»} --- «GLOS_D6»
  \item \textbf{«GLOS_T7»} --- «GLOS_D7»
  \item \textbf{«GLOS_T8»} --- «GLOS_D8»
  \item \textbf{«GLOS_T9»} --- «GLOS_D9»
  \item \textbf{«GLOS_T10»} --- «GLOS_D10»
  \item \textbf{«GLOS_T11»} --- «GLOS_D11»
  \item \textbf{«GLOS_T12»} --- «GLOS_D12»
\end{itemize}

«APX_A_P12»

\subsection*{«APX_A_SUB6»}

«APX_A_P13»

«APX_A_P14»

«APX_A_P15»

\subsection*{«APX_A_SUB7»}

«APX_A_P16»

\begin{itemize}[leftmargin=1.4em,itemsep=0.2em,topsep=0.3em]
  \item «APX_A_REF1»
  \item «APX_A_REF2»
  \item «APX_A_REF3»
  \item «APX_A_REF4»
  \item «APX_A_REF5»
  \item «APX_A_REF6»
\end{itemize}

«APX_A_P17»

«APX_A_P18»

\vspace{1.2em}

\begin{center}
{\sffamily\bfseries\color{accent}«APX_A_END_LABEL»}
\end{center}

\vspace{0.6em}

«APX_A_P19»

«APX_A_P20»

\end{document}
"""

# ============================================================================
# CONFIGURAÇÃO DE FONTES POR IDIOMA
# ============================================================================
LATIN_FONTS = r"""\usepackage{fontspec}
\usepackage{polyglossia}
\setdefaultlanguage{«POLYGLOSSIA»}
\PolyglossiaSetup{«POLYGLOSSIA»}{indentfirst=false}
\setmainfont{Latin Modern Roman}[Scale=1.08]
\setsansfont{Latin Modern Sans}[Scale=1.08]
\setmonofont{Latin Modern Mono}[Scale=1.00]
\usepackage{unicode-math}
\setmathfont{Latin Modern Math}[Scale=1.08]"""

CYRILLIC_FONTS = r"""\usepackage{fontspec}
\usepackage{polyglossia}
\setdefaultlanguage{russian}
\setotherlanguage{english}
\PolyglossiaSetup{russian}{indentfirst=false}
\setmainfont{Cambria}[Scale=1.05]
\setsansfont{Cambria}[Scale=1.05]
\setmonofont{Latin Modern Mono}
\usepackage{unicode-math}
\setmathfont{Latin Modern Math}[Scale=1.05]"""

CJK_FONTS_ZH = r"""\usepackage{fontspec}
\usepackage{xeCJK}
\setCJKmainfont{Microsoft YaHei}[Scale=1.05]
\setCJKsansfont{Microsoft YaHei}[Scale=1.05]
\setmainfont{Latin Modern Roman}[Scale=1.05]
\setsansfont{Latin Modern Sans}[Scale=1.05]
\setmonofont{Latin Modern Mono}
\usepackage{unicode-math}
\setmathfont{Latin Modern Math}[Scale=1.05]"""

CJK_FONTS_JA = r"""\usepackage{fontspec}
\usepackage{xeCJK}
\setCJKmainfont{Yu Gothic}[Scale=1.05]
\setCJKsansfont{Yu Gothic}[Scale=1.05]
\setmainfont{Latin Modern Roman}[Scale=1.05]
\setsansfont{Latin Modern Sans}[Scale=1.05]
\setmonofont{Latin Modern Mono}
\usepackage{unicode-math}
\setmathfont{Latin Modern Math}[Scale=1.05]"""

CJK_FONTS_KO = r"""\usepackage{fontspec}
\usepackage{xeCJK}
\xeCJKsetup{CJKspace=true}
\XeTeXlinebreaklocale "ko"
\XeTeXlinebreakskip=0pt plus 1pt minus 0.1pt
\setCJKmainfont{Malgun Gothic}[Scale=1.05]
\setCJKsansfont{Malgun Gothic}[Scale=1.05]
\setmainfont{Latin Modern Roman}[Scale=1.05]
\setsansfont{Latin Modern Sans}[Scale=1.05]
\setmonofont{Latin Modern Mono}
\usepackage{unicode-math}
\setmathfont{Latin Modern Math}[Scale=1.05]"""


def fonts_for(loc):
    if loc == "zh-CN":
        return CJK_FONTS_ZH
    if loc == "ja-JP":
        return CJK_FONTS_JA
    if loc == "ko-KR":
        return CJK_FONTS_KO
    if loc == "ru-RU":
        return CYRILLIC_FONTS
    pg = {"en-US":"english","es-ES":"spanish","pt-BR":"portuguese",
          "fr-FR":"french","de-DE":"german"}[loc]
    return LATIN_FONTS.replace("«POLYGLOSSIA»", pg)


# ============================================================================
# TRADUÇÕES (importadas dos módulos de traduções)
# ============================================================================
from translations import T

# ============================================================================
# BUILD
# ============================================================================
def build(loc):
    cfg = dict(T[loc])
    cfg["FONT_SETUP"] = fonts_for(loc)
    # Figure blocks: only the pt-BR build embeds them in this revision.
    # Other locales get an empty string for each FIG_* key.
    fig_keys = ("FIG_3ALG", "FIG_MODES", "FIG_3D", "FIG_CUTS",
                "FIG_SHADING", "FIG_OVERLAY", "FIG_OCTANTS", "FIG_TEXTURES",
                "BIBLIOGRAPHY")
    for k in fig_keys:
        cfg.setdefault(k, "")
    if loc == "pt-BR":
        cfg.update(FIG_BLOCKS_PT_BR)
    out = TEX
    # ordem de substituição não importa porque chaves são únicas
    for k, v in cfg.items():
        out = out.replace("«" + k + "»", v)
    # sanity check
    miss = re.findall(r"«[A-Z0-9_]+»", out)
    if miss:
        print(f"  WARN chaves nao substituidas em {loc}: {set(miss)}")
    tex_path = HERE / f"Block_Round_Math_{loc}.tex"
    tex_path.write_text(out, encoding="utf-8")
    # compila duas vezes (TOC + ref)
    for i in range(2):
        r = subprocess.run(
            [XELATEX, "-interaction=nonstopmode", "-enable-installer",
             tex_path.name],
            cwd=str(HERE), capture_output=True, timeout=300,
        )
    # limpa auxiliares
    for ext in ("aux","log","toc","out"):
        p = tex_path.with_suffix("." + ext)
        if p.exists(): p.unlink()
    return tex_path.with_suffix(".pdf")


# ============================================================================
# BLOCOS DE FIGURA — somente pt-BR nesta revisão
# ============================================================================
FIG_BLOCKS_PT_BR = {
    "FIG_3ALG": r"""\begin{figure}[!htbp]
\centering
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d10_eucl.png}
  \caption{\emph{Euclidiano}}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d10_bres.png}
  \caption{\emph{Bresenham}}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d10_thr.png}
  \caption{\emph{Limiar}}
\end{subfigure}
\caption{Mesma circunferência de diâmetro $D=10$ sob os três critérios. Cada figura é o conjunto de células marcadas pela respectiva versão da desigualdade $d_x^2+d_y^2\leq 1$, renderizada com a textura \emph{cobblestone} do Minecraft. Note como a transição entre filas, as células de quina e os pontos cardeais variam --- três respostas matematicamente corretas sob critérios distintos.}
\label{fig:comp-d10}
\end{figure}""",

    "FIG_MODES": r"""\begin{figure}[!htbp]
\centering
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d20_filled.png}
  \caption{\emph{Preenchido}}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d20_thin.png}
  \caption{\emph{Fino} (\emph{1 voxel})}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_2d_d20_thick.png}
  \caption{\emph{Grosso}}
\end{subfigure}
\caption{Os três modos de renderização para a mesma circunferência euclidiana de $D=20$. O modo \emph{Fino} corresponde ao bordo discreto topológico ($\partial F$); o modo \emph{Grosso} adiciona blocos diagonais para fechar buracos a $45^\circ$, essencial para construções estanques (cúpulas de Vidro/Gelo subaquáticas).}
\label{fig:modes}
\end{figure}""",

    "FIG_3D": r"""\begin{figure}[!htbp]
\centering
\begin{subfigure}[t]{0.46\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_sphere_d10.png}
  \caption{Esfera $D=10$, $r_x=r_y=r_z=5$.}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.46\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_ellipsoid.png}
  \caption{Elipsóide $W=20,\,H=10,\,D=12$.}
\end{subfigure}
\caption{Voxelização em $\mathbb{R}^3$. Cada cubo é um voxel; sua coordenada $(i,j,k)$ no centro é testada na equação implícita $a_x^2+a_y^2+a_z^2\leq 1$. As escadarias visíveis na superfície são consequência matemática da discretização --- exatamente o aspecto que dá ao Minecraft sua identidade visual.}
\label{fig:3d-shapes}
\end{figure}""",

    "FIG_CUTS": r"""\begin{figure}[!htbp]
\centering
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_cut_y.png}
  \caption{Corte $Y$ 50\% (cúpula)}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_cut_x.png}
  \caption{Corte $X$ 50\%}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_cut_diag.png}
  \caption{Diagonal 50\%}
\end{subfigure}
\caption{Três cortes na mesma esfera $D=16$, todos preservando 50\% do volume. O corte $Y$ produz a cúpula clássica $V_{\mathrm{cúpula}}=\tfrac{2}{3}\pi r^3$; o diagonal expõe a hipotenusa $x+y=k$ característica desse plano de corte.}
\label{fig:cuts}
\end{figure}""",

    "FIG_SHADING": r"""\begin{figure}[!htbp]
\centering
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_shading_classic.png}
  \caption{\emph{Classic} (contraste forte)}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_shading_blocks.png}
  \caption{\emph{Blocks} (default)}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.30\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_shading_smooth.png}
  \caption{\emph{Smooth} (faces parecidas)}
\end{subfigure}
\caption{Três multiplicadores de luz aplicados às mesmas três faces visíveis. \emph{Classic} dá o aspecto canônico Minecraft vanilla; \emph{Smooth} reduz o contraste para superfícies suaves; \emph{Blocks} é o intermediário com inset geométrico que revela fronteiras entre voxels mesmo quando a textura é a mesma.}
\label{fig:shading}
\end{figure}""",

    "FIG_OVERLAY": r"""\begin{figure}[!htbp]
\centering
\begin{subfigure}[t]{0.40\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_overlay_off.png}
  \caption{Overlay \emph{OFF}}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.40\linewidth}\centering
  \includegraphics[width=\linewidth]{math_3d_overlay_on.png}
  \caption{Overlay \emph{ON} (default)}
\end{subfigure}
\caption{Mesmo conjunto de voxels com e sem o contorno preto nas arestas expostas. Com o \emph{highlight overlay} ON, um bloco faltante na casca produz uma descontinuidade no padrão que o olho detecta de relance --- ferramenta de validação rápida durante a construção em survival.}
\label{fig:overlay}
\end{figure}""",

    "FIG_OCTANTS": r"""\begin{figure}[!htbp]
\centering
\includegraphics[width=0.45\linewidth]{math_3d_octants.png}
\caption{Esfera $D=10$ com o octante positivo $(+x,+y,+z)$ destacado em verde. Sob a ação do subgrupo $\mathbb{Z}_2^3 \leq O_h$ (ordem 8, gerado pelas três reflexões coordenadas), esse octante determina toda a esfera --- as outras sete regiões são obtidas por uma sequência de \cmd{/clone} com \emph{mode:masked} aplicadas sobre o octante construído manualmente.}
\label{fig:octants}
\end{figure}""",

    "FIG_TEXTURES": r"""\begin{figure}[!htbp]
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
\caption{A mesma esfera de diâmetro $D=8$ renderizada com três blocos diferentes. A silhueta voxelizada (matemática) é idêntica nas três: o algoritmo escolhe os voxels, a textura é uma camada estética posterior que não altera nem o volume nem a topologia.}
\label{fig:textures}
\end{figure}""",

    "BIBLIOGRAPHY": r"""\section*{\color{accent}Referências bibliográficas}
\addcontentsline{toc}{section}{Referências bibliográficas}
\label{sec:bib}

\subsection*{Referências técnicas (rasterização e topologia digital)}

\begin{itemize}[leftmargin=1.4em,itemsep=0.3em,topsep=0.3em]
  \item \textbf{Bresenham, J. E.} \emph{Algorithm for computer control of a digital plotter}.
        IBM Systems Journal, vol.~4, n.~1, p.~25--30, 1965.
        Disponível em \href{https://doi.org/10.1147/sj.41.0025}{doi:10.1147/sj.41.0025}.
        --- artigo original do algoritmo de meio-ponto inteiro tratado na §5 deste documento.

  \item \textbf{Pitteway, M.~L.~V.} \emph{Algorithm for drawing ellipses or hyperbolae
        with a digital plotter}. The Computer Journal, vol.~10, n.~3, p.~282--289, 1967.
        Disponível em \href{https://doi.org/10.1093/comjnl/10.3.282}{doi:10.1093/comjnl/10.3.282}.
        --- generalização do algoritmo de Bresenham para cônicas arbitrárias,
        base da extensão para elipses descrita na §5.

  \item \textbf{Kappel, A.} \emph{An ellipse-drawing algorithm for raster displays}.
        Em \emph{Fundamental Algorithms for Computer Graphics} (R.~A.~Earnshaw, ed.),
        NATO ASI Series F-17, Springer, 1985, p.~257--280.
        --- formulação por duas regiões usada na implementação de elipses.

  \item \textbf{Klette, R.; Rosenfeld, A.} \emph{Digital Geometry: Geometric Methods
        for Digital Picture Analysis}. Morgan Kaufmann, 2004. 656 páginas.
        --- referência padrão para topologia digital, operadores de bordo
        ($\partial F$), 4-/6-/26-conectividade. Usada nas §7, §12 e §18.

  \item \textbf{Foley, J.~D.; van Dam, A.; Feiner, S.~K.; Hughes, J.~F.}
        \emph{Computer Graphics: Principles and Practice}. 3.\textordmasculine{} ed., Addison-Wesley, 2014.
        --- tratamento clássico de rasterização, modelos de iluminação,
        projeção perspectiva. Relevante para as §13--15.
\end{itemize}

\subsection*{Especificações e ferramentas Minecraft referenciadas}

\begin{itemize}[leftmargin=1.4em,itemsep=0.3em,topsep=0.3em]
  \item \textbf{Sponge Project.} \emph{Sponge Schematic Specification, version~2}.
        \href{https://github.com/SpongePowered/Schematic-Specification}{github.com/SpongePowered/Schematic-Specification}.
        --- formato de arquivo \code{.schem} (gzip + NBT) que o Block Round
        exporta. Carregável por WorldEdit, Litematica e MCEdit.

  \item \textbf{EngineHub.} \emph{WorldEdit Documentation}.
        \href{https://worldedit.enginehub.org/}{worldedit.enginehub.org}.
        --- referência oficial para os comandos \cmd{//sphere}, \cmd{//hsphere},
        \cmd{//ellipsoid}, \cmd{//cyl}, \cmd{//schem load} citados ao longo do documento.

  \item \textbf{Mojang AB.} \emph{Minecraft Wiki --- Inventory}.
        \href{https://minecraft.wiki/w/Inventory}{minecraft.wiki/w/Inventory}.
        --- referência sobre slots, stacks, baús simples (27 slots) e
        baús duplos (54 slots) usados na §17.

  \item \textbf{Mojang AB.} \emph{Minecraft Wiki --- Commands/fill, /clone}.
        \href{https://minecraft.wiki/w/Commands/fill}{minecraft.wiki/w/Commands/fill},
        \href{https://minecraft.wiki/w/Commands/clone}{minecraft.wiki/w/Commands/clone}.
        --- comandos vanilla \cmd{/fill} e \cmd{/clone} citados nas §17 e §20.

  \item \textbf{Masady} (\emph{Litematica} mod).
        \href{https://github.com/maruohon/litematica}{github.com/maruohon/litematica}.
        --- mod do Minecraft Java Edition que importa schematics e exibe
        um fantasma translúcido da construção a executar.
\end{itemize}

\subsection*{Geometria, álgebra linear e teoria de grupos}

\begin{itemize}[leftmargin=1.4em,itemsep=0.3em,topsep=0.3em]
  \item \textbf{Lima, E.~L.} \emph{Geometria Analítica e Álgebra Linear}. Coleção
        Matemática Universitária, IMPA, 2.\textordmasculine{} ed., 2014.
        --- equação implícita da elipse, álgebra de planos no $\mathbb{R}^3$,
        coordenadas esféricas. Base do conteúdo das §3, §9 e §13.

  \item \textbf{Armstrong, M.~A.} \emph{Groups and Symmetry}. Undergraduate Texts in
        Mathematics, Springer, 1988.
        --- exposição introdutória ao grupo octaédrico $O_h$ e seus subgrupos,
        usada na §20.

  \item \textbf{Coxeter, H.~S.~M.} \emph{Regular Polytopes}. 3.\textordmasculine{} ed., Dover, 1973.
        --- referência canônica para os grupos de simetria dos sólidos regulares,
        incluindo o tratamento detalhado de $O_h$ de ordem 48 mencionado na §20.

  \item \textbf{Hilbert, D.; Cohn-Vossen, S.} \emph{Geometry and the Imagination}.
        AMS Chelsea, 1990 [orig.~1932].
        --- tratamento clássico de quádricas e visualização geométrica,
        base intuitiva da §9.
\end{itemize}

\subsection*{Algoritmos, estruturas de dados, complexidade}

\begin{itemize}[leftmargin=1.4em,itemsep=0.3em,topsep=0.3em]
  \item \textbf{Cormen, T.~H.; Leiserson, C.~E.; Rivest, R.~L.; Stein, C.}
        \emph{Introduction to Algorithms}. 4.\textordmasculine{} ed., MIT Press, 2022.
        --- análise de complexidade dos três algoritmos da §4--6, divisão
        com teto da §17.

  \item \textbf{Wirth, N.} \emph{Algorithms + Data Structures = Programs}.
        Prentice-Hall, 1976.
        --- exposição clássica do algoritmo de Bresenham para retas e
        sua extensão para circunferências.
\end{itemize}

\subsection*{Recursos online complementares}

\begin{itemize}[leftmargin=1.4em,itemsep=0.3em,topsep=0.3em]
  \item Block Round --- aplicativo: \href{https://vinisouza128.github.io/block-round/}{vinisouza128.github.io/block-round/}.
  \item Block Round --- repositório: \href{https://github.com/ViniSouza128/block-round}{github.com/ViniSouza128/block-round}.
  \item Projeto irmão Pixel Round (versão sem texturas Minecraft):
        \href{https://github.com/ViniSouza128/pixel-round}{github.com/ViniSouza128/pixel-round}.
  \item Plano de aula em pt-BR (3.\textordmasculine{} ano EM):
        \href{https://vinisouza128.github.io/block-round/docs_aula/Plano_de_Aula_pt-BR.pdf}{docs\_aula/Plano\_de\_Aula\_pt-BR.pdf}.
\end{itemize}
""",
}

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    locs = ["en-US","es-ES","pt-BR","fr-FR","de-DE","zh-CN","ja-JP","ru-RU","ko-KR"]
    for loc in locs:
        print(f"[build] {loc}")
        pdf = build(loc)
        if pdf.exists():
            print(f"  OK {pdf.name}  ({pdf.stat().st_size//1024} KB)")
        else:
            print(f"  FAIL")
