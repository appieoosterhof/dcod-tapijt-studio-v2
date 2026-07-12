"""
BUILD-016 -- Design Transfer Package (DTP).

Implementeert de Design Transfer Package Builder conform de goedgekeurde
ontwerpbaseline (BUILD-016 functioneel + technisch/TD-006, incl. de correcties
uit TR-008). De DTP Builder is de laatste ketenstap van BUILD-007 (ketenstap 11)
en UITSLUITEND UITVOEREND: zij verzamelt de reeds bevestigde ontwerpinhoud en
serialiseert die deterministisch tot één overdrachtsartefact voor DCOD. Zij voegt
GEEN ontwerpkeuze toe en draagt geen ontwerpautoriteit.

Kernprincipes (technisch geborgd, conform TD-006):
  * uitvoerende bundelcomponent, geen ontwerpcomponent; leest uitsluitend;
  * het `DesignTransferPackage` heeft GEEN eigen Voorgesteld/Bevestigd-status
    (TD-006 besluit 2) -- het is een zuivere, deterministische bundeling van
    reeds bevestigde bronnen; zijn geldigheid volgt uit die bronnen
    (stale-detectie), net als bij het SVGResultaat (TD-004) en de Visualisatie
    (TD-005);
  * bundelomvang (TD-006 besluit 1): EXPLICIET de bevestigde Ontwerpvisie, het
    Floor Design, het Material Profile, de Visualisatie en het SVGResultaat;
    het Pattern Profile en het Concept uitsluitend TRANSITIEF (herkomst);
  * AI-model-onafhankelijk: de export loopt via een injecteerbare,
    format-agnostische Transfer Boundary zonder ontwerplogica (de standaard is
    een deterministische placeholder; een concreet exportformaat kan later
    worden geinjecteerd zonder de component te wijzigen); geen LLM, geen
    promptteksten;
  * gate + herkomst-coherentiecontrole borgen dat uitsluitend een coherente,
    bevestigde ontwerpketen wordt gebundeld.

Volledig additief en losstaand: GEEN wijziging aan design_context.py,
reasoning_engine.py, material_planner.py, pattern_planner.py, svg_planner.py,
floor_visualization_engine.py of de bestaande render-/mockup-/projectiecode. De
DesignContext blijft volledig read-only; niets wordt erin geschreven.
"""

from __future__ import annotations

import copy
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

from design_context import DesignContext
from reasoning_engine import FloorDesign
from material_planner import MaterialProfile
from svg_planner import SVGResultaat
from floor_visualization_engine import Visualisatie


# ─── Transfer Boundary (AI-model-onafhankelijk, deterministisch, agnostisch) ──
#
# Contract: een functie die de platte bundelinhoud (read-only snapshots) ontvangt
# en een export-representatie (het overdrachtsartefact) retourneert. Bevat GEEN
# ontwerplogica -- puur bundelinhoud in, representatie uit. De boundary is
# FORMAT-AGNOSTISCH: welk concreet exportformaat wordt geleverd, is een keuze van
# de geinjecteerde implementatie, niet van deze component. De standaard hieronder
# is een deterministische placeholder.

TransferFunctie = Callable[[dict], object]


def placeholder_transfer(inhoud: dict) -> dict:
    """Deterministische placeholder voor de Transfer Boundary.

    Geen LLM-aanroep, geen promptteksten, geen willekeur: gelijke bundelinhoud
    levert exact dezelfde representatie. Bundelt de reeds bevestigde inhoud tot
    een eenvoudige, formaat-neutrale overdrachtsstructuur zonder een concreet
    productie-/exportformaat vast te leggen.
    """
    return {
        "formaat": "overdracht/placeholder-v1",
        "onderdelen": sorted(inhoud.keys()),
        "inhoud": inhoud,
    }


@dataclass
class DesignTransferPackage:
    """Technisch resultaat-object van de DTP Builder -- BUITEN de DesignContext.

    Draagt GEEN eigen bevestigingsstatus (TD-006 besluit 2): het is een
    deterministische bundeling van reeds bevestigde bronnen, met een
    overdrachts-motivering en herkomst-referenties naar alle expliciet gebundelde
    onderdelen (en, transitief, naar Pattern Profile en Concept).
    """

    identifier: str
    inhoud: dict                     # read-only snapshots van de vijf onderdelen
    overdracht_representatie: object  # door de Transfer Boundary geproduceerd
    overdracht_motivering: str
    herkomst: dict                   # identifiers van alle onderdelen (+ transitief)
    kwaliteitsinformatie: dict = field(default_factory=dict)


@dataclass
class DesignTransferPackageWikkel:
    """Technische returnvorm: een pakket, of uitsluitend signaleringen wanneer de
    DTP Builder niet mag of kan bundelen."""

    pakket: Optional[DesignTransferPackage] = None
    signaleringen: list[str] = field(default_factory=list)
    kwaliteitsinformatie: dict = field(default_factory=dict)

    @property
    def geslaagd(self) -> bool:
        return self.pakket is not None


class DesignTransferPackageBuilder:
    """Publieke component (BUILD-016) -- uitsluitend uitvoerende bundeling.

    `bundel(dc, floor_design, material_profile, svg_resultaat, visualisatie)`
    verzamelt de bevestigde inhoud en serialiseert die deterministisch tot een
    `DesignTransferPackage`. Leest alle invoer uitsluitend; wijzigt niets,
    beslist niets en bevestigt nooit. Het resultaat draagt geen eigen status.
    """

    STATUS_FLOOR_DESIGN_BEVESTIGD = "Bevestigd"      # Floor Design (AB-006)
    STATUS_MATERIAL_PROFILE_BEVESTIGD = "Bevestigd"  # Material Profile (AB-010)
    _VISIE_INHOUD_VELDEN = ("vrije_tekst", "sfeer", "gewenste_identiteit", "ontwerpambitie")
    MAX_BUNDEL_POGINGEN = 3

    def __init__(self, exporteer: TransferFunctie = placeholder_transfer) -> None:
        # De Transfer Boundary is injecteerbaar; standaard de placeholder.
        self._exporteer = exporteer

    # ── Orkestratie ───────────────────────────────────────────────────────────
    def bundel(
        self,
        dc: DesignContext,
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        svg_resultaat: SVGResultaat,
        visualisatie: Visualisatie,
    ) -> DesignTransferPackageWikkel:
        """Orkestreert de bundel-keten: gate -> coherentie -> inhoud verzamelen
        -> Transfer Boundary -> validatie -> verpakken. Leest alle invoer
        uitsluitend."""
        # 1. Deterministische gate (statussen, geldigheid, niet-stale Visualisatie).
        signaleringen = self._valideer_preconditie(
            dc, floor_design, material_profile, svg_resultaat, visualisatie
        )
        if signaleringen:
            return DesignTransferPackageWikkel(signaleringen=signaleringen)

        # 2. Interne herkomst-coherentie (één samenhangende ontwerpketen).
        coherentie = self._valideer_coherentie(
            floor_design, material_profile, svg_resultaat, visualisatie
        )
        if coherentie:
            return DesignTransferPackageWikkel(signaleringen=coherentie)

        # 3. Read-only snapshots verzamelen (deterministisch).
        inhoud = self._verzamel_inhoud(dc, floor_design, material_profile, svg_resultaat, visualisatie)
        herkomst = self._verzamel_herkomst(dc, floor_design, material_profile, svg_resultaat, visualisatie)
        laatste_afkeur: list[str] = []

        # 4-5. Export + validatie, met gelimiteerde her-bundeling.
        for poging in range(1, self.MAX_BUNDEL_POGINGEN + 1):
            try:
                representatie = self._exporteer(inhoud)
            except Exception as fout:  # boundary is injecteerbaar en onbekend
                return DesignTransferPackageWikkel(
                    signaleringen=[f"Technische fout in de Transfer Boundary: {fout}"]
                )

            laatste_afkeur = self._valideer_representatie(representatie)
            if not laatste_afkeur:
                pakket = self._bouw_pakket(inhoud, representatie, herkomst, poging)
                return DesignTransferPackageWikkel(
                    pakket=pakket,
                    kwaliteitsinformatie={"pogingen": poging, "geldig": True},
                )

        # 6. Her-bundelingslimiet bereikt -> geen geldig pakket, geen mutatie.
        return DesignTransferPackageWikkel(
            signaleringen=(
                [f"Geen geldig Design Transfer Package na {self.MAX_BUNDEL_POGINGEN} pogingen."]
                + laatste_afkeur
            ),
            kwaliteitsinformatie={"pogingen": self.MAX_BUNDEL_POGINGEN},
        )

    # ── Stale-detectie (TD-006 §5) ────────────────────────────────────────────
    @staticmethod
    def is_stale(
        pakket: DesignTransferPackage,
        svg_resultaat: SVGResultaat,
        visualisatie: Visualisatie,
    ) -> bool:
        """True wanneer een gebundelde bron-identifier niet meer overeenkomt met
        het actuele object (Visualisatie of SVGResultaat) en het pakket dus
        opnieuw moet worden gebundeld."""
        herkomst = pakket.herkomst or {}
        vis = herkomst.get("visualisatie") or {}
        svg = herkomst.get("svgresultaat") or {}
        return (
            vis.get("identifier") != visualisatie.identifier
            or svg.get("identifier") != svg_resultaat.identifier
        )

    # ── Preconditie (deterministische gate) ───────────────────────────────────
    def _valideer_preconditie(
        self,
        dc: DesignContext,
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        svg_resultaat: SVGResultaat,
        visualisatie: Visualisatie,
    ) -> list[str]:
        signaleringen: list[str] = []

        # 1. Bevestigd Floor Design + Material Profile.
        signaleringen += self._valideer_bevestigd(
            floor_design, self.STATUS_FLOOR_DESIGN_BEVESTIGD, "Floor Design"
        )
        signaleringen += self._valideer_bevestigd(
            material_profile, self.STATUS_MATERIAL_PROFILE_BEVESTIGD, "Material Profile"
        )

        # 2. Geldig SVGResultaat (niet-leeg, identificeerbaar).
        svg_geldig = True
        if svg_resultaat is None:
            signaleringen.append("Geen SVGResultaat meegegeven.")
            svg_geldig = False
        elif not (isinstance(getattr(svg_resultaat, "svg", None), str) and svg_resultaat.svg.strip()):
            signaleringen.append("SVGResultaat bevat geen geldig SVG-artefact.")
            svg_geldig = False
        elif not getattr(svg_resultaat, "identifier", None):
            signaleringen.append("SVGResultaat is niet identificeerbaar.")
            svg_geldig = False

        # 3. Geldige, niet-stale Visualisatie.
        if visualisatie is None:
            signaleringen.append("Geen Visualisatie meegegeven.")
        elif not getattr(visualisatie, "identifier", None):
            signaleringen.append("Visualisatie is niet identificeerbaar.")
        elif not getattr(visualisatie, "beeld", None):
            signaleringen.append("Visualisatie bevat geen beeld-artefact.")
        elif svg_geldig:
            # De content-staleness van het SVGResultaat t.o.v. zijn Pattern Profile
            # is upstream geborgd (SVG Planner -> FVE); de DTP borgt uitsluitend dat
            # de Visualisatie bij DIT SVGResultaat hoort (identifier-gelijkheid).
            herkomst = getattr(visualisatie, "svgresultaat_herkomst", {}) or {}
            if herkomst.get("identifier") != svg_resultaat.identifier:
                signaleringen.append(
                    "Visualisatie is stale: hoort niet bij het aangeleverde SVGResultaat."
                )

        # 4. Bevestigde, volledige Ontwerpvisie (laag 1).
        signaleringen += self._valideer_ontwerpvisie(dc)

        return signaleringen

    @staticmethod
    def _valideer_bevestigd(obj, verwachte_status: str, naam: str) -> list[str]:
        if obj is None:
            return [f"Geen {naam} meegegeven."]
        if getattr(obj, "status", None) != verwachte_status:
            return [f'{naam} is niet bevestigd; DTP bundelt niet '
                    f'(vereist status == "{verwachte_status}").']
        if not getattr(obj, "identifier", None):
            return [f"Bevestigd {naam} is niet identificeerbaar."]
        return []

    def _valideer_ontwerpvisie(self, dc: DesignContext) -> list[str]:
        visie = getattr(dc, "ontwerpvisie", None) if dc is not None else None
        if visie is None:
            return ["Geen Ontwerpvisie (laag 1) beschikbaar."]
        if not getattr(visie, "bevestigd_door_architect", False):
            return ['Ontwerpvisie is niet door de architect bevestigd; DTP bundelt niet '
                    "(vereist bevestigd_door_architect == True)."]
        heeft_inhoud = any(
            isinstance(getattr(visie, veld, None), str) and getattr(visie, veld).strip()
            for veld in self._VISIE_INHOUD_VELDEN
        )
        if not heeft_inhoud:
            return ["Bevestigde Ontwerpvisie is leeg/onvolledig."]
        return []

    # ── Herkomst-coherentie (één samenhangende ontwerpketen) ──────────────────
    @staticmethod
    def _valideer_coherentie(
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        svg_resultaat: SVGResultaat,
        visualisatie: Visualisatie,
    ) -> list[str]:
        signaleringen: list[str] = []
        fd_herkomst = getattr(svg_resultaat, "floor_design_herkomst", {}) or {}
        mp_herkomst = getattr(svg_resultaat, "material_profile_herkomst", {}) or {}
        if fd_herkomst.get("identifier") != floor_design.identifier:
            signaleringen.append(
                "Incoherente herkomst: SVGResultaat hoort niet bij het aangeleverde Floor Design."
            )
        if mp_herkomst.get("identifier") != material_profile.identifier:
            signaleringen.append(
                "Incoherente herkomst: SVGResultaat hoort niet bij het aangeleverde Material Profile."
            )
        return signaleringen

    # ── Read-only snapshots van de bundelinhoud (deterministisch) ─────────────
    def _verzamel_inhoud(
        self,
        dc: DesignContext,
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        svg_resultaat: SVGResultaat,
        visualisatie: Visualisatie,
    ) -> dict:
        visie = dc.ontwerpvisie
        return {
            "ontwerpvisie": {
                "vrije_tekst": visie.vrije_tekst,
                "sfeer": visie.sfeer,
                "gewenste_identiteit": visie.gewenste_identiteit,
                "ontwerpambitie": visie.ontwerpambitie,
                "bevestigd_door_architect": visie.bevestigd_door_architect,
            },
            "floor_design": {
                "identifier": floor_design.identifier,
                "ontwerprichting": floor_design.ontwerprichting,
                "motivering": floor_design.motivering,
                "status": floor_design.status,
            },
            "material_profile": {
                "identifier": material_profile.identifier,
                "materiaalsoort": material_profile.materiaalsoort,
                "structuur": material_profile.structuur,
                "pooltype": material_profile.pooltype,
                "tactiliteit": material_profile.tactiliteit,
                "uitstraling": material_profile.uitstraling,
                "status": material_profile.status,
            },
            "svgresultaat": {
                "identifier": svg_resultaat.identifier,
                "svg": svg_resultaat.svg,
                "weergave_motivering": svg_resultaat.weergave_motivering,
            },
            "visualisatie": {
                "identifier": visualisatie.identifier,
                # Defensieve diepe kopie: beeld bevat geneste mutabele structuren
                # (o.a. vloerpolygon); de bundel moet bevroren blijven.
                "beeld": copy.deepcopy(visualisatie.beeld),
                "weergave_motivering": visualisatie.weergave_motivering,
            },
        }

    # ── Herkomst-referenties (traceerbaarheid, TD-006 §7) ─────────────────────
    @staticmethod
    def _verzamel_herkomst(
        dc: DesignContext,
        floor_design: FloorDesign,
        material_profile: MaterialProfile,
        svg_resultaat: SVGResultaat,
        visualisatie: Visualisatie,
    ) -> dict:
        visie = dc.ontwerpvisie
        return {
            # Expliciet gebundelde onderdelen.
            "ontwerpvisie": {"bevestigd_door_architect": visie.bevestigd_door_architect},
            "floor_design": {"identifier": floor_design.identifier, "status": floor_design.status},
            "material_profile": {"identifier": material_profile.identifier, "status": material_profile.status},
            "svgresultaat": {"identifier": svg_resultaat.identifier},
            "visualisatie": {"identifier": visualisatie.identifier},
            # Transitief (via het SVGResultaat) -- niet als apart bundelonderdeel.
            "pattern_profile": {
                "identifier": (getattr(svg_resultaat, "pattern_profile_herkomst", {}) or {}).get("identifier")
            },
            # Defensieve kopie: concept_herkomst bevat een mutabele kleurpalet-dict.
            "concept": copy.deepcopy(getattr(svg_resultaat, "concept_herkomst", {}) or {}),
        }

    # ── Validatie van de export-representatie (formaat-onafhankelijk) ──────────
    @staticmethod
    def _valideer_representatie(representatie) -> list[str]:
        """Formaat-ONAFHANKELIJKE welgevormdheidstoets: de boundary moet een
        niet-lege representatie hebben geretourneerd. Elke formaat-specifieke
        validatie (schema, bestandsstructuur) hoort in de geinjecteerde boundary,
        niet hier -- zodat de component format-agnostisch blijft."""
        if representatie is None:
            return ["Transfer Boundary leverde geen export-representatie."]
        try:
            leeg = len(representatie) == 0  # str/list/dict/bytes e.d.
        except TypeError:
            leeg = False  # niet-meetbare objecten worden als aanwezig beschouwd
        if leeg:
            return ["Transfer Boundary leverde een lege export-representatie."]
        return []

    # ── Pakket bouwen (buiten de DesignContext, geen eigen status) ────────────
    @staticmethod
    def _bouw_pakket(
        inhoud: dict, representatie, herkomst: dict, poging: int
    ) -> DesignTransferPackage:
        return DesignTransferPackage(
            identifier=str(uuid.uuid4()),
            inhoud=inhoud,
            overdracht_representatie=representatie,
            overdracht_motivering=(
                "Getrouwe deterministische bundeling van de reeds bevestigde "
                "ontwerpinhoud voor overdracht aan DCOD; geen ontwerpkeuze toegevoegd."
            ),
            herkomst=herkomst,
            kwaliteitsinformatie={"geldig": True, "poging": poging},
        )
