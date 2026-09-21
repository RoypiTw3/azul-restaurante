"""Recrea el wordmark "azul" (aprox. al logo de Linktree) con Arial Black.
Salida: logo-color.png, logo-blanco.png, logo-negro.png (fondo transparente),
favicon.png y og.png (cuadrados con fondo crema)."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")
FONT = '/System/Library/Fonts/Supplemental/Arial Black.ttf'
GREEN = (0x3E, 0x70, 0x65); BLUE = (0x4B, 0x7A, 0x80); NAVY = (0x37, 0x4A, 0x5B)
CREAM = (0xED, 0xEA, 0xE1); INK = (0x12, 0x1A, 0x1A); WHITE = (255, 255, 255)
S = 1000
f = ImageFont.truetype(FONT, S)
fz = ImageFont.truetype(FONT, int(S * 1.10))

def glyph_mask(ch, font):
    bbox = font.getbbox(ch)
    m = Image.new('L', (bbox[2] - bbox[0] + 4, bbox[3] - bbox[1] + 4), 0)
    ImageDraw.Draw(m).text((-bbox[0] + 2, -bbox[1] + 2), ch, font=font, fill=255)
    return m, bbox

def build(ov_az=0.17, ov_zu=0.24, gap_ul=-0.01):
    ma, ba = glyph_mask('a', f); mz, bz = glyph_mask('z', fz); mu, bu = glyph_mask('u', f); ml, bl = glyph_mask('l', f)
    W = int(S * 3.2); H = int(S * 1.4)
    canvas = {k: Image.new('L', (W, H), 0) for k in 'azul'}
    base_y = int(S * 1.15)
    def place(key, m, bbox, font, x):
        y = base_y - (font.getmetrics()[0] - bbox[1])
        canvas[key].paste(m, (int(x), y - 2), m)
        return x + m.width - 4
    x = int(S * 0.08)
    xa_end = place('a', ma, ba, f, x)
    xz_end = place('z', mz, bz, fz, xa_end - ma.width * ov_az)
    xu_end = place('u', mu, bu, f, xz_end - mz.width * ov_zu)
    place('l', ml, bl, f, xu_end + mu.width * gap_ul)
    return canvas

canvas = build()
A, Z, U, L = (np.array(canvas[k]) for k in 'azul')
green = np.maximum(np.maximum(A, U), L)
overlap = np.minimum(Z, green)

def compose(cg, cb, cn, bg=None):
    H, W = A.shape
    out = np.zeros((H, W, 4), dtype=np.uint8)
    if bg is not None:
        out[..., :3] = bg; out[..., 3] = 255
    def paint(mask, col):
        a = mask.astype(float) / 255.0
        for i in range(3):
            out[..., i] = (out[..., i] * (1 - a) + col[i] * a).astype(np.uint8)
        out[..., 3] = np.maximum(out[..., 3], mask)
    paint(green, cg); paint(Z, cb); paint(overlap, cn)
    return Image.fromarray(out)

def crop_pad(im, pad):
    b = im.getchannel('A').getbbox()
    return im.crop((b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad))

color = crop_pad(compose(GREEN, BLUE, NAVY), 30)
color.save(os.path.join(OUT, 'logo-color.png'))
crop_pad(compose(WHITE, WHITE, WHITE), 30).save(os.path.join(OUT, 'logo-blanco.png'))
crop_pad(compose(INK, INK, INK), 30).save(os.path.join(OUT, 'logo-negro.png'))

# favicon y OG: cuadrado crema con el wordmark centrado
def square(size, scale=0.72):
    sq = Image.new('RGBA', (size, size), CREAM + (255,))
    lg = color.copy(); lg.thumbnail((int(size * scale), int(size * scale)))
    sq.alpha_composite(lg, ((size - lg.width) // 2, (size - lg.height) // 2 + int(size * 0.02)))
    return sq
square(512).save(os.path.join(OUT, 'favicon.png'))
og = Image.new('RGBA', (1200, 630), CREAM + (255,))
lg = color.copy(); lg.thumbnail((760, 400)); og.alpha_composite(lg, ((1200 - lg.width) // 2, (630 - lg.height) // 2))
og.convert('RGB').save(os.path.join(OUT, 'og.jpg'), quality=88)
print('logo', color.size)
