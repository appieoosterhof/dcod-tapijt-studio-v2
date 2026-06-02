code = open('app.py').read()

# Voeg gradient overlay toe aan build_repeat_svg
old = '''  <g clip-path="url(#canvas)">{"".join(tiles)}</g>
</svg>'''

new = '''  <g clip-path="url(#canvas)">{"".join(tiles)}</g>
  <defs>
    <linearGradient id="globalGrad" x1="0" y1="0" x2="0" y2="1">
      {grad_stops}
    </linearGradient>
  </defs>
  <rect width="{total_w}" height="{total_h}" fill="url(#globalGrad)" opacity="0.35" clip-path="url(#canvas)"/>
</svg>'''

# Bouw gradient stops uit palet
old2 = "    svg = f\"\"\"<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
new2 = """    # Bouw gradient stops
    pal = analysis.get('palette', {})
    colors = [pal.get('primary','#ffffff'), pal.get('secondary','#ffffff'), 
              pal.get('accent1','#ffffff'), pal.get('accent2','#ffffff')]
    grad_stops = ''
    for i, c in enumerate(colors):
        pct = int(i / (len(colors)-1) * 100)
        grad_stops += f'<stop offset="{pct}%" stop-color="{c}" stop-opacity="0.4"/>'
    
    svg = f\"\"\"<?xml version=\"1.0\" encoding=\"UTF-8\\\">"""

if 'globalGrad' not in code:
    code = code.replace(old, new)
    code = code.replace(old2, new2)
    open('app.py','w').write(code)
    print('gradient overlay toegevoegd')
else:
    print('al aanwezig')
