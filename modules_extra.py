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
    T=tile_size; k=_palet(palette); n={'low':3,'medium':4,'high':6}.get(complexity,4); b=T/n
    s=[]
    for i in range(n+1): s.append(f'<rect x="{i*b:.1f}" y="0" width="{b:.1f}" height="{T}" fill="{k[i%len(k)]}"/>')
    return '\n'.join(s)

def generate_mozaiek_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    n = {'low': 4, 'medium': 7, 'high': 11}.get(complexity, 7)
    b = T / n
    gap = max(1, int(b * 0.06))
    rng = random.Random(42)
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    for row in range(n):
        y = row * b
        for col in range(n):
            x = col * b
            kleur = k[rng.randint(1, len(k)-1)]
            s.append(f'<rect x="{x+gap:.1f}" y="{y+gap:.1f}" width="{b-gap*2:.1f}" height="{b-gap*2:.1f}" fill="{kleur}"/>')
    return chr(10).join(s)
def generate_chevron_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    n = {'low': 3, 'medium': 5, 'high': 8}.get(complexity, 5)
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
    """Naadloze visschub/dakpan-tessellatie. Elke schub is een gesloten vorm:
    bovenaan een ronde koepel, onderaan begrensd door de cirkels van de twee
    schubben eronder (holle gebogen zijkanten, geen rechte zijkanten, geen
    losse cirkels). De vorm is rond van verhouding en sluit perfect in elkaar.
    Lagere rijen worden later getekend en vallen vooraan. Horizontaal naadloos:
    schubbreedte deelt de tegel exact. Verticaal naadloos: rijhoogte = halve
    schubbreedte en het aantal rijen (2x kolommen, even) is een veelvoud van
    het aantal kleuren."""
    T = float(tile_size)
    k = _palet(palette)
    cols = {'low': 4, 'medium': 6, 'high': 8}.get(complexity, 6)
    sw = T / cols
    R = sw / 2.0
    rh = R
    rows = 2 * cols
    n_colors = max(1, len(k) - 1)
    s = ['<rect width="{:.1f}" height="{:.1f}" fill="{}"/>'.format(T, T, k[0])]

    def schub(cx, cy, kleur):
        # koepel omhoog (eigen cirkel), dan rechter- en linker-scoop langs de
        # cirkels van de twee schubben eronder; eindigt in punt (cx, cy+R)
        d = ('M {:.2f} {:.2f} '
             'A {:.2f} {:.2f} 0 0 1 {:.2f} {:.2f} '
             'A {:.2f} {:.2f} 0 0 0 {:.2f} {:.2f} '
             'A {:.2f} {:.2f} 0 0 0 {:.2f} {:.2f} '
             'Z').format(
            cx - R, cy,
            R, R, cx + R, cy,
            R, R, cx, cy + R,
            R, R, cx - R, cy)
        return '<path d="{}" fill="{}"/>'.format(d, kleur)

    for row in range(-2, rows + 3):
        kleur = k[1 + (row % n_colors)]
        cy = row * rh
        ox = (sw / 2.0) if (row % 2) else 0.0
        for col in range(-2, cols + 3):
            cx = col * sw + ox
            s.append(schub(cx, cy, kleur))
    return chr(10).join(s)
def generate_diamant_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    nc = {'low': 2, 'medium': 3, 'high': 4}.get(complexity, 3)
    # nl = aantal geneste ringen per diamant (fijn, strak concentrisch)
    nl = {'low': 9, 'medium': 13, 'high': 18}.get(complexity, 13)
    tw = T / nc
    # EVEN aantal rijen dat T exact opdeelt -> verticaal naadloos (half-drop wrapt)
    rows = max(2, round(nc / 1.3))
    if rows % 2 == 1:
        rows += 1
    th = T / rows
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    def draw_diamond(cx, cy):
        # van buiten naar binnen: gelijkmatig geneste ringen, strak gecentreerd
        for i in range(nl, 0, -1):
            sc = i / nl
            w2 = (tw / 2 - 2) * sc
            h2 = (th / 2 - 2) * sc
            kleur = k[1 + ((nl - i) % (len(k) - 1))]
            pts = f'{cx:.1f},{cy-h2:.1f} {cx+w2:.1f},{cy:.1f} {cx:.1f},{cy+h2:.1f} {cx-w2:.1f},{cy:.1f}'
            s.append(f'<polygon points="{pts}" fill="none" stroke="{kleur}" stroke-width="1.4"/>')
        # klein gevuld hart in het midden voor strakke focus
        cw = (tw / 2 - 2) / nl; ch = (th / 2 - 2) / nl
        hart = f'{cx:.1f},{cy-ch:.1f} {cx+cw:.1f},{cy:.1f} {cx:.1f},{cy+ch:.1f} {cx-cw:.1f},{cy:.1f}'
        s.append(f'<polygon points="{hart}" fill="{k[1]}"/>')
    for row in range(-1, rows + 2):
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
    return '\n'.join(s)


def generate_visgraat_svg(palette, tile_size, complexity):
    """Klassiek visgraat/herringbone patroon met afwisselend H en V blokken."""
    T = tile_size; k = _palet(palette)
    # Blok: breedte bw, hoogte bh = bw*2 (klassieke 1:2 verhouding)
    bw = {'low': T // 8, 'medium': T // 12, 'high': T // 18}.get(complexity, T // 12)
    bh = bw * 2
    c1 = k[1]
    c2 = k[0]
    s = [f'<rect width="{T}" height="{T}" fill="{c2}"/>']
    # Patroon-eenheid: 2*bw breed, 2*bh hoog
    # Bevat 4 blokken die het V-motief vormen:
    # [H][H]   rij 0: twee horizontale blokken naast elkaar
    # [V][V]   rij 1: twee verticale blokken naast elkaar, verschoven
    pw = bw * 2
    ph = bh + bw  # hoogte van de patroon-eenheid
    cols = T // pw + 3
    rows = T // ph + 3
    for row in range(-1, rows):
        for col in range(-1, cols):
            x0 = col * pw
            y0 = row * ph
            # Bovenste deel: 2 horizontale blokken (bh breed, bw hoog)
            # Blok 1 links
            s.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{bh:.1f}" height="{bw:.1f}" fill="{c1}"/>')
            # Blok 2 rechts (aansluitend)
            # Onderste deel: 2 verticale blokken (bw breed, bh hoog), verschoven met bw
            s.append(f'<rect x="{x0+bw:.1f}" y="{y0+bw:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{c1}"/>')
            s.append(f'<rect x="{x0-bw:.1f}" y="{y0+bw:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{c1}"/>')
    return "\n".join(s)

def generate_dots_svg(palette, tile_size, complexity):
    T = tile_size; k = _palet(palette)
    n = {'low': 4, 'medium': 6, 'high': 9}.get(complexity, 6)
    step = T / n
    r = step * 0.35
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    for row in range(n + 1):
        for col in range(n + 1):
            cx = col * step
            cy = row * step
            if row % 2 == 1:
                cx += step / 2
            kleur = k[1 + ((row + col) % (len(k) - 1))]
            s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{kleur}"/>')
    return "\n".join(s)
def generate_visgraat_lijn_svg(palette, tile_size, complexity):
    """Naadloos 45-graden parket van dikke plankjes in geweven verband.
    De diagonale periode deelt de tegel exact op, dus het patroon sluit
    naadloos aan zonder afgekapte vormen."""
    T = tile_size
    k = _palet(palette)
    niv = {"low": 1, "medium": 2, "high": 3}.get(complexity, 2)
    u = T / (4.0 * math.sqrt(2) * niv)   # korte zijde van een plankje
    blk = 2.0 * u                         # blokmaat
    gap = max(1.0, u * 0.10)              # smalle voeg tussen plankjes
    c = math.cos(math.pi / 4); s = math.sin(math.pi / 4)
    def scr(a, b):
        return (a * c - b * s, a * s + b * c)
    def plank(a0, b0, la, lb, kleur):
        a1 = a0 + gap / 2; b1 = b0 + gap / 2
        a2 = a0 + la - gap / 2; b2 = b0 + lb - gap / 2
        hoeken = [scr(a1, b1), scr(a2, b1), scr(a2, b2), scr(a1, b2)]
        ps = " ".join("{:.2f},{:.2f}".format(x, y) for x, y in hoeken)
        return '<polygon points="{}" fill="{}"/>'.format(ps, kleur)
    out = ['<rect width="{}" height="{}" fill="{}"/>'.format(T, T, k[0])]
    amin = -blk * 2; amax = T * 1.5 + blk * 2
    bmin = -(T * 0.9) - blk * 2; bmax = (T * 0.9) + blk * 2
    I0 = int(math.floor(amin / blk)); I1 = int(math.ceil(amax / blk))
    J0 = int(math.floor(bmin / blk)); J1 = int(math.ceil(bmax / blk))
    for J in range(J0, J1 + 1):
        for I in range(I0, I1 + 1):
            a0 = I * blk; b0 = J * blk
            if (I + J) % 2 == 0:
                out.append(plank(a0, b0, blk, u, k[1]))
                out.append(plank(a0, b0 + u, blk, u, k[2]))
            else:
                out.append(plank(a0, b0, u, blk, k[1]))
                out.append(plank(a0 + u, b0, u, blk, k[2]))
    return "\n".join(out)


def generate_bamboe_svg(palette, tile_size, complexity):
    """Verticale bamboestokken, naadloos in beide richtingen.
    De stok-afstand deelt de tegel exact (horizontaal naadloos) en de
    knopen worden met wrap-kopieen getekend (verticaal naadloos),
    om-en-om verspringend voor een natuurlijke look. De kleuren volgen
    het gekozen palet: elke stok krijgt donkere randen en een lichte
    highlight, afgeleid van de primaire kleur, voor een ronde buisvorm."""
    T = float(tile_size)
    k = _palet(palette)
    bg = k[0]
    basis = k[1]
    licht = _lerp(basis, '#ffffff', 0.42)
    donker = _lerp(basis, '#000000', 0.38)
    knoop_kleur = _lerp(basis, '#000000', 0.52)
    knoop_licht = _lerp(basis, '#ffffff', 0.20)
    aantal = {'low': 3, 'medium': 4, 'high': 6}.get(complexity, 4)
    n_knopen = {'low': 3, 'medium': 4, 'high': 5}.get(complexity, 4)
    pitch = T / aantal
    stok_b = pitch * 0.60
    strips = 11
    sw = stok_b / strips
    sp = T / n_knopen
    knoop_h = max(4.0, T * 0.022)
    nh = knoop_h / 2.0
    out = ['<rect width="{:.1f}" height="{:.1f}" fill="{}"/>'.format(T, T, bg)]
    def teken_knoop(cx, cy):
        x = cx - stok_b / 2.0 - stok_b * 0.06
        w = stok_b + stok_b * 0.12
        out.append('<rect x="{:.2f}" y="{:.2f}" width="{:.2f}" height="{:.2f}" fill="{}"/>'.format(x, cy - nh, w, knoop_h, knoop_kleur))
        out.append('<rect x="{:.2f}" y="{:.2f}" width="{:.2f}" height="{:.2f}" fill="{}"/>'.format(x, cy - nh - knoop_h * 0.22, w, knoop_h * 0.22, knoop_licht))
    for i in range(aantal):
        cx = i * pitch + pitch / 2.0
        for s_i in range(strips):
            t = (s_i + 0.5) / strips
            schaduw = min(abs(t - 0.40) / 0.60, 1.0)
            kleur = _lerp(licht, donker, schaduw)
            x = cx - stok_b / 2.0 + s_i * sw
            out.append('<rect x="{:.2f}" y="-1.0" width="{:.2f}" height="{:.1f}" fill="{}"/>'.format(x, sw + 0.6, T + 2.0, kleur))
        offset = sp * 0.25 + (sp * 0.5 if i % 2 else 0.0)
        for j in range(n_knopen):
            cy = offset + j * sp
            for dy in (0.0, T, -T):
                y = cy + dy
                if -nh - knoop_h < y < T + nh + knoop_h:
                    teken_knoop(cx, y)
    return "\n".join(out)


def generate_artdeco_svg(palette, tile_size, complexity):
    """Art Deco zonnestraal-rozetten in een raster met dubbele-lijn trellis en
    kleine stralenbursts op de kruispunten. Naadloos: alles is periodiek met de
    celmaat en de rozetten blijven binnen hun cel. Kleuren volgen het palet
    (primair = stralen, accent = afwisseling, secundair = trellis-lijnen)."""
    T = float(tile_size)
    k = _palet(palette)
    bg = k[0]
    goud = k[1]
    goud2 = k[3] if len(k) > 3 else k[1]
    lijn = k[2] if len(k) > 2 else k[1]
    cols = {'low': 2, 'medium': 3, 'high': 4}.get(complexity, 3)
    cell = T / cols
    mid = cell / 2.0
    ro = cell * 0.40
    ri = cell * 0.085
    N = {'low': 20, 'medium': 24, 'high': 28}.get(complexity, 24)
    s = ['<rect width="{:.1f}" height="{:.1f}" fill="{}"/>'.format(T, T, bg)]

    def rozet(cx, cy, ro, ri, N, c1, c2, centrum):
        ho = (math.pi / N) * 0.78
        hi = ho * 0.22
        for j in range(N):
            a = j * 2.0 * math.pi / N
            x1 = cx + ri * math.cos(a - hi); y1 = cy + ri * math.sin(a - hi)
            x2 = cx + ro * math.cos(a - ho); y2 = cy + ro * math.sin(a - ho)
            x3 = cx + ro * math.cos(a + ho); y3 = cy + ro * math.sin(a + ho)
            x4 = cx + ri * math.cos(a + hi); y4 = cy + ri * math.sin(a + hi)
            kleur = c1 if j % 2 == 0 else c2
            pts = '{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}'.format(x1, y1, x2, y2, x3, y3, x4, y4)
            s.append('<polygon points="{}" fill="{}"/>'.format(pts, kleur))
        if centrum:
            s.append('<circle cx="{:.1f}" cy="{:.1f}" r="{:.1f}" fill="{}"/>'.format(cx, cy, ri * 1.15, bg))
            s.append('<circle cx="{:.1f}" cy="{:.1f}" r="{:.1f}" fill="{}"/>'.format(cx, cy, ri * 0.5, c1))

    lw = max(1.2, cell * 0.016)
    gap = cell * 0.045
    for c in range(0, cols + 1):
        xx = c * cell
        s.append('<rect x="{:.2f}" y="0" width="{:.2f}" height="{:.1f}" fill="{}"/>'.format(xx - gap - lw, lw, T, lijn))
        s.append('<rect x="{:.2f}" y="0" width="{:.2f}" height="{:.1f}" fill="{}"/>'.format(xx + gap, lw, T, lijn))
        yy = c * cell
        s.append('<rect x="0" y="{:.2f}" width="{:.1f}" height="{:.2f}" fill="{}"/>'.format(yy - gap - lw, T, lw, lijn))
        s.append('<rect x="0" y="{:.2f}" width="{:.1f}" height="{:.2f}" fill="{}"/>'.format(yy + gap, T, lw, lijn))
    for rr in range(cols):
        for cc in range(cols):
            rozet(cc * cell + mid, rr * cell + mid, ro, ri, N, goud, goud2, True)
    for rr in range(0, cols + 1):
        for cc in range(0, cols + 1):
            rozet(cc * cell, rr * cell, cell * 0.13, cell * 0.028, 12, goud, goud2, False)
    return chr(10).join(s)


def generate_artdeco_hex_svg(palette, tile_size, complexity):
    """Art Deco honingraat: concentrische zeshoeken (rand-ring plus gevulde kern)
    in een verspringend raster. Naadloos: elke zeshoek blijft binnen zijn cel en
    de randmotieven worden met wrap-kopieen herhaald. Kleuren volgen het palet."""
    T = float(tile_size)
    k = _palet(palette)
    bg = k[0]
    c_rand = k[1]
    c_kern = k[1]
    cols = {'low': 2, 'medium': 4, 'high': 6}.get(complexity, 4)
    cs = T / cols
    R = cs * 0.49
    s = ['<rect width="{:.1f}" height="{:.1f}" fill="{}"/>'.format(T, T, bg)]
    def hexpts(cx, cy, rad):
        p = []
        for a in range(6):
            ang = math.radians(60 * a - 90)
            p.append('{:.2f},{:.2f}'.format(cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        return ' '.join(p)
    def motief(cx, cy):
        s.append('<polygon points="{}" fill="{}"/>'.format(hexpts(cx, cy, R), c_rand))
        s.append('<polygon points="{}" fill="{}"/>'.format(hexpts(cx, cy, R * 0.74), bg))
        s.append('<polygon points="{}" fill="{}"/>'.format(hexpts(cx, cy, R * 0.46), c_kern))
    for row in range(-1, cols + 2):
        for col in range(-1, cols + 2):
            cx = col * cs + (cs / 2.0 if row % 2 else 0.0)
            cy = row * cs
            motief(cx, cy)
    return chr(10).join(s)


def generate_chevron_bold_svg(palette, tile_size, complexity):
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
    return '\n'.join(s)


def generate_houndstooth_svg(palette, tile_size, complexity):
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
    return '\n'.join(parts)
