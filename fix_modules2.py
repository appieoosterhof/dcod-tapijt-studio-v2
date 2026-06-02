code = open('app.py').read()

# Fix 1: hexagoon prompt moet AI stijl "hexagoon" teruggeven
old = '"Hexagonaal honingraat patroon, zeshoeken"'
# Fix 2: zorg dat "hexagonen" chip ook naar hexagoon gaat
# Fix 3: voeg terrazzo en vrije_vormen toe aan extra_styles
old2 = 'extra_styles = ["strepen","mozaiek","chevron","hexagoon","ogee","diamant"]'
new2 = 'extra_styles = ["strepen","mozaiek","chevron","hexagoon","ogee","diamant","terrazzo","vrije_vormen"]'
if 'terrazzo' not in code:
    code = code.replace(old2, new2)

# Fix 4: voeg terrazzo en vrije_vormen toe aan STYLE_GENERATORS
old3 = '"diamant": generate_diamant_svg,'
new3 = '"diamant": generate_diamant_svg,\n    "terrazzo": generate_terrazzo_svg,\n    "vrije_vormen": generate_vrije_vormen_svg,'
if 'terrazzo_svg' not in code:
    code = code.replace(old3, new3)

# Fix 5: importeer de nieuwe functies
old4 = 'generate_strepen_svg,generate_mozaiek_svg,generate_chevron_svg,generate_hexagoon_svg,generate_ogee_svg,generate_diamant_svg'
new4 = 'generate_strepen_svg,generate_mozaiek_svg,generate_chevron_svg,generate_hexagoon_svg,generate_ogee_svg,generate_diamant_svg,generate_terrazzo_svg,generate_vrije_vormen_svg'
if 'terrazzo_svg' not in code:
    code = code.replace(old4, new4)

# Fix 6: AI prompt uitbreiden
old5 = 'strepen|mozaiek|chevron|hexagoon|ogee|diamant'
new5 = 'strepen|mozaiek|chevron|hexagoon|ogee|diamant|terrazzo|vrije_vormen'
code = code.replace(old5, new5)

open('app.py','w').write(code)
print('app.py bijgewerkt')
