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

def generate_mozaiek_svg(palette,tile_size,complexity):
    T=tile_size; k=_palet(palette); n={'low':8,'medium':14,'high':22}.get(complexity,14); b=T/n; rng=random.Random(2026); s=[]
    for col in range(n+1):
        x=col*b; y=0
        while y<T:
            h=rng.randint(int(b*0.6),int(b*2.2)); h=min(h,T-y)
            s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{b-1:.1f}" height="{h-1:.1f}" fill="{_gradient(k[1:],y/T)}"/>'); y+=h
    return '\n'.join(s)

def generate_chevron_svg(palette,tile_size,complexity):
    T=tile_size; k=_palet(palette); n={'low':5,'medium':8,'high':14}.get(complexity,8); h=T/n; s=[]
    for row in range(n+1):
        yb=row*h; kleur=_gradient(k[1:],row/max(n,1)); np2=math.ceil(T/h)+3; pts=[]
        for i in range(-1,np2):
            x=i*h; pts.append(f'{x:.1f},{yb+h:.1f}'); pts.append(f'{x+h/2:.1f},{yb:.1f}')
        pts.append(f'{T+h:.1f},{yb:.1f}'); pts.append(f'{T+h:.1f},{yb+h:.1f}')
        s.append(f'<polygon points="{" ".join(pts)}" fill="{kleur}"/>')
    return '\n'.join(s)

def generate_hexagoon_svg(palette,tile_size,complexity):
    T=tile_size; k=_palet(palette); r={'low':T//5,'medium':T//8,'high':T//12}.get(complexity,T//8)
    wh=math.sqrt(3)*r; cs=wh; rs=r*1.5; cols=math.ceil(T/cs)+3; rows=math.ceil(T/rs)+3; stroke=k[2]; s=[]
    # Achtergrond in eerste kleur zodat gaten niet wit zijn
    s.append(f'<rect width="{T}" height="{T}" fill="{k[1]}"/>')
    for row in range(rows):
        kleur=_gradient(k[1:],row/max(rows-1,1))
        for col in range(cols):
            cx=col*cs+(wh/2 if row%2 else 0)-wh/2; cy=row*rs-r
            # Gebruik exacte r zonder aftrek zodat er geen gaten zijn
            pts=[f'{cx+r*math.cos(math.radians(k2*60)):.2f},{cy+r*math.sin(math.radians(k2*60)):.2f}' for k2 in range(6)]
            s.append(f'<polygon points="{" ".join(pts)}" fill="{kleur}" stroke="{kleur}" stroke-width="1.5"/>')
    return '\n'.join(s)

def generate_ogee_svg(palette,tile_size,complexity):
    T=tile_size; k=_palet(palette); n={'low':3,'medium':5,'high':8}.get(complexity,5); b=T/n; h=b*0.8; rs=h*0.62; rows=math.ceil(T/rs)+4; s=[]
    s.append(f'<rect width="{T}" height="{T}" fill="{k[-1]}"/>')
    for row in range(rows-1,-1,-1):
        kleur=_gradient(k[1:],row/max(rows-1,1))
        for col in range(-1,n+2):
            x=col*b+(b/2 if row%2 else 0)-b; y=row*rs-h*0.3; cx=x+b/2
            d=(f'M {x:.1f} {y+h:.1f} ' 
               f'Q {cx:.1f} {y-h*0.1:.1f} {x+b:.1f} {y+h:.1f} ' 
               f'Q {x+b+b*0.1:.1f} {y+h*1.8:.1f} {cx:.1f} {y+h*1.75:.1f} ' 
               f'Q {x-b*0.1:.1f} {y+h*1.8:.1f} {x:.1f} {y+h:.1f} Z')
            s.append(f'<path d="{d}" fill="{kleur}" stroke="{kleur}" stroke-width="1.5"/>')
    return '\n'.join(s)

def generate_diamant_svg(palette,tile_size,complexity):
    T=tile_size; k=_palet(palette); nc={'low':2,'medium':3,'high':4}.get(complexity,3); nl={'low':5,'medium':8,'high':12}.get(complexity,8)
    tw=T/nc; th=tw*1.3; s=[]
    for row in range(-1,math.ceil(T/th)+2):
        for col in range(-1,nc+2):
            cx=col*tw+(tw/2 if row%2 else 0); cy=row*th+th/2
            for i in range(nl,0,-1):
                sc=i/nl; w2=(tw/2-3)*sc; h2=(th/2-3)*sc; kleur=_gradient(k[1:],1-(i/nl))
                pts=f'{cx:.1f},{cy-h2:.1f} {cx+w2:.1f},{cy:.1f} {cx:.1f},{cy+h2:.1f} {cx-w2:.1f},{cy:.1f}'
                s.append(f'<polygon points="{pts}" fill="none" stroke="{kleur}" stroke-width="1.2"/>')
    return '\n'.join(s)

def generate_terrazzo_svg(palette, tile_size, complexity, schaal=100):
    import random as _r
    T = tile_size
    k = _palet(palette)
    rng = _r.Random(42)
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    n = {'low':40,'medium':80,'high':140}.get(complexity,80)
    # Schaal bepaalt vlekgrootte direct
    factor = schaal / 100.0
    vlek_min = T * 0.015 * factor
    vlek_max = T * 0.055 * factor
    def ellips(x, y, w, h, angle, kleur):
        return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{w:.1f}" ry="{h:.1f}" fill="{kleur}" transform="rotate({angle:.0f} {x:.1f} {y:.1f})"/>'
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
    return '\n'.join(s)

def generate_vrije_vormen_svg(palette, tile_size, complexity):
    import random as _r
    T = tile_size
    k = _palet(palette)
    rng = _r.Random(99)
    s = [f'<rect width="{T}" height="{T}" fill="{k[0]}"/>']
    n = {'low':8,'medium':14,'high':22}.get(complexity,14)
    def vorm(cx, cy, r, sides, offsets, kleur):
        pts = []
        for j,off in enumerate(offsets):
            a = math.radians(j * 360/sides + off)
            rd = r * rng.uniform(0.6, 1.2)
            pts.append(f'{cx+rd*math.cos(a):.1f},{cy+rd*math.sin(a):.1f}')
        return f'<polygon points="{" ".join(pts)}" fill="{kleur}" opacity="0.82"/>'
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
    return '\n'.join(s)

