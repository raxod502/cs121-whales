import functools
import random
import util.chess


class NoSuchModelError(Exception):
    """
    Exception raised when you try to use a model that doesn't exist.
    """
    pass


def model_random(pgn):
    """
    Model that makes random moves.
    """
    board = util.chess.pgn_to_board(pgn)
    move = random.choice(list(board.legal_moves))
    board.push(move)
    return util.chess.board_to_pgn(board)


MODELS = {
    "random": {
        "display_name": "Random",
        "description": "Make random moves",
        "callable": model_random,
    },
}


def get_model_info():
    """
    Return a list of dicts that can be returned from the API when the
    frontend asks for a list of models and their information.
    """
    info_list = []
    for model, info in MODELS.items():
        info_list.append({
            "internalName": model,
            "displayName": info["display_name"],
            "description": info["description"],
        })
    info_list.sort(key=functools.attrgetter("internalName"))
    return info_list


def run_model(model_name, pgn):
    """
    Given the internal name of a model and a PGN string, run the model
    and return a PGN string. If there is no model by that name, raise
    NoSuchModelError.
    """
    if model_name not in MODELS:
        raise NoSuchModelError
    return MODELS[model_name]["callable"](pgn)
