js = open('static/js/app.js').read()
old = '"repeat_type": repeat_type,'
new = '"repeat_type": repeat_type,\n      "motief_schaal": parseInt(document.getElementById("motiefSchaal")?.value || "100"),'
if 'motief_schaal' not in js:
    js = js.replace(old, new)
    open('static/js/app.js','w').write(js)
    print('JS fix klaar')
else:
    print('al aanwezig')
