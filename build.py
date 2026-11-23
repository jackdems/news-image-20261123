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
stats = [("11", "days from Huang quitting Nvidia to his reinstatement"),
         ("7", "Ukrainian sea drones sent against the corvette Merkury"),
         ("15", "killed by Russian strikes in Kyiv region, officials say"),
         ("258", "House seats now won by Democrats, most since 1992"),
         ("24", "civilians killed in South Sudan attack, officials say"),
         ("1,000+", "Delta flights delayed by a weight-system glitch")]
sw = (W - 2 * M) / 6
for i, (n, c) in enumerate(stats):
    x = M + i * sw
    d.rectangle([x, 131, x + 3, 167], fill=RED)
    d.text((x + 9, 128), n, font=SERIF_B(21), fill=INK)
    text_block(x + 9, 153, c, SANS(8), sw - 16, GREY, 9)

# ---- region bar
counts = [("Europe", 5), ("Middle East", 5), ("Africa", 5), ("Americas", 12), ("Asia", 5), ("Global", 1)]
tot = sum(c for _, c in counts); x = M; y0 = 178
for name, c in counts:
    w = (W - 2 * M) * c / tot
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
    (7, "Middle East", "ANTALYA · CLIMATE", "Fallout as COP31 ends with no deal", "First failed cover text in 17 years.", "globe_cop", "COP31: NO DEAL", "Yale E360 · AP"),
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
OFF = {6: (16, 8), 10: (-12, 10), 11: (14, -10), 1: (-4, 0), 3: (8, 6), 8: (9, 6), 12: (-12, -3),
       2: (-9, 3), 7: (2, 9), 4: (-9, -8), 5: (9, -8), 13: (12, 4), 9: (0, 0)}
for n, lo, la, rg in pins:
    tx, ty = P(lo, la); ox, oy = OFF.get(n, (0, 0))
    px, py = min(max(tx + ox, mx0 + 8), mx1 - 8), min(max(ty + oy, my0 + 8), my1 - 8)
    if (ox, oy) != (0, 0):
        d.line([tx, ty, px, py], fill="white", width=1); d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill="white")
for n, lo, la, rg in pins:
    tx, ty = P(lo, la); ox, oy = OFF.get(n, (0, 0))
    px, py = min(max(tx + ox, mx0 + 8), mx1 - 8), min(max(ty + oy, my0 + 8), my1 - 8)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=REG[rg], outline="white")
    f = SANS_B(9 if n < 10 else 8); s = str(n)
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
    c_, r_ = divmod(i, 10); xx = bx + c_ * (colw + 12); yy = by + 15 + r_ * 13.4
    d.text((xx, yy), str(n), font=SANS_B(9), fill=REG[rg]); xx2 = xx + 16
    d.text((xx2, yy), pl, font=SANS_B(9), fill=INK); xx2 += tw(pl, SANS_B(9)) + 4
    d.text((xx2, yy), s, font=SANS(9), fill=INK); xx2 += tw(s, SANS(9)) + 3
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
