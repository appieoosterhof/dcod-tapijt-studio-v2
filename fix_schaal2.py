js = open('static/js/app.js').read()
old = "const repeat_type = document.getElementById('repeatType').value;"
new = "const repeat_type = document.getElementById('repeatType').value;\n  const motief_schaal = parseInt(document.getElementById('motiefSchaal')?.value || '100');"
old2 = '"repeat_type": repeat_type,'
new2 = '"repeat_type": repeat_type,\n      "motief_schaal": motief_schaal,'
if 'motief_schaal' not in js:
    js = js.replace(old, new).replace(old2, new2)
    open('static/js/app.js','w').write(js)
    print('JS klaar')
else:
    print('JS al aanwezig')

code = open('app.py').read()
old3 = '    tile_cm = int(data.get("tile_cm", 40))'
new3 = '    tile_cm = int(data.get("tile_cm", 40))\n    motief_schaal = int(data.get("motief_schaal", 100))'
old4 = '        tile_svg = build_tile_svg(analysis, tile_size=400)'
new4 = '        tile_svg = build_tile_svg(analysis, tile_size=400, motief_schaal=motief_schaal)'
old5 = 'def build_tile_svg(analysis: dict, tile_size: int = 400) -> str:'
new5 = 'def build_tile_svg(analysis: dict, tile_size: int = 400, motief_schaal: int = 100) -> str:'
old6 = '    complexity = analysis.get("complexity", "medium")'
new6 = '    complexity = analysis.get("complexity", "medium")\n    tile_size = int(tile_size / (motief_schaal / 100.0))'
if 'motief_schaal' not in code:
    code = code.replace(old3, new3).replace(old4, new4).replace(old5, new5).replace(old6, new6)
    open('app.py','w').write(code)
    print('backend klaar')
else:
    print('backend al aanwezig')
