"""
Module containing utility functions wrapping python-chess.
"""

import io

import chess.pgn
import chess


class InvalidPGNError(Exception):
    """
    Error raised when parsing invalid PGN.
    """

    pass


class SilentGameCreator(chess.pgn.GameCreator):
    """
    Visitor for chess.pgn.read_game that raises InvalidPGNError on an
    exception instead of logging the exception.
    """

    def handle_error(self, error):
        raise InvalidPGNError


def pgn_to_board(pgn):
    """
    Convert a PGN string into a python-chess Board object.

    Interpret an empty PGN string as a game with no moves.
    """
    if not pgn:
        pgn = "-"
    game = chess.pgn.read_game(io.StringIO(pgn), Visitor=SilentGameCreator)
    return game.end().board()


def board_to_pgn(board):
    """
    Convert a python-chess Board object into a PGN string.
    """
    game = chess.pgn.Game.from_board(board)
    game.headers.clear()
    return str(game)
