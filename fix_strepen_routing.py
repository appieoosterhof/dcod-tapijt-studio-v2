code = open('app.py').read()

# Fix 1: AI prompt uitbreiden met betere instructie voor strepen
old = '"style": "geometric|floral|medallion|tribal|abstract|botanical|nordic|persian|strepen|mozaiek|chevron|hexagoon|ogee|diamant|terrazzo|vrije_vormen",'
new = '"style": "geometric|floral|medallion|tribal|abstract|botanical|nordic|persian|strepen|mozaiek|chevron|hexagoon|ogee|diamant|terrazzo|vrije_vormen",\n\nBELANGRIJK voor stijl-herkenning:\n- "strepen", "streep", "stripe", "verticale lijnen", "horizontale lijnen" → style: "strepen"\n- "mozaiek", "pixels", "blokjes", "rechthoekjes" → style: "mozaiek"\n- "chevron", "zigzag", "pijl" → style: "chevron"\n- "hexagoon", "honingraat", "zeshoek" → style: "hexagoon"\n- "ogee", "schubben", "dakpan" → style: "ogee"\n- "diamant", "ruit", "concentrisch" → style: "diamant"\n- "terrazzo", "steensnippers" → style: "terrazzo"\n- "vrije vormen", "organisch", "vloeiend" → style: "vrije_vormen"'

if 'BELANGRIJK voor stijl-herkenning' not in code:
    code = code.replace(old, new)

# Fix 2: directe keyword routing in build_tile_svg vóór AI stijl
old2 = '    style = analysis.get("style", "geometric")'
new2 = '''    style = analysis.get("style", "geometric")
    # Directe keyword override op basis van prompt
    prompt_lower = analysis.get("description_nl", "").lower()
    if any(w in prompt_lower for w in ["streep", "strepen", "stripe", "verticale lijn"]):
        style = "strepen"
    elif any(w in prompt_lower for w in ["mozaiek", "pixel", "blokje"]):
        style = "mozaiek"
    elif any(w in prompt_lower for w in ["chevron", "zigzag", "pijl"]):
        style = "chevron"
    elif any(w in prompt_lower for w in ["hexagoon", "honingraat", "zeshoek"]):
        style = "hexagoon"
    elif any(w in prompt_lower for w in ["ogee", "schub", "dakpan"]):
        style = "ogee"
    elif any(w in prompt_lower for w in ["diamant", "concentrisch"]):
        style = "diamant"
    elif any(w in prompt_lower for w in ["terrazzo", "steensnipp"]):
        style = "terrazzo"
    elif any(w in prompt_lower for w in ["vrije vorm", "organisch", "vloeiend"]):
        style = "vrije_vormen"'''

if 'keyword override' not in code:
    code = code.replace(old2, new2)

open('app.py','w').write(code)
print('strepen routing gefixed')
