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
    """Grafische visgraat/parket: effen planken in EEN paletkleur met een dunne
    lijn-voeg. Kleuren volgen het palet (plank=primair, voeg=achtergrond).
    Bereik afgeleid uit de inverse 45-rotatie + per-plank cull, zodat de tegel
    netjes gevuld is en de inhoud binnen ~[-blok, T+blok] blijft (geen overloop
    die de tegel-plakkerij verstoort). Constante voeg (~3 mm) via tile_cm.
    Naadloos, geen witte naden, geen clipPath."""
    import math as _m
    _VG_STYLE = "grafisch-v2"
    T = float(tile_size)
    k = _palet(palette)
    voeg = k[0]
    plank = k[1]
    tile_cm = 40
    if isinstance(palette, dict):
        try:
            tile_cm = int(palette.get("_tile_cm", 40))
        except (TypeError, ValueError):
            tile_cm = 40
    ratio = 4
    reps = {"low": 3, "medium": 2, "high": 4}.get(complexity, 2)
    u = T / (ratio * reps * _m.sqrt(2.0))
    w = u
    blk = ratio * u
    voeg_mm = 3.0
    gap = max(0.5, voeg_mm / (tile_cm / 40.0))
    c = _m.cos(_m.pi / 4.0); s = _m.sin(_m.pi / 4.0)
    def scr(a, b):
        return (a * c - b * s, a * s + b * c)
    corners = [(0.0, 0.0), (T, 0.0), (0.0, T), (T, T)]
    Avals = [(x + y) / _m.sqrt(2.0) for (x, y) in corners]
    Bvals = [(y - x) / _m.sqrt(2.0) for (x, y) in corners]
    amin = min(Avals) - blk; amax = max(Avals) + blk
    bmin = min(Bvals) - blk; bmax = max(Bvals) + blk
    I0 = int(_m.floor(amin / blk)); I1 = int(_m.ceil(amax / blk))
    J0 = int(_m.floor(bmin / blk)); J1 = int(_m.ceil(bmax / blk))
    margin = blk * 0.75
    out = ['<rect width="{:.0f}" height="{:.0f}" fill="{}"/>'.format(T, T, voeg)]
    def plank_draw(a0, b0, la, lb):
        a1 = a0 + gap / 2.0; b1 = b0 + gap / 2.0
        a2 = a0 + la - gap / 2.0; b2 = b0 + lb - gap / 2.0
        pts = [scr(a1, b1), scr(a2, b1), scr(a2, b2), scr(a1, b2)]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        if max(xs) < -margin or min(xs) > T + margin or max(ys) < -margin or min(ys) > T + margin:
            return
        ps = " ".join("{:.2f},{:.2f}".format(x, y) for x, y in pts)
        out.append('<polygon points="{}" fill="{}"/>'.format(ps, plank))
    for J in range(J0, J1 + 1):
        for I in range(I0, I1 + 1):
            a0 = I * blk; b0 = J * blk
            if (I + J) % 2 == 0:
                for mm in range(ratio):
                    plank_draw(a0, b0 + mm * w, blk, w)
            else:
                for mm in range(ratio):
                    plank_draw(a0 + mm * w, b0, w, blk)
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


def generate_urban_plaid_svg(palette, tile_size, complexity):
    """Urban Plaid (tartan/ruit): naadloos raster van horizontale en verticale
    banden met wisselende diktes; kruispunten mengen via opacity (geweven
    tartan-effect). Geen clipPath (Safari-proof).
    Kleur via _palet: k[0]=achtergrond, k[1]/k[2]=bandkleuren."""
    T = float(tile_size)
    k = _palet(palette)
    bg = k[0]; c1 = k[1]; c2 = k[2]
    # sett: (breedte-eenheden, kleur). 0 = achtergrond (geen band).
    sett = [
        (8, 0), (10, c1), (2, c1), (4, 0), (2, c1), (6, 0), (1, c1), (3, 0), (1, c1), (4, 0),
        (16, c1),
        (4, 0), (2, c1), (2, 0), (2, c1), (4, 0),
        (6, c2), (2, 0), (6, c2),
        (4, 0), (1, c1), (2, 0), (1, c1), (4, 0),
        (12, c1), (3, 0), (3, c1),
        (6, 0),
    ]
    tot = sum(w for w, _ in sett)
    scale = T / tot
    bands = []
    pos = 0.0
    for w, col in sett:
        ww = w * scale
        if col != 0:
            bands.append((pos, ww, col))
        pos += ww
    op = "0.55"
    parts = ['<rect width="%.1f" height="%.1f" fill="%s"/>' % (T, T, bg)]
    for x, w, col in bands:
        parts.append('<rect x="%.2f" y="0" width="%.2f" height="%.1f" fill="%s" opacity="%s"/>' % (x, w, T, col, op))
    for y, w, col in bands:
        parts.append('<rect x="0" y="%.2f" width="%.1f" height="%.2f" fill="%s" opacity="%s"/>' % (y, T, w, col, op))
    return '\n'.join(parts)


# ---- Hoogtelijnen (topografische contourlijnen) - naadloos ----
def _topo_segments(T, complexity):
    fmax = {'low':3.4,'medium':4.6,'high':6.2}.get(complexity,4.6)
    levn = {'low':11,'medium':14,'high':18}.get(complexity,14)
    G = 120
    rng = random.Random(7)
    comps=[]
    for _ in range(28):
        fr = rng.uniform(1.0,fmax); ang=rng.uniform(0,2*math.pi)
        u = round(fr*math.cos(ang)); v=round(fr*math.sin(ang))
        if u==0 and v==0: u=1
        comps.append((u,v,1.0/fr,rng.uniform(0,2*math.pi)))
    F=[[0.0]*(G+1) for _ in range(G+1)]
    mn=1e9; mx=-1e9
    for i in range(G+1):
        y=i/G
        for j in range(G+1):
            x=j/G; s=0.0
            for (u,vv,a,ph) in comps:
                s+=a*math.cos(2*math.pi*(u*x+vv*y)+ph)
            F[i][j]=s
            if s<mn:mn=s
            if s>mx:mx=s
    rg=mx-mn or 1.0
    for i in range(G+1):
        for j in range(G+1):
            F[i][j]=(F[i][j]-mn)/rg
    def ep(L,ax,ay,av,bx,by,bv):
        d=bv-av; t=0.5 if abs(d)<1e-12 else (L-av)/d
        return (ax+(bx-ax)*t, ay+(by-ay)*t)
    sc=T/G; segs=[]
    levels=[0.06+(0.94-0.06)*k/(levn-1) for k in range(levn)]
    for L in levels:
        for i in range(G):
            for j in range(G):
                a=F[i][j]>=L; b=F[i][j+1]>=L; c=F[i+1][j+1]>=L; d=F[i+1][j]>=L
                code=(a)|(b<<1)|(c<<2)|(d<<3)
                if code==0 or code==15: continue
                av=F[i][j]; bv=F[i][j+1]; cv=F[i+1][j+1]; dv=F[i+1][j]
                P={}
                if a!=b: P['T']=ep(L,j,i,av,j+1,i,bv)
                if b!=c: P['R']=ep(L,j+1,i,bv,j+1,i+1,cv)
                if c!=d: P['B']=ep(L,j+1,i+1,cv,j,i+1,dv)
                if d!=a: P['L']=ep(L,j,i+1,dv,j,i,av)
                e=list(P)
                if len(e)==2:
                    segs.append((P[e[0]],P[e[1]]))
                elif len(e)==4:
                    segs.append((P['T'],P['R'])); segs.append((P['B'],P['L']))
    return [((p[0]*sc,p[1]*sc),(q[0]*sc,q[1]*sc)) for (p,q) in segs]

def generate_hoogtelijnen_svg(palette, tile_size, complexity):
    T=tile_size; k=_palet(palette); line=k[1]; lw=max(1.0, T/230.0)
    segs=_topo_segments(T, complexity)
    d=''.join('M{:.1f} {:.1f}L{:.1f} {:.1f}'.format(p[0],p[1],q[0],q[1]) for (p,q) in segs)
    return ('<rect width="{T}" height="{T}" fill="{bg}"/>'
            '<path d="{d}" stroke="{line}" stroke-width="{lw:.2f}" fill="none" stroke-linecap="round"/>'
            ).format(T=T,bg=k[0],d=d,line=line,lw=lw)


# =====================================================================
#  PRISM OVERLAY  --  generator voor modules_extra.py
#  Naadloze cirkels-op-plaid met intelligente transparantie.
#  Geen clipPath (Safari/base64-veilig). seed=None => verrassing per klik.
#  Aangeroepen door build_tile_svg als: generator(palette, g, complexity)
# =====================================================================
import math
import random


def _po_pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def _po_quarter(cx, cy, r, a1, a2):
    """Eén kwart als taartpunt-pad (twee radii + 90deg-boog). Geen clipPath."""
    x1, y1 = _po_pt(cx, cy, r, a1)
    x2, y2 = _po_pt(cx, cy, r, a2)
    return ("M%.2f,%.2f L%.2f,%.2f A%.2f,%.2f 0 0,1 %.2f,%.2f Z"
            % (cx, cy, x1, y1, r, r, x2, y2))


def _po_band_widths(rng, total, min_w, max_w):
    """Bandbreedtes die samen exact 'total' zijn -> wrapt naadloos."""
    min_w = max(2, min_w)
    max_w = max(min_w + 1, max_w)
    widths, acc = [], 0
    while acc < total - max_w:
        w = rng.randint(min_w, max_w)
        widths.append(w)
        acc += w
    widths.append(total - acc)   # sluitstuk maakt de som precies = total
    return widths


def _po_colors(palette):
    """Haal een lijst hex-kleuren uit wat 'palette' ook is (dict of lijst)."""
    cols = []
    if isinstance(palette, dict):
        if isinstance(palette.get("colors"), (list, tuple)):
            cols = list(palette["colors"])
        else:
            for v in palette.values():
                if isinstance(v, str) and v.startswith("#"):
                    cols.append(v)
                elif isinstance(v, (list, tuple)):
                    cols.extend([x for x in v if isinstance(x, str) and x.startswith("#")])
    elif isinstance(palette, (list, tuple)):
        cols = list(palette)
    cols = [c for c in cols if isinstance(c, str) and c.startswith("#")]
    if not cols:
        cols = ["#9B5C8F", "#F2C94C", "#4E9D4E", "#C0532B", "#E1A93C"]
    return cols


def generate_prism_overlay_svg(palette, tile_size=600, complexity="medium",
                               shape_list=None, N=4, seed=None):
    """
    Prism Overlay -- raster van N x N exacte vierkante cellen.
    - Cirkels blijven BINNEN hun cel (r = 0.48*cel) => geen overhang => naadloos.
    - Plaid = half-doorzichtige verticale + horizontale banden over lichte basis.
    - Per cirkel een modus met eigen doorzichtigheid:
        solid massief / vivid 4 felle kwarten / glas plaid schijnt door / duo 2 kwarten
    seed=None => varieert per aanroep (verrassing per klik).
    """
    rng = random.Random(seed)
    T = int(tile_size)
    C = T / float(N)
    r = 0.48 * C

    base = "#F6ECD2"
    colors = _po_colors(palette)
    plaid_pool = colors[:3] if len(colors) >= 3 else list(colors)
    circle_pool = (colors[2:] if len(colors) > 2 else list(colors)) + ["#141414"]

    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
         % (T, T, T, T),
         '<rect width="%d" height="%d" fill="%s"/>' % (T, T, base)]

    # ---- plaid (naadloos) ----
    x = 0
    for w in _po_band_widths(rng, T, int(C * 0.35), int(C * 0.95)):
        col = rng.choice(plaid_pool)
        op = rng.choice([0.0, 0.0, 0.55, 0.7])
        if op:
            p.append('<rect x="%.1f" y="0" width="%.1f" height="%d" fill="%s" fill-opacity="%s"/>'
                     % (x, w, T, col, op))
        x += w
    y = 0
    for h in _po_band_widths(rng, T, int(C * 0.35), int(C * 0.95)):
        col = rng.choice(plaid_pool)
        op = rng.choice([0.0, 0.0, 0.5, 0.65])
        if op:
            p.append('<rect x="0" y="%.1f" width="%d" height="%.1f" fill="%s" fill-opacity="%s"/>'
                     % (y, T, h, col, op))
        y += h

    # ---- cirkels (binnen de cel) ----
    quarters = [(0, 90), (90, 180), (180, 270), (270, 360)]
    for j in range(N):
        for i in range(N):
            cx = (i + 0.5) * C
            cy = (j + 0.5) * C
            mode = rng.choices(["solid", "vivid", "glas", "duo"],
                               weights=[0.22, 0.34, 0.30, 0.14])[0]
            if mode == "solid":
                col = rng.choice(circle_pool)
                op = rng.uniform(0.78, 0.92)
                p.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" fill-opacity="%.2f"/>'
                         % (cx, cy, r, col, op))
            else:
                lo, hi = {"vivid": (0.62, 0.78), "glas": (0.32, 0.46),
                          "duo": (0.55, 0.70)}[mode]
                cols = [rng.choice(circle_pool) for _ in range(4)]
                if mode == "duo":
                    cols = [cols[0], cols[1], cols[0], cols[1]]
                for (a1, a2), col in zip(quarters, cols):
                    op = rng.uniform(lo, hi)
                    p.append('<path d="%s" fill="%s" fill-opacity="%.2f"/>'
                             % (_po_quarter(cx, cy, r, a1, a2), col, op))

    p.append("</svg>")
    return "\n".join(p)


# =====================================================================
#  LIJNENSPEL -- generator voor modules_extra.py
#  Verticale lijn-clusters + horizontale kleurzones op donkere ondergrond.
#  Naadveilig: alleen doorlopende verticale lijnen (gelijke clusterafstand,
#  binnen de tegel) en horizontale banden -> wrapt in beide richtingen.
#  Geen clipPath. seed=None => verrassing per klik.
#  Aangeroepen als: generator(palette, g, complexity)
# =====================================================================
import random


def _ls_colors(palette):
    cols = []
    if isinstance(palette, dict):
        if isinstance(palette.get("colors"), (list, tuple)):
            cols = list(palette["colors"])
        else:
            for v in palette.values():
                if isinstance(v, str) and v.startswith("#"):
                    cols.append(v)
                elif isinstance(v, (list, tuple)):
                    cols.extend([x for x in v if isinstance(x, str) and x.startswith("#")])
    elif isinstance(palette, (list, tuple)):
        cols = list(palette)
    cols = [c for c in cols if isinstance(c, str) and c.startswith("#")]
    if not cols:
        cols = ["#9DB4C8", "#EDE3CF", "#C8A98C", "#D8B49A", "#E8E6DC"]
    return cols


def generate_lijnenspel_svg(palette, tile_size=600, complexity="medium",
                            shape_list=None, seed=None):
    rng = random.Random(seed)
    T = int(tile_size)
    base = "#342B34"
    line_cols = _ls_colors(palette)

    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
         % (T, T, T, T),
         '<rect width="%d" height="%d" fill="%s"/>' % (T, T, base)]

    # ---- horizontale zones (kleurvlakken), exacte verdeling -> naadloos ----
    Z = rng.choice([4, 5])
    edges = [round(T * k / Z) for k in range(Z + 1)]
    tones = [(255, 255, 255, 0.04), (255, 255, 255, 0.09),
             (0, 0, 0, 0.07), (255, 255, 255, 0.025), (0, 0, 0, 0.04)]
    for z in range(Z):
        y0, y1 = edges[z], edges[z + 1]
        r0, g0, b0, op = rng.choice(tones)
        if op:
            p.append('<rect x="0" y="%d" width="%d" height="%d" fill="rgb(%d,%d,%d)" fill-opacity="%s"/>'
                     % (y0, T, y1 - y0, r0, g0, b0, op))
    zone_line = [rng.choice(line_cols) for _ in range(Z)]

    # ---- verticale clusters op GELIJKE afstand -> naadloos, geen randoverhang ----
    n_c = rng.choice([6, 7, 8, 9])
    spacing = T / float(n_c)
    for c in range(n_c):
        cx = c * spacing
        k = rng.choice([2, 3, 3, 4])
        wln = rng.choice([3, 4, 5])
        ig = rng.choice([6, 8, 10])
        cw = k * (wln + ig)
        if cw > spacing - 4:                       # cluster moet binnen zijn vak passen
            k = max(2, int((spacing - 4) / (wln + ig)))
        for li in range(k):
            lx = cx + li * (wln + ig)
            for z in range(Z):
                y0, y1 = edges[z], edges[z + 1]
                col = zone_line[z]
                # gloed: brede vage rand
                p.append('<rect x="%.1f" y="%d" width="%d" height="%d" fill="%s" fill-opacity="0.16"/>'
                         % (lx - 2, y0, wln + 4, y1 - y0, col))
                # kern
                op = rng.uniform(0.6, 0.9)
                p.append('<rect x="%.1f" y="%d" width="%d" height="%d" fill="%s" fill-opacity="%.2f"/>'
                         % (lx, y0, wln, y1 - y0, col, op))

    p.append("</svg>")
    return "\n".join(p)


# =====================================================================
#  JAPANDI v8 -- collectie met transparantie/overlap + variant Golven
#  Eén generator, meerdere natuur-geïnspireerde sub-stijlen. De gekozen
#  variant lift mee in de prompt als "variant: <naam>" en bereikt de
#  generator via palette["_jp_prompt"]. Geen API/app.js-wijziging nodig.
#  Gedeelde basis: achtergrond uit palette["background"], kleurverzachting
#  met contrast, naadloze wrap, geen clipPath. seed=None => verrassing.
#  Varianten: organic (terugval/standaard), river_stones, stroming,
#  organic_leaves. Uitbreidbaar in batches.
# =====================================================================
import math
import random
import re

_JP_VERSION = "v8"
_JP_CREME = "#EFE8DA"
_JP_FALLBACK = ["#8C9472", "#6E7A55", "#B6A98C", "#5C5A4A", "#A7A98E"]


def _jp_hx(h):
    h = h.lstrip("#")
    return tuple(int(h[k:k + 2], 16) for k in (0, 2, 4))


def _jp_th(t):
    return "#%02X%02X%02X" % (int(max(0, min(255, t[0]))),
                              int(max(0, min(255, t[1]))),
                              int(max(0, min(255, t[2]))))


def _jp_is_hex(s):
    if not isinstance(s, str):
        return False
    s = s.strip()
    if len(s) != 7 or not s.startswith("#"):
        return False
    try:
        int(s[1:], 16); return True
    except ValueError:
        return False


def _jp_bg(palette):
    if isinstance(palette, dict):
        b = palette.get("background")
        if _jp_is_hex(b):
            return b
    return _JP_CREME


def _jp_lum(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def _jp_soften_toward(hexc, bg_rgb, desat=0.30):
    r, g, b = _jp_hx(hexc)
    l = 0.299 * r + 0.587 * g + 0.114 * b
    r = r + (l - r) * desat; g = g + (l - g) * desat; b = b + (l - b) * desat
    if _jp_lum(bg_rgb) < 128:
        light = 0.16 + 0.28 * (1.0 - l / 255.0); tgt = (236, 232, 222)
    else:
        light = 0.10 + 0.26 * (1.0 - l / 255.0); tgt = bg_rgb
    r = r + (tgt[0] - r) * light; g = g + (tgt[1] - g) * light; b = b + (tgt[2] - b) * light
    return _jp_th((r, g, b))


def _jp_lerp_hex(hexc, b_rgb, t):
    a = _jp_hx(hexc)
    return _jp_th((a[0] + (b_rgb[0] - a[0]) * t,
                   a[1] + (b_rgb[1] - a[1]) * t,
                   a[2] + (b_rgb[2] - a[2]) * t))


def _jp_colors(palette, exclude_hex):
    cols = []
    if isinstance(palette, dict):
        if isinstance(palette.get("colors"), (list, tuple)):
            cols = list(palette["colors"])
        else:
            for key, v in palette.items():
                if key in ("background", "_jp_prompt"):
                    continue
                if isinstance(v, str) and v.startswith("#"):
                    cols.append(v)
                elif isinstance(v, (list, tuple)):
                    cols.extend([x for x in v if isinstance(x, str) and x.startswith("#")])
    elif isinstance(palette, (list, tuple)):
        cols = list(palette)
    ex = (exclude_hex or "").lower()
    cols = [c for c in cols if isinstance(c, str) and c.startswith("#") and c.lower() != ex]
    return cols or list(_JP_FALLBACK)


def _jp_points(rng, T, rmin, cap=400):
    pts = []; tries = 0
    while tries < cap * 40 and len(pts) < cap:
        tries += 1
        p = (rng.uniform(0, T), rng.uniform(0, T)); ok = True
        for q in pts:
            dx = min(abs(p[0] - q[0]), T - abs(p[0] - q[0]))
            dy = min(abs(p[1] - q[1]), T - abs(p[1] - q[1]))
            if dx * dx + dy * dy < rmin * rmin:
                ok = False; break
        if ok:
            pts.append(p)
    return pts


def _jp_wrap(T, cx, cy, reach):
    res = []
    for dx in (-T, 0, T):
        for dy in (-T, 0, T):
            x, y = cx + dx, cy + dy
            if -reach - 2 <= x <= T + reach + 2 and -reach - 2 <= y <= T + reach + 2:
                res.append((x, y))
    return res


def _jp_leaf_path(cx, cy, L, W, ang, seg=28):
    yc = ((W / 2.0) ** 2 - (L / 2.0) ** 2) / W
    def arc(sgn):
        c = (0.0, yc * sgn); r = abs(W / 2.0 - yc)
        P1 = (-L / 2.0, 0.0); P2 = (L / 2.0, 0.0)
        a1 = math.atan2(P1[1] - c[1], P1[0] - c[0])
        a2 = math.atan2(P2[1] - c[1], P2[0] - c[0])
        return [(c[0] + r * math.cos(a1 + (a2 - a1) * k / seg),
                 c[1] + r * math.sin(a1 + (a2 - a1) * k / seg)) for k in range(seg + 1)]
    poly = arc(1) + arc(-1)[::-1]
    ca, sa = math.cos(ang), math.sin(ang)
    pts = ["%.2f,%.2f" % (cx + x * ca - y * sa, cy + x * sa + y * ca) for (x, y) in poly]
    return '<path d="M' + " L".join(pts) + ' Z"'


def _jp_variant_from(palette):
    pr = ""
    if isinstance(palette, dict):
        pr = palette.get("_jp_prompt", "") or ""
    m = re.search(r"variant:\s*([a-z_]+)", pr.lower())
    return m.group(1) if m else "organic"


# ---------------- sub-variant: organic (terugval, v6-look) ----------------
def _jp_sub_organic(rng, T, soft, bg_rgb, out):
    items = []
    for (cx, cy) in _jp_points(rng, T, T * 0.42)[:rng.choice([3, 3, 4])]:
        size = T * rng.uniform(0.20, 0.30)
        kind = "leaf" if rng.random() < 0.70 else "circle"
        items.append((size, cx, cy, kind, rng.choice(soft), rng.uniform(0, math.pi)))
    for (cx, cy) in _jp_points(rng, T, T * 0.20, cap=22):
        size = T * rng.uniform(0.04, 0.12)
        kind = "leaf" if rng.random() < 0.66 else "circle"
        items.append((size, cx, cy, kind, rng.choice(soft), rng.uniform(0, math.pi)))
    items.sort(key=lambda it: it[0], reverse=True)
    for (size, cx, cy, kind, col, ang) in items:
        if kind == "leaf":
            L = size * 2.0; W = size * 1.15
            for (x, y) in _jp_wrap(T, cx, cy, size * 1.15):
                out.append(_jp_leaf_path(x, y, L, W, ang) + ' fill="%s"/>' % col)
        else:
            for (x, y) in _jp_wrap(T, cx, cy, size):
                out.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (x, y, size, col))


# ---------------- sub-variant: river_stones (transparant, klein+groot) -------
def _jp_stone_harm(rng):
    return [(k, rng.uniform(0.03, 0.10), rng.uniform(0, 6.28)) for k in (2, 3, 4, 5)]


def _jp_sub_river_stones(rng, T, soft, bg_rgb, out):
    layers = []
    for (cx, cy) in _jp_points(rng, T, T * 0.30):
        layers.append((T * rng.uniform(0.17, 0.25), cx, cy))
    for (cx, cy) in _jp_points(rng, T, T * 0.20, cap=10):
        layers.append((T * rng.uniform(0.10, 0.15), cx, cy))
    for (cx, cy) in _jp_points(rng, T, T * 0.13, cap=16):
        layers.append((T * rng.uniform(0.055, 0.095), cx, cy))
    rng.shuffle(layers)
    n = 48
    for (r, cx, cy) in layers:
        col = rng.choice(soft); harm = _jp_stone_harm(rng); ang0 = rng.uniform(0, 6.28)
        for (x, y) in _jp_wrap(T, cx, cy, r * 1.35):
            pts = []
            for k in range(n):
                th = 2 * math.pi * k / n
                rad = r * (1 + sum(a * math.sin(kk * th + ph) for (kk, a, ph) in harm))
                pts.append("%.2f,%.2f" % (x + rad * math.cos(th + ang0), y + rad * math.sin(th + ang0)))
            out.append('<path d="M' + " L".join(pts) + ' Z" fill="%s" fill-opacity="0.45"/>' % col)


# ---------------- sub-variant: stroming (geveegd zand, fijne lijnen) ---------
def _jp_sub_stroming(rng, T, soft, bg_rgb, out):
    line = _jp_lerp_hex(rng.choice(soft), bg_rgb, 0.30)
    terms = [(rng.randint(1, 2), rng.randint(0, 1), rng.uniform(0, 6.28),
              rng.uniform(0.04, 0.08) * T) for _ in range(3)]
    def off(x, y):
        return sum(A * math.sin(2 * math.pi * fx * x / T + 2 * math.pi * fy * y / T + ph)
                   for (fx, fy, ph, A) in terms)
    nlines = 22; sp = T / float(nlines); step = T / 140.0
    ampmax = sum(A for (_fx, _fy, _ph, A) in terms)
    pad = int(math.ceil(ampmax / sp)) + 2
    for i in range(-pad, nlines + pad + 1):
        base = i * sp; pts = []; x = 0.0
        while x <= T + 0.1:
            pts.append("%.2f,%.2f" % (x, base + off(x, base))); x += step
        out.append('<path d="M' + " L".join(pts) + '" fill="none" stroke="%s" stroke-width="3"/>' % line)


# ---------------- sub-variant: golven (kleurrijke golvende banden) -----------
def _jp_sub_golven(rng, T, soft, bg_rgb, out):
    nb = rng.randint(14, 20); bh = T / float(nb)
    waves = [(rng.randint(1, 3), rng.uniform(0, 6.28), rng.uniform(0.04, 0.09) * T) for _ in range(3)]
    band_cols = [_jp_lerp_hex(rng.choice(soft), bg_rgb, rng.uniform(0.0, 0.5)) for _ in range(nb)]
    def off(x):
        return sum(A * math.sin(2 * math.pi * f * x / T + ph) for (f, ph, A) in waves)
    ampmax = sum(A for (_f, _p, A) in waves)
    pad = int(math.ceil(ampmax / bh)) + 2     # marge schaalt mee met golfhoogte
    overlap = 1.0                              # mini-overlap tegen AA-spleetjes
    step = T / 120.0
    for j in range(-pad, nb + pad):
        base = j * bh; col = band_cols[j % nb]; top = []; bot = []; x = 0.0
        while x <= T + 0.1:
            o = off(x)
            top.append("%.2f,%.2f" % (x, base + o)); bot.append("%.2f,%.2f" % (x, base + bh + o + overlap)); x += step
        out.append('<path d="M' + " L".join(top + bot[::-1]) + ' Z" fill="%s"/>' % col)


# ---------------- sub-variant: organic_leaves (transparant, overlap, takken) -
def _jp_sub_organic_leaves(rng, T, soft, bg_rgb, out):
    tw = _jp_lerp_hex(rng.choice(soft), (74, 70, 54), 0.55)
    data = []
    for (cx, cy) in _jp_points(rng, T, T * 0.30):
        L = T * rng.uniform(0.34, 0.52); W = L * rng.uniform(0.5, 0.62)
        ang = rng.uniform(0, math.pi); col = rng.choice(soft)
        data.append((cx, cy, L, W, ang, col))
    for (cx, cy, L, W, ang, col) in data:
        ca, sa = math.cos(ang), math.sin(ang)
        for (x, y) in _jp_wrap(T, cx, cy, L * 1.1):
            out.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="2" stroke-opacity="0.6"/>'
                       % (x - L * 1.05 * ca, y - L * 1.05 * sa, x + L * 0.7 * ca, y + L * 0.7 * sa, tw))
    for (cx, cy, L, W, ang, col) in data:
        for (x, y) in _jp_wrap(T, cx, cy, L / 2 * 1.1):
            out.append(_jp_leaf_path(x, y, L, W, ang) + ' fill="%s" fill-opacity="0.55"/>' % col)


_JP_VARIANTS = {
    "organic": _jp_sub_organic,
    "river_stones": _jp_sub_river_stones,
    "stroming": _jp_sub_stroming,
    "organic_leaves": _jp_sub_organic_leaves,
    "golven": _jp_sub_golven,
}


def generate_japandi_svg(palette, tile_size=600, complexity="medium",
                         shape_list=None, seed=None):
    rng = random.Random(seed)
    T = int(tile_size)
    bg = _jp_bg(palette)
    bg_rgb = _jp_hx(bg)
    soft = [_jp_soften_toward(c, bg_rgb) for c in _jp_colors(palette, bg)]
    variant = _jp_variant_from(palette)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
           % (T, T, T, T),
           '<rect width="%d" height="%d" fill="%s"/>' % (T, T, bg)]
    fn = _JP_VARIANTS.get(variant, _jp_sub_organic)
    fn(rng, T, soft, bg_rgb, out)
    out.append("</svg>")
    return "\n".join(out)


# =====================================================================
#  AARDLAGEN -- generator voor modules_extra.py (pure Python)
#  Dichte, geplooide contour-/aderlijnen (marching squares) die aardlagen /
#  agaat / natuursteen suggereren. Naadloos (periodiek veld, gehele
#  frequenties). Lijndikte CONSTANT ~3 mm via tile_cm. Kleuren volledig uit
#  het palet: achtergrond = ondergrond, primair = hoofd-lijnen, secondary/
#  accent1/accent2 = accent-aders. Geen clipPath. seed=None => verrassing.
# =====================================================================
def _al_field_fn(seed):
    import math as _m, random as _r
    rng = _r.Random(seed)
    base = [(rng.randint(1, 3), rng.randint(1, 3), rng.uniform(0, 6.28), 1.0 / (1 + rng.randint(1, 4))) for _ in range(5)]
    wx = [(rng.randint(1, 2), rng.randint(1, 2), rng.uniform(0, 6.28), 1.0 / (1 + rng.randint(1, 3))) for _ in range(3)]
    wy = [(rng.randint(1, 2), rng.randint(1, 2), rng.uniform(0, 6.28), 1.0 / (1 + rng.randint(1, 3))) for _ in range(3)]
    warp = 0.9
    def noise(x, y, terms):
        s = 0.0
        for (fx, fy, ph, a) in terms:
            s += a * _m.sin(fx * x + fy * y + ph)
        return s
    def H(u, v):
        ox = warp * noise(u + 0.0, v + 1.7, wx)
        oy = warp * noise(u + 2.3, v + 0.0, wy)
        return noise(u + ox, v + oy, base)
    return H


def _al_contours(H, T, G, levels):
    import math as _m
    twopi = 2 * _m.pi
    grid = [[H(i / G * twopi, j / G * twopi) for i in range(G + 1)] for j in range(G + 1)]
    def sx(i): return i / G * T
    def sy(j): return j / G * T
    out = []
    for lev in levels:
        segs = []
        for j in range(G):
            row = grid[j]; row2 = grid[j + 1]
            for i in range(G):
                a = row[i]; b = row[i + 1]; c = row2[i + 1]; dd = row2[i]
                idx = (a > lev) | ((b > lev) << 1) | ((c > lev) << 2) | ((dd > lev) << 3)
                if idx == 0 or idx == 15:
                    continue
                def ip(p1, p2, v1, v2):
                    t = 0.5 if v2 == v1 else (lev - v1) / (v2 - v1)
                    if t < 0: t = 0.0
                    if t > 1: t = 1.0
                    return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)
                x0 = sx(i); y0 = sy(j); x1 = sx(i + 1); y1 = sy(j + 1)
                TOP = ip((x0, y0), (x1, y0), a, b)
                RIGHT = ip((x1, y0), (x1, y1), b, c)
                BOT = ip((x0, y1), (x1, y1), dd, c)
                LEFT = ip((x0, y0), (x0, y1), a, dd)
                if idx in (1, 14): segs.append((LEFT, TOP))
                elif idx in (2, 13): segs.append((TOP, RIGHT))
                elif idx in (3, 12): segs.append((LEFT, RIGHT))
                elif idx in (4, 11): segs.append((RIGHT, BOT))
                elif idx in (6, 9): segs.append((TOP, BOT))
                elif idx in (7, 8): segs.append((LEFT, BOT))
                elif idx in (5, 10):
                    center = (a + b + c + dd) / 4.0
                    if (idx == 5) == (center > lev):
                        segs.append((LEFT, TOP)); segs.append((RIGHT, BOT))
                    else:
                        segs.append((LEFT, BOT)); segs.append((TOP, RIGHT))
        out.append(segs)
    return out


def generate_aardlagen_svg(palette, tile_size, complexity, seed=None):
    import math as _m, random as _r
    from collections import defaultdict
    T = float(tile_size)
    k = _palet(palette)
    bg = k[0]; lijn = k[1]
    ader1 = k[2] if len(k) > 2 else lijn
    ader2 = k[3] if len(k) > 3 else lijn
    ader3 = k[4] if len(k) > 4 else lijn
    tile_cm = 40
    if isinstance(palette, dict):
        try:
            tile_cm = int(palette.get("_tile_cm", 40))
        except (TypeError, ValueError):
            tile_cm = 40
    lw = max(0.5, 3.0 / (tile_cm / 40.0))
    if seed is None:
        seed = _r.randint(1, 10 ** 9)
    H = _al_field_fn(seed)
    G = {"low": 90, "medium": 120, "high": 150}.get(complexity, 120)
    nlev = {"low": 22, "medium": 30, "high": 40}.get(complexity, 30)
    probe = [H(i / 16.0 * 2 * _m.pi, j / 16.0 * 2 * _m.pi) for i in range(16) for j in range(16)]
    lo = min(probe); hi = max(probe)
    levels = [lo + (hi - lo) * (i / float(nlev)) for i in range(1, nlev)]
    segs_per_level = _al_contours(H, T, G, levels)
    def level_color(ix):
        rr = _r.Random(seed * 7 + ix).random()
        if rr < 0.08: return ader1
        if rr < 0.14: return ader2
        if rr < 0.20: return ader3
        return lijn
    bucket = defaultdict(list)
    for ix, segs in enumerate(segs_per_level):
        bucket[level_color(ix)].extend(segs)
    out = ['<rect width="{:.0f}" height="{:.0f}" fill="{}"/>'.format(T, T, bg)]
    for col, segs in bucket.items():
        if not segs:
            continue
        d = ''.join('M{:.1f} {:.1f}L{:.1f} {:.1f}'.format(p[0], p[1], q[0], q[1]) for (p, q) in segs)
        out.append('<path d="{}" stroke="{}" stroke-width="{:.2f}" fill="none" stroke-linecap="round"/>'.format(d, col, lw))
    return "\n".join(out)


# --- Art Deco WAAIER: vector aangeleverd door Ab; naadloos, paletgestuurd ---
_ARTDECO_WAAIER_PATHS = ['M798.52,599.24C798.36,580.24 795.54,561.87 790.39,544.48C699.68,572.57 632.76,644.62 610.01,733.37C611.32,729.68 612.74,726.02 614.27,722.38C624.43,698.37 638.98,676.81 657.49,658.29C676.01,639.78 697.57,625.24 721.58,615.08C745.98,604.76 771.85,599.44 798.52,599.24ZM585.72,722.38C587.26,726.02 588.68,729.68 590.00,733.37C567.24,644.62 500.33,572.57 409.61,544.48C404.46,561.87 401.63,580.24 401.48,599.24C428.16,599.44 454.03,604.76 478.42,615.08C502.43,625.24 524.00,639.78 542.51,658.29C561.03,676.81 575.57,698.37 585.72,722.38ZM410.52,541.52C437.36,549.83 462.67,562.24 485.78,578.44C509.00,594.73 529.46,614.44 546.59,637.05C563.91,659.91 577.42,685.19 586.76,712.18C587.90,715.50 588.98,718.84 590.00,722.20C569.72,629.45 514.00,547.41 432.67,494.06C423.31,508.69 415.81,524.62 410.52,541.52ZM434.36,491.46C484.13,524.12 525.74,568.76 554.76,620.66C569.65,647.27 581.18,675.67 589.04,705.06C590.88,711.94 592.52,718.88 593.95,725.86C581.45,623.14 543.28,525.97 481.74,441.41C463.20,455.21 447.14,472.16 434.36,491.46ZM484.24,439.58C521.24,490.42 550.07,546.30 569.94,605.70C581.74,640.96 590.26,677.16 595.47,713.95C588.36,611.18 568.64,510.16 536.57,412.64C517.71,419.02 500.10,428.16 484.24,439.58ZM663.42,412.64C631.36,510.16 611.63,611.18 604.53,713.95C609.73,677.16 618.26,640.96 630.06,605.70C649.93,546.30 678.77,490.42 715.76,439.58C699.90,428.16 682.30,419.02 663.42,412.64ZM718.26,441.41C656.72,525.97 618.55,623.14 606.06,725.86C607.49,718.88 609.12,711.94 610.96,705.06C618.82,675.67 630.36,647.27 645.24,620.66C674.26,568.76 715.87,524.12 765.64,491.46C752.86,472.16 736.80,455.21 718.26,441.41ZM601.53,712.43C608.72,609.84 628.47,509.02 660.48,411.67C641.87,405.70 622.07,402.41 601.53,402.25L601.53,712.43ZM598.44,402.25C577.91,402.42 558.12,405.70 539.52,411.67C571.46,508.81 591.19,609.41 598.44,711.76L598.44,402.25ZM767.33,494.06C686.01,547.41 630.28,629.45 610.01,722.20C611.02,718.84 612.10,715.50 613.25,712.18C622.57,685.19 636.09,659.91 653.41,637.05C670.55,614.44 691.01,594.73 714.23,578.44C737.33,562.24 762.64,549.83 789.48,541.52C784.19,524.62 776.69,508.69 767.33,494.06ZM801.62,600.79L801.62,602.34L800.07,602.34C691.74,602.34 603.41,689.53 601.56,797.43L601.56,798.29L601.57,798.41L601.57,800.88L598.42,800.88C598.42,800.72 598.44,800.57 598.44,800.41L598.44,796.87C596.28,689.24 508.06,602.34 399.93,602.34L398.38,602.34L398.38,600.79C398.38,573.56 403.71,547.16 414.23,522.30C424.38,498.29 438.92,476.72 457.44,458.20C475.96,439.69 497.52,425.15 521.54,414.99C546.38,404.48 572.77,399.15 599.98,399.14L600.02,399.14C627.23,399.15 653.62,404.48 678.47,414.99C702.48,425.15 724.04,439.69 742.56,458.20C761.08,476.72 775.62,498.29 785.77,522.30C796.28,547.16 801.62,573.56 801.62,600.79Z', 'M398.52,599.24C398.37,580.24 395.54,561.87 390.39,544.48C299.67,572.57 232.76,644.62 210.00,733.37C211.32,729.68 212.74,726.02 214.28,722.38C224.43,698.37 238.97,676.81 257.49,658.29C276.01,639.78 297.57,625.24 321.58,615.08C345.97,604.76 371.84,599.44 398.52,599.24ZM185.72,722.38C187.26,726.02 188.68,729.68 190.00,733.37C167.24,644.62 100.33,572.57 9.61,544.48C4.46,561.87 1.63,580.24 1.48,599.24C28.16,599.44 54.03,604.76 78.42,615.08C102.43,625.24 124.00,639.78 142.51,658.29C161.03,676.81 175.57,698.37 185.72,722.38ZM10.52,541.52C37.36,549.83 62.67,562.24 85.78,578.44C109.00,594.73 129.46,614.44 146.59,637.05C163.91,659.91 177.42,685.19 186.75,712.18C187.90,715.50 188.98,718.84 189.99,722.20C169.72,629.45 114.00,547.41 32.67,494.06C23.31,508.69 15.81,524.62 10.52,541.52ZM34.36,491.46C84.13,524.12 125.74,568.76 154.76,620.66C169.65,647.27 181.18,675.67 189.04,705.06C190.88,711.94 192.51,718.88 193.95,725.86C181.45,623.14 143.28,525.97 81.74,441.41C63.20,455.21 47.14,472.16 34.36,491.46ZM84.24,439.58C121.24,490.42 150.07,546.30 169.94,605.70C181.74,640.96 190.26,677.16 195.47,713.95C188.37,611.18 168.64,510.16 136.57,412.64C117.71,419.02 100.10,428.16 84.24,439.58ZM263.43,412.64C231.36,510.16 211.64,611.18 204.53,713.95C209.74,677.16 218.26,640.96 230.06,605.70C249.93,546.30 278.76,490.42 315.76,439.58C299.90,428.16 282.30,419.02 263.43,412.64ZM318.26,441.41C256.72,525.97 218.55,623.14 206.06,725.86C207.49,718.88 209.12,711.94 210.96,705.06C218.82,675.67 230.36,647.27 245.24,620.66C274.26,568.76 315.87,524.12 365.64,491.46C352.86,472.16 336.80,455.21 318.26,441.41ZM201.53,712.43C208.72,609.84 228.47,509.02 260.48,411.67C241.87,405.70 222.06,402.41 201.53,402.25L201.53,712.43ZM198.43,402.25C177.91,402.42 158.12,405.70 139.52,411.67C171.46,508.81 191.19,609.41 198.43,711.76L198.43,402.25ZM367.33,494.06C286.00,547.41 230.28,629.45 210.01,722.20C211.02,718.84 212.10,715.50 213.25,712.18C222.58,685.19 236.09,659.91 253.41,637.05C270.55,614.44 291.01,594.73 314.22,578.44C337.33,562.24 362.64,549.83 389.49,541.52C384.19,524.62 376.69,508.69 367.33,494.06ZM401.62,600.79L401.62,602.34L400.07,602.34C291.74,602.34 203.41,689.53 201.56,797.43C201.56,797.72 201.56,798.00 201.57,798.29L201.57,798.56C201.57,799.33 201.57,800.11 201.57,800.88L198.43,800.88C198.43,800.72 198.43,800.57 198.43,800.41L198.43,796.87C196.28,689.24 108.06,602.34 -0.07,602.34L-1.62,602.34L-1.62,600.79C-1.62,573.56 3.71,547.16 14.23,522.30C24.38,498.29 38.92,476.72 57.44,458.20C75.96,439.69 97.52,425.15 121.54,414.99C146.38,404.48 172.77,399.15 199.98,399.14L200.02,399.14C227.23,399.15 253.62,404.48 278.47,414.99C302.48,425.15 324.04,439.69 342.56,458.20C361.08,476.72 375.62,498.29 385.77,522.30C396.29,547.16 401.62,573.56 401.62,600.79Z', 'M-1.48,599.24C-1.63,580.24 -4.46,561.87 -9.61,544.48C-100.33,572.57 -167.24,644.62 -190.00,733.37C-188.68,729.68 -187.26,726.02 -185.72,722.38C-175.57,698.37 -161.03,676.81 -142.51,658.29C-123.99,639.78 -102.43,625.24 -78.42,615.08C-54.03,604.76 -28.16,599.44 -1.48,599.24ZM-214.28,722.38C-212.74,726.02 -211.32,729.68 -210.00,733.37C-232.76,644.62 -299.67,572.57 -390.39,544.48C-395.54,561.87 -398.37,580.24 -398.52,599.24C-371.84,599.44 -345.97,604.76 -321.58,615.08C-297.57,625.24 -276.00,639.78 -257.49,658.29C-238.97,676.81 -224.43,698.37 -214.28,722.38ZM-389.48,541.52C-362.64,549.83 -337.33,562.24 -314.22,578.44C-291.00,594.73 -270.55,614.44 -253.41,637.05C-236.09,659.91 -222.58,685.19 -213.25,712.18C-212.10,715.50 -211.02,718.84 -210.01,722.20C-230.28,629.45 -286.00,547.41 -367.33,494.06C-376.69,508.69 -384.19,524.62 -389.48,541.52ZM-365.64,491.46C-315.87,524.12 -274.26,568.76 -245.24,620.66C-230.35,647.27 -218.82,675.67 -210.96,705.06C-209.12,711.94 -207.49,718.88 -206.05,725.86C-218.55,623.14 -256.72,525.97 -318.26,441.41C-336.80,455.21 -352.86,472.16 -365.64,491.46ZM-315.76,439.58C-278.76,490.42 -249.93,546.30 -230.06,605.70C-218.26,640.96 -209.74,677.16 -204.53,713.95C-211.63,611.18 -231.36,510.16 -263.43,412.64C-282.29,419.02 -299.90,428.16 -315.76,439.58ZM-136.57,412.64C-168.64,510.16 -188.36,611.18 -195.47,713.95C-190.26,677.16 -181.74,640.96 -169.94,605.70C-150.07,546.30 -121.24,490.42 -84.24,439.58C-100.10,428.16 -117.70,419.02 -136.57,412.64ZM-81.74,441.41C-143.28,525.97 -181.45,623.14 -193.94,725.86C-192.51,718.88 -190.88,711.94 -189.04,705.06C-181.18,675.67 -169.64,647.27 -154.76,620.66C-125.74,568.76 -84.13,524.12 -34.36,491.46C-47.14,472.16 -63.20,455.21 -81.74,441.41ZM-198.47,712.43C-191.28,609.84 -171.53,509.02 -139.52,411.67C-158.13,405.70 -177.94,402.41 -198.47,402.25L-198.47,712.43ZM-201.57,402.25C-222.09,402.42 -241.88,405.70 -260.48,411.67C-228.54,508.81 -208.81,609.41 -201.57,711.76L-201.57,402.25ZM-32.67,494.06C-114.00,547.41 -169.72,629.45 -189.99,722.20C-188.98,718.84 -187.90,715.50 -186.75,712.18C-177.42,685.19 -163.91,659.91 -146.59,637.05C-129.45,614.44 -108.99,594.73 -85.78,578.44C-62.67,562.24 -37.36,549.83 -10.51,541.52C-15.81,524.62 -23.31,508.69 -32.67,494.06ZM1.62,600.79L1.62,602.34L0.07,602.34C-108.26,602.34 -196.59,689.53 -198.44,797.43C-198.44,797.72 -198.44,798.00 -198.43,798.29L-198.43,798.56C-198.43,799.33 -198.43,800.11 -198.43,800.88L-201.57,800.88C-201.57,800.72 -201.57,800.57 -201.57,800.41L-201.57,796.87C-203.72,689.24 -291.94,602.34 -400.07,602.34L-401.62,602.34L-401.62,600.79C-401.62,573.56 -396.29,547.16 -385.77,522.30C-375.62,498.29 -361.08,476.72 -342.56,458.20C-324.04,439.69 -302.48,425.15 -278.46,414.99C-253.62,404.48 -227.23,399.15 -200.02,399.14L-199.98,399.14C-172.77,399.15 -146.38,404.48 -121.53,414.99C-97.52,425.15 -75.96,439.69 -57.44,458.20C-38.92,476.72 -24.38,498.29 -14.23,522.30C-3.71,547.16 1.62,573.56 1.62,600.79Z', 'M598.52,399.24C598.36,380.24 595.54,361.87 590.39,344.48C499.67,372.57 432.76,444.62 410.00,533.38C411.32,529.68 412.74,526.02 414.28,522.39C424.43,498.38 438.97,476.81 457.49,458.30C476.01,439.78 497.57,425.24 521.58,415.08C545.97,404.77 571.84,399.44 598.52,399.24ZM385.72,522.39C387.26,526.02 388.68,529.68 390.00,533.38C367.24,444.62 300.33,372.57 209.61,344.48C204.46,361.87 201.63,380.24 201.48,399.24C228.16,399.44 254.03,404.77 278.42,415.08C302.43,425.24 324.00,439.78 342.51,458.30C361.03,476.81 375.57,498.38 385.72,522.39ZM210.52,341.52C237.36,349.83 262.67,362.24 285.78,378.44C309.00,394.72 329.46,414.44 346.59,437.05C363.91,459.91 377.42,485.18 386.75,512.18C387.90,515.50 388.98,518.84 389.99,522.20C369.72,429.45 314.00,347.41 232.67,294.06C223.31,308.69 215.81,324.62 210.52,341.52ZM234.36,291.46C284.13,324.12 325.74,368.75 354.76,420.66C369.65,447.27 381.18,475.67 389.04,505.06C390.88,511.94 392.51,518.88 393.95,525.86C381.45,423.14 343.28,325.97 281.74,241.41C263.20,255.21 247.14,272.16 234.36,291.46ZM284.24,239.58C321.24,290.42 350.07,346.30 369.94,405.70C381.74,440.96 390.26,477.16 395.47,513.95C388.37,411.17 368.64,310.16 336.57,212.64C317.71,219.02 300.10,228.16 284.24,239.58ZM463.43,212.64C431.36,310.16 411.64,411.17 404.53,513.95C409.74,477.16 418.26,440.96 430.06,405.70C449.93,346.30 478.76,290.42 515.76,239.58C499.90,228.16 482.30,219.02 463.43,212.64ZM518.26,241.41C456.72,325.97 418.55,423.14 406.06,525.86C407.49,518.88 409.12,511.94 410.96,505.06C418.82,475.67 430.36,447.27 445.24,420.66C474.26,368.75 515.87,324.12 565.64,291.46C552.86,272.16 536.80,255.21 518.26,241.41ZM401.53,512.43C408.72,409.84 428.47,309.02 460.48,211.67C441.87,205.70 422.06,202.41 401.53,202.25L401.53,512.43ZM398.43,202.25C377.91,202.42 358.12,205.70 339.52,211.67C371.46,308.81 391.19,409.41 398.43,511.76L398.43,202.25ZM567.33,294.06C486.00,347.41 430.28,429.45 410.01,522.20C411.02,518.84 412.10,515.50 413.25,512.18C422.58,485.18 436.09,459.91 453.41,437.05C470.55,414.44 491.01,394.72 514.22,378.44C537.33,362.24 562.64,349.83 589.48,341.52C584.19,324.62 576.69,308.69 567.33,294.06ZM601.62,400.78L601.62,402.34L600.07,402.34C491.74,402.34 403.41,489.54 401.56,597.43C401.56,597.72 401.56,598.00 401.57,598.29L401.57,598.56C401.57,599.33 401.57,600.11 401.57,600.88L398.43,600.88C398.43,600.72 398.43,600.57 398.43,600.41L398.43,596.87C396.28,489.23 308.06,402.34 199.93,402.34L198.38,402.34L198.38,400.78C198.38,373.56 203.71,347.16 214.23,322.30C224.38,298.29 238.92,276.72 257.44,258.20C275.96,239.69 297.52,225.15 321.54,214.99C346.38,204.48 372.77,199.15 399.98,199.14L400.02,199.14C427.23,199.15 453.62,204.48 478.47,214.99C502.48,225.15 524.04,239.69 542.56,258.20C561.08,276.72 575.62,298.29 585.77,322.30C596.28,347.16 601.62,373.56 601.62,400.78Z', 'M198.52,399.24C198.37,380.24 195.54,361.87 190.39,344.48C99.67,372.57 32.76,444.62 10.00,533.38C11.32,529.68 12.74,526.02 14.28,522.39C24.43,498.38 38.97,476.81 57.49,458.30C76.01,439.78 97.57,425.24 121.58,415.08C145.97,404.77 171.84,399.44 198.52,399.24ZM-14.28,522.39C-12.74,526.02 -11.32,529.68 -10.00,533.38C-32.76,444.62 -99.67,372.57 -190.39,344.48C-195.54,361.87 -198.37,380.24 -198.52,399.24C-171.84,399.44 -145.97,404.77 -121.58,415.08C-97.57,425.24 -76.00,439.78 -57.49,458.30C-38.97,476.81 -24.43,498.38 -14.28,522.39ZM-189.48,341.52C-162.64,349.83 -137.33,362.24 -114.22,378.44C-91.00,394.72 -70.54,414.44 -53.41,437.05C-36.09,459.91 -22.58,485.18 -13.25,512.18C-12.10,515.50 -11.02,518.84 -10.01,522.20C-30.28,429.45 -86.00,347.41 -167.33,294.06C-176.69,308.69 -184.19,324.62 -189.48,341.52ZM-165.64,291.46C-115.87,324.12 -74.26,368.75 -45.24,420.66C-30.35,447.27 -18.82,475.67 -10.96,505.06C-9.12,511.94 -7.49,518.88 -6.05,525.86C-18.55,423.14 -56.72,325.97 -118.26,241.41C-136.80,255.21 -152.86,272.16 -165.64,291.46ZM-115.76,239.58C-78.76,290.42 -49.93,346.30 -30.06,405.70C-18.26,440.96 -9.74,477.16 -4.53,513.95C-11.63,411.17 -31.36,310.16 -63.43,212.64C-82.29,219.02 -99.90,228.16 -115.76,239.58ZM63.43,212.64C31.36,310.16 11.64,411.17 4.53,513.95C9.74,477.16 18.26,440.96 30.06,405.70C49.93,346.30 78.76,290.42 115.76,239.58C99.90,228.16 82.30,219.02 63.43,212.64ZM118.26,241.41C56.72,325.97 18.55,423.14 6.06,525.86C7.49,518.88 9.12,511.94 10.96,505.06C18.82,475.67 30.36,447.27 45.24,420.66C74.26,368.75 115.87,324.12 165.64,291.46C152.86,272.16 136.80,255.21 118.26,241.41ZM1.53,512.43C8.72,409.84 28.47,309.02 60.48,211.67C41.87,205.70 22.06,202.41 1.53,202.25L1.53,512.43ZM-1.57,202.25C-22.09,202.42 -41.88,205.70 -60.48,211.67C-28.54,308.81 -8.81,409.41 -1.57,511.76L-1.57,202.25ZM167.33,294.06C86.00,347.41 30.28,429.45 10.01,522.20C11.02,518.84 12.10,515.50 13.25,512.18C22.58,485.18 36.09,459.91 53.41,437.05C70.55,414.44 91.01,394.72 114.22,378.44C137.33,362.24 162.64,349.83 189.49,341.52C184.19,324.62 176.69,308.69 167.33,294.06ZM201.62,400.78L201.62,402.34L200.07,402.34C91.74,402.34 3.41,489.54 1.56,597.43C1.56,597.72 1.56,598.00 1.57,598.29L1.57,598.56C1.57,599.33 1.57,600.11 1.57,600.88L-1.57,600.88C-1.57,600.72 -1.57,600.57 -1.57,600.41L-1.57,596.87C-3.72,489.23 -91.94,402.34 -200.07,402.34L-201.62,402.34L-201.62,400.78C-201.62,373.56 -196.29,347.16 -185.77,322.30C-175.62,298.29 -161.08,276.72 -142.56,258.20C-124.04,239.69 -102.48,225.15 -78.46,214.99C-53.62,204.48 -27.23,199.15 -0.02,199.14L0.02,199.14C27.23,199.15 53.62,204.48 78.47,214.99C102.48,225.15 124.04,239.69 142.56,258.20C161.08,276.72 175.62,298.29 185.77,322.30C196.29,347.16 201.62,373.56 201.62,400.78Z', 'M798.52,199.24C798.36,180.24 795.54,161.87 790.39,144.48C699.68,172.57 632.76,244.62 610.01,333.38C611.32,329.68 612.74,326.02 614.27,322.39C624.43,298.38 638.98,276.81 657.49,258.30C676.01,239.78 697.57,225.24 721.58,215.08C745.98,204.77 771.85,199.44 798.52,199.24ZM585.72,322.39C587.26,326.02 588.68,329.68 590.00,333.38C567.24,244.62 500.33,172.57 409.61,144.48C404.46,161.87 401.63,180.24 401.48,199.24C428.16,199.44 454.03,204.77 478.42,215.08C502.43,225.24 524.00,239.78 542.51,258.30C561.03,276.81 575.57,298.38 585.72,322.39ZM410.52,141.52C437.36,149.83 462.67,162.24 485.78,178.44C509.00,194.72 529.46,214.44 546.59,237.05C563.91,259.91 577.42,285.18 586.76,312.18C587.90,315.50 588.98,318.84 590.00,322.20C569.72,229.45 514.00,147.41 432.67,94.06C423.31,108.69 415.81,124.62 410.52,141.52ZM434.36,91.46C484.13,124.12 525.74,168.75 554.76,220.66C569.65,247.27 581.18,275.67 589.04,305.06C590.88,311.94 592.52,318.88 593.95,325.86C581.45,223.14 543.28,125.97 481.74,41.41C463.20,55.21 447.14,72.16 434.36,91.46ZM484.24,39.58C521.24,90.42 550.07,146.30 569.94,205.70C581.74,240.96 590.26,277.16 595.47,313.95C588.36,211.17 568.64,110.16 536.57,12.64C517.71,19.02 500.10,28.16 484.24,39.58ZM663.42,12.64C631.36,110.16 611.63,211.17 604.53,313.95C609.73,277.16 618.26,240.96 630.06,205.70C649.93,146.30 678.77,90.42 715.76,39.58C699.90,28.16 682.30,19.02 663.42,12.64ZM718.26,41.41C656.72,125.97 618.55,223.14 606.06,325.86C607.49,318.88 609.12,311.94 610.96,305.06C618.82,275.67 630.36,247.27 645.24,220.66C674.26,168.75 715.87,124.12 765.64,91.46C752.86,72.16 736.80,55.21 718.26,41.41ZM601.53,312.43C608.72,209.84 628.47,109.02 660.48,11.67C641.87,5.70 622.07,2.41 601.53,2.25L601.53,312.43ZM598.44,2.25C577.91,2.42 558.12,5.70 539.52,11.67C571.46,108.81 591.19,209.41 598.44,311.76L598.44,2.25ZM767.33,94.06C686.01,147.41 630.28,229.45 610.01,322.20C611.02,318.84 612.10,315.50 613.25,312.18C622.57,285.18 636.09,259.91 653.41,237.05C670.55,214.44 691.01,194.72 714.23,178.44C737.33,162.24 762.64,149.83 789.48,141.52C784.19,124.62 776.69,108.69 767.33,94.06ZM801.62,200.78L801.62,202.34L800.07,202.34C691.74,202.34 603.41,289.54 601.56,397.43L601.56,398.30L601.57,398.41L601.57,400.88L598.42,400.88C598.42,400.72 598.44,400.57 598.44,400.41L598.44,396.86C596.28,289.23 508.06,202.34 399.93,202.34L398.38,202.34L398.38,200.78C398.38,173.56 403.71,147.16 414.23,122.30C424.38,98.29 438.92,76.72 457.44,58.20C475.96,39.69 497.52,25.15 521.54,14.99C546.38,4.48 572.77,-0.85 599.98,-0.86L600.02,-0.86C627.23,-0.85 653.62,4.48 678.47,14.99C702.48,25.15 724.04,39.69 742.56,58.20C761.08,76.72 775.62,98.29 785.77,122.30C796.28,147.16 801.62,173.56 801.62,200.78Z', 'M398.52,199.24C398.37,180.24 395.54,161.87 390.39,144.48C299.67,172.57 232.76,244.62 210.00,333.38C211.32,329.68 212.74,326.02 214.28,322.39C224.43,298.38 238.97,276.81 257.49,258.30C276.01,239.78 297.57,225.24 321.58,215.08C345.97,204.77 371.84,199.44 398.52,199.24ZM185.72,322.39C187.26,326.02 188.68,329.68 190.00,333.38C167.24,244.62 100.33,172.57 9.61,144.48C4.46,161.87 1.63,180.24 1.48,199.24C28.16,199.44 54.03,204.77 78.42,215.08C102.43,225.24 124.00,239.78 142.51,258.30C161.03,276.81 175.57,298.38 185.72,322.39ZM10.52,141.52C37.36,149.83 62.67,162.24 85.78,178.44C109.00,194.72 129.46,214.44 146.59,237.05C163.91,259.91 177.42,285.18 186.75,312.18C187.90,315.50 188.98,318.84 189.99,322.20C169.72,229.45 114.00,147.41 32.67,94.06C23.31,108.69 15.81,124.62 10.52,141.52ZM34.36,91.46C84.13,124.12 125.74,168.75 154.76,220.66C169.65,247.27 181.18,275.67 189.04,305.06C190.88,311.94 192.51,318.88 193.95,325.86C181.45,223.14 143.28,125.97 81.74,41.41C63.20,55.21 47.14,72.16 34.36,91.46ZM84.24,39.58C121.24,90.42 150.07,146.30 169.94,205.70C181.74,240.96 190.26,277.16 195.47,313.95C188.37,211.17 168.64,110.16 136.57,12.64C117.71,19.02 100.10,28.16 84.24,39.58ZM263.43,12.64C231.36,110.16 211.64,211.17 204.53,313.95C209.74,277.16 218.26,240.96 230.06,205.70C249.93,146.30 278.76,90.42 315.76,39.58C299.90,28.16 282.30,19.02 263.43,12.64ZM318.26,41.41C256.72,125.97 218.55,223.14 206.06,325.86C207.49,318.88 209.12,311.94 210.96,305.06C218.82,275.67 230.36,247.27 245.24,220.66C274.26,168.75 315.87,124.12 365.64,91.46C352.86,72.16 336.80,55.21 318.26,41.41ZM201.53,312.43C208.72,209.84 228.47,109.02 260.48,11.67C241.87,5.70 222.06,2.41 201.53,2.25L201.53,312.43ZM198.43,2.25C177.91,2.42 158.12,5.70 139.52,11.67C171.46,108.81 191.19,209.41 198.43,311.76L198.43,2.25ZM367.33,94.06C286.00,147.41 230.28,229.45 210.01,322.20C211.02,318.84 212.10,315.50 213.25,312.18C222.58,285.18 236.09,259.91 253.41,237.05C270.55,214.44 291.01,194.72 314.22,178.44C337.33,162.24 362.64,149.83 389.49,141.52C384.19,124.62 376.69,108.69 367.33,94.06ZM401.62,200.78L401.62,202.34L400.07,202.34C291.74,202.34 203.41,289.54 201.56,397.43C201.56,397.72 201.56,398.00 201.57,398.29L201.57,398.55C201.57,399.32 201.57,400.10 201.57,400.88L198.43,400.88C198.43,400.72 198.43,400.57 198.43,400.41L198.43,396.86C196.28,289.23 108.06,202.34 -0.07,202.34L-1.62,202.34L-1.62,200.78C-1.62,173.56 3.71,147.16 14.23,122.30C24.38,98.29 38.92,76.72 57.44,58.20C75.96,39.69 97.52,25.15 121.54,14.99C146.38,4.48 172.77,-0.85 199.98,-0.86L200.02,-0.86C227.23,-0.85 253.62,4.48 278.47,14.99C302.48,25.15 324.04,39.69 342.56,58.20C361.08,76.72 375.62,98.29 385.77,122.30C396.29,147.16 401.62,173.56 401.62,200.78Z', 'M-1.48,199.24C-1.63,180.24 -4.46,161.87 -9.61,144.48C-100.33,172.57 -167.24,244.62 -190.00,333.38C-188.68,329.68 -187.26,326.02 -185.72,322.39C-175.57,298.38 -161.03,276.81 -142.51,258.30C-123.99,239.78 -102.43,225.24 -78.42,215.08C-54.03,204.77 -28.16,199.44 -1.48,199.24ZM-214.28,322.39C-212.74,326.02 -211.32,329.68 -210.00,333.38C-232.76,244.62 -299.67,172.57 -390.39,144.48C-395.54,161.87 -398.37,180.24 -398.52,199.24C-371.84,199.44 -345.97,204.77 -321.58,215.08C-297.57,225.24 -276.00,239.78 -257.49,258.30C-238.97,276.81 -224.43,298.38 -214.28,322.39ZM-389.48,141.52C-362.64,149.83 -337.33,162.24 -314.22,178.44C-291.00,194.72 -270.55,214.44 -253.41,237.05C-236.09,259.91 -222.58,285.18 -213.25,312.18C-212.10,315.50 -211.02,318.84 -210.01,322.20C-230.28,229.45 -286.00,147.41 -367.33,94.06C-376.69,108.69 -384.19,124.62 -389.48,141.52ZM-365.64,91.46C-315.87,124.12 -274.26,168.75 -245.24,220.66C-230.35,247.27 -218.82,275.67 -210.96,305.06C-209.12,311.94 -207.49,318.88 -206.05,325.86C-218.55,223.14 -256.72,125.97 -318.26,41.41C-336.80,55.21 -352.86,72.16 -365.64,91.46ZM-315.76,39.58C-278.76,90.42 -249.93,146.30 -230.06,205.70C-218.26,240.96 -209.74,277.16 -204.53,313.95C-211.63,211.17 -231.36,110.16 -263.43,12.64C-282.29,19.02 -299.90,28.16 -315.76,39.58ZM-136.57,12.64C-168.64,110.16 -188.36,211.17 -195.47,313.95C-190.26,277.16 -181.74,240.96 -169.94,205.70C-150.07,146.30 -121.24,90.42 -84.24,39.58C-100.10,28.16 -117.70,19.02 -136.57,12.64ZM-81.74,41.41C-143.28,125.97 -181.45,223.14 -193.94,325.86C-192.51,318.88 -190.88,311.94 -189.04,305.06C-181.18,275.67 -169.64,247.27 -154.76,220.66C-125.74,168.75 -84.13,124.12 -34.36,91.46C-47.14,72.16 -63.20,55.21 -81.74,41.41ZM-198.47,312.43C-191.28,209.84 -171.53,109.02 -139.52,11.67C-158.13,5.70 -177.94,2.41 -198.47,2.25L-198.47,312.43ZM-201.57,2.25C-222.09,2.42 -241.88,5.70 -260.48,11.67C-228.54,108.81 -208.81,209.41 -201.57,311.76L-201.57,2.25ZM-32.67,94.06C-114.00,147.41 -169.72,229.45 -189.99,322.20C-188.98,318.84 -187.90,315.50 -186.75,312.18C-177.42,285.18 -163.91,259.91 -146.59,237.05C-129.45,214.44 -108.99,194.72 -85.78,178.44C-62.67,162.24 -37.36,149.83 -10.51,141.52C-15.81,124.62 -23.31,108.69 -32.67,94.06ZM1.62,200.78L1.62,202.34L0.07,202.34C-108.26,202.34 -196.59,289.54 -198.44,397.43C-198.44,397.72 -198.44,398.00 -198.43,398.29L-198.43,398.55C-198.43,399.32 -198.43,400.10 -198.43,400.88L-201.57,400.88C-201.57,400.72 -201.57,400.57 -201.57,400.41L-201.57,396.86C-203.72,289.23 -291.94,202.34 -400.07,202.34L-401.62,202.34L-401.62,200.78C-401.62,173.56 -396.29,147.16 -385.77,122.30C-375.62,98.29 -361.08,76.72 -342.56,58.20C-324.04,39.69 -302.48,25.15 -278.46,14.99C-253.62,4.48 -227.23,-0.85 -200.02,-0.86L-199.98,-0.86C-172.77,-0.85 -146.38,4.48 -121.53,14.99C-97.52,25.15 -75.96,39.69 -57.44,58.20C-38.92,76.72 -24.38,98.29 -14.23,122.30C-3.71,147.16 1.62,173.56 1.62,200.78Z', 'M598.52,-0.76C598.36,-19.76 595.54,-38.13 590.39,-55.52C499.67,-27.43 432.76,44.62 410.00,133.38C411.32,129.68 412.74,126.02 414.28,122.39C424.43,98.38 438.97,76.81 457.49,58.30C476.01,39.78 497.57,25.24 521.58,15.08C545.97,4.77 571.84,-0.56 598.52,-0.76ZM385.72,122.39C387.26,126.02 388.68,129.68 390.00,133.38C367.24,44.62 300.33,-27.43 209.61,-55.52C204.46,-38.13 201.63,-19.76 201.48,-0.76C228.16,-0.56 254.03,4.77 278.42,15.08C302.43,25.24 324.00,39.78 342.51,58.30C361.03,76.81 375.57,98.38 385.72,122.39ZM210.52,-58.48C237.36,-50.17 262.67,-37.76 285.78,-21.56C309.00,-5.28 329.46,14.44 346.59,37.05C363.91,59.91 377.42,85.18 386.75,112.18C387.90,115.50 388.98,118.84 389.99,122.20C369.72,29.45 314.00,-52.59 232.67,-105.94C223.31,-91.31 215.81,-75.38 210.52,-58.48ZM234.36,-108.54C284.13,-75.88 325.74,-31.25 354.76,20.66C369.65,47.27 381.18,75.67 389.04,105.06C390.88,111.94 392.51,118.88 393.95,125.86C381.45,23.14 343.28,-74.03 281.74,-158.59C263.20,-144.79 247.14,-127.84 234.36,-108.54ZM284.24,-160.42C321.24,-109.58 350.07,-53.70 369.94,5.70C381.74,40.96 390.26,77.16 395.47,113.95C388.37,11.17 368.64,-89.84 336.57,-187.36C317.71,-180.98 300.10,-171.84 284.24,-160.42ZM463.43,-187.36C431.36,-89.84 411.64,11.17 404.53,113.95C409.74,77.16 418.26,40.96 430.06,5.70C449.93,-53.70 478.76,-109.58 515.76,-160.42C499.90,-171.84 482.30,-180.98 463.43,-187.36ZM518.26,-158.59C456.72,-74.03 418.55,23.14 406.06,125.86C407.49,118.88 409.12,111.94 410.96,105.06C418.82,75.67 430.36,47.27 445.24,20.66C474.26,-31.25 515.87,-75.88 565.64,-108.54C552.86,-127.84 536.80,-144.79 518.26,-158.59ZM401.53,112.43C408.72,9.84 428.47,-90.98 460.48,-188.33C441.87,-194.30 422.06,-197.59 401.53,-197.75L401.53,112.43ZM398.43,-197.75C377.91,-197.58 358.12,-194.30 339.52,-188.33C371.46,-91.19 391.19,9.41 398.43,111.76L398.43,-197.75ZM567.33,-105.94C486.00,-52.59 430.28,29.45 410.01,122.20C411.02,118.84 412.10,115.50 413.25,112.18C422.58,85.18 436.09,59.91 453.41,37.05C470.55,14.44 491.01,-5.28 514.22,-21.56C537.33,-37.76 562.64,-50.17 589.48,-58.48C584.19,-75.38 576.69,-91.31 567.33,-105.94ZM601.62,0.78L601.62,2.34L600.07,2.34C491.74,2.34 403.41,89.54 401.56,197.43C401.56,197.72 401.56,198.00 401.57,198.29L401.57,198.55C401.57,199.32 401.57,200.10 401.57,200.88L398.43,200.88C398.43,200.72 398.43,200.57 398.43,200.41L398.43,196.86C396.28,89.23 308.06,2.34 199.93,2.34L198.38,2.34L198.38,0.78C198.38,-26.44 203.71,-52.84 214.23,-77.70C224.38,-101.71 238.92,-123.28 257.44,-141.80C275.96,-160.31 297.52,-174.85 321.54,-185.01C346.38,-195.52 372.77,-200.85 399.98,-200.86L400.02,-200.86C427.23,-200.85 453.62,-195.52 478.47,-185.01C502.48,-174.85 524.04,-160.31 542.56,-141.80C561.08,-123.28 575.62,-101.71 585.77,-77.70C596.28,-52.84 601.62,-26.44 601.62,0.78Z', 'M198.52,-0.76C198.37,-19.76 195.54,-38.13 190.39,-55.52C99.67,-27.43 32.76,44.62 10.00,133.38C11.32,129.68 12.74,126.02 14.28,122.39C24.43,98.38 38.97,76.81 57.49,58.30C76.01,39.78 97.57,25.24 121.58,15.08C145.97,4.77 171.84,-0.56 198.52,-0.76ZM-14.28,122.39C-12.74,126.02 -11.32,129.68 -10.00,133.38C-32.76,44.62 -99.67,-27.43 -190.39,-55.52C-195.54,-38.13 -198.37,-19.76 -198.52,-0.76C-171.84,-0.56 -145.97,4.77 -121.58,15.08C-97.57,25.24 -76.00,39.78 -57.49,58.30C-38.97,76.81 -24.43,98.38 -14.28,122.39ZM-189.48,-58.48C-162.64,-50.17 -137.33,-37.76 -114.22,-21.56C-91.00,-5.28 -70.54,14.44 -53.41,37.05C-36.09,59.91 -22.58,85.18 -13.25,112.18C-12.10,115.50 -11.02,118.84 -10.01,122.20C-30.28,29.45 -86.00,-52.59 -167.33,-105.94C-176.69,-91.31 -184.19,-75.38 -189.48,-58.48ZM-165.64,-108.54C-115.87,-75.88 -74.26,-31.25 -45.24,20.66C-30.35,47.27 -18.82,75.67 -10.96,105.06C-9.12,111.94 -7.49,118.88 -6.05,125.86C-18.55,23.14 -56.72,-74.03 -118.26,-158.59C-136.80,-144.79 -152.86,-127.84 -165.64,-108.54ZM-115.76,-160.42C-78.76,-109.58 -49.93,-53.70 -30.06,5.70C-18.26,40.96 -9.74,77.16 -4.53,113.95C-11.63,11.17 -31.36,-89.84 -63.43,-187.36C-82.29,-180.98 -99.90,-171.84 -115.76,-160.42ZM63.43,-187.36C31.36,-89.84 11.64,11.17 4.53,113.95C9.74,77.16 18.26,40.96 30.06,5.70C49.93,-53.70 78.76,-109.58 115.76,-160.42C99.90,-171.84 82.30,-180.98 63.43,-187.36ZM118.26,-158.59C56.72,-74.03 18.55,23.14 6.06,125.86C7.49,118.88 9.12,111.94 10.96,105.06C18.82,75.67 30.36,47.27 45.24,20.66C74.26,-31.25 115.87,-75.88 165.64,-108.54C152.86,-127.84 136.80,-144.79 118.26,-158.59ZM1.53,112.43C8.72,9.84 28.47,-90.98 60.48,-188.33C41.87,-194.30 22.06,-197.59 1.53,-197.75L1.53,112.43ZM-1.57,-197.75C-22.09,-197.58 -41.88,-194.30 -60.48,-188.33C-28.54,-91.19 -8.81,9.41 -1.57,111.76L-1.57,-197.75ZM167.33,-105.94C86.00,-52.59 30.28,29.45 10.01,122.20C11.02,118.84 12.10,115.50 13.25,112.18C22.58,85.18 36.09,59.91 53.41,37.05C70.55,14.44 91.01,-5.28 114.22,-21.56C137.33,-37.76 162.64,-50.17 189.49,-58.48C184.19,-75.38 176.69,-91.31 167.33,-105.94ZM201.62,0.78L201.62,2.34L200.07,2.34C91.74,2.34 3.41,89.54 1.56,197.43C1.56,197.72 1.56,198.00 1.57,198.29L1.57,198.55C1.57,199.32 1.57,200.10 1.57,200.88L-1.57,200.88C-1.57,200.72 -1.57,200.57 -1.57,200.41L-1.57,196.86C-3.72,89.23 -91.94,2.34 -200.07,2.34L-201.62,2.34L-201.62,0.78C-201.62,-26.44 -196.29,-52.84 -185.77,-77.70C-175.62,-101.71 -161.08,-123.28 -142.56,-141.80C-124.04,-160.31 -102.48,-174.85 -78.46,-185.01C-53.62,-195.52 -27.23,-200.85 -0.02,-200.86L0.02,-200.86C27.23,-200.85 53.62,-195.52 78.47,-185.01C102.48,-174.85 124.04,-160.31 142.56,-141.80C161.08,-123.28 175.62,-101.71 185.77,-77.70C196.29,-52.84 201.62,-26.44 201.62,0.78Z', 'M798.52,-200.76C798.36,-219.76 795.54,-238.13 790.39,-255.52C699.68,-227.43 632.76,-155.38 610.01,-66.62C611.32,-70.32 612.74,-73.98 614.27,-77.61C624.43,-101.62 638.98,-123.19 657.49,-141.70C676.01,-160.22 697.57,-174.76 721.58,-184.92C745.98,-195.23 771.85,-200.56 798.52,-200.76ZM585.72,-77.61C587.26,-73.98 588.68,-70.32 590.00,-66.62C567.24,-155.38 500.33,-227.43 409.61,-255.52C404.46,-238.13 401.63,-219.76 401.48,-200.76C428.16,-200.56 454.03,-195.23 478.42,-184.92C502.43,-174.76 524.00,-160.22 542.51,-141.70C561.03,-123.19 575.57,-101.62 585.72,-77.61ZM410.52,-258.48C437.36,-250.17 462.67,-237.76 485.78,-221.56C509.00,-205.28 529.46,-185.56 546.59,-162.95C563.91,-140.09 577.42,-114.82 586.76,-87.82C587.90,-84.50 588.98,-81.16 590.00,-77.80C569.72,-170.55 514.00,-252.59 432.67,-305.94C423.31,-291.31 415.81,-275.38 410.52,-258.48ZM434.36,-308.54C484.13,-275.88 525.74,-231.25 554.76,-179.34C569.65,-152.73 581.18,-124.33 589.04,-94.94C590.88,-88.06 592.52,-81.12 593.95,-74.14C581.45,-176.86 543.28,-274.03 481.74,-358.59C463.20,-344.79 447.14,-327.84 434.36,-308.54ZM484.24,-360.42C521.24,-309.58 550.07,-253.70 569.94,-194.30C581.74,-159.04 590.26,-122.84 595.47,-86.05C588.36,-188.83 568.64,-289.84 536.57,-387.36C517.71,-380.98 500.10,-371.84 484.24,-360.42ZM663.42,-387.36C631.36,-289.84 611.63,-188.83 604.53,-86.05C609.73,-122.84 618.26,-159.04 630.06,-194.30C649.93,-253.70 678.77,-309.58 715.76,-360.42C699.90,-371.84 682.30,-380.98 663.42,-387.36ZM718.26,-358.59C656.72,-274.03 618.55,-176.86 606.06,-74.14C607.49,-81.12 609.12,-88.06 610.96,-94.94C618.82,-124.33 630.36,-152.73 645.24,-179.34C674.26,-231.25 715.87,-275.88 765.64,-308.54C752.86,-327.84 736.80,-344.79 718.26,-358.59ZM601.53,-87.57C608.72,-190.16 628.47,-290.98 660.48,-388.33C641.87,-394.30 622.07,-397.59 601.53,-397.75L601.53,-87.57ZM598.44,-397.75C577.91,-397.58 558.12,-394.30 539.52,-388.33C571.46,-291.19 591.19,-190.59 598.44,-88.24L598.44,-397.75ZM767.33,-305.94C686.01,-252.59 630.28,-170.55 610.01,-77.80C611.02,-81.16 612.10,-84.50 613.25,-87.82C622.57,-114.82 636.09,-140.09 653.41,-162.95C670.55,-185.56 691.01,-205.28 714.23,-221.56C737.33,-237.76 762.64,-250.17 789.48,-258.48C784.19,-275.38 776.69,-291.31 767.33,-305.94ZM801.62,-199.22L801.62,-197.66L800.07,-197.66C691.74,-197.66 603.41,-110.46 601.56,-2.57L601.56,-1.70L601.57,-1.59L601.57,0.88L598.42,0.88C598.42,0.72 598.44,0.57 598.44,0.41L598.44,-3.14C596.28,-110.77 508.06,-197.66 399.93,-197.66L398.38,-197.66L398.38,-199.22C398.38,-226.44 403.71,-252.84 414.23,-277.70C424.38,-301.71 438.92,-323.28 457.44,-341.80C475.96,-360.31 497.52,-374.85 521.54,-385.01C546.38,-395.52 572.77,-400.85 599.98,-400.86L600.02,-400.86C627.23,-400.85 653.62,-395.52 678.47,-385.01C702.48,-374.85 724.04,-360.31 742.56,-341.80C761.08,-323.28 775.62,-301.71 785.77,-277.70C796.28,-252.84 801.62,-226.44 801.62,-199.22Z', 'M398.52,-200.76C398.37,-219.76 395.54,-238.13 390.39,-255.52C299.67,-227.43 232.76,-155.38 210.00,-66.62C211.32,-70.32 212.74,-73.98 214.28,-77.61C224.43,-101.62 238.97,-123.19 257.49,-141.70C276.01,-160.22 297.57,-174.76 321.58,-184.92C345.97,-195.23 371.84,-200.56 398.52,-200.76ZM185.72,-77.61C187.26,-73.98 188.68,-70.32 190.00,-66.62C167.24,-155.38 100.33,-227.43 9.61,-255.52C4.46,-238.13 1.63,-219.76 1.48,-200.76C28.16,-200.56 54.03,-195.23 78.42,-184.92C102.43,-174.76 124.00,-160.22 142.51,-141.70C161.03,-123.19 175.57,-101.62 185.72,-77.61ZM10.52,-258.48C37.36,-250.17 62.67,-237.76 85.78,-221.56C109.00,-205.28 129.46,-185.56 146.59,-162.95C163.91,-140.09 177.42,-114.82 186.75,-87.82C187.90,-84.50 188.98,-81.16 189.99,-77.80C169.72,-170.55 114.00,-252.59 32.67,-305.94C23.31,-291.31 15.81,-275.38 10.52,-258.48ZM34.36,-308.54C84.13,-275.88 125.74,-231.25 154.76,-179.34C169.65,-152.73 181.18,-124.33 189.04,-94.94C190.88,-88.06 192.51,-81.12 193.95,-74.14C181.45,-176.86 143.28,-274.03 81.74,-358.59C63.20,-344.79 47.14,-327.84 34.36,-308.54ZM84.24,-360.42C121.24,-309.58 150.07,-253.70 169.94,-194.30C181.74,-159.04 190.26,-122.84 195.47,-86.05C188.37,-188.83 168.64,-289.84 136.57,-387.36C117.71,-380.98 100.10,-371.84 84.24,-360.42ZM263.43,-387.36C231.36,-289.84 211.64,-188.83 204.53,-86.05C209.74,-122.84 218.26,-159.04 230.06,-194.30C249.93,-253.70 278.76,-309.58 315.76,-360.42C299.90,-371.84 282.30,-380.98 263.43,-387.36ZM318.26,-358.59C256.72,-274.03 218.55,-176.86 206.06,-74.14C207.49,-81.12 209.12,-88.06 210.96,-94.94C218.82,-124.33 230.36,-152.73 245.24,-179.34C274.26,-231.25 315.87,-275.88 365.64,-308.54C352.86,-327.84 336.80,-344.79 318.26,-358.59ZM201.53,-87.57C208.72,-190.16 228.47,-290.98 260.48,-388.33C241.87,-394.30 222.06,-397.59 201.53,-397.75L201.53,-87.57ZM198.43,-397.75C177.91,-397.58 158.12,-394.30 139.52,-388.33C171.46,-291.19 191.19,-190.59 198.43,-88.24L198.43,-397.75ZM367.33,-305.94C286.00,-252.59 230.28,-170.55 210.01,-77.80C211.02,-81.16 212.10,-84.50 213.25,-87.82C222.58,-114.82 236.09,-140.09 253.41,-162.95C270.55,-185.56 291.01,-205.28 314.22,-221.56C337.33,-237.76 362.64,-250.17 389.49,-258.48C384.19,-275.38 376.69,-291.31 367.33,-305.94ZM401.62,-199.22L401.62,-197.66L400.07,-197.66C291.74,-197.66 203.41,-110.46 201.56,-2.57C201.56,-2.28 201.56,-2.00 201.57,-1.71L201.57,-1.45C201.57,-0.68 201.57,0.10 201.57,0.88L198.43,0.88C198.43,0.72 198.43,0.57 198.43,0.41L198.43,-3.14C196.28,-110.77 108.06,-197.66 -0.07,-197.66L-1.62,-197.66L-1.62,-199.22C-1.62,-226.44 3.71,-252.84 14.23,-277.70C24.38,-301.71 38.92,-323.28 57.44,-341.80C75.96,-360.31 97.52,-374.85 121.54,-385.01C146.38,-395.52 172.77,-400.85 199.98,-400.86L200.02,-400.86C227.23,-400.85 253.62,-395.52 278.47,-385.01C302.48,-374.85 324.04,-360.31 342.56,-341.80C361.08,-323.28 375.62,-301.71 385.77,-277.70C396.29,-252.84 401.62,-226.44 401.62,-199.22Z', 'M-1.48,-200.76C-1.63,-219.76 -4.46,-238.13 -9.61,-255.52C-100.33,-227.43 -167.24,-155.38 -190.00,-66.62C-188.68,-70.32 -187.26,-73.98 -185.72,-77.61C-175.57,-101.62 -161.03,-123.19 -142.51,-141.70C-123.99,-160.22 -102.43,-174.76 -78.42,-184.92C-54.03,-195.23 -28.16,-200.56 -1.48,-200.76ZM-214.28,-77.61C-212.74,-73.98 -211.32,-70.32 -210.00,-66.62C-232.76,-155.38 -299.67,-227.43 -390.39,-255.52C-395.54,-238.13 -398.37,-219.76 -398.52,-200.76C-371.84,-200.56 -345.97,-195.23 -321.58,-184.92C-297.57,-174.76 -276.00,-160.22 -257.49,-141.70C-238.97,-123.19 -224.43,-101.62 -214.28,-77.61ZM-389.48,-258.48C-362.64,-250.17 -337.33,-237.76 -314.22,-221.56C-291.00,-205.28 -270.55,-185.56 -253.41,-162.95C-236.09,-140.09 -222.58,-114.82 -213.25,-87.82C-212.10,-84.50 -211.02,-81.16 -210.01,-77.80C-230.28,-170.55 -286.00,-252.59 -367.33,-305.94C-376.69,-291.31 -384.19,-275.38 -389.48,-258.48ZM-365.64,-308.54C-315.87,-275.88 -274.26,-231.25 -245.24,-179.34C-230.35,-152.73 -218.82,-124.33 -210.96,-94.94C-209.12,-88.06 -207.49,-81.12 -206.05,-74.14C-218.55,-176.86 -256.72,-274.03 -318.26,-358.59C-336.80,-344.79 -352.86,-327.84 -365.64,-308.54ZM-315.76,-360.42C-278.76,-309.58 -249.93,-253.70 -230.06,-194.30C-218.26,-159.04 -209.74,-122.84 -204.53,-86.05C-211.63,-188.83 -231.36,-289.84 -263.43,-387.36C-282.29,-380.98 -299.90,-371.84 -315.76,-360.42ZM-136.57,-387.36C-168.64,-289.84 -188.36,-188.83 -195.47,-86.05C-190.26,-122.84 -181.74,-159.04 -169.94,-194.30C-150.07,-253.70 -121.24,-309.58 -84.24,-360.42C-100.10,-371.84 -117.70,-380.98 -136.57,-387.36ZM-81.74,-358.59C-143.28,-274.03 -181.45,-176.86 -193.94,-74.14C-192.51,-81.12 -190.88,-88.06 -189.04,-94.94C-181.18,-124.33 -169.64,-152.73 -154.76,-179.34C-125.74,-231.25 -84.13,-275.88 -34.36,-308.54C-47.14,-327.84 -63.20,-344.79 -81.74,-358.59ZM-198.47,-87.57C-191.28,-190.16 -171.53,-290.98 -139.52,-388.33C-158.13,-394.30 -177.94,-397.59 -198.47,-397.75L-198.47,-87.57ZM-201.57,-397.75C-222.09,-397.58 -241.88,-394.30 -260.48,-388.33C-228.54,-291.19 -208.81,-190.59 -201.57,-88.24L-201.57,-397.75ZM-32.67,-305.94C-114.00,-252.59 -169.72,-170.55 -189.99,-77.80C-188.98,-81.16 -187.90,-84.50 -186.75,-87.82C-177.42,-114.82 -163.91,-140.09 -146.59,-162.95C-129.45,-185.56 -108.99,-205.28 -85.78,-221.56C-62.67,-237.76 -37.36,-250.17 -10.51,-258.48C-15.81,-275.38 -23.31,-291.31 -32.67,-305.94ZM1.62,-199.22L1.62,-197.66L0.07,-197.66C-108.26,-197.66 -196.59,-110.46 -198.44,-2.57C-198.44,-2.28 -198.44,-2.00 -198.43,-1.71L-198.43,-1.45C-198.43,-0.68 -198.43,0.10 -198.43,0.88L-201.57,0.88C-201.57,0.72 -201.57,0.57 -201.57,0.41L-201.57,-3.14C-203.72,-110.77 -291.94,-197.66 -400.07,-197.66L-401.62,-197.66L-401.62,-199.22C-401.62,-226.44 -396.29,-252.84 -385.77,-277.70C-375.62,-301.71 -361.08,-323.28 -342.56,-341.80C-324.04,-360.31 -302.48,-374.85 -278.46,-385.01C-253.62,-395.52 -227.23,-400.85 -200.02,-400.86L-199.98,-400.86C-172.77,-400.85 -146.38,-395.52 -121.53,-385.01C-97.52,-374.85 -75.96,-360.31 -57.44,-341.80C-38.92,-323.28 -24.38,-301.71 -14.23,-277.70C-3.71,-252.84 1.62,-226.44 1.62,-199.22Z']

def generate_artdeco_waaier_svg(palette, tile_size, complexity):
    """Art Deco waaier op basis van een aangeleverd vectorpatroon.
    Naadloze repeat-cel, evenodd-vulling, geen clipPath.
    Achtergrond = palet[0], waaier = palet[1]."""
    T = float(tile_size)
    k = _palet(palette)
    bg = k[0]
    goud = k[1]
    sc = T / 400.0
    s = ["<rect width=\"{:.1f}\" height=\"{:.1f}\" fill=\"{}\"/>".format(T, T, bg)]
    s.append("<g transform=\"scale({:.6f})\">".format(sc))
    for d in _ARTDECO_WAAIER_PATHS:
        s.append("<path d=\"{}\" fill=\"{}\" fill-rule=\"evenodd\"/>".format(d, goud))
    s.append("</g>")
    return s
