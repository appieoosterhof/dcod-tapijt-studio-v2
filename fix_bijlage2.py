content = open('app.py').read()

old = """        # Voeg dessin toe als bijlage
        img_b64 = data.get('img_b64', '')
        if img_b64:
            try:
                img_data = base64.b64decode(img_b64)
                img = MIMEImage(img_data, name='dessin.png')
                img.add_header('Content-Disposition', 'attachment', filename='dessin.png')
                msg.attach(img)
            except Exception as e:
                print(f"Bijlage fout: {e}")"""

new = """        # Voeg dessin toe als bijlage
        img_b64 = data.get('img_b64', '')
        if img_b64:
            try:
                img_data = base64.b64decode(img_b64)
                img = MIMEImage(img_data, _subtype='png', name='dessin.png')
                img.add_header('Content-Disposition', 'attachment', filename='dessin.png')
                msg.attach(img)
            except Exception as e:
                print(f"Bijlage fout: {e}")"""

if old in content:
    open('app.py', 'w').write(content.replace(old, new))
    print("Fix toegepast!")
else:
    print("Niet gevonden")
