code = open('modules_extra.py').read()

# Hexagoon: stroke zelfde kleur als fill zodat gaten verdwijnen
code = code.replace(
    'stroke="{kleur}" stroke-width="0.5"/>\')',
    'stroke="{kleur}" stroke-width="1.5"/>\')'
)

# Ogee: verwijder dunne lijntjes door stroke weg te halen
code = code.replace(
    'stroke="{kleur}" stroke-width="0.5"/>\')\')',
    '/>\')\')'
)

open('modules_extra.py','w').write(code)
print('fixes klaar')
