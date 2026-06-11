#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bouw_urban_plaid.py
--------------------
Bouwt de nieuwe stijl 'urban_plaid' (tartan/ruit) volledig in, zelfde aanpak
als houndstooth/chevron_bold:
- generator zonder clipPath (Safari-proof), naadloos raster van banden
- mengkruispunten via opacity 0.55 (geweven tartan-effect)
- kleuren uit het palet (primary + secondary als bandkleuren, background = bg)
- routing-guards op alle 3 de blokken
- geregistreerd in import, STYLE_GENERATORS, extra_styles, trefwoorden
- knop in index.html (alfabetisch tussen Terrazzo en Visgraat)
- cache-stempel opgehoogd

Timestamped backups van alle 3 de bestanden. Idempotent.
Draai vanuit de projectmap; stop Flask eerst.
"""
import os, re, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path):
    shutil.copy2(path, path + ".bak_" + STAMP)
    print("  + Backup: " + path + ".bak_" + STAMP)

# ---------- 1. Generator ----------
GEN = '''

def generate_urban_plaid_svg(palette, tile_size, complexity):
    """Urban Plaid (tartan/ruit): naadloos raster van horizontale en verticale
    banden met wisselende diktes; kruispunten mengen via opacity (geweven
    tartan-effect). Geen clipPath (Safari-proof).
    Kleur via _palet: k[0]=achtergrond, k[1]/k[2]=bandkleuren."""
    T = float(tile_size)
    k = _palet(palette)
    bg = k[0]; c1 = k[1]; c2 = k[2]
    # sett: (breedte-eenheden, kleur). 0 = achtergrond (geen band).
    sett = [
        (8, 0), (10, c1), (2, c1), (4, 0), (2, c1), (6, 0), (1, c1), (3, 0), (1, c1), (4, 0),
        (16, c1),
        (4, 0), (2, c1), (2, 0), (2, c1), (4, 0),
        (6, c2), (2, 0), (6, c2),
        (4, 0), (1, c1), (2, 0), (1, c1), (4, 0),
        (12, c1), (3, 0), (3, c1),
        (6, 0),
    ]
    tot = sum(w for w, _ in sett)
    scale = T / tot
    bands = []
    pos = 0.0
    for w, col in sett:
        ww = w * scale
        if col != 0:
            bands.append((pos, ww, col))
        pos += ww
    op = "0.55"
    parts = ['<rect width="%.1f" height="%.1f" fill="%s"/>' % (T, T, bg)]
    for x, w, col in bands:
        parts.append('<rect x="%.2f" y="0" width="%.2f" height="%.1f" fill="%s" opacity="%s"/>' % (x, w, T, col, op))
    for y, w, col in bands:
        parts.append('<rect x="0" y="%.2f" width="%.1f" height="%.2f" fill="%s" opacity="%s"/>' % (y, T, w, col, op))
    return '\\n'.join(parts)
'''

def patch_modules():
    path = "modules_extra.py"
    print("[1/3] " + path)
    with open(path, encoding="utf-8") as f: txt = f.read()
    if "def generate_urban_plaid_svg" in txt:
        print("  = generator staat er al"); return
    backup(path)
    with open(path, "a", encoding="utf-8") as f: f.write(GEN)
    print("  + generate_urban_plaid_svg toegevoegd")

def patch_app():
    path = "app.py"
    print("[2/3] " + path)
    with open(path, encoding="utf-8") as f: txt = f.read()
    if "generate_urban_plaid_svg" in txt:
        print("  = app.py al gepatcht"); return
    backup(path)

    txt = txt.replace(
        "generate_chevron_bold_svg, generate_houndstooth_svg",
        "generate_chevron_bold_svg, generate_houndstooth_svg, generate_urban_plaid_svg", 1)

    txt = txt.replace(
        '    "houndstooth": generate_houndstooth_svg,\n',
        '    "houndstooth": generate_houndstooth_svg,\n    "urban_plaid": generate_urban_plaid_svg,\n', 1)

    # eerste routing-blok (p)
    txt = txt.replace(
        '    elif style == "houndstooth" or any(w in p for w in ["houndstooth", "hanenpoot", "pied-de-poule", "pied de poule", "pita"]):\n        style = "houndstooth"\n',
        '    elif style == "houndstooth" or any(w in p for w in ["houndstooth", "hanenpoot", "pied-de-poule", "pied de poule", "pita"]):\n        style = "houndstooth"\n'
        '    elif style == "urban_plaid" or any(w in p for w in ["urban plaid", "plaid", "tartan", "ruit", "schots"]):\n        style = "urban_plaid"\n', 1)

    # tweede routing-blok (prompt_lower)
    txt = txt.replace(
        '    elif style == "houndstooth" or any(w in prompt_lower for w in ["houndstooth", "hanenpoot", "pied-de-poule", "pied de poule", "pita"]):\n        style = "houndstooth"\n',
        '    elif style == "houndstooth" or any(w in prompt_lower for w in ["houndstooth", "hanenpoot", "pied-de-poule", "pied de poule", "pita"]):\n        style = "houndstooth"\n'
        '    elif style == "urban_plaid" or any(w in prompt_lower for w in ["urban plaid", "plaid", "tartan", "ruit", "schots"]):\n        style = "urban_plaid"\n', 1)

    # derde routing-blok (analysis)
    txt = txt.replace(
        "        elif analysis.get('style') == 'houndstooth' or any(w in p for w in ['houndstooth', 'hanenpoot', 'pied-de-poule', 'pied de poule', 'pita']):\n            analysis['style'] = 'houndstooth'\n",
        "        elif analysis.get('style') == 'houndstooth' or any(w in p for w in ['houndstooth', 'hanenpoot', 'pied-de-poule', 'pied de poule', 'pita']):\n            analysis['style'] = 'houndstooth'\n"
        "        elif analysis.get('style') == 'urban_plaid' or any(w in p for w in ['urban plaid', 'plaid', 'tartan', 'ruit', 'schots']):\n            analysis['style'] = 'urban_plaid'\n", 1)

    # extra_styles
    txt = txt.replace(
        '"houndstooth","hexagon"',
        '"houndstooth","urban_plaid","hexagon"', 1)

    # trefwoorden
    txt = txt.replace(
        "            (['houndstooth', 'hanenpoot', 'pied-de-poule', 'pied de poule', 'pita'], 'houndstooth'),\n",
        "            (['houndstooth', 'hanenpoot', 'pied-de-poule', 'pied de poule', 'pita'], 'houndstooth'),\n"
        "            (['urban plaid', 'plaid', 'tartan', 'ruit', 'schots'], 'urban_plaid'),\n", 1)

    with open(path, "w", encoding="utf-8") as f: f.write(txt)
    print("  + app.py gepatcht (import, STYLE_GENERATORS, 3 routing-blokken, extra_styles, trefwoorden)")

def patch_index():
    path = "templates/index.html"
    print("[3/3] " + path)
    with open(path, encoding="utf-8") as f: txt = f.read()
    if "Urban Plaid" in txt:
        print("  = knop staat er al")
        return
    backup(path)
    # knop toevoegen na Terrazzo (alfabetisch komt Urban Plaid na Terrazzo, voor Visgraat)
    terr = '<button class="chip" onclick="setPrompt(&#39;Terrazzo patroon, gekleurde steensnippers op lichte ondergrond&#39;)">Terrazzo</button>'.replace("&#39;", chr(39))
    up = '<button class="chip" onclick="setPrompt(&#39;urban plaid tartan ruit patroon, geweven lijnen&#39;)">Urban Plaid</button>'.replace("&#39;", chr(39))
    if terr in txt:
        txt = txt.replace(terr, terr + "\\n          " + up, 1)
        print("  + Urban Plaid-knop toegevoegd na Terrazzo")
    else:
        # fallback: na Houndstooth
        hb = '>Houndstooth</button>'
        idx = txt.find(hb)
        if idx != -1:
            end = idx + len(hb)
            txt = txt[:end] + "\\n          " + up + txt[end:]
            print("  + Urban Plaid-knop toegevoegd na Houndstooth (fallback)")
        else:
            print("  ! Kon geen ankerknop vinden -- knop niet toegevoegd")
    txt = re.sub(r'app\\.js\\?v=[0-9_]+', 'app.js?v=' + STAMP, txt, count=1)
    with open(path, "w", encoding="utf-8") as f: f.write(txt)
    print("  + cache-stempel -> v=" + STAMP)

def main():
    need = ["modules_extra.py", "app.py", "templates/index.html"]
    if not all(os.path.exists(x) for x in need):
        sys.exit("FOUT: draai vanuit ~/Desktop/tapijt-studio.")
    print("=== Urban Plaid inbouwen (" + STAMP + ") ===")
    patch_modules()
    patch_app()
    patch_index()
    print("")
    print("Hierna:")
    print("  1) python3 -m py_compile app.py modules_extra.py")
    print("  2) Start Flask opnieuw")
    print("  3) Hard refresh (Cmd+Shift+R)")
    print("  4) Klik 'Urban Plaid' -> geweven tartan verschijnt")

if __name__ == "__main__":
    main()
