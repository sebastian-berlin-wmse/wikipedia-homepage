from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import flask_babel
from flask_babel import Babel
from flask_babel import _
import requests
import yaml

app = Flask(__name__)
babel = Babel(app)
language = "sv"

@app.route("/")
@app.route("/<search_language>")
def start(search_language=None):
    if not search_language:
        search_language = "sv"
    with open("config.yaml") as config_file:
        config = yaml.safe_load(config_file)

    if "footer" in config:
        footer = config["footer"]
    else:
        # Empty list instead of None to make the template code a bit
        # cleaner.
        footer = []

    attributions = []
    if "wikipedia_logo_attribution" in config:
        attributions.append(config["wikipedia_logo_attribution"])
    for block in footer:
        if "attribution" in block:
            attributions.append(block["attribution"])

    search_language_parameters = config["search_languages"][search_language]
    search_language_parameters["code"] = search_language

    return render_template(
        "index.html",
        lang=language,
        search_languages=config["search_languages"],
        search_language=search_language_parameters,
        footer=footer,
        attributions=attributions
    )

@app.route("/suggest")
def suggest():
    language = request.args.get("lang")
    search = request.args.get("search")
    url = f"https://{language}.wikipedia.org/w/api.php"
    parameters = {
        "action": "query",
        "list": "allpages",
        "apnamespace": 0,
        "aplimit": 10,
        "apprefix": search,
        "format": "json"
    }
    response = requests.get(url, params=parameters).json()
    suggestions = [p["title"] for p in response["query"]["allpages"]]
    return suggestions;

@app.route("/go")
def go():
    language = request.args.get("l")
    query = request.args.get("q")
    url = f"http://{language}.wikipedia.org/wiki/{query}"
    return redirect(url)

@babel.localeselector
def get_locale():
    return language

