content = open('app.py').read()

old1 = "from email.mime.multipart import MIMEMultipart"
new1 = "from email.mime.multipart import MIMEMultipart\nfrom email.mime.image import MIMEImage\nimport base64"

old2 = "        msg.attach(MIMEText(html, 'html'))\n        server = smtplib.SMTP_SSL"
new2 = """        msg.attach(MIMEText(html, 'html'))

        # Voeg dessin toe als bijlage
        img_b64 = data.get('img_b64', '')
        if img_b64:
            try:
                img_data = base64.b64decode(img_b64)
                img = MIMEImage(img_data, name='dessin.png')
                img.add_header('Content-Disposition', 'attachment', filename='dessin.png')
                msg.attach(img)
            except Exception as e:
                print(f"Bijlage fout: {e}")

        server = smtplib.SMTP_SSL"""

if old1 in content and "MIMEImage" not in content:
    content = content.replace(old1, new1)
    print("Imports toegevoegd!")

if old2 in content:
    content = content.replace(old2, new2)
    print("Bijlage code toegevoegd!")
else:
    print("Bijlage positie niet gevonden")

open('app.py', 'w').write(content)
