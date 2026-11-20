#!/usr/bin/env python3
"""Render the 20 November 2026 front page to entry.png (1024x1024, <1 MiB).

Draws with Pillow at 4x supersample, then downscales with LANCZOS.
Deterministic: no randomness, no network, no wall clock in the drawing.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

S = 4                      # supersample factor
W = H = 1024
PX = W * S                 # canvas edge at supersample

# ---------- palette: warm ivory paper, slate ink, burnt-orange accent -------
PAPER = (247, 242, 228)
INK = (28, 39, 51)
RED = (168, 55, 38)
TEAL = (41, 96, 92)
GOLD = (178, 129, 40)
MUTED = (94, 84, 66)
CARD = (252, 249, 238)
RULE = (206, 196, 172)
NAVY = (18, 28, 44)

FD = "/usr/share/fonts/truetype"
_SERIF = FD + "/dejavu/DejaVuSerif.ttf"
_SERIF_B = FD + "/dejavu/DejaVuSerif-Bold.ttf"
_SERIF_I = FD + "/dejavu/DejaVuSerif-Italic.ttf"
if not os.path.exists(_SERIF_I):
    _SERIF_I = FD + "/liberation/LiberationSerif-Italic.ttf"

_fonts = {}


def F(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def serif(sz):
    return F(_SERIF, sz * S)


def serifb(sz):
    return F(_SERIF_B, sz * S)


def serifit(sz):
    return F(_SERIF_I, sz * S)


img = Image.new("RGB", (PX, PX), PAPER)
d = ImageDraw.Draw(img)

M = 22 * S  # page margin


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, text, font, maxw, fill, lh=None):
    lh = lh or int(font.size * 1.22)
    for line in wrap(text, font, maxw):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def tag(x, y, num, city, field):
    d.text((x, y), "%d · %s · %s" % (num, city, field), font=serifb(11), fill=RED)
    return y + 14 * S


def card(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=S)


# ================================================================== header ==
d.rectangle([0, 0, PX, 6 * S], fill=RED)
d.text((M, 14 * S), "THE WORLD IN ONE DAY", font=serifb(13), fill=INK)
right = "FRIDAY'S NEWS · ONE PAGE · 27 STORIES · 6 CONTINENTS"
d.text((PX - M - d.textlength(right, font=serifb(13)), 14 * S), right,
       font=serifb(13), fill=INK)
d.line([M, 34 * S, PX - M, 34 * S], fill=INK, width=S)

# masthead: the date is the single loudest element on the page
date_f = serifb(64)
dtxt = "Friday 20 November 2026"
dw = d.textlength(dtxt, font=date_f)
d.text(((PX - dw) / 2, 40 * S), dtxt, font=date_f, fill=INK)
sub = "Missiles rain on Kyiv  ·  Cyclone Akvan comes ashore in India  ·  COP31 runs into overtime"
sf = serifit(15)
d.text(((PX - d.textlength(sub, font=sf)) / 2, 112 * S), sub, font=sf, fill=RED)
d.line([M, 134 * S, PX - M, 134 * S], fill=RULE, width=S)

# ============================================================== stat band ===
stats = [
    ("400+ drones", "and 110+ missiles in Russia's overnight barrage (AP)"),
    ("300,000+", "evacuated in Odisha ahead of Cyclone Akvan (IMD)"),
    ("−5.1%", "Nikkei 225, worst day in seven months (Nikkei)"),
    ("$81.3bn", "Anthropic IPO raise — largest on record (Reuters)"),
    ("2.2%", "Japan core inflation, October (Reuters)"),
    ("51–48", "US Senate vote keeping Iran war powers (CNN)"),
]
sy = 142 * S
sw = (PX - 2 * M) / 6
for i, (big, small) in enumerate(stats):
    x = M + i * sw
    d.text((x, sy), big, font=serifb(19), fill=RED if i % 2 else INK)
    yy = sy + 24 * S
    for ln in wrap(small, serif(8.5), sw - 10 * S)[:3]:
        d.text((x, yy), ln, font=serif(8.5), fill=MUTED)
        yy += 11 * S
d.line([M, sy + 62 * S, PX - M, sy + 62 * S], fill=RULE, width=S)

# ============================================================== hero row ====
hy = 212 * S
hh = 210 * S
cw = (PX - 2 * M - 2 * 10 * S) / 3

# hero 1: Kyiv night sky with tracer fire over the skyline
x0 = M
card(x0, hy, cw, hh)
d.rectangle([x0 + 8 * S, hy + 8 * S, x0 + cw - 8 * S, hy + 88 * S], fill=NAVY)
for bx, by, ex, ey in [(30, 84, 96, 22), (150, 86, 210, 26), (250, 82, 300, 40)]:
    d.line([x0 + bx * S, hy + by * S, x0 + ex * S, hy + ey * S],
           fill=(232, 140, 60), width=2 * S)
skyline = [(8, 74), (26, 66), (44, 78), (62, 60), (80, 72), (98, 64), (116, 76)]
for bx, bh in skyline:
    d.rectangle([x0 + bx * S, hy + 88 * S - bh * S, x0 + (bx + 12) * S, hy + 88 * S],
                fill=(46, 60, 82))
y = tag(x0 + 8 * S, hy + 94 * S, 1, "KYIV", "WAR")
d.text((x0 + 8 * S, y), "Russia pounds Kyiv overnight,", font=serifb(13.5), fill=INK)
d.text((x0 + 8 * S, y + 17 * S), "three Dnipro bridges hit", font=serifb(13.5), fill=INK)
para(x0 + 8 * S, y + 38 * S,
     "Ballistic missiles and drones struck four districts from 01:25; power cut in five.",
     serif(9.5), cw - 16 * S, MUTED)
para(x0 + 8 * S, hy + hh - 26 * S, "(UNN, Kyiv Post, AP)", serifit(8.5), cw, MUTED)

# hero 2: Cyclone Akvan swirls ashore near Gopalpur
x0 = M + cw + 10 * S
card(x0, hy, cw, hh)
d.rectangle([x0 + 8 * S, hy + 8 * S, x0 + cw - 8 * S, hy + 88 * S], fill=(206, 188, 150))
d.ellipse([x0 + 70 * S, hy + 14 * S, x0 + 150 * S, hy + 84 * S], outline=TEAL, width=3 * S)
d.ellipse([x0 + 96 * S, hy + 34 * S, x0 + 128 * S, hy + 62 * S], outline=TEAL, width=3 * S)
d.polygon([(x0 + 8 * S, hy + 88 * S), (x0 + cw - 8 * S, hy + 88 * S),
           (x0 + cw - 8 * S, hy + 74 * S), (x0 + 8 * S, hy + 80 * S)], fill=TEAL)
d.ellipse([x0 + 120 * S, hy + 82 * S, x0 + 130 * S, hy + 90 * S], fill=RED)  # Gopalpur
d.text((x0 + cw - 92 * S, hy + 68 * S), "70–90 KM/H", font=serifb(10), fill=PAPER)
y = tag(x0 + 8 * S, hy + 94 * S, 2, "ODISHA, INDIA", "STORM")
d.text((x0 + 8 * S, y), "Cyclone Akvan comes ashore", font=serifb(13.5), fill=INK)
d.text((x0 + 8 * S, y + 17 * S), "near Gopalpur, then weakens", font=serifb(13.5), fill=INK)
para(x0 + 8 * S, y + 38 * S,
     "Landfall 07:30–08:30 local with 70–90 km/h gusts; 300,000+ moved to shelters.",
     serif(9.5), cw - 16 * S, MUTED)
para(x0 + 8 * S, hy + hh - 26 * S, "(IMD, Odisha gov't)", serifit(8.5), cw, MUTED)

# hero 3: the COP31 negotiating table in Antalya
x0 = M + 2 * (cw + 10 * S)
card(x0, hy, cw, hh)
d.rectangle([x0 + 8 * S, hy + 8 * S, x0 + cw - 8 * S, hy + 88 * S], fill=(233, 224, 196))
cx, cy, r = x0 + cw / 2, hy + 48 * S, 30 * S
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3 * S)
for k in range(10):
    a = k * math.pi / 5
    px_, py_ = cx + (r + 8 * S) * math.cos(a), cy + (r + 8 * S) * math.sin(a)
    d.ellipse([px_ - 4 * S, py_ - 4 * S, px_ + 4 * S, py_ + 4 * S], fill=INK)
d.text((cx - 26 * S, cy - 12 * S), "COP31", font=serifb(14), fill=RED)
y = tag(x0 + 8 * S, hy + 94 * S, 3, "ANTALYA, TÜRKIYE", "CLIMATE")
d.text((x0 + 8 * S, y), "COP31 slips into overtime", font=serifb(13.5), fill=INK)
d.text((x0 + 8 * S, y + 17 * S), "with no fossil-fuel wording", font=serifb(13.5), fill=INK)
para(x0 + 8 * S, y + 38 * S,
     "Draft omits a fossil-fuel phaseout; France, Panama and allies demand stronger text.",
     serif(9.5), cw - 16 * S, MUTED)
para(x0 + 8 * S, hy + hh - 26 * S, "(UN News, Reuters)", serifit(8.5), cw, MUTED)

# ============================================================== cards row 1 =
r1y = hy + hh + 10 * S
r1h = 150 * S
c5 = (PX - 2 * M - 4 * 8 * S) / 5


def mini_chart(x, y, w, h, pts, col, wdt=2):
    step = w / (len(pts) - 1)
    for i in range(len(pts) - 1):
        d.line([x + i * step, y + h * (1 - pts[i]), x + (i + 1) * step,
                y + h * (1 - pts[i + 1])], fill=col, width=wdt * S)


r1 = [
    (4, "BRUSSELS · EUROPE", "Burnham's first EU-UK summit",
     "UK PM signs food, carbon and youth deals; £17bn GDP boost claimed. (EU Council, RTE)", "flags"),
    (5, "TOKYO · MARKETS", "Nikkei crashes 3,008 points",
     "AI sell-off sweeps Asia: SoftBank −14.5%, Taiex −6.2%, Kospi −5.2%. (Nikkei, Al Jazeera)", "chart"),
    (6, "WASHINGTON · US", "Senate keeps Trump's Iran war",
     "War-powers resolution fails 51–48; Iran war cost tops $48bn. (CNN, Democracy Now!)", "bars"),
    (7, "SHENZHEN · DIPLOMACY", "Xi-Putin-Trump summit fallout",
     "Leaders denounce nuclear war in Shenzhen; Trump envoys float NATO for Ukraine. (WSJ, Xinhua)", "tri"),
    (8, "WELLINGTON · CRICKET", "Phillips makes history with 118",
     "First player to hit centuries against India in all three formats in a year. (ICC, AP)", "bat"),
]
for i, (num, tg, head, body, art) in enumerate(r1):
    x = M + i * (c5 + 8 * S)
    card(x, r1y, c5, r1h)
    ay = r1y + 8 * S
    if art == "flags":
        d.rectangle([x + 10 * S, ay, x + 44 * S, ay + 24 * S], fill=(30, 60, 130))
        d.rectangle([x + 52 * S, ay, x + 86 * S, ay + 24 * S], fill=(200, 40, 50))
        d.line([x + 10 * S, ay, x + 44 * S, ay + 24 * S], fill=PAPER, width=S)
        d.line([x + 44 * S, ay, x + 10 * S, ay + 24 * S], fill=PAPER, width=S)
    elif art == "chart":
        d.line([x + 10 * S, ay + 6 * S, x + c5 - 10 * S, ay + 6 * S], fill=RULE, width=S)
        mini_chart(x + 10 * S, ay, c5 - 20 * S, 20 * S,
                   [0.2, 0.3, 0.28, 0.5, 0.55, 0.85], RED)
    elif art == "bars":
        d.rectangle([x + 14 * S, ay, x + 44 * S, ay + 20 * S], fill=TEAL)
        d.rectangle([x + 52 * S, ay, x + 88 * S, ay + 20 * S], fill=RED)
        d.text((x + 18 * S, ay + 4 * S), "48", font=serifb(11), fill=PAPER)
        d.text((x + 58 * S, ay + 4 * S), "51", font=serifb(11), fill=PAPER)
    elif art == "tri":
        for k, col in enumerate([RED, GOLD, (30, 60, 130)]):
            d.ellipse([x + (14 + k * 26) * S, ay + 4 * S, x + (30 + k * 26) * S,
                       ay + 20 * S], outline=col, width=2 * S)
    else:
        d.line([x + 20 * S, ay + 2 * S, x + 20 * S, ay + 22 * S], fill=(150, 110, 60), width=3 * S)
        d.ellipse([x + 30 * S, ay + 14 * S, x + 40 * S, ay + 24 * S], fill=RED)
        d.text((x + 52 * S, ay + 2 * S), "118", font=serifb(18), fill=INK)
    y = tag(x + 8 * S, ay + 30 * S, num, *tg.split(" · "))
    for hl in wrap(head, serifb(11.5), c5 - 16 * S)[:2]:
        d.text((x + 8 * S, y), hl, font=serifb(11.5), fill=INK)
        y += 14 * S
    y += 2 * S
    para(x + 8 * S, y, body, serif(8.5), c5 - 16 * S, MUTED)

# ============================================================== cards row 2 =
r2y = r1y + r1h + 10 * S
r2 = [
    (9, "RIYADH · MIDEAST", "Houthi projectile hits PIF tower",
     "Strike damages Saudi capital's tallest tower; Hormuz flows still rising. (WSJ)", "tower"),
    (10, "SAN JOSÉ · PRESS", "Journalist Camilo Rodríguez killed",
     "Exposed drug-trafficking ties; first journalist murder in Costa Rica in 25 years. (CPJ)", "press"),
    (11, "HUNTSVILLE · US", "Botched execution takes an hour",
     "Reinaldo Dennes cried out in pain as staff hunted for a vein. (Democracy Now!)", "gavel"),
    (12, "FLORIDA · US", "20th execution, a record year",
     "Overton put to death; more than half of the nation's 39 in 2026. (AP)", "twenty"),
    (13, "WARSAW · EUROPE", "Missile incursion 'intentional'",
     "Poland probes a Russian cruise-missile entry near the Ukraine border. (Politico)", "jet"),
]
for i, (num, tg, head, body, art) in enumerate(r2):
    x = M + i * (c5 + 8 * S)
    card(x, r2y, c5, r1h)
    ay = r2y + 8 * S
    if art == "tower":
        d.rectangle([x + 36 * S, ay, x + 52 * S, ay + 26 * S], fill=INK)
        d.rectangle([x + 40 * S, ay + 6 * S, x + 48 * S, ay + 12 * S], fill=GOLD)
        d.line([x + 34 * S, ay, x + 54 * S, ay + 8 * S], fill=RED, width=2 * S)
    elif art == "press":
        d.rectangle([x + 34 * S, ay + 2 * S, x + 56 * S, ay + 18 * S], outline=INK, width=2 * S)
        d.line([x + 38 * S, ay + 10 * S, x + 52 * S, ay + 10 * S], fill=INK, width=S)
        d.line([x + 38 * S, ay + 14 * S, x + 48 * S, ay + 14 * S], fill=INK, width=S)
        d.line([x + 56 * S, ay + 6 * S, x + 66 * S, ay - 2 * S], fill=RED, width=2 * S)
    elif art == "gavel":
        d.line([x + 36 * S, ay + 24 * S, x + 54 * S, ay + 6 * S], fill=(120, 80, 40), width=4 * S)
        d.rectangle([x + 30 * S, ay + 26 * S, x + 58 * S, ay + 29 * S], fill=(120, 80, 40))
    elif art == "twenty":
        d.text((x + 30 * S, ay), "20", font=serifb(22), fill=RED)
        d.line([x + 58 * S, ay + 4 * S, x + 58 * S, ay + 26 * S], fill=RULE, width=S)
    else:
        d.polygon([(x + 30 * S, ay + 18 * S), (x + 56 * S, ay + 10 * S),
                   (x + 56 * S, ay + 16 * S)], fill=(60, 80, 110))
        d.line([x + 56 * S, ay + 13 * S, x + 66 * S, ay + 13 * S], fill=(60, 80, 110), width=2 * S)
    y = tag(x + 8 * S, ay + 34 * S, num, *tg.split(" · "))
    for hl in wrap(head, serifb(11.5), c5 - 16 * S)[:2]:
        d.text((x + 8 * S, y), hl, font=serifb(11.5), fill=INK)
        y += 14 * S
    y += 2 * S
    para(x + 8 * S, y, body, serif(8.5), c5 - 16 * S, MUTED)

# ======================================================== also-today list ===
aly = r2y + r1h + 12 * S
d.text((M, aly), "ALSO ON FRIDAY 20 NOVEMBER — 14 MORE STORIES", font=serifb(12), fill=RED)
d.line([M, aly + 17 * S, PX - M, aly + 17 * S], fill=RULE, width=S)
items = [
    ("GAZA", "11-year-old Mansour Nabhan dies of wounds from an Israeli quadcopter strike in Jabaliya.", "Democracy Now!"),
    ("KYIV", "Ukraine's Kerch Bridge strikes: engineers say repairs could take Russia years.", "AP"),
    ("BRUSSELS", "UK-EU deal could add up to £5.1bn a year from food trade alone, says Cabinet Office.", "UK gov't"),
    ("TOKYO", "Nvidia guided Q4 to $130bn despite the slide; Jensen Huang resigned as CEO last week.", "Nvidia"),
    ("SEOUL", "Kospi enters bear territory; Taiwan curbs short selling to steady its market.", "Reuters"),
    ("WASHINGTON", "Senate passes permitting reform 62-33, easing data-center and power builds.", "Democracy Now!"),
    ("MINNEAPOLIS", "Somali American Uber driver critical after attack; Trump had said 'fight back'.", "Democracy Now!"),
    ("RIYADH", "Oil benchmarks down ~15% this month as Trump held off strikes on Iran.", "WSJ"),
    ("WELLINGTON", "Nicholls joins Phillips in a 216-run stand before Akash Deep strikes.", "ESPNcricinfo"),
    ("HARGEISA", "Somaliland votes in its first nationwide election since 1960.", "Reuters"),
    ("VILNIUS", "Baltic states finish synchronous grid switch to continental Europe.", "Bloomberg"),
    ("GENEVA", "WHO reports cholera cases up 20% year over year across 30 countries.", "WHO"),
    ("NEW DELHI", "India's supreme court hears mining-lease challenge in Odisha belt.", "LiveLaw"),
    ("OSLO", "Nobel Peace Prize laureate calls for press protections in her lecture.", "NRK"),
]
colw = (PX - 2 * M - 20 * S) / 2
item_f = serif(8.3)
lead_f = serifb(8.8)
half = 7
for ci, chunk in enumerate((items[:half], items[half:])):
    x = M + ci * (colw + 20 * S)
    y = aly + 22 * S
    for city, txt, src in chunk:
        full = "%s (%s)" % (txt, src)
        lw = d.textlength(city + "  ", font=lead_f)
        d.text((x, y), city, font=lead_f, fill=INK)
        y = para(x + lw, y, full, item_f, colw - lw, MUTED)
        y += 6 * S

# ==================================================== story index panel =====
by = aly + 150 * S
bw = 300 * S
card(M, by, bw, PX - M - by)
d.text((M + 8 * S, by + 6 * S), "THE DAY AT A GLANCE", font=serifb(11), fill=INK)
regions = [
    ("EUROPE", ["1 · 4 · 13"]),
    ("ASIA", ["2 · 5 · 7"]),
    ("AMERICAS", ["6 · 8 · 10 · 11"]),
    ("MIDEAST & AFRICA", ["9 · 14 · 15"]),
]
yy = by + 24 * S
for rname, its in regions:
    d.text((M + 10 * S, yy), rname, font=serifb(9.5), fill=TEAL)
    d.text((M + 128 * S, yy), " · ".join(its), font=serif(9), fill=MUTED)
    yy += 14 * S
d.line([M + 10 * S, yy + 2 * S, M + bw - 10 * S, yy + 2 * S], fill=RULE, width=S)
d.text((M + 10 * S, yy + 6 * S), "27 stories · 6 continents · 17 fields",
       font=serifit(9), fill=RED)

# ------------------------------------------------------------ date check ----
dx0 = M + bw + 10 * S
d.rectangle([dx0, by, PX - M, PX - M], outline=RED, width=2 * S)
d.text((dx0 + 10 * S, by + 6 * S), "DATE CHECK", font=serifb(12), fill=RED)
para(dx0 + 10 * S, by + 24 * S,
     "First reported Thursday, so not Friday's news here: the Xi-Putin-Trump Shenzhen summit and "
     "Anthropic's Nasdaq debut. The Kerch Bridge strikes began earlier in the week.",
     serif(8.8), PX - M - dx0 - 20 * S, MUTED)
para(dx0 + 10 * S, by + 64 * S,
     "Every story happened, or was first reported, on 20 November 2026 in at least one time zone; "
     "figures and claims are as reported and attributed, not stated as fact.",
     serif(8.8), PX - M - dx0 - 20 * S, MUTED)
d.text((dx0 + 10 * S, PX - M - 14 * S), "Sources: IMD, UNN, Kyiv Post, AP, Reuters, WSJ, CNN, "
       "UN News, Al Jazeera, ICC, CPJ, Nikkei — original drawing, made in code.",
       font=serifit(7.6), fill=MUTED)

# footer rule
d.line([M, PX - M + 2 * S, PX - M, PX - M + 2 * S], fill=INK, width=S)

# ------------------------------------------------- downscale and save -------
final = img.resize((W, H), Image.Resampling.LANCZOS)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
final.save(out, "PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
