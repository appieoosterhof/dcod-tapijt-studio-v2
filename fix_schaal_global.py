code = open('app.py').read()

# In build_tile_svg: pas tile_size aan voor ALLE generators
old = '    complexity = analysis.get("complexity", "medium")\n    shape_list = analysis.get("shapes", [])'
new = '    complexity = analysis.get("complexity", "medium")\n    shape_list = analysis.get("shapes", [])\n    # Schaal aanpassen: kleiner tile = fijner patroon\n    tile_size = max(50, int(tile_size * (100 / max(motief_schaal, 10))))'

if 'Schaal aanpassen' not in code:
    code = code.replace(old, new)
    open('app.py','w').write(code)
    print('schaal globaal toegepast')
else:
    print('al aanwezig')
