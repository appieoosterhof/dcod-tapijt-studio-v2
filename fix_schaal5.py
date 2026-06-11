code = open('app.py').read()

# Verwijder de tile_size aanpassing - die veroorzaakt het probleem
old = '    complexity = analysis.get("complexity", "medium")\n    tile_size = int(tile_size / (motief_schaal / 100.0))'
new = '    complexity = analysis.get("complexity", "medium")'

code = code.replace(old, new)
open('app.py','w').write(code)
print('tile_size aanpassing verwijderd')
