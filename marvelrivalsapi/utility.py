from __future__ import annotations

import typing
from enum import Enum, IntEnum

import httpx

ReturnStr = typing.Callable[..., str]
StrReturnStr = typing.Callable[[str], str]

__all__ = ("Endpoints", "Heroes", "MarvelRivalsAPIError", "image")


class MarvelRivalsAPIError(Exception):
    """
    Base class for all exceptions raised by the MarvelRivalsAPI.

    This exception is raised when an API request fails due to an error
    returned by the server.

    Parameters
    ----------
    res : httpx.Response
        The HTTP response that resulted in the error.

    Attributes
    ----------
    response : httpx.Response
        The HTTP response object containing error details.
    """

    def __init__(self, res: httpx.Response) -> None:
        self.response = res
        try:
            message = f"{res.status_code}: {res.json()['error']}"
        except:
            message = f"{res.status_code}: {res.text}"
        super().__init__(message)


class Heroes(Enum):
    """
    Enum of all heroes available in the Marvel Rivals API.

    This enumeration provides convenient access to all hero identifiers
    that can be used with the API. Hero names are standardized to lowercase
    with appropriate spacing.

    Examples
    --------
    >>> from marvelrivalsapi.utility import Heroes
    >>> Heroes.SPIDER_MAN.value
    'spider-man'
    """

    HULK = "hulk"
    THE_PUNISHER = "the punisher"
    STORM = "storm"
    LOKI = "loki"
    HUMAN_TORCH = "human torch"
    DOCTOR_STRANGE = "doctor strange"
    MANTIS = "mantis"
    HAWKEYE = "hawkeye"
    CAPTAIN_AMERICA = "captain america"
    ROCKET_RACCOON = "rocket raccoon"
    HELA = "hela"
    CLOAK_AND_DAGGER = "cloak & dagger"
    BLACK_PANTHER = "black panther"
    GROOT = "groot"
    MAGIK = "magik"
    MOON_KNIGHT = "moon knight"
    LUNA_SNOW = "luna snow"
    SQUIRREL_GIRL = "squirrel girl"
    BLACK_WIDOW = "black widow"
    IRON_MAN = "iron man"
    VENOM = "venom"
    SPIDER_MAN = "spider-man"
    MAGNETO = "magneto"
    SCARLET_WITCH = "scarlet witch"
    THOR = "thor"
    MISTER_FANTASTIC = "mister fantastic"
    WINTER_SOLDIER = "winter soldier"
    PENI_PARKER = "peni parker"
    STAR_LORD = "star-lord"
    NAMOR = "namor"
    ADAM_WARLOCK = "adam warlock"
    JEFF_THE_LAND_SHARK = "jeff the land shark"
    PSYLOCKE = "psylocke"
    WOLVERINE = "wolverine"
    INVISIBLE_WOMAN = "invisible woman"
    THE_THING = "the thing"
    IRON_FIST = "iron fist"
    EMMA_FROST = "emma frost"


class LoginOS(IntEnum):
    PC = 1
    PS = 2
    XBOX = 3


class Endpoints:
    """
    Collection of API endpoint URL generators.

    This class provides methods to generate URLs for different API endpoints.
    All methods return fully qualified URLs that can be used with HTTP clients.

    Attributes
    ----------
    BASE_IMAGE_URL : Callable
        Returns the base URL for hero images.
    ALL_HEROES : Callable
        Returns the URL for retrieving all heroes.
    GET_HERO : Callable
        Returns the URL for retrieving a specific hero by ID.

    Examples
    --------
    >>> from marvelrivalsapi.utility import Endpoints
    >>> Endpoints.ALL_HEROES()
    'https://marvelrivalsapi.com/api/v1/heroes'
    >>> Endpoints.GET_HERO("spider-man")
    'https://marvelrivalsapi.com/api/v1/heroes/hero/spider-man'
    """

    BASE_IMAGE_URL: ReturnStr = lambda *_: "https://marvelrivalsapi.com/rivals"
    ALL_HEROES: ReturnStr = lambda *_: "https://marvelrivalsapi.com/api/v1/heroes"
    GET_HERO: StrReturnStr = (
        lambda hero_id: f"https://marvelrivalsapi.com/api/v1/heroes/hero/{hero_id}"
    )
    HERO_STATS: StrReturnStr = (
        lambda hero_id: f"https://marvelrivalsapi.com/api/v1/heroes/hero/{hero_id}/stats"
    )
    HERO_LEADERBOARD: typing.Callable[[str, str], str] = lambda hero, platform: (
        f"https://marvelrivalsapi.com/api/v1/heroes/leaderboard/{hero}?platform={platform}"
    )
    ALL_COSTUMES: StrReturnStr = lambda hero_id: (
        f"https://marvelrivalsapi.com/api/v1/heroes/hero/{hero_id}/costumes"
    )
    GET_COSTUME: typing.Callable[[str, str], str] = lambda hero_id, costume_id: (
        f"https://marvelrivalsapi.com/api/v1/heroes/hero/{hero_id}/costume/{costume_id}"
    )


def image(url: str) -> str:
    """
    Returns the full URL for an image resource.

    This function prepends the base image URL to the provided image path.

    Parameters
    ----------
    url : str
        The relative path of the image resource.

    Returns
    -------
    str
        The complete URL to the image resource.

    Examples
    --------
    >>> from marvelrivalsapi.utility import image
    >>> image("/heroes/spider-man/icon.png")
    'https://marvelrivalsapi.com/rivals/heroes/spider-man/icon.png'
    """
    return f"{Endpoints.BASE_IMAGE_URL()}{url.split('rivals')[1]}"
