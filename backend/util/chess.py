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
    game = chess.pgn.Game.without_tag_roster()
    node = game
    for move in board.move_stack:
        node = node.add_variation(move)
    return game
