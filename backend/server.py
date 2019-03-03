#!/usr/bin/env python3

import api

import flask

app = flask.Flask(__name__)

@app.route("/")
def begin():
    return flask.render_template('chess.html')

@app.route("/api/v1/http", methods=['POST'])
def http_endpoint():
    """
    HTTP endpoint for API.
    """
    request = flask.request.get_json(silent=True)

    if request is not None:
        response = api.query(request)
    else:
        response = api.error_response("invalid or missing JSON")
    return flask.jsonify(response)


if __name__ == "__main__":
    app.run()
