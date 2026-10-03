"""Rebuild the coloured monogram files from the traced geometry.

The geometry is traced from public/images/ashish-website-logo.png (2400 px, a perfect circle of r=1200,
strokes 100 px wide with round caps and joins); it matches the original to within about 1% of stroke
pixels. Only the colours change. The short top bar (the "flag" on the second upright) can take its own
colour so it echoes Alu's orange flag.

Run from the repo root:  python docs/design/logo/build_logo.py
Writes logo-<name>.svg and logo-<name>.png (1024 px, transparent) next to this file.
"""
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).parent
SIZE = 2400
W = 100  # stroke width

# Two strokes: the left upright + long diagonal, then the crossbar, return diagonal, second upright and top bar.
STROKES = [
    [(577.5, 1835), (577.5, 557), (1855, 1835)],
    [(577.5, 1209.5), (1855, 1209.5), (1210, 1835), (1210, 557), (1857, 557)],
]
FLAG = ((1260, 557), (1857, 557))  # the top bar, right of the second upright

NAVY, OCEAN, CYAN, CREAM, ORANGE = "#03045E", "#0077B6", "#00B4D8", "#FFFCF7", "#FF9F1C"
VARIANTS = {
    "alu":     dict(disc=CREAM, stroke=NAVY,  flag=ORANGE),
    "ocean":   dict(disc=OCEAN, stroke=CREAM, flag=ORANGE),
    "powered": dict(disc=NAVY,  stroke=CYAN,  flag=ORANGE),
    "cyan":    dict(disc=CYAN,  stroke=NAVY,  flag=CREAM),
}


def svg(disc, stroke, flag):
    (fx0, fy), (fx1, _) = FLAG
    d = " ".join("M" + " L".join(f"{x:g} {y:g}" for x, y in s) for s in STROKES)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}">
  <circle cx="1200" cy="1200" r="1200" fill="{disc}"/>
  <path d="{d}" fill="none" stroke="{stroke}" stroke-width="{W}" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M{fx0} {fy - W / 2:g}H{fx1}a{W / 2:g} {W / 2:g} 0 0 1 0 {W}H{fx0}z" fill="{flag}"/>
</svg>
"""


def png(disc, stroke, flag, out=1024, ss=4):
    big = out * ss
    k = big / SIZE
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.ellipse((0, 0, big - 1, big - 1), fill=disc)
    r = W * k / 2
    for s in STROKES:
        pts = [(x * k, y * k) for x, y in s]
        dr.line(pts, fill=stroke, width=round(W * k), joint="curve")
        for x, y in (pts[0], pts[-1]):
            dr.ellipse((x - r, y - r, x + r, y + r), fill=stroke)
    (fx0, fy), (fx1, _) = FLAG
    dr.rectangle((fx0 * k, (fy - W / 2) * k, fx1 * k, (fy + W / 2) * k), fill=flag)
    dr.ellipse((fx1 * k - r, fy * k - r, fx1 * k + r, fy * k + r), fill=flag)
    return im.resize((out, out), Image.LANCZOS)


if __name__ == "__main__":
    for name, c in VARIANTS.items():
        (HERE / f"logo-{name}.svg").write_text(svg(**c), encoding="utf-8")
        png(**c).save(HERE / f"logo-{name}.png")
        print("wrote", name)
