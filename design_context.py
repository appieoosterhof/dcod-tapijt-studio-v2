"""
DesignContext-domeinmodel (BUILD-001A skelet + BUILD-001 fase 2).

Implementeert de datastructuur van het DesignContext Model v1.0 zoals
vastgelegd in DESIGN_CONTEXT_MODEL.md, plus (fase 2) de additieve
vertaling vanuit de bestaande `analysis`-dictionary van app.py en de
tijdelijke Parallelle Validatie die beide naast elkaar legt.

Deze module bevat geen AI-aanroepen en wijzigt niets aan
analyse_prompt(), build_tile_svg(), build_repeat_svg() of de frontend.
De vertaalfuncties hieronder LEZEN uitsluitend uit de bestaande
`analysis`-dict; de generatie zelf blijft in app.py volledig op
`analysis` gebaseerd, niet op DesignContext (zie
BUILD-001_DESIGNCONTEXT_INTEGRATIE.md, fase 2 en 2a/2b).

Rollback: app.py roept deze module in fase 2 puur observationeel aan
(resultaat wordt alleen gelogd, nooit gebruikt voor de generatie zelf).
Verwijderen van dit bestand plus de betreffende aanroep in app.py maakt
dit volledig ongedaan.
"""

from __future__ import annotations

import copy
import dataclasses
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class OntwerpVisie:
    """
    Laag 1: de ontwerpvisie van de architect.

    Eigenaar: de Architect, exclusief. DCOD mag een interpretatie van de
    visie voorstellen, maar alleen de architect kan de visie definitief
    bevestigen. Na bevestiging is deze laag onaantastbaar voor de rest
    van het ontwerpproces.

    Attributes:
        vrije_tekst: de oorspronkelijke, vrije verwoording van de wens.
        sfeer: de beleving/sfeer die de architect nastreeft.
        voorgestelde_interpretatie: de lezing van de visie zoals DCOD
            die voorstelt, voorafgaand aan bevestiging.
        bevestigd_door_architect: of de architect deze visie definitief
            heeft vastgesteld.
    """
    vrije_tekst: Optional[str] = None
    sfeer: Optional[str] = None
    voorgestelde_interpretatie: Optional[str] = None
    bevestigd_door_architect: bool = False


@dataclass
class ProjectContext:
    """
    Laag 2: de project-/ruimtecontext waarin de ontwerpvisie landt.

    Eigenaar: de Architect levert de feiten (het is zijn project), DCOD
    structureert/categoriseert deze. Bevat uitdrukkelijk geen fysieke
    ruimte-informatie (foto's, mockups) -- dat valt buiten de
    DesignContext van v1.

    Attributes:
        projecttype: het type project/branche (bv. kantoor, hotel).
        ruimtetype: de aard van de ruimte (representatief, functioneel,
            publiek-intensief, ...).
        gebruikscontext: hoe de ruimte in de praktijk gebruikt wordt.
        startconcept: het eventueel gekozen startconcept uit de
            inspiratie-flow.
    """
    projecttype: Optional[str] = None
    ruimtetype: Optional[str] = None
    gebruikscontext: Optional[str] = None
    startconcept: Optional[str] = None


@dataclass
class OntwerpStrategie:
    """
    Laag 3: de professionele vertaalslag tussen Ontwerpvisie+ProjectContext
    en het uiteindelijke Concept.

    Eigenaar: gezamenlijk. DCOD ontwikkelt samen met de architect de
    ontwerpstrategie -- DCOD brengt vakkennis in, de architect bewaakt
    dat de strategie de ontwerpvisie recht blijft doen.

    Attributes:
        aanpak: de gekozen aanpak, in benoembare termen.
        onderbouwing: de onderbouwing van deze aanpak vanuit visie en
            context.
        status: de status van de gezamenlijke ontwikkeling (bv.
            "in ontwikkeling", "vastgesteld").
    """
    aanpak: Optional[str] = None
    onderbouwing: Optional[str] = None
    status: Optional[str] = None


@dataclass
class Concept:
    """
    Laag 4: de concrete, esthetische invulling van de strategie.

    Eigenaar: gedeeld -- DCOD stelt voor (stijlfamilie, kleurpalet,
    complexiteit, motiefkarakter) binnen de grenzen van de strategie, de
    architect beoordeelt en stuurt vrij bij.

    Attributes:
        stijlfamilie: de gekozen stijlrichting.
        kleurpalet: het kleurpalet, als dictionary.
        complexiteit: de complexiteit van het motief (bv. low/medium/high).
        motiefschaal: de schaal/grootte van het motief.
        status: status van deze deelkeuze (voorgesteld/geaccepteerd).
    """
    stijlfamilie: Optional[str] = None
    kleurpalet: Optional[dict] = None
    complexiteit: Optional[str] = None
    motiefschaal: Optional[str] = None
    status: Optional[str] = None


@dataclass
class Materialisatie:
    """
    Laag 5: de ontwerptechnische vertaalslag van het concept naar het
    fysieke eindproduct.

    Eigenaar: gedeeld -- DCOD brengt materiaalkennis in, de architect
    stuurt op tactiliteit en uitstraling. In BUILD-001A bevat deze laag
    uitsluitend de structuur; er is nog geen keuzelogica.

    Attributes:
        materiaalsoort: de gekozen materiaalsoort.
        structuur: de structuur van het materiaal.
        pooltype: het pooltype van het tapijt.
        tactiliteit: hoe het materiaal aanvoelt.
        uitstraling: de visuele uitstraling van het materiaal.
        glans: de glansgraad.
        textuur: de textuur van het oppervlak.
        status: status van deze deelkeuze (voorgesteld/geaccepteerd).
    """
    materiaalsoort: Optional[str] = None
    structuur: Optional[str] = None
    pooltype: Optional[str] = None
    tactiliteit: Optional[str] = None
    uitstraling: Optional[str] = None
    glans: Optional[str] = None
    textuur: Optional[str] = None
    status: Optional[str] = None


@dataclass
class ProductieRealisatie:
    """
    Laag 6: de zuiver technische/productiegerichte haalbaarheidstoets.

    Eigenaar: DCOD, volledig. Bevat uitsluitend techniek en productie --
    geen ontwerpbeslissingen.

    Attributes:
        technische_haalbaarheid: of het concept technisch haalbaar is.
        repeat_type: het herhaalpatroon (bv. full, half-drop, brick,
            mirror).
        resolutie_dpi: de exportresolutie in DPI.
        printtechniek: de gekozen printtechniek.
        productiecontrole_status: status van de productiecontrole (bv.
            "verkennend", "productierijp").
    """
    technische_haalbaarheid: Optional[bool] = None
    repeat_type: Optional[str] = None
    resolutie_dpi: Optional[int] = None
    printtechniek: Optional[str] = None
    productiecontrole_status: Optional[str] = None


@dataclass
class Ontwerpredenering:
    """
    Doorlopende laag: legt niet vast wat er is besloten, maar waarom --
    en bewaakt zo de samenhang tussen alle andere lagen gedurende het
    hele ontwerpproces.

    Eigenaar: DCOD (het Dessinator-systeem) is bewaker; de inhoud
    weerspiegelt beslissingen van beide partijen (architect en DCOD).

    Attributes:
        beslissingen: de beslisgeschiedenis, als lijst van dictionaries
            met minimaal de sleutels "laag", "reden" en "vervangt".
    """
    beslissingen: list[dict[str, Any]] = field(default_factory=list)

    def voeg_beslissing_toe(
        self, laag: str, reden: str, vervangt: Optional[str] = None
    ) -> None:
        """Registreert een enkele beslissing in de beslisgeschiedenis.

        Args:
            laag: de laag van het DesignContext Model waarop de
                beslissing betrekking heeft.
            reden: de onderbouwing van de beslissing.
            vervangt: omschrijving van de voorgaande beslissing die
                hiermee wordt vervangen of bevestigd, indien van
                toepassing.
        """
        self.beslissingen.append(
            {"laag": laag, "reden": reden, "vervangt": vervangt}
        )


@dataclass
class DesignContext:
    """
    Centraal domeinobject van de Dessinator (DesignContext Model v1.0).

    Bundelt alle zes lagen van het domeinmodel plus de doorlopende
    Ontwerpredenering. Dit is in BUILD-001A een pure datastructuur zonder
    bedrijfslogica, en wordt door niets in de bestaande Dessinator
    gebruikt of aangeroepen.

    Attributes:
        ontwerpvisie: laag 1, zie OntwerpVisie.
        projectcontext: laag 2, zie ProjectContext.
        ontwerpstrategie: laag 3, zie OntwerpStrategie.
        concept: laag 4, zie Concept.
        materialisatie: laag 5, zie Materialisatie.
        productierealisatie: laag 6, zie ProductieRealisatie.
        ontwerpredenering: de doorlopende laag, zie Ontwerpredenering.
    """
    ontwerpvisie: OntwerpVisie = field(default_factory=OntwerpVisie)
    projectcontext: ProjectContext = field(default_factory=ProjectContext)
    ontwerpstrategie: OntwerpStrategie = field(default_factory=OntwerpStrategie)
    concept: Concept = field(default_factory=Concept)
    materialisatie: Materialisatie = field(default_factory=Materialisatie)
    productierealisatie: ProductieRealisatie = field(default_factory=ProductieRealisatie)
    ontwerpredenering: Ontwerpredenering = field(default_factory=Ontwerpredenering)

    def to_dict(self) -> dict[str, Any]:
        """Zet de volledige DesignContext om naar een platte dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DesignContext":
        """Bouwt een DesignContext op vanuit een eerder opgeslagen dictionary.

        Args:
            data: een dictionary in dezelfde vorm als geproduceerd door
                to_dict().

        Returns:
            Een nieuwe DesignContext-instantie met de waarden uit data.
        """
        return cls(
            ontwerpvisie=OntwerpVisie(**data.get("ontwerpvisie", {})),
            projectcontext=ProjectContext(**data.get("projectcontext", {})),
            ontwerpstrategie=OntwerpStrategie(**data.get("ontwerpstrategie", {})),
            concept=Concept(**data.get("concept", {})),
            materialisatie=Materialisatie(**data.get("materialisatie", {})),
            productierealisatie=ProductieRealisatie(**data.get("productierealisatie", {})),
            ontwerpredenering=Ontwerpredenering(**data.get("ontwerpredenering", {})),
        )

    def kopie(self) -> "DesignContext":
        """Geeft een volledig onafhankelijke kopie van deze DesignContext terug."""
        return copy.deepcopy(self)


# ─── Fase 2: additieve vertaling vanuit de bestaande analysis-dict ──────────
#
# Er is precies één functie die uit `analysis` leest per DesignContext-laag
# (Fase 2a, regel 1) -- dit voorkomt dat de vertaling op meerdere plekken in
# de code losraakt van de werkelijke `analysis`-vorm.


def vertaal_analysis_naar_strategie(analysis: dict[str, Any]) -> OntwerpStrategie:
    """Leidt een OntwerpStrategie af uit de bestaande analysis-dict.

    De huidige Dessinator kent nog geen apart "strategie"-veld -- de
    dichtstbijzijnde bestaande proxy is de gekozen stijl (de aanpak) en de
    AI-onderbouwing in ontwerpvisie_nl/description_nl. Dit voegt geen
    nieuwe AI-logica toe, het hergebruikt uitsluitend bestaande velden.
    """
    return OntwerpStrategie(
        aanpak=analysis.get("style"),
        onderbouwing=analysis.get("ontwerpvisie_nl") or analysis.get("description_nl"),
        status="voorgesteld",
    )


def vertaal_analysis_naar_concept(analysis: dict[str, Any]) -> Concept:
    """Leidt een Concept af uit de bestaande analysis-dict.

    Wordt geacht te worden aangeroepen met de `analysis`-dict zoals die
    is vlak vóór build_tile_svg() -- dus ná de bestaande keyword-overrides
    in api_generate(), niet met het ruwe analyse_prompt()-resultaat (zie
    Fase 2a, regel 2: vers afgeleid, niet opgeslagen).
    """
    return Concept(
        stijlfamilie=analysis.get("style"),
        kleurpalet=analysis.get("palette"),
        complexiteit=analysis.get("complexity"),
        motiefschaal=analysis.get("motif_size"),
        status="voorgesteld",
    )


def vertaal_data_naar_productierealisatie(data: dict[str, Any]) -> ProductieRealisatie:
    """Leidt een ProductieRealisatie af uit de inkomende request-payload.

    Repeat-type heeft nooit in de analysis-dict gezeten (het is puur een
    gebruikerskeuze, niet iets wat analyse_prompt() bepaalt) -- dit wordt
    daarom rechtstreeks uit `data` gehaald, dezelfde bron als de bestaande
    `repeat_type = data.get("repeat_type", "full")` in api_generate().
    """
    return ProductieRealisatie(repeat_type=data.get("repeat_type", "full"))


def bouw_context_uit_request(data: dict[str, Any], analysis: dict[str, Any]) -> DesignContext:
    """Bouwt een request-scoped DesignContext op uit de inkomende payload
    en de (na overrides) definitieve analysis-dict.

    Puur additief en observationeel in fase 2: het resultaat wordt nergens
    voor de daadwerkelijke generatie gebruikt.
    """
    dc = DesignContext()
    dc.ontwerpvisie = OntwerpVisie(vrije_tekst=data.get("prompt"))
    dc.ontwerpstrategie = vertaal_analysis_naar_strategie(analysis)
    dc.concept = vertaal_analysis_naar_concept(analysis)
    dc.productierealisatie = vertaal_data_naar_productierealisatie(data)
    return dc


# ─── Fase 2b: Parallelle Validatie ───────────────────────────────────────────
#
# Vergelijkt DesignContext met de analysis-dict waaruit hij is afgeleid.
# Doel is niet om fouten te verbergen, maar te begrijpen waarom een
# afwijking ontstaat. Tijdelijk: vervalt na afronding van fase 4.

_VERGELIJKINGSVELDEN = [
    # (laag, DesignContext-pad, analysis-sleutel)
    ("Ontwerpstrategie", "ontwerpstrategie.aanpak", "style"),
    ("Concept", "concept.stijlfamilie", "style"),
    ("Concept", "concept.kleurpalet", "palette"),
    ("Concept", "concept.complexiteit", "complexity"),
]

# Velden die niet uit analysis komen maar rechtstreeks uit de request-payload
# (data) -- repeat_type heeft nooit in analysis gezeten (BUILD-003).
_DATA_VERGELIJKINGSVELDEN = [
    # (laag, DesignContext-pad, data-sleutel, default)
    ("Productierealisatie", "productierealisatie.repeat_type", "repeat_type", "full"),
]


def vergelijk_met_analysis(
    dc: DesignContext, analysis: dict[str, Any], data: dict[str, Any] = None
) -> list[dict[str, Any]]:
    """Vergelijkt de kernvelden van DesignContext met de bron waaruit hij is
    afgeleid (analysis en, indien opgegeven, de request-payload data), en
    rapporteert elke afwijking.

    Omdat dc in dezelfde request, uit dezelfde analysis-snapshot, via
    vertaal_analysis_naar_*() is opgebouwd, hoort dit bij een correcte
    vertaling altijd een lege lijst op te leveren. Een gevonden afwijking
    wijst op een van drie oorzaken (zie BUILD-001_DESIGNCONTEXT_INTEGRATIE.md,
    Fase 2b): een verkeerd vastgelegd moment, tegenstrijdigheid tussen de
    twee bestaande keyword-overrideblokken, of een echte mapping-fout.

    Returns:
        Een lijst met per afwijking: welke laag, welk veld, de waarde in
        de bron, de waarde in DesignContext, en een aanwijzing voor de
        vermoedelijke oorzaak.
    """
    afwijkingen = []
    for laag, dc_pad, analysis_sleutel in _VERGELIJKINGSVELDEN:
        obj_naam, veld_naam = dc_pad.split(".")
        dc_waarde = getattr(getattr(dc, obj_naam), veld_naam)
        analysis_waarde = analysis.get(analysis_sleutel)
        if dc_waarde != analysis_waarde:
            afwijkingen.append({
                "laag": laag,
                "veld": dc_pad,
                "analysis_waarde": analysis_waarde,
                "designcontext_waarde": dc_waarde,
                "vermoedelijke_oorzaak": (
                    "DesignContext is mogelijk op een ander moment vastgelegd dan de "
                    "uiteindelijke analysis-staat, of de twee bestaande "
                    "keyword-overrideblokken (api_generate/build_tile_svg) spreken "
                    "elkaar tegen -- zie Fase 2b in het architectuurdocument."
                ),
            })
    if data is not None:
        for laag, dc_pad, data_sleutel, default in _DATA_VERGELIJKINGSVELDEN:
            obj_naam, veld_naam = dc_pad.split(".")
            dc_waarde = getattr(getattr(dc, obj_naam), veld_naam)
            data_waarde = data.get(data_sleutel, default)
            if dc_waarde != data_waarde:
                afwijkingen.append({
                    "laag": laag,
                    "veld": dc_pad,
                    "analysis_waarde": data_waarde,
                    "designcontext_waarde": dc_waarde,
                    "vermoedelijke_oorzaak": (
                        "DesignContext is mogelijk op een ander moment vastgelegd dan de "
                        "request-payload, of er is een mapping-fout in "
                        "vertaal_data_naar_productierealisatie() -- zie BUILD-003."
                    ),
                })
    return afwijkingen
