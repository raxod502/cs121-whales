import operator
import random
import util.chess
from minimax_ab import minimax
from neural_net.interface import evaluation_function as neural_net_eval


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


def model_material_depth1(pgn):
    """
    Model that uses a depth 1 minimax tree with evaluation function
    based on how much relative material each color has
    """
    board = util.chess.pgn_to_board(pgn)
    move = minimax.minimax(board, max_plies=1, eval_fn=minimax.eval_material)[1]
    board.push(move)
    return util.chess.board_to_pgn(board)


def model_neural_depth1(pgn):
    """
    Model that uses a depth 2 minimax tree with evaluation function
    using neural net
    """
    board = util.chess.pgn_to_board(pgn)
    move = minimax.minimax(
        board, max_plies=1, eval_fn=neural_net_eval, starting_player=board.turn
    )[1]
    board.push(move)
    return util.chess.board_to_pgn(board)


MODELS = {
    "random": {
        "display_name": "Random",
        "description": "Make random moves",
        "callable": model_random,
    },
    "material-depth1": {
        "display_name": "Minimax depth 1 using material",
        "description": "Simple material evaluation function using depth 1 minimax",
        "callable": model_material_depth1,
    },
    "neuralnet-depth1": {
        "display_name": "Minimax depth 1 using neural net",
        "description": "Neural net evaluation function using depth 1 minimax",
        "callable": model_neural_depth1,
    },
}


def get_model_info():
    """
    Return a list of dicts that can be returned from the API when the
    frontend asks for a list of models and their information.
    """
    info_list = []
    for model, info in MODELS.items():
        info_list.append(
            {
                "internalName": model,
                "displayName": info["display_name"],
                "description": info["description"],
            }
        )
    info_list.sort(key=operator.itemgetter("internalName"))
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
