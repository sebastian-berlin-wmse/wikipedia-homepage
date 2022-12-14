from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import flask_babel
from flask_babel import Babel
from flask_babel import _
import requests

app = Flask(__name__)
babel = Babel(app)

@app.route("/")
def start():
    return render_template("index.html", lang="sv")

@app.route("/suggest")
def suggest():
    language = request.args.get("lang")
    search = request.args.get("search")
    url = f"https://{language}.wikipedia.org/w/api.php"
    parameters = {
        "action": "query",
        "list": "allpages",
        "apnamespace": 0,
        "aplimit": 20,
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
    return "sv"
