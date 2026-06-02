code = open('app.py').read()

# Zorg dat de nieuwe modules altijd direct hun generator aanroepen
# zonder de shape-detectie logica te storen
old = """    user_specified = any(s in default_shapes and s != "octagon" for s in shape_list)
    if user_specified or shape_list == ["circle"] or shape_list == ["square"] or shape_list == ["triangle"]:
        inner = generate_geometric_svg(palette, tile_size, complexity, shape_list)
    else:
        generator = STYLE_GENERATORS.get(style, generate_geometric_svg)
        if generator == generate_geometric_svg:
            inner = generator(palette, tile_size, complexity, shape_list or ["octagon"])
        else:
            inner = generator(palette, tile_size, complexity)"""

new = """    extra_styles = ["strepen","mozaiek","chevron","hexagoon","ogee","diamant"]
    user_specified = any(s in default_shapes and s != "octagon" for s in shape_list)
    if style in extra_styles:
        generator = STYLE_GENERATORS.get(style)
        inner = generator(palette, tile_size, complexity)
    elif user_specified or shape_list == ["circle"] or shape_list == ["square"] or shape_list == ["triangle"]:
        inner = generate_geometric_svg(palette, tile_size, complexity, shape_list)
    else:
        generator = STYLE_GENERATORS.get(style, generate_geometric_svg)
        if generator == generate_geometric_svg:
            inner = generator(palette, tile_size, complexity, shape_list or ["octagon"])
        else:
            inner = generator(palette, tile_size, complexity)"""

if 'extra_styles' not in code:
    code = code.replace(old, new)
    open('app.py','w').write(code)
    print('fix toegepast')
else:
    print('al gedaan')
