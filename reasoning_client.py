"""
reasoning_client.py — Gedeelde reasoning-client (IMP-015).

Vendor-agnostische MODEL-POORT voor productie-Reasoning Capabilities, plus de
enige leverancier-specifieke adapter. Capabilities (Ontwerpstrategie, en later
Conceptvorming e.v.) kennen UITSLUITEND de abstracte `ModelClient`-interface;
zij bevatten geen leveranciersspecifieke logica (PLATFORM-001 §5, BUILD-024 §5,
REASONING-001 §7).

Kent geen HTTP-endpoints, sessies, opslag, DesignContext of orchestratie. Een
implementatie mag falen (exceptions) — de aanroepende capability vangt dat af en
valt gecontroleerd terug op haar deterministische placeholder (AB-012).
"""

from __future__ import annotations

import json
from typing import Protocol

# Modelkeuze conform de rest van de Dessinator (CLAUDE.md). Uitsluitend hier en
# in de adapter; capabilities noemen nooit een model of leverancier.
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_MAX_TOKENS = 600
DEFAULT_TIMEOUT_S = 30.0


class ModelClient(Protocol):
    """Abstracte reasoning-interface: systeem- + gebruiker-prompt in, ruwe tekst
    uit. Leverancier-onafhankelijk. Implementaties mogen exceptions werpen bij
    netwerk-, timeout-, authenticatie-, rate-limit- of beschikbaarheidsfouten;
    de capability behandelt dat als reden voor gecontroleerde terugval."""

    def genereer(self, systeem: str, gebruiker: str) -> str: ...


class AnthropicModelClient:
    """Enige leverancier-adapter (Anthropic).

    Geen enkele capability importeert deze klasse rechtstreeks; zij wordt
    uitsluitend via de configuratie-factory van een capability gekozen, zodat de
    leverancierskeuze op één plek staat (Configuratie-eis IMP-015). `anthropic`
    wordt lokaal geïmporteerd, zodat de leverancier alleen wordt geraakt wanneer
    de productieclient daadwerkelijk wordt geconstrueerd.
    """

    def __init__(
        self,
        api_sleutel: str,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        timeout: float = DEFAULT_TIMEOUT_S,
    ) -> None:
        import anthropic  # leverancier uitsluitend hier

        self._client = anthropic.Anthropic(api_key=api_sleutel, timeout=timeout)
        self._model = model
        self._max_tokens = max_tokens

    def genereer(self, systeem: str, gebruiker: str) -> str:
        bericht = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=systeem,
            messages=[{"role": "user", "content": gebruiker}],
        )
        return bericht.content[0].text


def extraheer_json(tekst: str) -> dict:
    """Haalt een JSON-object uit modeltekst (verwijdert ```json-hekjes), op
    dezelfde manier als de bestaande Context Interpreter. Werpt bij ongeldige of
    niet-object-JSON — de capability vangt dat af als reden voor terugval."""
    schoon = (tekst or "").strip().replace("```json", "").replace("```", "").strip()
    data = json.loads(schoon)
    if not isinstance(data, dict):
        raise ValueError("Modelantwoord is geen JSON-object.")
    return data
