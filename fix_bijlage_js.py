content = open('static/js/app.js').read()

old = "  const dessin_info = document.getElementById('descText')?.textContent || '';"
new = """  const dessin_info = document.getElementById('descText')?.textContent || '';
  const previewImg = document.getElementById('previewRepeat');
  const img_b64 = previewImg?.src?.includes('data:image') ? previewImg.src.split(',')[1] : '';"""

old2 = "body: JSON.stringify({ naam, email, telefoon, wensen, dessin_info, img_b64, product,"
new2 = "body: JSON.stringify({ naam, email, telefoon, wensen, dessin_info, img_b64, product,"

if old in content:
    content = content.replace(old, new)
    print("Afbeelding code toegevoegd!")
else:
    print("Al aanwezig of niet gevonden")

if "body: JSON.stringify({ naam, email, telefoon, wensen, dessin_info, product," in content:
    content = content.replace(
        "body: JSON.stringify({ naam, email, telefoon, wensen, dessin_info, product,",
        "body: JSON.stringify({ naam, email, telefoon, wensen, dessin_info, img_b64, product,"
    )
    print("img_b64 toegevoegd aan verzenddata!")

open('static/js/app.js', 'w').write(content)
