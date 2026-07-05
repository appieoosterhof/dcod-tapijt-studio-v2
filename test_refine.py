#!/usr/bin/env python3
"""
TESTVERSIE — losstaand van de webapp.
Test of de AI vrije tekst ("maak de aders 30% breder") correct kan vertalen
naar een parameter-aanpassing, zonder dat dit al gekoppeld is aan de
Dessinator of aan modules_extra.py.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 test_refine.py "maak de aders 30% breder"

Vraagt om je Claude API-sleutel (dezelfde die je ook in de Dessinator gebruikt).
"""
import sys
import os
import json
import getpass
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("FOUT: het 'anthropic' package is niet geinstalleerd in deze omgeving.")
    print("Dit hoort al aanwezig te zijn omdat de Dessinator het ook gebruikt.")
    sys.exit(1)


def lees_api_key():
    """Leest de API-sleutel uit api_key.txt als dat bestaat, anders via prompt."""
    key_file = Path("api_key.txt")
    if key_file.exists():
        key = key_file.read_text(encoding="utf-8").strip()
        if key:
            print(f"API-sleutel gelezen uit {key_file} (lengte: {len(key)} tekens)")
            return key
    return getpass.getpass("Plak je Claude API-sleutel (niet zichtbaar tijdens typen): ").strip()


SYSTEM_INSTRUCTIE = """Je bent een assistent die vrije-tekst-instructies voor een
tapijtdessin vertaalt naar EEN parameter-aanpassing. Je verzint GEEN nieuwe
stijl en GEEN nieuw kleurenpalet. Je past alleen bestaande parameters aan.

Geef ALLEEN een JSON-object terug (geen uitleg, geen markdown), met dit exacte format:

{
  "lw_factor": 1.3,
  "toelichting_nl": "Korte uitleg van wat je hebt aangepast en waarom"
}

Regels voor lw_factor (lijndikte-vermenigvuldiger):
- 1.0 = ongewijzigd (standaard dikte)
- Groter dan 1.0 = dikkere lijnen (bv. "30% breder" -> 1.3)
- Kleiner dan 1.0 = dunnere lijnen (bv. "de helft dunner" -> 0.5)
- Blijf binnen het bereik 0.3 tot 3.0, ook als de gebruiker iets extremers vraagt
- Als de instructie niets met lijndikte te maken heeft, geef dan lw_factor: 1.0
  en leg in toelichting_nl uit dat dit (nog) niet ondersteund wordt.
"""


def main():
    if len(sys.argv) < 2:
        print('Gebruik: python3 test_refine.py "maak de aders 30% breder"')
        sys.exit(1)

    instructie = " ".join(sys.argv[1:])
    print(f"Instructie: {instructie}")
    print()

    api_key = lees_api_key()
    if not api_key:
        print("FOUT: geen API-sleutel opgegeven.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print()
    print("Bezig met AI-aanroep (claude-haiku-4-5-20251001)...")
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=SYSTEM_INSTRUCTIE,
            messages=[{"role": "user", "content": instructie}],
        )
    except Exception as e:
        print(f"FOUT bij AI-aanroep: {e}")
        sys.exit(1)

    ruwe_tekst = message.content[0].text.strip()
    print()
    print("Ruwe AI-respons:")
    print(ruwe_tekst)
    print()

    # AI verpakt het antwoord soms in een markdown-codeblok (```json ... ```)
    # ondanks de instructie dat niet te doen. Strip dat hier weg.
    schoon = ruwe_tekst.strip()
    if schoon.startswith("```"):
        schoon = schoon.split("\n", 1)[1] if "\n" in schoon else schoon
        if schoon.rstrip().endswith("```"):
            schoon = schoon.rstrip()[:-3]
        schoon = schoon.strip()
        if schoon.startswith("json"):
            schoon = schoon[4:].strip()

    try:
        resultaat = json.loads(schoon)
    except json.JSONDecodeError:
        print("FOUT: AI gaf geen geldige JSON terug. Zie ruwe respons hierboven.")
        sys.exit(1)

    lw_factor = resultaat.get("lw_factor")
    toelichting = resultaat.get("toelichting_nl", "")

    print("Geparsed resultaat:")
    print(f"  lw_factor: {lw_factor}")
    print(f"  toelichting: {toelichting}")
    print()

    if not isinstance(lw_factor, (int, float)):
        print("WAARSCHUWING: lw_factor is geen getal, zou niet toepasbaar zijn.")
    elif not (0.3 <= lw_factor <= 3.0):
        print(f"WAARSCHUWING: lw_factor {lw_factor} valt buiten het verwachte bereik 0.3-3.0.")
    else:
        print("OK: lw_factor valt binnen het verwachte bereik en is klaar om toe te passen.")


if __name__ == "__main__":
    main()
