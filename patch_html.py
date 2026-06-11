code=open('templates/index.html').read()
open('templates/index.html.backup','w').write(code)
chips='\n          <button class="chip" onclick="setPrompt(\'Strakke verticale strepen, strak en modern\')">Strepen</button>\n          <button class="chip" onclick="setPrompt(\'Pixel mozaiek patroon, kleurrijke blokken\')">Mozaiek</button>\n          <button class="chip" onclick="setPrompt(\'Chevron zigzag patroon, pijlvormen\')">Chevron</button>\n          <button class="chip" onclick="setPrompt(\'Hexagonaal honingraat patroon\')">Hexagoon</button>\n          <button class="chip" onclick="setPrompt(\'Ogee schubben dakpan patroon\')">Ogee</button>\n          <button class="chip" onclick="setPrompt(\'Concentrische diamanten patroon\')">Diamant</button>'
if 'Strepen' not in code:
    code=code.replace('>Terrazzo</button>','>Terrazzo</button>'+chips)
    open('templates/index.html','w').write(code)
    print('index.html klaar')
else:
    print('al gedaan')
