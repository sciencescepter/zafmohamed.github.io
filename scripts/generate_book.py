"""Generate assets/hero-book.svg: an open book with pages mid-flip.

The book is modelled in 3D, split into small quads, sorted back to front
(painter's algorithm), and projected with perspective. Edit the settings
below and run:

    python3 scripts/generate_book.py

World axes: x across the spread (spine at x=0), y from the bottom edge of
the pages (0) to the top (D), z up off the table.
"""
import math
from pathlib import Path

# ---- View ----------------------------------------------------------------
ELEV = math.radians(40)   # camera angle above the table
YAW = math.radians(14)    # book rotated on the table; right side recedes
DIST = 5.0                # camera distance; smaller = stronger perspective
SCALE = 260               # world units -> svg px

# ---- Book ----------------------------------------------------------------
W, D = 1.0, 1.4           # page width, page height
COVER = 0.04              # cover overhang past the pages
COVER_T = 0.03            # cover board thickness
BLOCK = 0.13              # page block thickness at the fore-edge
FLIP_ANGLES = [42, 74, 104, 136]  # loose pages, degrees up from the right block
FLIP_BEND = -38           # degrees each loose page curls along its width

# ---- Palette (matches css/styles.css) ------------------------------------
BG, SURFACE, PAGE, LINE, MUTED = '#0a0a0a', '#141414', '#1b1b1b', '#f5f5f5', '#8c8c8c'

NU, NY = 18, 6            # quads per surface across / down the page
ROWS = [0.12 + 0.065 * i for i in range(13) if i != 6]  # printed lines (fraction of D)


def block_top(u):
    """Top page height at fraction u from the spine (0) to the fore-edge (1)."""
    return BLOCK * (1 - (1 - u) ** 5) + 0.07 * math.sin(math.pi * u ** 0.8) + 0.012


def world(x, y, z):
    """Centre the book and rotate it on the table."""
    y -= D / 2
    return (x * math.cos(YAW) - y * math.sin(YAW), x * math.sin(YAW) + y * math.cos(YAW), z)


def depth(p):
    x, y, z = world(*p)
    return y * math.cos(ELEV) - z * math.sin(ELEV)


def project(p):
    x, y, z = world(*p)
    k = DIST / (DIST + y * math.cos(ELEV) - z * math.sin(ELEV))
    return (SCALE * x * k, -SCALE * k * (y * math.sin(ELEV) + z * math.cos(ELEV)))


class Quad:
    def __init__(self, corners, fill, lines=()):
        self.corners = corners          # 3D points
        self.fill = fill
        self.lines = list(lines)        # (points, style class)
        self.depth = sum(depth(c) for c in corners) / len(corners)


quads = []


def lerp(a, b, t):
    return a + (b - a) * t


def sheet(curve, fill, rows, outline_u0=False, outline_u1=True, text_from=0.14, text_to=0.88):
    """A surface swept along y from a cross-section curve(u) -> (x, z).

    Split into NU x NY quads. Printed lines, the top/bottom page edges, and
    the side edges travel with the quad they sit on, so nearer quads hide them.
    """
    for i in range(NU):
        u0, u1 = i / NU, (i + 1) / NU
        (xa, za), (xb, zb) = curve(u0), curve(u1)
        for j in range(NY):
            y0, y1 = D * j / NY, D * (j + 1) / NY
            lines = []
            if j == 0:
                lines.append(([(xa, 0, za), (xb, 0, zb)], 'o'))
            if j == NY - 1:
                lines.append(([(xa, D, za), (xb, D, zb)], 'o'))
            if i == 0 and outline_u0:
                lines.append(([(xa, y0, za), (xa, y1, za)], 'o'))
            if i == NU - 1 and outline_u1:
                lines.append(([(xb, y0, zb), (xb, y1, zb)], 'o'))
            for r in rows:
                y = r * D
                if y0 <= y < y1:
                    a, b = max(u0, text_from), min(u1, text_to)
                    if a < b:
                        ta, tb = (a - u0) / (u1 - u0), (b - u0) / (u1 - u0)
                        lines.append(([(lerp(xa, xb, ta), y, lerp(za, zb, ta) + 0.003),
                                       (lerp(xa, xb, tb), y, lerp(za, zb, tb) + 0.003)], 't'))
            quads.append(Quad([(xa, y0, za), (xb, y0, zb), (xb, y1, zb), (xa, y1, za)], fill, lines))


def block_faces(side):
    """Bottom face and fore-edge of one page block, with page-edge lines."""
    for i in range(NU):
        u0, u1 = i / NU, (i + 1) / NU
        xa, xb = side * u0 * W, side * u1 * W
        za, zb = block_top(u0), block_top(u1)
        edges = [([(xa, 0, za * k), (xb, 0, zb * k)], 'e') for k in (0.2, 0.4, 0.6, 0.8)]
        quads.append(Quad([(xa, 0, 0), (xb, 0, 0), (xb, 0, zb), (xa, 0, za)], BG, edges))
    x, top = side * W, block_top(1)
    for j in range(NY):
        y0, y1 = D * j / NY, D * (j + 1) / NY
        edges = [([(x, y0, top * k), (x, y1, top * k)], 'e') for k in (0.2, 0.4, 0.6, 0.8)]
        edges.append(([(x, y0, 0), (x, y1, 0)], 'o'))
        quads.append(Quad([(x, y0, 0), (x, y1, 0), (x, y1, top), (x, y0, top)], BG, edges))


def flipping_page(angle_deg):
    """A loose page hinged at the spine, curling as it turns."""
    base_z = block_top(0)
    steps = 200

    def curve(u):
        x, z = 0.0, base_z
        n = int(u * steps)
        for k in range(n):
            phi = math.radians(angle_deg + FLIP_BEND * (k + 0.5) / steps)
            x += math.cos(phi) * W / steps
            z += math.sin(phi) * W / steps
        return (x, z)

    sheet(curve, PAGE, ROWS[::2], text_from=0.16, text_to=0.84)


# Page blocks: their top surfaces and visible faces
sheet(lambda u: (-u * W, block_top(u)), SURFACE, ROWS)
sheet(lambda u: (u * W, block_top(u)), SURFACE, ROWS)
block_faces(-1)
block_faces(1)
for a in FLIP_ANGLES:
    flipping_page(a)

# Cover board sits under everything, so it is drawn first
cx0, cx1, cy0, cy1 = -W - COVER, W + COVER, -COVER, D + COVER
cover = [
    ([(cx0, cy0, 0), (cx1, cy0, 0), (cx1, cy1, 0), (cx0, cy1, 0)], SURFACE),
    ([(cx0, cy0, -COVER_T), (cx1, cy0, -COVER_T), (cx1, cy0, 0), (cx0, cy0, 0)], LINE),
    ([(cx0, cy0, -COVER_T), (cx0, cy1, -COVER_T), (cx0, cy1, 0), (cx0, cy0, 0)], LINE),
]

# ---- Render ----------------------------------------------------------------
# Styles live in one <style> block; consecutive shapes with the same style are
# merged into a single path to keep the file small.
FILLS = {BG: 'b', SURFACE: 's', PAGE: 'p', LINE: 'w'}
pts, out = [], []


def d_attr(points, close):
    proj = [project(p) for p in points]
    pts.extend(proj)
    return 'M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in proj) + ('Z' if close else '')


def emit(cls, d):
    if out and out[-1][0] == cls:
        out[-1][1].append(d)
    else:
        out.append((cls, [d]))


for corners, fill in cover:
    emit('c' + FILLS[fill], d_attr(corners, True))

for q in sorted(quads, key=lambda q: -q.depth):
    emit(FILLS[q.fill], d_attr(q.corners, True))
    for points, cls in q.lines:
        emit(cls, d_attr(points, False))

xs, ys = [p[0] for p in pts], [p[1] for p in pts]
pad = 8
x0, y0 = min(xs) - pad, min(ys) - pad
w, h = max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad

style = (
    f'.b{{fill:{BG};stroke:{BG}}}.s{{fill:{SURFACE};stroke:{SURFACE}}}.p{{fill:{PAGE};stroke:{PAGE}}}'
    f'.b,.s,.p{{stroke-width:.8}}'
    f'.cs{{fill:{SURFACE}}}.cw{{fill:{LINE}}}.cs,.cw,.o{{stroke:{LINE};stroke-width:1.5}}'
    f'.t{{stroke:{MUTED};stroke-width:1}}.e{{stroke:{MUTED};stroke-width:.7}}'
    '.o,.t,.e{fill:none}'
)
body = '\n'.join(f'<path class="{cls}" d="{"".join(ds)}"/>' for cls, ds in out)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {w:.0f} {h:.0f}" '
       f'stroke-linecap="round" stroke-linejoin="round">\n'
       '<!-- Generated by scripts/generate_book.py. Edit the script, not this file. -->\n'
       f'<style>{style}</style>\n{body}\n</svg>\n')

dest = Path(__file__).resolve().parent.parent / 'assets' / 'hero-book.svg'
dest.parent.mkdir(exist_ok=True)
dest.write_text(svg)
print(f'wrote {dest} ({len(svg) // 1024} KB, {len(quads)} quads)')
