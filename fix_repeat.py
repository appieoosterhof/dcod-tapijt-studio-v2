content = open('app.py').read()
old = '''    for r in range(-1, rows + 2):
        for c in range(-1, cols + 2):'''
if old in content:
    print("Nieuwe versie al aanwezig")
else:
    old2 = '''    for r in range(rows + 2):
        for c in range(cols + 2):'''
    new = content.replace(old2, '''    for r in range(-1, rows + 2):
        for c in range(-1, cols + 2):''')
    new = new.replace(
        '            elif repeat_type == "half-drop":\n                y += (c % 2) * (T // 2)\n                y -= T // 2',
        '            elif repeat_type == "half-drop":\n                y += (c % 2) * (T // 2)'
    )
    open('app.py', 'w').write(new)
    print("Fix toegepast")
