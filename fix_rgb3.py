import re

content = open('/Users/abmac/Desktop/tapijt-studio/templates/index.html').read()

# Vervang de smalle input stijl door bredere
old = 'width:100%;padding:2px;border:1px solid #ddd;border-radius:4px;font-size:10px;text-align:center;'
new = 'width:100%;padding:4px 2px;border:1px solid #ddd;border-radius:4px;font-size:11px;text-align:center;'

count = content.count(old)
print(f"Gevonden: {count}x")
content = content.replace(old, new)

# Maak de R/G/B labels iets groter
old2 = 'font-size:9px;color:#999;margin-bottom:2px;'
new2 = 'font-size:10px;color:#666;font-weight:bold;margin-bottom:3px;'

content = content.replace(old2, new2)

open('/Users/abmac/Desktop/tapijt-studio/templates/index.html', 'w').write(content)
print("RGB velden vergroot!")
