import requests
from typing import Union
from datetime import datetime

"""
Allowed values for various filters (case sensitive):
sellerType:   "For Sale By Owner", "Dealership"
newUsed:      "Used", "New", "Certified"
transmission: "Automatic", "Manual", "CVT", "Automanual"
fuel:         "Compressed Natural Gas", "Diesel", "Electric", "Flex Fuel", "Gasoline", "Hybrid"
drive:        "2-Wheel Drive", "4-Wheel Drive", "AWD", "FWD", "RWD"
titleType:    "Clean Title", "Dismantled Title", "Not Specified", "Rebuilt/Reconstructed Title", "Salvage Title"
"""


def semicolonize(input_list: Union[list, str]) -> str:
    """
    Joins lists with semicolons which is what the API requires for multiple parameters
    """
    if type(input_list) is str:
        return input_list
    return ";".join(input_list)


def get_makes_models_trims(make: str = None, model: str = None) -> list:
    """
    Function to return all available makes, models, and trims
    """
    headers = {"Content-Type": "application/json"}
    data = {"endpoint": "/classifieds/cars/category/getTrimsForMakeModel"}
    page = requests.post(f"https://cars.ksl.com/nextjs-api/proxy", headers=headers, json=data)
    cars = page.json()["data"]

    # return models if make defined
    if make and not model:
        models = list()
        for m in cars[make]:
            models.append(m)
        return models

    # return trims if make and model defined
    if make and model:
        trims = list()
        for t in cars[make][model]:
            trims.append(t)
        return trims

    # return all makes if nothing defined
    makes = list()
    for m in cars:
        makes.append(m)
    return makes


def ksl_auto_search(keyword: str = None, filters: dict = None, page: int = 1) -> dict:
    """
    Returns dictionary of car listings per given keyword/filters
    """
    if filters is None:
        filters = {}
    if keyword:
        filters["keyword"] = keyword

    filter_array = list()

    possible_filters = [
        "sellerType",
        "newUsed",
        "make",
        "model",
        "priceTo",
        "priceFrom",
        "mileageFrom",
        "mileageTo",
        "trim",
        "transmission",
        "keyword",
        "fuel",
        "drive",
        "titleType"
    ]

    # add filter to filter_array if it exists
    for f in possible_filters:
        if f in filters.keys():
            filter_value = semicolonize(filters[f])
            filter_array.extend([f, filter_value])

    headers = {"Content-Type": "application/json"}
    data = {
        "endpoint": "/classifieds/cars/search/searchByUrlParams",
        "options": {
            "body": ["page", f"{page}"]
        }
    }

    # add filters to data
    data["options"]["body"].extend(filter_array)
    page = requests.post(f"https://cars.ksl.com/nextjs-api/proxy", headers=headers, json=data)
    car_listings = page.json()["data"]["items"]

    all_listings = dict()
    for i, listing in enumerate(car_listings):
        year = listing["makeYear"]
        make = listing["make"]
        model = listing["model"]

        try:
            trim = listing["trim"]
        except KeyError:
            trim = None

        title = f"{year} {make} {model}"
        if trim:
            title += f" {trim}"

        try:
            transmission = listing["transmission"]
        except KeyError:
            transmission = None

        try:
            fuel = listing["fuel"]
        except KeyError:
            fuel = None

        try:
            title_type = listing["titleType"]
        except KeyError:
            title_type = None

        price        = f"${listing['price']}"
        miles        = listing["mileage"]
        location     = f"{listing['city']}, {listing['state']}"
        vin          = listing["vin"]
        body_type    = listing["body"]
        link         = f"https://cars.ksl.com/listing/{listing['id']}"
        seller_type  = listing["sellerType"]
        new_or_used  = listing["newUsed"]

        timestamp = listing["displayTime"]
        time_created = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


        listing_dict = {
            "listing_title": title,
            "year": year,
            "make": make,
            "model": model,
            "trim": trim,
            "price": price,
            "miles": miles,
            "new_or_used": new_or_used,
            "location": location,
            "vin": vin,
            "body_type": body_type,
            "fuel_type": fuel,
            "transmission": transmission,
            "link": link,
            "seller_type": seller_type,
            "title_type": title_type,
            "time_created_utc": time_created,
            "unix_timestamp": timestamp
        }
        all_listings[i] = listing_dict

    if all_listings:
        return all_listings
    return {"error": "No listings found"}


if __name__ == "__main__":
    # Example code
    import json

    listings = ksl_auto_search(keyword="Honda civic", page=1)
    print(json.dumps(listings, indent=4))
