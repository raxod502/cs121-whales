import functools
import operator
import random

from whales.minimax_ab import minimax
from whales.neural_net.interface import evaluation_function as neural_net_eval
import whales.util.chess


class NoSuchModelError(Exception):
    """
    Exception raised when you try to use a model that doesn't exist.
    """

    pass


def model_random(pgn):
    """
    Model that makes random moves.
    """
    board = whales.util.chess.pgn_to_board(pgn)
    move = random.choice(list(board.legal_moves))
    board.push(move)
    return whales.util.chess.board_to_pgn(board)


def model_material_depth1(pgn):
    """
    Model that uses a depth 1 minimax tree with evaluation function
    based on how much relative material each color has
    """
    board = whales.util.chess.pgn_to_board(pgn)
    move = minimax.minimax(board, max_depth=2, eval_fn=minimax.eval_material)[1]
    board.push(move)
    return whales.util.chess.board_to_pgn(board)


def model_neural_depth1(pgn, model_name):
    """
    Model that uses a depth 1 minimax tree with evaluation function
    using a neural net
    """
    board = whales.util.chess.pgn_to_board(pgn)
    move = minimax.minimax(
        board,
        max_depth=2,
        eval_fn=functools.partial(neural_net_eval, model_name=model_name),
    )[1]
    board.push(move)
    return whales.util.chess.board_to_pgn(board)


def new_model(pgn, model_name):
    """
    Model that uses a depth 1 minimax tree with evaluation function
    using a neural net
    """
    board = whales.util.chess.pgn_to_board(pgn)
    move = minimax.alt_minimax(
        board, eval_fn=functools.partial(neural_net_eval, model_name=model_name)
    )
    board.push(move)
    return whales.util.chess.board_to_pgn(board)


def chess_alpha_zero_policy(pgn, model_name):
    """
    Model that uses the chess_alpha_zero policy prediction to pick its
    next move
    """
    board = whales.util.chess.pgn_to_board(pgn)
    move_uci = neural_net_eval(board, model_name)
    move = whales.util.chess.convert_move(move_uci)
    board.push(move)
    return whales.util.chess.board_to_pgn(board)


MODELS = {
    "random": {
        "display_name": "Easy",
        "description": "Make random moves",
        "callable": model_random,
    },
    "neuralnet-depth1-model-1": {
        "display_name": "Normal",
        "description": "'Model 1' neural net evaluation function using depth 1 minimax",
        "callable": functools.partial(model_neural_depth1, model_name="model 1"),
    },
    "neuralnet-depth1-chess-alpha-zero": {
        "display_name": "Hard",
        "description": "Chess-Alpha-Zero neural net evaluation function using depth 1 minimax",
        "callable": functools.partial(
            model_neural_depth1, model_name="chess_alpha_zero"
        ),
    },
    "new": {
        "display_name": "New",
        "description": "Simple evaluation with neural net with alternative minimax",
        "callable": functools.partial(new_model, model_name="alt_minimax"),
    },
    "neuralnet-no-minimax-chess-alpha-zero": {
        "display_name": "Medium",
        "description": "Simple evaluation exclusively using the chess-alpha-zero neural network",
        "callable": functools.partial(new_model, model_name="alt_minimax"),
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
