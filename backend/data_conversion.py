import chess.pgn
import chess
import numpy as np


def file_to_arrays(filename):
    """
    Reads in a .pgn file and returns a NumPy array with dimensions
    nx7x8x8 where n is the total number of board positions in all of
    the games in the .pgn file.
    """
    # Initialize the data to contain a single empty set of placeholder
    # 'boards', to set the size of the NumPy array.
    data = np.zeros((1, 7, 8, 8))

    with open(filename) as chess_file:
        # Continually read games and write to the NumPy arrays until
        # there are no more games to read.
        game = chess.pgn.read_game(chess_file)
        while game is not None:
            data = game_to_arrays(game, data)
            game = chess.pgn.read_game(chess_file)

    # Remove the initial placeholder 'boards'.
    return data[1:]


def game_to_arrays(game, data):
    """
    Appends a nx7x8x8x numpy array, where n is the number of board
    positions that occurred during that game, to the passed in data.
    The modified array is returned.
    """
    # Until the entire game has been processed, use Python lists,
    # because they're easier to work with.
    new_data = []
    board = game.board()

    # Every board position in the game gets added to the data.
    for move in game.mainline_moves():
        board.push(move)
        new_data.append(board_to_arrays(board))

    numpy_data = np.array(new_data)

    # Convert to NumPy and return.
    return np.vstack((data, numpy_data))


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
    # Create the empty 8x8x6 array
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
            square_num = 8*row + col
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
