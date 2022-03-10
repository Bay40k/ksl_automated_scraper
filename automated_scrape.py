import logging
from datetime import datetime

import ksl_scrape
from ksl_scrape import enable_logging
from config import config_options

KEYWORD = config_options["settings"]["keyword"]
PRICE_FROM = config_options["settings"]["price_from"]
PRICE_TO = config_options["settings"]["price_to"]
ZIP_CODE = config_options["settings"]["zip_code"]
MILES_RADIUS = config_options["settings"]["miles_radius"]


async def do_scrape(only_unsent: bool = True) -> str:
    """
    Returns scraped data using `config_options` from `config.py`.

    :param only_unsent: Bool whether to return only unsent listings
    :return: String containing scraped data, separated by equals signs.
    """
    await enable_logging()
    search_results_html = await ksl_scrape.get_search_results(
        KEYWORD, PRICE_FROM, PRICE_TO, ZIP_CODE, MILES_RADIUS
    )
    search_results = await ksl_scrape.parse_search_results(
        search_results_html, only_unsent=only_unsent
    )
    if not search_results:
        logging.info("No *new* results were found.")
        return None
    search_results_string = "\n=========================\n".join(
        [f"{result.link}\n{result.text}" for result in search_results]
    )
    search_results_string = search_results_string.replace(
        "\n\n", "\n"
    )  # Remove redundant newlines
    logging.info(search_results_string)
    subject = f"New KSL Search Results for '{KEYWORD}' | {datetime.now()}"
    return f"{subject}\n{search_results_string}"
