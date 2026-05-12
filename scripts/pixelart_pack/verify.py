"""Script CLI: percorre textures-pixelart/ e valida o pack contra textures/.

Uso:
    python -m scripts.pixelart_pack.verify             # do repo root
    python scripts/pixelart_pack/verify.py [--qa]      # qualquer subpasta

Sai com codigo 0 se todas as texturas presentes passarem; codigo 1 se
qualquer textura existente quebrar alguma regra. Texturas ausentes em
textures-pixelart/ apenas aparecem como AUSENTES (nao causam falha,
porque o pack e construido em rodadas).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

# permite execucao direta como script
if __package__ is None or __package__ == '':
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.pixelart_pack import helpers


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / 'textures'
DST_DIR = REPO_ROOT / 'textures-pixelart'
QA_DIR = REPO_ROOT / 'scripts' / 'pixelart_pack' / '_qa'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--qa', action='store_true', help='gera grid comparativo em _qa/compare.png')
    parser.add_argument('--apenas', nargs='*', help='valida so esses arquivos (sem extensao opcional)')
    args = parser.parse_args()

    originais = sorted(SRC_DIR.glob('*.png'))
    if args.apenas:
        filtro = set()
        for nome in args.apenas:
            filtro.add(nome if nome.endswith('.png') else f'{nome}.png')
        originais = [p for p in originais if p.name in filtro]

    total = 0
    ok = 0
    ausentes = []
    falhas = []
    pares_qa: list[tuple[Path, Path, str]] = []

    for orig in originais:
        total += 1
        nova = DST_DIR / orig.name
        if not nova.exists():
            ausentes.append(orig.name)
            continue

        try:
            erros = _validar_par(orig, nova)
        except Exception as exc:
            falhas.append((orig.name, [f'excecao: {exc}']))
            continue

        if erros:
            falhas.append((orig.name, erros))
        else:
            ok += 1
            pares_qa.append((orig, nova, orig.stem))

    _imprimir_relatorio(total, ok, ausentes, falhas)

    if args.qa and pares_qa:
        QA_DIR.mkdir(parents=True, exist_ok=True)
        out = QA_DIR / 'compare.png'
        helpers.comparar_grid(
            [str(o) for o, _, _ in pares_qa],
            [str(n) for _, n, _ in pares_qa],
            str(out),
            cols=8,
            escala=8,
            rotulos=[r for _, _, r in pares_qa],
        )
        print(f'\nGrid comparativo: {out.relative_to(REPO_ROOT)}')

    return 1 if falhas else 0


def _validar_par(orig: Path, nova: Path) -> list[str]:
    erros: list[str] = []

    src = Image.open(orig).convert('RGBA')
    dst = Image.open(nova).convert('RGBA')

    if src.size != dst.size:
        erros.append(f'dimensao {dst.size} != {src.size}')
        return erros

    # alpha preservado: se origem tem algum pixel translucido, o destino deve ter algum tambem
    src_tem_alpha = any(p[3] < 255 for p in src.getdata())
    dst_tem_alpha = any(p[3] < 255 for p in dst.getdata())
    if src_tem_alpha and not dst_tem_alpha:
        erros.append('alpha presente no original mas ausente no novo')

    # tileabilidade — apenas para PNGs 16x16 (strips animacao validam frame a frame)
    if dst.width == 16 and dst.height == 16:
        erros.extend(helpers.tile_check(dst))
    elif dst.width == 16 and dst.height > 16:
        frames = dst.height // 16
        if dst.height % 16 != 0:
            erros.append(f'strip {dst.size} nao e multiplo de 16 em altura')
        for f in range(frames):
            frame = dst.crop((0, f * 16, 16, (f + 1) * 16))
            for e in helpers.tile_check(frame):
                erros.append(f'frame {f}: {e}')

    return erros


def _imprimir_relatorio(total: int, ok: int, ausentes: list, falhas: list) -> None:
    print('=' * 56)
    print(f'  verify.py — pack pixel-art alternativo')
    print('=' * 56)
    print(f'  totais em textures/ : {total}')
    print(f'  presentes & ok      : {ok}')
    print(f'  ausentes            : {len(ausentes)}')
    print(f'  falhas              : {len(falhas)}')
    print('=' * 56)

    if falhas:
        print('\nFALHAS')
        for nome, erros in falhas:
            print(f'  X {nome}')
            for e in erros:
                print(f'      - {e}')

    if ok > 0:
        print(f'\n{ok} texturas validadas com sucesso.')

    if ausentes and len(ausentes) <= 20:
        print(f'\nAUSENTES ({len(ausentes)}): {", ".join(ausentes)}')
    elif ausentes:
        print(f'\nAUSENTES ({len(ausentes)}): {", ".join(ausentes[:10])}, ... (+{len(ausentes) - 10})')


if __name__ == '__main__':
    sys.exit(main())
