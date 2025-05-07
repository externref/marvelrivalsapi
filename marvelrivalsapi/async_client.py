from __future__ import annotations

import typing

import httpx
from attrs import define, field

from marvelrivalsapi.utility import Endpoints, Heroes, MarvelRivalsAPIError
from marvelrivalsapi.models import Hero

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
        response = await self.client.get(Endpoints.GET_HERO(hero.value if isinstance(hero, Heroes) else hero))
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
        return None if not error else  self.throw(response)
    
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