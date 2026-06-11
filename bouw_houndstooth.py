#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bouw_houndstooth.py
--------------------
Bouwt de nieuwe stijl 'houndstooth' (pied-de-poule / hanenpoot) volledig in,
op exact dezelfde manier als chevron_bold, met alle geleerde lessen:
- generator zonder clipPath (Safari-proof base64-img)
- routing-guard zodat de AI-beschrijving de stijl niet kaapt
- geregistreerd in STYLE_GENERATORS, extra_styles, beide routing-blokken,
  trefwoordenlijst, en import
- knop in index.html
- cache-stempel opgehoogd

Wiskundig exacte tegel: zwart en wit vormen identieke ineengrijpende haken
(verified: tegelt naadloos).

Timestamped backups van alle 3 de bestanden. Idempotent.
Draai vanuit de projectmap; stop Flask eerst.
"""
import os, re, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path):
    shutil.copy2(path, path + ".bak_" + STAMP)
    print("  + Backup: " + path + ".bak_" + STAMP)

# ---------- 1. Generator in modules_extra.py ----------
GEN = '''

def generate_houndstooth_svg(palette, tile_size, complexity):
    """Pied-de-poule (hanenpoot): wiskundig exacte getande haakvorm die
    naadloos tegelt; zwart en wit vormen identieke ineengrijpende haken.
    Geen clipPath (Safari-proof als base64-img).
    Kleur via _palet: k[0]=achtergrond (witte ruimte), k[1]=motief (haak)."""
    T = float(tile_size)
    k = _palet(palette)
    c_bg = k[0]
    c_fg = k[1]
    s = T / 4.0
    poly = [(0,2),(2,0),(2,1),(3,1),(3,0),(4,0),(4,2),(2,4),(2,3),(1,3),(1,4),(0,4)]
    pts = ' '.join('%.2f,%.2f' % (x*s, y*s) for x, y in poly)
    parts = ['<rect width="%.1f" height="%.1f" fill="%s"/>' % (T, T, c_bg)]
    parts.append('<polygon points="%s" fill="%s"/>' % (pts, c_fg))
    return '\\n'.join(parts)
'''

def patch_modules():
    path = "modules_extra.py"
    print("[1/3] " + path)
    with open(path, encoding="utf-8") as f: txt = f.read()
    if "def generate_houndstooth_svg" in txt:
        print("  = generator staat er al"); return
    backup(path)
    with open(path, "a", encoding="utf-8") as f: f.write(GEN)
    print("  + generate_houndstooth_svg toegevoegd")

# ---------- 2. app.py op alle plekken ----------
def patch_app():
    path = "app.py"
    print("[2/3] " + path)
    with open(path, encoding="utf-8") as f: txt = f.read()
    if "generate_houndstooth_svg" in txt:
        print("  = app.py al gepatcht"); return
    backup(path)

    # 2a. import (achter ..., generate_chevron_bold_svg)
    txt = txt.replace(
        "generate_artdeco_svg, generate_chevron_bold_svg",
        "generate_artdeco_svg, generate_chevron_bold_svg, generate_houndstooth_svg", 1)

    # 2b. STYLE_GENERATORS
    txt = txt.replace(
        '    "chevron_bold": generate_chevron_bold_svg,\n',
        '    "chevron_bold": generate_chevron_bold_svg,\n    "houndstooth": generate_houndstooth_svg,\n', 1)

    # 2c. eerste routing-blok (gebruikt 'p'), met guard
    txt = txt.replace(
        '    elif any(w in p for w in ["chevronbold", "chevron bold", "chevron blok"]):\n        style = "chevron_bold"\n',
        '    elif any(w in p for w in ["chevronbold", "chevron bold", "chevron blok"]):\n        style = "chevron_bold"\n'
        '    elif style == "houndstooth" or any(w in p for w in ["houndstooth", "hanenpoot", "pied-de-poule", "pied de poule", "pita"]):\n        style = "houndstooth"\n', 1)

    # 2d. tweede routing-blok (prompt_lower), met guard
    txt = txt.replace(
        '    elif style == "chevron_bold" or any(w in prompt_lower for w in ["chevronbold", "chevron bold", "chevron blok"]):\n        style = "chevron_bold"\n',
        '    elif style == "chevron_bold" or any(w in prompt_lower for w in ["chevronbold", "chevron bold", "chevron blok"]):\n        style = "chevron_bold"\n'
        '    elif style == "houndstooth" or any(w in prompt_lower for w in ["houndstooth", "hanenpoot", "pied-de-poule", "pied de poule", "pita"]):\n        style = "houndstooth"\n', 1)

    # 2e. derde routing-blok in analyse (analysis['style']), met guard
    txt = txt.replace(
        "        elif any(w in p for w in ['chevronbold', 'chevron bold', 'chevron blok']):\n            analysis['style'] = 'chevron_bold'\n",
        "        elif any(w in p for w in ['chevronbold', 'chevron bold', 'chevron blok']):\n            analysis['style'] = 'chevron_bold'\n"
        "        elif analysis.get('style') == 'houndstooth' or any(w in p for w in ['houndstooth', 'hanenpoot', 'pied-de-poule', 'pied de poule', 'pita']):\n            analysis['style'] = 'houndstooth'\n", 1)

    # 2f. extra_styles lijst
    txt = txt.replace(
        '"chevron_bold","hexagon"',
        '"chevron_bold","houndstooth","hexagon"', 1)

    # 2g. trefwoordenlijst (tuples)
    txt = txt.replace(
        "            (['chevronbold', 'chevron bold', 'chevron blok'], 'chevron_bold'),\n",
        "            (['chevronbold', 'chevron bold', 'chevron blok'], 'chevron_bold'),\n"
        "            (['houndstooth', 'hanenpoot', 'pied-de-poule', 'pied de poule', 'pita'], 'houndstooth'),\n", 1)

    with open(path, "w", encoding="utf-8") as f: f.write(txt)
    print("  + app.py gepatcht (import, STYLE_GENERATORS, 3 routing-blokken, extra_styles, trefwoorden)")

# ---------- 3. index.html knop + cache-stempel ----------
def patch_index():
    path = "templates/index.html"
    print("[3/3] " + path)
    with open(path, encoding="utf-8") as f: txt = f.read()
    if "Hanenpoot" in txt or "houndstooth patroon" in txt:
        print("  = knop staat er al")
    else:
        backup(path)
        anchor = "<button class=\"chip\" onclick=\"setPrompt('chevronbold patroon, gevulde schuine plankjes, zwart wit')\">Chevron Bold</button>"
        hb = "<button class=\"chip\" onclick=\"setPrompt('houndstooth patroon, hanenpoot pied-de-poule, zwart wit')\">Hanenpoot</button>"
        newbtn = anchor + "\n          " + hb
        txt = txt.replace(anchor, newbtn, 1)
        # cache-stempel ophogen
        txt = re.sub(r'app\\.js\\?v=[0-9_]+', 'app.js?v=' + STAMP, txt, count=1)
        with open(path, "w", encoding="utf-8") as f: f.write(txt)
        print("  + Hanenpoot-knop toegevoegd + cache-stempel opgehoogd naar v=" + STAMP)

def main():
    need = ["modules_extra.py", "app.py", "templates/index.html"]
    if not all(os.path.exists(x) for x in need):
        sys.exit("FOUT: draai vanuit ~/Desktop/tapijt-studio.")
    print("=== Houndstooth inbouwen (" + STAMP + ") ===")
    patch_modules()
    patch_app()
    patch_index()
    print("")
    print("Hierna:")
    print("  1) python3 -m py_compile app.py modules_extra.py")
    print("  2) Start Flask opnieuw")
    print("  3) Hard refresh (Cmd+Shift+R)")
    print("  4) Klik de knop 'Hanenpoot' -> pied-de-poule verschijnt")

if __name__ == "__main__":
    main()
