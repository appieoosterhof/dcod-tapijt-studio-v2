code = open('modules_extra.py').read()

old = '''def generate_terrazzo_svg(palette, tile_size, complexity):
    import random as _r
    T = tile_size
    k = _palet(palette)
    rng = _r.Random(42)
    s = [f\'<rect width="{T}" height="{T}" fill="{k[0]}"/>\']
    n = {\'low\':40,\'medium\':80,\'high\':140}.get(complexity,80)
    def ellips(x, y, w, h, angle, kleur):
        return f\'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{w:.1f}" ry="{h:.1f}" fill="{kleur}" transform="rotate({angle:.0f} {x:.1f} {y:.1f})"/>\'
    for _ in range(n):
        x = rng.uniform(0, T)
        y = rng.uniform(0, T)
        w = rng.uniform(T*0.02, T*0.07)
        h = rng.uniform(T*0.02, T*0.06)
        angle = rng.uniform(0, 180)
        kleur = rng.choice(k[1:])
        for dx in [0, T, -T]:
            for dy in [0, T, -T]:
                if dx == 0 and dy == 0:
                    s.append(ellips(x+dx, y+dy, w, h, angle, kleur))
                elif abs(x+dx-T/2) < T/2+w and abs(y+dy-T/2) < T/2+h:
                    s.append(ellips(x+dx, y+dy, w, h, angle, kleur))
    return \'\\n\'.join(s)'''

new = '''def generate_terrazzo_svg(palette, tile_size, complexity, schaal=100):
    import random as _r
    T = tile_size
    k = _palet(palette)
    rng = _r.Random(42)
    s = [f\'<rect width="{T}" height="{T}" fill="{k[0]}"/>\']
    n = {\'low\':40,\'medium\':80,\'high\':140}.get(complexity,80)
    # Schaal bepaalt vlekgrootte direct
    factor = schaal / 100.0
    vlek_min = T * 0.015 * factor
    vlek_max = T * 0.055 * factor
    def ellips(x, y, w, h, angle, kleur):
        return f\'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{w:.1f}" ry="{h:.1f}" fill="{kleur}" transform="rotate({angle:.0f} {x:.1f} {y:.1f})"/>\'
    for _ in range(n):
        x = rng.uniform(0, T)
        y = rng.uniform(0, T)
        w = rng.uniform(vlek_min, vlek_max)
        h = rng.uniform(vlek_min * 0.5, vlek_max * 0.8)
        angle = rng.uniform(0, 180)
        kleur = rng.choice(k[1:])
        for dx in [0, T, -T]:
            for dy in [0, T, -T]:
                if dx == 0 and dy == 0:
                    s.append(ellips(x+dx, y+dy, w, h, angle, kleur))
                elif abs(x+dx-T/2) < T/2+w and abs(y+dy-T/2) < T/2+h:
                    s.append(ellips(x+dx, y+dy, w, h, angle, kleur))
    return \'\\n\'.join(s)'''

code = code.replace(old, new)
open('modules_extra.py','w').write(code)
print('terrazzo schaal fix klaar')
