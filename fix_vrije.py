code = open('modules_extra.py').read()

old = '''def generate_vrije_vormen_svg(palette, tile_size, complexity):
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

new = '''def generate_vrije_vormen_svg(palette, tile_size, complexity):
    import random as _r
    T = tile_size
    k = _palet(palette)
    rng = _r.Random(99)
    s = [f\'<rect width="{T}" height="{T}" fill="{k[0]}"/>\']
    n = {\'low\':8,\'medium\':14,\'high\':22}.get(complexity,14)
    def vorm(cx, cy, r, sides, offsets, kleur):
        pts = []
        for j,off in enumerate(offsets):
            a = math.radians(j * 360/sides + off)
            rd = r * rng.uniform(0.6, 1.2)
            pts.append(f\'{cx+rd*math.cos(a):.1f},{cy+rd*math.sin(a):.1f}\')
        return f\'<polygon points="{" ".join(pts)}" fill="{kleur}" opacity="0.82"/>\'
    shapes = []
    # Verdeel vormen gelijkmatig over grid
    grid = int(n**0.5) + 1
    cel = T / grid
    for i in range(n):
        row = i // grid
        col = i % grid
        cx = col * cel + rng.uniform(cel*0.1, cel*0.9)
        cy = row * cel + rng.uniform(cel*0.1, cel*0.9)
        r = rng.uniform(T*0.06, T*0.14)
        sides = rng.randint(4,8)
        offsets = [rng.uniform(-25,25) for _ in range(sides)]
        kleur = k[(i+1) % len(k)]
        shapes.append((cx, cy, r, sides, offsets, kleur))
    for cx, cy, r, sides, offsets, kleur in shapes:
        for dx in [0, T, -T]:
            for dy in [0, T, -T]:
                nx, ny = cx+dx, cy+dy
                if -r < nx < T+r and -r < ny < T+r:
                    s.append(vorm(nx, ny, r, sides, offsets, kleur))
    return \'\\n\'.join(s)'''

code = code.replace(old, new)
open('modules_extra.py','w').write(code)
print('vrije vormen bijgewerkt')
