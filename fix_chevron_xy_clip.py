#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_chevron_xy_clip.py
-----------------------
Definitieve fix voor generate_chevron_bold_svg.

Probleem: de vorige clipPath-vrije versie clipte de banden alleen horizontaal
(kolombreedte). Door de naad-fix liepen banden ver buiten beeld (y tot -1100),
en zonder verticale clip vielen alleen verticale-balk-stukken binnen de
viewBox -> je zag balken i.p.v. schuine banden.

Fix: clip de polygonen in Python OOK verticaal op 0..T. Dan valt alleen het
zichtbare schuine deel binnen de tegel. Geen SVG clipPath (Safari-proof).
Visueel geverifieerd (clip_xy.png -> correcte versprongen chevron).

Timestamped backup vooraf. Idempotent.

Draai vanuit de projectmap:  python3 fix_chevron_xy_clip.py
BELANGRIJK: stop Flask (Ctrl+C) eerst.
"""

import os, re, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "modules_extra.py"

NEW_FUNC = '''def generate_chevron_bold_svg(palette, tile_size, complexity):
    """Chevron Bold: versprongen 45-graden velden, helling spiegelt per veld.
    Banden worden in Python bijgesneden op zowel de kolomgrenzen als de
    tegelranden (0..T), zodat de SVG alleen schone polygonen binnen de tegel
    bevat -- geen SVG clipPath (Safari-proof in base64-<img>). Naadloos.
    Kleur via _palet: k[0]=achtergrond, k[1]=bandkleur."""
    T = float(tile_size)
    k = _palet(palette)
    c_band = k[1]
    c_bg = k[0]
    n_cols = {'low': 3, 'medium': 4, 'high': 6}.get(complexity, 4)
    cw = T / n_cols
    stripe_w = cw * 0.5
    step = stripe_w * 2.0

    def _clip(pts, xmin, xmax, ymin, ymax):
        def edge(poly, inside, ix):
            out = []
            n = len(poly)
            for i in range(n):
                cur = poly[i]; prv = poly[i-1]
                ci = inside(cur); pi = inside(prv)
                if ci:
                    if not pi:
                        out.append(ix(prv, cur))
                    out.append(cur)
                elif pi:
                    out.append(ix(prv, cur))
            return out
        def ixx(a, b, xv):
            (x1, y1), (x2, y2) = a, b
            if x2 == x1:
                return (xv, y1)
            t = (xv - x1) / (x2 - x1)
            return (xv, y1 + t * (y2 - y1))
        def ixy(a, b, yv):
            (x1, y1), (x2, y2) = a, b
            if y2 == y1:
                return (x1, yv)
            t = (yv - y1) / (y2 - y1)
            return (x1 + t * (x2 - x1), yv)
        poly = pts
        poly = edge(poly, lambda p: p[0] >= xmin, lambda a, b: ixx(a, b, xmin))
        if not poly: return []
        poly = edge(poly, lambda p: p[0] <= xmax, lambda a, b: ixx(a, b, xmax))
        if not poly: return []
        poly = edge(poly, lambda p: p[1] >= ymin, lambda a, b: ixy(a, b, ymin))
        if not poly: return []
        poly = edge(poly, lambda p: p[1] <= ymax, lambda a, b: ixy(a, b, ymax))
        return poly

    s = ['<rect width="%.1f" height="%.1f" fill="%s"/>' % (T, T, c_bg)]
    for col in range(n_cols):
        x0 = col * cw
        x1 = x0 + cw
        slope = 1 if (col % 2 == 0) else -1
        voff = col * step * 0.5
        c = -int((T + cw) / step) - 6
        while c * step < 2 * T + cw + 6 * step:
            yb = c * step + voff
            if slope == 1:
                pts = [(x0, yb), (x0, yb + stripe_w),
                       (x1, yb + stripe_w - cw), (x1, yb - cw)]
            else:
                pts = [(x0, yb), (x0, yb + stripe_w),
                       (x1, yb + stripe_w + cw), (x1, yb + cw)]
            clipped = _clip(pts, x0, x1, 0.0, T)
            if len(clipped) >= 3:
                pts_str = ' '.join('%.2f,%.2f' % (px, py) for px, py in clipped)
                s.append('<polygon points="%s" fill="%s"/>' % (pts_str, c_band))
            c += 1
    return '\\n'.join(s)
'''

def main():
    if not os.path.exists(PATH):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")
    with open(PATH, "r", encoding="utf-8") as f:
        txt = f.read()
    if "zowel de kolomgrenzen als de tegelranden" in txt:
        print("= xy-clip-versie staat er al -- overgeslagen")
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
    print("+ generate_chevron_bold_svg vervangen (xy-clip, geen clipPath)")
    print("")
    print("Hierna:")
    print("  1) python3 -m py_compile modules_extra.py")
    print("  2) Start Flask opnieuw")
    print("  3) Hard refresh (Cmd+Shift+R), klik 'Chevron Bold'")
    print("  4) Zowel Basistegel als All-over repeat moeten de chevron tonen")

if __name__ == "__main__":
    main()
