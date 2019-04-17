"""
Module containing the backend models which users can select to play
against in the app. A model is a function that takes a PGN string and
returns a new PGN string with an additional move. Passing a model a PGN
string that is a completed game produces an unspecified result, but
should not be an error. (Malformed PGN may produce an InvalidPGNError.)

For convenience, mostly this module defines functions which *return* a
model, so that you can easily construct models with different parameters
substituted in.
"""

import operator
import random

import whales.minimax_ab.minimax as minimax
import whales.neural_net.interface as neural_net
import whales.util.chess


class NoSuchModelError(Exception):
    """
    Exception raised when you try to use a model that doesn't exist.
    """

    pass


def model_random():
    """
    Return a model that makes random moves.
    """

    def model(pgn):
        board = whales.util.chess.pgn_to_board(pgn)
        move = random.choice(list(board.legal_moves))
        board.push(move)
        return whales.util.chess.board_to_pgn(board)

    return model


def model_neural_net(nn_name):
    """
    Return a model that uses a neural net to predict optimal moves. The
    neural net must return move data in UCI format.
    """

    def model(pgn):
        board = whales.util.chess.pgn_to_board(pgn)
        move_uci = neural_net.evaluation_function(board, nn_name)
        move = whales.util.chess.convert_move(move_uci)
        board.push(move)
        return whales.util.chess.board_to_pgn(board)

    return model


def model_onlymax(eval_fn):
    """
    Return a model that uses minimax with a depth of 1/2, meaning only
    looking at the possible next moves and not at any potential
    countermoves.
    """

    def model(pgn):
        board = whales.util.chess.pgn_to_board(pgn)
        move = minimax.alt_minimax(board, eval_fn=eval_fn)
        board.push(move)
        return whales.util.chess.board_to_pgn(board)

    return model


def model_onlymax_with_neural_net(nn_name):
    """
    Return a model that uses minimax with a depth of 1/2, with the given
    neural network as the evaluation function. The neural network must
    return a list of floating-point numbers when given a list of boards.
    """

    def eval_fn(boards):
        return neural_net.evaluation_function(boards, nn_name)

    return model_onlymax(eval_fn)


def model_minimax(depth, eval_fn):
    """
    Return a model that uses minimax to the given depth with the given
    evaluation function to find the optimal move.

    To use a neural net as the evaluation function, see
    `model_minimax_with_neural_net` instead.
    """

    def model(pgn):
        board = whales.util.chess.pgn_to_board(pgn)
        result = minimax.minimax(board, max_plies=depth, eval_fn=eval_fn)
        move = result[1]
        board.push(move)
        return whales.util.chess.board_to_pgn(board)

    return model


def model_minimax_with_neural_net(depth, nn_name):
    """
    Return a model that uses minimax to the given depth with the neural
    net by the given name as the evaluation function to find the optimal
    move.

    The given neural net must return a floating-point number evaluating
    the desirability of the board state.
    """

    def eval_fn(board):
        return neural_net.evaluation_function(board, nn_name)

    return model_minimax(depth, eval_fn)


MODELS = {
    "random": {
        "display_name": "Easy",
        "description": "Make random moves",
        "callable": model_random(),
    },
    "neuralnet-depth1-model-1": {
        "display_name": "Normal",
        "description": "'Model 1' neural net evaluation function using depth 1 minimax",
        "callable": model_minimax_with_neural_net(depth=1, nn_name="model 1"),
    },
    "neuralnet-no-minimax-chess-alpha-zero": {
        "display_name": "Medium",
        "description": "Simple evaluation exclusively using the chess-alpha-zero neural network",
        "callable": model_onlymax_with_neural_net("alt_minimax"),
    },
    "neuralnet-depth1-chess-alpha-zero": {
        "display_name": "Hard",
        "description": "Chess-Alpha-Zero neural net evaluation function using depth 1 minimax",
        "callable": model_minimax_with_neural_net(depth=1, nn_name="chess_alpha_zero"),
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
