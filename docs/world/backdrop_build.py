# Builds the hero backdrop (matte painting) from the approved key art inspo/Section_One.png:
# sky, the big cloud, the far headland with its crane, and the sea, with everything that the
# 3D scene draws itself removed (UI, Alu, the gate, the pines, the foreground). The web maps
# it onto a dome by view direction, as if it were infinitely far (src/hero/Sky.tsx), so the
# hero camera at rest sees exactly the key art behind the 3D foreground.
#
#   python docs/world/backdrop_build.py            (needs numpy + Pillow)
#
# Output: public/images/hero/backdrop.webp and docs/world/renders/backdrop_debug.png.
# The mapping constants (PAD_*, F_PX, HORIZON_Y) are mirrored in src/hero/Sky.tsx.
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = os.path.join(ROOT, 'inspo', 'Section_One.png')
OUT = os.path.join(ROOT, 'public', 'images', 'hero', 'backdrop.webp')
DEBUG = os.path.join(ROOT, 'docs', 'world', 'renders', 'backdrop_debug.png')

W, H = 1536, 1024           # key art size
HORIZON_Y = 620             # sea horizon row (level camera, lens shift)
F_PX = 34 / 36 * W          # 34 mm lens on a 36 mm sensor -> focal length in pixels
PAD_X, PAD_TOP, PAD_BOTTOM = 160, 288, 64

img = np.asarray(Image.open(SRC).convert('RGB').resize((W, H), Image.LANCZOS)).astype(np.float32) / 255
yy, xx = np.mgrid[0:H, 0:W]


# ---------------------------------------------------------------- masks
def poly_mask(points, dilate=0):
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in points], fill=255)
    if dilate:
        m = m.filter(ImageFilter.MaxFilter(dilate * 2 + 1))
    return np.asarray(m) > 127


def rrect_mask(x0, y0, x1, y1, r, dilate=0):
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle((x0 - dilate, y0 - dilate, x1 + dilate, y1 + dilate),
                                        radius=max(0, r + dilate), fill=255)
    return np.asarray(m) > 127


ui = (rrect_mask(36, 26, 238, 72, 6) | rrect_mask(1392, 20, 1506, 76, 28)
      | rrect_mask(279, 384, 568, 455, 20, 3) | rrect_mask(285, 374, 353, 405, 12, 3)
      | poly_mask([(458, 448), (500, 448), (490, 480)], 3))

alu = poly_mask([(440, 552), (470, 545), (486, 518), (492, 500), (496, 476), (520, 468), (524, 454),
                 (544, 454), (544, 502), (628, 502), (634, 486), (648, 478), (662, 486), (662, 632),
                 (634, 652), (634, 720), (614, 742), (614, 780), (490, 780), (488, 700), (468, 652),
                 (440, 642)], 4)

# gate: the frame ring (plus its inner glow) and the glass opening
gate_outer = rrect_mask(642, 246, 898, 756, 26, 6) | poly_mask([(628, 760), (912, 760), (904, 730), (636, 730)])
glass_in = rrect_mask(663, 266, 877, 732, 22, -24)   # the inner-edge glow goes too
frame = gate_outer & ~glass_in
glass_low = rrect_mask(663, 266, 877, 732, 22) & (yy >= 592)      # glow over the sea: rebuilt


# pines: pine-coloured pixels inside their boxes (olive foliage, brown trunk), grown a little.
# Sky and sea are blue; the terrace and rocks are pale; the headland's rock is blue-grey and
# its sunlit cliff is brown-pink, so near the headland only olive counts.
def not_sky(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    m = (b - r < 0.10) & (r + g + b < 2.05)
    near_headland = (xx > 1300) & (xx < 1450) & (yy > 540) & (yy < 642)
    olive = (g - b > 0.02) & (g > 0.9 * r)        # shaded boughs are barely green
    return m & ~(near_headland & ~olive)


pine_box = ((xx < 214) & (yy > 350) & (yy < 690)) | ((xx > 1370) & (yy > 376) & (yy < 742))
pines = pine_box & not_sky(img)
pines = np.asarray(Image.fromarray((pines * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(11))) > 127
pines &= pine_box

hole = ui | alu | frame | glass_low | pines

# ---------------------------------------------------------------- sky: smooth model + residual
sky_rows = yy < HORIZON_Y
headland = (xx > 1080) & (xx < 1460) & (yy > 540) & (yy < 640)


def design(x, y):
    u, v = x / W * 2 - 1, y / H * 2 - 1
    cols = [np.ones_like(u)]
    for d in range(1, 5):
        for i in range(d + 1):
            cols.append(u ** (d - i) * v ** i)
    return np.stack(cols, -1)


fit = sky_rows & ~hole & ~headland & ((xx % 3) == 0) & ((yy % 3) == 0)
for it in range(4):
    A = design(xx[fit].astype(np.float32), yy[fit].astype(np.float32))
    coef, *_ = np.linalg.lstsq(A, img[fit], rcond=None)
    model = design(xx.astype(np.float32), yy.astype(np.float32)) @ coef
    res = img - model
    # clouds and wisps are warmer/whiter than the sky behind them: drop them from the fit
    fit = sky_rows & ~hole & ~headland & ((xx % 3) == 0) & ((yy % 3) == 0) & (res[..., 0] < 0.035)


def harmonic_fill(field, known, iters=(400, 220, 140, 90), domain=None):
    """Fills unknown pixels with the smooth (Laplace) interpolation of the known ones,
    coarse to fine. Reflective borders; pixels outside `domain` are walls (never averaged in)."""
    if domain is None:
        domain = np.ones(known.shape, bool)
    levels = [(field, known, domain)]
    f, k, dm = field, known, domain
    while min(f.shape[:2]) > 64:
        h2, w2 = f.shape[0] // 2 * 2, f.shape[1] // 2 * 2
        fk = (f[:h2, :w2] * k[:h2, :w2, None]).reshape(h2 // 2, 2, w2 // 2, 2, -1).sum((1, 3))
        kk = k[:h2, :w2].reshape(h2 // 2, 2, w2 // 2, 2).sum((1, 3))
        f = fk / np.maximum(kk, 1)[..., None]
        k = kk > 0
        dm = dm[:h2, :w2].reshape(h2 // 2, 2, w2 // 2, 2).any((1, 3))
        levels.append((f, k, dm))
    guess = None
    for li, (f, k, dm) in enumerate(reversed(levels)):
        u = f.copy()
        if guess is not None:
            g = np.repeat(np.repeat(guess, 2, 0), 2, 1)
            g = np.pad(g, ((0, u.shape[0] - g.shape[0]), (0, u.shape[1] - g.shape[1]), (0, 0)), mode='edge')
            u[~k] = g[~k]
        wd = np.pad(dm.astype(np.float32), 1, mode='edge')
        wsum = wd[:-2, 1:-1] + wd[2:, 1:-1] + wd[1:-1, :-2] + wd[1:-1, 2:]
        n = iters[min(li, len(iters) - 1)] if li < len(levels) - 1 else iters[-1]
        for _ in range(n):
            p = np.pad(u * dm[..., None], ((1, 1), (1, 1), (0, 0)), mode='edge')
            s = p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]
            avg = s / np.maximum(wsum, 1)[..., None]
            u = np.where(k[..., None] | ~dm[..., None], f, avg)
        guess = u
    return guess


sky_known = ~hole & sky_rows
res_fill = harmonic_fill(np.where(sky_known[..., None], img - model, 0), sky_known | ~sky_rows)
sky = np.where(sky_rows[..., None], model + res_fill, 0)
sky = np.where(sky_known[..., None], img, sky)

# ---------------------------------------------------------------- sea: rebuilt row by row
r, g, b = img[..., 0], img[..., 1], img[..., 2]
sea_class = (b - r > 0.18) & (g - r > 0.12)
sea_known = (yy >= HORIZON_Y) & sea_class & ~hole
sea_known = ~(np.asarray(Image.fromarray(((~sea_known) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 127)
sea_known &= yy >= HORIZON_Y
sea_known |= headland & (yy >= HORIZON_Y) & ~hole & ~sea_class & (yy < 640)   # headland waterline

# Each row: known water stays; short gaps (Alu, the gate posts) are bridged by interpolating
# along the row, which suits the horizontal wave bands; everything else takes the row's mean
# water colour (the last reliable row's, further down, so the shore tint does not drift).
sea = img.copy()
rng = np.random.default_rng(7)
mean = None
for y in range(HORIZON_Y, H):
    k = sea_known[y]
    row = img[y].copy()
    if k.sum() > 120:
        mean = np.median(img[y, k], axis=0)
    fill = np.broadcast_to(mean, (W, 3)).copy()
    fill += rng.normal(0, 0.006, (W, 1)).astype(np.float32)
    if k.sum() > 2:
        xs = np.nonzero(k)[0]
        gap_l = np.searchsorted(xs, np.arange(W)) - 1
        gap_r = np.minimum(gap_l + 1, len(xs) - 1)
        gl, gr = xs[np.clip(gap_l, 0, None)], xs[gap_r]
        bridged = (gap_l >= 0) & (gr > np.arange(W)) & (gr - gl < 360)
        interp = np.stack([np.interp(np.arange(W), xs, img[y, xs, c]) for c in range(3)], -1)
        fill[bridged] = interp[bridged]
    row[~k] = fill[~k]
    sea[y] = row
# soften the synthesized parts a touch horizontally so they read as water, not streaks
syn = (yy >= HORIZON_Y) & ~sea_known
blur = np.asarray(Image.fromarray((np.clip(sea, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(2))).astype(np.float32) / 255
sea = np.where(syn[..., None], blur, sea)

plate = np.where(sky_rows[..., None], sky, sea)
plate = np.clip(plate, 0, 1)

# ---------------------------------------------------------------- pad for parallax and tall screens
PW, PH = W + 2 * PAD_X, H + PAD_TOP + PAD_BOTTOM
out = np.zeros((PH, PW, 3), np.float32)
out[PAD_TOP:PAD_TOP + H, PAD_X:PAD_X + W] = plate


def edge_band(cols):
    """Mean of the outer columns, blurred down the rows (sky rows only, the horizon stays sharp)."""
    e = cols.mean(1)
    k = 41
    pad = np.pad(e[:HORIZON_Y], ((k // 2, k // 2), (0, 0)), mode='edge')
    cs = np.cumsum(np.vstack([np.zeros((1, 3), np.float32), pad]), 0)
    e[:HORIZON_Y] = (cs[k:] - cs[:-k]) / k
    return e


eL, eR = edge_band(plate[:, :24]), edge_band(plate[:, -24:])
for i in range(PAD_X):
    t = (PAD_X - i) / PAD_X                     # 1 at the outer edge
    out[PAD_TOP:PAD_TOP + H, i] = plate[:, 0] * (1 - t) ** 3 + eL * (1 - (1 - t) ** 3)
    out[PAD_TOP:PAD_TOP + H, PAD_X + W + PAD_X - 1 - i] = plate[:, -1] * (1 - t) ** 3 + eR * (1 - (1 - t) ** 3)
out[PAD_TOP + H:] = out[PAD_TOP + H - 1:PAD_TOP + H]
# above the key art: the top rows, smoothed sideways, deepening toward the zenith blue
top = out[PAD_TOP:PAD_TOP + 16].mean(0)
k = 301
cs = np.cumsum(np.vstack([np.zeros((1, 3), np.float32), np.pad(top, ((k // 2, k // 2), (0, 0)), mode='edge')]), 0)
top_s = (cs[k:] - cs[:-k]) / k
zenith = np.array([0.09, 0.53, 0.86], np.float32)
for i in range(PAD_TOP):
    t = (PAD_TOP - i) / PAD_TOP
    s = t * t * (3 - 2 * t)
    out[i] = (top * (1 - s) + top_s * s) * (1 - 0.6 * t) + zenith * 0.6 * t
os.makedirs(os.path.dirname(OUT), exist_ok=True)
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(OUT, 'WEBP', quality=92, method=6)

# ================================================================ the plate (foreground layer)
# What the 3D foreground shows by projection from the hero camera: ground, slabs, rocks and
# pines as painted, with the things the scene draws itself (Alu, the gate, the gold tufts,
# the "scroll" label) painted out, and the foreground colours grown a little past their
# edges so a slightly-too-big proxy mesh never picks up sky or sea.
PLATE = os.path.join(ROOT, 'public', 'images', 'hero', 'plate.webp')

# where the water ends, per column: the first run of sea below the horizon (masks skipped)
sea_px = ((yy >= HORIZON_Y) & sea_class) | (headland & (yy < 642))
bottom = np.full(W, -1)
for x in range(W):
    y = HORIZON_Y
    while y < H and (sea_px[y, x] or hole[y, x]):
        y += 1
    if not hole[y - 1, x] or y == HORIZON_Y:
        bottom[x] = y
known_cols = bottom >= 0
xs_k = np.nonzero(known_cols)[0]
bottom = np.interp(np.arange(W), xs_k, bottom[xs_k])
bottom[628:913] = 746                     # behind the gate the slab ends at its base
fg = (yy >= bottom[None, :]) | (pines & (yy < HORIZON_Y + 140))
fg &= ~(headland & (yy < 640) & ~pines)       # the headland is backdrop, the boughs in front are not


def grow(m, n):
    return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(n * 2 + 1))) > 127


def gold_px(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return (r > 0.62) & (r - b > 0.38) & (g > 0.33) & (g / np.maximum(r, 1e-3) > 0.5)


tuft_zones = [(203, 708, 288, 776), (286, 680, 360, 768), (366, 820, 476, 900), (216, 888, 320, 974),
              (580, 676, 644, 750), (1026, 788, 1158, 880), (1222, 922, 1306, 1010)]
tufts = np.zeros((H, W), bool)
for (x0, y0, x1, y1) in tuft_zones:
    box = (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
    tufts |= box & gold_px(img)
tufts = grow(tufts, 2)
label = (xx >= 664) & (xx < 872) & (yy >= 950) & (yy < 978)
# the painted frame stays in the plate: the 3D frame wears it by projection
frame_px = (rrect_mask(642, 246, 898, 756, 26, 2) | poly_mask([(630, 758), (910, 758), (902, 732), (638, 732)]))     & ~rrect_mask(663, 266, 877, 732, 22, -1)
fg = fg | frame_px
paint_out = (alu | tufts | label) & fg           # includes Alu's antenna across the left post

plate_fg = harmonic_fill(np.where((fg & ~paint_out)[..., None], img, 0), fg & ~paint_out,
                         iters=(500, 300, 200, 160), domain=fg)
plate_fg = np.where(paint_out[..., None], plate_fg, img)
# where Alu's antenna crossed the left post: interpolate down each column, which keeps the
# post's shading across its width (a 2D fill would average in the sky beside it)
post = paint_out & frame_px
for x in np.nonzero(post.any(0))[0]:
    col = post[:, x]
    ys = np.nonzero(col)[0]
    ya, yb = ys.min() - 1, ys.max() + 1
    while ya > 0 and paint_out[ya, x]:
        ya -= 1
    while yb < H - 1 and paint_out[yb, x]:
        yb += 1
    t = ((ys - ya) / max(1, yb - ya))[:, None]
    plate_fg[ys, x] = img[ya, x] * (1 - t) + img[yb, x] * t

# grow foreground colours outward (nearest-ish), then everything else is the backdrop
cur, have = plate_fg * fg[..., None], fg.copy()
for _ in range(2):   # just past anti-aliased edges; a bigger proxy should show the sea
    p = np.pad(cur, ((1, 1), (1, 1), (0, 0)))
    hp = np.pad(have.astype(np.float32), 1)
    s = p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]
    n = hp[:-2, 1:-1] + hp[2:, 1:-1] + hp[1:-1, :-2] + hp[1:-1, 2:]
    new = ~have & (n > 0)
    cur = np.where(new[..., None], s / np.maximum(n, 1)[..., None], cur)
    have |= new
plate_img = np.where(have[..., None], cur, plate)
Image.fromarray((np.clip(plate_img, 0, 1) * 255).astype(np.uint8)).save(PLATE, 'WEBP', quality=93, method=6)

dbg = (np.clip(out, 0, 1) * 255).astype(np.uint8).copy()
edge = np.zeros((H, W), bool)
for m in (ui, alu, frame, glass_low, pines):
    e = m & ~(np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3))) > 127)
    edge |= e
dbg[PAD_TOP:PAD_TOP + H, PAD_X:PAD_X + W][edge] = (255, 0, 160)
Image.fromarray(dbg).save(DEBUG)
pd = (np.clip(plate_img, 0, 1) * 255).astype(np.uint8).copy()
fe = (fg & grow(~fg, 1)) | (paint_out & grow(~paint_out, 1))
pd[fe] = (255, 0, 160)
Image.fromarray(pd).save(DEBUG.replace('backdrop_debug', 'plate_debug'))
np.save(os.path.join(os.path.dirname(DEBUG), 'fg_mask.npy'), fg)

# pine silhouettes (left/right extent per row) for the 3D proxies in hero_build.py
raw = not_sky(img)
sil = {}
for name, (x0, x1, y_end) in {'Pine_L': (0, 214, 652), 'Pine_R': (1370, W, 736)}.items():
    rows = []
    for y in range(340, y_end, 6):
        cols = np.nonzero(raw[y, x0:x1])[0]
        if len(cols) > 3:
            L, Rr = int(cols.min() + x0), int(cols.max() + x0)
            rows.append([y, L - 60 if L <= x0 + 1 else L, Rr + 60 if Rr >= W - 2 else Rr])
    sil[name] = rows
with open(os.path.join(os.path.dirname(DEBUG), 'pines.json'), 'w') as fh:
    json.dump(sil, fh)
print(json.dumps({'backdrop': OUT, 'size': [PW, PH], 'pad': [PAD_X, PAD_TOP], 'f_px': F_PX, 'horizon_y': HORIZON_Y,
                  'kb': round(os.path.getsize(OUT) / 1024), 'plate_kb': round(os.path.getsize(PLATE) / 1024)}))
