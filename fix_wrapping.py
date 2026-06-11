code = open('modules_extra.py').read()

old_terrazzo = '''def generate_terrazzo_svg(palette, tile_size, complexity):
    import random as _r
    T = tile_size
    k = _palet(palette)
    rng = _r.Random(42)
    s = [f\'<rect width="{T}" height="{T}" fill="{k[0]}"/>\']
    n = {\'low\':40,\'medium\':80,\'high\':140}.get(complexity,80)
    for _ in range(n):
        x = rng.uniform(0, T)
        y = rng.uniform(0, T)
        w = rng.uniform(T*0.02, T*0.07)
        h = rng.uniform(T*0.02, T*0.06)
        angle = rng.uniform(0, 180)
        kleur = rng.choice(k[1:])
        s.append(f\'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{w:.1f}" ry="{h:.1f}" fill="{kleur}" transform="rotate({angle:.0f} {x:.1f} {y:.1f})"/>\')
    return \'\\n\'.join(s)'''

new_terrazzo = '''def generate_terrazzo_svg(palette, tile_size, complexity):
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

old_vrije = '''def generate_vrije_vormen_svg(palette, tile_size, complexity):
    import random as _r
    T = tile_size
    k = _palet(palette)
    rng = _r.Random(99)
    s = [f\'<rect width="{T}" height="{T}" fill="{k[0]}"/>\']
    n = {\'low\':6,\'medium\':10,\'high\':16}.get(complexity,10)
    for i in range(n):
        kleur = k[(i+1) % len(k)]
        cx = rng.uniform(T*0.1, T*0.9)
        cy = rng.uniform(T*0.1, T*0.9)
        r = rng.uniform(T*0.08, T*0.22)
        pts = []
        sides = rng.randint(5,9)
        for j in range(sides):
            a = math.radians(j * 360/sides + rng.uniform(-20,20))
            rd = r * rng.uniform(0.7, 1.3)
            pts.append(f\'{cx+rd*math.cos(a):.1f},{cy+rd*math.sin(a):.1f}\')
        s.append(f\'<polygon points="{" ".join(pts)}" fill="{kleur}" opacity="0.85"/>\')
    return \'\\n\'.join(s)'''

new_vrije = '''def generate_vrije_vormen_svg(palette, tile_size, complexity):
    import random as _r
    T = tile_size
    k = _palet(palette)
    rng = _r.Random(99)
    s = [f\'<rect width="{T}" height="{T}" fill="{k[0]}"/>\']
    n = {\'low\':6,\'medium\':10,\'high\':16}.get(complexity,10)
    def vorm(cx, cy, r, sides, offsets, kleur):
        pts = []
        for j,off in enumerate(offsets):
            a = math.radians(j * 360/sides + off)
            rd = r * 0.7 + r * 0.6 * (j % 3) / 3
            pts.append(f\'{cx+rd*math.cos(a):.1f},{cy+rd*math.sin(a):.1f}\')
        return f\'<polygon points="{" ".join(pts)}" fill="{kleur}" opacity="0.85"/>\'
    shapes = []
    for i in range(n):
        kleur = k[(i+1) % len(k)]
        cx = rng.uniform(0, T)
        cy = rng.uniform(0, T)
        r = rng.uniform(T*0.08, T*0.18)
        sides = rng.randint(5,8)
        offsets = [rng.uniform(-20,20) for _ in range(sides)]
        shapes.append((cx, cy, r, sides, offsets, kleur))
    for cx, cy, r, sides, offsets, kleur in shapes:
        for dx in [0, T, -T]:
            for dy in [0, T, -T]:
                nx, ny = cx+dx, cy+dy
                if -r < nx < T+r and -r < ny < T+r:
                    s.append(vorm(nx, ny, r, sides, offsets, kleur))
    return \'\\n\'.join(s)'''

code = code.replace(old_terrazzo, new_terrazzo)
code = code.replace(old_vrije, new_vrije)
open('modules_extra.py','w').write(code)
print('wrapping fix toegepast')
