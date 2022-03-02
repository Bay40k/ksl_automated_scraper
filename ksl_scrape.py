from __future__ import annotations

from dataclasses import dataclass
from typing import List

import bs4.element
import requests
from bs4 import BeautifulSoup


# TODO:
# - Keep track of already sent results

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
)
BASE_URL = "https://classifieds.ksl.com"


@dataclass
class SearchResult:
    title: str
    price: str
    location: str
    link: str
    text: str

    def __init__(self, html: bs4.element.Tag):
        self.html = html
        self.link = BASE_URL + html.a["href"]
        self.text = html.text.strip()

        self.text_list = list(filter(None, self.text.split("\n")))
        self.title = self.text_list[0]
        self.price = self.text_list[1]
        self.location = self.text_list[2]


async def get_search_results(
    keyword: str,
    price_from: int | None = None,
    price_to: int | None = None,
    page: int | None = None,
) -> str:
    headers = {
        "Accept": "text/html",
        "User-Agent": USER_AGENT,
    }
    url_string = f"{BASE_URL}/search/keyword/{keyword}"
    if price_from:
        url_string += f"/priceFrom/{price_from}"
    if price_to:
        url_string += f"/priceTo/{price_to}"
    if page and page > 0:
        url_string += f"/page/{page + 1}"
    my_request = requests.get(url_string, headers=headers)
    return my_request.text


async def parse_search_results(search_results_html: str) -> List[SearchResult]:
    soup = BeautifulSoup(search_results_html, "html.parser")
    all_listings_tags = soup.find_all(class_="listing-item featured")
    return [SearchResult(listing) for listing in all_listings_tags]
