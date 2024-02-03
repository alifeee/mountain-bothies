"""
gets all bothies from https://www.mountainbothies.org.uk/bothies/
 and gets their lat/long coordinates
"""

import os
import json
import time
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BOTHIE_URLS = [
    "https://www.mountainbothies.org.uk/bothies/northern-highlands/",
    "https://www.mountainbothies.org.uk/bothies/north-west-highlands-islands/",
    "https://www.mountainbothies.org.uk/bothies/western-highlands-islands/",
    "https://www.mountainbothies.org.uk/bothies/southwest-highlands-islands/",
    "https://www.mountainbothies.org.uk/bothies/central-highlands/",
    "https://www.mountainbothies.org.uk/bothies/eastern-highlands/",
    "https://www.mountainbothies.org.uk/bothies/southern-scotland/",
    "https://www.mountainbothies.org.uk/bothies/northern-england-borders/",
    "https://www.mountainbothies.org.uk/bothies/wales/",
]

CACHE_FOLDER = "cache"

OVERRIDES = {
    "https://www.mountainbothies.org.uk/bothies/western-highlands-islands/sourlies/": "NM 868 951",
    "https://www.mountainbothies.org.uk/bothies/central-highlands/culra/": "NN 523 762",
    "https://www.mountainbothies.org.uk/bothies/eastern-highlands/callater-stable/": "NO 178 845",
    "https://www.mountainbothies.org.uk/bothies/northern-england-borders/haughtongreen/": "NY 788 713",
    "https://www.mountainbothies.org.uk/bothies/wales/dulyn/": "SH 705 664",
    "https://www.mountainbothies.org.uk/bothies/eastern-highlands/gelder-shiel-stable/": "NO 258 900",
}

GRID_REF_REGEX = re.compile(r"[^A-Z]([A-Z]{2}\s*\d+\s+\d+)")


def get_url_or_cache(url):
    """gets url or returns from cache"""

    def url_to_filename(url):
        """converts url to filename"""
        return url.replace("/", "_").replace(":", "_")

    filename = url_to_filename(url)
    filepath = os.path.join(CACHE_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as cache_file:
            return cache_file.read()
    else:
        page = requests.get(url, timeout=10)
        with open(filepath, "w", encoding="utf-8") as cache_file:
            cache_file.write(page.text)
        return page.text


def get_bothies_from_region(url):
    """gets bothies from url"""
    bothie_urls = []
    page = get_url_or_cache(url)
    soup = BeautifulSoup(page, "html.parser")
    # find <h2> with "Bothies in [region]"
    region = soup.find("h2", string=lambda text: "Bothies in" in text)
    if region:
        bothies = region.find_next_sibling("ul").find_all("li")
        for bothy in bothies:
            link = bothy.find("a")
            bothie_urls.append(link["href"])
    return bothie_urls


def get_bothie_info(url):
    """gets grid reference from url"""
    page = get_url_or_cache(url)
    soup = BeautifulSoup(page, "html.parser")
    gridref_title = soup.find("span", string=lambda text: "Grid Ref:" in text)
    if gridref_title:
        gridref_parent = gridref_title.parent
        gridref_text = gridref_parent.text
        # get grid ref
        match = GRID_REF_REGEX.search(gridref_text)
        if match:
            gridref_text = match.group(1)
            # if no space after first two letters, add one
            if gridref_text[2] != " ":
                gridref_text = gridref_text[:2] + " " + gridref_text[2:]
            # if numbers do not have leading zeros, add them (/[0-9]{2}/)
            gridref_text = re.sub(r"(\s[0-9]{2}\s)", r" 0\1 ", gridref_text)
        else:
            gridref_text = None
    else:
        gridref_text = None

    # get name (span within h1)
    name = soup.find("h1").find("span").text

    # get location (content of strong next to span with "Location:")
    #  i.e., <strong><span>Location:</span> Eastern Highlands</strong>
    location = soup.find("span", string=lambda text: "Location:" in text)
    if location:
        location_text = location.parent.text
        location_text = location_text.replace("Location:", "").strip()
    else:
        location_text = None

    # get features
    features_text = soup.find(
        "h2", string=lambda text: "Features" in text if text else False
    )
    if features_text:
        features_ul = features_text.find_next_sibling("ul")
        features = [li.text for li in features_ul.find_all("li")]
    else:
        features = []

    return {
        "grid_ref": gridref_text,
        "features": features,
        "name": name,
        "location": location_text,
    }


def save_cache(file, cache):
    """saves cache to file"""
    with open(file, "w", encoding="utf-8") as cache_file:
        json.dump(cache, cache_file)


def main():
    """main"""
    bothie_urls = []
    for url in tqdm(BOTHIE_URLS):
        bothie_urls.extend(get_bothies_from_region(url))

    bothies = {}
    for url in tqdm(bothie_urls):
        bothie_info = get_bothie_info(url)
        if OVERRIDES.get(url):
            bothie_info["grid_ref"] = OVERRIDES[url]
        bothies[url] = bothie_info

    save_cache("bothies.json", bothies)


if __name__ == "__main__":
    main()
