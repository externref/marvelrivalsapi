"""MIT License

Copyright (c) 2025 sarthak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from __future__ import annotations

import json
import typing
from datetime import datetime

from attrs import define, field
from pygments import formatters, highlight, lexers  # type: ignore

from marvelrivalsapi.utility import LoginOS, image

__all__ = (
    "Hero",
    "Costume",
    "Ability",
    "Transformation",
    "HeroStat",
    "RankSeason",
    "PlayerInfo",
    "LeaderboardPlayer",
    "HeroLeaderboard",
    "Achievement",
    "AchievementList",
    "Item",
    "ItemList",
    "BattlePassItem",
    "BattlePass",
    "SubMap",
    "Map",
    "MapList",
)


class Model:
    raw_dict: dict[str, typing.Any]

    def pretty_str(self, color: bool = True) -> str:
        jsond = json.dumps(self.raw_dict, indent=4)
        return (
            highlight(jsond, lexers.JsonLexer(), formatters.TerminalFormatter())
            if color
            else jsond
        )


@define(kw_only=True)
class Transformation(Model):
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
class Costume(Model):
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
            quality=data.get("quality", "NO_QUALITY"),
            description=data["description"],
            appearance=data["appearance"],
            raw_dict=data.copy(),
        )


@define(kw_only=True)
class Ability(Model):
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
class Hero(Model):
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


@define(kw_only=True)
class HeroStat(Model):
    """
    Represents statistics for a hero in Marvel Rivals.

    Attributes
    ----------
    hero_id : int
        Unique identifier for the hero.
    hero_name : str
        Display name of the hero.
    hero_icon : str
        Path or URL to the hero's icon image.
    matches : int
        Total number of matches the hero has been played in.
    wins : int
        Total number of matches won with this hero.
    k : float
        Average kills per match.
    d : float
        Average deaths per match.
    a : float
        Average assists per match.
    play_time : str
        Total play time with this hero (formatted as hours, minutes, and seconds).
    total_hero_damage : int
        Total damage dealt to enemy heroes.
    total_hero_heal : int
        Total healing done by this hero.
    total_damage_taken : int
        Total damage taken while playing this hero.
    session_hit_rate : float
        Hit rate during sessions, usually a value between 0 and 1.
    solo_kill : float
        Average number of solo kills per match.
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    hero_id: int
    hero_name: str
    hero_icon: str
    matches: int
    wins: int
    k: float
    d: float
    a: float
    play_time: str
    total_hero_damage: int
    total_hero_heal: int
    total_damage_taken: int
    session_hit_rate: float
    solo_kill: float
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> HeroStat:
        """
        Create a HeroStat instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing hero statistics data.

        Returns
        -------
        HeroStat
            A new HeroStat instance.
        """
        return cls(
            hero_id=data["hero_id"],
            hero_name=data["hero_name"],
            hero_icon=data["hero_icon"],
            matches=data["matches"],
            wins=data["wins"],
            k=data["k"],
            d=data["d"],
            a=data["a"],
            play_time=data["play_time"],
            total_hero_damage=data["total_hero_damage"],
            total_hero_heal=data["total_hero_heal"],
            total_damage_taken=data["total_damage_taken"],
            session_hit_rate=data["session_hit_rate"],
            solo_kill=data["solo_kill"],
            raw_dict=data.copy(),
        )

    @property
    def win_rate(self) -> float:
        """
        Calculate win rate for this hero.

        Returns
        -------
        float
            Win rate as a decimal between 0 and 1.
        """
        return self.wins / self.matches if self.matches > 0 else 0.0

    @property
    def kda(self) -> float:
        """
        Calculate KDA (Kills + Assists / Deaths) ratio.

        Returns
        -------
        float
            KDA ratio. Returns (K+A) if deaths is 0.
        """
        return (self.k + self.a) / (self.d or 1)


@define(kw_only=True)
class RankSeason(Model):
    """
    Represents ranking information for a player in the current season.

    Attributes
    ----------
    rank_game_id : int
        ID of the ranked game mode.
    level : int
        Current rank level.
    rank_score : str
        Current rank score.
    max_level : int
        Highest rank level achieved during the season.
    max_rank_score : str
        Highest rank score achieved during the season.
    update_time : int
        Last update timestamp (Unix time).
    win_count : int
        Number of ranked wins.
    protect_score : int
        Score protected due to rank protection mechanics.
    diff_score : str
        Score change since the last update.
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    rank_game_id: int
    level: int
    rank_score: str
    max_level: int
    max_rank_score: str
    update_time: int
    win_count: int
    protect_score: int
    diff_score: str
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> RankSeason:
        """
        Create a RankSeason instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing rank season data.

        Returns
        -------
        RankSeason
            A new RankSeason instance.
        """
        if not data:
            return cls(
                rank_game_id=0,
                level=0,
                rank_score="0",
                max_level=0,
                max_rank_score="0",
                update_time=0,
                win_count=0,
                protect_score=0,
                diff_score="0",
                raw_dict=data.copy(),
            )

        return cls(
            rank_game_id=data["rank_game_id"],
            level=data["level"],
            rank_score=data["rank_score"],
            max_level=data["max_level"],
            max_rank_score=data["max_rank_score"],
            update_time=data["update_time"],
            win_count=data["win_count"],
            protect_score=data["protect_score"],
            diff_score=data["diff_score"],
            raw_dict=data.copy(),
        )

    @property
    def last_updated(self) -> datetime:
        """
        Get the last update time as a datetime object.

        Returns
        -------
        datetime
            The last time the rank was updated.
        """
        return datetime.fromtimestamp(self.update_time)


@define(kw_only=True)
class PlayerInfo(Model):
    """
    Represents basic information about a player.

    Attributes
    ----------
    name : str
        Player's in-game name.
    cur_head_icon_id : str
        ID of the current avatar or head icon.
    rank_season : RankSeason
        Ranking information for the current season.
    login_os : str
        Operating system used at last login (e.g., "1" = Android, "2" = iOS).
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    name: str
    cur_head_icon_id: str
    rank_season: RankSeason
    login_os: str
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> PlayerInfo:
        """
        Create a PlayerInfo instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing player info data.

        Returns
        -------
        PlayerInfo
            A new PlayerInfo instance.
        """
        return cls(
            name=data["name"],
            cur_head_icon_id=data["cur_head_icon_id"],
            rank_season=RankSeason.from_dict(data["rank_season"]),
            login_os=data["login_os"],
            raw_dict=data.copy(),
        )

    @property
    def platform(self) -> LoginOS:
        """
        Get the platform name based on the login OS code.

        Returns
        -------
        str
            The platform name (PC, PS or Xbox).
        """
        platforms = {
            "1": "PC",
            "2": "PS",
            "3": "XBOX",
        }
        return LoginOS(int(platforms.get(self.login_os, 1)))


@define(kw_only=True)
class LeaderboardPlayer(Model):
    """
    Represents a player entry in the leaderboard.

    Attributes
    ----------
    info : PlayerInfo
        Basic information about the player.
    player_uid : int
        Unique identifier for the player.
    matches : int
        Total matches played.
    wins : int
        Total matches won.
    kills : int
        Total kills achieved.
    deaths : int
        Total number of deaths.
    assists : int
        Total number of assists.
    play_time : str
        Total play time in minutes, as a string with decimal value.
    total_hero_damage : str
        Total damage dealt to enemy heroes.
    total_damage_taken : str
        Total damage taken from enemies.
    total_hero_heal : str
        Total healing done to heroes.
    mvps : int
        Number of times the player was MVP (Most Valuable Player).
    svps : int
        Number of times the player was SVP (Second Valuable Player).
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    info: PlayerInfo
    player_uid: int
    matches: int
    wins: int
    kills: int
    deaths: int
    assists: int
    play_time: str
    total_hero_damage: str
    total_damage_taken: str
    total_hero_heal: str
    mvps: int
    svps: int
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> LeaderboardPlayer:
        """
        Create a LeaderboardPlayer instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing leaderboard player data.

        Returns
        -------
        LeaderboardPlayer
            A new LeaderboardPlayer instance.
        """
        return cls(
            info=PlayerInfo.from_dict(data["info"]),
            player_uid=data["player_uid"],
            matches=data["matches"],
            wins=data["wins"],
            kills=data["kills"],
            deaths=data["deaths"],
            assists=data["assists"],
            play_time=data["play_time"],
            total_hero_damage=data["total_hero_damage"],
            total_damage_taken=data["total_damage_taken"],
            total_hero_heal=data["total_hero_heal"],
            mvps=data["mvps"],
            svps=data["svps"],
            raw_dict=data.copy(),
        )

    @property
    def win_rate(self) -> float:
        """
        Calculate win rate for this player.

        Returns
        -------
        float
            Win rate as a decimal between 0 and 1.
        """
        return self.wins / self.matches if self.matches > 0 else 0.0

    @property
    def kda(self) -> float:
        """
        Calculate KDA (Kills + Assists / Deaths) ratio.

        Returns
        -------
        float
            KDA ratio. Uses deaths = 1 if deaths = 0.
        """
        return (self.kills + self.assists) / (self.deaths or 1)

    @property
    def avg_kills(self) -> float:
        """
        Calculate average kills per match.

        Returns
        -------
        float
            Average kills per match.
        """
        return self.kills / self.matches if self.matches > 0 else 0.0

    @property
    def avg_deaths(self) -> float:
        """
        Calculate average deaths per match.

        Returns
        -------
        float
            Average deaths per match.
        """
        return self.deaths / self.matches if self.matches > 0 else 0.0

    @property
    def avg_assists(self) -> float:
        """
        Calculate average assists per match.

        Returns
        -------
        float
            Average assists per match.
        """
        return self.assists / self.matches if self.matches > 0 else 0.0

    @property
    def avg_hero_damage(self) -> float:
        """
        Calculate average hero damage per match.

        Returns
        -------
        float
            Average hero damage per match.
        """
        try:
            return (
                float(self.total_hero_damage) / self.matches
                if self.matches > 0
                else 0.0
            )
        except (ValueError, TypeError):
            return 0.0

    @property
    def mvp_rate(self) -> float:
        """
        Calculate rate of MVP awards.

        Returns
        -------
        float
            Percentage of matches where player was MVP, as a decimal.
        """
        return self.mvps / self.matches if self.matches > 0 else 0.0


@define(kw_only=True)
class HeroLeaderboard(Model):
    """
    Represents a leaderboard with multiple players.

    Attributes
    ----------
    players : list[LeaderboardPlayer]
        List of players on the leaderboard.
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    players: list[LeaderboardPlayer] = field(factory=list)
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> HeroLeaderboard:
        """
        Create a Leaderboard instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing leaderboard data.

        Returns
        -------
        Leaderboard
            A new Leaderboard instance.
        """
        return cls(
            players=[
                LeaderboardPlayer.from_dict(player)
                for player in data.get("players", [])
            ],
            raw_dict=data.copy(),
        )

    def top_players(self, limit: int = 10) -> list[LeaderboardPlayer]:
        """
        Get the top players from the leaderboard.

        Parameters
        ----------
        limit : int, optional
            Number of top players to return, by default 10

        Returns
        -------
        list[LeaderboardPlayer]
            List of top players, limited by the specified number.
        """
        return self.players[:limit]

    def sort_by_wins(self) -> list[LeaderboardPlayer]:
        """
        Sort players by number of wins (descending).

        Returns
        -------
        list[LeaderboardPlayer]
            List of players sorted by wins.
        """
        return sorted(self.players, key=lambda p: p.wins, reverse=True)

    def sort_by_kda(self) -> list[LeaderboardPlayer]:
        """
        Sort players by KDA ratio (descending).

        Returns
        -------
        list[LeaderboardPlayer]
            List of players sorted by KDA.
        """
        return sorted(self.players, key=lambda p: p.kda, reverse=True)

    def sort_by_rank(self) -> list[LeaderboardPlayer]:
        """
        Sort players by rank level (descending).

        Returns
        -------
        list[LeaderboardPlayer]
            List of players sorted by rank level.
        """
        return sorted(
            self.players, key=lambda p: p.info.rank_season.level, reverse=True
        )


@define(kw_only=True)
class CostumePremiumWrapper(Costume):
    video: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> Costume:
        return cls(
            id=data["id"],
            name=data["name"],
            icon=data["icon"],
            quality=data.get("quality", "NO_QUALITY"),
            description=data["description"],
            appearance=data["appearance"],
            video=data.get("video"),
            raw_dict=data.copy(),
        )


@define(kw_only=True)
class Achievement:
    """
    Represents a single achievement in Marvel Rivals.

    Attributes
    ----------
    id : str
        Unique identifier for the achievement (Name if not exists).
    name : str
        Display name of the achievement.
    category : str
        Category the achievement belongs to (e.g., "Combat").
    points : int
        Point value of the achievement.
    icon : str
        Path to the achievement's icon image.
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    id: str
    name: str
    mission: str
    category: str
    points: int
    icon: str
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> Achievement:
        """
        Create an Achievement instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing achievement data.

        Returns
        -------
        Achievement
            A new Achievement instance.
        """
        return cls(
            id=data.get("id", data["name"]),
            name=data["name"],
            category=data["category"],
            points=data["points"],
            icon=data["icon"],
            mission=data["mission"],
            raw_dict=data.copy(),
        )

    @property
    def icon_url(self) -> str:
        """
        Get the full URL for the achievement icon.

        Returns
        -------
        str
            The complete URL to the achievement icon.
        """
        return image(self.icon)


@define(kw_only=True)
class AchievementList:
    """
    Represents a collection of achievements in Marvel Rivals.

    Attributes
    ----------
    total_achievements : int
        Total number of achievements available.
    achievements : list[Achievement]
        List of achievements.
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    total_achievements: int
    achievements: list[Achievement] = field(factory=list)
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> AchievementList:
        """
        Create an AchievementList instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing achievement list data.

        Returns
        -------
        AchievementList
            A new AchievementList instance.
        """
        return cls(
            total_achievements=data["total_achievements"],
            achievements=[
                Achievement.from_dict(achievement)
                for achievement in data.get("achievements", [])
            ],
            raw_dict=data.copy(),
        )

    def filter_by_category(self, category: str) -> list[Achievement]:
        """
        Filter achievements by category.

        Parameters
        ----------
        category : str
            The category to filter by.

        Returns
        -------
        list[Achievement]
            List of achievements in the specified category.
        """
        return [a for a in self.achievements if a.category.lower() == category.lower()]

    def get_achievement(self, achievement_id: str) -> Achievement | None:
        """
        Get an achievement by its ID.

        Parameters
        ----------
        achievement_id : str
            The achievement ID to look for.

        Returns
        -------
        Achievement | None
            The achievement if found, None otherwise.
        """
        for achievement in self.achievements:
            if achievement.id == achievement_id:
                return achievement
        return None

    def get_total_points(self) -> int:
        """
        Calculate the total points value of all achievements.

        Returns
        -------
        int
            Sum of points for all achievements.
        """
        return sum(achievement.points for achievement in self.achievements)


@define(kw_only=True)
class Item(Model):
    """
    Represents a collectible item in Marvel Rivals.

    Attributes
    ----------
    id : str
        Unique identifier for the item.
    name : str
        Display name of the item.
    quality : str
        Rarity/quality level of the item (e.g., "BLUE").
    type : str
        Type of the item (e.g., "Nameplate").
    associated_hero : str
        ID of the associated hero, or "0" if not hero-specific.
    slug : str
        URL-friendly identifier for the item.
    description : str | None
        Description of the item, if available.
    icon : str
        Path to the item's icon image.
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    id: str
    name: str
    quality: str
    type: str
    associated_hero: str
    slug: str
    description: str | None
    icon: str
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> Item:
        """
        Create an Item instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing item data.

        Returns
        -------
        Item
            A new Item instance.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            quality=data["quality"],
            type=data["type"],
            associated_hero=data["associated_hero"],
            slug=data["slug"],
            description=data.get("description"),
            icon=data["icon"],
            raw_dict=data.copy(),
        )

    @property
    def icon_url(self) -> str:
        """
        Get the full URL for the item icon.

        Returns
        -------
        str
            The complete URL to the item icon.
        """
        return image(self.icon)

    @property
    def is_hero_specific(self) -> bool:
        """
        Check if the item is associated with a specific hero.

        Returns
        -------
        bool
            True if the item is associated with a specific hero, False otherwise.
        """
        return self.associated_hero != "0"


@define(kw_only=True)
class ItemList(Model):
    """
    Represents a collection of items in Marvel Rivals.

    Attributes
    ----------
    total_items : int
        Total number of items available.
    items : list[Item]
        List of items.
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    total_items: int
    items: list[Item] = field(factory=list)
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> ItemList:
        """
        Create an ItemList instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing item list data.

        Returns
        -------
        ItemList
            A new ItemList instance.
        """
        return cls(
            total_items=data["total_items"],
            items=[Item.from_dict(item) for item in data.get("items", [])],
            raw_dict=data.copy(),
        )

    def filter_by_type(self, item_type: str) -> list[Item]:
        """
        Filter items by type.

        Parameters
        ----------
        item_type : str
            The item type to filter by.

        Returns
        -------
        list[Item]
            List of items of the specified type.
        """
        return [item for item in self.items if item.type.lower() == item_type.lower()]

    def filter_by_quality(self, quality: str) -> list[Item]:
        """
        Filter items by quality/rarity.

        Parameters
        ----------
        quality : str
            The quality to filter by.

        Returns
        -------
        list[Item]
            List of items with the specified quality.
        """
        return [item for item in self.items if item.quality.lower() == quality.lower()]

    def filter_by_hero(self, hero_id: str) -> list[Item]:
        """
        Filter items by associated hero.

        Parameters
        ----------
        hero_id : str
            The hero ID to filter by.

        Returns
        -------
        list[Item]
            List of items associated with the specified hero.
        """
        return [item for item in self.items if item.associated_hero == hero_id]

    def get_item(self, item_id: str) -> Item | None:
        """
        Get an item by its ID.

        Parameters
        ----------
        item_id : str
            The item ID to look for.

        Returns
        -------
        Item | None
            The item if found, None otherwise.
        """
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def get_item_by_slug(self, slug: str) -> Item | None:
        """
        Get an item by its slug.

        Parameters
        ----------
        slug : str
            The item slug to look for.

        Returns
        -------
        Item | None
            The item if found, None otherwise.
        """
        for item in self.items:
            if item.slug == slug:
                return item
        return None


@define(kw_only=True)
class BattlePassItem(Model):
    """
    Represents an item in the Battle Pass.

    Attributes
    ----------
    name : str
        Name of the Battle Pass item.
    image : str
        Path to the item's image.
    cost : str
        Cost to unlock the item (e.g., "Unlock To Claim").
    isLuxury : bool
        Whether this is a premium/luxury tier item.
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    name: str
    image: str
    cost: str
    isLuxury: bool
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> BattlePassItem:
        """
        Create a BattlePassItem instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing Battle Pass item data.

        Returns
        -------
        BattlePassItem
            A new BattlePassItem instance.
        """
        return cls(
            name=data["name"],
            image=data["image"],
            cost=data["cost"],
            isLuxury=data["isLuxury"],
            raw_dict=data.copy(),
        )

    @property
    def image_url(self) -> str:
        """
        Get the full URL for the item image.

        Returns
        -------
        str
            The complete URL to the item image.
        """
        return image(self.image)


@define(kw_only=True)
class BattlePass(Model):
    """
    Represents a Battle Pass season in Marvel Rivals.

    Attributes
    ----------
    season : int
        Battle Pass season number.
    season_name : str
        Name of the Battle Pass season.
    items : list[BattlePassItem]
        Items available in the Battle Pass.
    raw_dict : dict
        The original JSON data used to create this instance.
    """

    season: int
    season_name: str
    items: list[BattlePassItem] = field(factory=list)
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> BattlePass:
        """
        Create a BattlePass instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing Battle Pass data.

        Returns
        -------
        BattlePass
            A new BattlePass instance.
        """
        return cls(
            season=data["season"],
            season_name=data["season_name"],
            items=[BattlePassItem.from_dict(item) for item in data.get("items", [])],
            raw_dict=data.copy(),
        )

    def get_free_items(self) -> list[BattlePassItem]:
        """
        Get all free (non-luxury) items in the Battle Pass.

        Returns
        -------
        list[BattlePassItem]
            List of free items.
        """
        return [item for item in self.items if not item.isLuxury]

    def get_premium_items(self) -> list[BattlePassItem]:
        """
        Get all premium (luxury) items in the Battle Pass.

        Returns
        -------
        list[BattlePassItem]
            List of premium items.
        """
        return [item for item in self.items if item.isLuxury]

    def find_item(self, name: str) -> BattlePassItem | None:
        """
        Find a Battle Pass item by name.

        Parameters
        ----------
        name : str
            The item name to search for.

        Returns
        -------
        BattlePassItem | None
            The matching item if found, None otherwise.
        """
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None


@define(kw_only=True)
class SubMap(Model):
    """
    Represents a sub-map within a main map in Marvel Rivals.

    Attributes
    ----------
    id : int
        Unique identifier for the sub-map.
    name : str | None
        Name of the sub-map, if available.
    thumbnail : str | None
        Path to the sub-map's thumbnail image, if available.
    raw_dict : dict
        The original JSON data used to create this instance.
    """
    id: int
    name: str | None = None
    thumbnail: str | None = None
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> SubMap:
        """
        Create a SubMap instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing sub-map data.

        Returns
        -------
        SubMap
            A new SubMap instance.
        """
        return cls(
            id=data["id"],
            name=data.get("name"),
            thumbnail=data.get("thumbnail"),
            raw_dict=data.copy(),
        )


@define(kw_only=True)
class Map(Model):
    """
    Represents a game map in Marvel Rivals.

    Attributes
    ----------
    id : int
        Unique identifier for the map.
    name : str
        Short name of the map.
    full_name : str
        Complete name of the map including location.
    location : str
        Location/realm where the map is set.
    description : str
        Lore description of the map.
    game_mode : str
        Game mode associated with this map (e.g., "Convoy", "Convergence").
    is_competitive : bool
        Whether the map is available in competitive play.
    sub_map : SubMap
        Information about sub-areas within the map.
    video : str
        URL to a video showcase of the map.
    images : list[str]
        List of image paths for the map in different sizes.
    raw_dict : dict
        The original JSON data used to create this instance.
    """
    id: int
    name: str
    full_name: str
    location: str
    description: str
    game_mode: str
    is_competitive: bool
    sub_map: SubMap
    video: str
    images: list[str] = field(factory=list)
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> Map:
        """
        Create a Map instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing map data.

        Returns
        -------
        Map
            A new Map instance.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            full_name=data["full_name"],
            location=data["location"],
            description=data.get("description", "Not provided"),
            game_mode=data["game_mode"],
            is_competitive=data.get("is_competitive", False),
            sub_map=SubMap.from_dict(data["sub_map"]),
            video=data["video"],
            images=data.get("images", []),
            raw_dict=data.copy(),
        )

    @property
    def thumbnail_url(self) -> str | None:
        """
        Get the URL for the map's thumbnail image.

        Returns
        -------
        str | None
            The URL to the map's thumbnail image, or None if not available.
        """
        if not self.images:
            return None
        return image(self.images[0])

    @property
    def medium_image_url(self) -> str | None:
        """
        Get the URL for the map's medium-sized image.

        Returns
        -------
        str | None
            The URL to the map's medium image, or None if not available.
        """
        if len(self.images) < 2:
            return self.thumbnail_url
        return image(self.images[1])

    @property
    def large_image_url(self) -> str | None:
        """
        Get the URL for the map's large-sized image.

        Returns
        -------
        str | None
            The URL to the map's large image, or None if not available.
        """
        if len(self.images) < 3:
            return self.medium_image_url
        return image(self.images[2])

    @property
    def video_id(self) -> str | None:
        """
        Extract the YouTube video ID from the video URL.

        Returns
        -------
        str | None
            The YouTube video ID if the URL is a YouTube link, None otherwise.
        """
        if not self.video or "youtu" not in self.video:
            return None

        if "youtube.com/watch" in self.video:
            import re
            pattern = r"v=([a-zA-Z0-9_-]+)"
            match = re.search(pattern, self.video)
            return match.group(1) if match else None
        elif "youtu.be/" in self.video:
            return self.video.split("youtu.be/")[1].split("?")[0]
        return None


@define(kw_only=True)
class MapList(Model):
    """
    Represents a collection of maps in Marvel Rivals.

    Attributes
    ----------
    total_maps : int
        Total number of maps available.
    maps : list[Map]
        List of maps.
    raw_dict : dict
        The original JSON data used to create this instance.
    """
    total_maps: int
    maps: list[Map] = field(factory=list)
    raw_dict: dict[str, typing.Any] = field(factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> MapList:
        """
        Create a MapList instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing map list data.

        Returns
        -------
        MapList
            A new MapList instance.
        """
        return cls(
            total_maps=data["total_maps"],
            maps=[Map.from_dict(map_data) for map_data in data.get("maps", [])],
            raw_dict=data.copy(),
        )

    def filter_by_game_mode(self, game_mode: str) -> list[Map]:
        """
        Filter maps by game mode.

        Parameters
        ----------
        game_mode : str
            The game mode to filter by (e.g., "Convoy", "Convergence").

        Returns
        -------
        list[Map]
            List of maps with the specified game mode.
        """
        return [map for map in self.maps if map.game_mode.lower() == game_mode.lower()]

    def filter_by_location(self, location: str) -> list[Map]:
        """
        Filter maps by location.

        Parameters
        ----------
        location : str
            The location to filter by (e.g., "Yggsgard", "Tokyo 2099").

        Returns
        -------
        list[Map]
            List of maps in the specified location.
        """
        return [map for map in self.maps if map.location.lower() == location.lower()]

    def get_competitive_maps(self) -> list[Map]:
        """
        Get all maps that are available in competitive play.

        Returns
        -------
        list[Map]
            List of competitive maps.
        """
        return [map for map in self.maps if map.is_competitive]

    def get_map(self, map_id: int) -> Map | None:
        """
        Get a map by its ID.

        Parameters
        ----------
        map_id : int
            The map ID to look for.

        Returns
        -------
        Map | None
            The map if found, None otherwise.
        """
        for map in self.maps:
            if map.id == map_id:
                return map
        return None

    def get_map_by_name(self, name: str) -> Map | None:
        """
        Get a map by its name.

        Parameters
        ----------
        name : str
            The map name to look for.

        Returns
        -------
        Map | None
            The map if found, None otherwise.
        """
        for map in self.maps:
            if map.name.lower() == name.lower():
                return map
        return None
