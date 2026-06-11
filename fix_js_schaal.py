js = open('static/js/app.js').read()
# Zoek de exacte regel
for i, line in enumerate(js.split('\n')):
    if 'motief_schaal' in line or 'motiefSchaal' in line:
        print(f'regel {i}: {line}')
