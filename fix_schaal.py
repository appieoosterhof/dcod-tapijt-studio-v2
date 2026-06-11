html = open('templates/index.html').read()

old = '<div class="field">\n          <label>Repeat type</label>'
new = '''<div class="field">
          <label>Motief grootte (%)</label>
          <div style="display:flex;align-items:center;gap:8px;">
            <input type="number" id="motiefSchaal" value="100" min="25" max="400" step="5"
              style="width:90px;padding:8px;border:1px solid #ddd;border-radius:6px;font-size:14px;text-align:center;">
            <span style="font-size:13px;color:#999;">% &nbsp;(25% = fijn · 100% = normaal · 200% = groot)</span>
          </div>
        </div>
        <div class="field">
          <label>Repeat type</label>'''

if 'motiefSchaal' not in html:
    html = html.replace(old, new)
    open('templates/index.html','w').write(html)
    print('invoerveld toegevoegd')
else:
    print('al aanwezig')
