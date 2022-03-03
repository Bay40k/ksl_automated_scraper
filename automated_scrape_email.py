import asyncio
from datetime import datetime

from automated_scrape import do_scrape
from config import config_options
from send_email import send_email


async def main():
    scraped_data = await do_scrape()
    if scraped_data:
        subject = f"New KSL Search Results | {datetime.now()}"
        await send_email(
            config_options["email"]["mail_server"],
            config_options["email"]["mail_port"],
            config_options["email"]["email_from"],
            config_options["email"]["email_password"],
            config_options["email"]["email_to"],
            subject,
            scraped_data,
        )


if __name__ == "__main__":
    asyncio.run(main())
