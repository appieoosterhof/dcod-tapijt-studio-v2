content = open('app.py').read()

# Verwijder de foutieve kopie code
idx_start = content.find("        # Kopie naar aanvrager\n        if email and email != 'administratie@dcod.nl':")
idx_eind = content.find("        server.quit()")

if idx_start > -1 and idx_eind > -1:
    content = content[:idx_start] + content[idx_eind:]
    open('app.py', 'w').write(content)
    print("Foutieve code verwijderd!")
else:
    print("Zoeken...")
    idx = content.find("html_kopie = f")
    print(content[idx-100:idx+50])
