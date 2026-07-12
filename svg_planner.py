"""
BUILD-014 -- SVG Planner.

Implementeert de SVG Planner conform de goedgekeurde ontwerpbaseline
(BUILD-014 functioneel + technisch/TD-004). De SVG Planner is de reeds erkende,
UITSLUITEND UITVOERENDE renderer (AB-005/AR-004/AR-005): hij rendert een reeds
bevestigd patroon deterministisch tot een SVG. Hij voegt GEEN ontwerpkeuze toe
en draagt geen ontwerpautoriteit.

Kernprincipes (technisch geborgd, conform TD-004):
  * uitvoerende renderer, geen ontwerpcomponent; leest uitsluitend;
  * het SVG-resultaat heeft GEEN eigen Voorgesteld/Bevestigd-status -- het is
    uitsluitend een deterministische rendering van het bevestigde Pattern
    Profile; zijn geldigheid volgt uit dat Pattern Profile (stale-detectie);
  * AI-model-onafhankelijk: de rendering loopt via een injecteerbare
    SVG Rendering Boundary zonder ontwerplogica (de standaard omhult de
    bestaande pipeline uit AB-005; hier een deterministische placeholder voor
    test); geen LLM, geen promptteksten;
  * viervoudige deterministische preconditie: bevestigd Concept
    (Concept.status == "bevestigd"), bevestigd Floor Design, bevestigd Material
    Profile en bevestigd Pattern Profile (status == "Bevestigd").

Volledig additief en losstaand: GEEN wijziging aan design_context.py,
reasoning_engine.py, material_planner.py, pattern_planner.py of de bestaande
pipeline (app.py/modules_extra.py). Nog NIET geimplementeerd: Floor
Visualization Engine, Design Transfer Package, overige downstream-componenten
en aanvullende persistentie.
"""

from __future__ import annotations

import copy
import html
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

from design_context import Concept, DesignContext
from reasoning_engine import FloorDesign
from material_planner import MaterialProfile
from pattern_planner import PatternProfile


# ─── SVG Rendering Boundary (AI-model-onafhankelijk, deterministisch) ────────
#
# Contract: een functie die een platte render-invoer-dict ontvangt (projectie
# van de bevestigde objecten) en een SVG-string retourneert. Bevat GEEN
# ontwerplogica -- puur render in, SVG uit. De standaard-implementatie kan de
# bestaande pipeline (build_tile_svg/build_repeat_svg, AB-005) omhullen; hier
# een deterministische placeholder.

SVGRenderFunctie = Callable[[dict], str]


def placeholder_svg_rendering(invoer: dict) -> str:
    """Deterministische placeholder voor de SVG Rendering Boundary.

    Geen LLM-aanroep, geen promptteksten, geen willekeur: gelijke invoer levert
    exact dezelfde SVG. Rendert een eenvoudige 400px-tegel (naadloze-tegeling-
    conventie) op basis van het kleurpalet en de motiefstructuur. Gebruikt geen
    clipPath (Safari-valkuil).
    """
    palet = invoer.get("kleurpalet") or {}
    achtergrond = palet.get("achtergrond") or palet.get("primary") or "#f5f5f0"
    voorgrond = palet.get("primary") or "#8a8a7a"
    motief = html.escape(str(invoer.get("motiefstructuur") or "patroon"))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">'
        f'<rect width="400" height="400" fill="{achtergrond}"/>'
        f'<circle cx="200" cy="200" r="120" fill="{voorgrond}"/>'
        f'<text x="200" y="384" text-anchor="middle" font-size="12" fill="{voorgrond}">{motief}</text>'
        "</svg>"
    )


@dataclass
class SVGResultaat:
    """Technisch resultaat-object van de SVG Planner -- BUITEN de DesignContext.

    Draagt GEEN eigen bevestigingsstatus (TD-004): het is een deterministische
    rendering van het bevestigde Pattern Profile, met een weergave-motivering en
    herkomst-referenties naar de vier bevestigde bronobjecten.
    """

    identifier: str
    svg: str
    weergave_motivering: str
    concept_herkomst: dict
    floor_design_herkomst: dict
    material_profile_herkomst: dict
    pattern_profile_herkomst: dict
    kwaliteitsinformatie: dict = field(default_factory=dict)


@dataclass
class SVGResultaatWikkel:
    """Technische returnvorm: een SVG-resultaat, of uitsluitend signaleringen
    wanneer de SVG Planner niet mag of kan renderen."""

    svg_resultaat: Optional[SVGResultaat] = None
    signaleringen: list[str] = field(default_factory=list)
    kwaliteitsinformatie: dict = field(default_factory=dict)

    @property
    def geslaagd(self) -> bool:
        return self.svg_resultaat is not None


class SVGPlanner:
    """Publieke component (BUILD-014) -- uitsluitend uitvoerende renderer.

    `render(dc, floor_design, material_profile, pattern_profile)` rendert het
    bevestigde Pattern Profile deterministisch tot een SVG. Leest alle invoer
    uitsluitend; wijzigt niets, beslist niets en bevestigt nooit. Het resultaat
    draagt geen eigen status.
    """

    STATUS_CONCEPT_BEVESTIGD = "bevestigd"           # laag 4 (Concept)
    STATUS_FLOOR_DESIGN_BEVESTIGD = "Bevestigd"      # Floor Design (AB-006)
    STATUS_MATERIAL_PROFILE_BEVESTIGD = "Bevestigd"  # Material Profile (AB-010)
    STATUS_PATTERN_PROFILE_BEVESTIGD = "Bevestigd"   # Pattern Profile (AB-011)
    _VERPLICHTE_CONCEPT_VELDEN = ("stijlfamilie", "kleurpalet", "complexiteit", "motiefschaal")
    MAX_RENDER_POGINGEN = 3

    def __init__(self, render: SVGRenderFunctie = placeholder_svg_rendering) -> None:
        # De SVG Rendering Boundary is injecteerbaar; standaard de placeholder.
        self._render = render

    # ── Orkestratie ───────────────────────────────────────────────────────────
    def render(
        self,
        dc: DesignContext,
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        pattern_profile: PatternProfile,
    ) -> SVGResultaatWikkel:
        """Orkestreert de render-keten: gate -> projectie -> rendering ->
        validatie -> verpakken. Leest alle invoer uitsluitend."""
        # 1. Viervoudige deterministische gate.
        signaleringen = self._valideer_preconditie(dc, floor_design, material_profile, pattern_profile)
        if signaleringen:
            return SVGResultaatWikkel(signaleringen=signaleringen)

        invoer = self._verzamel_render_invoer(dc, floor_design, material_profile, pattern_profile)
        herkomsten = (
            self._concept_snapshot(dc.concept),
            self._object_snapshot(floor_design),
            self._object_snapshot(material_profile),
            self._object_snapshot(pattern_profile),
        )
        laatste_afkeur: list[str] = []

        # 2-4. Rendering + validatie, met gelimiteerde re-render.
        for poging in range(1, self.MAX_RENDER_POGINGEN + 1):
            try:
                svg = self._render(invoer)
            except Exception as fout:  # boundary is injecteerbaar en onbekend
                return SVGResultaatWikkel(
                    signaleringen=[f"Technische fout in de SVG Rendering Boundary: {fout}"]
                )

            laatste_afkeur = self._valideer_svg(svg)
            if not laatste_afkeur:
                resultaat = self._bouw_svg_resultaat(svg, *herkomsten, poging=poging)
                return SVGResultaatWikkel(
                    svg_resultaat=resultaat,
                    kwaliteitsinformatie={"pogingen": poging, "geldig": True},
                )

        # 5. Re-renderlimiet bereikt -> geen geldig resultaat, geen mutatie.
        return SVGResultaatWikkel(
            signaleringen=(
                [f"Geen geldige SVG na {self.MAX_RENDER_POGINGEN} pogingen."] + laatste_afkeur
            ),
            kwaliteitsinformatie={"pogingen": self.MAX_RENDER_POGINGEN},
        )

    # ── Stale-detectie (TD-004 §5) ────────────────────────────────────────────
    @staticmethod
    def is_stale(svg_resultaat: SVGResultaat, pattern_profile: PatternProfile) -> bool:
        """True wanneer het SVG-resultaat niet meer bij het (huidige) bevestigde
        Pattern Profile hoort en dus opnieuw moet worden gerenderd."""
        return svg_resultaat.pattern_profile_herkomst.get("identifier") != pattern_profile.identifier

    # ── Preconditie (viervoudige deterministische gate) ───────────────────────
    def _valideer_preconditie(
        self,
        dc: DesignContext,
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        pattern_profile: PatternProfile,
    ) -> list[str]:
        signaleringen: list[str] = []

        if dc.concept.status != self.STATUS_CONCEPT_BEVESTIGD:
            signaleringen.append(
                'Concept is niet bevestigd; SVG Planner rendert niet '
                '(vereist Concept.status == "bevestigd").'
            )
        else:
            for veld in self._VERPLICHTE_CONCEPT_VELDEN:
                waarde = getattr(dc.concept, veld)
                if waarde is None or (isinstance(waarde, str) and not waarde.strip()):
                    signaleringen.append(f"Bevestigd Concept mist verplicht veld: {veld}.")

        signaleringen += self._valideer_bevestigd(
            floor_design, self.STATUS_FLOOR_DESIGN_BEVESTIGD, "Floor Design"
        )
        signaleringen += self._valideer_bevestigd(
            material_profile, self.STATUS_MATERIAL_PROFILE_BEVESTIGD, "Material Profile"
        )
        signaleringen += self._valideer_bevestigd(
            pattern_profile, self.STATUS_PATTERN_PROFILE_BEVESTIGD, "Pattern Profile"
        )
        return signaleringen

    @staticmethod
    def _valideer_bevestigd(obj, verwachte_status: str, naam: str) -> list[str]:
        if obj is None:
            return [f"Geen {naam} meegegeven."]
        if getattr(obj, "status", None) != verwachte_status:
            return [f'{naam} is niet bevestigd; SVG Planner rendert niet '
                    f'(vereist status == "{verwachte_status}").']
        if not getattr(obj, "identifier", None):
            return [f"Bevestigd {naam} is niet identificeerbaar."]
        return []

    # ── Render-invoer projecteren ─────────────────────────────────────────────
    @staticmethod
    def _verzamel_render_invoer(
        dc: DesignContext,
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        pattern_profile: PatternProfile,
    ) -> dict:
        c = dc.concept
        return {
            "kleurpalet": c.kleurpalet,
            "stijlfamilie": c.stijlfamilie,
            "complexiteit": c.complexiteit,
            "ontwerprichting": floor_design.ontwerprichting,
            "structuur": material_profile.structuur,
            "pooltype": material_profile.pooltype,
            "uitstraling": material_profile.uitstraling,
            "motiefstructuur": pattern_profile.motiefstructuur,
            "motiefschaal": pattern_profile.motiefschaal,
            "dichtheid": pattern_profile.dichtheid,
            "herhalingskarakter": pattern_profile.herhalingskarakter,
        }

    # ── Herkomst-referenties (traceerbaarheid) ────────────────────────────────
    @staticmethod
    def _concept_snapshot(concept: Concept) -> dict:
        return {
            "stijlfamilie": concept.stijlfamilie,
            # Defensieve kopie: kleurpalet is een mutabele dict; een snapshot moet
            # bevroren blijven ook als het bron-Concept later zou wijzigen.
            "kleurpalet": copy.deepcopy(concept.kleurpalet),
            "complexiteit": concept.complexiteit,
            "motiefschaal": concept.motiefschaal,
            "status": concept.status,
        }

    @staticmethod
    def _object_snapshot(obj) -> dict:
        """Enkelvoudige herkomst-snapshot van een resultaat-object."""
        return {"identifier": getattr(obj, "identifier", None), "status": getattr(obj, "status", None)}

    # ── Validatie van het SVG-artefact ────────────────────────────────────────
    @staticmethod
    def _valideer_svg(svg) -> list[str]:
        if not isinstance(svg, str) or not svg.strip():
            return ["Rendering leverde geen geldige SVG-string."]
        if "<svg" not in svg or "</svg>" not in svg:
            return ["SVG-artefact is niet welgevormd (mist <svg>/</svg>)."]
        return []

    # ── SVG-resultaat bouwen (buiten de DesignContext, geen eigen status) ─────
    @staticmethod
    def _bouw_svg_resultaat(
        svg: str,
        concept_herkomst: dict,
        floor_design_herkomst: dict,
        material_profile_herkomst: dict,
        pattern_profile_herkomst: dict,
        poging: int,
    ) -> SVGResultaat:
        return SVGResultaat(
            identifier=str(uuid.uuid4()),
            svg=svg,
            weergave_motivering=(
                "Getrouwe deterministische rendering van het bevestigde Pattern "
                "Profile; geen ontwerpkeuze toegevoegd."
            ),
            concept_herkomst=concept_herkomst,
            floor_design_herkomst=floor_design_herkomst,
            material_profile_herkomst=material_profile_herkomst,
            pattern_profile_herkomst=pattern_profile_herkomst,
            kwaliteitsinformatie={"geldig": True, "poging": poging},
        )
