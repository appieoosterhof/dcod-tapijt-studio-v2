content = open('static/js/app.js').read()

old = """  const previewImg = document.getElementById('previewRepeat');
  const img_b64 = previewImg?.src?.includes('data:image') ? previewImg.src.split(',')[1] : '';"""

new = """  let img_b64 = '';
  try {
    const canvas = document.createElement('canvas');
    const previewImg = document.getElementById('previewRepeat');
    if (previewImg && previewImg.naturalWidth > 0) {
      canvas.width = previewImg.naturalWidth;
      canvas.height = previewImg.naturalHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(previewImg, 0, 0);
      img_b64 = canvas.toDataURL('image/png').split(',')[1];
    }
  } catch(e) { console.log('Afbeelding niet beschikbaar:', e); }"""

if old in content:
    open('static/js/app.js', 'w').write(content.replace(old, new))
    print("JavaScript bijgewerkt!")
else:
    print("Niet gevonden")
    idx = content.find('img_b64')
    print(content[idx-50:idx+100])
