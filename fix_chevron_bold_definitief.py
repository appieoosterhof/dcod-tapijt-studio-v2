#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_chevron_bold_definitief.py
-------------------------------
Vervangt generate_chevron_bold_svg door de GEVERIFIEERDE horizontale
chevron-stripe (V's omhoog), opgebouwd als doorlopende polyline-banden
volgens y = abs(mod(x,p) - p/2). Geen losse driehoeken.

Vooraf visueel gerenderd en gecontroleerd.

- Timestamped backup van modules_extra.py vooraf.
- Vervangt ALLEEN de functie generate_chevron_bold_svg.
- Idempotent: herkent of deze versie er al staat.

Draai vanuit de projectmap:  python3 fix_chevron_bold_definitief.py
BELANGRIJK: stop Flask (Ctrl+C) voordat je dit draait.
"""

import os
import re
import shutil
import datetime
import sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "modules_extra.py"

NEW_FUNC = '''def generate_chevron_bold_svg(palette, tile_size, complexity):
    """Chevron Bold: horizontale doorlopende chevron-stripe (V's omhoog).
    Opgebouwd als polyline-banden volgens y = abs(mod(x,p) - p/2), met
    constante breedte. Geen losse driehoeken. Naadloos: horizontale periode
    deelt de tegel (400) exact en de banden herhalen verticaal met dezelfde
    pitch. Kleur-klaar via _palet: k[0]=achtergrond, k[1]=bandkleur."""
    T = float(tile_size)
    k = _palet(palette)
    c_bg = k[0]
    c_band = k[1]
    n_strips = {'low': 4, 'medium': 6, 'high': 10}.get(complexity, 6)
    pitch = T / n_strips        # verticale afstand tussen banden
    p = pitch                   # horizontale periode = pitch -> 45 graden
    amp = pitch / 2.0           # verticale uitslag van de zigzag
    stripe_w = pitch * 0.5      # bandbreedte (verticaal gemeten)

    # Bemonster x fijn over [-T, 2T] zodat de polyline buiten de tegel doorloopt
    # (naadloos bij het tegelen). 240 samples geeft scherpe knikken.
    N = 240
    xs = [(-T) + (3.0 * T) * (i / float(N)) for i in range(N + 1)]

    s = ['<rect width="%.1f" height="%.1f" fill="%s"/>' % (T, T, c_bg)]
    for sidx in range(-1, n_strips + 1):
        y_center = sidx * pitch
        top = []
        bot = []
        for x in xs:
            m = x % p
            base = abs(m - p / 2.0)
            yz = (base / (p / 2.0)) * amp
            top.append((x, y_center + yz))
            bot.append((x, y_center + yz + stripe_w))
        poly_pts = top + bot[::-1]
        pts_str = ' '.join('%.2f,%.2f' % (px, py) for px, py in poly_pts)
        s.append('<polygon points="%s" fill="%s"/>' % (pts_str, c_band))
    return '\\n'.join(s)
'''

def main():
    if not os.path.exists(PATH):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")

    with open(PATH, "r", encoding="utf-8") as f:
        txt = f.read()

    if "horizontale doorlopende chevron-stripe" in txt:
        print("= Definitieve chevron-versie staat er al -- overgeslagen")
        return

    pat = re.compile(r'def generate_chevron_bold_svg\(.*?\):.*?(?=\ndef |\Z)', re.DOTALL)
    m = pat.search(txt)
    if not m:
        print("! Kon generate_chevron_bold_svg niet vinden -- handmatig nodig")
        return

    bak = PATH + ".bak_" + STAMP
    shutil.copy2(PATH, bak)
    print("+ Backup gemaakt: " + bak)

    txt = txt[:m.start()] + NEW_FUNC + txt[m.end():]
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(txt)
    print("+ generate_chevron_bold_svg vervangen (horizontale V's-omhoog chevron)")
    print("")
    print("Klaar. Hierna:")
    print("  1) python3 -m py_compile modules_extra.py")
    print("  2) Start Flask opnieuw")
    print("  3) Hard refresh (Cmd+Shift+R), klik 'Chevron Bold'")
    print("  4) Je zou nu horizontale zwarte zigzag-strepen (V's omhoog) moeten zien")

if __name__ == "__main__":
    main()
