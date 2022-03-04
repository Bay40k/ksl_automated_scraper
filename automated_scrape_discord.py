import asyncio

import discord

from automated_scrape import do_scrape
from config import config_options

client = discord.Client()

TOKEN = config_options["discord"]["discord_token"]
USER_ID = config_options["discord"]["discord_user_id"]


async def send_message(user_id: str, message_text: str):
    user = await client.fetch_user(user_id)
    user_dm = await user.create_dm()
    await user_dm.send(message_text)


async def chunks(string_to_chunk: str, chunk_length):
    """Produce `chunk_length`-character chunks from `string_to_chunk`."""
    for start in range(0, len(string_to_chunk), chunk_length):
        yield string_to_chunk[start : start + chunk_length]


async def main():
    scraped_data = await do_scrape()
    if not scraped_data:
        return None
    scraped_data_chunks = chunks(
        scraped_data, 2000
    )  # Split into 2,000 character chunks (Discord char limit)
    await client.login(TOKEN)
    async for chunk in scraped_data_chunks:
        await send_message(USER_ID, chunk)
    await client.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
