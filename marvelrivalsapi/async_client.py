from __future__ import annotations

import typing

import httpx
from attrs import define, field

from marvelrivalsapi.models import (Costume, CostumePremiumWrapper, Hero,
                                    HeroLeaderboard, HeroStat)
from marvelrivalsapi.utility import Endpoints, Heroes, MarvelRivalsAPIError

__all__ = ("AsyncMarvelRivalsClient",)


@define
class AsyncMarvelRivalsClient:
    """
    Asynchronous client for interacting with the Marvel Rivals API.

    This client allows for fetching hero data from the Marvel Rivals API
    using asynchronous HTTP requests.

    Parameters
    ----------
    api_key : str
        The API key to authenticate requests to the Marvel Rivals API.

    Attributes
    ----------
    client : httpx.AsyncClient
        The HTTP client used for making asynchronous requests.

    Examples
    --------
    >>> import asyncio
    >>> from marvelrivalsapi import AsyncMarvelRivalsClient
    >>>
    >>> async def main():
    ...     client = AsyncMarvelRivalsClient("your-api-key")
    ...     hero = await client.get_hero("spider-man")
    ...     print(hero.name)
    ...     await client.close()
    >>>
    >>> asyncio.run(main())
    """

    api_key: str
    client: httpx.AsyncClient = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.client = httpx.AsyncClient(headers={"x-api-key": self.api_key})

    def throw(self, res: httpx.Response) -> None:
        raise MarvelRivalsAPIError(res)

    @typing.overload
    async def get_hero(self, hero: str | Heroes, *, error: bool) -> Hero: ...

    @typing.overload
    async def get_hero(self, hero: str | Heroes) -> Hero | None: ...

    async def get_hero(self, hero: str | Heroes, *, error: bool = False) -> Hero | None:
        """
        Get a hero by name or ID asynchronously.

        Parameters
        ----------
        hero : str | Heroes
            The hero name or ID to retrieve.
        error : bool
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
        >>> async with AsyncMarvelRivalsClient("your-api-key") as client:
        ...     hero = await client.get_hero("spider-man")
        ...     if hero:
        ...         print(hero.name)
        """
        response = await self.client.get(
            Endpoints.GET_HERO(hero.value if isinstance(hero, Heroes) else hero)
        )
        if response.status_code == 200:
            return Hero.from_dict(response.json())
        return None if not error else self.throw(response)

    @typing.overload
    async def get_all_heroes(self, *, error: bool) -> list[Hero]: ...

    @typing.overload
    async def get_all_heroes(self) -> list[Hero] | None: ...

    async def get_all_heroes(self, *, error: bool = False) -> list[Hero] | None:
        """
        Get all available heroes asynchronously.

        Parameters
        ----------
        error : bool
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
        >>> async with AsyncMarvelRivalsClient("your-api-key") as client:
        ...     heroes = await client.get_all_heroes()
        ...     if heroes:
        ...         for hero in heroes:
        ...             print(hero.name)
        """
        response = await self.client.get(Endpoints.ALL_HEROES())
        if response.status_code == 200:
            return [Hero.from_dict(hero) for hero in response.json()]
        return None if not error else self.throw(response)

    @typing.overload
    async def get_hero_stats(self, hero: str | Heroes, *, error: bool) -> HeroStat: ...

    @typing.overload
    async def get_hero_stats(self, hero: str | Heroes) -> HeroStat | None: ...

    async def get_hero_stats(
        self, hero: str | Heroes, *, error: bool = False
    ) -> HeroStat | None:
        """
        Get statistics for a specific hero asynchronously.

        Parameters
        ----------
        hero : str | Heroes
            The hero name or ID to retrieve stats for.
        error : bool
            If True, raises an error on failure instead of returning None.
            Default is False.

        Returns
        -------
        HeroStat | None
            The hero statistics if found, None if not found and error is False.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> async with AsyncMarvelRivalsClient("your-api-key") as client:
        ...     stats = await client.get_hero_stats("Spider-Man")
        ...     if stats:
        ...         print(f"Win rate: {stats.win_rate:.2%}")
        """
        response = await self.client.get(
            Endpoints.HERO_STATS(hero.value if isinstance(hero, Heroes) else hero)
        )
        if response.status_code == 200:
            return HeroStat.from_dict(response.json())
        return None if not error else self.throw(response)

    @typing.overload
    async def get_hero_leaderboard(
        self, hero: str | Heroes, platform: str, *, error: bool
    ) -> HeroLeaderboard: ...

    @typing.overload
    async def get_hero_leaderboard(
        self, hero: str | Heroes, platform: str
    ) -> HeroLeaderboard | None: ...

    @typing.overload
    async def get_hero_leaderboard(
        self, hero: str | Heroes, *, error: bool
    ) -> HeroLeaderboard: ...

    @typing.overload
    async def get_hero_leaderboard(
        self, hero: str | Heroes
    ) -> HeroLeaderboard | None: ...

    async def get_hero_leaderboard(
        self, hero: str | Heroes, platform: str = "pc", *, error: bool = False
    ) -> HeroLeaderboard | None:
        """
        Get the leaderboard for a specific hero and platform asynchronously.

        Parameters
        ----------
        hero : str | Heroes
            The hero name or ID to retrieve the leaderboard for.
        platform : str
            The platform to filter the leaderboard by.
        error : bool
            If True, raises an error on failure instead of returning None.
            Default is False.

        Returns
        -------
        HeroLeaderboard | None
            The leaderboard data if found, None if not found and error is False.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> async with AsyncMarvelRivalsClient("your-api-key") as client:
        ...     leaderboard = await client.get_hero_leaderboard("spider-man")
        ...     if leaderboard:
        ...         for entry in leaderboard.entries:
        ...             print(f"{entry.name}: {entry.score}")
        """
        response = await self.client.get(
            Endpoints.HERO_LEADERBOARD(
                hero.value if isinstance(hero, Heroes) else hero, platform
            )
        )
        if response.status_code == 200:
            return HeroLeaderboard.from_dict(response.json())
        return None if not error else self.throw(response)

    @typing.overload
    async def get_hero_costumes(
        self, hero: str | Heroes, *, error: bool
    ) -> list[Costume]: ...

    @typing.overload
    async def get_hero_costumes(self, hero: str | Heroes) -> list[Costume] | None: ...

    async def get_hero_costumes(
        self, hero: str | Heroes, *, error: bool = False
    ) -> list[Costume] | None:
        """
        Get all costumes for a specific hero asynchronously.

        Parameters
        ----------
        hero : str | Heroes
            The hero name or ID to retrieve costumes for.
        error : bool
            If True, raises an error on failure instead of returning None.
            Default is False.

        Returns
        -------
        list[Costume] | None
            A list of costumes if found, None if not found and error is False.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> async with AsyncMarvelRivalsClient("your-api-key") as client:
        ...     costumes = await client.get_hero_costumes("spider-man")
        ...     if costumes:
        ...         for costume in costumes:
        ...             print(costume.name)
        """
        response = await self.client.get(
            Endpoints.ALL_COSTUMES(hero.value if isinstance(hero, Heroes) else hero)
        )
        if response.status_code == 200:
            return [Costume.from_dict(costume) for costume in response.json()]
        return None if not error else self.throw(response)

    @typing.overload
    async def get_costume(
        self, hero: str | Heroes, costume_id: str, *, error: bool
    ) -> Costume: ...

    @typing.overload
    async def get_costume(
        self, hero: str | Heroes, costume_id: str
    ) -> Costume | None: ...

    async def get_costume(
        self, hero: str | Heroes, costume_id: str, *, error: bool = False
    ) -> Costume | None:
        """
        Get a specific costume for a hero asynchronously.

        Parameters
        ----------
        hero : str | Heroes
            The hero name or ID to retrieve the costume for.
        costume_id : str
            The ID of the costume to retrieve.
        error : bool
            If True, raises an error on failure instead of returning None.
            Default is False.

        Returns
        -------
        Costume | None
            The costume if found, None if not found and error is False.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> async with AsyncMarvelRivalsClient("your-api-key") as client:
        ...     costume = await client.get_costume("squirrel girl", "Cheerful Dragoness")
        ...     if costume:
        ...         print(costume.name)
        """
        response = await self.client.get(
            Endpoints.GET_COSTUME(
                hero.value if isinstance(hero, Heroes) else hero, costume_id
            )
        )
        if response.status_code == 200:
            return CostumePremiumWrapper.from_dict(response.json())
        return None if not error else self.throw(response)

    async def close(self) -> None:
        """
        Close the HTTP client session.

        This method should be called when the client is no longer needed to
        properly clean up resources.

        Examples
        --------
        >>> async def main():
        ...     client = AsyncMarvelRivalsClient("your-api-key")
        ...     # Use the client...
        ...     await client.close()
        """
        await self.client.aclose()

    async def __aenter__(self) -> AsyncMarvelRivalsClient:
        return self

    async def __aexit__(self, *args: typing.Any) -> None:
        await self.close()
