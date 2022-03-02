import asyncio
from datetime import datetime

import ksl_scrape
from send_email import send_email
from config import config_options

KEYWORD = config_options["settings"]["keyword"]
PRICE_FROM = config_options["settings"]["price_from"]
PRICE_TO = config_options["settings"]["price_to"]


async def main():
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
    await send_email(
        config_options["email"]["mail_server"],
        config_options["email"]["mail_port"],
        config_options["email"]["email_from"],
        config_options["email"]["email_password"],
        config_options["email"]["email_to"],
        subject,
        search_results_string,
    )


if __name__ == "__main__":
    asyncio.run(main())
