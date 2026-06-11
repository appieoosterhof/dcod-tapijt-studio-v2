content = open('app.py').read()

old = '  {"".join(tiles)}'
new = '  <g clip-path="url(#canvas)">{"".join(tiles)}</g>'

if old in content:
    open('app.py', 'w').write(content.replace(old, new))
    print("Fix toegepast!")
else:
    print("Niet gevonden - zoeken...")
    idx = content.find('join(tiles)')
    print(content[idx-50:idx+50])
