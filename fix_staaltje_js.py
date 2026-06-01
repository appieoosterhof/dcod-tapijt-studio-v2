content = open('static/js/app.js').read()

old = "// M2 berekening"
new = """// Staaltje tonen/verbergen
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('bestelSaaltje')?.addEventListener('change', function() {
    document.getElementById('bestelAdresVeld').style.display = this.checked ? 'block' : 'none';
  });
});

// M2 berekening"""

content = content.replace(old, new)

# Voeg staaltje toe aan verzenddata
old2 = "      body: JSON.stringify({ naam, email, telefoon, wensen, dessin_info, product, afmeting:"
new2 = """      const staaltje = document.getElementById('bestelSaaltje')?.checked ? 'Ja' : 'Nee';
      const adres = document.getElementById('bestelAdres')?.value || '';
      body: JSON.stringify({ naam, email, telefoon, wensen, dessin_info, product, afmeting:"""

content = content.replace(old2, new2)

old3 = "afmeting: breedte && lengte ? breedte + ' x ' + lengte + ' cm (' + m2 + ')' : 'Niet opgegeven' })"
new3 = "afmeting: breedte && lengte ? breedte + ' x ' + lengte + ' cm (' + m2 + ')' : 'Niet opgegeven', staaltje, adres })"

content = content.replace(old3, new3)
open('static/js/app.js', 'w').write(content)
print("Stap 3 klaar!")
