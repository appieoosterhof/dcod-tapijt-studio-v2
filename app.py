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
from modules_extra import generate_strepen_svg, generate_mozaiek_svg, generate_chevron_svg, generate_hexagoon_svg, generate_ogee_svg, generate_diamant_svg, generate_terrazzo_svg, generate_vrije_vormen_svg, generate_visgraat_svg, generate_dots_svg, generate_visgraat_lijn_svg

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
        max_tokens=400,
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
  "description_nl": "Korte beschrijving van het dessin in het Nederlands"
}}

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
    step = T // 4 if complexity == "high" else T // 3 if complexity == "medium" else T // 2
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
    T = tile_size
    bg = palette["background"]
    c1 = palette["primary"]
    c2 = palette["secondary"]
    c3 = palette["accent1"]
    c4 = palette["accent2"]
    cols = 3 if complexity == "high" else 2
    step = T // cols
    shapes = []
    def flower(cx, cy, r, fill, center):
        petals = 8
        for k in range(petals):
            angle = math.radians(k * (360 / petals))
            px = cx + r * 0.55 * math.cos(angle)
            py = cy + r * 0.55 * math.sin(angle)
            shapes.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r*0.28:.1f}" ry="{r*0.42:.1f}" '
                          f'fill="{fill}" opacity="0.85" transform="rotate({math.degrees(angle):.1f} {px:.1f} {py:.1f})"/>')
        shapes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.22:.1f}" fill="{center}"/>')
        shapes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.10:.1f}" fill="{c2}" opacity="0.6"/>')
    for row in range(cols):
        for col in range(cols):
            cx = col * step + step // 2
            cy = row * step + step // 2
            r = step * 0.44
            flower(cx, cy, r, c1, c3)
    # Half-staggered tussenin
    for row in range(cols + 1):
        for col in range(cols + 1):
            cx = col * step
            cy = row * step
            if cx <= T and cy <= T:
                flower(cx, cy, step * 0.22, c3, c4)
    # Sierlijke stengels
    shapes.append(f'<line x1="0" y1="{T//2}" x2="{T}" y2="{T//2}" stroke="{c2}" stroke-width="1.2" opacity="0.3"/>')
    shapes.append(f'<line x1="{T//2}" y1="0" x2="{T//2}" y2="{T}" stroke="{c2}" stroke-width="1.2" opacity="0.3"/>')
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


def generate_nordic_svg(palette: dict, tile_size: int, complexity: str) -> str:
    T = tile_size
    bg = palette["background"]
    c1 = palette["primary"]
    c2 = palette["secondary"]
    c3 = palette["accent1"]
    shapes = []
    step = T // 6 if complexity == "high" else T // 5 if complexity == "medium" else T // 4
    arm = step * 0.38
    w = step * 0.13
    # Achtergrondvlakken afwisselend
    for row in range(-1, T // step + 2):
        for col in range(-1, T // step + 2):
            x = col * step
            y = row * step
            fill = c1 if (row + col) % 2 == 0 else c2
            shapes.append(f'<rect x="{x}" y="{y}" width="{step}" height="{step}" fill="{fill}"/>')
    # Nordic kruis op elk rasterpunt
    for row in range(0, T + step, step):
        for col in range(0, T + step, step):
            cx = col
            cy = row
            bg_kleur = c2 if ((row // step) + (col // step)) % 2 == 0 else c1
            # Verticale arm van het kruis
            shapes.append(f'<rect x="{cx-w:.1f}" y="{cy-arm:.1f}" width="{w*2:.1f}" height="{arm*2:.1f}" fill="{bg_kleur}"/>')
            # Horizontale arm
            shapes.append(f'<rect x="{cx-arm:.1f}" y="{cy-w:.1f}" width="{arm*2:.1f}" height="{w*2:.1f}" fill="{bg_kleur}"/>')
            # Accent stipje
            shapes.append(f'<rect x="{cx-w*0.6:.1f}" y="{cy-w*0.6:.1f}" width="{w*1.2:.1f}" height="{w*1.2:.1f}" fill="{c3}"/>')
    return "\n".join(shapes)
def generate_abstract_svg(palette: dict, tile_size: int, complexity: str) -> str:
    T = tile_size
    c1 = palette["primary"]
    c2 = palette["secondary"]
    c3 = palette["accent1"]
    c4 = palette["accent2"]
    shapes = []
    cols = 8 if complexity == "high" else 5
    step = T // cols
    color_list = [c1, c2, c3, c4, palette["background"]]
    for row in range(cols):
        for col in range(cols):
            x, y = col * step, row * step
            fill = color_list[(row * 3 + col * 2) % len(color_list)]
            if (row + col) % 3 == 0:
                shapes.append(f'<rect x="{x}" y="{y}" width="{step}" height="{step}" fill="{fill}"/>')
            elif (row + col) % 3 == 1:
                shapes.append(f'<circle cx="{x + step//2}" cy="{y + step//2}" r="{step*0.48:.1f}" fill="{fill}"/>')
            else:
                pts = f"{x+step//2},{y} {x+step},{y+step} {x},{y+step}"
                shapes.append(f'<polygon points="{pts}" fill="{fill}"/>')
    return "\n".join(shapes)


STYLE_GENERATORS = {
    "geometric": generate_geometric_svg,
    "medallion": generate_medallion_svg,
    "floral": generate_floral_svg,
    "botanical": generate_floral_svg,
    "nordic": generate_nordic_svg,
    "persian": generate_medallion_svg,
    "classic": generate_medallion_svg,
    "abstract": generate_abstract_svg,
    "strepen": generate_strepen_svg,
    "mozaiek": generate_mozaiek_svg,
    "chevron": generate_chevron_svg,
    "hexagon": generate_hexagoon_svg,
    "ogee": generate_ogee_svg,
    "diamant": generate_diamant_svg,
    "terrazzo": generate_terrazzo_svg,
    "visgraat": generate_visgraat_lijn_svg,
    "dots": generate_dots_svg,
    "vrije_vormen": generate_vrije_vormen_svg,
}


def build_tile_svg(analysis: dict, tile_size: int = 400, motief_schaal: int = 100) -> str:
    """Bouw de SVG voor één basistegel."""
    style = analysis.get("style", "geometric")
    p = analysis.get("_prompt", "")
    if any(w in p for w in ["streep", "strepen", "stripe"]):
        style = "strepen"
    elif any(w in p for w in ["mozaiek", "pixel", "blokje"]):
        style = "mozaiek"
    elif any(w in p for w in ["chevron", "zigzag"]):
        style = "chevron"
    elif any(w in p for w in ["hexagon", "honingraat", "zeshoek"]):
        style = "hexagon"
    elif any(w in p for w in ["ogee", "schub", "dakpan"]):
        style = "ogee"
    elif any(w in p for w in ["nordic", "scandinavisch", "noors", "kruis", "sneeuwvlok"]):
        style = "nordic"
    elif any(w in p for w in ["diamant", "concentrisch"]):
        style = "diamant"
    elif any(w in p for w in ["terrazzo", "steensnipp"]):
        style = "terrazzo"
    elif any(w in p for w in ["vrije vorm", "organisch", "vloeiend"]):
        style = "vrije_vormen"

    # Directe keyword override op basis van prompt
    prompt_lower = analysis.get("description_nl", "").lower()
    if any(w in prompt_lower for w in ["streep", "strepen", "stripe", "verticale lijn"]):
        style = "strepen"
    elif any(w in prompt_lower for w in ["mozaiek", "pixel", "blokje"]):
        style = "mozaiek"
    elif any(w in prompt_lower for w in ["chevron", "zigzag", "pijl"]):
        style = "chevron"
    elif any(w in prompt_lower for w in ["hexagon", "honingraat", "zeshoek"]):
        style = "hexagon"
    elif any(w in prompt_lower for w in ["ogee", "schub", "dakpan"]):
        style = "ogee"
    elif any(w in prompt_lower for w in ["nordic", "scandinavisch", "noors", "kruis", "ruitpatroon"]):
        style = "nordic"
    elif any(w in prompt_lower for w in ["diamant", "concentrisch"]):
        style = "diamant"
    elif any(w in prompt_lower for w in ["terrazzo", "steensnipp"]):
        style = "terrazzo"
    elif any(w in prompt_lower for w in ["vrije vorm", "organisch", "vloeiend"]):
        style = "vrije_vormen"
    palette = analysis.get("palette", {
        "background": "#F5E6D3", "primary": "#C4753A",
        "secondary": "#8B4513", "accent1": "#D4A055", "accent2": "#F0C080"
    })
    complexity = analysis.get("complexity", "medium")
    shape_list = analysis.get("shapes", [])
    # Schaal aanpassen: kleiner tile = fijner patroon
    tile_size = max(50, int(tile_size * (100 / max(motief_schaal, 10))))
    # Als gebruiker specifieke vormen vraagt, altijd geometric generator gebruiken
    extra_styles = ["strepen","mozaiek","chevron","hexagon","ogee","diamant","terrazzo","vrije_vormen","dots","dots","vlechtwerk","visgraat","batik","botanical","floral","nordic","persian","medallion","abstract"]
    default_shapes = ["octagon", "diamond", "circle", "square", "triangle", "hexagon", "star"]
    user_specified = any(s in default_shapes and s != "octagon" for s in shape_list)
    if style in extra_styles:
        generator = STYLE_GENERATORS.get(style)
        try:
            inner = generator(palette, tile_size, complexity, motief_schaal)
        except TypeError:
            inner = generator(palette, tile_size, complexity)
    elif user_specified or shape_list == ["circle"] or shape_list == ["square"] or shape_list == ["triangle"]:
        inner = generate_geometric_svg(palette, tile_size, complexity, shape_list)
    else:
        generator = STYLE_GENERATORS.get(style, generate_geometric_svg)
        if generator == generate_geometric_svg:
            inner = generator(palette, tile_size, complexity, shape_list or ["octagon"])
        else:
            inner = generator(palette, tile_size, complexity)
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {tile_size} {tile_size}"
     width="{tile_size}" height="{tile_size}">
  <rect width="{tile_size}" height="{tile_size}" fill="{palette['background']}"/>
  {inner}
</svg>"""
    return svg


def build_repeat_svg(tile_svg: str, analysis: dict,
                     tile_cm: int, repeat_type: str,
                     dpi: int, cols: int = 3, rows: int = 3) -> str:
    """Bouw een all-over repeat SVG met het opgegeven repeat-type."""
    T = 400
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
                transform = f"translate({tx},{ty}) scale({sx},{sy})"
            else:
                transform = f"translate({x},{y})"

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
        if any(w in p for w in ['botanisch', 'bloem', 'blad', 'botanical', 'plant', 'flora']):
            analysis['style'] = 'botanical'
        elif any(w in p for w in ['vlechtwerk', 'vlecht', 'gevlochten', 'basketweave']):
            analysis['style'] = 'vlechtwerk'
        elif any(w in p for w in ['visgraat', 'herringbone', 'visbot']):
            analysis['style'] = 'visgraat'
        elif any(w in p for w in ['streep', 'strepen', 'stripe']):
            analysis['style'] = 'strepen'
        elif any(w in p for w in ['mozaiek', 'pixel', 'blokje']):
            analysis['style'] = 'mozaiek'
        elif any(w in p for w in ['chevron', 'zigzag']):
            analysis['style'] = 'chevron'
        elif any(w in p for w in ['hexagon', 'honingraat', 'zeshoek']):
            analysis['style'] = 'hexagon'
        elif any(w in p for w in ['ogee', 'schub', 'dakpan']):
            analysis['style'] = 'ogee'
        elif any(w in p for w in ['nordic', 'scandinavisch', 'noors', 'kruis', 'sneeuwvlok']):
            analysis['style'] = 'nordic'
        elif any(w in p for w in ['diamant', 'concentrisch']):
            analysis['style'] = 'diamant'
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
        tile_svg = build_tile_svg(analysis, tile_size=400, motief_schaal=motief_schaal)

        # Stap 3: Bouw all-over repeat
        repeat_svg = build_repeat_svg(tile_svg, analysis, tile_cm, repeat_type, dpi)

        # Stap 4: SVG als base64 voor preview in browser
        tile_b64 = base64.b64encode(tile_svg.encode()).decode()
        repeat_b64 = base64.b64encode(repeat_svg.encode()).decode()

        # Stap 5: Bereken resolutie-informatie
        px_per_tile = round(tile_cm / 2.54 * dpi)

        return jsonify({
            "success": True,
            "analysis": analysis,
            "tile_svg_b64": tile_b64,
            "repeat_svg_b64": repeat_b64,
            "info": {
                "style": analysis.get("style", ""),
                "description": analysis.get("description_nl", ""),
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
            + '</table></body></html>')
        msg1.attach(MIMEText(html1, 'html'))
        if bijlage:
            msg1.attach(bijlage)
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
