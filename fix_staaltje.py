content = open('templates/index.html').read()

old = '    <div id="bestelFout"'
new = '''    <div style="margin-bottom:16px;">
      <label style="display:block;font-size:12px;font-weight:bold;margin-bottom:8px;">STAALTJE AANVRAGEN</label>
      <label style="display:flex;align-items:center;gap:10px;cursor:pointer;font-size:15px;">
        <input type="checkbox" id="bestelSaaltje" style="width:18px;height:18px;accent-color:#4A7C3F;">
        Ja, stuur mij een gratis staaltje toe
      </label>
      <div id="bestelAdresVeld" style="display:none;margin-top:12px;">
        <label style="display:block;font-size:12px;color:#666;margin-bottom:6px;">AFLEVERADRES STAALTJE</label>
        <input id="bestelAdres" type="text" placeholder="Straat + huisnummer, postcode, plaats" style="width:100%;padding:10px;border:1px solid #ddd;border-radius:8px;font-size:15px;box-sizing:border-box;"/>
      </div>
    </div>
    <div id="bestelFout"'''

content = content.replace(old, new)
open('templates/index.html', 'w').write(content)
print("Stap 2 klaar!")
