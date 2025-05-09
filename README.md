<div align="center">
    
# MarvelRivalsAPI

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub License](https://img.shields.io/github/license/externref/marvelrivalsapi)](https://github.com/externref/marvelrivalsapi/blob/main/LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/mypy-typed-blue)](https://mypy.readthedocs.io/en/stable/)
[![PyPI version](https://badge.fury.io/py/marvelrivalsapi.svg)](https://badge.fury.io/py/marvelrivalsapi)
[![GitHub stars](https://img.shields.io/github/stars/externref/marvelrivalsapi)](https://github.com/externref/marvelrivalsapi/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/externref/marvelrivalsapi)](https://github.com/externref/marvelrivalsapi/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/externref/marvelrivalsapi)](https://github.com/externref/marvelrivalsapi/commits/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![Banner Image](https://github.com/externref/marvelrivalsapi/blob/main/docs/assets/banner.jpeg?raw=true)

</div>

Opinionated python API Wrapper for the Unofficial [Marvel Rivals API](https://marvelrivalsapi.com).

> [!IMPORTANT]  
> Package still under development, install the package from the source whenever possible because it's more updated. 
Use `git+https://github.com/externref/marvelrivals` as the package name to install from source.

#### GET STARTED
Read the elaborate [tutorial](https://externref.github.io/marvelrivalsapi/tutorial/) to start developing with `marvelrivalsapi`

### Features
 
* Easy to use API interface
* Support for both blocking and `async` workflows
* Type support with `mypy` and `pyright` check

### Example

```python
import marvelrivalsapi

def main() -> None:
    client = marvelrivalsapi.MarvelRivalsClient("api-key-here")
    spiderman = client.get_hero("spider-man")
    season_bp = client.get_battlepass(2)
    maps = client.get_all_maps()
    # and more ...

main()
```

### Coverage
- [x] All Heroes
- [x] Get Hero
- [x] Hero Stats
- [x] Hero Leaderboard
- [x] All Costumes
- [x] Get Costume
- [x] Items
- [x] Achievements
- [x] Battlepass
- [x] Maps
- [ ] Patch Notes
- [ ] Player Data
- [ ] Match Data
