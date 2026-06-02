code = open('app.py').read()
for i, line in enumerate(code.split('\n')):
    if 'strepen' in line.lower() and 'generate' in line:
        print(f'regel {i}: {line}')
