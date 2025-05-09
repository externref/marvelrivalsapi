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

import typing

import httpx
from attrs import define, field

from marvelrivalsapi.models import (Achievement, AchievementList, BattlePass,
                                    Costume, CostumePremiumWrapper, Hero,
                                    HeroLeaderboard, HeroStat, Item, ItemList)
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
    error : bool
        If True, raises an error on failure instead of returning None (Defaults to False).

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
    error: bool = field(default=False)
    client: httpx.AsyncClient = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.client = httpx.AsyncClient(headers={"x-api-key": self.api_key})

    def throw(self, res: httpx.Response) -> typing.NoReturn:
        raise MarvelRivalsAPIError(res)

    async def _handle_error(
        self, response: httpx.Response, error: bool | None
    ) -> typing.NoReturn | None:
        should_raise = error if error is not None else self.error
        if should_raise:
            self.throw(response)
        return None

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
            The method will also error if the client's error attribute is True.

        Returns
        -------
        Hero | None
            The hero if found, None if not found and neither error parameters are True.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and either error parameter is True.

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
        return await self._handle_error(response, error)

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
        return await self._handle_error(response, error)

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
        return await self._handle_error(response, error)

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
        return await self._handle_error(response, error)

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
        return await self._handle_error(response, error)

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
        return await self._handle_error(response, error)

    @typing.overload
    async def get_all_achievements(
        self, *, query: str, page: int | None, limit: int | None, error: bool = False
    ) -> AchievementList: ...

    @typing.overload
    async def get_all_achievements(
        self,
        *,
        query: str | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> AchievementList | None: ...

    @typing.overload
    async def get_all_achievements(self, *, error: bool) -> AchievementList | None: ...

    async def get_all_achievements(
        self,
        *,
        query: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        error: bool = False,
    ) -> AchievementList | None:
        """
        Get all achievements.

        Parameters
        ----------
        query : str | None
            The query string to filter achievements by name.
        page : int | None
            The page number for pagination.
        limit : int | None
            The number of achievements to return per page.

        Returns
        -------
        AchievementList | None
            A list of all achievements if successful, None if the request fails.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> client = MarvelRivalsClient("your-api-key")
        >>> achievements = client.get_all_achievements()
        >>> if achievements:
        ...     for achievement in achievements:
        ...         print(achievement.name)
        """

        response = await self.client.get(
            Endpoints.ALL_ACHIVEMENTS(query=query, page=page, limit=limit)
        )

        if response.status_code == 200:
            return AchievementList.from_dict(response.json())

        return await self._handle_error(response, error)

    @typing.overload
    async def get_achievement(
        self, achievement: str, *, error: bool
    ) -> Achievement: ...

    @typing.overload
    async def get_achievement(self, achievement: str) -> Achievement | None: ...

    async def get_achievement(
        self, achievement: str, *, error: bool = False
    ) -> Achievement | None:
        """
        Get a specific achievement by Name.

        Parameters
        ----------
        achievement : str
            The name of the achievement to retrieve.

        Returns
        -------
        Achievement | None
            The achievement if found, None if not found.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> client = MarvelRivalsClient("your-api-key")
        >>> achievement = client.get_achievement("some-achievement-name")
        >>> if achievement:
        ...     print(achievement.name)
        """

        response = await self.client.get(Endpoints.GET_ACHIVEMENT(achievement))

        if response.status_code == 200:
            return Achievement.from_dict(response.json())

        return await self._handle_error(response, error)

    @typing.overload
    async def get_all_items(
        self, *, query: str, page: int | None, limit: int | None, error: bool = True
    ) -> ItemList: ...

    @typing.overload
    async def get_all_items(self, *, error: bool) -> ItemList: ...

    @typing.overload
    async def get_all_items(
        self,
        *,
        query: str | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> ItemList | None: ...

    async def get_all_items(
        self,
        *,
        query: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        error: bool = False,
    ) -> ItemList | None:
        """
        Get all items.

        Parameters
        ----------
        query : str | None
            The query string to filter items by name.
        page : int | None
            The page number for pagination.
        limit : int | None
            The number of items to return per page.
        error : bool | None
            If True, raises an error on failure instead of returning None.

        Returns
        -------
        ItemList | None
            A list of all items if successful, None if the request fails.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> client = MarvelRivalsClient("your-api-key")
        >>> items = client.get_all_items()
        >>> if items:
        ...     for item in items:
        ...         print(item.name)
        """

        response = await self.client.get(
            Endpoints.ALL_ITEMS(query=query, page=page, limit=limit)
        )

        if response.status_code == 200:
            return ItemList.from_dict(response.json())

        return await self._handle_error(response, error)

    @typing.overload
    async def get_item(self, item: str, *, error: bool) -> Item: ...

    @typing.overload
    async def get_item(self, item: str) -> Item | None: ...

    async def get_item(self, item: str, *, error: bool = False) -> Item | None:
        """
        Get a specific item by ID.

        Parameters
        ----------
        item : str
            The ID of the item to retrieve.
        error : bool | None
            If True, raises an error on failure instead of returning None.

        Returns
        -------
        Item | None
            The item if found, None if not found.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and error is True.

        Examples
        --------
        >>> client = MarvelRivalsClient("your-api-key")
        >>> item = client.get_item("some-item-name")
        >>> if item:
        ...     print(item.name)
        """

        response = await self.client.get(Endpoints.GET_ITEM(item))

        if response.status_code == 200:
            return Item.from_dict(response.json())

        return await self._handle_error(response, error)

    @typing.overload
    async def get_battlepass(self, season: float, *, error: bool) -> BattlePass: ...

    @typing.overload
    async def get_battlepass(self, season: float) -> BattlePass | None: ...

    async def get_battlepass(
        self, season: float, *, error: bool = False
    ) -> BattlePass | None:
        """
        Get a specific battlepass by season asynchronously.

        Parameters
        ----------
        season : float
            The season of the battlepass to retrieve.
        error : bool
            If True, raises an error on failure instead of returning None.
            The method will also error if the client's error attribute is True.

        Returns
        -------
        BattlePass | None
            The battlepass if found, None if not found and neither error parameters are True.

        Raises
        ------
        MarvelRivalsAPIError
            When the API request fails and either error parameter is True.

        Examples
        --------
        >>> async with AsyncMarvelRivalsClient("your-api-key") as client:
        ...     battlepass = await client.get_battlepass(1.0)
        ...     if battlepass:
        ...         print(battlepass.season_name)
        """
        response = await self.client.get(Endpoints.GET_BATTLEPASS(str(season)))

        if response.status_code == 200:
            return BattlePass.from_dict(response.json())

        return await self._handle_error(response, error)

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
