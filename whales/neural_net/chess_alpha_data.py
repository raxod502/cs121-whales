import enum
import numpy as np

# TODO: check if logging is actually needed
from logging import getLogger

logger = getLogger(__name__)


def board_to_arrays_alpha_chess(board):
    """
    Create an 18x8x8 Python list representing a chess board, in the
    format understood by the chess_alpha_zero neural net.

    pieces_order = "KQRBNPkqrbnp"   # 12x8x8
    castling_order = "KQkq"         # 4x8x8
    fifty-move-rule                 # 1x8x8
    en en_passant                   # 1x8x8
    """
    return canon_input_planes(board.fen())


####
# Below this point, the code is copied directly from chess-alpha-zero
####

# noinspection PyArgumentList
Winner = enum.Enum("Winner", "black white draw")

# input planes
# noinspection SpellCheckingInspection
pieces_order = "KQRBNPkqrbnp"  # 12x8x8
castling_order = "KQkq"  # 4x8x8
# fifty-move-rule               # 1x8x8
# en en_passant                 # 1x8x8

ind = {pieces_order[i]: i for i in range(12)}


def canon_input_planes(fen):
    """

    :param fen:
    :return : (18, 8, 8) representation of the game state
    """
    fen = maybe_flip_fen(fen, is_black_turn(fen))
    return all_input_planes(fen)


def all_input_planes(fen):
    current_aux_planes = aux_planes(fen)

    history_both = to_planes(fen)

    ret = np.vstack((history_both, current_aux_planes))
    assert ret.shape == (18, 8, 8)
    return ret


def maybe_flip_fen(fen, flip=False):
    if not flip:
        return fen
    foo = fen.split(" ")
    rows = foo[0].split("/")

    def swapcase(a):
        if a.isalpha():
            return a.lower() if a.isupper() else a.upper()
        return a

    def swapall(aa):
        return "".join([swapcase(a) for a in aa])

    return (
        "/".join([swapall(row) for row in reversed(rows)])
        + " "
        + ("w" if foo[1] == "b" else "b")
        + " "
        + "".join(sorted(swapall(foo[2])))
        + " "
        + foo[3]
        + " "
        + foo[4]
        + " "
        + foo[5]
    )


def aux_planes(fen):
    foo = fen.split(" ")

    en_passant = np.zeros((8, 8), dtype=np.float32)
    if foo[3] != "-":
        eps = alg_to_coord(foo[3])
        en_passant[eps[0]][eps[1]] = 1

    fifty_move_count = int(foo[4])
    fifty_move = np.full((8, 8), fifty_move_count, dtype=np.float32)

    castling = foo[2]
    auxiliary_planes = [
        np.full((8, 8), int("K" in castling), dtype=np.float32),
        np.full((8, 8), int("Q" in castling), dtype=np.float32),
        np.full((8, 8), int("k" in castling), dtype=np.float32),
        np.full((8, 8), int("q" in castling), dtype=np.float32),
        fifty_move,
        en_passant,
    ]

    ret = np.asarray(auxiliary_planes, dtype=np.float32)
    assert ret.shape == (6, 8, 8)
    return ret


# FEN board is like this:
# a8 b8 .. h8
# a7 b7 .. h7
# .. .. .. ..
# a1 b1 .. h1
#
# FEN string is like this:
#  0  1 ..  7
#  8  9 .. 15
# .. .. .. ..
# 56 57 .. 63

# my planes are like this:
# 00 01 .. 07
# 10 11 .. 17
# .. .. .. ..
# 70 71 .. 77
#


def alg_to_coord(alg):
    rank = 8 - int(alg[1])  # 0-7
    file = ord(alg[0]) - ord("a")  # 0-7
    return rank, file


def coord_to_alg(coord):
    letter = chr(ord("a") + coord[1])
    number = str(8 - coord[0])
    return letter + number


def to_planes(fen):
    board_state = replace_tags_board(fen)
    pieces_both = np.zeros(shape=(12, 8, 8), dtype=np.float32)
    for rank in range(8):
        for file in range(8):
            v = board_state[rank * 8 + file]
            if v.isalpha():
                pieces_both[ind[v]][rank][file] = 1
    assert pieces_both.shape == (12, 8, 8)
    return pieces_both


def replace_tags_board(board_san):
    board_san = board_san.split(" ")[0]
    board_san = board_san.replace("2", "11")
    board_san = board_san.replace("3", "111")
    board_san = board_san.replace("4", "1111")
    board_san = board_san.replace("5", "11111")
    board_san = board_san.replace("6", "111111")
    board_san = board_san.replace("7", "1111111")
    board_san = board_san.replace("8", "11111111")
    return board_san.replace("/", "")


def is_black_turn(fen):
    return fen.split(" ")[1] == "b"
