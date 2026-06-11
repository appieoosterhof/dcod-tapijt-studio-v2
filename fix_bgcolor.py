content = open('app.py').read()

old = '    T = 400  # basistegel grootte in SVG units'
new = '''    T = 400  # basistegel grootte in SVG units
    bg_color = analysis.get('background_color', '#F5F5F5')'''

if old in content:
    open('app.py', 'w').write(content.replace(old, new))
    print("Fix toegepast!")
else:
    print("Niet gevonden")
