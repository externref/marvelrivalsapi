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
