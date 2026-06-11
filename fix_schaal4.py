code = open('app.py').read()

old = '''    if style in extra_styles:
        generator = STYLE_GENERATORS.get(style)
        inner = generator(palette, tile_size, complexity)'''

new = '''    if style in extra_styles:
        generator = STYLE_GENERATORS.get(style)
        try:
            inner = generator(palette, tile_size, complexity, motief_schaal)
        except TypeError:
            inner = generator(palette, tile_size, complexity)'''

if 'motief_schaal)' not in code:
    code = code.replace(old, new)
    open('app.py','w').write(code)
    print('backend fix klaar')
else:
    print('al aanwezig')
