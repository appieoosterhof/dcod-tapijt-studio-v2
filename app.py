"""
RepeatTile Studio — Tapijt Dessin Generator
Backend server (Flask + Python)
"""

import os
import json
import math
import time
import base64
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import base64
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import anthropic
from PIL import Image, ImageDraw
from modules_extra import generate_strepen_svg, generate_mozaiek_svg, generate_chevron_svg, generate_hexagoon_svg, generate_ogee_svg, generate_diamant_svg, generate_terrazzo_svg, generate_vrije_vormen_svg, generate_visgraat_svg, generate_dots_svg, generate_visgraat_lijn_svg, generate_bamboe_svg, generate_artdeco_svg, generate_chevron_bold_svg, generate_houndstooth_svg, generate_urban_plaid_svg
from modules_extra import generate_artdeco_svg, generate_artdeco_hex_svg
from modules_extra import generate_hoogtelijnen_svg

app = Flask(__name__)
CORS(app)

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

# ─── AI analyse ──────────────────────────────────────────────────────────────

def analyse_prompt(prompt: str, api_key: str) -> dict:
    """Stuur de gebruikersprompt naar Claude voor stijlanalyse."""
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[{
            "role": "user",
            "content": f"""Je bent een expert in tapijt- en textielontwerp.
Analyseer de volgende dessin-prompt en geef ALLEEN een JSON-object terug (geen uitleg, geen markdown):

{{
  "style": "geometric|floral|medallion|tribal|abstract|botanical|nordic|persian",
  "palette": {{
    "background": "#hexkleur",
    "primary": "#hexkleur",
    "secondary": "#hexkleur",
    "accent1": "#hexkleur",
    "accent2": "#hexkleur"
  }},
  "complexity": "low|medium|high",
  "motif_size": "small|medium|large",
  "shapes": ["circle|square|triangle|diamond|hexagon|star|cross|leaf|flower"],
  "description_nl": "Korte feitelijke beschrijving van het dessin in het Nederlands",
  "sfeer_nl": ["woord1", "woord2", "woord3"],
  "geschikt_voor_nl": ["ruimte1", "ruimte2", "ruimte3"],
  "ontwerpvisie_nl": "Een of twee korte, verkopende zinnen over de inspiratie en het gevoel van dit dessin (bv. waarop het is geinspireerd en welke beleving het geeft). Niet de vormen beschrijven."
}}

Voor sfeer_nl: drie korte sfeerwoorden (bv. Rustgevend, Organisch, Architectonisch).
Voor geschikt_voor_nl: drie passende commerciele toepassingen (bv. Hotel, Kantoor, Zorg, Entree, Retail, Bibliotheek, Onderwijs).

Prompt: "{prompt}"

BELANGRIJK voor shapes: analyseer welke geometrische vormen de gebruiker wil.
- "alleen cirkels" of "cirkels" → ["circle"]
- "ruiten" of "diamanten" → ["diamond"]
- "sterren" → ["star"]
- "bloemen" → ["flower"]
- Niet gespecificeerd → kies passende vormen bij de stijl

Zorg dat de kleuren exact passen bij de beschrijving.
Bij 'Marokkaans' gebruik warme terracotta/goud tonen.
Bij 'Nordic' gebruik blauw/wit/grijs. Bij 'Perzisch' gebruik donkerblauw/rood/goud.
Gebruik ALTIJD exact dezelfde hexkleuren — geen variaties per tegel."""
        }]
    )
    text = message.content[0].text.strip()
    # Verwijder eventuele markdown-backticks
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


# ─── SVG patroon generators ───────────────────────────────────────────────────

def hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def generate_geometric_svg(palette: dict, tile_size: int, complexity: str, shape_list: list = None) -> str:
    T = tile_size
    bg = palette["background"]
    c1 = palette["primary"]
    c2 = palette["secondary"]
    c3 = palette["accent1"]
    c4 = palette["accent2"]
    step = T // 3 if complexity == "high" else T // 2 if complexity == "medium" else T // 2
    if not shape_list:
        shape_list = ["octagon"]
    svgs = []
    colors = [c1, c2, c3, c4]
    for row in range(0, T, step):
        for col in range(0, T, step):
            cx, cy = col + step // 2, row + step // 2
            r = step * 0.42
            idx = (row // step + col // step) % len(colors)
            fill = colors[idx]
            shape = shape_list[(row // step * (T // step) + col // step) % len(shape_list)]

            if shape == "circle":
                svgs.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')
                svgs.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.4:.1f}" fill="{bg}" stroke="{c2}" stroke-width="0.5"/>')

            elif shape == "square":
                x0, y0 = cx - r, cy - r
                svgs.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{r*2:.1f}" height="{r*2:.1f}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')
                svgs.append(f'<rect x="{cx-r*0.4:.1f}" y="{cy-r*0.4:.1f}" width="{r*0.8:.1f}" height="{r*0.8:.1f}" fill="{bg}" stroke="{c2}" stroke-width="0.5"/>')

            elif shape == "triangle":
                pts = f"{cx:.1f},{cy-r:.1f} {cx+r:.1f},{cy+r:.1f} {cx-r:.1f},{cy+r:.1f}"
                svgs.append(f'<polygon points="{pts}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')

            elif shape == "diamond":
                pts = f"{cx:.1f},{cy-r:.1f} {cx+r:.1f},{cy:.1f} {cx:.1f},{cy+r:.1f} {cx-r:.1f},{cy:.1f}"
                svgs.append(f'<polygon points="{pts}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')
                ri = r * 0.45
                inner = f"{cx:.1f},{cy-ri:.1f} {cx+ri:.1f},{cy:.1f} {cx:.1f},{cy+ri:.1f} {cx-ri:.1f},{cy:.1f}"
                svgs.append(f'<polygon points="{inner}" fill="{bg}" stroke="{c2}" stroke-width="0.5"/>')

            elif shape == "hexagon":
                pts = []
                for k in range(6):
                    angle = math.radians(k * 60 + 30)
                    pts.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
                svgs.append(f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')

            elif shape == "star":
                pts = []
                for k in range(10):
                    angle = math.radians(k * 36 - 90)
                    rad = r if k % 2 == 0 else r * 0.45
                    pts.append(f"{cx + rad * math.cos(angle):.1f},{cy + rad * math.sin(angle):.1f}")
                svgs.append(f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')

            else:
                # Standaard achthoek
                pts = []
                for k in range(8):
                    angle = math.radians(k * 45 + 22.5)
                    pts.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
                fill2 = c1 if (row // step + col // step) % 2 == 0 else c3
                svgs.append(f'<polygon points="{" ".join(pts)}" fill="{fill2}" stroke="{c2}" stroke-width="1"/>')
                ri = r * 0.45
                inner = [f"{cx:.1f},{cy-ri:.1f}", f"{cx+ri:.1f},{cy:.1f}", f"{cx:.1f},{cy+ri:.1f}", f"{cx-ri:.1f},{cy:.1f}"]
                svgs.append(f'<polygon points="{" ".join(inner)}" fill="{c4}" stroke="{c2}" stroke-width="0.5"/>')
                svgs.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.12:.1f}" fill="{c2}"/>')

    return "\n".join(svgs)


def generate_floral_svg(palette: dict, tile_size: int, complexity: str) -> str:
    """Rijk botanisch bloemmotief: gelaagde bloemblaadjes, blaadjes rondom,
    een gedetailleerd hart en kleine knopjes als opvulling. Naadloos: de
    hoofdbloemen staan binnen hun cel en de knopjes op de gedeelde celhoeken
    (incl. randen), zodat het patroon rondom aansluit."""
    T = tile_size
    bg = palette["background"]
    c1 = palette["primary"]
    c2 = palette["secondary"]
    c3 = palette["accent1"]
    c4 = palette["accent2"]
    cols = {"low": 2, "medium": 3, "high": 3}.get(complexity, 3)
    step = T / cols
    shapes = []

    def blad(cx, cy, lengte, ang, kleur):
        dx = lengte * math.cos(math.radians(ang))
        dy = lengte * math.sin(math.radians(ang))
        ex = cx + dx
        ey = cy + dy
        px = -dy * 0.5
        py = dx * 0.5
        d = "M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z" % (
            cx, cy, cx + dx * 0.5 + px, cy + dy * 0.5 + py, ex, ey,
            cx + dx * 0.5 - px, cy + dy * 0.5 - py, cx, cy)
        shapes.append('<path d="%s" fill="%s" opacity="0.9"/>' % (d, kleur))
        shapes.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.8" opacity="0.5"/>' % (cx, cy, ex, ey, c2))

    def bloem(cx, cy, r, buiten, binnen):
        for a in (45, 135, 225, 315):
            blad(cx, cy, r * 1.2, a, c2)
        for kk in range(8):
            a = math.radians(kk * 45)
            px = cx + r * 0.55 * math.cos(a)
            py = cy + r * 0.55 * math.sin(a)
            shapes.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="0.92" transform="rotate(%.1f %.1f %.1f)"/>' % (
                px, py, r * 0.30, r * 0.46, buiten, math.degrees(a), px, py))
        for kk in range(8):
            a = math.radians(kk * 45 + 22.5)
            px = cx + r * 0.34 * math.cos(a)
            py = cy + r * 0.34 * math.sin(a)
            shapes.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="0.95" transform="rotate(%.1f %.1f %.1f)"/>' % (
                px, py, r * 0.18, r * 0.30, binnen, math.degrees(a) + 22.5, px, py))
        shapes.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r * 0.22, c4))
        for kk in range(6):
            a = math.radians(kk * 60)
            shapes.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (
                cx + r * 0.12 * math.cos(a), cy + r * 0.12 * math.sin(a), r * 0.04, c2))
        shapes.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r * 0.07, c2))

    def knop(cx, cy, r, kleur):
        for kk in range(5):
            a = math.radians(kk * 72 - 90)
            px = cx + r * 0.5 * math.cos(a)
            py = cy + r * 0.5 * math.sin(a)
            shapes.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="0.9" transform="rotate(%.1f %.1f %.1f)"/>' % (
                px, py, r * 0.30, r * 0.44, kleur, math.degrees(a) + 90, px, py))
        shapes.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r * 0.24, c4))

    for row in range(cols):
        for col in range(cols):
            cx = col * step + step / 2
            cy = row * step + step / 2
            r = step * 0.40
            if (row + col) % 2 == 0:
                bloem(cx, cy, r, c1, c3)
            else:
                bloem(cx, cy, r, c3, c1)
    for row in range(cols + 1):
        for col in range(cols + 1):
            knop(col * step, row * step, step * 0.17, c4)
    return "\n".join(shapes)

def generate_medallion_svg(palette: dict, tile_size: int, complexity: str) -> str:
    T = tile_size
    c1 = palette["primary"]
    c2 = palette["secondary"]
    c3 = palette["accent1"]
    c4 = palette["accent2"]
    cx, cy = T // 2, T // 2
    shapes = []
    # Buitenste border
    shapes.append(f'<rect x="4" y="4" width="{T-8}" height="{T-8}" fill="none" stroke="{c2}" stroke-width="3"/>')
    shapes.append(f'<rect x="10" y="10" width="{T-20}" height="{T-20}" fill="none" stroke="{c1}" stroke-width="1.5"/>')
    # Centrale medallion
    layers = [0.45, 0.35, 0.25, 0.15]
    colors = [c1, c3, c2, c4]
    for i, (ratio, color) in enumerate(zip(layers, colors)):
        r = T * ratio
        pts = []
        sides = 12 if complexity == "high" else 8
        for k in range(sides):
            angle = math.radians(k * (360 / sides))
            pts.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
        shapes.append(f'<polygon points="{" ".join(pts)}" fill="{color}" stroke="{c2}" stroke-width="1" opacity="0.9"/>')
    # Stralende lijnen
    for k in range(16):
        angle = math.radians(k * 22.5)
        x2 = cx + T * 0.44 * math.cos(angle)
        y2 = cy + T * 0.44 * math.sin(angle)
        shapes.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c2}" stroke-width="0.7" opacity="0.35"/>')
    # Hoekdecoraties
    corner_r = T * 0.1
    for (ex, ey) in [(corner_r, corner_r), (T - corner_r, corner_r),
                      (corner_r, T - corner_r), (T - corner_r, T - corner_r)]:
        shapes.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{corner_r:.1f}" fill="{c3}" stroke="{c2}" stroke-width="1"/>')
        shapes.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{corner_r*0.45:.1f}" fill="{c1}"/>')
    shapes.append(f'<circle cx="{cx}" cy="{cy}" r="{T*0.06:.1f}" fill="{c4}"/>')
    return "\n".join(shapes)


def generate_knitwerk_svg(palette: dict, tile_size: int, complexity: str) -> str:
    T = tile_size
    bg = palette["background"]
    c1 = palette["primary"]
    c2 = palette["secondary"]
    c3 = palette["accent1"]
    c4 = palette["accent2"]
    shapes = []
    # cells MOET T exact opdelen voor naadloze wrap (delers van 400: 20, 25).
    cells = {"low": 5, "medium": 5, "high": 10}.get(complexity, 5)
    step = T / cells
    rows = cells
    cmap = {1: c1, 2: c2, 3: c3, 4: c4}
    shapes.append(f'<rect x="0" y="0" width="{T}" height="{T}" fill="{bg}"/>')
    # Banden met periode 5 (deelt rows=25 exact -> naadloos verticaal).
    #  sub 0: dikke kleurband (wisselt c1/c2 per blok)
    #  sub 1: stippellijn c3
    #  sub 2: diamant-centrum (c2) met armen (c4)
    #  sub 3: diamant-buitenpunten (c2)
    #  sub 4: achtergrond
    grid = [[0] * cells for _ in range(rows)]
    for r in range(rows):
        block = r // 5
        sub = r % 5
        bandcol = 1 if block % 2 == 0 else 2
        if sub == 0:
            for c in range(cells):
                grid[r][c] = bandcol
        elif sub == 1:
            for c in range(cells):
                grid[r][c] = 3 if c % 2 == 0 else 0
        elif sub == 2:
            for c in range(cells):
                if c % 5 == 2:
                    grid[r][c] = 2
                elif c % 5 in (1, 3):
                    grid[r][c] = 4
        elif sub == 3:
            for c in range(cells):
                if c % 5 in (0, 4):
                    grid[r][c] = 2
    for r in range(rows):
        for c in range(cells):
            col = grid[r][c]
            if col == 0:
                continue
            fill = cmap[col]
            x = c * step
            y = r * step
            cxm = x + step / 2
            shapes.append(
                f'<path d="M {x:.2f} {y:.2f} '
                f'L {cxm:.2f} {y+step*0.55:.2f} '
                f'L {x+step:.2f} {y:.2f} '
                f'L {x+step:.2f} {y+step*0.45:.2f} '
                f'L {cxm:.2f} {y+step:.2f} '
                f'L {x:.2f} {y+step*0.45:.2f} Z" fill="{fill}"/>'
            )
    return "\n".join(shapes)


def generate_bauhaus_svg(palette: dict, tile_size: int, complexity: str) -> str:
    import random
    T = tile_size
    bg = palette["background"]
    cols = [palette["primary"], palette["secondary"], palette["accent1"], palette["accent2"], bg]
    shapes = []
    grid = {"low": 3, "medium": 3, "high": 4}.get(complexity, 3)
    cell = T / grid
    rnd = random.Random(1234 + grid)
    shapes.append(f'<rect x="0" y="0" width="{T}" height="{T}" fill="{bg}"/>')

    def pick(exclude=None):
        c = rnd.choice(cols)
        while exclude is not None and c == exclude:
            c = rnd.choice(cols)
        return c

    for row in range(grid):
        for col in range(grid):
            x = col * cell
            y = row * cell
            base = pick()
            fg = pick(exclude=base)
            shapes.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="{base}"/>')
            motif = rnd.choice(["halfcircle", "triangle", "quarter", "rings", "stripes", "circle", "diag"])
            cx = x + cell / 2
            cy = y + cell / 2
            if motif == "halfcircle":
                r = cell / 2
                orient = rnd.choice(["t", "b", "l", "rr"])
                if orient == "t":
                    d = f'M {x:.1f} {y+r:.1f} A {r:.1f} {r:.1f} 0 0 1 {x+cell:.1f} {y+r:.1f} Z'
                elif orient == "b":
                    d = f'M {x:.1f} {y+r:.1f} A {r:.1f} {r:.1f} 0 0 0 {x+cell:.1f} {y+r:.1f} Z'
                elif orient == "l":
                    d = f'M {x+r:.1f} {y:.1f} A {r:.1f} {r:.1f} 0 0 0 {x+r:.1f} {y+cell:.1f} Z'
                else:
                    d = f'M {x+r:.1f} {y:.1f} A {r:.1f} {r:.1f} 0 0 1 {x+r:.1f} {y+cell:.1f} Z'
                shapes.append(f'<path d="{d}" fill="{fg}"/>')
            elif motif == "triangle":
                orient = rnd.choice(["u", "d", "l", "rr"])
                if orient == "u":
                    pts = f'{cx:.1f},{y:.1f} {x+cell:.1f},{y+cell:.1f} {x:.1f},{y+cell:.1f}'
                elif orient == "d":
                    pts = f'{x:.1f},{y:.1f} {x+cell:.1f},{y:.1f} {cx:.1f},{y+cell:.1f}'
                elif orient == "l":
                    pts = f'{x:.1f},{y:.1f} {x+cell:.1f},{cy:.1f} {x:.1f},{y+cell:.1f}'
                else:
                    pts = f'{x+cell:.1f},{y:.1f} {x+cell:.1f},{y+cell:.1f} {x:.1f},{cy:.1f}'
                shapes.append(f'<polygon points="{pts}" fill="{fg}"/>')
            elif motif == "quarter":
                corner = rnd.choice(["tl", "tr", "bl", "br"])
                r = cell
                if corner == "tl":
                    d = f'M {x:.1f} {y:.1f} L {x+r:.1f} {y:.1f} A {r:.1f} {r:.1f} 0 0 1 {x:.1f} {y+r:.1f} Z'
                elif corner == "tr":
                    d = f'M {x+cell:.1f} {y:.1f} L {x+cell:.1f} {y+r:.1f} A {r:.1f} {r:.1f} 0 0 1 {x+cell-r:.1f} {y:.1f} Z'
                elif corner == "bl":
                    d = f'M {x:.1f} {y+cell:.1f} L {x:.1f} {y+cell-r:.1f} A {r:.1f} {r:.1f} 0 0 1 {x+r:.1f} {y+cell:.1f} Z'
                else:
                    d = f'M {x+cell:.1f} {y+cell:.1f} L {x+cell-r:.1f} {y+cell:.1f} A {r:.1f} {r:.1f} 0 0 1 {x+cell:.1f} {y+cell-r:.1f} Z'
                shapes.append(f'<path d="{d}" fill="{fg}"/>')
            elif motif == "rings":
                fg2 = pick(exclude=base)
                n = 5
                for i in range(n, 0, -1):
                    rr = (cell / 2) * (i / n) * 0.9
                    ringfill = fg if i % 2 == 0 else fg2
                    shapes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr:.1f}" fill="{ringfill}"/>')
            elif motif == "stripes":
                n = 5
                sh = cell / (n * 2)
                for i in range(n):
                    yy = y + i * 2 * sh
                    shapes.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{cell:.1f}" height="{sh:.1f}" fill="{fg}"/>')
            elif motif == "circle":
                shapes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{cell*0.40:.1f}" fill="{fg}"/>')
            elif motif == "diag":
                if rnd.random() < 0.5:
                    pts = f'{x:.1f},{y:.1f} {x+cell:.1f},{y:.1f} {x:.1f},{y+cell:.1f}'
                else:
                    pts = f'{x+cell:.1f},{y:.1f} {x+cell:.1f},{y+cell:.1f} {x:.1f},{y+cell:.1f}'
                shapes.append(f'<polygon points="{pts}" fill="{fg}"/>')
    return "\n".join(shapes)


STYLE_GENERATORS = {
    "bauhaus": generate_bauhaus_svg,
    "geometric": generate_geometric_svg,
    "medallion": generate_medallion_svg,
    "floral": generate_floral_svg,
    "botanical": generate_floral_svg,
    "knitwerk": generate_knitwerk_svg,
    "persian": generate_medallion_svg,
    "classic": generate_medallion_svg,
    "strepen": generate_strepen_svg,
    "mozaiek": generate_mozaiek_svg,
    "chevron": generate_chevron_svg,
    "chevron_bold": generate_chevron_bold_svg,
    "houndstooth": generate_houndstooth_svg,
    "urban_plaid": generate_urban_plaid_svg,
    "hexagon": generate_hexagoon_svg,
    "ogee": generate_ogee_svg,
    "diamant": generate_diamant_svg,
    "terrazzo": generate_terrazzo_svg,
    "visgraat": generate_visgraat_lijn_svg,
    "dots": generate_dots_svg,
    "hoogtelijnen": generate_hoogtelijnen_svg,
    "vrije_vormen": generate_vrije_vormen_svg,
    "bamboe": generate_bamboe_svg,
    "art_deco_hex": generate_artdeco_hex_svg,
    "art_deco": generate_artdeco_svg,
}


def build_tile_svg(analysis: dict, tile_size: int = 400, motief_schaal: int = 100) -> str:
    """Bouw de SVG voor één basistegel."""
    style = analysis.get("style", "geometric")
    p = analysis.get("_prompt", "")
    if style == "bauhaus" or "bauhaus" in p:
        style = "bauhaus"
    elif style == "knitwerk" or any(w in p for w in ['knitwerk', 'knit', 'gebreid', 'breiwerk', 'fair isle', 'noorse trui', 'nordic', 'scandinavisch', 'noors', 'sneeuwvlok']):
        style = "knitwerk"
    elif style == "hoogtelijnen" or any(w in p for w in ["hoogtelijn", "topografie", "contour"]):
        style = "hoogtelijnen"
    elif any(w in p for w in ["streep", "strepen", "stripe"]):
        style = "strepen"
    elif any(w in p for w in ["mozaiek", "pixel", "blokje"]):
        style = "mozaiek"
    elif any(w in p for w in ["chevronbold", "chevron bold", "chevron blok"]):
        style = "chevron_bold"
    elif style == "houndstooth" or any(w in p for w in ["houndstooth", "hanenpoot", "pied-de-poule", "pied de poule", "pita"]):
        style = "houndstooth"
    elif style == "urban_plaid" or any(w in p for w in ["urban plaid", "plaid", "tartan", "schots"]):
        style = "urban_plaid"
    elif any(w in p for w in ["chevron", "zigzag"]):
        style = "chevron"
    elif any(w in p for w in ["hexagon", "honingraat", "zeshoek"]):
        style = "hexagon"
    elif any(w in p for w in ["ogee", "schub", "dakpan"]):
        style = "ogee"
    elif any(w in p for w in ["nordic", "scandinavisch", "noors", "kruis", "sneeuwvlok", "knitwerk", "knit", "gebreid", "breiwerk"]):
        style = "knitwerk"
    elif any(w in p for w in ["terrazzo", "steensnipp"]):
        style = "terrazzo"
    elif any(w in p for w in ["vrije vorm", "organisch", "vloeiend"]):
        style = "vrije_vormen"

    # Directe keyword override op basis van de ORIGINELE PROMPT (niet description_nl,
    # want de AI-omschrijving varieert per generatie en kan de juiste stijl overschrijven)
    prompt_lower = analysis.get("_prompt", "").lower()
    if style == "bauhaus":
        pass
    elif style == "knitwerk":
        pass
    elif style == "hoogtelijnen" or any(w in prompt_lower for w in ["hoogtelijn", "topografie", "contour"]):
        style = "hoogtelijnen"
    elif any(w in prompt_lower for w in ["streep", "strepen", "stripe", "verticale lijn"]):
        style = "strepen"
    elif any(w in prompt_lower for w in ["mozaiek", "pixel", "blokje"]):
        style = "mozaiek"
    elif style == "chevron_bold" or any(w in prompt_lower for w in ["chevronbold", "chevron bold", "chevron blok"]):
        style = "chevron_bold"
    elif style == "houndstooth" or any(w in prompt_lower for w in ["houndstooth", "hanenpoot", "pied-de-poule", "pied de poule", "pita"]):
        style = "houndstooth"
    elif style == "urban_plaid" or any(w in prompt_lower for w in ["urban plaid", "plaid", "tartan", "schots"]):
        style = "urban_plaid"
    elif any(w in prompt_lower for w in ["chevron", "zigzag", "pijl"]):
        style = "chevron"
    elif any(w in prompt_lower for w in ["hexagon", "honingraat", "zeshoek"]):
        style = "hexagon"
    elif any(w in prompt_lower for w in ["ogee", "schub", "dakpan"]):
        style = "ogee"
    elif any(w in prompt_lower for w in ["nordic", "scandinavisch", "noors", "knitwerk", "knit", "gebreid", "breiwerk", "fair isle"]):
        style = "knitwerk"
    elif any(w in prompt_lower for w in ["terrazzo", "steensnipp"]):
        style = "terrazzo"
    elif any(w in prompt_lower for w in ["vrije vorm", "organisch", "vloeiend"]):
        style = "vrije_vormen"
    if "bamboe" in p or "bamboo" in p:
        style = "bamboe"
    if "art deco" in p or "jaren 20" in p or "jaren twintig" in p:
        if any(w in p for w in ["hexagon", "zeshoek", "honingraat"]):
            style = "art_deco_hex"
        else:
            style = "art_deco"
    if any(w in p for w in ["botanisch", "bloem", "blad", "botanical", "plant", "flora"]):
        style = "botanical"
    if "medaillon" in p or "medallion" in p:
        style = "medallion"
    palette = analysis.get("palette", {
        "background": "#F5E6D3", "primary": "#C4753A",
        "secondary": "#8B4513", "accent1": "#D4A055", "accent2": "#F0C080"
    })
    complexity = analysis.get("complexity", "medium")
    shape_list = analysis.get("shapes", [])
    # --- Motief-schaal via naadloze tegeling (tegel blijft ALTIJD 400) ---
    # Kleiner % = fijner = motief vaker herhaald binnen de 400-tegel.
    # n is een deler van 400, dus het patroon sluit exact aan (naadloos).
    TEGEL = 400
    delers = [1, 2, 4, 5, 8, 10]
    ratio = 100.0 / max(int(motief_schaal), 10)
    n = min(delers, key=lambda d: abs(d - ratio))
    if n < 1:
        n = 1
    g = TEGEL // n  # interne grootte waarop de generator tekent
    extra_styles = ["bauhaus","knitwerk","strepen","mozaiek","chevron","chevron_bold","houndstooth","urban_plaid","hexagon","ogee","diamant","terrazzo","vrije_vormen","dots","dots","hoogtelijnen","vlechtwerk","visgraat","batik","botanical","floral","nordic","persian","medallion","abstract","bamboe","art_deco","art_deco_hex"]
    default_shapes = ["octagon", "diamond", "circle", "square", "triangle", "hexagon", "star"]
    user_specified = any(s in default_shapes and s != "octagon" for s in shape_list)
    if style in extra_styles:
        generator = STYLE_GENERATORS.get(style, generate_geometric_svg)
        try:
            inner = generator(palette, g, complexity)
        except TypeError:
            inner = generator(palette, g, complexity, None)
    elif user_specified or shape_list == ["circle"] or shape_list == ["square"] or shape_list == ["triangle"]:
        inner = generate_geometric_svg(palette, g, complexity, shape_list)
    else:
        generator = STYLE_GENERATORS.get(style, generate_geometric_svg)
        if generator == generate_geometric_svg:
            inner = generator(palette, g, complexity, shape_list or ["octagon"])
        else:
            inner = generator(palette, g, complexity)
    # Tegel het motief n x n binnen de 400-tegel (naadloos want 400 = n * g)
    if n > 1:
        kopieen = []
        for iy in range(n):
            for ix in range(n):
                kopieen.append(f'<g transform="translate({ix * g},{iy * g})">{inner}</g>')
        inner = "".join(kopieen)
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TEGEL} {TEGEL}"
     width="{TEGEL}" height="{TEGEL}">
  <rect width="{TEGEL}" height="{TEGEL}" fill="{palette['background']}"/>
  {inner}
</svg>"""
    return svg


def build_repeat_svg(tile_svg: str, analysis: dict,
                     tile_cm: int, repeat_type: str,
                     dpi: int, cols: int = 3, rows: int = 3) -> str:
    """Bouw een all-over repeat SVG met het opgegeven repeat-type."""
    T = 400
    OVERLAP_SCALE = 1.006  # minieme tegel-overlap om haarlijn-naden te dichten
    bg_color = analysis.get('palette', {}).get('background', '#F5F5F5')
    total_w = T * cols
    total_h = T * rows

    inner_start = tile_svg.index(">", tile_svg.index("<svg")) + 1
    inner_end = tile_svg.rindex("</svg>")
    inner_content = tile_svg[inner_start:inner_end].strip()

    tiles = []
    clip_defs = []
    clip_id = 0

    for r in range(-1, rows + 2):
        for c in range(-1, cols + 2):
            x = c * T
            y = r * T
            if repeat_type == "half-drop":
                y += (c % 2) * (T // 2)
            elif repeat_type == "brick":
                x += (r % 2) * (T // 2)

            if repeat_type == "mirror":
                sx = -1 if c % 2 == 1 else 1
                sy = -1 if r % 2 == 1 else 1
                tx = x + (T if sx == -1 else 0)
                ty = y + (T if sy == -1 else 0)
                transform = f"translate({tx},{ty}) scale({sx*OVERLAP_SCALE},{sy*OVERLAP_SCALE})"
            else:
                transform = f"translate({x},{y}) scale({OVERLAP_SCALE})"

            tiles.append(f'''<g transform="{transform}">{inner_content}</g>''')

    px_w = round(total_w / 400 * (tile_cm / 2.54 * dpi))
    px_h = round(total_h / 400 * (tile_cm / 2.54 * dpi))

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {total_w} {total_h}"
     width="{px_w}px" height="{px_h}px">
  <defs>
    <clipPath id="canvas"><rect width="{total_w}" height="{total_h}"/></clipPath>
    {"".join(clip_defs)}
  </defs>
  <rect width="{total_w}" height="{total_h}" fill="{bg_color}"/>
  <g clip-path="url(#canvas)">{"".join(tiles)}</g>
</svg>"""
    return svg


# ─── PNG rendering ────────────────────────────────────────────────────────────

def svg_to_png(svg_string: str, output_path: str, dpi: int = 150, tile_cm: int = 40) -> str:
    return output_path


# ─── Flask routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.json
    prompt = data.get("prompt", "").strip()
    api_key = data.get("api_key", "").strip()
    tile_cm = int(data.get("tile_cm", 40))
    repeat_type = data.get("repeat_type", "full")
    dpi = int(data.get("dpi", 150))

    if not prompt:
        return jsonify({"error": "Voer een dessin beschrijving in."}), 400
    if not api_key:
        return jsonify({"error": "Vul uw API-sleutel in."}), 400

    try:
        # Stap 1: AI analyse
        analysis = analyse_prompt(prompt, api_key)
        analysis["_prompt"] = prompt.lower()
        # Overschrijf palet als gebruiker eigen kleuren heeft opgegeven
        aangepast_palet = data.get('aangepast_palet')
        if aangepast_palet:
            analysis['palette'] = {
                'background': aangepast_palet.get('background', '#F5F5F5'),
                'primary': aangepast_palet.get('primary', '#C4753A'),
                'secondary': aangepast_palet.get('secondary', '#8B4513'),
                'accent1': aangepast_palet.get('accent1', '#D4A055'),
                'accent2': aangepast_palet.get('accent2', '#F0C080')
            }
    except json.JSONDecodeError:
        return jsonify({"error": "AI gaf een onverwacht antwoord. Probeer opnieuw."}), 500
    except Exception as e:
        return jsonify({"error": f"AI-fout: {str(e)}"}), 500

    motief_schaal = int(data.get("motief_schaal", 100))
    try:
        # Stap 2: Genereer basistegel SVG
        p = prompt.lower()
        if 'bauhaus' in p:
            analysis['style'] = 'bauhaus'
        if 'bamboe' in p or 'bamboo' in p:
            analysis['style'] = 'bamboe'
        elif any(w in p for w in ['botanisch', 'bloem', 'blad', 'botanical', 'plant', 'flora']):
            analysis['style'] = 'botanical'
        elif any(w in p for w in ['vlechtwerk', 'vlecht', 'gevlochten', 'basketweave']):
            analysis['style'] = 'vlechtwerk'
        elif any(w in p for w in ['visgraat', 'herringbone', 'visbot']):
            analysis['style'] = 'visgraat'
        elif any(w in p for w in ['streep', 'strepen', 'stripe']):
            analysis['style'] = 'strepen'
        elif any(w in p for w in ['mozaiek', 'pixel', 'blokje']):
            analysis['style'] = 'mozaiek'
        elif any(w in p for w in ['chevronbold', 'chevron bold', 'chevron blok']):
            analysis['style'] = 'chevron_bold'
        elif analysis.get('style') == 'houndstooth' or any(w in p for w in ['houndstooth', 'hanenpoot', 'pied-de-poule', 'pied de poule', 'pita']):
            analysis['style'] = 'houndstooth'
        elif any(w in p for w in ['knitwerk', 'knit', 'gebreid', 'breiwerk', 'fair isle', 'noorse trui', 'nordic', 'scandinavisch', 'noors', 'sneeuwvlok']):
            analysis['style'] = 'knitwerk'
        elif analysis.get('style') == 'urban_plaid' or any(w in p for w in ['urban plaid', 'plaid', 'tartan', 'schots']):
            analysis['style'] = 'urban_plaid'
        elif any(w in p for w in ['chevron', 'zigzag']):
            analysis['style'] = 'chevron'
        elif any(w in p for w in ['hexagon', 'honingraat', 'zeshoek']):
            analysis['style'] = 'hexagon'
        elif any(w in p for w in ['ogee', 'schub', 'dakpan']):
            analysis['style'] = 'ogee'
        elif any(w in p for w in ['batik', 'mirror', 'spiegel', 'tie-dye', 'ikat']):
            analysis['style'] = 'batik'
        elif any(w in p for w in ['vlechtwerk', 'vlecht', 'gevlochten', 'basketweave']):
            analysis['style'] = 'vlechtwerk'
        elif any(w in p for w in ['visgraat', 'herringbone', 'visbot']):
            analysis['style'] = 'visgraat'
        elif any(w in p for w in ['dots', 'stippen', 'polka']):
            analysis['style'] = 'dots'
        elif any(w in p for w in ['terrazzo', 'steensnipp']):
            analysis['style'] = 'terrazzo'
        elif any(w in p for w in ['vrije vorm', 'organisch', 'vloeiend']):
            analysis['style'] = 'vrije_vormen'
        # Cirkels-knop ('Alleen cirkels, strak en minimalistisch'): forceer echte cirkels,
        # ongeacht welke vormen de AI teruggeeft. Specifiek op 'alleen cirkel' zodat
        # bv. Bauhaus ('halve cirkels') niet wordt geraakt.
        if 'alleen cirkel' in p:
            analysis['style'] = 'geometric'
            analysis['shapes'] = ['circle']
        tile_svg = build_tile_svg(analysis, tile_size=400, motief_schaal=motief_schaal)

        # Stap 3: Bouw all-over repeat
        repeat_svg = build_repeat_svg(tile_svg, analysis, tile_cm, repeat_type, dpi)

        # Stap 4: SVG als base64 voor preview in browser
        tile_b64 = base64.b64encode(tile_svg.encode()).decode()
        repeat_b64 = base64.b64encode(repeat_svg.encode()).decode()

        # Stap 5: Bereken resolutie-informatie
        px_per_tile = round(tile_cm / 2.54 * dpi)

        # Vriendelijk stijl-label (alleen weergave; verandert de tekening niet)
        p_low = prompt.lower()
        label_map = [
            (['bamboe', 'bamboo'], 'bamboe'),
            (['art deco', 'jaren 20', 'jaren twintig'], 'art deco'),
            (['schub', 'dakpan', 'ogee'], 'schubben'),
            (['sterren'], 'sterren'),
            (['bauhaus'], 'bauhaus'),
            (['cirkel'], 'cirkels'),
            (['ruiten', 'diamant'], 'ruiten'),
            (['terrazzo'], 'terrazzo'),
            (['mozaiek'], 'mozaiek'),
            (['visgraat', 'herringbone'], 'visgraat'),
            (['strepen', 'streep', 'stripe'], 'strepen'),
            (['dots', 'stippen', 'polka'], 'dots'),
            (['chevronbold', 'chevron bold', 'chevron blok'], 'chevron_bold'),
            (['houndstooth', 'hanenpoot', 'pied-de-poule', 'pied de poule', 'pita'], 'houndstooth'),
            (['knitwerk', 'knit', 'gebreid', 'breiwerk', 'fair isle', 'noorse trui', 'nordic', 'scandinavisch', 'noors'], 'knitwerk'),
            (['urban plaid', 'plaid', 'tartan', 'schots'], 'urban_plaid'),
            (['chevron', 'zigzag'], 'chevron'),
            (['hexagon', 'honingraat', 'zeshoek'], 'hexagon'),
            (['vrije vorm', 'organisch', 'vloeiend'], 'vrije vormen'),
            (['medaillon', 'medallion'], 'medaillon'),
            (['perzisch', 'persian'], 'perzisch'),
            (['botanisch', 'bloem', 'botanical'], 'botanisch'),
        ]
        weergave_stijl = analysis.get('style', '')
        for _sleutels, _naam in label_map:
            if any(_s in p_low for _s in _sleutels):
                weergave_stijl = _naam
                break

        return jsonify({
            "success": True,
            "analysis": analysis,
            "tile_svg_b64": tile_b64,
            "repeat_svg_b64": repeat_b64,
            "info": {
                "style": weergave_stijl,
                "description": analysis.get("description_nl", ""),
                "sfeer": analysis.get("sfeer_nl", []),
                "geschikt_voor": analysis.get("geschikt_voor_nl", []),
                "ontwerpvisie": analysis.get("ontwerpvisie_nl", ""),
                "complexity": analysis.get("complexity", ""),
                "dpi": dpi,
                "tile_px": px_per_tile,
                "tile_cm": tile_cm,
                "repeat_type": repeat_type,
                "colors": analysis.get("palette", {})
            }
        })
    except Exception as e:
        return jsonify({"error": f"Generatie-fout: {str(e)}"}), 500


@app.route("/api/export/svg", methods=["POST"])
def export_svg():
    data = request.json
    svg_b64 = data.get("svg_b64", "")
    filename = data.get("filename", f"dessin_{int(time.time())}.svg")
    svg_bytes = base64.b64decode(svg_b64)
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "wb") as f:
        f.write(svg_bytes)
    return send_file(path, as_attachment=True, download_name=filename,
                     mimetype="image/svg+xml")


@app.route("/api/export/png", methods=["POST"])
def export_png():
    data = request.json
    svg_b64 = data.get("svg_b64", "")
    dpi = int(data.get("dpi", 150))
    tile_cm = int(data.get("tile_cm", 40))
    filename = data.get("filename", f"dessin_{int(time.time())}.png")
    svg_string = base64.b64decode(svg_b64).decode("utf-8")
    path = os.path.join(EXPORT_DIR, filename)
    svg_to_png(svg_string, path, dpi=dpi, tile_cm=tile_cm)
    return send_file(path, as_attachment=True, download_name=filename,
                     mimetype="image/png")


if __name__ == "__main__":
    print("=" * 55)
    print("  RepeatTile Studio — Tapijt Dessin Generator")
    print("=" * 55)
    print("  Open uw browser en ga naar: http://localhost:5000")
    print("  Druk op Ctrl+C om te stoppen.")
    print("=" * 55)
    app.run(debug=False, host="0.0.0.0", port=5000)


# E-mail bestelling

@app.route('/api/bestelling', methods=['POST'])
def api_bestelling():
    try:
        data = request.get_json()
        naam = data.get('naam', '')
        email = data.get('email', '')
        telefoon = data.get('telefoon', '')
        bedrijf = data.get('bedrijf', '')
        wensen = data.get('wensen', '')
        product = data.get('product', 'Printtapijt')
        afmeting = data.get('afmeting', 'Niet opgegeven')
        staaltje = data.get('staaltje', 'Nee')
        adres = data.get('adres', '')
        straat = data.get('straat', '')
        postcode = data.get('postcode', '')
        plaats = data.get('plaats', '')
        land = data.get('land', 'Nederland')
        adres_volledig = ', '.join(filter(None, [straat, postcode + ' ' + plaats if postcode or plaats else '', land])).strip(', ')
        dessin_info = data.get('dessin_info', '')
        dessin_ref = data.get('dessin_ref', 'Onbekend')
        repeat_type = data.get('repeat_type', '')
        tegel_maat = data.get('tegel_maat', '')
        resolutie = data.get('resolutie', '')
        datum = data.get('datum', '')
        # Gekozen dessin-kleuren (HEX + RGB) -> alleen voor interne mail
        kleuren = data.get('kleuren', []) or []
        kleuren_rows = ''
        for _k in kleuren:
            _hex = (_k.get('hex') or '').strip()
            if not _hex:
                continue
            _lbl = _k.get('label', '')
            _r = _k.get('r', ''); _g = _k.get('g', ''); _b = _k.get('b', '')
            _rgb = f'{_r}, {_g}, {_b}' if (_r != '' and _g != '' and _b != '') else ''
            _swatch = f'<span style="display:inline-block;width:14px;height:14px;border:1px solid #999;background:{_hex};vertical-align:middle;margin-right:6px"></span>'
            _waarde = f'{_swatch}{_hex}' + (f' &nbsp; RGB {_rgb}' if _rgb else '')
            kleuren_rows += f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Kleur ({_lbl})</td><td style="padding:8px">{_waarde}</td></tr>'
        bedrijf = data.get('bedrijf', '')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Nieuwe tapijt offerte - {naam}'
        msg['From'] = 'appieoosterhof@gmail.com'
        msg['To'] = 'administratie@dcod.nl'
        msg['Cc'] = 'appieoosterhof@gmail.com'
        html = f"""<html><body style="font-family:Arial;">
        <h2 style="color:#4A7C3F;">Nieuwe offerte aanvraag</h2>
        <table style="border-collapse:collapse;width:100%">
        <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Product</td><td style="padding:8px">{product}</td></tr>
        <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Afmeting</td><td style="padding:8px">{afmeting}</td></tr>
        <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Naam</td><td style="padding:8px">{naam}</td></tr>
        <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">E-mail</td><td style="padding:8px">{email}</td></tr>
        <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Telefoon</td><td style="padding:8px">{telefoon}</td></tr>
        <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Dessin</td><td style="padding:8px">{dessin_info}</td></tr>
        <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Wensen</td><td style="padding:8px">{wensen}</td></tr>
        </table></body></html>"""
        msg.attach(MIMEText(html, 'html'))

        # Voeg dessin toe als bijlage
        img_b64 = data.get('img_b64', '')
        if img_b64:
            try:
                img_data = base64.b64decode(img_b64)
                img = MIMEImage(img_data, _subtype='png', name='dessin.png')
                img.add_header('Content-Disposition', 'attachment', filename='dessin.png')
                msg.attach(img)
            except Exception as e:
                print(f"Bijlage fout: {e}")

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('appieoosterhof@gmail.com', 'lvxyxlzlzxwneldz')

        bijlage = None
        img_b64_data = data.get('img_b64', '')
        if img_b64_data:
            try:
                img_data = base64.b64decode(img_b64_data)
                bijlage = MIMEImage(img_data, _subtype='png', name='dessin.png')
                bijlage.add_header('Content-Disposition', 'attachment', filename='dessin.png')
            except Exception as e:
                print(f"Bijlage fout: {e}")

        msg1 = MIMEMultipart('mixed')
        msg1['Subject'] = f'Nieuwe tapijt offerte - {naam}'
        msg1['From'] = 'appieoosterhof@gmail.com'
        msg1['To'] = 'administratie@dcod.nl'
        msg1['Cc'] = 'appieoosterhof@gmail.com'
        html1 = ('<html><body style="font-family:Arial;"><h2 style="color:#4A7C3F;">Nieuwe offerte aanvraag</h2><table style="border-collapse:collapse;width:100%">'
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Referentie</td><td style="padding:8px">{dessin_ref}</td></tr>' if dessin_ref else "")
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Datum</td><td style="padding:8px">{datum}</td></tr>' if datum else "")
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Bedrijf</td><td style="padding:8px">{bedrijf}</td></tr>' if bedrijf else "")
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Naam</td><td style="padding:8px">{naam}</td></tr>'
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">E-mail</td><td style="padding:8px">{email}</td></tr>'
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Telefoon</td><td style="padding:8px">{telefoon}</td></tr>'
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Product</td><td style="padding:8px">{product}</td></tr>'
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Herhaalpatroon</td><td style="padding:8px">{repeat_type}</td></tr>' if repeat_type else "")
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Tegelmaat</td><td style="padding:8px">{tegel_maat}</td></tr>' if tegel_maat else "")
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Resolutie</td><td style="padding:8px">{resolutie}</td></tr>' if resolutie else "")
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Afmeting</td><td style="padding:8px">{afmeting}</td></tr>'
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Dessin</td><td style="padding:8px">{dessin_info}</td></tr>'
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Wensen</td><td style="padding:8px">{wensen}</td></tr>'
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Staaltje</td><td style="padding:8px">{staaltje}</td></tr>'+ (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Afleveradres</td><td style="padding:8px">{adres_volledig}</td></tr>' if adres_volledig else '')
            + kleuren_rows
            + '</table></body></html>')
        msg1.attach(MIMEText(html1, 'html'))
        if bijlage:
            msg1.attach(bijlage)
        # Schone, drukklare SVG's alleen intern meesturen (niet naar de klant)
        from email.mime.base import MIMEBase
        from email import encoders as _encoders
        for _veld, _naam in [('tile_svg_b64', 'dessin_tegel.svg')]:
            _b64 = data.get(_veld, '')
            if _b64:
                try:
                    _svg_bytes = base64.b64decode(_b64)
                    _part = MIMEBase('image', 'svg+xml')
                    _part.set_payload(_svg_bytes)
                    _encoders.encode_base64(_part)
                    _part.add_header('Content-Disposition', 'attachment', filename=_naam)
                    msg1.attach(_part)
                except Exception as _e:
                    print("SVG-bijlage fout (" + _naam + "): " + str(_e))
        server.sendmail('appieoosterhof@gmail.com', ['administratie@dcod.nl', 'appieoosterhof@gmail.com'], msg1.as_string())

        if email:
            from copy import deepcopy
            msg2 = MIMEMultipart('mixed')
            msg2['Subject'] = 'Uw offerte aanvraag bij DCOD Printtapijt'
            msg2['From'] = 'appieoosterhof@gmail.com'
            msg2['To'] = email
            html2 = ('<html><body style="font-family:Arial;">'
                + '<p style="color:#666;font-style:italic;">Hierbij een kopie van uw aanvraag.</p>'
                + f'<h2 style="color:#4A7C3F;">Bedankt, {naam}!</h2>'
                + '<p>Wij nemen binnen 2 werkdagen contact met u op.</p>'
                + '<table style="border-collapse:collapse;width:100%">'
                + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Referentie</td><td style="padding:8px">{dessin_ref}</td></tr>' if dessin_ref else "")
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Datum</td><td style="padding:8px">{datum}</td></tr>' if datum else "")
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Bedrijf</td><td style="padding:8px">{bedrijf}</td></tr>' if bedrijf else "")
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Naam</td><td style="padding:8px">{naam}</td></tr>'
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">E-mail</td><td style="padding:8px">{email}</td></tr>'
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Telefoon</td><td style="padding:8px">{telefoon}</td></tr>'
            + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Product</td><td style="padding:8px">{product}</td></tr>'
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Herhaalpatroon</td><td style="padding:8px">{repeat_type}</td></tr>' if repeat_type else "")
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Tegelmaat</td><td style="padding:8px">{tegel_maat}</td></tr>' if tegel_maat else "")
            + (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Resolutie</td><td style="padding:8px">{resolutie}</td></tr>' if resolutie else "")
                + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Afmeting</td><td style="padding:8px">{afmeting}</td></tr>'
                + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Dessin</td><td style="padding:8px">{dessin_info}</td></tr>'
                + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Wensen</td><td style="padding:8px">{wensen}</td></tr>'
                + f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Staaltje</td><td style="padding:8px">{staaltje}</td></tr>'+ (f'<tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Afleveradres</td><td style="padding:8px">{adres_volledig}</td></tr>' if adres_volledig else '')
                + '</table><br><p>Met vriendelijke groet,<br><strong>DCOD Printtapijt</strong><br>www.dcod-printtapijt.nl</p></body></html>')
            msg2.attach(MIMEText(html2, 'html'))
            if bijlage:
                msg2.attach(deepcopy(bijlage))
            server.sendmail('appieoosterhof@gmail.com', [email], msg2.as_string())

        server.quit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Mail fout: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
