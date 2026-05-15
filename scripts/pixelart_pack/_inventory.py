"""Mapa do que falta — diff entre textures/ e textures-pixelart/."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'textures'
DST = ROOT / 'textures-pixelart'

ja = {p.name for p in DST.glob('*.png')}
todos = {p.name for p in SRC.glob('*.png')}
faltam = sorted(todos - ja)

print(f'JA FEITOS: {len(ja)}/{len(todos)}')
print(f'FALTAM   : {len(faltam)}')
print()
for n in faltam:
    img = Image.open(SRC / n).convert('RGBA')
    a = sum(1 for px in img.getdata() if px[3] < 255)
    extra = f' STRIP {img.size}' if img.size != (16, 16) else ''
    marca = f' alpha={a}' if a else ''
    print(f'  {n}{extra}{marca}')
