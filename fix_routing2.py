code = open('app.py').read()
old = '    style = analysis.get("style", "geometric")'
new = '''    style = analysis.get("style", "geometric")
    p = prompt.lower()
    if any(w in p for w in ["streep", "strepen", "stripe", "verticale lijn"]):
        style = "strepen"
    elif any(w in p for w in ["mozaiek", "mozaiek", "pixel", "blokje"]):
        style = "mozaiek"
    elif any(w in p for w in ["chevron", "zigzag"]):
        style = "chevron"
    elif any(w in p for w in ["hexagoon", "honingraat", "zeshoek"]):
        style = "hexagoon"
    elif any(w in p for w in ["ogee", "schub", "dakpan"]):
        style = "ogee"
    elif any(w in p for w in ["diamant", "concentrisch"]):
        style = "diamant"
    elif any(w in p for w in ["terrazzo", "steensnipp"]):
        style = "terrazzo"
    elif any(w in p for w in ["vrije vorm", "organisch", "vloeiend"]):
        style = "vrije_vormen"'''
if 'p = prompt.lower()' not in code:
    code = code.replace(old, new)
    open('app.py','w').write(code)
    print('routing klaar')
else:
    print('al aanwezig')
