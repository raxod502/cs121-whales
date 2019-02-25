#!/usr/bin/env python3

import flask

app = flask.Flask(__name__)


@app.route("/")
def hello():
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
