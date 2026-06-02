code = open('modules_extra.py').read()

old = '''def generate_ogee_svg(palette,tile_size,complexity):
    T=tile_size; k=_palet(palette); n={'low':3,'medium':5,'high':8}.get(complexity,5); b=T/n; h=b*0.75; rs=h*0.6; rows=math.ceil(T/rs)+3; s=[]
    for row in range(rows-1,-1,-1):
        kleur=_gradient(k[1:],row/max(rows-1,1))
        for col in range(-1,n+2):
            x=col*b+(b/2 if row%2 else 0)-b; y=row*rs-h*0.3; cx=x+b/2
            d=f'M {x:.1f} {y+h:.1f} Q {cx:.1f} {y:.1f} {x+b:.1f} {y+h:.1f} Q {x+b:.1f} {y+h*1.7:.1f} {cx:.1f} {y+h*1.7:.1f} Q {x:.1f} {y+h*1.7:.1f} {x:.1f} {y+h:.1f} Z'
            s.append(f'<path d="{d}" fill="{kleur}"/>')
    return '\\n'.join(s)'''

new = '''def generate_ogee_svg(palette,tile_size,complexity):
    T=tile_size; k=_palet(palette); n={'low':3,'medium':5,'high':8}.get(complexity,5); b=T/n; h=b*0.8; rs=h*0.62; rows=math.ceil(T/rs)+4; s=[]
    s.append(f\'<rect width="{T}" height="{T}" fill="{k[-1]}"/>\')
    for row in range(rows-1,-1,-1):
        kleur=_gradient(k[1:],row/max(rows-1,1))
        for col in range(-1,n+2):
            x=col*b+(b/2 if row%2 else 0)-b; y=row*rs-h*0.3; cx=x+b/2
            d=(f\'M {x:.1f} {y+h:.1f} \' 
               f\'Q {cx:.1f} {y-h*0.1:.1f} {x+b:.1f} {y+h:.1f} \' 
               f\'Q {x+b+b*0.1:.1f} {y+h*1.8:.1f} {cx:.1f} {y+h*1.75:.1f} \' 
               f\'Q {x-b*0.1:.1f} {y+h*1.8:.1f} {x:.1f} {y+h:.1f} Z\')
            s.append(f\'<path d="{d}" fill="{kleur}" stroke="{kleur}" stroke-width="0.5"/>\')
    return \'\\n\'.join(s)'''

code = code.replace(old, new)
open('modules_extra.py','w').write(code)
print('ogee fix klaar')
