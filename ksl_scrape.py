from __future__ import annotations

from dataclasses import dataclass
from typing import List

import aiosqlite
import bs4.element
import requests
from bs4 import BeautifulSoup

from config import config_options

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
)
BASE_URL = "https://classifieds.ksl.com"
ALREADY_SENT_DB = config_options["database"]["db_location"]

PROXY_USERNAME = config_options["proxy"]["username"]
PROXY_PASSWORD = config_options["proxy"]["password"]
PROXY_URL = config_options["proxy"]["url"]
PROXY_PORT = config_options["proxy"]["port"]


async def has_link_been_sent(link_to_result: str) -> bool:
    """
    Indicates whether the specified link exists in DB, and therefore if that listing has already been sent
    Also adds links that haven't been sent to `ALREADY_SENT_DB`

    :param link_to_result: link to KSL search result
    :return: Boolean indicating whether the result has already been sent or not
    """
    async with aiosqlite.connect(ALREADY_SENT_DB) as db:
        async with db.execute(
            f"SELECT link from links WHERE link='{link_to_result}'"
        ) as cursor:
            result = await cursor.fetchone()
            if result is not None:
                return True
            await db.execute(f"INSERT INTO links(link) VALUES ('{link_to_result}');")
            await db.commit()
            print(f"Added link '{link_to_result}' to db '{ALREADY_SENT_DB}'")
            return False


@dataclass
class KSLSearchResult:
    """
    KSLSearchResult object
    """

    title: str
    price: str
    location: str
    link: str
    text: str

    def __init__(self, html: bs4.element.Tag):
        """
        Turns search results into a KSLSearchResult object

        :param html: BS4 HTML element tag with class "listing-item featured"
        """
        self.html = html
        self.link = BASE_URL + html.a["href"]
        self.text = html.text.strip()
        self.text_list = list(
            filter(None, self.text.split("\n"))
        )  # Remove empty elements (empty lines) after splitting by newline
        self.title = self.text_list[0]
        self.price = self.text_list[1]
        self.location = self.text_list[2]


async def get_search_results(
    keyword: str,
    price_from: int | None = None,
    price_to: int | None = None,
    zip_code: int | None = None,
    miles_radius: int | None = None,
    page: int | None = None,
) -> str:
    """
    Obtain HTML page of KSL classifieds search results.

    :param keyword: Keyword to search for
    :param price_from: Lower bound of price
    :param price_to: Upper bound of price
    :param zip_code: Optional zip code for search results radius
    :param miles_radius: Miles radius around defined zip code
    :param page: Page of search results to retrieve
    :return: String containing the HTML page of KSL classifieds search results
    """

    headers = {
        "Accept": "text/html",
        "User-Agent": USER_AGENT,
    }
    url_string = f"{BASE_URL}/search/keyword/{keyword}"

    if miles_radius is not None and miles_radius not in [0, 10, 25, 50, 100, 150, 200]:
        if miles_radius > 200:
            miles_radius = 10000
        else:
            miles_radius = None

    if zip_code is not None:
        if miles_radius is None:
            miles_radius = 0
        url_string += f"/zip/{zip_code}/miles/{miles_radius}"

    if price_from is not None:
        url_string += f"/priceFrom/{price_from}"

    if price_to is not None:
        url_string += f"/priceTo/{price_to}"

    if page is not None and page > 0 and page != 1:
        url_string += f"/page/{page - 1}"

    if (
        PROXY_USERNAME != ""
        and PROXY_PASSWORD != ""
        and PROXY_URL != ""
        and PROXY_PORT != 0
    ):
        print(f"Using proxy '{PROXY_URL}:{PROXY_PORT}'...")
        prox = f"socks5://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_URL}:{PROXY_PORT}"
    else:
        prox = None
    with requests.Session() as r:
        if prox:
            r.proxies["http"] = prox
            r.proxies["https"] = prox
        print(f"Getting URL: '{url_string}'")
        my_request = r.get(url_string, headers=headers)
    return my_request.text


async def parse_search_results(
    search_results_html: str, only_unsent: bool = True
) -> List[KSLSearchResult]:
    """
    Retrieves list of `KSLSearchResult` objects, from raw HTML search results.

    :param search_results_html: Raw HTML string
    :param only_unsent: Bool indicating whether to only return unsent search results
    :return: List of of `KSLSearchResult` objects
    """
    soup = BeautifulSoup(search_results_html, "html.parser")
    all_listings_tags = soup.find_all(class_="listing-item featured")
    all_listings = [KSLSearchResult(listing) for listing in all_listings_tags]
    if not only_unsent:
        return all_listings
    unsent_listings = []
    for listing in all_listings:
        is_listing_sent = await has_link_been_sent(listing.link)
        if not is_listing_sent:
            unsent_listings.append(listing)
    return unsent_listings
