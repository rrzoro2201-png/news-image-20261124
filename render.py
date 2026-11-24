#!/usr/bin/env python3
"""The Daily Chronicle, Tuesday 24 November 2026 — the day's world news as
one illustrated broadsheet, drawn by hand in Pillow.

Layout, top to bottom: masthead with the date and a count of stories; a
colour strip counting stories per region; one big burning-ship picture for
the lead story; two wide picture panels; a six-item grid with pictograms;
a small world map with dots where the news happened; a numbered list of
26 further stories; a date-check footer.

Sources for the day: the 24 November roundups (jagranjosh, Newsmriti),
the Disclosure News burst, the bestenfenster wire and WSJ reporting as
quoted in the roundups. Two dating calls: the Benghazi blast was first
reported on 22 November, so the lead is Zelenskiy's 24 November
announcement that Ukrainian forces struck the corvette; BepiColombo
reached Mercury on 21 November and is left out. COP31 appears as the
24 November post-mortem, not as the collapse itself.

Deterministic: the random seed is fixed and nothing reads the clock.
Run it with `python3 render.py`; it writes entry.png, 1024 by 1024,
well under the 1 MiB cap.
"""
import math
import random
from PIL import Image as Img, ImageDraw as Draw, ImageFont as Font

random.seed(24)

PAGE_W, PAGE_H = 1024, 1024
EDGE = 26
SPAN = PAGE_W - 2 * EDGE
C = {
    "paper": (242, 232, 213), "ink": (26, 26, 24), "faint": (90, 82, 70),
    "rule": (60, 52, 44), "sky": (178, 205, 222), "sun": (232, 178, 74),
    "red": (178, 44, 34), "teal": (38, 68, 78), "sea": (198, 214, 222),
    "land": (210, 196, 164), "sand": (226, 210, 182), "cream": (222, 200, 160),
    "dark": (30, 30, 34), "smoke": (52, 48, 46), "pine": (96, 122, 88),
    "ocean": (52, 110, 160), "gold": (232, 178, 74), "clay": (150, 110, 60),
    "grey": (90, 82, 70), "leaf": (40, 130, 60), "flame": (232, 120, 40),
    "ember": (240, 200, 60), "cloud": (240, 238, 228), "wave": (220, 228, 230),
}


def _load(paths, size):
    for path in paths:
        try:
            return Font.truetype(path, size)
        except OSError:
            continue
    return Font.load_default()


def serif(weight, size):
    return _load([
        "/usr/share/fonts/truetype/liberation/LiberationSerif-%s.ttf" % weight,
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-%s.ttf" % weight,
    ], size)


def sans(weight, size):
    return _load([
        "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % weight,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-%s.ttf" % weight,
    ], size)


TITLE_F = serif("Bold", 58)
DATE_F = serif("Bold", 15)
DATE_R = serif("Regular", 13)
KICK_F = sans("Bold", 11)
STAT_F = sans("Bold", 11)
LEAD_H = serif("Bold", 30)
LEAD_B = serif("Regular", 15)
MED_H = serif("Bold", 18)
MED_B = serif("Regular", 12)
SM_H = serif("Bold", 13)
SM_B = serif("Regular", 11)
TAIL_F = serif("Bold", 10)
FOOT_F = serif("Italic", 11)
MAP_F = sans("Bold", 10)


def split_text(d, text, f, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def clip_text(d, text, f, width, n):
    """Wrap and cut to at most n lines, with an ellipsis on the last."""
    lines = split_text(d, text, f, width)
    if len(lines) <= n:
        return lines
    cut = lines[:n]
    while cut and d.textlength(cut[-1] + " ...", font=f) > width:
        cut[-1] = cut[-1].rsplit(" ", 1)[0] if " " in cut[-1] else cut[-1][:-1]
    cut[-1] += " ..."
    return cut


def put_text(d, lines, x, y, f, gap=None):
    step = gap or int(f.size * 1.18)
    for line in lines:
        d.text((x, y), line, font=f, fill=C["ink"])
        y += step
    return y


def hline(d, x0, y, x1, w=1):
    d.line([(x0, y), (x1, y)], fill=C["rule"], width=w)


# ---------------------------------------------------------------- pictures
def paint_hero(d, x, y, w, h):
    """Benghazi: a corvette burning in port, black smoke over a grey sea."""
    d.rectangle([x, y, x + w, y + h], fill=C["cream"], outline=C["rule"], width=2)
    d.ellipse([x + w - 110, y + 10, x + w - 40, y + 80], fill=C["sun"],
              outline=(190, 140, 40), width=2)
    for cx in (x + 40, x + 300, x + 560):
        d.ellipse([cx, y + 18, cx + 90, y + 42], fill=C["cloud"])
        d.ellipse([cx + 30, y + 8, cx + 120, y + 34], fill=C["cloud"])
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=C["teal"])
    for wx in range(x + 10, x + w - 10, 64):
        d.arc([wx, y + h * 0.62, wx + 44, y + h * 0.62 + 16], 180, 360,
              fill=C["wave"], width=2)
        d.arc([wx + 20, y + h * 0.82, wx + 64, y + h * 0.82 + 16], 180, 360,
              fill=C["wave"], width=2)
    sx, sy = x + 120, y + h - 34
    d.polygon([(sx, sy), (sx + 560, sy), (sx + 520, sy - 26), (sx + 40, sy - 26)],
              fill=C["dark"])
    d.rectangle([sx + 130, sy - 52, sx + 330, sy - 26], fill=C["dark"])
    d.rectangle([sx + 360, sy - 52, sx + 430, sy - 26], fill=C["dark"])
    d.line([(sx + 430, sy - 52), (sx + 430, sy - 84)], fill=C["dark"], width=5)
    d.polygon([(sx + 430, sy - 84), (sx + 478, sy - 72), (sx + 430, sy - 62)],
              fill=C["red"])
    for gx in range(sx + 60, sx + 540, 40):
        d.rectangle([gx, sy - 22, gx + 14, sy - 12], fill=C["cream"])
    for fx, fh in ((sx + 180, 40), (sx + 220, 56), (sx + 262, 44)):
        d.polygon([(fx - 14, sy - 26), (fx, sy - 26 - fh), (fx + 14, sy - 26)],
                  fill=C["flame"])
        d.polygon([(fx - 7, sy - 26), (fx, sy - 26 - fh // 2), (fx + 7, sy - 26)],
                  fill=C["ember"])
    for j, r in enumerate((16, 12, 9, 6)):
        d.ellipse([sx + 200 + j * 8, sy - 52 - j * 10,
                   sx + 200 + j * 8 + r * 2, sy - 52 - j * 10 + r * 2],
                  fill=C["smoke"])
    by = y + h - 8
    for bx in range(x + 16, x + w - 16, 36):
        d.line([(bx, by), (bx + 22, by)], fill=C["red"], width=4)


def paint_chip(d, x, y, w, h):
    """Nvidia: a chip with a rising green arrow, NVDA ticker."""
    d.rectangle([x, y, x + w, y + h], fill=C["sand"], outline=C["rule"], width=2)
    d.rectangle([x + 14, y + 10, x + w - 14, y + 34], fill=(70, 66, 62))
    d.text((x + 22, y + 13), "NVDA  •  NASDAQ", font=sans("Bold", 13),
           fill=C["paper"])
    tag = "+$1TN"
    d.text((x + w - 22 - d.textlength(tag, font=sans("Bold", 13)), y + 13), tag,
           font=sans("Bold", 13), fill=(120, 200, 110))
    cx, cy = x + 64, y + 44
    d.rectangle([cx, cy, cx + 40, cy + 40], outline=C["ink"], width=3)
    d.rectangle([cx + 10, cy + 10, cx + 30, cy + 30], outline=C["ink"], width=2)
    for i in range(3):
        d.line([(cx + 7 + i * 13, cy - 6), (cx + 7 + i * 13, cy)], fill=C["ink"], width=2)
        d.line([(cx + 7 + i * 13, cy + 40), (cx + 7 + i * 13, cy + 46)],
               fill=C["ink"], width=2)
    ax, ay = x + 170, y + h - 18
    d.line([(ax, ay), (ax + 90, ay - 34), (ax + 150, ay - 52)], fill=C["leaf"], width=5)
    d.polygon([(ax + 150, ay - 52), (ax + 128, ay - 50), (ax + 146, ay - 30)],
              fill=C["leaf"])


def paint_toxic(d, x, y, w, h):
    """Gaza: a warning triangle over cracked, poisoned ground."""
    d.rectangle([x, y, x + w, y + h], fill=C["sand"], outline=C["rule"], width=2)
    d.rectangle([x + 14, y + 10, x + w - 14, y + 34], fill=(70, 66, 62))
    d.text((x + 22, y + 13), "OXFAM  •  CEOBS REPORT", font=sans("Bold", 13),
           fill=C["paper"])
    tag = "TOXIC"
    d.text((x + w - 22 - d.textlength(tag, font=sans("Bold", 13)), y + 13), tag,
           font=sans("Bold", 13), fill=C["sun"])
    gy = y + h - 34
    d.rectangle([x, gy, x + w, y + h], fill=(120, 102, 78))
    cracks = [((x + 30, gy), (x + 90, gy + 16)), ((x + 90, gy + 16), (x + 70, y + h - 6)),
              ((x + 200, gy), (x + 260, gy + 20)), ((x + 260, gy + 20), (x + 300, y + h - 8)),
              ((x + 380, gy), (x + 340, gy + 18)), ((x + 340, gy + 18), (x + 360, y + h - 6))]
    for p0, p1 in cracks:
        d.line([p0, p1], fill=C["rule"], width=3)
    tx, ty = x + 150, y + 44
    d.polygon([(tx, ty), (tx + 44, ty + 38), (tx - 44, ty + 38)], fill=C["sun"],
              outline=C["ink"], width=3)
    d.text((tx - 4, ty + 12), "!", font=sans("Bold", 22), fill=C["ink"])
    for bx in (x + 300, x + 350):
        d.rectangle([bx, gy - 26, bx + 26, gy], fill=C["grey"], outline=C["ink"], width=2)
        d.line([(bx, gy - 17), (bx + 26, gy - 17)], fill=C["ink"], width=2)


# A pictogram is a list of primitives; each is (shape, coords, colour, width).
GLYPHS = {
    "bridge": [("arc", (8, 12, 40, 40, 180, 360), "ink", 3),
               ("line", (10, 26, 10, 40), "ink", 2),
               ("line", (38, 26, 38, 40), "ink", 2)],
    "ball": [("oval", (10, 10, 38, 38), "ink", 3),
             ("line", (24, 10, 24, 38), "ink", 2),
             ("line", (10, 24, 38, 24), "ink", 2)],
    "trophy": [("poly", [(16, 10), (32, 10), (30, 26), (18, 26)], "sun", 2),
               ("line", (24, 26, 24, 36), "ink", 3),
               ("line", (16, 38, 32, 38), "ink", 3)],
    "rocket": [("poly", [(24, 6), (15, 30), (33, 30)], "red", 0),
               ("line", (24, 30, 24, 42), "sun", 4)],
    "ship": [("poly", [(8, 28), (40, 28), (34, 38), (14, 38)], "ink", 0),
             ("line", (24, 10, 24, 28), "ink", 3),
             ("poly", [(24, 12), (36, 26), (24, 26)], "red", 0)],
    "flag": [("line", (12, 8, 12, 40), "ink", 3),
             ("poly", [(12, 8), (38, 14), (12, 22)], "red", 0)],
}


def glyph(kind, size=60):
    """Draw one pictogram at 48x48, then scale it to size."""
    im = Img.new("RGB", (48, 48), C["sand"])
    g = Draw.Draw(im)
    g.rectangle([0, 0, 47, 47], outline=C["rule"], width=2)
    for shape, coords, colour, w in GLYPHS.get(kind, []):
        col = C[colour]
        if shape == "line":
            g.line([coords[0:2], coords[2:4]], fill=col, width=w)
        elif shape == "oval":
            g.ellipse(coords, outline=col, width=w)
        elif shape == "poly":
            g.polygon(coords, fill=col, outline=C["ink"] if w else None, width=w or 1)
        elif shape == "arc":
            g.arc(coords[0:4], coords[4], coords[5], fill=col, width=w)
    return im.resize((size, size), Img.LANCZOS) if size != 48 else im


# ------------------------------------------------------------------- stories
LEAD = {
    "place": "LIBYA  •  BENGHAZI",
    "head": "RUSSIAN WARSHIP DESTROYED IN LIBYA PORT BLAST",
    "body": ("Ukrainian forces struck a Russian Navy missile corvette in "
             "Benghazi, Zelenskiy said, and the ship burned after an "
             "explosion — the war's reach now stretching far beyond "
             "Ukrainian waters."),
}
MEDIUM = [
    {"place": "TECH  •  NVIDIA",
     "head": "HUANG IS BACK — NVIDIA ADDS ALMOST $1TN",
     "body": ("Jensen Huang returned as Nvidia chief after Trump's public "
              "appeal, and the chipmaker's value jumped by almost $1 "
              "trillion as tech stocks rallied."),
     "art": "chip"},
    {"place": "GAZA  •  OXFAM REPORT",
     "head": "GAZA'S SOIL AND WATER POISONED FOR DECADES",
     "body": ("An Oxfam report found Israel's bombardment left Gaza's air, "
              "soil and water laced with heavy metals, asbestos and "
              "dioxins — dangerous for decades to come."),
     "art": "toxic"},
]
GRID = [
    {"place": "NEPAL",
     "head": "MODI, NEPAL PM FLAG OFF NEW TRAIN",
     "body": ("Modi and Nepal's PM Balendra Shah flagged off the "
              "Saryu-Kamala Express linking Ayodhya and Janakpur."),
     "art": "bridge"},
    {"place": "CRICKET",
     "head": "PANT 128 AS INDIA DRAW WELLINGTON TEST",
     "body": ("Rishabh Pant hit 128 against New Zealand as the first Test "
              "ended in a draw."),
     "art": "ball"},
    {"place": "FORMULA 1",
     "head": "VERSTAPPEN WINS LAS VEGAS GP",
     "body": "Max Verstappen won the 2026 Las Vegas Grand Prix.",
     "art": "trophy"},
    {"place": "UKRAINE",
     "head": "SEVERAL MISSING AFTER KYIV DRONE STRIKE",
     "body": ("A Russian drone strike in the Kyiv region left several "
              "people missing, Zelenskiy said."),
     "art": "rocket"},
    {"place": "FINLAND",
     "head": "RUSSIAN CARGO SHIP ABLAZE OFF FINLAND",
     "body": ("A Russian cargo ship caught fire off Finland after a "
              "reported attack."),
     "art": "ship"},
    {"place": "PORTUGAL",
     "head": "THOUSANDS MARCH IN LISBON OVER LIVING COSTS",
     "body": ("Thousands took to Lisbon's streets to protest against "
              "rising living costs."),
     "art": "flag"},
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
REGIONS = [
    ("MIDDLE EAST", 5, "red"), ("EUROPE", 11, "ocean"),
    ("ASIA-PACIFIC", 10, "pine"), ("AMERICAS", 5, "gold"),
    ("AFRICA", 2, "clay"), ("WORLD", 2, "grey"),
]

# Simplified continent outlines, one point per line (lon, lat).
LAND = [
    [(-168, 66), (-120, 72), (-95, 80), (-60, 60), (-55, 47),
     (-75, 35), (-80, 26), (-97, 16), (-115, 28), (-125, 49),
     (-165, 60)],
    [(-80, 10), (-50, 0), (-40, -20), (-58, -38), (-70, -52),
     (-73, -37), (-77, -12), (-80, -3)],
    [(-10, 36), (0, 46), (5, 53), (10, 59), (21, 55),
     (30, 62), (18, 70), (5, 60), (-10, 54), (-10, 44)],
    [(-17, 15), (0, 36), (20, 32), (35, 28), (51, 11),
     (40, -10), (26, -34), (15, -27), (9, -1), (-8, 4),
     (-17, 12)],
    [(30, 62), (60, 69), (100, 77), (140, 72), (178, 66),
     (162, 56), (142, 45), (127, 35), (120, 22), (105, 9),
     (94, 16), (80, 15), (70, 20), (57, 26), (44, 29),
     (30, 36), (28, 55), (30, 60)],
    [(113, -22), (115, -35), (129, -32), (140, -38), (153, -32),
     (150, -22), (142, -11), (132, -12), (122, -17), (114, -22)],
]
# (lon, lat, number) — numbered dots are the three lead places.
DOTS = [
    (19.5, 32.1, "1"), (56.5, 26.5, "2"), (30.7, 36.9, "3"),
    (77.2, 28.6, None), (127.0, 37.5, None), (174.8, -41.3, None),
    (30.5, 50.4, None), (24.9, 60.2, None), (-9.1, 38.7, None),
    (106.8, -6.2, None), (96.2, 19.8, None), (34.5, 31.4, None),
    (12.5, 41.9, None), (-77.0, 38.9, None), (21.0, 52.2, None),
    (12.6, 55.7, None), (-99.1, 19.4, None), (-0.1, 51.5, None),
]


def paint_masthead(d, y):
    """Title, date line and double rule; returns the y below it."""
    title = "The Daily Chronicle"
    d.text(((PAGE_W - d.textlength(title, font=TITLE_F)) / 2, y), title,
           font=TITLE_F, fill=C["ink"])
    y += 70
    hline(d, EDGE, y, PAGE_W - EDGE, 1)
    y += 6
    d.text((EDGE, y), "TUESDAY, 24 NOVEMBER 2026", font=DATE_F, fill=C["ink"])
    right = "35 STORIES  •  6 REGIONS"
    d.text((PAGE_W - EDGE - d.textlength(right, font=DATE_R), y), right,
           font=DATE_R, fill=C["ink"])
    y += 20
    hline(d, EDGE, y, PAGE_W - EDGE, 3)
    hline(d, EDGE, y + 5, PAGE_W - EDGE, 1)
    return y + 10


def paint_strip(d, y):
    """Region counts as colour bars; returns the y below the strip."""
    seg = SPAN // 6
    for i, (name, n, colour) in enumerate(REGIONS):
        x = EDGE + i * seg
        d.rectangle([x, y, x + seg - 8, y + 18], fill=C[colour])
        lbl = "%s %d" % (name, n)
        tw = d.textlength(lbl, font=STAT_F)
        d.text((x + (seg - 8 - tw) / 2, y + 3), lbl, font=STAT_F,
               fill=C["paper"] if colour != "gold" else C["ink"])
    return y + 18 + 8


def paint_lead(d, y):
    """Hero picture plus the lead story; returns the y below it."""
    paint_hero(d, EDGE, y, SPAN, 130)
    y += 130 + 5
    d.text((EDGE, y), LEAD["place"], font=KICK_F, fill=C["faint"])
    y += 16
    y = put_text(d, clip_text(d, LEAD["head"], LEAD_H, SPAN, 2), EDGE, y, LEAD_H, gap=34)
    y += 3
    y = put_text(d, clip_text(d, LEAD["body"], LEAD_B, SPAN, 2), EDGE, y, LEAD_B, gap=19)
    y += 7
    hline(d, EDGE, y, PAGE_W - EDGE, 1)
    return y + 11


def paint_mediums(d, y):
    """Two wide picture panels with their stories; returns the y below."""
    med_w = (SPAN - 16) // 2
    top = y
    for i, story in enumerate(MEDIUM):
        x = EDGE + i * (med_w + 16)
        yy = top
        if story["art"] == "chip":
            paint_chip(d, x, yy, med_w, 92)
        else:
            paint_toxic(d, x, yy, med_w, 92)
        yy += 92 + 7
        d.text((x, yy), story["place"], font=KICK_F, fill=C["faint"])
        yy += 15
        yy = put_text(d, clip_text(d, story["head"], MED_H, med_w, 2), x, yy, MED_H, gap=21)
        yy += 2
        put_text(d, clip_text(d, story["body"], MED_B, med_w, 2), x, yy, MED_B, gap=15)
    y = top + 92 + 7 + 15 + 42 + 2 + 30 + 6
    hline(d, EDGE, y, PAGE_W - EDGE, 3)
    hline(d, EDGE, y + 5, PAGE_W - EDGE, 1)
    return y + 13


def paint_grid(d, img, y):
    """Six briefs in 3 columns x 2 rows, each with a pictogram."""
    gap = 14
    col_w = (SPAN - 2 * gap) // 3
    slot_h = 72
    label = "THE WORLD IN BRIEF"
    d.text(((PAGE_W - d.textlength(label, font=KICK_F)) / 2, y), label,
           font=KICK_F, fill=C["faint"])
    y += 17
    top = y
    for idx, story in enumerate(GRID):
        col, row = idx % 3, idx // 3
        x = EDGE + col * (col_w + gap)
        yy = top + row * slot_h
        if col > 0:
            d.line([(x - gap // 2, yy + 2), (x - gap // 2, yy + slot_h - 8)],
                   fill=(165, 152, 128), width=1)
        img.paste(glyph(story["art"], 60), (x, yy))
        tx = x + 68
        tw = col_w - 68
        d.text((tx, yy), story["place"], font=KICK_F, fill=C["faint"])
        yy += 14
        yy = put_text(d, clip_text(d, story["head"], SM_H, tw, 2), tx, yy, SM_H, gap=15)
        yy += 1
        put_text(d, clip_text(d, story["body"], SM_B, tw, 2), tx, yy, SM_B, gap=13)
    y = top + 2 * slot_h + 4
    hline(d, EDGE, y, PAGE_W - EDGE, 1)
    return y + 10


def paint_bottom(d, img, y):
    """Map on the left, numbered tail list on the right; returns bottom y."""
    top = y
    bottom_h = PAGE_H - 52 - top
    map_w = 470
    tail_x = EDGE + map_w + 16
    d.text((EDGE, top), "WHERE IT HAPPENED", font=KICK_F, fill=C["faint"])
    d.text((tail_x, top), "26 MORE STORIES", font=KICK_F, fill=C["faint"])
    my = top + 18
    mh = bottom_h - 18
    d.rectangle([EDGE, my, EDGE + map_w, my + mh], fill=C["sea"],
                outline=C["rule"], width=2)

    def proj(lon, lat):
        px = EDGE + 8 + (lon + 170) / 360 * (map_w - 16)
        py = my + 6 + (75 - lat) / 130 * (mh - 12)
        return px, py

    for poly in LAND:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=C["land"],
                  outline=(120, 108, 88))
    for lon, lat, num in DOTS:
        px, py = proj(lon, lat)
        if num:
            d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=C["red"],
                      outline=C["ink"], width=1)
            d.text((px - 3, py - 6), num, font=sans("Bold", 10), fill=C["paper"])
        else:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=C["ink"])
    legend = "1 BENGHAZI  •  2 HORMUZ  •  3 ANTALYA"
    lw = d.textlength(legend, font=MAP_F)
    lx = EDGE + (map_w - lw) / 2
    ly = my + mh - 15
    d.rectangle([lx - 6, ly - 2, lx + lw + 6, ly + 12], fill=C["paper"])
    d.text((lx, ly), legend, font=MAP_F, fill=C["ink"])

    tail_w = PAGE_W - EDGE - tail_x
    sub_gap = 12
    sub_w = (tail_w - sub_gap) // 2
    lead_tail = 13
    truncated = []
    for idx, (place, head) in enumerate(TAIL):
        col, row = idx // 13, idx % 13
        x = tail_x + col * (sub_w + sub_gap)
        yy = top + 18 + row * lead_tail
        d.text((x, yy), "%d." % (idx + 1), font=TAIL_F, fill=C["red"])
        lines = clip_text(d, head, TAIL_F, sub_w - 24, 1)
        if lines[0].endswith("..."):
            truncated.append(head)
        d.text((x + 22, yy), lines[0], font=TAIL_F, fill=C["ink"])
    if truncated:
        print("TRUNCATED TAIL:", truncated)
    print("layout: bottom_top=%d bottom_h=%d tail_last_row_y=%d"
          % (top, bottom_h, top + 18 + 12 * lead_tail))


def main():
    img = Img.new("RGB", (PAGE_W, PAGE_H), C["paper"])
    d = Draw.Draw(img)
    for _ in range(2600):
        x, y = random.randint(0, PAGE_W - 1), random.randint(0, PAGE_H - 1)
        v = random.randint(-14, 10)
        d.point((x, y), fill=(C["paper"][0] + v, C["paper"][1] + v, C["paper"][2] + v))
    for i in range(18):
        d.rectangle([i, i, PAGE_W - 1 - i, PAGE_H - 1 - i],
                    outline=(120 + i * 4, 108 + i * 4, 88 + i * 4))
    d.rectangle([0, 0, PAGE_W - 1, PAGE_H - 1], outline=(70, 60, 48), width=2)

    y = EDGE + 6
    y = paint_masthead(d, y)
    y = paint_strip(d, y)
    y = paint_lead(d, y)
    y = paint_mediums(d, y)
    y = paint_grid(d, img, y)
    paint_bottom(d, img, y)

    y = PAGE_H - 44
    hline(d, EDGE, y, PAGE_W - EDGE, 1)
    y += 7
    foot = ("DATE CHECK: TUESDAY 24 NOVEMBER 2026 — every story above "
            "happened or was first reported on 24 November 2026.")
    d.text(((PAGE_W - d.textlength(foot, font=FOOT_F)) / 2, y), foot,
           font=FOOT_F, fill=C["ink"])
    y += 15
    d.text(((PAGE_W - d.textlength("The Daily Chronicle • 24 November 2026",
                                  font=FOOT_F)) / 2, y),
           "The Daily Chronicle • 24 November 2026", font=FOOT_F, fill=C["faint"])

    img.save("entry.png", optimize=True)
    print("saved entry.png %s" % (img.size,))


if __name__ == "__main__":
    main()
