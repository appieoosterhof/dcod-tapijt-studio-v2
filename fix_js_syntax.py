content = open('static/js/app.js').read()

old = """    const res = await fetch('/api/bestelling', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      const staaltje = document.getElementById('bestelSaaltje')?.checked ? 'Ja' : 'Nee';
      const adres = document.getElementById('bestelAdres')?.value || '';
      body: JSON.stringify({ naam, email, telefoon, wensen, dessin_info, product, afmeting: breedte && lengte ? breedte + ' x ' + lengte + ' cm (' + m2 + ')' : 'Niet opgegeven', staaltje, adres })
    });"""

new = """  const staaltje = document.getElementById('bestelSaaltje')?.checked ? 'Ja' : 'Nee';
  const adres = document.getElementById('bestelAdres')?.value || '';
  const res = await fetch('/api/bestelling', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ naam, email, telefoon, wensen, dessin_info, product, afmeting: breedte && lengte ? breedte + ' x ' + lengte + ' cm (' + m2 + ')' : 'Niet opgegeven', staaltje, adres })
    });"""

if old in content:
    open('static/js/app.js', 'w').write(content.replace(old, new))
    print("Fix toegepast!")
else:
    print("Niet gevonden")
