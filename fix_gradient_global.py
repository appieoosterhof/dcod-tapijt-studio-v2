code = open('app.py').read()

# Voeg row_offset toe aan build_repeat_svg zodat generators
# de absolute positie kennen
old = '        inner = generator(palette, tile_size, complexity, motief_schaal)'
new = '        inner = generator(palette, tile_size, complexity, motief_schaal)'

# Betere oplossing: geef aan extra generators een globale seed mee
# zodat kleurverloop consistent is over tegels
# Dit doen we door complexity te vervangen door een vaste waarde bij repeat
print('analyse klaar - oplossing via SVG gradient overlay')
