"""
BUILD-015 -- Floor Visualization Engine (FVE).

Implementeert de Floor Visualization Engine conform de goedgekeurde
ontwerpbaseline (BUILD-015 functioneel + technisch/TD-005). De FVE is de reeds
bestaande, UITSLUITEND UITVOERENDE visualisatiecomponent (BUILD-007/VISION-001):
zij projecteert het gerenderde `SVGResultaat` op de Scene en voegt Floor Design
en Material Profile samen tot één Visualisatie. Zij voegt GEEN ontwerpkeuze toe
en draagt geen ontwerpautoriteit.

Kernprincipes (technisch geborgd, conform TD-005):
  * uitvoerende compositiecomponent, geen ontwerpcomponent; leest uitsluitend;
  * de `Visualisatie` heeft GEEN eigen Voorgesteld/Bevestigd-status (VR-027) --
    zij is een zuivere, deterministische compositie van reeds bevestigde
    bronnen; haar geldigheid volgt uit die bronnen (stale-detectie);
  * AI-model-onafhankelijk: de compositie loopt via een injecteerbare
    Visualization Boundary die de bestaande mockup-/projectie-engine omhult
    (matrix3d-projectie op het vloerpolygon, ROOM_MOCKUPS/floorvisualizer in
    static/js/app.js, AB-005); hier een deterministische placeholder voor test;
    geen LLM, geen promptteksten;
  * viervoudige deterministische gate: een geldig `SVGResultaat`, een bevestigd
    Floor Design (status == "Bevestigd"), een bevestigd Material Profile
    (status == "Bevestigd") en een geldige (gekalibreerde) Scene.

Volledig additief en losstaand: GEEN wijziging aan design_context.py,
reasoning_engine.py, material_planner.py, pattern_planner.py, svg_planner.py of
de bestaande render-/mockup-/projectiecode. Nog NIET geimplementeerd: Design
Transfer Package en overige downstream-componenten.
"""

from __future__ import annotations

import copy
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

from reasoning_engine import FloorDesign
from material_planner import MaterialProfile
from svg_planner import SVGResultaat
from scene_builder import Scene


# ─── Visualization Boundary (AI-model-onafhankelijk, deterministisch) ────────
#
# Contract: een functie die een platte compositie-invoer-dict ontvangt en een
# Visualisatie-artefact (dict) retourneert. Bevat GEEN ontwerplogica -- puur
# compositie in, artefact uit. De standaard-implementatie kan de bestaande
# projectie-engine (mockup/floorvisualizer, AB-005) omhullen; hier een
# deterministische placeholder.

VisualisatieBoundary = Callable[[dict], dict]


def placeholder_visualisatie(invoer: dict) -> dict:
    """Deterministische placeholder voor de Visualization Boundary.

    Geen LLM-aanroep, geen promptteksten, geen willekeur: gelijke invoer levert
    exact hetzelfde artefact. Beschrijft de compositie -- het SVG-artefact
    geprojecteerd op het vloerpolygon van de Scene, met de achtergrond -- zonder
    de bestaande projectie-engine te wijzigen.
    """
    return {
        "achtergrond_url": invoer.get("achtergrond_url"),
        "vloerpolygon": invoer.get("polygon"),
        "svg": invoer.get("svg"),
        "beschrijving": "SVG-afwerking geprojecteerd op het vloerpolygon van de Scene.",
    }


@dataclass
class Visualisatie:
    """Technisch resultaat-artefact van de FVE -- BUITEN de DesignContext.

    Draagt GEEN eigen bevestigingsstatus (TD-005): het is een deterministische
    compositie van reeds bevestigde bronnen, met een weergave-motivering en
    herkomst-referenties naar het `SVGResultaat` en de Scene (en via het
    `SVGResultaat` transitief naar Concept, Floor Design, Material Profile en
    Pattern Profile).
    """

    identifier: str
    beeld: dict
    weergave_motivering: str
    svgresultaat_herkomst: dict
    scene_herkomst: dict
    kwaliteitsinformatie: dict = field(default_factory=dict)


@dataclass
class VisualisatieResultaat:
    """Technische returnvorm: een Visualisatie, of uitsluitend signaleringen
    wanneer de FVE niet mag of kan componeren."""

    visualisatie: Optional[Visualisatie] = None
    signaleringen: list[str] = field(default_factory=list)
    kwaliteitsinformatie: dict = field(default_factory=dict)

    @property
    def geslaagd(self) -> bool:
        return self.visualisatie is not None


class FloorVisualizationEngine:
    """Publieke component (BUILD-015) -- uitsluitend uitvoerende compositie.

    `componeer(svg_resultaat, floor_design, material_profile, scene)` projecteert
    het `SVGResultaat` deterministisch op de Scene en voegt Floor Design en
    Material Profile samen tot één Visualisatie. Leest alle invoer uitsluitend;
    wijzigt niets, beslist niets en bevestigt nooit. Het resultaat draagt geen
    eigen status.
    """

    STATUS_FLOOR_DESIGN_BEVESTIGD = "Bevestigd"      # Floor Design (AB-006)
    STATUS_MATERIAL_PROFILE_BEVESTIGD = "Bevestigd"  # Material Profile (AB-010)
    MAX_COMPOSITIE_POGINGEN = 3

    def __init__(self, visualiseer: VisualisatieBoundary = placeholder_visualisatie) -> None:
        # De Visualization Boundary is injecteerbaar; standaard de placeholder.
        self._visualiseer = visualiseer

    # ── Orkestratie ───────────────────────────────────────────────────────────
    def componeer(
        self,
        svg_resultaat: SVGResultaat,
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        scene: Scene,
    ) -> VisualisatieResultaat:
        """Orkestreert de compositie-keten: gate -> projectie-invoer -> boundary
        -> validatie -> verpakken. Leest alle invoer uitsluitend."""
        # 1. Viervoudige deterministische gate.
        signaleringen = self._valideer_preconditie(svg_resultaat, floor_design, material_profile, scene)
        if signaleringen:
            return VisualisatieResultaat(signaleringen=signaleringen)

        invoer = self._verzamel_invoer(svg_resultaat, floor_design, material_profile, scene)
        svg_herkomst = self._svgresultaat_snapshot(svg_resultaat)
        scene_herkomst = {"identifier": scene.id}
        laatste_afkeur: list[str] = []

        # 2-4. Compositie + validatie, met gelimiteerde her-compositie.
        for poging in range(1, self.MAX_COMPOSITIE_POGINGEN + 1):
            try:
                artefact = self._visualiseer(invoer)
            except Exception as fout:  # boundary is injecteerbaar en onbekend
                return VisualisatieResultaat(
                    signaleringen=[f"Technische fout in de Visualization Boundary: {fout}"]
                )

            laatste_afkeur = self._valideer_compositie(artefact)
            if not laatste_afkeur:
                visualisatie = self._bouw_visualisatie(artefact, svg_herkomst, scene_herkomst, poging)
                return VisualisatieResultaat(
                    visualisatie=visualisatie,
                    kwaliteitsinformatie={"pogingen": poging, "geldig": True},
                )

        # 5. Her-compositielimiet bereikt -> geen geldig resultaat, geen mutatie.
        return VisualisatieResultaat(
            signaleringen=(
                [f"Geen geldige Visualisatie na {self.MAX_COMPOSITIE_POGINGEN} pogingen."]
                + laatste_afkeur
            ),
            kwaliteitsinformatie={"pogingen": self.MAX_COMPOSITIE_POGINGEN},
        )

    # ── Stale-detectie (TD-005 §5) ────────────────────────────────────────────
    @staticmethod
    def is_stale(visualisatie: Visualisatie, svg_resultaat: SVGResultaat) -> bool:
        """True wanneer de Visualisatie niet meer bij het (huidige) `SVGResultaat`
        hoort en dus opnieuw moet worden samengesteld."""
        return visualisatie.svgresultaat_herkomst.get("identifier") != svg_resultaat.identifier

    # ── Preconditie (viervoudige deterministische gate) ───────────────────────
    def _valideer_preconditie(
        self,
        svg_resultaat: SVGResultaat,
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        scene: Scene,
    ) -> list[str]:
        signaleringen: list[str] = []

        # 1. Geldig SVGResultaat.
        if svg_resultaat is None:
            signaleringen.append("Geen SVGResultaat meegegeven.")
        elif not (isinstance(getattr(svg_resultaat, "svg", None), str) and svg_resultaat.svg.strip()):
            signaleringen.append("SVGResultaat bevat geen geldig SVG-artefact.")
        elif not getattr(svg_resultaat, "identifier", None):
            signaleringen.append("SVGResultaat is niet identificeerbaar.")

        # 2. Bevestigd Floor Design.
        signaleringen += self._valideer_bevestigd(
            floor_design, self.STATUS_FLOOR_DESIGN_BEVESTIGD, "Floor Design"
        )
        # 3. Bevestigd Material Profile.
        signaleringen += self._valideer_bevestigd(
            material_profile, self.STATUS_MATERIAL_PROFILE_BEVESTIGD, "Material Profile"
        )

        # 4. Geldige, gekalibreerde Scene.
        if scene is None:
            signaleringen.append("Geen Scene meegegeven.")
        elif not getattr(scene, "id", None):
            signaleringen.append("Scene is niet identificeerbaar.")
        elif not (scene.surface and scene.surface.is_gekalibreerd()):
            signaleringen.append("Scene is niet gekalibreerd (vloerpolygon ontbreekt of onvolledig).")

        return signaleringen

    @staticmethod
    def _valideer_bevestigd(obj, verwachte_status: str, naam: str) -> list[str]:
        if obj is None:
            return [f"Geen {naam} meegegeven."]
        if getattr(obj, "status", None) != verwachte_status:
            return [f'{naam} is niet bevestigd; FVE componeert niet '
                    f'(vereist status == "{verwachte_status}").']
        if not getattr(obj, "identifier", None):
            return [f"Bevestigd {naam} is niet identificeerbaar."]
        return []

    # ── Compositie-invoer projecteren ─────────────────────────────────────────
    @staticmethod
    def _verzamel_invoer(
        svg_resultaat: SVGResultaat,
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        scene: Scene,
    ) -> dict:
        return {
            "svg": svg_resultaat.svg,
            "achtergrond_url": scene.achtergrond_url(),
            # Defensieve diepe kopie: het vloerpolygon is een lijst van sublijsten;
            # list() zou de sublijsten met de Scene delen. Zo blijft de FVE read-only.
            "polygon": copy.deepcopy(scene.surface.polygon),
            "ontwerprichting": floor_design.ontwerprichting,
            "uitstraling": material_profile.uitstraling,
        }

    # ── Herkomst-referentie (traceerbaarheid) ─────────────────────────────────
    @staticmethod
    def _svgresultaat_snapshot(svg_resultaat: SVGResultaat) -> dict:
        pp = getattr(svg_resultaat, "pattern_profile_herkomst", {}) or {}
        return {
            "identifier": svg_resultaat.identifier,
            "pattern_profile": pp.get("identifier") if isinstance(pp, dict) else None,
        }

    # ── Validatie van het compositie-artefact ─────────────────────────────────
    @staticmethod
    def _valideer_compositie(artefact) -> list[str]:
        if not isinstance(artefact, dict):
            return ["Compositie leverde geen geldig artefact terug."]
        svg = artefact.get("svg")
        polygon = artefact.get("vloerpolygon")
        signaleringen: list[str] = []
        if not (isinstance(svg, str) and svg.strip()):
            signaleringen.append("Visualisatie-artefact mist een geldige SVG.")
        if not (isinstance(polygon, list) and len(polygon) == 4):
            signaleringen.append("Visualisatie-artefact mist een geldig vloerpolygon (4 hoekpunten).")
        return signaleringen

    # ── Visualisatie bouwen (buiten de DesignContext, geen eigen status) ──────
    @staticmethod
    def _bouw_visualisatie(
        artefact: dict, svg_herkomst: dict, scene_herkomst: dict, poging: int
    ) -> Visualisatie:
        return Visualisatie(
            identifier=str(uuid.uuid4()),
            beeld=artefact,
            weergave_motivering=(
                "Getrouwe deterministische compositie van het bevestigde SVGResultaat "
                "op de Scene; geen ontwerpkeuze toegevoegd."
            ),
            svgresultaat_herkomst=svg_herkomst,
            scene_herkomst=scene_herkomst,
            kwaliteitsinformatie={"geldig": True, "poging": poging},
        )
