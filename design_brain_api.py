"""
BUILD-019 / TD-008 -- Integratie Design Brain in de bestaande Flask-app.

Additieve, UITSLUITEND ORKESTRERENDE ontsluitingslaag (Flask Blueprint) die de
bestaande Design Brain-componenten aanstuurt. Stateless per request: elke
endpoint laadt de gesprekstoestand op grond van een `gesprek_id`, roept precies
één bestaande component aan, en slaat de toestand atomair terug.

Kernprincipes (conform TD-008):
  * geen ontwerplogica, geen duplicatie, geen bypass -- uitsluitend bestaande
    componenten worden aangeroepen;
  * id-gesleutelde, PERSISTENTE `Gesprekstoestand` (JSON per id, patroon van de
    Scene Builder) in een NIET-geserveerde map (buiten static/) -- geen mutabele
    globals, geen gedeelde toestand tussen gesprekken;
  * atomaire schrijf via os.replace (harde garantie tegen corruptie/isolatie);
    per-`gesprek_id` in-process slot als best-effort serialisatie binnen één
    proces (multi-process: de atomaire schrijf blijft de garantie);
  * eenzijdige neerwaartse import-richting: dit bestand importeert de keten-
    modules; geen keten-module importeert `app` op moduleniveau. De BUILD-018
    lui-import van `build_tile_svg` blijft leidend (binnen de boundary).

Volledig additief: de enige aanraking van `app.py` is `register_blueprint`. Geen
wijziging aan de Design Brain, de SVG-productiepipeline of de bestaande routes.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from functools import wraps
from typing import Optional

from flask import Blueprint, jsonify, request

from design_context import DesignContext
from conversation_planner import ConversationPlanner
from context_interpreter import interpreteer_context, pas_interpretaties_toe
from ontwerpstrategie_stap import OntwerpStrategieStap
from ontwerpstrategie_capability import maak_ontwerpstrategie_redeneerfunctie
from conceptvorming_capability import maak_conceptvorming_redeneerfunctie
from reasoning_engine import ReasoningEngine, FloorDesign
from material_planner import MaterialPlanner, MaterialProfile
from pattern_planner import PatternPlanner, PatternProfile
from svg_planner import SVGResultaat, SVGPlanner
from svg_planner_pipeline import maak_svg_planner
from floor_visualization_engine import FloorVisualizationEngine, Visualisatie
from design_transfer_package import DesignTransferPackageBuilder, DesignTransferPackage
import scene_builder


# ─── Gesprekstoestand (verzameling BESTAANDE objecten; geen nieuw domeinobject) ─
@dataclass
class Gesprekstoestand:
    design_context: DesignContext = field(default_factory=DesignContext)
    floor_designs: list = field(default_factory=list)
    floor_design: Optional[FloorDesign] = None
    material_profiles: list = field(default_factory=list)
    material_profile: Optional[MaterialProfile] = None
    pattern_profiles: list = field(default_factory=list)
    pattern_profile: Optional[PatternProfile] = None
    svg_resultaat: Optional[SVGResultaat] = None
    visualisatie: Optional[Visualisatie] = None
    pakket: Optional[DesignTransferPackage] = None


def _artefact_naar_dict(obj):
    return asdict(obj) if obj is not None else None


def _artefact_uit_dict(cls, data):
    return cls(**data) if data is not None else None


def _toestand_naar_dict(t: Gesprekstoestand) -> dict:
    return {
        "design_context": t.design_context.to_dict(),
        "floor_designs": [asdict(x) for x in t.floor_designs],
        "floor_design": _artefact_naar_dict(t.floor_design),
        "material_profiles": [asdict(x) for x in t.material_profiles],
        "material_profile": _artefact_naar_dict(t.material_profile),
        "pattern_profiles": [asdict(x) for x in t.pattern_profiles],
        "pattern_profile": _artefact_naar_dict(t.pattern_profile),
        "svg_resultaat": _artefact_naar_dict(t.svg_resultaat),
        "visualisatie": _artefact_naar_dict(t.visualisatie),
        "pakket": _artefact_naar_dict(t.pakket),
    }


def _toestand_uit_dict(d: dict) -> Gesprekstoestand:
    return Gesprekstoestand(
        design_context=DesignContext.from_dict(d.get("design_context", {})),
        floor_designs=[FloorDesign(**x) for x in d.get("floor_designs", [])],
        floor_design=_artefact_uit_dict(FloorDesign, d.get("floor_design")),
        material_profiles=[MaterialProfile(**x) for x in d.get("material_profiles", [])],
        material_profile=_artefact_uit_dict(MaterialProfile, d.get("material_profile")),
        pattern_profiles=[PatternProfile(**x) for x in d.get("pattern_profiles", [])],
        pattern_profile=_artefact_uit_dict(PatternProfile, d.get("pattern_profile")),
        svg_resultaat=_artefact_uit_dict(SVGResultaat, d.get("svg_resultaat")),
        visualisatie=_artefact_uit_dict(Visualisatie, d.get("visualisatie")),
        pakket=_artefact_uit_dict(DesignTransferPackage, d.get("pakket")),
    )


# ─── Persistente store (buiten static/, id-gesleuteld, atomair) ───────────────
GESPREKKEN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gesprekken")


def _geldig_gid(gid: str) -> bool:
    """Uitsluitend door ons gegenereerde UUID's -- voorkomt path-traversal."""
    try:
        uuid.UUID(str(gid))
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def _pad(gid: str) -> str:
    return os.path.join(GESPREKKEN_DIR, f"{gid}.json")


def _laad(gid: str) -> Optional[Gesprekstoestand]:
    pad = _pad(gid)
    if not os.path.isfile(pad):
        return None
    with open(pad, encoding="utf-8") as f:
        return _toestand_uit_dict(json.load(f))


def _sla_op(gid: str, toestand: Gesprekstoestand) -> None:
    os.makedirs(GESPREKKEN_DIR, exist_ok=True)
    pad = _pad(gid)
    tmp = f"{pad}.tmp.{uuid.uuid4().hex}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(_toestand_naar_dict(toestand), f, ensure_ascii=False)
    os.replace(tmp, pad)  # atomair -- geen half-geschreven toestand


# ─── Per-gesprek slot (best-effort, in-process; houdt GEEN gesprekstoestand) ──
_sloten: dict[str, threading.Lock] = {}
_sloten_meta = threading.Lock()


def _slot(gid: str) -> threading.Lock:
    with _sloten_meta:
        slot = _sloten.get(gid)
        if slot is None:
            slot = threading.Lock()
            _sloten[gid] = slot
        return slot


# ─── Response-helpers ─────────────────────────────────────────────────────────
def _ok(payload: dict, code: int = 200):
    return jsonify({"success": True, **payload}), code


def _fout(bericht: str, code: int):
    return jsonify({"success": False, "error": bericht}), code


def _signalering(signaleringen: list):
    # Een gate-uitkomst is een normale toestand, geen serverfout.
    return jsonify({"success": False, "signaleringen": signaleringen}), 200


def _onbeschikbaar():
    """AB-012: neutrale 'AI-infrastructuur niet beschikbaar'-status -- nooit
    technische details, modelnamen, sleutels of foutcodes naar de gebruiker."""
    return jsonify({"success": False, "onbeschikbaar": True}), 200


def _ai_sleutel() -> str:
    """AB-012: de AI-sleutel is uitsluitend SERVERCONFIGURATIE.

    Volgorde: omgevingsvariabele (productie) -> het reeds bestaande, gitignored
    `api_key.txt` (dev). Wordt NOOIT uit de request/frontend gelezen.
    """
    sleutel = (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("DCOD_AI_KEY") or "").strip()
    if not sleutel:
        pad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api_key.txt")
        try:
            with open(pad, encoding="utf-8") as f:
                sleutel = f.read().strip()
        except OSError:
            sleutel = ""
    return sleutel


def _herkomst_id(obj, veld):
    """Hulp: de herkomst-identifier van een resultaat-object, of None."""
    return (getattr(obj, veld, None) or {}).get("identifier")


def _invalideer_verouderd(toestand) -> None:
    """BUILD-023 R4 — gerichte invalidatie via UITSLUITEND de bestaande
    is_stale/herkomst-mechanismen. Verwijdert (lazy, idempotent) downstream-
    resultaten die niet meer bij hun bevestigde upstream horen, zodat hergebruik
    en fase-routing consistent zijn. Geen nieuw cache-/statusmechanisme.
    """
    t = toestand
    fd_id = t.floor_design.identifier if t.floor_design else None
    # Material Profile(s) <- Floor Design (herkomst-identifier).
    if t.material_profile and _herkomst_id(t.material_profile, "floor_design_herkomst") != fd_id:
        t.material_profile = None
    if t.material_profiles and _herkomst_id(t.material_profiles[0], "floor_design_herkomst") != fd_id:
        t.material_profiles = []
    mp_id = t.material_profile.identifier if t.material_profile else None
    # Pattern Profile(s) <- Material Profile (herkomst-identifier).
    if t.pattern_profile and _herkomst_id(t.pattern_profile, "material_profile_herkomst") != mp_id:
        t.pattern_profile = None
    if t.pattern_profiles and _herkomst_id(t.pattern_profiles[0], "material_profile_herkomst") != mp_id:
        t.pattern_profiles = []
    # SVGResultaat <- Pattern Profile (bestaande is_stale).
    if t.svg_resultaat and (t.pattern_profile is None or SVGPlanner.is_stale(t.svg_resultaat, t.pattern_profile)):
        t.svg_resultaat = None
    # Visualisatie <- SVGResultaat (bestaande is_stale).
    if t.visualisatie and (t.svg_resultaat is None or FloorVisualizationEngine.is_stale(t.visualisatie, t.svg_resultaat)):
        t.visualisatie = None
    # Design Transfer Package <- SVGResultaat + Visualisatie (bestaande is_stale).
    if t.pakket and (t.svg_resultaat is None or t.visualisatie is None
                     or DesignTransferPackageBuilder.is_stale(t.pakket, t.svg_resultaat, t.visualisatie)):
        t.pakket = None


# ─── Blueprint ────────────────────────────────────────────────────────────────
design_brain_bp = Blueprint("design_brain", __name__, url_prefix="/api/design-brain")


def _met_gesprek(fn):
    """Laadt onder het per-id-slot de toestand (404 bij onbekend id) en vangt
    onverwachte fouten af. De endpoint slaat zelf expliciet op bij succes."""
    @wraps(fn)
    def wrapper(gesprek_id):
        if not _geldig_gid(gesprek_id):
            return _fout("Ongeldig gesprek_id.", 400)
        with _slot(gesprek_id):
            toestand = _laad(gesprek_id)
            if toestand is None:
                return _fout("Onbekend gesprek.", 404)
            _invalideer_verouderd(toestand)  # BUILD-023 R4 (gerichte invalidatie)
            try:
                return fn(gesprek_id, toestand)
            except Exception as exc:  # nooit een half-geschreven toestand
                return _fout(f"Interne fout: {exc}", 500)
    return wrapper


@design_brain_bp.route("/gesprek", methods=["POST"])
def start_gesprek():
    gid = str(uuid.uuid4())
    _sla_op(gid, Gesprekstoestand())
    return _ok({"gesprek_id": gid}, 201)


@design_brain_bp.route("/<gesprek_id>", methods=["GET"])
def status(gesprek_id):
    if not _geldig_gid(gesprek_id):
        return _fout("Ongeldig gesprek_id.", 400)
    toestand = _laad(gesprek_id)  # read-only: geen slot, geen opslag
    if toestand is None:
        return _fout("Onbekend gesprek.", 404)
    _invalideer_verouderd(toestand)  # BUILD-023 R4 (consistente clientweergave)
    return _ok({"toestand": _toestand_naar_dict(toestand)})


@design_brain_bp.route("/<gesprek_id>/dialoog", methods=["POST"])
@_met_gesprek
def dialoog(gesprek_id, toestand):
    data = request.get_json(silent=True) or {}
    invoer = (data.get("invoer") or "").strip()
    dc = toestand.design_context

    # AB-012: de AI-sleutel komt UITSLUITEND uit serverconfiguratie, nooit uit de
    # request/frontend. Zonder geldige AI-config is de studio "niet beschikbaar"
    # (mensvriendelijk, zonder technische details).
    sleutel = _ai_sleutel()
    if invoer and not sleutel:
        return _onbeschikbaar()

    # BUILD-020: ÉÉN interpretatie per beurt. De Conversation Planner roept de
    # Context Interpreter aan (BUILD-017-boundary) en projecteert laag 1; wij
    # vangen exact diezelfde interpretatielijst op om er de laag-2-subset uit te
    # projecteren -- geen tweede interpretatie. De Context Interpreter blijft de
    # enige interpreter; pas_interpretaties_toe blijft de enige projectie.
    opgevangen: dict = {}

    def interpreter(tekst):
        interpretaties = interpreteer_context(tekst, api_key=sleutel)
        opgevangen["interpretaties"] = interpretaties
        return interpretaties

    resultaat = ConversationPlanner(interpreteer=interpreter).verwerk(dc, invoer)

    # Laag-2-projectie uit dezelfde interpretatie. Loopt uitsluitend tijdens de
    # dialoogfase: bij een reeds bevestigde visie roept de CP de interpreter niet
    # aan (write-gate/read-only), dus blijft `opgevangen` leeg en wordt laag 2
    # niet herschreven.
    if "interpretaties" in opgevangen:
        laag2 = [i for i in opgevangen["interpretaties"]
                 if getattr(i, "laag", None) == "projectcontext"]
        if laag2:
            pas_interpretaties_toe(dc, laag2)

    _sla_op(gesprek_id, toestand)  # laag 1 (CP) + laag 2 (projectie) behouden
    if not resultaat.geslaagd:
        # Interpretatie mislukt = AI-infrastructuur niet beschikbaar (AB-012):
        # neutrale melding, nooit de technische signalering (bv. sleutel/model).
        return _onbeschikbaar()
    vs = resultaat.vervolgstap
    return _ok({
        "vervolgstap": {"type": vs.type, "inhoud": vs.inhoud} if vs else None,
        "ontwerpvisie": asdict(dc.ontwerpvisie),
        "projectcontext": asdict(dc.projectcontext),
    })


@design_brain_bp.route("/<gesprek_id>/bevestig-visie", methods=["POST"])
@_met_gesprek
def bevestig_visie(gesprek_id, toestand):
    # Expliciete architect-actie; de component zet deze vlag nooit zelf.
    toestand.design_context.ontwerpvisie.bevestigd_door_architect = True
    _sla_op(gesprek_id, toestand)
    return _ok({"bevestigd_door_architect": True})


@design_brain_bp.route("/<gesprek_id>/ontwerpstrategie", methods=["POST"])
@_met_gesprek
def ontwerpstrategie(gesprek_id, toestand):
    # BUILD-023 R1/R6: hergebruik een bestaande strategie (laag 3 = presence-based);
    # geen nieuwe reasoning-aanroep zonder nieuwe ontwerpwaarde.
    if toestand.design_context.ontwerpstrategie.aanpak:
        return _ok({"ontwerpstrategie": asdict(toestand.design_context.ontwerpstrategie)})
    # BUILD-020 / BUILD-009: laag 3 uit de bevestigde visie (laag 1) + de
    # geprojecteerde Project-/Ruimtecontext (laag 2). De component stelt voor
    # (status "in ontwikkeling") en bevestigt nooit; muteert nooit laag 1/2.
    # IMP-015: de reasoning boundary is nu configuratie-gestuurd (productie of
    # deterministische placeholder). De sleutel is uitsluitend serverconfig
    # (AB-012, _ai_sleutel); de component/orchestratie blijft ongewijzigd.
    redeneer = maak_ontwerpstrategie_redeneerfunctie(_ai_sleutel())
    resultaat = OntwerpStrategieStap(redeneer=redeneer).stel_voor(toestand.design_context)
    if not resultaat.geslaagd:
        return _signalering(resultaat.signaleringen)
    _sla_op(gesprek_id, toestand)  # dc.ontwerpstrategie + Ontwerpredenering
    return _ok({"ontwerpstrategie": asdict(toestand.design_context.ontwerpstrategie)})


@design_brain_bp.route("/<gesprek_id>/bevestig-strategie", methods=["POST"])
@_met_gesprek
def bevestig_strategie(gesprek_id, toestand):
    # Gezamenlijke vaststelling (architect + DCOD, laag 3 is GEZAMENLIJK); de
    # component zet deze status nooit zelf.
    st = toestand.design_context.ontwerpstrategie
    if not st.aanpak:
        return _fout("Geen voorgestelde Ontwerpstrategie om vast te stellen.", 409)
    st.status = OntwerpStrategieStap.STATUS_VASTGESTELD
    _sla_op(gesprek_id, toestand)
    return _ok({"ontwerpstrategie_status": st.status})


@design_brain_bp.route("/<gesprek_id>/concept", methods=["POST"])
@_met_gesprek
def concept(gesprek_id, toestand):
    # BUILD-023 R1/R6: hergebruik een bestaand Concept (laag 4 = presence-based).
    if toestand.design_context.concept.stijlfamilie:
        return _ok({"concept": asdict(toestand.design_context.concept)})
    # Workflow-gate (BUILD-020 / gelaagde bevestiging): het Concept volgt pas op
    # een vastgestelde Ontwerpstrategie. vorm_concept zelf toetst uitsluitend
    # `aanpak`; deze gate borgt de gezamenlijke vaststelling van laag 3.
    if toestand.design_context.ontwerpstrategie.status != OntwerpStrategieStap.STATUS_VASTGESTELD:
        return _fout("Stel eerst de Ontwerpstrategie vast.", 409)
    # IMP-016: de Concept-reasoning boundary (Fase 1) is nu configuratie-gestuurd
    # (productie of deterministische placeholder). Alleen `conceptvorming` wordt
    # geïnjecteerd; Floor Design-generatie (Fase 2) blijft de placeholder. De
    # sleutel is uitsluitend serverconfig (AB-012, _ai_sleutel); component/
    # orchestratie ongewijzigd.
    engine = ReasoningEngine(conceptvorming=maak_conceptvorming_redeneerfunctie(_ai_sleutel()))
    resultaat = engine.vorm_concept(toestand.design_context)
    if not resultaat.geslaagd:
        return _signalering(resultaat.signaleringen)
    _sla_op(gesprek_id, toestand)  # dc.concept (voorgesteld) + Ontwerpredenering
    return _ok({"concept": asdict(toestand.design_context.concept)})


@design_brain_bp.route("/<gesprek_id>/bevestig-concept", methods=["POST"])
@_met_gesprek
def bevestig_concept(gesprek_id, toestand):
    c = toestand.design_context.concept
    if not c.stijlfamilie:
        return _fout("Geen voorgesteld Concept om te bevestigen.", 409)
    c.status = "bevestigd"  # architect-actie
    _sla_op(gesprek_id, toestand)
    return _ok({"concept_status": c.status})


@design_brain_bp.route("/<gesprek_id>/floor-designs", methods=["POST"])
@_met_gesprek
def floor_designs(gesprek_id, toestand):
    # BUILD-023 R1/R4: hergebruik bestaande (niet-stale) Floor Designs.
    if toestand.floor_designs:
        return _ok({"floor_designs": [asdict(x) for x in toestand.floor_designs]})
    resultaat = ReasoningEngine().genereer_floor_designs(toestand.design_context)
    if not resultaat.geslaagd:
        return _signalering(resultaat.signaleringen)
    toestand.floor_designs = resultaat.floor_designs
    toestand.floor_design = None
    _sla_op(gesprek_id, toestand)
    return _ok({"floor_designs": [asdict(x) for x in resultaat.floor_designs]})


@design_brain_bp.route("/<gesprek_id>/bevestig-floor-design", methods=["POST"])
@_met_gesprek
def bevestig_floor_design(gesprek_id, toestand):
    data = request.get_json(silent=True) or {}
    idx = data.get("index", 0)
    if not isinstance(idx, int) or not (0 <= idx < len(toestand.floor_designs)):
        return _fout("Ongeldige index voor Floor Design.", 400)
    fd = toestand.floor_designs[idx]
    fd.status = "Bevestigd"  # architect-actie
    toestand.floor_design = fd
    _sla_op(gesprek_id, toestand)
    return _ok({"floor_design": asdict(fd)})


@design_brain_bp.route("/<gesprek_id>/material-profiles", methods=["POST"])
@_met_gesprek
def material_profiles(gesprek_id, toestand):
    # BUILD-023 R1/R4: hergebruik bestaande (niet-stale) Material Profiles.
    if toestand.material_profiles:
        return _ok({"material_profiles": [asdict(x) for x in toestand.material_profiles]})
    if toestand.floor_design is None:
        return _fout("Bevestig eerst een Floor Design.", 409)
    resultaat = MaterialPlanner().stel_material_profiles_voor(
        toestand.design_context, toestand.floor_design)
    if not resultaat.geslaagd:
        return _signalering(resultaat.signaleringen)
    toestand.material_profiles = resultaat.material_profiles
    toestand.material_profile = None
    _sla_op(gesprek_id, toestand)
    return _ok({"material_profiles": [asdict(x) for x in resultaat.material_profiles]})


@design_brain_bp.route("/<gesprek_id>/bevestig-material-profile", methods=["POST"])
@_met_gesprek
def bevestig_material_profile(gesprek_id, toestand):
    data = request.get_json(silent=True) or {}
    idx = data.get("index", 0)
    if not isinstance(idx, int) or not (0 <= idx < len(toestand.material_profiles)):
        return _fout("Ongeldige index voor Material Profile.", 400)
    mp = toestand.material_profiles[idx]
    mp.status = "Bevestigd"  # architect-actie
    toestand.material_profile = mp
    _sla_op(gesprek_id, toestand)
    return _ok({"material_profile": asdict(mp)})


@design_brain_bp.route("/<gesprek_id>/pattern-profiles", methods=["POST"])
@_met_gesprek
def pattern_profiles(gesprek_id, toestand):
    # BUILD-023 R1/R4: hergebruik bestaande (niet-stale) Pattern Profiles.
    if toestand.pattern_profiles:
        return _ok({"pattern_profiles": [asdict(x) for x in toestand.pattern_profiles]})
    if toestand.material_profile is None:
        return _fout("Bevestig eerst een Material Profile.", 409)
    resultaat = PatternPlanner().stel_pattern_profiles_voor(
        toestand.design_context, toestand.floor_design, toestand.material_profile)
    if not resultaat.geslaagd:
        return _signalering(resultaat.signaleringen)
    toestand.pattern_profiles = resultaat.pattern_profiles
    toestand.pattern_profile = None
    _sla_op(gesprek_id, toestand)
    return _ok({"pattern_profiles": [asdict(x) for x in resultaat.pattern_profiles]})


@design_brain_bp.route("/<gesprek_id>/bevestig-pattern-profile", methods=["POST"])
@_met_gesprek
def bevestig_pattern_profile(gesprek_id, toestand):
    data = request.get_json(silent=True) or {}
    idx = data.get("index", 0)
    if not isinstance(idx, int) or not (0 <= idx < len(toestand.pattern_profiles)):
        return _fout("Ongeldige index voor Pattern Profile.", 400)
    pp = toestand.pattern_profiles[idx]
    pp.status = "Bevestigd"  # architect-actie
    toestand.pattern_profile = pp
    _sla_op(gesprek_id, toestand)
    return _ok({"pattern_profile": asdict(pp)})


@design_brain_bp.route("/<gesprek_id>/svg", methods=["POST"])
@_met_gesprek
def svg(gesprek_id, toestand):
    # BUILD-023 R1/R3: hergebruik een bestaand (niet-stale) SVGResultaat --
    # deterministisch, geen herberekening bij ongewijzigd patroon.
    if toestand.svg_resultaat:
        return _ok({"svg_resultaat": asdict(toestand.svg_resultaat)})
    if toestand.pattern_profile is None:
        return _fout("Bevestig eerst een Pattern Profile.", 409)
    # SVG Planner met de PRODUCTIE-pipeline (BUILD-018-adapter).
    resultaat = maak_svg_planner().render(
        toestand.design_context, toestand.floor_design,
        toestand.material_profile, toestand.pattern_profile)
    if not resultaat.geslaagd:
        return _signalering(resultaat.signaleringen)
    toestand.svg_resultaat = resultaat.svg_resultaat
    _sla_op(gesprek_id, toestand)
    return _ok({"svg_resultaat": asdict(resultaat.svg_resultaat)})


@design_brain_bp.route("/<gesprek_id>/visualisatie", methods=["POST"])
@_met_gesprek
def visualisatie(gesprek_id, toestand):
    data = request.get_json(silent=True) or {}
    scene_id = (data.get("scene_id") or "").strip()
    # BUILD-023 R1/R3: hergebruik de Visualisatie als zij bij DEZELFDE ruimte hoort
    # (een andere ruimte = gewijzigde invoer -> nieuwe projectie). Stale t.o.v. het
    # SVGResultaat is al door de invalidatie afgevangen.
    if toestand.visualisatie and _herkomst_id(toestand.visualisatie, "scene_herkomst") == scene_id:
        return _ok({"visualisatie": asdict(toestand.visualisatie)})
    if toestand.svg_resultaat is None:
        return _fout("Genereer eerst een SVG.", 409)
    try:
        scene = scene_builder.laad_scene(scene_id)  # read-only, bestaande Scene Builder
    except Exception:
        return _fout("Onbekende of ongeldige scene.", 400)
    resultaat = FloorVisualizationEngine().componeer(
        toestand.svg_resultaat, toestand.floor_design, toestand.material_profile, scene)
    if not resultaat.geslaagd:
        return _signalering(resultaat.signaleringen)
    toestand.visualisatie = resultaat.visualisatie
    _sla_op(gesprek_id, toestand)
    return _ok({"visualisatie": asdict(resultaat.visualisatie)})


@design_brain_bp.route("/<gesprek_id>/transfer-package", methods=["POST"])
@_met_gesprek
def transfer_package(gesprek_id, toestand):
    # BUILD-023 R1/R4: hergebruik een bestaand (niet-stale) Design Transfer Package.
    if toestand.pakket:
        return _ok({"design_transfer_package": asdict(toestand.pakket)})
    if toestand.visualisatie is None:
        return _fout("Maak eerst een Visualisatie.", 409)
    resultaat = DesignTransferPackageBuilder().bundel(
        toestand.design_context, toestand.floor_design, toestand.material_profile,
        toestand.svg_resultaat, toestand.visualisatie)
    if not resultaat.geslaagd:
        return _signalering(resultaat.signaleringen)
    toestand.pakket = resultaat.pakket
    _sla_op(gesprek_id, toestand)
    return _ok({"design_transfer_package": asdict(resultaat.pakket)})
