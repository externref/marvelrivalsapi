# Tutorial
### API Key
Before anything, you'd like to get a API key from [the website](https://marvelrivalsapi.com).

!!! note
    You might want to keep the API key as an environment variable instead of pasting it directly into source code in most cases. To do this, install the `python-dotenv` library and create a `.env` file in the same directory as your code file. 
    
    **.env** 
    ```python
    API_KEY="abcd1234"
    ``` 
    **main.py**
    ```python
    import os

    import dotenv

    dotenv.load_dotenv()
    
    KEY = os.environ["API_KEY"]
    ```

### Installing the library

=== "pip"

    ``` shell
    pip install marvelrivalsapi
    ```

=== "poetry"

    ``` shell
    poetry add marvelrivalsapi
    ```
=== "uv"

    ``` shell
    uv add marvelrivalsapi
    ```

Use `pip` if you don't know what you're doing.

### First Steps

The client objects are the entry point to the API and you'll mostly be using them to perform all the package related tasks.

=== "sync"

    ```python
    import marvelrivalsapi

    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    # rest of code
    ```

=== "async"
 
    ```python
    import asyncio

    import marvelrivalsapi

    def main():
        client = marvelrivalsapi.AsyncMarvelRivalsClient("mykeyhere")
        # rest of code
        await client.close()

    asyncio.run(main())
    ```

=== "async context"

    ```python
    import asyncio

    import marvelrivalsapi

    def main():
        async with marvelrivalsapi.AsyncMarvelRivalsClient("mykeyhere") as client:
            # other stuff here
            ...

    asyncio.run(main())
    ```

### Example: Fetching a hero data

=== "sync"

    ```python
    import marvelrivalsapi

    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    spiderman = client.get_hero(marvelrivalsapi.Heroes.SPIDER_MAN)
    print(spiderman)
    ```

=== "async"
 
    ```python
    import asyncio

    import marvelrivalsapi

    def main():
        client = marvelrivalsapi.AsyncMarvelRivalsClient("mykeyhere")
        spiderman = await client.get_hero(marvelrivalsapi.Heroes.SPIDER_MAN)
        print(spiderman)
        await client.close()

    asyncio.run(main())
    ```

### Example: Getting All Heroes

=== "sync"

    ```python
    import marvelrivalsapi

    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    heroes = client.get_all_heroes()
    print(f"Found {len(heroes)} heroes")
    ```

=== "async"
 
    ```python
    import asyncio
    import marvelrivalsapi

    async def main():
        client = marvelrivalsapi.AsyncMarvelRivalsClient("mykeyhere")
        heroes = await client.get_all_heroes()
        print(f"Found {len(heroes)} heroes")
        await client.close()

    asyncio.run(main())
    ```

### Example: Hero Leaderboards

=== "sync"

    ```python
    import marvelrivalsapi

    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    leaderboard = client.get_hero_leaderboard(marvelrivalsapi.Heroes.EMMA_FROST)
    for player in leaderboard.players[:5]:  # Top 5 players
        print(f"{player.info.name}: {player.wins} wins, {player.kda:.2f} KDA")
    ```

=== "async"
 
    ```python
    import asyncio
    import marvelrivalsapi

    async def main():
        async with marvelrivalsapi.AsyncMarvelRivalsClient("mykeyhere") as client:
            leaderboard = await client.get_hero_leaderboard(marvelrivalsapi.Heroes.EMMA_FROST)
            for player in leaderboard.players[:5]:  # Top 5 players
                print(f"{player.info.name}: {player.wins} wins, {player.kda:.2f} KDA")

    asyncio.run(main())
    ```

### Example: Getting Hero Costumes

=== "sync"

    ```python
    import marvelrivalsapi

    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    costumes = client.get_hero_costumes(marvelrivalsapi.Heroes.EMMA_FROST)
    for costume in costumes:
        print(f"{costume.name}: {costume.rarity}")
    ```

=== "async"
 
    ```python
    import asyncio
    import marvelrivalsapi

    async def main():
        client = marvelrivalsapi.AsyncMarvelRivalsClient("mykeyhere")
        costumes = await client.get_hero_costumes(marvelrivalsapi.Heroes.EMMA_FROST)
        for costume in costumes:
            print(f"{costume.name}: {costume.rarity}")
        await client.close()

    asyncio.run(main())
    ```

### Example: Working with Achievements

=== "Get All Achievements"

    ```python
    import marvelrivalsapi

    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    achievements = client.get_all_achievements()
    
    # Get achievements by category
    combat_achievements = achievements.filter_by_category("Combat")
    print(f"Found {len(combat_achievements)} combat achievements")
    
    # Calculate total points
    total_points = achievements.get_total_points()
    print(f"Total achievement points: {total_points}")
    ```

=== "Get Specific Achievement"

    ```python
    import marvelrivalsapi

    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    achievement = client.get_achievement("Sticking Around")
    
    if achievement:
        print(f"Achievement: {achievement.name}")
        print(f"Category: {achievement.category}")
        print(f"Points: {achievement.points}")
        print(f"Icon URL: {achievement.icon_url}")
    ```

### Example: Working with Items

=== "Get All Items"

    ```python
    import marvelrivalsapi

    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    items = client.get_all_items()
    
    # Filter items by type
    nameplates = items.filter_by_type("Nameplate")
    print(f"Found {len(nameplates)} nameplates")
    
    # Filter items by quality
    rare_items = items.filter_by_quality("BLUE")
    print(f"Found {len(rare_items)} rare items")
    ```

=== "Get Specific Item"

    ```python
    import marvelrivalsapi

    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    item = client.get_item("30000001")
    
    if item:
        print(f"Item: {item.name}")
        print(f"Type: {item.type}")
        print(f"Quality: {item.quality}")
        print(f"Icon URL: {item.icon_url}")
        
        if item.is_hero_specific:
            print(f"Associated with hero ID: {item.associated_hero}")
    ```

### Example: Battle Pass Information

=== "sync"

    ```python
    import marvelrivalsapi

    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    battlepass = client.get_battlepass(1.0)
    
    print(f"Battle Pass: {battlepass.season_name}")
    
    # Get premium items
    premium_items = battlepass.get_premium_items()
    print(f"Premium items: {len(premium_items)}")
    
    # Get free items
    free_items = battlepass.get_free_items()
    print(f"Free items: {len(free_items)}")
    
    # Find a specific item
    item = battlepass.find_item("All-Butcher")
    if item:
        print(f"Found item: {item.name} (Premium: {'Yes' if item.isLuxury else 'No'})")
    ```

=== "async"

    ```python
    import asyncio
    import marvelrivalsapi

    async def main():
        async with marvelrivalsapi.AsyncMarvelRivalsClient("mykeyhere") as client:
            battlepass = await client.get_battlepass(1.0)
            
            print(f"Battle Pass: {battlepass.season_name}")
            
            # Get premium items
            premium_items = battlepass.get_premium_items()
            print(f"Premium items: {len(premium_items)}")
            
            # Get free items
            free_items = battlepass.get_free_items()
            print(f"Free items: {len(free_items)}")

    asyncio.run(main())
    ```

### Error Handling

The Marvel Rivals API client provides two ways to handle errors:

1. Default behavior: Return `None` when API calls fail
2. Error-raising behavior: Raise a `MarvelRivalsAPIError` exception

=== "Global Setting"

    ```python
    import marvelrivalsapi
    
    # Create a client that always raises errors on API failures
    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere", error=True)
    
    try:
        # This will raise an exception if the hero doesn't exist
        hero = client.get_hero("non-existent-hero")
        print(hero.name)
    except marvelrivalsapi.MarvelRivalsAPIError as e:
        print(f"API error: {e}")
    ```

=== "Per-Method Setting"

    ```python
    import marvelrivalsapi
    
    # Create a client with default behavior (return None on failure)
    client = marvelrivalsapi.MarvelRivalsClient("mykeyhere")
    
    # Normal call - returns None on failure
    hero1 = client.get_hero("non-existent-hero")
    if hero1 is None:
        print("Hero not found")
    
    # Override for a specific call - will raise an exception
    try:
        hero2 = client.get_hero("another-non-existent-hero", error=True)
    except marvelrivalsapi.MarvelRivalsAPIError as e:
        print(f"API error: {e}")
    ```
