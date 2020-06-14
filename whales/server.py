"""
Module that contains our Flask app.
"""

import os
import threading

import flask
import flask.json
import flask_talisman

import whales.api
import whales.util

app = flask.Flask(__name__, static_folder=None, template_folder="html")

if os.environ.get("WHALES_NO_SSL") in (None, "", "0"):
    flask_talisman.Talisman(app, content_security_policy=None)

analytics_enabled = bool(os.environ.get("WHALES_ANALYTICS"))


def stream_json(ping_secs):
    """
    Wrap a view that returns a Python object so that the object is
    JSONified before being returned. If the view takes longer than
    ping_secs to compute its result, send a byte of whitespace to the
    client so the connection is kept alive by Heroku.
    """

    def decorator(orig_view):
        def new_view(*args, **kwargs):
            def generate():
                result = whales.util.UNSET
                done = threading.Event()

                @flask.copy_current_request_context
                def handle():
                    nonlocal result
                    result = flask.json.dumps(orig_view(*args, **kwargs))
                    done.set()

                thread = threading.Thread(target=handle, daemon=True)
                thread.start()
                while True:
                    if done.wait(timeout=ping_secs):
                        yield result
                        break
                    yield " "

            generator = flask.stream_with_context(generate())
            return flask.Response(generator, mimetype="application/json")

        return new_view

    return decorator


@app.route("/")
def page_new_game():
    """
    Serve HTML page for configuring new game of chess.
    """
    return flask.render_template("new-game.html", analytics_enabled=analytics_enabled)


@app.route("/play")
def page_play():
    """
    Serve HTML page for playing chess.
    """
    return flask.render_template("play.html", analytics_enabled=analytics_enabled)


@app.route("/about")
def page_about():
    """
    Serve HTML page with rules and instructions.
    """
    return flask.render_template("about.html", analytics_enabled=analytics_enabled)


@app.route("/api/v1/http")
def http_endpoint_get():
    """
    Error with method not allowed.
    """
    flask.abort(405)


@app.route("/api/v1/http", methods=["POST"])
@stream_json(20)
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
    return response


@app.route("/<path:path>")
def static(path):
    """
    Serve non-HTML static files.
    """
    return flask.send_from_directory("static", path)
