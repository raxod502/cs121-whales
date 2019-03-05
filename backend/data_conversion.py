import chess.pgn
import chess
import numpy as np
import os
import sys
from timeit import default_timer as timer


def pgn_to_npy(pgn_file, x_file_name, y_file_name):
    """
    Reads in all of the chess games in pgn_file, converts them to
    numpy arrays, and save those arrays to x_file_name and
    y_file_name.
    """
    x, y = file_to_arrays(pgn_file)
    arrays_to_file(x, y, x_file_name, y_file_name)


def compare_times(num_games, pgn_file):
    """
    Computes the time it takes to process the given number of games
    from a .pgn file into numpy arrays, writes those arrays to files,
    and computes the time it takes to read the arrays back out of the
    files.
    """
    x_test_file_name = 'x_test.npy'
    y_test_file_name = 'y_test.npy'

    print("Comparing the time to process or read " + str(num_games)
          + " games...")

    process_start_time = timer()
    x, y = file_to_arrays(pgn_file, num_games)
    process_end_time = timer()
    process_total_time = process_end_time - process_start_time

    arrays_to_file(x,
                   y,
                   x_file_name=x_test_file_name,
                   y_file_name=y_test_file_name)

    read_start_time = timer()
    x_read = np.load(x_test_file_name)
    y_read = np.load(y_test_file_name)
    read_end_time = timer()
    read_total_time = read_end_time - read_start_time

    print("processing data time: " + str(process_total_time))
    print("reading data time: " + str(read_total_time))

    os.remove(x_test_file_name)
    os.remove(y_test_file_name)


def arrays_to_file(x_data,
                   y_data,
                   x_file_name='x_data.npy',
                   y_file_name='y_data.npy'):
    """
    Writes the two input numpy arrays to .npy files.
    """
    np.save(x_file_name, x_data)
    np.save(y_file_name, y_data)


def file_to_arrays(filename, max_games=sys.maxsize):
    """
    Reads in a .pgn file and returns two NumPy arrays, one with
    dimensions nx7x8x8 where n is the total number of board
    positions in all of the games in the .pgn file, and one that is
    n, which labels who won the game that each position came from.
    """
    # Initialize the data to contain a single empty set of placeholder
    # 'boards', to set the size of the NumPy arrays.
    x_data = np.zeros((1, 7, 8, 8), dtype=int)
    y_data = np.zeros(1, dtype=int)

    with open(filename) as chess_file:
        # Continually read games and write to the NumPy arrays until
        # there are no more games to read.
        game = chess.pgn.read_game(chess_file)
        num_games = 1
        while game is not None and num_games < max_games:
            x_data, y_data = game_to_arrays(game, x_data, y_data)
            game = chess.pgn.read_game(chess_file)
            num_games += 1

    # Remove the initial placeholder 'boards'.
    return x_data[1:], y_data[1:]


def game_to_arrays(game, x_data, y_data):
    """
    Extracts board positions out of the given game and adds the new
    board positions and labels to the bottom of the input data,
    which is then returned.
    """
    # Until the entire game has been processed, use Python lists,
    # because they're easier to work with.
    new_x_data = []
    board = game.board()

    # Every board position in the game gets added to the data.
    for move in game.mainline_moves():
        board.push(move)
        new_x_data.append(board_to_arrays(board))

    numpy_x_data = np.array(new_x_data, dtype=int)
    num_positions = numpy_x_data.shape[0]

    # Use game.headers result, not board.result(), because many
    # Lichess games ended in someone resigning, which is tracked
    # by the header but not by the board. Currently we treat a resign
    # as a loss.
    if game.headers['Result'] == '1-0':
        result = 1
    elif game.headers['Result'] == '0-1':
        result = -1
    # If the game ended in a draw, throw away the new data.
    else:
        return x_data, y_data

    # Create the column of labels.
    numpy_y_data = np.full(num_positions, result, dtype=int)

    # vstack the games to get a nx7x8x8 array, but hstack the labels
    # to get an n array instead of a nx1 array.
    return np.vstack((x_data, numpy_x_data)), np.hstack((y_data, numpy_y_data))


def board_to_arrays(board):
    """
    Creates a 7x8x8 Python list representing a chess board. The first
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
    # Create the empty 6x8x8 array
    data = [[[0]*8 for i in range(8)] for j in range(6)]

    board_from_type = {chess.PAWN: 0,
                       chess.KNIGHT: 1,
                       chess.BISHOP: 2,
                       chess.ROOK: 3,
                       chess.QUEEN: 4,
                       chess.KING: 5}
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
        data.append([[1]*8 for i in range(8)])
    elif board.turn == chess.BLACK:
        data.append([[-1]*8 for i in range(8)])

    return data
