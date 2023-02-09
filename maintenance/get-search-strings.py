#! /usr/local/bin python

from html.parser import HTMLParser
import requests
import yaml
from bs4 import BeautifulSoup as Soup
# from soupselect import select
import urllib
import re
import json

# def get_search_strings(language):
#     try:
#         messages = requests.get(f"https://github.com/wikimedia/mediawiki/raw/master/languages/i18n/{language}-arab.json").json()
#     except:
#         return ""
#     # print(request.content)
#     # messages = json.loads(request.content)
#     wikitext = messages["searchsuggest-search"]
#     api_url = f"https://{language}.wikipedia.org/w/api.php"
#     parameters = {
#         "action": "parse",
#         "format": "json",
#         "text": wikitext,
#         "prop": "text",
#         # "wrapoutputclass": "",
#         # "disableeditsection": 1,
#         # "disabletoc": 1,
#         # "contentmodel": "wikitext",
#         "formatversion": "2"
#     }
#     api_response = requests.get(api_url, params=parameters).json()
#     html = api_response["parse"]["text"]
#     # print(html)
#     soup = Soup(html, features="html.parser")
#     text = soup.get_text().strip()
#     return text

def get_search_strings(language):
    response = requests.get(f"https://{language}.wikipedia.org")
    html = response.content
    soup = Soup(html, features="html.parser")
    # search_field = soup.select('[placeholder="Search Wikipedia"]')
    search_field_string = soup.select("#searchInput")[0]["placeholder"]
    return search_field_string
    # search_for_label = soup.find_all(re.compile("[Ss]earch"))
    # print(search_for_label)
    # search_suggestion_string = soup.select(".suggestions-special")
    # print(search_suggestion_string)

    # response = requests.get(f"https://{language}.wikipedia.org")
    # html = response.text
    # parser.feed(html)

# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         attributes = dict(attrs)
#         if "id" in attributes and attributes["id"] == "searchInput":
#             print(attributes["placeholder"])

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)

# parser = MyHTMLParser()

for language in config["search_languages"]:
    print(language)
    message = get_search_strings(language)
    print(f"        placeholder: {message}")

# print(get_search_strings("en"))
