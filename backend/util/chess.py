import chess.pgn
import io


def pgn_to_board(pgn):
    """
    Convert a PGN string into a python-chess Board object.
    """
    return chess.pgn.read_game(io.StringIO(pgn)).board()


def board_to_pgn(board):
    """
    Convert a python-chess Board object into a PGN string.
    """
    raise NotImplementedError
