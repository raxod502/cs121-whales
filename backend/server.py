#!/usr/bin/env python3

import models
import util.chess

import flask

app = flask.Flask(__name__)


class APIError(Exception):
    pass


@app.route("/api/v1")
def api():
    try:
        response = []
        json = flask.request.get_json(silent=True)
        if not isinstance(json, dict):
            raise APIError("invalid or missing JSON")
        if "command" not in json:
            raise APIError("no command specified")
        command = json["command"]
        if command == "list_models":
            info = models.get_model_info()
            response = {
                "models": info,
            }
        elif command == "get_move":
            for param in ["model", "pgn"]:
                if param not in json:
                    raise APIError("missing required parameter {}"
                                   .format(repr(param)))
            model_name = json["model"]
            old_pgn = json["pgn"]
            try:
                new_pgn = models.run_model(model_name, old_pgn)
            except models.NoSuchModelError:
                raise APIError("unknown model {}".format(repr(model_name)))
            except util.chess.InvalidPGNError:
                raise APIError("invalid PGN")
            response = {
                "pgn": new_pgn,
            }
        else:
            raise APIError("unknown command {}".format(repr(command)))
        response["error"] = None
    except APIError as e:
        response = {
            "error": str(e),
        }
    return flask.jsonify(response)


if __name__ == "__main__":
    app.run()
