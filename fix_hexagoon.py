code = open('modules_extra.py').read()

old = '''def generate_hexagoon_svg(palette,tile_size,complexity):
    T=tile_size; k=_palet(palette); r={'low':T//5,'medium':T//8,'high':T//12}.get(complexity,T//8)
    wh=math.sqrt(3)*r; cs=wh; rs=r*1.5; cols=math.ceil(T/cs)+2; rows=math.ceil(T/rs)+2; stroke=k[2]; s=[]
    for row in range(rows):
        kleur=_gradient(k[1:],row/max(rows-1,1))
        for col in range(cols):
            cx=col*cs+(wh/2 if row%2 else 0)-wh/2; cy=row*rs-r
            pts=[f'{cx+(r-1)*math.cos(math.radians(k2*60)):.1f},{cy+(r-1)*math.sin(math.radians(k2*60)):.1f}' for k2 in range(6)]
            s.append(f'<polygon points="{" ".join(pts)}" fill="{kleur}" stroke="{stroke}" stroke-width="1"/>')
    return '\\n'.join(s)'''

new = '''def generate_hexagoon_svg(palette,tile_size,complexity):
    T=tile_size; k=_palet(palette); r={'low':T//5,'medium':T//8,'high':T//12}.get(complexity,T//8)
    wh=math.sqrt(3)*r; cs=wh; rs=r*1.5; cols=math.ceil(T/cs)+3; rows=math.ceil(T/rs)+3; stroke=k[2]; s=[]
    # Achtergrond in eerste kleur zodat gaten niet wit zijn
    s.append(f\'<rect width="{T}" height="{T}" fill="{k[1]}"/>\')
    for row in range(rows):
        kleur=_gradient(k[1:],row/max(rows-1,1))
        for col in range(cols):
            cx=col*cs+(wh/2 if row%2 else 0)-wh/2; cy=row*rs-r
            # Gebruik exacte r zonder aftrek zodat er geen gaten zijn
            pts=[f\'{cx+r*math.cos(math.radians(k2*60)):.2f},{cy+r*math.sin(math.radians(k2*60)):.2f}\' for k2 in range(6)]
            s.append(f\'<polygon points="{" ".join(pts)}" fill="{kleur}" stroke="{kleur}" stroke-width="0.5"/>\')
    return \'\\n\'.join(s)'''

code = code.replace(old, new)
open('modules_extra.py','w').write(code)
print('hexagoon fix klaar')
