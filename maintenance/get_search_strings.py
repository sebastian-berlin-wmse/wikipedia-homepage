#! /usr/local/bin python

"""Retrieves a list of placeholder strings for the search field

The strings are fetched from live Wikipedia, specifically from the
search field. This will be what it looks like when you're not logged
in, so it may differ from some skins.

Each language specified in the config is processed. The output has the
same format as in the config for easy copying.

"""

import requests
import yaml
from bs4 import BeautifulSoup as Soup

def get_search_strings(language):
    response = requests.get(f"https://{language}.wikipedia.org")
    html = response.content
    soup = Soup(html, features="html.parser")
    search_field_string = soup.select("#searchInput")[0]["placeholder"]
    return search_field_string

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)

for language in config["search_languages"]:
    print(language)
    message = get_search_strings(language)
    print(f"        placeholder: {message}")

