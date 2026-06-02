code = open('app.py').read()
old = '"abstract": generate_abstract_svg,'
new = '"abstract": generate_abstract_svg,\n    "strepen": generate_strepen_svg,\n    "mozaiek": generate_mozaiek_svg,\n    "chevron": generate_chevron_svg,\n    "hexagoon": generate_hexagoon_svg,\n    "ogee": generate_ogee_svg,\n    "diamant": generate_diamant_svg,'
if '"strepen": generate_strepen_svg' not in code:
    code = code.replace(old, new)
    open('app.py','w').write(code)
    print('generators toegevoegd aan STYLE_GENERATORS')
else:
    print('al aanwezig')
