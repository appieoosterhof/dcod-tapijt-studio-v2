code = open('app.py').read()
old = '    motief_schaal = int(data.get("motief_schaal", 100))\n    try:\n        # Stap 1: AI analyse'
new = '    motief_schaal = int(data.get("motief_schaal", 100))\n    print(f"DEBUG schaal ontvangen: {motief_schaal}")\n    try:\n        # Stap 1: AI analyse'
code = code.replace(old, new)
open('app.py','w').write(code)
print('debug toegevoegd')
