import asyncio
import marvelrivalsapi
import dotenv
import os
dotenv.load_dotenv()

client = marvelrivalsapi.MarvelRivalsClient(os.environ["API_KEY"])
async_client = marvelrivalsapi.AsyncMarvelRivalsClient(os.environ["API_KEY"])

async def main():
    jeff = client.get_hero(marvelrivalsapi.Heroes.JEFF_THE_LAND_SHARK, error=True)
    print(jeff.lore)
    spider = await async_client.get_hero(marvelrivalsapi.Heroes.SPIDER_MAN, error=True)
    print(spider.lore)


asyncio.run(main())