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

from marvelrivalsapi.utility import LoginOS

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
