import math, random

def _hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _lerp(c1, c2, t):
    r1,g1,b1 = _hex_to_rgb(c1)
    r2,g2,b2 = _hex_to_rgb(c2)
    return '#{:02x}{:02x}{:02x}'.format(int(r1+(r2-r1)*t),int(g1+(g2-g1)*t),int(b1+(b2-b1)*t))

def _gradient(colors, t):
    if len(colors)==1: return colors[0]
    n=len(colors)-1; i=min(int(t*n),n-1)
    return _lerp(colors[i],colors[i+1],(t*n)-i)

def _palet(palette):
    return [palette.get('background','#F5F5F5'),palette.get('primary','#C4753A'),palette.get('secondary','#8B4513'),palette.get('accent1','#D4A055'),palette.get('accent2','#F0C080')]

def generate_strepen_svg(palette,tile_size,complexity):
    T=tile_size; k=_palet(palette); n={'low':4,'medium':6,'high':10}.get(complexity,6); b=T/n
    s=[]
    for i in range(n+1): s.append(f'<rect x="{i*b:.1f}" y="0" width="{b:.1f}" height="{T}" fill="{k[i%len(k)]}"/>')
    return '\n'.join(s)

def generate_mozaiek_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    n = {'low': 8, 'medium': 14, 'high': 22}.get(complexity, 14)
    b = T / n; rng = random.Random(2026)
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    for col in range(n + 1):
        x = col * b; y = 0
        while y < T:
            h = rng.randint(int(b * 0.6), int(b * 2.2)); h = min(h, T - y)
            kleur = k[(col + int(y / b)) % len(k)]
            s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{b-1:.1f}" height="{h-1:.1f}" fill="{kleur}"/>')
            y += h
    return '\n'.join(s)

def generate_chevron_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    n = {'low': 5, 'medium': 8, 'high': 14}.get(complexity, 8)
    h = T / n
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    for row in range(-1, n + 2):
        yb = row * h
        kleur = k[1 + (row % (len(k) - 1))]
        np2 = math.ceil(T / h) + 3
        pts = []
        for i in range(-1, np2):
            x = i * h
            pts.append(f'{x:.1f},{yb + h:.1f}')
            pts.append(f'{x + h / 2:.1f},{yb:.1f}')
        pts.append(f'{T + h:.1f},{yb:.1f}')
        pts.append(f'{T + h:.1f},{yb + h:.1f}')
        pts_str = ' '.join(pts)
        s.append(f'<polygon points="{pts_str}" fill="{kleur}"/>')
    return '\n'.join(s)

def generate_hexagoon_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    r = {'low': T // 5, 'medium': T // 8, 'high': T // 12}.get(complexity, T // 8)
    wh = math.sqrt(3) * r; cs = wh; rs = r * 1.5
    cols = math.ceil(T / cs) + 3; rows = math.ceil(T / rs) + 3
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    for row in range(-1, rows):
        for col in range(-1, cols):
            cx = col * cs + (wh / 2 if row % 2 else 0) - wh / 2
            cy = row * rs - r
            kleur = k[1 + ((col + row) % (len(k) - 1))]
            stroke = k[2]
            pts = [f'{cx + r * math.cos(math.radians(a * 60)):.2f},{cy + r * math.sin(math.radians(a * 60)):.2f}' for a in range(6)]
            pts_str = ' '.join(pts)
            s.append(f'<polygon points="{pts_str}" fill="{kleur}" stroke="{stroke}" stroke-width="1"/>')
    return '\n'.join(s)

def generate_ogee_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    n = {'low': 3, 'medium': 5, 'high': 8}.get(complexity, 5)
    b = T / n; h = b * 0.8; rs = h * 0.62
    rows = math.ceil(T / rs) + 4
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    for row in range(rows - 1, -2, -1):
        kleur = k[1 + (row % (len(k) - 1))]
        for col in range(-1, n + 2):
            x = col * b + (b / 2 if row % 2 else 0) - b
            y = row * rs - h * 0.3
            cx = x + b / 2
            d = f'M {x:.1f} {y+h:.1f} Q {cx:.1f} {y-h*0.1:.1f} {x+b:.1f} {y+h:.1f} Q {x+b+b*0.1:.1f} {y+h*1.8:.1f} {cx:.1f} {y+h*1.75:.1f} Q {x-b*0.1:.1f} {y+h*1.8:.1f} {x:.1f} {y+h:.1f} Z'
            s.append(f'<path d="{d}" fill="{kleur}" stroke="{k[0]}" stroke-width="0.5"/>')
    return '\n'.join(s)

def generate_diamant_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    nc = {'low': 2, 'medium': 3, 'high': 4}.get(complexity, 3)
    nl = {'low': 5, 'medium': 8, 'high': 12}.get(complexity, 8)
    tw = T / nc; th = tw * 1.3
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    def draw_diamond(cx, cy):
        for i in range(nl, 0, -1):
            sc = i / nl; w2 = (tw / 2 - 3) * sc; h2 = (th / 2 - 3) * sc
            kleur = k[1 + ((nl - i) % (len(k) - 1))]
            pts = f'{cx:.1f},{cy-h2:.1f} {cx+w2:.1f},{cy:.1f} {cx:.1f},{cy+h2:.1f} {cx-w2:.1f},{cy:.1f}'
            s.append(f'<polygon points="{pts}" fill="none" stroke="{kleur}" stroke-width="1.2"/>')
    for row in range(-1, math.ceil(T / th) + 2):
        for col in range(-1, nc + 2):
            cx = col * tw + (tw / 2 if row % 2 else 0)
            cy = row * th + th / 2
            draw_diamond(cx, cy)
            margin = tw / 2
            if cx - margin < 0: draw_diamond(cx + T, cy)
            if cx + margin > T: draw_diamond(cx - T, cy)
            if cy - th / 2 < 0: draw_diamond(cx, cy + T)
            if cy + th / 2 > T: draw_diamond(cx, cy - T)
    return '\n'.join(s)

def generate_terrazzo_svg(palette, tile_size, complexity, schaal=100):
    import random as _r
    T = tile_size; k = _palet(palette); rng = _r.Random(42)
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    n = {'low': 40, 'medium': 80, 'high': 140}.get(complexity, 80)
    factor = schaal / 100.0
    vlek_min = T * 0.015 * factor; vlek_max = T * 0.055 * factor
    def ellips(x, y, w, h, angle, kleur):
        return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{w:.1f}" ry="{h:.1f}" fill="{kleur}" transform="rotate({angle:.0f} {x:.1f} {y:.1f})"/>'
    for _ in range(n):
        x = rng.uniform(0, T); y = rng.uniform(0, T)
        w = rng.uniform(vlek_min, vlek_max); h = rng.uniform(vlek_min * 0.5, vlek_max * 0.8)
        angle = rng.uniform(0, 180); kleur = rng.choice(k[1:])
        for dx in [0, T, -T]:
            for dy in [0, T, -T]:
                if dx == 0 and dy == 0: s.append(ellips(x+dx, y+dy, w, h, angle, kleur))
                elif abs(x+dx-T/2) < T/2+w and abs(y+dy-T/2) < T/2+h: s.append(ellips(x+dx, y+dy, w, h, angle, kleur))
    return '\n'.join(s)

def generate_vrije_vormen_svg(palette, tile_size, complexity):
    import random as _r
    T = tile_size; k = _palet(palette); rng = _r.Random(99)
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    n = {'low': 8, 'medium': 14, 'high': 22}.get(complexity, 14)
    def vorm(cx, cy, r, sides, offsets, kleur):
        pts = []
        for j, off in enumerate(offsets):
            a = math.radians(j * 360 / sides + off)
            rd = r * rng.uniform(0.6, 1.2)
            pts.append(f'{cx+rd*math.cos(a):.1f},{cy+rd*math.sin(a):.1f}')
        pts_str = ' '.join(pts)
        return f'<polygon points="{pts_str}" fill="{kleur}" opacity="0.82"/>'
    shapes = []
    grid = int(n ** 0.5) + 1; cel = T / grid
    for i in range(n):
        row = i // grid; col = i % grid
        cx = col * cel + rng.uniform(cel * 0.1, cel * 0.9)
        cy = row * cel + rng.uniform(cel * 0.1, cel * 0.9)
        r = rng.uniform(T * 0.06, T * 0.14)
        sides = rng.randint(4, 8)
        offsets = [rng.uniform(-25, 25) for _ in range(sides)]
        kleur = k[(i + 1) % len(k)]
        shapes.append((cx, cy, r, sides, offsets, kleur))
    for cx, cy, r, sides, offsets, kleur in shapes:
        for dx in [0, T, -T]:
            for dy in [0, T, -T]:
                nx, ny = cx + dx, cy + dy
                if -r < nx < T + r and -r < ny < T + r:
                    s.append(vorm(nx, ny, r, sides, offsets, kleur))
    return '\n'.join(s)

def generate_visgraat_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    bw = {'low': T // 8, 'medium': T // 12, 'high': T // 18}.get(complexity, T // 12)
    bh = bw * 2
    c1 = k[1]; bg = k[0]
    pw = bw * 2; ph = bw * 3
    s = ['<rect width="' + str(T) + '" height="' + str(T) + '" fill="' + bg + '"/>']
    cols = T // pw + 3
    rows = T // ph + 3
    for row in range(-1, rows):
        for col in range(-1, cols):
            x = col * pw
            y = row * ph
            s.append('<rect x="' + f'{x:.1f}' + '" y="' + f'{y:.1f}' + '" width="' + f'{bh:.1f}' + '" height="' + f'{bw:.1f}' + '" fill="' + c1 + '"/>')
            s.append('<rect x="' + f'{x+bw:.1f}' + '" y="' + f'{y+bw:.1f}' + '" width="' + f'{bw:.1f}' + '" height="' + f'{bh:.1f}' + '" fill="' + c1 + '"/>')
    return '\n'.join(s)

def generate_visgraat_svg2(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    u = {'low': T // 10, 'medium': T // 14, 'high': T // 20}.get(complexity, T // 14)
    c1 = k[1]; bg = k[0]
    s = ['<rect width="' + str(T) + '" height="' + str(T) + '" fill="' + bg + '"/>']
    for row in range(-1, T // u + 4):
        for col in range(-1, T // u + 4):
            x = col * u * 2
            y = row * u * 4
            if (col % 2 == 0):
                s.append('<rect x="' + f'{x:.0f}' + '" y="' + f'{y:.0f}' + '" width="' + f'{u*2:.0f}' + '" height="' + f'{u:.0f}' + '" fill="' + c1 + '"/>')
                s.append('<rect x="' + f'{x+u:.0f}' + '" y="' + f'{y+u:.0f}' + '" width="' + f'{u:.0f}' + '" height="' + f'{u*2:.0f}' + '" fill="' + c1 + '"/>')
                s.append('<rect x="' + f'{x:.0f}' + '" y="' + f'{y+u*2:.0f}' + '" width="' + f'{u*2:.0f}' + '" height="' + f'{u:.0f}' + '" fill="' + c1 + '"/>')
                s.append('<rect x="' + f'{x:.0f}' + '" y="' + f'{y+u*3:.0f}' + '" width="' + f'{u:.0f}' + '" height="' + f'{u*2:.0f}' + '" fill="' + c1 + '"/>')
    return '\n'.join(s)

def generate_visgraat_svg5(palette, tile_size, complexity):
    import math
    T = tile_size; k = _palet(palette)
    res = 200
    L = T / {'low': 5, 'medium': 8, 'high': 12}.get(complexity, 8)
    cell = T / res
    c1 = k[1]; c2 = k[2]
    s = ['<rect width="' + str(T) + '" height="' + str(T) + '" fill="' + k[0] + '"/>']
    for row in range(res):
        for col in range(res):
            x = col * cell + cell/2
            y = row * cell + cell/2
            H = math.floor((x + y) / L)
            V = math.floor((x - y) / L)
            kleur = c1 if (H + V) % 2 == 0 else c2
            s.append('<rect x="' + f'{col*cell:.2f}' + '" y="' + f'{row*cell:.2f}' + '" width="' + f'{cell:.2f}' + '" height="' + f'{cell:.2f}' + '" fill="' + kleur + '"/>')
    return '\n'.join(s)

def generate_visgraat_svg6(palette, tile_size, complexity):
    import math
    T = tile_size; k = _palet(palette)
    u = {'low': T//8, 'medium': T//12, 'high': T//16}.get(complexity, T//12)
    c1 = k[1]; c2 = k[0]
    # Herringbone: 4 parallelogrammen per pattern-eenheid
    # Eenheid is 2u x 2u, rotatie 45 graden
    pw = u * 4; ph = u * 4
    def plank(x1,y1, x2,y2, x3,y3, x4,y4, kleur):
        return '<polygon points="' + f'{x1},{y1} {x2},{y2} {x3},{y3} {x4},{y4}' + '" fill="' + kleur + '"/>'
    s = ['<defs>']
    s.append('  <pattern id="hb" x="0" y="0" width="' + str(pw) + '" height="' + str(ph) + '" patternUnits="userSpaceOnUse">')
    s.append('    <rect width="' + str(pw) + '" height="' + str(ph) + '" fill="' + c2 + '"/>')
    # Plank 1: diagonaal linksonder-rechtsboven
    s.append('    ' + plank(0,u, u,0, u*3,0, u*2,u, c1))
    # Plank 2: haaks erop
    s.append('    ' + plank(u*2,u, u*3,0, u*3,u*2, u*2,u*3, c1))
    # Plank 3: verschoven
    s.append('    ' + plank(0,u*3, u,u*2, u*3,u*2, u*2,u*3, c1))
    # Plank 4
    s.append('    ' + plank(0,u, 0,u*3, u,u*4, u,u*2, c1))
    s.append('  </pattern>')
    s.append('</defs>')
    s.append('<rect width="' + str(T) + '" height="' + str(T) + '" fill="url(#hb)"/>')
    return '\n'.join(s)
