code = open('static/js/app.js').read()

# Zoek de plek waar het modal geopend wordt en velden ingevuld worden
old = """  const naam = localStorage.getItem('bestel_naam') || '';
  const email = localStorage.getItem('bestel_email') || '';
  const telefoon = localStorage.getItem('bestel_telefoon') || '';"""

new = """  const naam = localStorage.getItem('bestel_naam') || '';
  const email = localStorage.getItem('bestel_email') || '';
  const telefoon = localStorage.getItem('bestel_telefoon') || '';
  const bedrijf = localStorage.getItem('bestel_bedrijf') || '';
  const straat = localStorage.getItem('bestel_straat') || '';
  const postcode = localStorage.getItem('bestel_postcode') || '';
  const plaats = localStorage.getItem('bestel_plaats') || '';
  if (naam) document.getElementById('bestelNaam').value = naam;
  if (email) document.getElementById('bestelEmail').value = email;
  if (telefoon) document.getElementById('bestelTelefoon').value = telefoon;
  if (bedrijf) document.getElementById('bestelBedrijf').value = bedrijf;
  if (straat) document.getElementById('bestelStraat').value = straat;
  if (postcode) document.getElementById('bestelPostcode').value = postcode;
  if (plaats) document.getElementById('bestelPlaats').value = plaats;"""

# Sla ook bedrijf en adres op bij verzenden
old2 = """function slaContactGegevensOp(naam, email, telefoon) {
  localStorage.setItem('bestel_naam', naam);
  localStorage.setItem('bestel_email', email);
  localStorage.setItem('bestel_telefoon', telefoon);"""

new2 = """function slaContactGegevensOp(naam, email, telefoon) {
  localStorage.setItem('bestel_naam', naam);
  localStorage.setItem('bestel_email', email);
  localStorage.setItem('bestel_telefoon', telefoon);
  const b = document.getElementById('bestelBedrijf')?.value || '';
  const s = document.getElementById('bestelStraat')?.value || '';
  const p = document.getElementById('bestelPostcode')?.value || '';
  const pl = document.getElementById('bestelPlaats')?.value || '';
  if (b) localStorage.setItem('bestel_bedrijf', b);
  if (s) localStorage.setItem('bestel_straat', s);
  if (p) localStorage.setItem('bestel_postcode', p);
  if (pl) localStorage.setItem('bestel_plaats', pl);"""

code = code.replace(old, new)
code = code.replace(old2, new2)
open('static/js/app.js','w').write(code)
print('localStorage uitgebreid')
