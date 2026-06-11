code = open('app.py').read()
# Zoek de exacte importregel
for i, line in enumerate(code.split('\n')):
    if 'modules_extra' in line:
        print(f'regel {i}: {line}')
