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
    b = T / n  # blokgrootte
    gap = max(1, int(b * 0.06))
    rng = random.Random(42)
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    # Vast raster: elke cel is b x b, kleur willekeurig per cel
    for row in range(n):
        y = row * b
        for col in range(n):
            x = col * b
            kleur = k[rng.randint(1, len(k)-1)]
            s.append(f'<rect x="{x+gap:.1f}" y="{y+gap:.1f}" width="{b-gap*2:.1f}" height="{b-gap*2:.1f}" fill="{kleur}"/>')
    return "\n".join(s)

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
    r = float(r)
    pw = math.sqrt(3) * r  # pattern breedte = 1 hex-kolom
    ph = 3.0 * r           # pattern hoogte = 2 hex-rijen
    # Hexagoon punten (pointy-top, gecentreerd op cx,cy)
    def hpoly(cx, cy, kleur, fill_kleur):
        pts = ["{:.3f},{:.3f}".format(
            cx + r * math.cos(math.radians(a * 60 + 30)),
            cy + r * math.sin(math.radians(a * 60 + 30)))
            for a in range(6)]
        pts_str = " ".join(pts)
        return '<polygon points="' + pts_str + '" fill="' + fill_kleur + '" stroke="' + kleur + '" stroke-width="1.5"/>'
    # 2 hexagonen per pattern-eenheid
    h1 = hpoly(pw / 2, r, k[0], k[1])         # rij 0, kolom 0.5
    h2a = hpoly(0, r * 2.5, k[0], k[2])        # rij 1, linkerrand
    h2b = hpoly(pw, r * 2.5, k[0], k[2])       # rij 1, rechterrand
    s = []
    s.append("<defs>")
    s.append('  <pattern id="hexpat" x="0" y="0" width="' + "{:.4f}".format(pw) + '" height="' + "{:.4f}".format(ph) + '" patternUnits="userSpaceOnUse">')
    s.append('    <rect width="' + "{:.4f}".format(pw) + '" height="' + "{:.4f}".format(ph) + '" fill="' + k[0] + '"/>')
    s.append("    " + h1)
    s.append("    " + h2a)
    s.append("    " + h2b)
    s.append("  </pattern>")
    s.append("</defs>")
    s.append('<rect width="' + str(T) + '" height="' + str(T) + '" fill="url(#hexpat)"/>')
    return "\n".join(s)

def generate_ogee_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    n = {'low': 3, 'medium': 5, 'high': 8}.get(complexity, 5)
    b = T / n; h = b * 0.8
    rs_raw = h * 0.62
    n_colors = len(k) - 1
    n_rows_raw = max(1, round(T / rs_raw))
    n_rows = round(n_rows_raw / n_colors) * n_colors
    if n_rows == 0: n_rows = n_colors
    rs = T / n_rows
    offset = h * 0.42
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    for row in range(n_rows + 2, -2, -1):
        kleur = k[1 + (row % n_colors)]
        y0 = row * rs - offset
        for col in range(-1, n + 2):
            x = col * b + (b / 2 if row % 2 else 0) - b
            cx = x + b / 2
            d = "M {:.1f} {:.1f} Q {:.1f} {:.1f} {:.1f} {:.1f} Q {:.1f} {:.1f} {:.1f} {:.1f} Q {:.1f} {:.1f} {:.1f} {:.1f} Z".format(
                x, y0+h, cx, y0-h*0.1, x+b, y0+h,
                x+b+b*0.15, y0+h+rs-h*0.12, cx, y0+h+rs-h*0.15,
                x-b*0.15, y0+h+rs-h*0.12, x, y0+h)
            s.append(f'<path d="{d}" fill="{kleur}" stroke="{k[0]}" stroke-width="0.5"/>')
    return "\n".join(s)

def generate_diamant_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    nc = {'low': 2, 'medium': 3, 'high': 4}.get(complexity, 3)
    nl = {'low': 5, 'medium': 8, 'high': 12}.get(complexity, 8)
    # Pas tw aan zodat T exact deelbaar is door tw
    tw = T / nc
    # th moet zo zijn dat T exact deelbaar is door th
    # en dat de offset-rijen (halve stap) ook kloppen
    # Voor half-drop: th * aantal_rijen = T, en aantal_rijen is even
    th_raw = tw * 1.3
    nr = max(2, round(T / th_raw))
    if nr % 2 != 0: nr += 1  # moet even zijn voor half-drop aansluiting
    th = T / nr
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    def draw_diamond(cx, cy):
        for i in range(nl, 0, -1):
            sc = i / nl
            w2 = (tw / 2 - 2) * sc
            h2 = (th / 2 - 2) * sc
            kleur = k[1 + ((nl - i) % (len(k) - 1))]
            pts = f'{cx:.1f},{cy-h2:.1f} {cx+w2:.1f},{cy:.1f} {cx:.1f},{cy+h2:.1f} {cx-w2:.1f},{cy:.1f}'
            s.append(f'<polygon points="{pts}" fill="none" stroke="{kleur}" stroke-width="1.2"/>')
    for row in range(-1, nr + 2):
        for col in range(-1, nc + 2):
            cx = col * tw + (tw / 2 if row % 2 else 0)
            cy = row * th + th / 2
            draw_diamond(cx, cy)
            # Wrap-around
            if cx - tw/2 < 0: draw_diamond(cx + T, cy)
            if cx + tw/2 > T: draw_diamond(cx - T, cy)
            if cy - th/2 < 0: draw_diamond(cx, cy + T)
            if cy + th/2 > T: draw_diamond(cx, cy - T)
    return "\n".join(s)

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
