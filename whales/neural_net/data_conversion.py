import argparse
import os
import sys
from timeit import default_timer as timer

import chess
import chess.pgn
import numpy as np

from whales.neural_net.chess_alpha_data import board_to_arrays_alpha_chess


def pgn_to_npy(pgn_file: str, data_name: str, max_games: int, use_chess_alpha: bool):
    """
    Read in max_games of the chess games in pgn_file, convert them to
    numpy arrays, and save those arrays to the new files
    x_<data_name>.npy and y_<data_name>.npy in the same directory as
    this file.

    pgn_file should be the full string name of a file ending in .pgn
    which is in the same directory as this file.

    Note that the .npy files are much faster to read numpy arrays from,
    but are also MUCH bigger.

    If use_chess_alpha is enabled, the chess data is converted to
    arrays in the format understood by the neural net from the
    chess_alpha_zero project. Otherwise, it is converted into the
    format understood by the neural net named 'model 1'.
    """
    # TODO: refactor to give max_games a default value as a parameter
    if max_games is None:
        max_games = sys.maxsize

    x, y = file_to_arrays(pgn_file, max_games, use_chess_alpha)

    file_dir = os.path.dirname(__file__)
    x_file_name = os.path.join(file_dir, f"x_{data_name}.npy")
    y_file_name = os.path.join(file_dir, f"y_{data_name}.npy")
    arrays_to_file(x, y, x_file_name, y_file_name)


def compare_times(num_games, pgn_file):
    """
    Compute the time it takes to process the given number of games
    from a .pgn file into numpy arrays, write those arrays to files,
    compute the time it takes to read the arrays back out of the
    files, and print these times.

    pgn_file should be the full string name of a file ending in .pgn
    which is in the same directory as this file.
    """
    x_test_file_name = "x_test.npy"
    y_test_file_name = "y_test.npy"

    print("Comparing the time to process or read " + str(num_games) + " games...")

    # Measure how long it takes to process the pgn file.
    process_start_time = timer()
    # TODO: update to match current file_to_arrays
    x, y = file_to_arrays(pgn_file, num_games)
    process_end_time = timer()
    process_total_time = process_end_time - process_start_time

    # Save the newly processed data to the test files.
    arrays_to_file(x, y, x_file_name=x_test_file_name, y_file_name=y_test_file_name)

    # Measure how long it takes to read the data from the files.
    read_start_time = timer()
    x_read = np.load(x_test_file_name)
    y_read = np.load(y_test_file_name)
    read_end_time = timer()
    read_total_time = read_end_time - read_start_time

    print("processing data time: " + str(process_total_time))
    print("reading data time: " + str(read_total_time))

    os.remove(x_test_file_name)
    os.remove(y_test_file_name)


def arrays_to_file(x_data, y_data, x_file_name, y_file_name):
    """
    Write the two input numpy arrays to .npy files in the same
    directory as this file.

    x_data and y_data should be numpy arrays, and each file name
    should end in .npy.
    """
    np.save(x_file_name, x_data)
    np.save(y_file_name, y_data)


def file_to_arrays(filename, max_games, use_chess_alpha):
    """
    Read in a .pgn file and returns two numpy arrays, one with
    dimensions nxmx8x8 where n is the total number of board
    positions in all of the games in the .pgn file and m depends on
    the encoding of the boards used (i.e. whether use_chess_alpha is
    enabled), and one that is n, which labels who won the game that
    each position came from.
    """
    # Initialize the data to contain a single empty set of placeholder
    # 'boards', to set the size of the numpy arrays.
    if use_chess_alpha:
        x_data = np.zeros((1, 18, 8, 8), dtype=int)
    else:
        x_data = np.zeros((1, 7, 8, 8), dtype=int)
    y_data = np.zeros(1, dtype=int)

    with open(filename) as chess_file:
        # Continually read games and write to the numpy arrays until
        # there are no more games to read.
        game = chess.pgn.read_game(chess_file)
        num_games = 0
        while game is not None and num_games < max_games:
            if num_games % 10 == 0:
                print("Converting game ", num_games)
            x_data, y_data = game_to_arrays(game, x_data, y_data, use_chess_alpha)
            game = chess.pgn.read_game(chess_file)
            num_games += 1

    # Remove the initial placeholder 'boards'.
    return x_data[1:], y_data[1:]


def game_to_arrays(game, x_data, y_data, use_chess_alpha):
    """
    Extract board positions out of the given game, add the new
    board positions and label to the bottom of the input data,
    and return the modified input data.
    """
    # Until the entire game has been processed, use Python lists,
    # because they're easier to work with.
    new_x_data = []
    board = game.board()

    # Every board position in the game gets added to the data.
    for move in game.mainline_moves():
        board.push(move)

        if use_chess_alpha:
            new_x_data.append(board_to_arrays_alpha_chess(board))
        else:
            new_x_data.append(board_to_arrays(board))

    numpy_x_data = np.array(new_x_data, dtype=int)
    num_positions = numpy_x_data.shape[0]

    # Use game.headers result, not board.result(), because many
    # Lichess games ended in someone resigning, which is tracked
    # by the header but not by the board. Currently we treat a resign
    # as a loss.
    if game.headers["Result"] == "1-0":
        result = 1
    elif game.headers["Result"] == "0-1":
        result = -1
    else:
        # If the game ended in a draw, throw away the new data.
        return x_data, y_data

    # Create the column of labels. For chess_alpha_zero, alternate back
    # and forth between 1 and -1 since chess_alpha_zero return values
    # from perspective of the moving player.
    # (Note that beginning game state fen is not included, so the first
    # fen is black's turn.)
    numpy_y_data = np.full(num_positions, result, dtype=int)
    if use_chess_alpha:
        numpy_y_data[::2] = -result

    # vstack the games to get a nxmx8x8 array, but hstack the labels
    # to get an n array instead of a nx1 array.
    return np.vstack((x_data, numpy_x_data)), np.hstack((y_data, numpy_y_data))


def board_to_arrays(board):
    """
    Create a 7x8x8 Python list representing a chess board. The first
    6 8x8 arrays represent the board for a different piece type, with 1
    indicating a white piece of that type, -1 indicating a black piece
    of that type, and 0 indicating empty. The final 8x8 board
    represents which color moves next, with all 1s being white and all
    -1s being black.
    The boards are in the following order:
    pawn
    knight
    bishop
    rook
    queen
    king
    turn
    """
    # Create the empty 6x8x8 array.
    data = [[[0] * 8 for i in range(8)] for j in range(6)]

    board_from_type = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5,
    }
    val_from_color = {chess.WHITE: 1, chess.BLACK: -1}

    # Loop through the squares by the indices they'll have in the 8x8
    # arrays.
    for row in range(8):
        for col in range(8):
            # Convert to the 0-63 indices used by the chess module.
            square_num = 8 * row + col
            piece = board.piece_at(square_num)
            if piece is None:
                continue

            # If there is a piece at that square, figure out which
            # board this piece affects, and which value should go in
            # that space.
            board_num = board_from_type[piece.piece_type]
            data[board_num][row][col] = val_from_color[piece.color]

    # Add on the final 8x8 array representing which color moves next.
    if board.turn == chess.WHITE:
        data.append([[1] * 8 for i in range(8)])
    elif board.turn == chess.BLACK:
        data.append([[-1] * 8 for i in range(8)])

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pgn_file", help="The name of the .pgn file to read in chess data from."
    )
    parser.add_argument(
        "data_name",
        help="The desired name of the converted data. It will get written to "
        "app/neural_net/x_<data_name>.npy and app/neural_net/y_<data_name>.npy.",
    )
    parser.add_argument(
        "-max_games",
        help="Set a maximum number of games to process from the .pgn file, "
        "instead of processing the entire file.",
        type=int,
    )

    # If enabled, writes the data in the numpy format understood by the
    # chess-alpha-zero neural net.
    parser.add_argument(
        "-use_chess_alpha",
        help="Process the data into the 18x8x8 arrays used by chess-alpha-zero, "
        "instead of the 7x8x8 default.",
        action="store_true",
    )

    args = parser.parse_args()

    pgn_to_npy(args.pgn_file, args.data_name, args.max_games, args.use_chess_alpha)
