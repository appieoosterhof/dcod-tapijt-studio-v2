code = open('app.py').read()
old = '    if style in extra_styles:\n        generator = STYLE_GENERATORS.get(style)\n        inner = generator(palette, tile_size, complexity)'
new = '    if style in extra_styles:\n        generator = STYLE_GENERATORS.get(style)\n        try:\n            inner = generator(palette, tile_size, complexity, motief_schaal)\n        except TypeError:\n            inner = generator(palette, tile_size, complexity)'
code = code.replace(old, new)
open('app.py','w').write(code)
print('schaal doorgegeven aan generator')
