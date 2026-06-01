content = open('app.py').read()

old = '''    for r in range(rows):
        for c in range(cols):'''

new = '''    for r in range(-1, rows + 1):
        for c in range(-1, cols + 1):'''

if old in content:
    open('app.py', 'w').write(content.replace(old, new))
    print("Fix toegepast!")
else:
    print("Niet gevonden")
