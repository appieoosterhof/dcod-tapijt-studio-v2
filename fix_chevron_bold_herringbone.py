#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_chevron_bold_herringbone.py
--------------------------------
Vervangt generate_chevron_bold_svg door de GEVERIFIEERDE herringbone:
mirror-symmetrical 45-degree parallel stripe fields.

Verticale velden (kolommen) met evenwijdige 45-graden banden, afwisselend
twee kleuren; de helling spiegelt per veld -> versprongen naad op de
kolomgrens (zoals echte parket-visgraat).

Vooraf visueel gerenderd en gecontroleerd (fields_b).

- Timestamped backup van modules_extra.py vooraf.
- Vervangt ALLEEN generate_chevron_bold_svg.
- Idempotent.

Draai vanuit de projectmap:  python3 fix_chevron_bold_herringbone.py
BELANGRIJK: stop Flask (Ctrl+C) eerst.
"""

import os, re, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "modules_extra.py"

NEW_FUNC = '''def generate_chevron_bold_svg(palette, tile_size, complexity):
    """Chevron Bold: mirror-symmetrical 45-degree parallel stripe fields.
    Verticale velden met evenwijdige 45-graden banden (twee kleuren
    afwisselend); de helling spiegelt per veld, met versprongen naad op de
    kolomgrens (parket-visgraat look). Naadloos: veldbreedte deelt 400 exact
    en de banden lopen ruim buiten de tegel door.
    Kleur via _palet: k[0]=achtergrond/tweede band, k[1]=eerste band."""
    T = float(tile_size)
    k = _palet(palette)
    c_band = k[1]
    c_bg = k[0]
    n_cols = {'low': 3, 'medium': 4, 'high': 6}.get(complexity, 4)
    cw = T / n_cols
    stripe_w = cw * 0.5          # bandbreedte; 0.5*cw geeft brede banden zoals referentie
    step = stripe_w * 2.0

    s = ['<rect width="%.1f" height="%.1f" fill="%s"/>' % (T, T, c_bg)]
    for col in range(n_cols):
        x0 = col * cw
        x1 = x0 + cw
        slope = 1 if (col % 2 == 0) else -1
        clip_id = "cb_%d" % col
        s.append('<clipPath id="%s"><rect x="%.2f" y="0" width="%.2f" height="%.2f"/></clipPath>'
                 % (clip_id, x0, cw, T))
        s.append('<g clip-path="url(#%s)">' % clip_id)
        c = -int((T + cw) / step) - 2
        while c * step < 2 * T + cw:
            yb = c * step
            if slope == 1:
                pts = [(x0, yb), (x0, yb + stripe_w),
                       (x1, yb + stripe_w - cw), (x1, yb - cw)]
            else:
                pts = [(x0, yb), (x0, yb + stripe_w),
                       (x1, yb + stripe_w + cw), (x1, yb + cw)]
            pts_str = ' '.join('%.2f,%.2f' % (px, py) for px, py in pts)
            s.append('<polygon points="%s" fill="%s"/>' % (pts_str, c_band))
            c += 1
        s.append('</g>')
    return '\\n'.join(s)
'''

def main():
    if not os.path.exists(PATH):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")
    with open(PATH, "r", encoding="utf-8") as f:
        txt = f.read()
    if "mirror-symmetrical 45-degree parallel stripe fields" in txt:
        print("= Herringbone-versie staat er al -- overgeslagen")
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
    print("+ generate_chevron_bold_svg vervangen (herringbone stripe fields)")
    print("")
    print("Hierna:")
    print("  1) python3 -m py_compile modules_extra.py")
    print("  2) Start Flask opnieuw, hard refresh (Cmd+Shift+R), klik 'Chevron Bold'")

if __name__ == "__main__":
    main()
