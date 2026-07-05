#!/usr/bin/env python3
"""
Breidt setPrompt() uit met een optioneel tweede argument: het geklikte
subknop-element. Als dat wordt meegegeven, krijgt die knop de klasse
'sub-active' en verliezen zijn buren (binnen dezelfde ouder) die klasse.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_subknop_active_js.py
Maakt automatisch een timestamped .bak van static/js/app.js
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("static/js/app.js")

OLD = '''function setPrompt(text) {
  document.getElementById('prompt').value = text;
  document.getElementById('prompt').focus();
}'''

NEW = '''function setPrompt(text, btn) {
  document.getElementById('prompt').value = text;
  document.getElementById('prompt').focus();
  if (btn && btn.parentElement) {
    btn.parentElement.querySelectorAll('.chip').forEach(function(el){ el.classList.remove('sub-active'); });
    btn.classList.add('sub-active');
  }
}'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    count = content.count(OLD)
    if count == 0:
        print("FOUT: de verwachte oude setPrompt-functie is niet exact gevonden.")
        sys.exit(1)
    if count > 1:
        print(f"FOUT: komt {count}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"app.js.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")
    print("app.js aangepast: setPrompt() markeert nu de geklikte subknop als actief")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -n "sub-active" static/js/app.js')


if __name__ == "__main__":
    main()
