# Fix modules_extra.py - verwijder dubbele definities (regels 116+)
lines = open('modules_extra.py').readlines()
# Bewaar alleen tot en met de eerste generate_terrazzo definitie afronding
cleaned = []
seen = set()
skip = False
for line in lines:
    if line.startswith('def generate_'):
        fname = line.split('(')[0].replace('def ','')
        if fname in seen:
            skip = True
        else:
            seen.add(fname)
            skip = False
    if not skip:
        cleaned.append(line)
open('modules_extra.py','w').writelines(cleaned)
print('modules_extra.py opgeschoond')

# Fix app.py import
code = open('app.py').read()
old = 'generate_strepen_svg,generate_mozaiek_svg,generate_chevron_svg,generate_hexagoon_svg,generate_ogee_svg,generate_diamant_svg'
new = 'generate_strepen_svg,generate_mozaiek_svg,generate_chevron_svg,generate_hexagoon_svg,generate_ogee_svg,generate_diamant_svg,generate_terrazzo_svg,generate_vrije_vormen_svg'
if 'terrazzo_svg' not in code:
    code = code.replace(old, new)
    open('app.py','w').write(code)
    print('import bijgewerkt')
else:
    print('import was al ok')
