code = open('app.py').read()
old1 = '        analysis = analyse_prompt(prompt, api_key)'
new1 = '        analysis = analyse_prompt(prompt, api_key)\n        analysis["_prompt"] = prompt.lower()'
old2 = '    style = analysis.get("style", "geometric")'
new2 = '''    style = analysis.get("style", "geometric")
    p = analysis.get("_prompt", "")
    if any(w in p for w in ["streep", "strepen", "stripe"]):
        style = "strepen"
    elif any(w in p for w in ["mozaiek", "pixel", "blokje"]):
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
if '_prompt' not in code:
    code = code.replace(old1, new1)
if 'analysis.get("_prompt"' not in code:
    code = code.replace(old2, new2)
open('app.py','w').write(code)
print('klaar')
