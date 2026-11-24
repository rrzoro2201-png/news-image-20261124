#!/usr/bin/env python3
"""The Daily Chronicle — Tuesday 24 November 2026 world news, one image.

Illustrated front page, v2 pictures + @ilyayaaa structure: stats strip with
region counts, 3 big illustrated leads, an illustrated grid, a world map
("WHERE IT HAPPENED") with dots, a numbered tail list, DATE CHECK footer.

Every story below happened or was first reported on 24 November 2026,
cross-checked against the day's reporting (jagranjosh/Newsmriti roundups,
Disclosure News burst, bestenfenster wire, WSJ via roundups). Dating notes:
the Benghazi blast was first reported 22 Nov — the 24 Nov news is
Zelenskiy's announcement that Ukrainian forces struck the corvette.
BepiColombo entered Mercury orbit on 21 Nov, so it is NOT used again.
COP31's collapse was 23 Nov; the 24 Nov story is the post-mortem
(no fossil-fuel deal) and the calls for a new approach.

Deterministic: fixed seed, no timestamps. Run: python3 render.py
Writes entry.png (1024x1024, < 1 MiB).
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 26
CW = W - 2 * M
PAPER = (242, 232, 213)
INK = (26, 26, 24)
FAINT = (90, 82, 70)
RULE = (60, 52, 44)
SKY = (178, 205, 222)
SUN = (232, 178, 74)
RED = (178, 44, 34)
TEAL = (38, 68, 78)
SEA = (198, 214, 222)
LAND = (210, 196, 164)

random.seed(7)


def font(name, size):
    for p in (f"/usr/share/fonts/truetype/liberation/LiberationSerif-{name}.ttf",
              f"/usr/share/fonts/truetype/dejavu/DejaVuSerif-{name}.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def sfont(name, size):
    for p in (f"/usr/share/fonts/truetype/liberation/LiberationSans-{name}.ttf",
              f"/usr/share/fonts/truetype/dejavu/DejaVuSans-{name}.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


F_TITLE = font("Bold", 58)
F_DATE = font("Bold", 15)
F_DATE_R = font("Regular", 13)
F_KICK = sfont("Bold", 11)
F_STAT = sfont("Bold", 11)
F_LEAD_H = font("Bold", 30)
F_LEAD_B = font("Regular", 15)
F_MED_H = font("Bold", 18)
F_MED_B = font("Regular", 12)
F_SM_H = font("Bold", 13)
F_SM_B = font("Regular", 11)
F_TAIL = font("Bold", 10)
F_CAP = font("Italic", 11)
F_FOOT = font("Italic", 11)
F_MAP_LBL = sfont("Bold", 10)


def wrap(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, fnt, width, max_lines):
    lines = wrap(d, text, fnt, width)
    if len(lines) <= max_lines:
        return lines
    cut = lines[:max_lines]
    while cut and d.textlength(cut[-1] + " ...", font=fnt) > width:
        cut[-1] = cut[-1].rsplit(" ", 1)[0] if " " in cut[-1] else cut[-1][:-1]
    cut[-1] += " ..."
    return cut


def draw_lines(d, lines, x, y, fnt, leading=None):
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=INK)
        y += lh
    return y


def rule(d, x0, y, x1, w=1):
    d.line([(x0, y), (x1, y)], fill=RULE, width=w)


# ------------------------------------------------------------ illustrations
def hero_burning_ship(d, x, y, w, h):
    """Benghazi: corvette burning in port, black smoke over a grey sea."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 200, 160), outline=RULE, width=2)
    d.ellipse([x + w - 110, y + 10, x + w - 40, y + 80], fill=SUN, outline=(190, 140, 40), width=2)
    for cx in (x + 40, x + 300, x + 560):
        d.ellipse([cx, y + 18, cx + 90, y + 42], fill=(240, 238, 228))
        d.ellipse([cx + 30, y + 8, cx + 120, y + 34], fill=(240, 238, 228))
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=TEAL)
    for wx in range(x + 10, x + w - 10, 64):
        d.arc([wx, y + h * 0.62, wx + 44, y + h * 0.62 + 16], 180, 360, fill=(220, 228, 230), width=2)
        d.arc([wx + 20, y + h * 0.82, wx + 64, y + h * 0.82 + 16], 180, 360, fill=(220, 228, 230), width=2)
    # warship silhouette
    sx, sy = x + 120, y + h - 34
    d.polygon([(sx, sy), (sx + 560, sy), (sx + 520, sy - 26), (sx + 40, sy - 26)], fill=(30, 30, 34))
    d.rectangle([sx + 130, sy - 52, sx + 330, sy - 26], fill=(30, 30, 34))
    d.rectangle([sx + 360, sy - 52, sx + 430, sy - 26], fill=(30, 30, 34))
    d.line([(sx + 430, sy - 52), (sx + 430, sy - 84)], fill=(30, 30, 34), width=5)
    d.polygon([(sx + 430, sy - 84), (sx + 478, sy - 72), (sx + 430, sy - 62)], fill=RED)
    for gx in range(sx + 60, sx + 540, 40):
        d.rectangle([gx, sy - 22, gx + 14, sy - 12], fill=(222, 200, 160))
    # flames on deck
    for fx, fh in ((sx + 180, 40), (sx + 220, 56), (sx + 262, 44)):
        d.polygon([(fx - 14, sy - 26), (fx, sy - 26 - fh), (fx + 14, sy - 26)], fill=(232, 120, 40))
        d.polygon([(fx - 7, sy - 26), (fx, sy - 26 - fh // 2), (fx + 7, sy - 26)], fill=(240, 200, 60))
    # black smoke, kept inside the frame
    for j, r in enumerate((16, 12, 9, 6)):
        d.ellipse([sx + 200 + j * 8, sy - 52 - j * 10, sx + 200 + j * 8 + r * 2,
                   sy - 52 - j * 10 + r * 2], fill=(52, 48, 46))
    # red alert dashes along the waterline
    by = y + h - 8
    for bx in range(x + 16, x + w - 16, 36):
        d.line([(bx, by), (bx + 22, by)], fill=RED, width=4)


def panel_chip(d, x, y, w, h):
    """Nvidia: a chip with a rising green arrow, NVDA ticker."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 210, 182), outline=RULE, width=2)
    d.rectangle([x + 14, y + 10, x + w - 14, y + 34], fill=(70, 66, 62))
    d.text((x + 22, y + 13), "NVDA  •  NASDAQ", font=sfont("Bold", 13), fill=(242, 232, 213))
    nd = "+$1TN"
    d.text((x + w - 22 - d.textlength(nd, font=sfont("Bold", 13)), y + 13), nd,
           font=sfont("Bold", 13), fill=(120, 200, 110))
    # chip
    cx, cy = x + 64, y + 44
    d.rectangle([cx, cy, cx + 40, cy + 40], outline=INK, width=3)
    d.rectangle([cx + 10, cy + 10, cx + 30, cy + 30], outline=INK, width=2)
    for i in range(3):
        d.line([(cx + 7 + i * 13, cy - 6), (cx + 7 + i * 13, cy)], fill=INK, width=2)
        d.line([(cx + 7 + i * 13, cy + 40), (cx + 7 + i * 13, cy + 46)], fill=INK, width=2)
    # rising arrow
    ax, ay = x + 170, y + h - 18
    d.line([(ax, ay), (ax + 90, ay - 34), (ax + 150, ay - 52)], fill=(40, 130, 60), width=5)
    d.polygon([(ax + 150, ay - 52), (ax + 128, ay - 50), (ax + 146, ay - 30)], fill=(40, 130, 60))


def panel_toxic(d, x, y, w, h):
    """Gaza: warning triangle over cracked, poisoned ground."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 210, 182), outline=RULE, width=2)
    d.rectangle([x + 14, y + 10, x + w - 14, y + 34], fill=(70, 66, 62))
    d.text((x + 22, y + 13), "OXFAM  •  CEOBS REPORT", font=sfont("Bold", 13), fill=(242, 232, 213))
    nd = "TOXIC"
    d.text((x + w - 22 - d.textlength(nd, font=sfont("Bold", 13)), y + 13), nd,
           font=sfont("Bold", 13), fill=SUN)
    # cracked ground
    gy = y + h - 34
    d.rectangle([x, gy, x + w, y + h], fill=(120, 102, 78))
    for (x0, y0, x1, y1) in ((x + 30, gy, x + 90, gy + 16), (x + 90, gy + 16, x + 70, y + h - 6),
                             (x + 200, gy, x + 260, gy + 20), (x + 260, gy + 20, x + 300, y + h - 8),
                             (x + 380, gy, x + 340, gy + 18), (x + 340, gy + 18, x + 360, y + h - 6)):
        d.line([(x0, y0), (x1, y1)], fill=(60, 52, 44), width=3)
    # warning triangle
    tx, ty = x + 150, y + 44
    d.polygon([(tx, ty), (tx + 44, ty + 38), (tx - 44, ty + 38)], fill=SUN, outline=INK, width=3)
    d.text((tx - 4, ty + 12), "!", font=sfont("Bold", 22), fill=INK)
    # barrels
    for bx in (x + 300, x + 350):
        d.rectangle([bx, gy - 26, bx + 26, gy], fill=(90, 82, 70), outline=INK, width=2)
        d.line([(bx, gy - 17), (bx + 26, gy - 17)], fill=INK, width=2)


def icon_image(kind, s=48):
    """Pictogram drawn at 48x48 then scaled to s (LANCZOS)."""
    im = Image.new("RGB", (48, 48), (226, 210, 182))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 47, 47], outline=RULE, width=2)
    c = 24
    if kind == "quake":
        d.line([(8, 12), (18, 26), (26, 14), (36, 30), (42, 18)], fill=RED, width=3)
        d.line([(8, 36), (40, 36)], fill=INK, width=2)
    elif kind == "rocket":
        d.polygon([(c, 6), (c - 9, 30), (c + 9, 30)], fill=RED)
        d.line([(c, 30), (c, 42)], fill=SUN, width=4)
    elif kind == "waves":
        for yy in (16, 26, 36):
            d.arc([8, yy - 6, 40, yy + 6], 0, 180, fill=(52, 110, 160), width=3)
    elif kind == "ball":
        d.ellipse([10, 10, 38, 38], outline=INK, width=3)
        d.line([(c, 10), (c, 38)], fill=INK, width=2)
        d.line([(10, c), (38, c)], fill=INK, width=2)
    elif kind == "chip":
        d.rectangle([14, 14, 34, 34], outline=INK, width=3)
        for i in range(3):
            d.line([(14 + i * 10, 8), (14 + i * 10, 14)], fill=INK, width=2)
            d.line([(14 + i * 10, 34), (14 + i * 10, 40)], fill=INK, width=2)
    elif kind == "globe":
        d.ellipse([10, 10, 38, 38], outline=INK, width=3)
        d.ellipse([c - 7, 10, c + 7, 38], outline=INK, width=2)
        d.line([(10, c), (38, c)], fill=INK, width=2)
    elif kind == "ship":
        d.polygon([(8, 28), (40, 28), (34, 38), (14, 38)], fill=INK)
        d.line([(c, 10), (c, 28)], fill=INK, width=3)
        d.polygon([(c, 12), (c + 12, 26), (c, 26)], fill=RED)
    elif kind == "bridge":
        d.arc([8, 12, 40, 40], 180, 360, fill=INK, width=3)
        d.line([(10, 26), (10, 40)], fill=INK, width=2)
        d.line([(38, 26), (38, 40)], fill=INK, width=2)
    elif kind == "flag":
        d.line([(12, 8), (12, 40)], fill=INK, width=3)
        d.polygon([(12, 8), (38, 14), (12, 22)], fill=RED)
    elif kind == "coin":
        d.ellipse([10, 10, 38, 38], outline=INK, width=3)
        d.text((c - 5, 13), "$", font=font("Bold", 20), fill=INK)
    elif kind == "court":
        d.line([(c, 8), (c, 40)], fill=INK, width=3)
        d.line([(10, 40), (38, 40)], fill=INK, width=3)
        d.line([(12, 14), (36, 14)], fill=INK, width=3)
    elif kind == "plane":
        d.polygon([(8, 26), (40, 20), (40, 28), (8, 32)], fill=INK)
        d.polygon([(c - 4, 12), (c + 4, 12), (c, 34)], fill=INK)
    elif kind == "sun":
        d.ellipse([14, 14, 34, 34], fill=SUN, outline=(190, 140, 40), width=2)
        for a in range(0, 360, 45):
            x1 = c + int(20 * math.cos(math.radians(a)))
            y1 = c + int(20 * math.sin(math.radians(a)))
            x2 = c + int(24 * math.cos(math.radians(a)))
            y2 = c + int(24 * math.sin(math.radians(a)))
            d.line([(x1, y1), (x2, y2)], fill=(190, 140, 40), width=2)
    elif kind == "camera":
        d.rounded_rectangle([8, 14, 40, 36], radius=4, outline=INK, width=3)
        d.ellipse([c - 7, c - 7, c + 7, c + 7], outline=INK, width=3)
    elif kind == "flame":
        d.polygon([(c, 8), (c + 12, 26), (c + 6, 40), (c - 6, 40), (c - 12, 26)], fill=(232, 120, 40))
        d.polygon([(c, 22), (c + 6, 32), (c, 40), (c - 6, 32)], fill=(240, 200, 60))
    elif kind == "cap":
        d.polygon([(8, 20), (c, 12), (40, 20), (c, 28)], fill=INK)
        d.line([(c, 28), (c, 38)], fill=INK, width=3)
        d.line([(14, 34), (34, 34)], fill=INK, width=2)
    elif kind == "drop":
        d.polygon([(c, 8), (c + 11, 26), (c, 40), (c - 11, 26)], fill=(52, 110, 160))
    elif kind == "trophy":
        d.polygon([(16, 10), (32, 10), (30, 26), (18, 26)], fill=SUN, outline=INK, width=2)
        d.line([(c, 26), (c, 36)], fill=INK, width=3)
        d.line([(16, 38), (32, 38)], fill=INK, width=3)
    elif kind == "bug":
        d.ellipse([c - 8, 16, c + 8, 34], outline=INK, width=3)
        for yy in (20, 26, 32):
            d.line([(c - 8, yy), (c - 16, yy - 4)], fill=INK, width=2)
            d.line([(c + 8, yy), (c + 16, yy - 4)], fill=INK, width=2)
        d.line([(c - 4, 16), (c - 8, 8)], fill=INK, width=2)
        d.line([(c + 4, 16), (c + 8, 8)], fill=INK, width=2)
    elif kind == "gavel":
        d.rectangle([14, 12, 34, 20], fill=INK)
        d.line([(c, 20), (c + 10, 38)], fill=INK, width=4)
        d.line([(12, 40), (36, 40)], fill=INK, width=3)
    else:
        d.text((c - 8, 12), "*", font=font("Bold", 26), fill=INK)
    return im.resize((s, s), Image.LANCZOS) if s != 48 else im


# ------------------------------------------------------------ stories
# (region, kicker, headline, body, icon) — 35 stories, all 24 Nov 2026.
LEAD = ("LIBYA  •  BENGHAZI",
        "RUSSIAN WARSHIP DESTROYED IN LIBYA PORT BLAST",
        "Zelenskiy said Ukrainian forces struck a Russian Navy missile corvette in Benghazi, where it burned after an explosion — the war's reach now stretching far beyond Ukrainian waters.")
MEDIUM = [
    ("TECH  •  NVIDIA",
     "HUANG IS BACK — NVIDIA ADDS ALMOST $1TN",
     "Jensen Huang returned as Nvidia chief after Trump's public appeal, and the chipmaker's value jumped by almost $1 trillion as tech stocks rallied.",
     "chip"),
    ("GAZA  •  OXFAM REPORT",
     "GAZA'S SOIL AND WATER POISONED FOR DECADES",
     "An Oxfam report found Israel's bombardment left Gaza's air, soil and water laced with heavy metals, asbestos and dioxins — dangerous for decades to come.",
     "toxic"),
]
GRID = [
    ("NEPAL", "MODI, NEPAL PM FLAG OFF NEW TRAIN",
     "Modi and Nepal's PM Balendra Shah flagged off the Saryu-Kamala Express linking Ayodhya and Janakpur.", "bridge"),
    ("CRICKET", "PANT 128 AS INDIA DRAW WELLINGTON TEST",
     "Rishabh Pant hit 128 against New Zealand as the first Test ended in a draw.", "ball"),
    ("FORMULA 1", "VERSTAPPEN WINS LAS VEGAS GP",
     "Max Verstappen won the 2026 Las Vegas Grand Prix.", "trophy"),
    ("UKRAINE", "SEVERAL MISSING AFTER KYIV DRONE STRIKE",
     "A Russian drone strike in the Kyiv region left several people missing, Zelenskiy said.", "rocket"),
    ("FINLAND", "RUSSIAN CARGO SHIP ABLAZE OFF FINLAND",
     "A Russian cargo ship caught fire off Finland after a reported attack.", "ship"),
    ("PORTUGAL", "THOUSANDS MARCH IN LISBON OVER LIVING COSTS",
     "Thousands took to Lisbon's streets to protest against rising living costs.", "flag"),
]
TAIL = [
    ("INDONESIA", "BANTEN FACTORY FIRE KILLS WORKERS"),
    ("KOREA", "TRUMP'S KIM OUTREACH IGNORED"),
    ("EU", "EU READIES NEW RUSSIA SANCTIONS"),
    ("DENMARK", "COURT BACKS HARDLINE 'GHETTO LAW'"),
    ("US", "TRUMP PATH TO ERASE CONVICTION"),
    ("KOREA", "SEOUL NAMES NEW FOREIGN MINISTER"),
    ("MYANMAR", "MYANMAR CALLS ASEAN MOVE 'UNFAIR'"),
    ("POLAND", "RUSSIAN MISSILES FELL IN POLAND"),
    ("IRAN", "IRAN READY TO REOPEN HORMUZ"),
    ("MEXICO", "MOST-WANTED CARTEL BOSS CAUGHT"),
    ("YEMEN", "6 DEAD IN SAUDI STRIKE ON HODEIDA"),
    ("AFGHANISTAN", "TALIBAN ERASES WOMEN'S NAMES"),
    ("SPACE", "SUPERMOON MEETS THE SEVEN SISTERS"),
    ("INDIA", "OIL IMPORT BILL UP 60% IN OCTOBER"),
    ("BUSINESS", "SPICEJET CRISIS DEEPENS"),
    ("BUSINESS", "FERRARI UNVEILS TWO NEW 296 MODELS"),
    ("FOOTBALL", "DE BRUYNE: CITY LOVE UNCHANGED"),
    ("FIFA", "FIFA PICKS 2031, 2035 CUP HOSTS"),
    ("US", "TRUMP TO TARGET NEWSOM AT DOJ"),
    ("ISRAEL", "ISRAEL BARS POLISH MP OVER FLOTILLA"),
    ("BOSNIA", "DODIK PICKED TO HEAD SERB ENTITY"),
    ("IRAQ", "TROOPS RAID MILITIA HQ"),
    ("NETHERLANDS", "DUTCH PM DOUBTS JOINT EU ARMY"),
    ("BUSINESS", "AMAZON TOPS MTN BID FOR TELKOM"),
    ("CLIMATE", "COP31: NO DEAL ON FOSSIL FUELS"),
    ("NEPAL", "INDIA ANNOUNCES $1.6BN NEPAL AID"),
]
REGIONS = [("MIDDLE EAST", 5, (178, 44, 34)), ("EUROPE", 11, (52, 110, 160)),
           ("ASIA-PACIFIC", 10, (96, 122, 88)), ("AMERICAS", 5, (232, 178, 74)),
           ("AFRICA", 2, (150, 110, 60)), ("WORLD", 2, (90, 82, 70))]

# world map: rough continent polygons in lon/lat
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
     (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28), (-58, -38),
     (-65, -45), (-70, -52), (-73, -37), (-70, -18), (-77, -12), (-80, -3)],
    [(-10, 36), (-9, 43), (0, 46), (-2, 50), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (28, 59), (30, 62), (28, 71), (18, 70), (12, 66), (5, 60), (-5, 58),
     (-10, 54), (-10, 44)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
     (51, 11), (48, 0), (40, -10), (35, -18), (32, -26), (26, -34), (19, -35),
     (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(30, 62), (40, 68), (60, 69), (80, 73), (100, 77), (120, 76), (140, 72),
     (160, 69), (178, 66), (170, 60), (162, 56), (158, 50), (142, 45), (135, 43),
     (130, 38), (127, 35), (122, 30), (120, 22), (110, 20), (108, 12), (105, 9),
     (100, 7), (98, 12), (94, 16), (91, 22), (88, 22), (80, 15), (77, 8), (75, 15),
     (70, 20), (66, 25), (62, 25), (57, 26), (52, 28), (48, 30), (44, 29), (40, 32),
     (36, 36), (30, 36), (28, 40), (30, 45), (28, 55), (30, 60)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (129, -32), (132, -32), (136, -35),
     (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20), (114, -22)],
]
# (lon, lat, number-or-None, label, label-side)
DOTS = [
    (19.5, 32.1, "1", "BENGHAZI", "left"), (56.5, 26.5, "2", "HORMUZ", "below"),
    (30.7, 36.9, "3", "ANTALYA", "above"),
    (77.2, 28.6, None, None, None), (127.0, 37.5, None, None, None),
    (174.8, -41.3, None, None, None), (30.5, 50.4, None, None, None),
    (24.9, 60.2, None, None, None), (-9.1, 38.7, None, None, None),
    (106.8, -6.2, None, None, None), (96.2, 19.8, None, None, None),
    (34.5, 31.4, None, None, None), (12.5, 41.9, None, None, None),
    (-77.0, 38.9, None, None, None), (21.0, 52.2, None, None, None),
    (12.6, 55.7, None, None, None), (-99.1, 19.4, None, None, None),
    (-0.1, 51.5, None, None, None),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    for _ in range(2600):
        x, y = random.randint(0, W - 1), random.randint(0, H - 1)
        v = random.randint(-14, 10)
        d.point((x, y), fill=(PAPER[0] + v, PAPER[1] + v, PAPER[2] + v))
    for i in range(18):
        a = 10 + i
        d.rectangle([i, i, W - 1 - i, H - 1 - i], outline=(120 + i * 4, 108 + i * 4, 88 + i * 4))
    d.rectangle([0, 0, W - 1, H - 1], outline=(70, 60, 48), width=2)

    y = M + 6
    title = "The Daily Chronicle"
    d.text(((W - d.textlength(title, font=F_TITLE)) / 2, y), title, font=F_TITLE, fill=INK)
    y += 70
    rule(d, M, y, W - M, 1)
    y += 6
    d.text((M, y), "TUESDAY, 24 NOVEMBER 2026", font=F_DATE, fill=INK)
    right = "35 STORIES  •  6 REGIONS"
    d.text((W - M - d.textlength(right, font=F_DATE_R), y), right, font=F_DATE_R, fill=INK)
    y += 20
    rule(d, M, y, W - M, 3)
    rule(d, M, y + 5, W - M, 1)
    y += 10

    # --- stats strip: region counts with colour bars ---
    seg = CW // 6
    for i, (name, n, col) in enumerate(REGIONS):
        x = M + i * seg
        d.rectangle([x, y, x + seg - 8, y + 18], fill=col)
        lbl = f"{name} {n}"
        tw = d.textlength(lbl, font=F_STAT)
        d.text((x + (seg - 8 - tw) / 2, y + 3), lbl, font=F_STAT,
               fill=(242, 232, 213) if col != (232, 178, 74) else INK)
    y += 18 + 8

    # --- hero: burning corvette illustration + lead ---
    hero_burning_ship(d, M, y, CW, 130)
    y += 130 + 5
    d.text((M, y), LEAD[0], font=F_KICK, fill=FAINT)
    y += 16
    y = draw_lines(d, fit(d, LEAD[1], F_LEAD_H, CW, 2), M, y, F_LEAD_H, leading=34)
    y += 3
    y = draw_lines(d, fit(d, LEAD[2], F_LEAD_B, CW, 2), M, y, F_LEAD_B, leading=19)
    y += 7
    rule(d, M, y, W - M, 1)
    y += 11

    # --- medium stories: wide illustration panels ---
    med_w = (CW - 16) // 2
    med_y = y
    for i, (kick, head, body, kind) in enumerate(MEDIUM):
        x = M + i * (med_w + 16)
        yy = med_y
        if kind == "chip":
            panel_chip(d, x, yy, med_w, 92)
        else:
            panel_toxic(d, x, yy, med_w, 92)
        yy += 92 + 7
        d.text((x, yy), kick, font=F_KICK, fill=FAINT)
        yy += 15
        yy = draw_lines(d, fit(d, head, F_MED_H, med_w, 2), x, yy, F_MED_H, leading=21)
        yy += 2
        draw_lines(d, fit(d, body, F_MED_B, med_w, 2), x, yy, F_MED_B, leading=15)
    y = med_y + 92 + 7 + 15 + 42 + 2 + 30 + 6
    rule(d, M, y, W - M, 3)
    rule(d, M, y + 5, W - M, 1)
    y += 13
    label = "THE WORLD IN BRIEF"
    d.text(((W - d.textlength(label, font=F_KICK)) / 2, y), label, font=F_KICK, fill=FAINT)
    y += 17

    # --- grid: 3 cols x 2 rows, 60px icons ---
    gap = 14
    col_w = (CW - 2 * gap) // 3
    rows = 2
    grid_top = y
    slot_h = 72
    for idx, (kick, head, body, kind) in enumerate(GRID):
        col, row = idx % 3, idx // 3
        x = M + col * (col_w + gap)
        yy = grid_top + row * slot_h
        if col > 0:
            d.line([(x - gap // 2, yy + 2), (x - gap // 2, yy + slot_h - 8)],
                   fill=(165, 152, 128), width=1)
        img.paste(icon_image(kind, 60), (x, yy))
        tx = x + 68
        tw = col_w - 68
        d.text((tx, yy), kick, font=F_KICK, fill=FAINT)
        yy += 14
        yy = draw_lines(d, fit(d, head, F_SM_H, tw, 2), tx, yy, F_SM_H, leading=15)
        yy += 1
        draw_lines(d, fit(d, body, F_SM_B, tw, 2), tx, yy, F_SM_B, leading=13)
    y = grid_top + rows * slot_h + 4
    rule(d, M, y, W - M, 1)
    y += 10

    # --- bottom row: map (left) + numbered tail list (right) ---
    bottom_top = y
    bottom_h = H - 52 - bottom_top
    map_w = 470
    tail_x = M + map_w + 16
    tail_w = W - M - tail_x
    d.text((M, bottom_top), "WHERE IT HAPPENED", font=F_KICK, fill=FAINT)
    d.text((tail_x, bottom_top), "26 MORE STORIES", font=F_KICK, fill=FAINT)
    my = bottom_top + 18
    mh = bottom_h - 18
    d.rectangle([M, my, M + map_w, my + mh], fill=SEA, outline=RULE, width=2)

    def proj(lon, lat):
        px = M + 8 + (lon + 170) / 360 * (map_w - 16)
        py = my + 6 + (75 - lat) / 130 * (mh - 12)
        return px, py

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=(120, 108, 88))
    for lon, lat, num, lbl, side in DOTS:
        px, py = proj(lon, lat)
        if num:
            d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=INK, width=1)
            d.text((px - 3, py - 6), num, font=sfont("Bold", 10), fill=(242, 232, 213))
        else:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=INK)
    # legend for the three numbered dots, on a paper strip at the map's foot
    legend = "1 BENGHAZI  •  2 HORMUZ  •  3 ANTALYA"
    lw = d.textlength(legend, font=F_MAP_LBL)
    lx = M + (map_w - lw) / 2
    ly = my + mh - 15
    d.rectangle([lx - 6, ly - 2, lx + lw + 6, ly + 12], fill=PAPER)
    d.text((lx, ly), legend, font=F_MAP_LBL, fill=INK)

    # tail list: 2 sub-columns x 13
    sub_gap = 12
    sub_w = (tail_w - sub_gap) // 2
    lead_tail = 13
    truncated = []
    for idx, (kick, head) in enumerate(TAIL):
        col, row = idx // 13, idx % 13
        x = tail_x + col * (sub_w + sub_gap)
        yy = bottom_top + 18 + row * lead_tail
        d.text((x, yy), f"{idx + 1}.", font=F_TAIL, fill=RED)
        lines = fit(d, head, F_TAIL, sub_w - 24, 1)
        if lines[0].endswith("..."):
            truncated.append(head)
        d.text((x + 22, yy), lines[0], font=F_TAIL, fill=INK)
    if truncated:
        print("TRUNCATED TAIL:", truncated)

    y = H - 44
    rule(d, M, y, W - M, 1)
    y += 7
    foot = ("DATE CHECK: TUESDAY 24 NOVEMBER 2026 — every story above happened or was first reported on 24 November 2026.")
    d.text(((W - d.textlength(foot, font=F_FOOT)) / 2, y), foot, font=F_FOOT, fill=INK)
    y += 15
    d.text(((W - d.textlength("The Daily Chronicle • 24 November 2026", font=F_FOOT)) / 2, y),
           "The Daily Chronicle • 24 November 2026", font=F_FOOT, fill=FAINT)

    img.save("entry.png", optimize=True)
    print(f"saved entry.png {img.size}")
    print(f"layout: bottom_top={bottom_top} bottom_h={bottom_h} "
          f"tail_last_row_y={bottom_top + 18 + 12 * lead_tail} footer_rule_y={H - 44}")


if __name__ == "__main__":
    main()
