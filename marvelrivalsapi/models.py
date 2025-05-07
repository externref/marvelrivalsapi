from __future__ import annotations

import typing

from attrs import define, field

__all__ = (
    "Hero", 
    "Costume",
    "Ability",
    "Transformation",
)

@define(kw_only=True)
class Transformation:
    """
    Represents a hero transformation in Marvel Rivals.
    
    Attributes
    ----------
    id : str
        Unique identifier for the transformation.
    name : str
        Name of the transformation (e.g., Bruce Banner).
    icon : str
        Image path for the transformation.
    health : str | None
        Health for the transformation, if available.
    movement_speed : str | None
        Movement speed in meters per second (e.g., "6m/s").
    raw_dict : dict
        The original JSON data used to create this instance.
    """
    id: str
    name: str
    icon: str
    health: str | None = None
    movement_speed: str | None = None
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> Transformation:
        return cls(
            id=data["id"],
            name=data["name"],
            icon=data["icon"],
            health=data.get("health"),
            movement_speed=data.get("movement_speed"),
            raw_dict=data.copy(),
        )


@define(kw_only=True)
class Costume:
    """
    Represents a hero costume/skin in Marvel Rivals.
    
    Attributes
    ----------
    id : str
        Unique identifier for the costume.
    name : str
        Name of the costume.
    icon : str
        Icon path for the costume.
    quality : str
        Quality level (e.g., NO_QUALITY).
    description : str
        Description of the costume.
    appearance : str
        Visual details about the costume appearance.
    raw_dict : dict
        The original JSON data used to create this instance.
    """
    id: str
    name: str
    icon: str
    quality: str
    description: str
    appearance: str
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> Costume:
        return cls(
            id=data["id"],
            name=data["name"],
            icon=data["icon"],
            quality=data["quality"],
            description=data["description"],
            appearance=data["appearance"],
            raw_dict=data.copy(),
        )


@define(kw_only=True)
class Ability:
    """
    Represents a hero ability in Marvel Rivals.
    
    Attributes
    ----------
    id : int
        Unique ability identifier.
    icon : str | None
        Icon path for the ability.
    name : str | None
        Name of the ability.
    type : str
        Type of the ability (e.g., Ultimate, Passive).
    isCollab : bool
        Whether the ability is from a collaboration.
    description : str | None
        Description of what the ability does.
    transformation_id : str
        ID of the transformation this ability is tied to.
    additional_fields : dict
        Dynamic key-value object with extra metadata. Keys vary per ability
        and may include: Key, Casting, Cooldown, Energy Cost, Special Effect, etc.
    raw_dict : dict
        The original JSON data used to create this instance.
    """
    id: int
    icon: str | None
    name: str | None
    type: str
    isCollab: bool
    description: str | None
    transformation_id: str
    additional_fields: dict[str, object] = field(factory=dict)
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> Ability:
        return cls(
            id=data["id"],
            icon=data.get("icon"),
            name=data.get("name"),
            type=data["type"],
            isCollab=data["isCollab"],
            description=data.get("description"),
            transformation_id=data["transformation_id"],
            additional_fields=data.get("additional_fields", {}),
            raw_dict=data.copy(),
        )


@define(kw_only=True)
class Hero:
    """
    Represents a hero character in Marvel Rivals.
    
    Attributes
    ----------
    id : str
        Unique hero identifier.
    name : str
        Hero's display name.
    real_name : str
        The hero's real-world identity.
    imageUrl : str
        URL or path to the hero's image.
    role : str
        The hero's role (e.g., Vanguard, Support).
    attack_type : str
        Hero's attack type (e.g., Melee Heroes).
    team : list[str]
        Factions or affiliations the hero belongs to (e.g., Avengers).
    difficulty : str
        Difficulty rating of the hero (e.g., "4").
    bio : str
        Short biography of the hero.
    lore : str
        Extended lore/backstory of the hero.
    transformations : list[Transformation]
        Different forms the hero can transform into.
    costumes : list[Costume]
        List of hero costumes/skins.
    abilities : list[Ability]
        List of the hero's abilities.
    raw_dict : dict
        The original JSON data used to create this instance.
    """
    id: str
    name: str
    real_name: str
    imageUrl: str
    role: str
    attack_type: str
    team: list[str] = field(factory=list)
    difficulty: str
    bio: str
    lore: str
    transformations: list[Transformation] = field(factory=list)
    costumes: list[Costume] = field(factory=list)
    abilities: list[Ability] = field(factory=list)
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> Hero:
        return cls(
            id=data["id"],
            name=data["name"],
            real_name=data["real_name"],
            imageUrl=data["imageUrl"],
            role=data["role"],
            attack_type=data["attack_type"],
            team=data.get("team", []),
            difficulty=data["difficulty"],
            bio=data["bio"],
            lore=data["lore"],
            transformations=[
                Transformation.from_dict(t) for t in data.get("transformations", [])
            ],
            costumes=[Costume.from_dict(c) for c in data.get("costumes", [])],
            abilities=[Ability.from_dict(a) for a in data.get("abilities", [])],
            raw_dict=data.copy(),
        )
