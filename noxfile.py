import os

import dotenv
import nox

import marvelrivalsapi

dotenv.load_dotenv()
client = marvelrivalsapi.MarvelRivalsClient(os.environ["API_KEY"])


@nox.session(venv_backend="none")
def get_heroes(session: nox.Session) -> None:
    heroes = client.get_all_heroes()
    assert heroes is not None, "Failed to get heroes"


@nox.session(venv_backend="none")
def get_hero(session: nox.Session) -> None:
    heroes = client.get_hero(marvelrivalsapi.Heroes.EMMA_FROST)
    assert heroes is not None, "Failed to get hero"


@nox.session(venv_backend="none")
def get_hero_leaderboard(session: nox.Session) -> None:
    heroes = client.get_hero_leaderboard(marvelrivalsapi.Heroes.EMMA_FROST)
    assert heroes is not None, "Failed to get hero leaderboard"


@nox.session(venv_backend="none")
def get_hero_costumes(session: nox.Session) -> None:
    heroes = client.get_hero_costumes(marvelrivalsapi.Heroes.EMMA_FROST)
    assert heroes is not None, "Failed to get hero costumes"


@nox.session(venv_backend="none")
def get_all_achievements(session: nox.Session) -> None:
    achievements = client.get_all_achievements()
    assert achievements is not None, "Failed to get all achievements"


@nox.session(venv_backend="none")
def get_achievement(session: nox.Session) -> None:
    achievements = client.get_achievement("Sticking Around")
    assert achievements is not None, "Failed to get achievement"


@nox.session(venv_backend="none")
def get_all_items(session: nox.Session) -> None:
    items = client.get_all_items()
    assert items is not None, "Failed to get all items"


@nox.session(venv_backend="none")
def get_item(session: nox.Session) -> None:
    item = client.get_item("30000001")
    assert item is not None, "Failed to get item"

@nox.session(venv_backend="none")
def get_battlepass(session: nox.Session) -> None:
    battlepass = client.get_battlepass(0)
    assert battlepass is not None, "Failed to get battlepass"

@nox.session(venv_backend="none")
def get_all_maps(session: nox.Session) -> None:
    maps = client.get_all_maps()
    assert maps is not None, "Failed to get all maps"


@nox.session(venv_backend="none")
def test_error_handling(session: nox.Session) -> None:
    client = marvelrivalsapi.MarvelRivalsClient(os.environ["API_KEY"], error=True)
    try:
        client.get_hero("invalid_hero_id")
    except marvelrivalsapi.MarvelRivalsAPIError:
        pass
    should_be_none = client.get_hero("invalid_hero_id", error=False)
    assert should_be_none is None, "Error handling failed"
