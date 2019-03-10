#!/usr/bin/env python3

import os

import flask

import api

app = flask.Flask(__name__, static_folder=None)


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
        response = api.query(request)
    else:
        response = api.error_response("invalid or missing JSON")
    return flask.jsonify(response)


if __name__ == "__main__":
    port = os.environ.get("PORT")
    if port:
        try:
            port = int(port)
        except ValueError:
            port = None
    if not port:
        port = 5000
    app.run(port=port)
