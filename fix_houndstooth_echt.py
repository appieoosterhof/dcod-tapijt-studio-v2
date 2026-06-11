#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_houndstooth_echt.py
------------------------
Vervangt generate_houndstooth_svg door een ECHTE, herkenbare pied-de-poule:
de bewezen houndstooth-haakpolygon, meerdere keren herhaald per tegel zodat
de schaal klopt (fijne geweven textuur, herkenbaar ook bij verkleinen in
'Bekijk in ruimte').

Dichtheid instelbaar via complexiteit: low=3x3, medium=4x4, high=6x6.
Geen clipPath (Safari-proof). Naadloos via wrap (-1..n_rep+1).
Kleur via _palet: k[0]=achtergrond, k[1]=motief.

Visueel geverifieerd (final_3.png / final_5.png). Raakt alleen modules_extra.py.
Backup. Idempotent. Draai vanuit projectmap; stop Flask eerst.
"""
import os, re, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "modules_extra.py"

NEW = '''def generate_houndstooth_svg(palette, tile_size, complexity):
    """Echte pied-de-poule (hanenpoot): de karakteristieke haakvorm, meerdere
    keren per tegel herhaald voor de fijne geweven textuur. Dichtheid via
    complexiteit (low=3, medium=4, high=6). Geen clipPath (Safari-proof).
    Naadloos via wrap. Kleur: k[0]=achtergrond, k[1]=motief."""
    T = float(tile_size)
    k = _palet(palette)
    c_bg = k[0]
    c_fg = k[1]
    n_rep = {'low': 3, 'medium': 4, 'high': 6}.get(complexity, 4)
    unit = T / n_rep
    s = unit / 4.0
    base = [(0,2),(2,0),(2,1),(3,1),(3,0),(4,0),(4,2),(2,4),(2,3),(1,3),(1,4),(0,4)]
    parts = ['<rect width="%.1f" height="%.1f" fill="%s"/>' % (T, T, c_bg)]
    for i in range(-1, n_rep + 1):
        for j in range(-1, n_rep + 1):
            ox = i * unit
            oy = j * unit
            pts = ' '.join('%.2f,%.2f' % (x*s + ox, y*s + oy) for x, y in base)
            parts.append('<polygon points="%s" fill="%s"/>' % (pts, c_fg))
    return '\\n'.join(parts)
'''

def main():
    if not os.path.exists(PATH):
        sys.exit("FOUT: draai vanuit ~/Desktop/tapijt-studio.")
    with open(PATH, encoding="utf-8") as f:
        txt = f.read()
    if "meerdere\n    keren per tegel herhaald" in txt or "n_rep = {'low': 3, 'medium': 4, 'high': 6}" in txt:
        print("= Echte houndstooth staat er al -- overgeslagen"); return
    pat = re.compile(r'def generate_houndstooth_svg\(.*?\):.*?(?=\ndef |\Z)', re.DOTALL)
    m = pat.search(txt)
    if not m:
        print("! Kon generate_houndstooth_svg niet vinden"); return
    shutil.copy2(PATH, PATH + ".bak_" + STAMP)
    print("+ Backup: " + PATH + ".bak_" + STAMP)
    txt = txt[:m.start()] + NEW + txt[m.end():]
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(txt)
    print("+ generate_houndstooth_svg vervangen (echte, fijnere pied-de-poule)")
    print("")
    print("Hierna:")
    print("  1) python3 -m py_compile modules_extra.py")
    print("  2) Start Flask opnieuw")
    print("  3) Hard refresh, klik 'Houndstooth' -> fijne herkenbare hanenpoot")
    print("     (Tip: complexiteit low/medium/high regelt de fijnheid)")

if __name__ == "__main__":
    main()
