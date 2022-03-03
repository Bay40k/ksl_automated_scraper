import asyncio
from datetime import datetime

import discord

import ksl_scrape
from config import config_options

client = discord.Client()

KEYWORD = config_options["settings"]["keyword"]
PRICE_FROM = config_options["settings"]["price_from"]
PRICE_TO = config_options["settings"]["price_to"]

TOKEN = config_options["discord"]["discord_token"]
USER_ID = config_options["discord"]["discord_user_id"]


async def do_scrape() -> str:
    search_results_html = await ksl_scrape.get_search_results(
        KEYWORD, PRICE_FROM, PRICE_TO
    )
    search_results = await ksl_scrape.parse_search_results(search_results_html)
    if not search_results:
        print("No new results were found.")
        return None
    search_results_string = "\n\n=========================\n\n".join(
        [f"{result.link}\n{result.text}" for result in search_results]
    )
    print(search_results_string)
    subject = f"New KSL Search Results for '{KEYWORD}' | {datetime.now()}"
    return f"{subject}\n\n{search_results_string}"


async def send_message(user_id: str, message_text: str):
    user = await client.fetch_user(user_id)
    user_dm = await user.create_dm()
    await user_dm.send(message_text)


async def main():
    await client.login(TOKEN)
    scraped_data = await do_scrape()
    await send_message(USER_ID, scraped_data[:2000])
    await client.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
