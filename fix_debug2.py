code = open('app.py').read()
old = '    motief_schaal = int(data.get("motief_schaal", 100))\n    repeat_type = data.get("repeat_type", "full")'
new = '    motief_schaal = int(data.get("motief_schaal", 100))\n    print(f"DEBUG schaal: {motief_schaal}")\n    repeat_type = data.get("repeat_type", "full")'
code = code.replace(old, new)
open('app.py','w').write(code)
print('klaar')
