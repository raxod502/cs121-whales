"""
Module that contains our Flask app.
"""

import os

import flask
import flask_talisman

import whales.api

app = flask.Flask(__name__, static_folder=None)

if os.environ.get("WHALES_NO_SSL") in (None, "", "0"):
    flask_talisman.Talisman(app, content_security_policy=None)


@app.route("/")
def page_new_game():
    """
    Serve HTML page for configuring new game of chess.
    """
    return flask.send_from_directory("html", "new-game.html")


@app.route("/play")
def page_play():
    """
    Serve HTML page for playing chess.
    """
    return flask.send_from_directory("html", "play.html")


@app.route("/about")
def page_about():
    """
    Serve HTML page with rules and instructions.
    """
    return flask.send_from_directory("html", "about.html")


@app.route("/<path:path>")
def static(path):
    """
    Serve non-HTML static files.
    """
    return flask.send_from_directory("static", path)


@app.route("/api/v1/http", methods=["POST"])
def http_endpoint():
    """
    HTTP endpoint for API.
    """
    request = flask.request.get_json(silent=True)
    print(request)

    if request is not None:
        response = whales.api.query(request)
    else:
        response = whales.api.error_response("invalid or missing JSON")
    return flask.jsonify(response)
