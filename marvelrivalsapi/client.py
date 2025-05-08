from __future__ import annotations

import typing

import httpx
from attrs import define, field

from marvelrivalsapi.models import (Costume, CostumePremiumWrapper, Hero,
                                    HeroLeaderboard, HeroStat)
from marvelrivalsapi.utility import Endpoints, Heroes, MarvelRivalsAPIError

__all__ = ("MarvelRivalsClient",)


@define
class MarvelRivalsClient:
    """
    Client for interacting with the Marvel Rivals API.

    This client allows for fetching hero data from the Marvel Rivals API.

    Parameters
    ----------
    api_key : str
        The API key to authenticate requests to the Marvel Rivals API.

    Attributes
    ----------
    client : httpx.Client
        The HTTP client used for making requests.
    """

    api_key: str
    client: httpx.Client = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.client = httpx.Client(headers={"x-api-key": self.api_key})

    def throw(self, res: httpx.Response) -> None:
        raise MarvelRivalsAPIError(res)

    @typing.overload
    def get_hero(self, hero: str | Heroes, *, error: bool) -> Hero: ...

    @typing.overload
    def get_hero(self, hero: str | Heroes) -> Hero | None: ...

    def get_hero(self, hero: str | Heroes, *, error: bool = False) -> Hero | None:
        """
        Get a hero by name or ID.

        Parameters
        ----------
        hero : str | Heroes
            The hero name or ID to retrieve.
        error : bool | None
            If True, raises an error on failure instead of returning None.
            Default is False.

        Returns
        -------
        Hero | None
            The hero if found, None if not found and error is False.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> client = MarvelRivalsClient("your-api-key")
        >>> hero = client.get_hero("Spider-Man")
        >>> if hero:
        ...     print(hero.name)
        """
        response = self.client.get(
            Endpoints.GET_HERO(hero.value if isinstance(hero, Heroes) else hero)
        )
        if response.status_code == 200:
            return Hero.from_dict(response.json())
        return None if not error else self.throw(response)

    @typing.overload
    def get_all_heroes(self, *, error: bool) -> list[Hero]: ...

    @typing.overload
    def get_all_heroes(
        self,
    ) -> list[Hero] | None: ...

    def get_all_heroes(self, *, error: bool = False) -> list[Hero] | None:
        """
        Get all available heroes.

        Parameters
        ----------
        error : bool | None
            If True, raises an error on failure instead of returning None.
            Default is False.

        Returns
        -------
        list[Hero] | None
            A list of all heroes if successful, None if the request fails and error is False.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> client = MarvelRivalsClient("your-api-key")
        >>> heroes = client.get_all_heroes()
        >>> if heroes:
        ...     for hero in heroes:
        ...         print(hero.name)
        """
        response = self.client.get(Endpoints.ALL_HEROES())
        if response.status_code == 200:
            return [Hero.from_dict(hero) for hero in response.json()]
        return None if not error else self.throw(response)

    @typing.overload
    def get_hero_stat(self, hero: str | Heroes, *, error: bool) -> HeroStat: ...

    @typing.overload
    def get_hero_stat(self, hero: str | Heroes) -> HeroStat | None: ...

    def get_hero_stat(
        self, hero: str | Heroes, *, error: bool = False
    ) -> HeroStat | None:
        """
        Get hero stats by name or ID.

        Parameters
        ----------
        hero : str | Heroes
            The hero name or ID to retrieve stats for.
        error : bool | None
            If True, raises an error on failure instead of returning None.
            Default is False.

        Returns
        -------
        dict[str, typing.Any] | None
            The hero stats if found, None if not found and error is False.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> client = MarvelRivalsClient("your-api-key")
        >>> stats = client.get_hero_stat("spider-man")
        >>> if stats:
        ...     print(stats)
        """
        response = self.client.get(
            Endpoints.HERO_STATS(hero.value if isinstance(hero, Heroes) else hero)
        )
        if response.status_code == 200:
            print(response.json())
            return HeroStat.from_dict(response.json())
        return None if not error else self.throw(response)

    @typing.overload
    def get_hero_leaderboard(
        self, hero: str | Heroes, platform: str, *, error: bool
    ) -> HeroLeaderboard: ...

    @typing.overload
    def get_hero_leaderboard(
        self, hero: str | Heroes, platform: str
    ) -> HeroLeaderboard | None: ...

    @typing.overload
    def get_hero_leaderboard(
        self, hero: str | Heroes, *, error: bool
    ) -> HeroLeaderboard: ...

    @typing.overload
    def get_hero_leaderboard(self, hero: str | Heroes) -> HeroLeaderboard | None: ...

    def get_hero_leaderboard(
        self, hero: str | Heroes, platform: str = "pc", *, error: bool = False
    ) -> HeroLeaderboard | None:
        """
        Get hero leaderboard by name or ID.

        Parameters
        ----------
        hero : str | Heroes
            The hero name or ID to retrieve stats for.
        error : bool | None
            If True, raises an error on failure instead of returning None.
            Default is False.

        Returns
        -------
        dict[HeroLeaderboard] | None
            The hero stats if found, None if not found and error is False.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> client = MarvelRivalsClient("your-api-key")
        >>> stats = client.get_hero_leaderboard("spider-man")
        >>> if stats:
        ...     print(stats)
        """
        response = self.client.get(
            Endpoints.HERO_LEADERBOARD(
                hero.value if isinstance(hero, Heroes) else hero, platform
            )
        )
        if response.status_code == 200:
            return HeroLeaderboard.from_dict(response.json())
        return None if not error else self.throw(response)

    @typing.overload
    def get_hero_costumes(
        self, hero: str | Heroes, *, error: bool
    ) -> list[Costume]: ...

    @typing.overload
    def get_hero_costumes(self, hero: str | Heroes) -> list[Costume] | None: ...

    def get_hero_costumes(
        self, hero: str | Heroes, *, error: bool = False
    ) -> list[Costume] | None:
        """
        Get all costumes for a specific hero.

        Parameters
        ----------
        hero : str | Heroes
            The hero name or ID to retrieve costumes for.
        error : bool | None
            If True, raises an error on failure instead of returning None.
            Default is False.

        Returns
        -------
        list[Costume] | None
            A list of all costumes for the specified hero if successful,
            None if the request fails and error is False.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> client = MarvelRivalsClient("your-api-key")
        >>> costumes = client.get_hero_costumes("spider-man")
        >>> if costumes:
        ...     for costume in costumes:
        ...         print(costume.name)
        """
        response = self.client.get(
            Endpoints.ALL_COSTUMES(hero.value if isinstance(hero, Heroes) else hero)
        )
        if response.status_code == 200:
            return [Costume.from_dict(costume) for costume in response.json()]
        return None if not error else self.throw(response)

    @typing.overload
    def get_costume(
        self, hero: str | Heroes, costume_id: str, *, error: bool
    ) -> Costume: ...

    @typing.overload
    def get_costume(self, hero: str | Heroes, costume_id: str) -> Costume | None: ...

    def get_costume(
        self, hero: str | Heroes, costume_id: str, *, error: bool = False
    ) -> Costume | None:
        """
        Get a specific costume for a hero.

        Parameters
        ----------
        hero : str | Heroes
            The hero name or ID to retrieve the costume for.
        costume_id : str
            The ID of the costume to retrieve.

        Returns
        -------
        Costume | None
            The costume if found, None if not found.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> client = MarvelRivalsClient("your-api-key")
        >>> costume = client.get_costume("squirrel girl", "Cheerful Dragoness")
        ... if costume:
        ...     print(costume.name)
        """
        response = self.client.get(
            Endpoints.GET_COSTUME(
                hero.value if isinstance(hero, Heroes) else hero, costume_id
            )
        )
        if response.status_code == 200:
            return CostumePremiumWrapper.from_dict(response.json())
        return None if not error else self.throw(response)
