content = open('app.py').read()

old = '<symbol id="tile" viewBox="0 0 {T} {T}" width="{T}" height="{T}" overflow="visible">'
new = '<symbol id="tile" viewBox="0 0 {T} {T}" width="{T}" height="{T}" overflow="hidden">'

if old in content:
    open('app.py', 'w').write(content.replace(old, new))
    print("Fix toegepast!")
else:
    print("Niet gevonden - zoeken...")
    idx = content.find('symbol id="tile"')
    print(content[idx-10:idx+150])
