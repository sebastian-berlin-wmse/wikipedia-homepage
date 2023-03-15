# Wikipedia homepage

A homepage for Wikipedia that can be used for alternative URLs, such
as wikipedia.se. Has a search box for Wikipedia and space for
information about chapter, user group or similar.

Based on [Wikimedia.de](https://github.com/wmde/Wikipedia.de)
developed by [Wikimedia Deutschland](https://www.wikimedia.de).

## Running

It's recommended to use venv.

Install dependencies:
```
pip install -r requirements.txt
```

Start with:
```
flask run
```

Add `--debug` when developing to make your life easier.

# Endpoints

## `/suggest`

Used internally to fetch search suggestions.

## `/go`

Used internally to go to a Wikipedia page.

## `/preview-banner`

Used to get a preview of a banner without saving it. Uses variables
under `banner` from config.yaml.  Parameters `url` and `selector` can
be used to use content from another URL in the preview. See
config.yaml for details.

## `/set-banner`

Saves banner content for subsequent visits. Uses variables under
`banner` from config.yaml.

# Maintenance Scripts

These scripts can help with setting up, but aren't used during
runtime. They're located in the `maintenance` folder.

## get_search_strings.py

Generates the placeholder strings for the search field, e.g. "Search
Wikipedia" for English, for each search language in the config. Each
string is retrieved from the search field on that language version of
Wikipedia.
