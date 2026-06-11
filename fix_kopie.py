content = open('app.py').read()

kopie_code = '''
        # Kopie naar aanvrager
        if email:
            msg_kopie = MIMEMultipart("alternative")
            msg_kopie["Subject"] = "Uw offerte aanvraag bij DCOD Printtapijt"
            msg_kopie["From"] = "appieoosterhof@gmail.com"
            msg_kopie["To"] = email
            html_kopie = f"""<html><body style="font-family:Arial;">
            <h2 style="color:#4A7C3F;">Bedankt voor uw aanvraag!</h2>
            <p>Beste {naam},</p>
            <p>Wij hebben uw aanvraag ontvangen en nemen binnen 2 werkdagen contact met u op.</p>
            <table style="border-collapse:collapse;width:100%">
            <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Product</td><td style="padding:8px">{product}</td></tr>
            <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Afmeting</td><td style="padding:8px">{afmeting}</td></tr>
            <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Dessin</td><td style="padding:8px">{dessin_info}</td></tr>
            <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Wensen</td><td style="padding:8px">{wensen}</td></tr>
            </table>
            <br><p>Met vriendelijke groet,<br><strong>DCOD Printtapijt</strong><br>www.dcod-printtapijt.nl</p>
            </body></html>"""
            msg_kopie.attach(MIMEText(html_kopie, "html"))
            server.sendmail("appieoosterhof@gmail.com", [email], msg_kopie.as_string())
'''

old = '        server.quit()'
new = kopie_code + '        server.quit()'

if old in content:
    open('app.py', 'w').write(content.replace(old, new, 1))
    print("Kopie mail toegevoegd!")
else:
    print("Niet gevonden")
