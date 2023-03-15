import json
import logging
import yaml

from flask import Flask
from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import g
import flask_babel
from flask_babel import Babel
from flask_babel import _
import requests
from requests import Timeout
from werkzeug.exceptions import HTTPException
from bs4 import BeautifulSoup
from bs4 import Comment

app = Flask(__name__)
babel = Babel(app)
language = "sv"

@app.route("/")
def start():
    search_language = request.args.get("language")
    if (
            not search_language or
            config().get("search_languages").get(search_language) is None
    ):
        search_language = "sv"

    footer = config().get("footer", [])
    attributions = []
    if "wikipedia_logo_attribution" in config():
        attributions.append(config()["wikipedia_logo_attribution"])
    for block in footer:
        if "attribution" in block:
            attributions.append(block["attribution"])

    search_language_parameters = config()["search_languages"][search_language]
    search_language_parameters["code"] = search_language
    if "placeholder" not in search_language_parameters:
        default_language = config()["search_languages"][language]
        search_language_parameters["placeholder"] = default_language["placeholder"]

    return render_template(
        "index.html",
        lang=language,
        search_languages=config()["search_languages"],
        search_language=search_language_parameters,
        footer=footer,
        attributions=attributions,
        banner=banner
    )

def config():
    """Get config

    Loads config the first time this is used and saves it for later
    access.

    """
    if g.get("config") is None:
        with open("config.yaml") as config_file:
            g.config = yaml.safe_load(config_file)

    return g.config

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
    try:
        response = requests.get(url, params=parameters, timeout=1.0).json()
    except Timeout as e:
        logging.error("Timeout for request to Wikipedia API.", exc_info=e)
        abort(504)
    except Exception as e:
        logging.error("Error for request to Wikipedia API.", exc_info=e)
        abort(500)
    suggestions = [p["title"] for p in response["query"]["allpages"]]
    return suggestions

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route("/go")
def go():
    language = request.args.get("l")
    query = request.args.get("q")
    url = f"http://{language}.wikipedia.org/wiki/{query}"
    return redirect(url)

@app.route("/preview-banner")
def preview():
    url = request.args.get("url")
    selector = request.args.get("selector")
    banner_html = get_banner_html(url, selector)
    return start(banner=banner_html)

def get_banner_html(url=None, selector=None):
    """Generate HTML for the banner

    Uses url and selector from parameters if given and values from
    config if not.

    """
    if url is None:
        banner = config().get("banner", {})
        url = banner.get("url")
        if not url:
            message = "Missing config variable <code>banner: url</code>."
            return render_template("banner-error.html", message=message)

        selector = banner.get("selector")

    response = requests.get(url).text
    if selector:
        soup = BeautifulSoup(response, "html.parser")
        html = soup.select(selector)[0]
    else:
        html = response

    return html

@app.route("/set-banner")
def banner():
    html = get_banner_html(url, selector)
    with open("templates/banner.html", "w") as f:
        f.write(str(html))

    return start()

@babel.localeselector
def get_locale():
    return language

