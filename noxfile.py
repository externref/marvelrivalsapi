import os

import dotenv
import nox

import marvelrivalsapi

dotenv.load_dotenv()
client = marvelrivalsapi.MarvelRivalsClient(os.environ["API_KEY"])


@nox.session(venv_backend="venv")
def get_heroes(session: nox.Session) -> None:
    heroes = client.get_all_heroes()
    assert heroes is not None, "Failed to get heroes"


@nox.session(venv_backend="venv")
def get_hero(session: nox.Session) -> None:
    heroes = client.get_hero(marvelrivalsapi.Heroes.EMMA_FROST)
    assert heroes is not None, "Failed to get hero"


@nox.session(venv_backend="venv")
def get_hero_leaderboard(session: nox.Session) -> None:
    heroes = client.get_hero_leaderboard(marvelrivalsapi.Heroes.EMMA_FROST)
    assert heroes is not None, "Failed to get hero leaderboard"


@nox.session(venv_backend="venv")
def get_hero_costumes(session: nox.Session) -> None:
    heroes = client.get_hero_costumes(marvelrivalsapi.Heroes.EMMA_FROST)
    assert heroes is not None, "Failed to get hero costumes"
