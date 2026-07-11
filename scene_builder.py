"""
Scene Builder (BUILD-006).

Realiseert het Scene-model uit VISION-001 (Floor Visualization Platform):
een gestandaardiseerde Scene bestaat uit een achtergrondafbeelding en
precies één Surface (de vloer), met precies één polygon van vier
hoekpunten. Geen automatische detectie, geen AI -- de vier hoekpunten
worden altijd handmatig vastgelegd.

Eén Scene = één map onder SCENES_DIR, met:
  - scene.json   (metadata + polygon)
  - een achtergrondbestand (de geuploade afbeelding, ongewijzigd bewaard)

SCENES_DIR staat onder static/ zodat Flask de achtergrondafbeeldingen
zonder aparte route kan serveren (dezelfde aanpak als static/img/ voor
de bestaande mockup-afbeeldingen).

Volledig losstaand van BUILD-004 (Context Interpreter) en BUILD-005
(Conversation Planner) -- geen enkele afhankelijkheid in beide
richtingen. Wijzigt niets aan de bestaande Mockup Engine
(static/js/app.js); een Scene is bedoeld om in diezelfde render-engine
geladen te kunnen worden (zie BUILD-006-technisch-ontwerp), niet om
die render-engine te vervangen.
"""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

SCENES_DIR = os.path.join(os.path.dirname(__file__), "static", "scenes")


class SceneValidatieFout(ValueError):
    """Wordt gegeven bij een ongeldige Scene- of polygon-opbouw."""


@dataclass
class Surface:
    """
    Eén Surface binnen een Scene (BUILD-006: uitsluitend de vloer).

    Attributes:
        type: het type oppervlak. In BUILD-006 uitsluitend "floor" --
            geen meerdere Surfaces, geen andere typen.
        polygon: de vier hoekpunten van het oppervlak, als fracties van
            de scene-breedte/-hoogte, in volgorde [TL, TR, BL, BR] --
            dezelfde vorm als de bestaande `floorPoints` in
            `ROOM_MOCKUPS` (static/js/app.js), bewust hergebruikt zodat
            een Scene rechtstreeks in de bestaande render-engine past.
    """
    type: str = "floor"
    polygon: list[list[float]] = field(default_factory=list)

    def is_gekalibreerd(self) -> bool:
        return len(self.polygon) == 4


@dataclass
class Scene:
    """
    Eén Scene (BUILD-006): een achtergrondafbeelding plus precies één
    Surface (de vloer).

    Attributes:
        id: unieke identifier van de scene.
        naam: leesbare naam, door de gebruiker opgegeven.
        achtergrond_bestand: bestandsnaam van de achtergrondafbeelding,
            relatief aan de scene-map.
        surface: de ene Surface van deze scene (BUILD-006: altijd de vloer).
    """
    id: str
    naam: str
    achtergrond_bestand: str
    surface: Surface = field(default_factory=Surface)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "naam": self.naam,
            "achtergrond_bestand": self.achtergrond_bestand,
            "surface": {"type": self.surface.type, "polygon": self.surface.polygon},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Scene":
        surface_data = data.get("surface", {})
        return cls(
            id=data["id"],
            naam=data.get("naam", ""),
            achtergrond_bestand=data["achtergrond_bestand"],
            surface=Surface(
                type=surface_data.get("type", "floor"),
                polygon=surface_data.get("polygon", []),
            ),
        )

    def achtergrond_url(self) -> str:
        """De publieke URL waarop de achtergrondafbeelding staat (static/)."""
        return f"/static/scenes/{self.id}/{self.achtergrond_bestand}"


def _scene_map(scene_id: str) -> str:
    return os.path.join(SCENES_DIR, scene_id)


def _scene_json_pad(scene_id: str) -> str:
    return os.path.join(_scene_map(scene_id), "scene.json")


def _valideer_polygon(polygon: list) -> None:
    if not isinstance(polygon, list) or len(polygon) != 4:
        raise SceneValidatieFout("Een polygon moet precies vier hoekpunten bevatten.")
    for punt in polygon:
        if not (isinstance(punt, (list, tuple)) and len(punt) == 2):
            raise SceneValidatieFout("Elk hoekpunt moet een [x, y]-paar zijn.")


def maak_scene(naam: str, achtergrond_bron_pad: str, achtergrond_extensie: str) -> Scene:
    """Maakt een nieuwe, nog niet gekalibreerde Scene aan.

    Args:
        naam: leesbare naam voor de scene.
        achtergrond_bron_pad: pad naar het reeds op schijf staande,
            geuploade afbeeldingsbestand (de aanroeper -- de Flask-route
            -- heeft dit al veilig opgeslagen; deze functie verplaatst
            het naar de scene-map).
        achtergrond_extensie: de bestandsextensie (bv. "jpg", "png"),
            zonder punt.

    Returns:
        De nieuwe Scene, met een lege (nog niet gekalibreerde) polygon.
    """
    scene_id = uuid.uuid4().hex[:12]
    scene_dir = _scene_map(scene_id)
    os.makedirs(scene_dir, exist_ok=True)

    achtergrond_bestand = f"achtergrond.{achtergrond_extensie.lstrip('.')}"
    doel_pad = os.path.join(scene_dir, achtergrond_bestand)
    os.replace(achtergrond_bron_pad, doel_pad)

    scene = Scene(id=scene_id, naam=naam, achtergrond_bestand=achtergrond_bestand)
    _schrijf_scene_json(scene)
    return scene


def sla_kalibratie_op(scene_id: str, polygon: list[list[float]]) -> Scene:
    """Legt de vier vloerhoeken van een bestaande scene vast.

    Args:
        scene_id: de scene om bij te werken.
        polygon: exact vier [x, y]-hoekpunten, als fracties van de
            scene-afmetingen, in volgorde [TL, TR, BL, BR].

    Returns:
        De bijgewerkte Scene.

    Raises:
        SceneValidatieFout: als de polygon niet uit precies vier
            geldige punten bestaat.
        FileNotFoundError: als de scene niet bestaat.
    """
    _valideer_polygon(polygon)
    scene = laad_scene(scene_id)
    scene.surface.polygon = [[float(p[0]), float(p[1])] for p in polygon]
    _schrijf_scene_json(scene)
    return scene


def laad_scene(scene_id: str) -> Scene:
    """Laadt een eerder opgeslagen scene, zonder informatieverlies."""
    pad = _scene_json_pad(scene_id)
    if not os.path.isfile(pad):
        raise FileNotFoundError(f"Scene '{scene_id}' bestaat niet.")
    with open(pad, "r", encoding="utf-8") as f:
        return Scene.from_dict(json.load(f))


def lijst_scenes() -> list[dict[str, Any]]:
    """Geeft een overzicht van alle opgeslagen scenes (voor het opnieuw openen)."""
    if not os.path.isdir(SCENES_DIR):
        return []
    resultaat = []
    for scene_id in sorted(os.listdir(SCENES_DIR)):
        try:
            scene = laad_scene(scene_id)
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            continue
        resultaat.append({
            "id": scene.id,
            "naam": scene.naam,
            "achtergrond_url": scene.achtergrond_url(),
            "gekalibreerd": scene.surface.is_gekalibreerd(),
        })
    return resultaat


def _schrijf_scene_json(scene: Scene) -> None:
    with open(_scene_json_pad(scene.id), "w", encoding="utf-8") as f:
        json.dump(scene.to_dict(), f, ensure_ascii=False, indent=2)
