#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_vrije_vormen_rijk.py
-------------------------
Vervangt generate_vrije_vormen_svg door een rijkere versie:
- MEER vormen (medium 20 i.p.v. 7), dichter op elkaar
- GROTER en overlappend (opacity-menging)
- MEER kleurvariatie (willekeurig uit hele palet per vorm)
- gelijkmatig verspreid via jittered grid (geen lege banden)
- WILLEKEURIGE seed -> elke klik een andere vorm
- naadloos via wrap; geen clipPath (Safari-proof)

Visueel geverifieerd (vrije_d.png). Raakt alleen modules_extra.py.
Backup. Idempotent. Draai vanuit projectmap; stop Flask eerst.
"""
import os, re, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "modules_extra.py"

NEW = '''def generate_vrije_vormen_svg(palette, tile_size, complexity):
    """Rijke organische vormen: veel overlappende veelhoeken, alle paletkleuren
    door elkaar, gelijkmatig verspreid, naadloos via wrap. Willekeurige seed ->
    elke generatie anders. Geen clipPath (Safari-proof)."""
    import random as _r
    T = tile_size; k = _palet(palette); rng = _r.Random()
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    n = {'low': 12, 'medium': 20, 'high': 30}.get(complexity, 20)
    cols = max(3, int(n ** 0.5) + 1); rows = max(3, (n + cols - 1) // cols)
    sx = T / cols; sy = T / rows
    shapes = []
    idx = 0
    for row in range(rows):
        for col in range(cols):
            if idx >= n: break
            cx = (col + 0.5) * sx + rng.uniform(-sx * 0.35, sx * 0.35)
            cy = (row + 0.5) * sy + rng.uniform(-sy * 0.35, sy * 0.35)
            r = rng.uniform(T * 0.09, T * 0.17)
            sides = rng.randint(5, 9)
            offs = [rng.uniform(-18, 18) for _ in range(sides)]
            rads = [r * rng.uniform(0.7, 1.25) for _ in range(sides)]
            kleur = k[rng.randint(1, 4)]
            shapes.append((cx % T, cy % T, sides, offs, rads, kleur))
            idx += 1
    def vorm(cx, cy, sides, offs, rads, kleur):
        pts = []
        for j in range(sides):
            a = math.radians(j * 360 / sides + offs[j])
            pts.append(f'{cx+rads[j]*math.cos(a):.1f},{cy+rads[j]*math.sin(a):.1f}')
        return f'<polygon points="{" ".join(pts)}" fill="{kleur}" opacity="0.88"/>'
    for cx, cy, sides, offs, rads, kleur in shapes:
        mr = max(rads)
        for dx in (0, T, -T):
            for dy in (0, T, -T):
                nx, ny = cx + dx, cy + dy
                if -mr < nx < T + mr and -mr < ny < T + mr:
                    s.append(vorm(nx, ny, sides, offs, rads, kleur))
    return '\\n'.join(s)
'''

def main():
    if not os.path.exists(PATH):
        sys.exit("FOUT: draai vanuit ~/Desktop/tapijt-studio.")
    with open(PATH, encoding="utf-8") as f:
        txt = f.read()
    if "Rijke organische vormen" in txt:
        print("= Rijke versie staat er al -- overgeslagen"); return
    pat = re.compile(r'def generate_vrije_vormen_svg\(.*?\):.*?(?=\ndef )', re.DOTALL)
    m = pat.search(txt)
    if not m:
        print("! Kon generate_vrije_vormen_svg niet vinden"); return
    shutil.copy2(PATH, PATH + ".bak_" + STAMP)
    print("+ Backup: " + PATH + ".bak_" + STAMP)
    txt = txt[:m.start()] + NEW + "\n" + txt[m.end():]
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(txt)
    print("+ generate_vrije_vormen_svg vervangen (rijker + variatie)")
    print("")
    print("Hierna:")
    print("  1) python3 -m py_compile modules_extra.py")
    print("  2) Start Flask opnieuw")
    print("  3) Hard refresh, klik meermaals 'Vrije vormen' -> elke keer anders")

if __name__ == "__main__":
    main()
