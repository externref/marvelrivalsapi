from __future__ import annotations

import typing

import httpx
from attrs import define, field

from marvelrivalsapi.utility import Endpoints, Heroes, MarvelRivalsAPIError
from marvelrivalsapi.models import Hero

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
        response = self.client.get(Endpoints.GET_HERO(hero.value if isinstance(hero, Heroes) else hero))
        if response.status_code == 200:
            return Hero.from_dict(response.json())
        return None if not error else self.throw(response)
    
    @typing.overload
    def get_all_heroes(self, *, error: bool) -> list[Hero]: ...

    @typing.overload
    def get_all_heroes(self,) -> list[Hero] | None: ...


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