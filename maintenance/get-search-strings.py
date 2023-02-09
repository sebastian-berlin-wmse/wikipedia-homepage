#! /usr/local/bin python

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

