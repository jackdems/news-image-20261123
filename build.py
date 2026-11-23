# Draws the 23 November 2026 world-news front page (benchmark layout: example.jpg).
from PIL import Image, ImageDraw, ImageFont
import math, os

W = H = 1024
BG = (244, 241, 234); INK = (26, 26, 26); RED = (192, 38, 45); GREY = (95, 95, 95)
REG = {"Europe": (47, 93, 168), "Asia": (192, 38, 45), "Middle East": (199, 122, 18),
       "Africa": (46, 139, 62), "Americas": (110, 63, 163), "Global": (90, 95, 102)}
FD = "C:/Windows/Fonts/"
def F(name, size): return ImageFont.truetype(FD + name, size)
SERIF_B = lambda s: F("georgiab.ttf", s); SERIF_I = lambda s: F("georgiai.ttf", s)
SANS = lambda s: F("arial.ttf", s); SANS_B = lambda s: F("arialbd.ttf", s)

img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)

def tw(t, f): return d.textlength(t, font=f)
def wrap(t, f, width):
    out, cur = [], ""
    for w in t.split():
        test = (cur + " " + w).strip()
        if tw(test, f) <= width: cur = test
        else: out.append(cur); cur = w
    out.append(cur); return out
def text_block(x, y, t, f, width, fill=INK, lh=None):
    lh = lh or int(f.size * 1.18)
    for ln in wrap(t, f, width):
        d.text((x, y), ln, font=f, fill=fill); y += lh
    return y
def spaced(x, y, t, f, fill, sp=1.2):
    for ch in t:
        d.text((x, y), ch, font=f, fill=fill); x += tw(ch, f) + sp
    return x
def spaced_w(t, f, sp=1.2): return sum(tw(c, f) + sp for c in t)

M = 16
# ---- top utility line + masthead
spaced(M, 10, "THE WORLD IN ONE DAY", SANS_B(10), RED, 1.6)
r = "33 STORIES · 6 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER 2026"
spaced(W - M - spaced_w(r, SANS_B(9), 0.8), 11, r, SANS_B(9), INK, 0.8)
d.rectangle([M, 25, W - M, 27], fill=INK)
mf = SERIF_B(66); t = "Monday 23 November 2026"
d.text(((W - tw(t, mf)) / 2, 30), t, font=mf, fill=INK)
deck = "Nvidia brings back Jensen Huang · Ukraine says it sank a Russian warship in Libya · UN chief calls for global AI rules"
df = SERIF_I(13); d.text(((W - tw(deck, df)) / 2, 104), deck, font=df, fill=INK)
d.line([M, 124, W - M, 124], fill=INK, width=1)

# ---- stats strip
stats = [("11", "days: Huang out, then back"),
         ("7", "sea drones hit warship"),
         ("15", "killed near Kyiv"),
         ("258", "Democrat House seats"),
         ("24", "killed in South Sudan"),
         ("1,000+", "Delta flights delayed")]
sw = (W - 2 * M) / 6
for i, (n, c) in enumerate(stats):
    x = M + i * sw
    d.rectangle([x, 131, x + 3, 167], fill=RED)
    d.text((x + 9, 128), n, font=SERIF_B(21), fill=INK)
    text_block(x + 9, 152, c, SANS_B(11), sw - 14, INK, 12)

# ---- region bar
counts = [("Europe", 5), ("Middle East", 5), ("Africa", 5), ("Americas", 12), ("Asia", 5), ("Global", 1)]
tot = sum(c for _, c in counts); x = M; y0 = 178
MINW = 62; _tw = W - 2 * M; _big = sum(c for _, c in counts if _tw * c / tot >= MINW); _small = sum(1 for _, c in counts if _tw * c / tot < MINW)
for name, c in counts:
    w = MINW if _tw * c / tot < MINW else (_tw - MINW * _small) * c / _big
    d.rectangle([x, y0, x + w, y0 + 15], fill=REG[name])
    lab = f"{name} {c}"; f = SANS_B(9)
    if tw(lab, f) >= w - 4: lab = str(c)
    if tw(lab, f) < w - 2: d.text((x + (w - tw(lab, f)) / 2, y0 + 2), lab, font=f, fill="white")
    x += w

# ---- illustrations (flat shapes)
def label(x, y, t, chip=None):
    f = SANS_B(10); w = tw(t, f) + 12
    d.rectangle([x, y, x + w, y + 17], fill=RED); d.rectangle([x + 2, y + 2, x + w - 2, y + 15], outline="white")
    d.text((x + 6, y + 3), t, font=f, fill="white")
    if chip:
        f2 = SANS_B(9); w2 = tw(chip, f2) + 10
        d.rectangle([x, y + 20, x + w2, y + 34], fill="white"); d.text((x + 5, y + 22), chip, font=f2, fill=INK)
def tag(x0, y1, x1, t):
    f = SANS(8); w = tw(t, f) + 8
    d.rectangle([x1 - w, y1 - 13, x1, y1], fill=INK); d.text((x1 - w + 4, y1 - 12), t, font=f, fill="white")

def art(kind, box):
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; h = y1 - y0
    if kind == "chip":
        d.rectangle(box, fill=(18, 30, 52))
        for i in range(6):  # rising bars
            bx = x1 - 70 + i * 10; d.rectangle([bx, y1 - 12 - i * 7, bx + 6, y1 - 6], fill=(118, 185, 0))
        s = h * 0.32; d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(40, 52, 76), outline=(118, 185, 0), width=3)
        for k in range(5):
            o = -s + (k + 0.5) * 2 * s / 5
            for a, b in ((cx + o, cy - s), (cx + o, cy + s)):
                d.line([a, b, a, b + (-8 if b < cy else 8)], fill=(170, 170, 170), width=2)
            for a, b in ((cx - s, cy + o), (cx + s, cy + o)):
                d.line([a, b, a + (-8 if a < cx else 8), b], fill=(170, 170, 170), width=2)
        d.text((cx - tw("CEO", SANS_B(16)) / 2, cy - 10), "CEO", font=SANS_B(16), fill=(118, 185, 0))
    elif kind == "warship":
        d.rectangle(box, fill=(26, 52, 92)); d.rectangle([x0, cy + 8, x1, y1], fill=(36, 82, 130))
        # tilted capsizing hull
        pts = [(cx - 70, cy + 4), (cx + 60, cy - 14), (cx + 52, cy + 14), (cx - 62, cy + 26)]
        d.polygon(pts, fill=(110, 115, 122)); d.polygon([(cx - 20, cy - 4), (cx + 20, cy - 12), (cx + 18, cy - 30), (cx - 16, cy - 24)], fill=(130, 135, 142))
        for r_, c in ((30, (240, 120, 30)), (18, (255, 200, 60))):
            d.polygon([(cx + 10 + r_ * (1 if k % 2 == 0 else 0.5) * math.cos(math.radians(k * 30)), cy - 18 + r_ * (1 if k % 2 == 0 else 0.5) * math.sin(math.radians(k * 30))) for k in range(12)], fill=c)
        for i in range(3):  # drone wakes
            yy = y1 - 14 - i * 9; xx = x0 + 20 + i * 30
            d.line([xx, yy, xx + 40, yy - 4], fill="white", width=2); d.polygon([(xx + 40, yy - 7), (xx + 50, yy - 4), (xx + 40, yy - 1)], fill=(250, 210, 40))
    elif kind == "ai":
        d.rectangle(box, fill=(0, 158, 219)); d.rectangle([x0, y1 - 22, x1, y1], fill=(237, 220, 170))
        r_ = h * 0.30
        d.ellipse([cx - r_, cy - r_ - 6, cx + r_, cy + r_ - 6], outline="white", width=3)
        for k in range(-2, 3): d.arc([cx - r_ * abs(k) / 2.2, cy - r_ - 6, cx + r_ * abs(k) / 2.2, cy + r_ - 6], 0, 360, fill="white")
        d.line([cx - r_, cy - 6, cx + r_, cy - 6], fill="white", width=2)
        d.text((cx - tw("AI", SANS_B(22)) / 2, cy - 19), "AI", font=SANS_B(22), fill=(255, 220, 60))
        d.polygon([(x1 - 40, y1 - 22), (x1 - 30, y1 - 52), (x1 - 20, y1 - 22)], fill=(30, 120, 60))
    elif kind == "flag_ua":
        d.rectangle([x0, y0, x1, cy], fill=(0, 87, 183)); d.rectangle([x0, cy, x1, y1], fill=(255, 215, 0))
        d.rectangle([cx - 22, cy - 20, cx + 22, y1 - 6], fill=(80, 80, 80))
        for i in range(3):
            for j in range(3): d.rectangle([cx - 16 + i * 12, cy - 14 + j * 10, cx - 10 + i * 12, cy - 8 + j * 10], fill=(30, 30, 30))
    elif kind == "scroll":
        d.rectangle(box, fill=(242, 168, 0)); d.rectangle([x0, y0, x1, y0 + h / 3], fill=(217, 0, 18)); d.rectangle([x0, y0 + h / 3, x1, y0 + 2 * h / 3], fill=(0, 51, 160))
        d.rectangle([cx - 20, cy - 24, cx + 20, cy + 24], fill=(250, 245, 230), outline=INK)
        for k in range(5): d.line([cx - 14, cy - 16 + k * 8, cx + 14, cy - 16 + k * 8], fill=GREY)
    elif kind == "capitol":
        d.rectangle(box, fill=(30, 60, 140))
        d.rectangle([cx - 34, cy + 4, cx + 34, y1 - 8], fill="white"); d.pieslice([cx - 18, cy - 22, cx + 18, cy + 14], 180, 360, fill="white")
        d.rectangle([cx - 2, cy - 30, cx + 2, cy - 20], fill="white")
        for k in range(6): d.rectangle([cx - 30 + k * 12, cy + 8, cx - 26 + k * 12, y1 - 12], fill=(30, 60, 140))
    elif kind == "globe_cop":
        d.rectangle(box, fill=(200, 225, 190)); r_ = h * 0.3
        d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], fill=(60, 130, 200), outline=(30, 80, 140), width=2)
        d.polygon([(cx - r_ * .6, cy - r_ * .5), (cx - r_ * .1, cy - r_ * .7), (cx + r_ * .1, cy - r_ * .2), (cx - r_ * .3, cy + r_ * .5), (cx - r_ * .7, cy + r_ * .1)], fill=(70, 160, 80))
        d.polygon([(cx + r_ * .3, cy - r_ * .6), (cx + r_ * .8, cy - r_ * .3), (cx + r_ * .6, cy + r_ * .4), (cx + r_ * .3, cy + r_ * .1)], fill=(70, 160, 80))
        d.arc([cx - r_ * .45, cy - r_, cx + r_ * .45, cy + r_], 0, 360, fill=(200, 225, 245), width=1); d.line([cx - r_, cy, cx + r_, cy], fill=(200, 225, 245), width=1)
        d.rounded_rectangle([cx - 38, cy - 9, cx + 38, cy + 9], 3, fill="white", outline=RED, width=3)
        d.text((cx - d.textlength("NO DEAL", font=SANS_B(12)) / 2, cy - 8), "NO DEAL", font=SANS_B(12), fill=RED)
    elif kind == "virus":
        d.rectangle(box, fill=(250, 236, 200)); r_ = h * 0.2
        for a in range(0, 360, 30):
            ax, ay = cx + math.cos(math.radians(a)) * r_ * 1.5, cy + math.sin(math.radians(a)) * r_ * 1.5
            d.line([cx, cy, ax, ay], fill=(170, 40, 40), width=3); d.ellipse([ax - 4, ay - 4, ax + 4, ay + 4], fill=(170, 40, 40))
        d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], fill=(200, 60, 60))
    elif kind == "phone":
        d.rectangle(box, fill=(0, 106, 78)); d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(244, 42, 65))
        d.rounded_rectangle([cx - 14, cy - 24, cx + 14, cy + 24], 4, fill=INK); d.rectangle([cx - 10, cy - 18, cx + 10, cy + 16], fill=(200, 220, 240))
        d.line([cx - 22, cy - 28, cx + 22, cy + 28], fill="white", width=5)
    elif kind == "plane":
        d.rectangle(box, fill=(150, 200, 235))
        d.rounded_rectangle([cx - 44, cy - 5, cx + 40, cy + 5], 5, fill="white"); d.ellipse([cx + 30, cy - 5, cx + 50, cy + 5], fill="white")
        d.polygon([(cx + 4, cy - 3), (cx - 14, cy - 34), (cx - 6, cy - 34), (cx + 20, cy - 3)], fill="white")
        d.polygon([(cx + 4, cy + 3), (cx - 14, cy + 34), (cx - 6, cy + 34), (cx + 20, cy + 3)], fill="white")
        d.polygon([(cx - 40, cy - 3), (cx - 50, cy - 16), (cx - 44, cy - 16), (cx - 32, cy - 3)], fill="white")
        d.polygon([(cx - 40, cy + 3), (cx - 50, cy + 16), (cx - 44, cy + 16), (cx - 32, cy + 3)], fill="white")
        d.text((x0 + 8, y1 - 24), "ON TIME", font=SANS_B(11), fill=(20, 120, 50))
    elif kind == "market":
        d.rectangle(box, fill=(20, 24, 30)); pts = []
        vals = [8, 6, 9, 4, 3, 2, 5, 9, 14]
        for i, v in enumerate(vals): pts.append((x0 + 10 + i * (x1 - x0 - 20) / 8, y1 - 12 - v * (h - 30) / 16))
        d.line(pts, fill=(60, 200, 90), width=3)
        d.text((x0 + 6, y0 + 22), "NASDAQ FUT +3.6%", font=SANS_B(9), fill=(60, 200, 90))
    elif kind == "sudan":
        d.rectangle([x0, y0, x1, y0 + h / 3], fill=INK); d.rectangle([x0, y0 + h / 3, x1, y0 + 2 * h / 3], fill=(218, 18, 26)); d.rectangle([x0, y0 + 2 * h / 3, x1, y1], fill=(7, 137, 48))
        for yy in (y0 + h / 3, y0 + 2 * h / 3): d.rectangle([x0, yy - 3, x1, yy + 3], fill="white")
        d.polygon([(x0, y0), (x0 + h * 0.55, cy), (x0, y1)], fill=(15, 71, 175))
        sx, sy, R = x0 + h * 0.2, cy, h * 0.11
        d.polygon([(sx + (R if k % 2 == 0 else R * 0.4) * math.cos(math.radians(-90 + k * 36)), sy + (R if k % 2 == 0 else R * 0.4) * math.sin(math.radians(-90 + k * 36))) for k in range(10)], fill=(252, 221, 9))
    elif kind == "fire":
        d.rectangle(box, fill=(60, 50, 60)); d.rectangle([x0, y1 - 18, x1, y1], fill=(90, 80, 70))
        for k in range(4): d.rectangle([cx - 40 + k * 22, cy - 6 - k * 3, cx - 28 + k * 22, y1 - 18], fill=(120, 120, 120))
        for sx_, sy_, sr in ((-22, -34, 14), (6, -40, 17), (30, -32, 13)): d.ellipse([cx + sx_ - sr, cy + sy_ - sr, cx + sx_ + sr, cy + sy_ + sr], fill=(160, 155, 160))
        for r_, c in ((40, (220, 60, 30)), (30, (245, 130, 30)), (17, (255, 215, 80))):
            d.polygon([(cx + 4 + r_ * (1 if k % 2 == 0 else 0.5) * math.cos(math.radians(k * 20)), cy - 4 + r_ * 0.8 * (1 if k % 2 == 0 else 0.5) * math.sin(math.radians(k * 20))) for k in range(18)], fill=c)


# ---- richer illustrations (override): gradient skies, shading, detail
def _mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def grad(box, c1, c2):
    x0, y0, x1, y1 = box; n = max(1, int(y1 - y0))
    for i in range(n): d.line([x0, y0 + i, x1, y0 + i], fill=_mix(c1, c2, i / n), width=1)
def star(cx, cy, R, r, k, fill, rot=-90):
    d.polygon([(cx + (R if j % 2 == 0 else r) * math.cos(math.radians(rot + j * 180 / k)), cy + (R if j % 2 == 0 else r) * math.sin(math.radians(rot + j * 180 / k))) for j in range(2 * k)], fill=fill)
def blast(cx, cy, s):
    for R, c in ((1.0, (200, 50, 20)), (0.75, (245, 130, 30)), (0.45, (255, 220, 90)), (0.2, (255, 250, 220))):
        star(cx, cy, 34 * s * R, 18 * s * R, 9, c, rot=-80)
_art_old = art
def art(kind, box):
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; h = y1 - y0; w = x1 - x0
    if kind == "chip":
        grad(box, (10, 18, 36), (30, 48, 80))
        for i in range(0, int(w), 14): d.line([x0 + i, y0, x0 + i, y1], fill=(24, 38, 62), width=1)
        for k in range(7):
            yy = y0 + 10 + k * h / 7; d.line([x0, yy, cx - 50, yy], fill=(118, 185, 0), width=1); d.ellipse([cx - 53, yy - 3, cx - 47, yy + 3], fill=(118, 185, 0))
        pts = [(x1 - 90 + i * 12, y1 - 14 - v) for i, v in enumerate([6, 14, 9, 22, 30, 44, 58])]
        d.polygon(pts + [(pts[-1][0], y1 - 8), (pts[0][0], y1 - 8)], fill=(60, 110, 20)); d.line(pts, fill=(160, 230, 40), width=3)
        s_ = h * 0.30
        d.rounded_rectangle([cx - s_ + 4, cy - s_ + 6, cx + s_ + 4, cy + s_ + 6], 6, fill=(5, 10, 20))
        for k in range(6):
            o = -s_ + (k + 0.5) * 2 * s_ / 6
            d.line([cx + o, cy - s_ - 9, cx + o, cy + s_ + 9], fill=(200, 175, 90), width=2)
            d.line([cx - s_ - 9, cy + o, cx + s_ + 9, cy + o], fill=(200, 175, 90), width=2)
        d.rounded_rectangle([cx - s_, cy - s_, cx + s_, cy + s_], 6, fill=(44, 58, 84), outline=(118, 185, 0), width=3)
        d.rounded_rectangle([cx - s_ + 7, cy - s_ + 7, cx + s_ - 7, cy + s_ - 7], 4, fill=(32, 44, 66))
        d.polygon([(cx - 18, cy - 4), (cx - 18, cy - 20), (cx - 9, cy - 11), (cx, cy - 24), (cx + 9, cy - 11), (cx + 18, cy - 20), (cx + 18, cy - 4)], fill=(250, 200, 40))
        d.text((cx - tw("CEO", SANS_B(15)) / 2, cy), "CEO", font=SANS_B(15), fill=(160, 230, 40))
    elif kind == "warship":
        grad([x0, y0, x1, cy + 8], (250, 150, 80), (120, 70, 110)); grad([x0, cy + 8, x1, y1], (30, 60, 100), (10, 25, 50))
        d.ellipse([x1 - 60, y0 + 8, x1 - 34, y0 + 34], fill=(255, 225, 150))
        for k in range(4): d.polygon([(x0 + k * 46, cy + 8), (x0 + 20 + k * 46, cy - 2 - k % 2 * 5), (x0 + 44 + k * 46, cy + 8)], fill=(110, 70, 90))
        for k in range(6): d.line([x0 + k * 55, cy + 16 + k % 3 * 9, x0 + 30 + k * 55, cy + 16 + k % 3 * 9], fill=(70, 110, 160), width=1)
        d.polygon([(cx - 70, cy + 4), (cx + 62, cy - 16), (cx + 54, cy + 14), (cx - 60, cy + 26)], fill=(85, 90, 100))
        d.polygon([(cx - 70, cy + 4), (cx + 62, cy - 16), (cx + 60, cy - 10), (cx - 68, cy + 10)], fill=(140, 145, 155))
        d.polygon([(cx - 24, cy - 2), (cx + 22, cy - 10), (cx + 20, cy - 30), (cx - 20, cy - 24)], fill=(120, 125, 135))
        d.line([cx, cy - 27, cx - 3, cy - 46], fill=(60, 60, 70), width=2)
        for sx_, sy_, sr in ((-6, -50, 10), (6, -60, 13), (20, -68, 15)): d.ellipse([cx + sx_ - sr, cy + sy_ - sr, cx + sx_ + sr, cy + sy_ + sr], fill=(70, 60, 70))
        blast(cx + 30, cy - 10, 0.8)
        for i in range(3):
            yy = y1 - 12 - i * 10; xx = x0 + 44 + i * 34
            d.polygon([(xx - 30, yy + 3), (xx, yy - 1), (xx, yy + 2)], fill=(200, 225, 245)); d.polygon([(xx, yy - 4), (xx + 16, yy - 1), (xx, yy + 3)], fill=(250, 210, 40))
    elif kind == "ai":
        grad(box, (0, 120, 200), (120, 210, 240)); grad([x0, y1 - 24, x1, y1], (60, 170, 200), (20, 110, 160))
        d.ellipse([x0 + 20, y1 - 30, x0 + 140, y1 - 4], fill=(237, 220, 170))
        for px_ in (x0 + 40, x1 - 40):
            d.line([px_, y1 - 18, px_ + 6, y1 - 58], fill=(110, 80, 40), width=3)
            for a in (-150, -110, -60, -20): d.line([px_ + 6, y1 - 58, px_ + 6 + 22 * math.cos(math.radians(a)), y1 - 58 + 12 * math.sin(math.radians(a)) + 8], fill=(30, 130, 60), width=4)
        r_ = h * 0.30; gx_, gy_ = cx, cy - 8
        d.ellipse([gx_ - r_ - 6, gy_ - r_ - 6, gx_ + r_ + 6, gy_ + r_ + 6], fill=(255, 255, 255))
        d.ellipse([gx_ - r_, gy_ - r_, gx_ + r_, gy_ + r_], fill=(0, 158, 219))
        for k in range(1, 3): d.ellipse([gx_ - r_ * k / 3, gy_ - r_, gx_ + r_ * k / 3, gy_ + r_], outline="white", width=1)
        for k in (-0.5, 0, 0.5): d.line([gx_ - r_ * math.cos(math.asin(k)), gy_ + r_ * k, gx_ + r_ * math.cos(math.asin(k)), gy_ + r_ * k], fill="white", width=1)
        for a in range(0, 360, 45):
            ax, ay = gx_ + (r_ + 14) * math.cos(math.radians(a)), gy_ + (r_ + 14) * math.sin(math.radians(a))
            d.line([gx_ + r_ * math.cos(math.radians(a)), gy_ + r_ * math.sin(math.radians(a)), ax, ay], fill=(255, 220, 60), width=2); d.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=(255, 220, 60))
        d.rounded_rectangle([gx_ - 17, gy_ - 13, gx_ + 17, gy_ + 13], 4, fill=(10, 40, 80))
        d.text((gx_ - tw("AI", SANS_B(20)) / 2, gy_ - 12), "AI", font=SANS_B(20), fill=(255, 220, 60))
    elif kind == "flag_ua":
        grad([x0, y0, x1, cy], (0, 70, 160), (0, 100, 200)); grad([x0, cy, x1, y1], (255, 225, 40), (230, 180, 0))
        for k, (bh, bw_) in enumerate(((42, 26), (30, 22), (50, 30))):
            bx_ = cx - 66 + k * 34; d.rectangle([bx_, y1 - 6 - bh, bx_ + bw_, y1 - 6], fill=(70, 70, 75))
            for i in range(2):
                for j in range(bh // 11): d.rectangle([bx_ + 4 + i * (bw_ / 2), y1 - bh + j * 11, bx_ + 9 + i * (bw_ / 2), y1 - bh + 5 + j * 11], fill=(250, 200, 80) if (i + j + k) % 3 else (25, 25, 25))
        for sx_, sy_, sr in ((24, -70, 9), (34, -80, 12), (46, -86, 10)): d.ellipse([cx + sx_ - sr, y1 + sy_ - sr, cx + sx_ + sr, y1 + sy_ + sr], fill=(90, 90, 95))
        star(cx + 30, y1 - 58, 8, 4, 6, (240, 100, 30))
    elif kind == "scroll":
        d.rectangle([x0, y0, x1, y0 + h / 3], fill=(217, 0, 18)); d.rectangle([x0, y0 + h / 3, x1, y0 + 2 * h / 3], fill=(0, 51, 160)); d.rectangle([x0, y0 + 2 * h / 3, x1, y1], fill=(242, 168, 0))
        d.polygon([(cx - 24, cy - 26), (cx + 26, cy - 24), (cx + 22, cy + 30), (cx - 28, cy + 28)], fill=(60, 40, 20))
        d.rectangle([cx - 24, cy - 28, cx + 24, cy + 26], fill=(250, 245, 228), outline=(120, 90, 50))
        for e in (cy - 30, cy + 24): d.rounded_rectangle([cx - 30, e, cx + 30, e + 6], 3, fill=(190, 150, 90))
        for k in range(5): d.line([cx - 16, cy - 18 + k * 7, cx + 16 - (k == 4) * 10, cy - 18 + k * 7], fill=GREY, width=1)
        d.line([cx + 12, cy + 18, cx + 34, cy - 10], fill=(40, 40, 40), width=3); d.polygon([(cx + 10, cy + 22), (cx + 11, cy + 15), (cx + 15, cy + 18)], fill=INK)
    elif kind == "capitol":
        grad(box, (20, 40, 110), (90, 120, 190))
        for k in range(12): star(x0 + 10 + (k * 17) % (w - 10), y0 + 8 + (k * 7) % 22, 3, 1.3, 5, (255, 255, 255))
        d.rectangle([x0, y1 - 8, x1, y1], fill=(60, 120, 60))
        d.rectangle([cx - 46, cy + 12, cx + 46, y1 - 8], fill=(240, 238, 230)); d.polygon([(cx - 50, cy + 12), (cx, cy + 2), (cx + 50, cy + 12)], fill=(250, 250, 245))
        d.rectangle([cx - 20, cy - 6, cx + 20, cy + 4], fill=(240, 238, 230)); d.pieslice([cx - 20, cy - 30, cx + 20, cy + 10], 180, 360, fill="white")
        d.rectangle([cx - 2, cy - 38, cx + 2, cy - 28], fill="white"); d.ellipse([cx - 3, cy - 42, cx + 3, cy - 36], fill="white")
        for k in range(8): d.rectangle([cx - 40 + k * 11, cy + 16, cx - 37 + k * 11, y1 - 10], fill=(170, 170, 180))
    elif kind == "globe_cop":
        grad(box, (150, 200, 160), (70, 120, 90)); r_ = h * 0.36
        d.ellipse([cx - r_ + 3, cy - r_ + 5, cx + r_ + 3, cy + r_ + 5], fill=(80, 110, 80))
        d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], fill=(50, 120, 200))
        d.polygon([(cx - r_ * .6, cy - r_ * .5), (cx - r_ * .1, cy - r_ * .75), (cx + r_ * .1, cy - r_ * .2), (cx - r_ * .3, cy + r_ * .6), (cx - r_ * .75, cy + r_ * .1)], fill=(70, 160, 80))
        d.polygon([(cx + r_ * .3, cy - r_ * .6), (cx + r_ * .85, cy - r_ * .3), (cx + r_ * .6, cy + r_ * .45), (cx + r_ * .3, cy + r_ * .1)], fill=(70, 160, 80))
        for k in range(3): d.line([cx + r_ + 4, cy - 10 + k * 8, cx + r_ + 14 + k * 3, cy - 14 + k * 8], fill=(220, 70, 40), width=2)
        d.rounded_rectangle([cx - 40, cy + r_ - 14, cx + 40, cy + r_ + 6], 3, fill="white", outline=RED, width=3)
        d.text((cx - tw("NO DEAL", SANS_B(12)) / 2, cy + r_ - 12), "NO DEAL", font=SANS_B(12), fill=RED)
    elif kind == "virus":
        grad(box, (255, 244, 215), (240, 210, 170)); r_ = h * 0.2
        for ox_, oy_, sc in ((-w * .32, -h * .2, .4), (w * .33, h * .18, .35)):
            d.ellipse([cx + ox_ - r_ * sc, cy + oy_ - r_ * sc, cx + ox_ + r_ * sc, cy + oy_ + r_ * sc], fill=(225, 140, 130))
        for a in range(0, 360, 30):
            ax, ay = cx + math.cos(math.radians(a)) * r_ * 1.55, cy + math.sin(math.radians(a)) * r_ * 1.55
            d.line([cx, cy, ax, ay], fill=(150, 30, 30), width=3); d.ellipse([ax - 5, ay - 5, ax + 5, ay + 5], fill=(150, 30, 30))
        d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], fill=(200, 60, 60)); d.ellipse([cx - r_ * .7, cy - r_ * .7, cx, cy], fill=(225, 100, 95))
        d.rounded_rectangle([x0 + 8, y1 - 22, x0 + 30, y1 - 6], 3, fill="white", outline=RED, width=2); d.rectangle([x0 + 17, y1 - 20, x0 + 21, y1 - 8], fill=RED); d.rectangle([x0 + 13, y1 - 16, x0 + 25, y1 - 12], fill=RED)
    elif kind == "phone":
        grad(box, (0, 120, 90), (0, 80, 60)); d.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], fill=(244, 42, 65))
        d.rounded_rectangle([cx - 14, cy - 24, cx + 14, cy + 22], 5, fill=INK)
        d.rectangle([cx - 11, cy - 19, cx + 11, cy + 17], fill=(210, 230, 250))
        for k, c in enumerate(((240, 80, 120), (60, 140, 240), (250, 190, 40), (90, 200, 120))): d.rounded_rectangle([cx - 10 + (k % 2) * 11, cy - 17 + (k // 2) * 11, cx - 2 + (k % 2) * 11, cy - 9 + (k // 2) * 11], 2, fill=c)
        d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], outline="white", width=5); d.line([cx - 29, cy - 29, cx + 29, cy + 29], fill="white", width=5)
    elif kind == "plane":
        grad(box, (110, 170, 225), (200, 230, 250))
        for ox_, oy_ in ((-60, -20), (55, 22)):
            for a, b in ((-10, 2), (0, -3), (12, 2)): d.ellipse([cx + ox_ + a - 12, cy + oy_ - 7 + b, cx + ox_ + a + 12, cy + oy_ + 7 + b], fill="white")
        d.polygon([(cx + 4, cy - 4), (cx - 16, cy - 36), (cx - 6, cy - 36), (cx + 22, cy - 4)], fill=(235, 240, 248))
        d.polygon([(cx + 4, cy + 4), (cx - 16, cy + 36), (cx - 6, cy + 36), (cx + 22, cy + 4)], fill=(215, 222, 232))
        d.polygon([(cx - 40, cy - 4), (cx - 52, cy - 20), (cx - 44, cy - 20), (cx - 32, cy - 4)], fill=(200, 60, 60))
        d.rounded_rectangle([cx - 44, cy - 6, cx + 40, cy + 6], 6, fill="white"); d.ellipse([cx + 30, cy - 6, cx + 52, cy + 6], fill="white")
        d.line([cx - 36, cy + 3, cx + 46, cy + 3], fill=(200, 60, 60), width=2)
        for k in range(7): d.ellipse([cx - 26 + k * 9, cy - 3, cx - 23 + k * 9, cy], fill=(60, 90, 140))
        d.rounded_rectangle([x1 - 74, y0 + 6, x1 - 6, y0 + 22], 3, fill=(20, 120, 50)); d.text((x1 - 68, y0 + 7), "ON TIME", font=SANS_B(11), fill="white")
    elif kind == "market":
        grad(box, (16, 20, 28), (30, 36, 48))
        for k in range(1, 4): d.line([x0, y0 + k * h / 4, x1, y0 + k * h / 4], fill=(45, 52, 66), width=1)
        vals = [8, 6, 9, 4, 3, 2, 5, 9, 14]; step = (w - 24) / 8
        for i, v in enumerate(vals):
            xx = x0 + 12 + i * step; top = y1 - 14 - v * 3.2; bot = top + 10 + (i % 3) * 4; up = i == 0 or v >= vals[i - 1]
            c = (60, 200, 90) if up else (220, 70, 70); d.line([xx, top - 5, xx, bot + 5], fill=c, width=1); d.rectangle([xx - 4, top, xx + 4, bot], fill=c)
        d.text((x0 + 6, y0 + 22), "NASDAQ FUT +3.6%", font=SANS_B(9), fill=(60, 200, 90))
    elif kind == "sudan":
        _art_old(kind, box)
        d.rectangle([x0, y1 - 20, x1, y1], fill=(120, 70, 40))
        for k in range(3):
            hx = x0 + 70 + k * 30; d.rectangle([hx - 10, y1 - 30, hx + 10, y1 - 14], fill=(200, 170, 120)); d.polygon([(hx - 14, y1 - 30), (hx, y1 - 44), (hx + 14, y1 - 30)], fill=(150, 110, 60))
    elif kind == "fire":
        grad(box, (40, 30, 50), (110, 60, 50)); d.rectangle([x0, y1 - 18, x1, y1], fill=(80, 70, 60))
        for k in range(5):
            d.rectangle([cx - 50 + k * 20, cy - 4 - (k % 3) * 6, cx - 36 + k * 20, y1 - 18], fill=(130, 130, 135))
        for sx_, sy_, sr in ((-26, -34, 14), (4, -42, 18), (30, -34, 14)): d.ellipse([cx + sx_ - sr, cy + sy_ - sr, cx + sx_ + sr, cy + sy_ + sr], fill=(120, 110, 115))
        blast(cx + 4, cy - 2, 0.9)
        fx, fy = x1 - 52, y0 + 8; d.rectangle([fx - 1, fy - 1, fx + 45, fy + 27], fill=INK); d.rectangle([fx, fy, fx + 44, fy + 26], fill=(206, 17, 38))
        d.polygon([(fx, fy)] + [(fx + (12 if j % 2 == 0 else 20), fy + j * 26 / 10) for j in range(11)] + [(fx, fy + 26)], fill="white")
    else:
        _art_old(kind, box)

# ---- card helper
SS = 4  # supersample factor: illustrations drawn at 4x, downsampled -> smooth anti-aliased vector look
class SD:
    def __init__(s, base, ox, oy): s.base, s.ox, s.oy = base, ox, oy; s.dr = None
    def textlength(s, t, font=None): return s.base.textlength(t, font=font)
    def _cv(s, a):
        flat = []
        def walk(v):
            if isinstance(v, (int, float)): flat.append(v)
            else:
                for e in v: walk(e)
        walk(a)
        return [((flat[i] - s.ox) * SS, (flat[i + 1] - s.oy) * SS) for i in range(0, len(flat), 2)]
    def __getattr__(s, name):
        fn = getattr(s.dr, name)
        def call(*args, **kw):
            args = list(args)
            if name == "text":
                args[0] = s._cv(args[0])[0]
                if kw.get("font") is not None: kw["font"] = ImageFont.truetype(kw["font"].path, int(kw["font"].size * SS))
            else:
                pts = s._cv(args[0])
                if name in ("rectangle", "ellipse", "arc", "pieslice", "rounded_rectangle"):
                    (a, b), (c, e) = pts; pts = [min(a, c), min(b, e), max(a, c), max(b, e)]
                args[0] = pts
                if name == "rounded_rectangle" and len(args) > 1: args[1] *= SS
                if "radius" in kw: kw["radius"] *= SS
            if "width" in kw: kw["width"] = max(1, int(kw["width"] * SS))
            return fn(*args, **kw)
        return call
def art_hq(kind, box):
    global d
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    tmp = Image.new("RGB", ((x1 - x0) * SS, (y1 - y0) * SS), BG)
    base = d; p = SD(base, x0, y0); p.dr = ImageDraw.Draw(tmp); d = p
    try: art(kind, (x0, y0, x1, y1))
    finally: d = base
    img.paste(tmp.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))

def card(x, y, w, ih, n, region, kicker, head, body, kind, lab, src, chip=None, hf=19, lead=False):
    art_hq(kind, (x, y, x + w, y + ih)); label(x + 6, y + 6, lab, chip); tag(x, y + ih, x + w, src)
    yy = y + ih + 6; c = REG[region]
    d.ellipse([x, yy, x + 15, yy + 15], fill=c); f = SANS_B(8 if n < 10 else 7)
    d.text((x + 7.5 - tw(str(n), f) / 2, yy + 3), str(n), font=f, fill="white")
    spaced(x + 20, yy + 3, kicker, SANS_B(8), c, 0.7)
    yy = text_block(x, yy + 19, head, SERIF_B(hf), w, INK, int(hf * 1.12))
    text_block(x, yy + 2, body, SANS(10 if lead else 9), w, (55, 55, 55), 12 if lead else 11)

leads = [
    (1, "Americas", "SANTA CLARA, US · BUSINESS", "Nvidia reinstates Jensen Huang as chief executive",
     "Board vote unanimous, 11 days after he quit over a scandal; it says US officials saw no security risk. Shares jumped. (Nvidia, CNN)",
     "chip", "NVIDIA: HUANG BACK", "Effective immediately", "Statement · Nvidia"),
    (2, "Africa", "BENGHAZI, LIBYA · WAR", "Zelensky: sea drones sank Russian warship in Libya",
     "Seven Ukrainian naval drones hit the corvette Merkury at Benghazi on Sunday, he said; Libya says a cargo ship was hit too. (AP, AFP)",
     "warship", "LIBYA: CORVETTE HIT", "Kyiv claims it Monday", "Ukraine's claim · AP"),
    (3, "Americas", "BRIDGETOWN, BARBADOS · TECHNOLOGY", "UN chief calls for global AI risk framework",
     "At the Bridgetown AI safety summit, Guterres asked states to start talks, warning of \"the biggest transfer of power\" in history. (UN News)",
     "ai", "BARBADOS: AI SUMMIT", "UN · Barbados co-host", "UN News"),
]
gx = M; gw = (W - 2 * M - 2 * 14) / 3; y = 202
for i, L in enumerate(leads):
    n, rg, k, hd, bd, kind, lab, chip, src = L
    card(M + i * (gw + 14), y, gw, 118, n, rg, k, hd, bd, kind, lab, src, chip, 18, True)

sec = [
    (4, "Europe", "DYMER · WAR", "Russian strikes kill 15 around Kyiv", "Flats collapse in Dymer; day of mourning.", "flag_ua", "KYIV REGION: 15", "Officials · AFP"),
    (5, "Europe", "YEREVAN · POLITICS", "Armenia publishes draft new constitution", "Pashinyan ties it to Azerbaijan peace.", "scroll", "ARMENIA: CHARTER", "PM's office"),
    (6, "Americas", "WASHINGTON · ELECTIONS", "Democrats hit 258 House seats", "Largest majority since 1992.", "capitol", "US HOUSE: 258", "Projections · AP"),
    (7, "Middle East", "ANTALYA · CLIMATE", "Fallout as COP31 ends with no deal", "First failed cover decision in 17 years.", "globe_cop", "COP31: NO DEAL", "Yale E360 · AP"),
    (8, "Africa", "ITURI, DR CONGO · HEALTH", "Fighting disrupts Ebola response", "WHO: teams trapped near a hospital.", "virus", "CONGO: EBOLA", "WHO · Reuters"),
    (9, "Asia", "DHAKA · TECHNOLOGY", "Court orders social media curbs for under-16s", "Expert panel to study feeds.", "phone", "BANGLADESH: <16", "Court order · PTI"),
    (10, "Americas", "ATLANTA · AVIATION", "Delta stable after glitch delayed 1,000+ flights", "Weight system fixed before Thanksgiving.", "plane", "DELTA: RESTORED", "Airline · AP"),
    (11, "Americas", "NEW YORK · MARKETS", "Tech leads Wall Street rebound", "Futures up after last week's sell-off.", "market", "WALL ST: REBOUND", "Markets · AP"),
    (12, "Africa", "WARRAP, S. SUDAN · CONFLICT", "Attack kills 24 civilians", "Officials blame SPLA-IO fighters.", "sudan", "S. SUDAN: 24", "Officials · AFP"),
    (13, "Middle East", "MANAMA · WAR", "Bahrain: 2 hurt in Iranian strike", "Gulf states condemn hit on Sitra site.", "fire", "BAHRAIN: STRIKE", "Ministry · AFP"),
]
cw = (W - 2 * M - 4 * 12) / 5
y = 432
for i, S in enumerate(sec):
    r_, c_ = divmod(i, 5)
    n, rg, k, hd, bd, kind, lab, src = S
    card(M + c_ * (cw + 12), y + r_ * 182, cw, 84, n, rg, k, hd, bd, kind, lab, src, None, 13)

# ---- bottom: map + briefs
by = 808; d.line([M, by - 4, W - M, by - 4], fill=INK, width=1)
spaced(M, by, "WHERE IT HAPPENED", SANS_B(9), INK, 1)
mx0, my0, mx1, my1 = M, by + 14, M + 290, by + 140
d.rectangle([mx0, my0, mx1, my1], fill=(28, 48, 84))
def P(lon, lat): return (mx0 + (lon + 180) / 360 * (mx1 - mx0), my0 + (80 - lat) / 140 * (my1 - my0))
LAND = (214, 196, 160)
import json as _json, os as _os
_gj = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "ne110.geojson"), encoding="utf-8"))
def _clamp(pt):
    x, y = P(*pt[:2]); return (min(max(x, mx0), mx1), min(max(y, my0), my1))
for _ft in _gj["features"]:
    _g = _ft.get("geometry") or {}
    _polys = [_g["coordinates"]] if _g.get("type") == "Polygon" else _g.get("coordinates", []) if _g.get("type") == "MultiPolygon" else []
    for _pl in _polys:
        _ring = _pl[0]
        if max(p[1] for p in _ring) < -60 or len(_ring) < 3: continue
        d.polygon([_clamp(p) for p in _ring], fill=LAND, outline=(180, 162, 128))
pins = [(1, -122, 37, "Americas"), (2, 20, 32, "Africa"), (3, -59.6, 13, "Americas"), (4, 30.5, 50.8, "Europe"), (5, 44.5, 40.2, "Europe"),
        (6, -77, 38.9, "Americas"), (7, 30.7, 36.9, "Middle East"), (8, 30, 1.5, "Africa"), (9, 90.4, 23.8, "Asia"), (10, -84.4, 33.7, "Americas"),
        (11, -74, 40.7, "Americas"), (12, 28.5, 8.2, "Africa"), (13, 50.6, 26.2, "Middle East")]
OFF = {6: (16, 8), 10: (-12, 10), 11: (14, -10), 1: (-4, 0), 3: (8, 6), 8: (9, 6), 12: (-14, 2),
       2: (-12, -8), 7: (2, 9), 4: (-9, -8), 5: (9, -8), 13: (12, 4), 9: (0, 0)}
for n, lo, la, rg in pins:
    tx, ty = P(lo, la); ox, oy = OFF.get(n, (0, 0))
    px, py = min(max(tx + ox, mx0 + 8), mx1 - 8), min(max(ty + oy, my0 + 8), my1 - 8)
    if (ox, oy) != (0, 0):
        d.line([tx, ty, px, py], fill="white", width=1); d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill="white")
for n, lo, la, rg in pins:
    tx, ty = P(lo, la); ox, oy = OFF.get(n, (0, 0))
    px, py = min(max(tx + ox, mx0 + 8), mx1 - 8), min(max(ty + oy, my0 + 8), my1 - 8)
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=REG[rg], outline="white")
    f = SANS_B(12 if n < 10 else 10); s = str(n)
    bb = d.textbbox((0, 0), s, font=f); d.text((px - (bb[0] + bb[2]) / 2, py - (bb[1] + bb[3]) / 2), s, font=f, fill="white")
d.text((M, my1 + 3), "Pins show stories 1-13; white lines mark exact spots.", font=SANS(8), fill=GREY)

bx = M + 306
spaced(bx, by, "ALSO ON MONDAY 23 NOVEMBER 2026 — 20 MORE STORIES", SANS_B(9), INK, 1)
briefs = [
    (14, "Middle East", "Benghazi", "UN mission urges probe into port attacks", "UN"),
    (15, "Europe", "Kyiv", "Drone debris sets fire in city centre; 5 hurt", "Kyiv Indep."),
    (16, "Europe", "Warsaw", "Poland: Russia twice plotted to kill rapper", "AP"),
    (17, "Asia", "Jakarta", "6 police officials named treason suspects", "AP"),
    (18, "Asia", "Bangkok", "Court upholds MP's royal defamation verdict", "AP"),
    (19, "Asia", "Kathmandu", "India and Nepal sign 8 agreements", "Bus. Standard"),
    (20, "Asia", "Kabul", "Taliban patrols target illegal logging", "AP"),
    (21, "Middle East", "Tehran", "Iran warns of retaliation if US attacks", "AP"),
    (22, "Americas", "Washington", "Trump: Iran strikes may resume next year", "Bus. Standard"),
    (23, "Americas", "Washington", "China opposes US phone-number ban", "Reuters"),
    (24, "Americas", "Havana", "WHO chief visits Cuba's failing hospitals", "AP"),
    (25, "Americas", "Iowa", "Army to detonate bomb-making chemicals", "AP"),
    (26, "Americas", "Seattle", "ICE detains father and daughter at airport", "AP"),
    (27, "Americas", "Washington", "Trump hosts gala for his sinking meme coin", "Reuters"),
    (28, "Middle East", "Gaza", "Study finds war caused environmental ruin", "AP"),
    (29, "Europe", "London", "Don Toliver postpones show after evacuation", "AP"),
    (30, "Global", "Markets", "S&P 500 still 11.6% below October peak", "Reuters"),
    (31, "Africa", "Canary route", "Effort to identify Atlantic migrant dead", "AP"),
    (32, "Americas", "Denver", "Broncos star Tom Jackson dies at 75", "AP"),
    (33, "Asia", "Hindu Kush", "El Niño flood and landslide risk flagged", "ICIMOD"),
]
colw = (W - M - bx - 12) / 2
for i, (n, rg, pl, s, src) in enumerate(briefs):
    c_, r_ = divmod(i, 10); xx = bx + c_ * (colw + 12); yy = by + 15 + r_ * 14.2
    d.text((xx, yy), str(n), font=SANS_B(11), fill=REG[rg]); xx2 = xx + 18
    d.text((xx2, yy), pl, font=SANS_B(11), fill=INK); xx2 += tw(pl, SANS_B(11)) + 4
    d.text((xx2, yy), s, font=SANS(11), fill=INK); xx2 += tw(s, SANS(11)) + 3
    if xx2 + tw(f"({src})", SANS(8)) < xx + colw: d.text((xx2, yy + 1), f"({src})", font=SANS(8), fill=GREY)

# ---- date check + footer
dy = 966
d.rectangle([M, dy, W - M, dy + 34], fill=BG, outline=RED, width=1)
x = spaced(M + 6, dy + 5, "DATE CHECK", SANS_B(9), RED, 0.8) + 6
text_block(x, dy + 4, "Sunday's events shown (Merkury, Dymer, COP31's end, Delta, Warrap, Bahrain) were confirmed, claimed or first fully reported on Monday 23 November, "
           "as attributed. Left out as older news: Huang's 12 Nov resignation, El Chapo Isidro's capture (21 Nov), the Canadian roast dinner (21 Nov).",
           SANS(9), W - M - 6 - x, INK, 11)
d.text((M, 1006), "Every story here happened, or was first reported, on Monday 23 November 2026. Officials' counts and claims are attributed.", font=SANS(8), fill=GREY)
r = "Sources named beside each story · original drawings"; d.text((W - M - tw(r, SANS(8)), 1006), r, font=SANS(8), fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry", "entry.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, optimize=True)
print(out, os.path.getsize(out))
