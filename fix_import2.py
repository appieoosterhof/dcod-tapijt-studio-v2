code = open('app.py').read()
old = 'from modules_extra import generate_strepen_svg,generate_mozaiek_svg,generate_chevron_svg,generate_hexagoon_svg,generate_ogee_svg,generate_diamant_svg'
new = 'from modules_extra import generate_strepen_svg,generate_mozaiek_svg,generate_chevron_svg,generate_hexagoon_svg,generate_ogee_svg,generate_diamant_svg,generate_terrazzo_svg,generate_vrije_vormen_svg'
code = code.replace(old, new)
open('app.py','w').write(code)
print('klaar')
