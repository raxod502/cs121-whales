import os

import chess
import numpy as np
from keras.models import model_from_json

from whales.neural_net.chess_alpha_data import board_to_arrays_alpha_chess
from whales.neural_net.data_conversion import board_to_arrays


def save_neural_nets(neural_nets):
    """
    Save a list of Keras neural net Models to .json files and their
    weights to .h5 files. A neural net with net_name will be saved
    to net_name.json and net_name.h5 in the same directory as this
    file.
    """
    for neural_net in neural_nets:
        with open("{}.json".format(neural_net.name), "w") as file:
            file.write(neural_net.to_json())
            neural_net.save_weights("{}.h5".format(neural_net.name))


def load_neural_nets(net_names):
    """
    Load a list of Keras neural net Models from .json and .h5 files in
    the format net_name.json and net_name.h5, whose files are located
    in the same directory as this file.
    """
    neural_nets = []
    for index, name in enumerate(net_names):
        file_dir = os.path.dirname(__file__)
        file_path = os.path.join(file_dir, name)
        with open(file_path + ".json", "r") as file:
            neural_nets.append(model_from_json(file.read()))
            neural_nets[index].load_weights(file_path + ".h5")
    return neural_nets


def chess_alpha_zero_helper(board):
    """
    Get a prediction from the chess_alpha_zero neural net.
    Return [policy, value], where policy is a size 1968 vector of
    probabilities associated with each chess move to make next (higher
    probability seems to indicate a better move), and value is a number
    from -1 to 1 indicating how good the current board is for the player
    who moves next.
    """
    # Chess_alpha_zero's neural net wants prediction input to be in the
    # form nx18x8x8, so wrap the 18x8x8 board arrays in another list
    # before converting to numpy and feeding it to the net.
    array = [board_to_arrays_alpha_chess(board)]
    np_array = np.array(array, dtype=int)

    # Chess_alpha_zero returns [policy, value] predictions, and we want
    # the predictions of the first board in the list (though the list
    # does only have one board in it).
    policy, value = neural_net_dict["chess_alpha_zero"].predict(np_array)
    return policy[0], value[0]


### Copied from chess_alpha_zero repository, with docstring annotated
def create_uci_labels():
    """
    Create UCI labels for every chess move, put them into an array, and
    return the array.

    This is used to map between chess_alpha_zero's policy predictions
    and the labels of the moves the policy vector is referring to.
    """
    labels_array = []
    letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
    promoted_to = ["q", "r", "b", "n"]

    for l1 in range(8):
        for n1 in range(8):
            destinations = (
                [(t, n1) for t in range(8)]
                + [(l1, t) for t in range(8)]
                + [(l1 + t, n1 + t) for t in range(-7, 8)]
                + [(l1 + t, n1 - t) for t in range(-7, 8)]
                + [
                    (l1 + a, n1 + b)
                    for (a, b) in [
                        (-2, -1),
                        (-1, -2),
                        (-2, 1),
                        (1, -2),
                        (2, -1),
                        (-1, 2),
                        (2, 1),
                        (1, 2),
                    ]
                ]
            )
            for (l2, n2) in destinations:
                if (l1, n1) != (l2, n2) and l2 in range(8) and n2 in range(8):
                    move = letters[l1] + numbers[n1] + letters[l2] + numbers[n2]
                    labels_array.append(move)
    for l1 in range(8):
        l = letters[l1]
        for p in promoted_to:
            labels_array.append(l + "2" + l + "1" + p)
            labels_array.append(l + "7" + l + "8" + p)
            if l1 > 0:
                l_l = letters[l1 - 1]
                labels_array.append(l + "2" + l_l + "1" + p)
                labels_array.append(l + "7" + l_l + "8" + p)
            if l1 < 7:
                l_r = letters[l1 + 1]
                labels_array.append(l + "2" + l_r + "1" + p)
                labels_array.append(l + "7" + l_r + "8" + p)
    return labels_array


def model_1_prediction(board):
    """
    Evaluate the board using the neural net 'model 1', and return a
    single value where 1 means the board is good for white and -1
    means the board is good for black.
    """
    # The 'model 1' neural net wants prediction input to be in the form
    # nx7x8x8, so wrap the 7x8x8 board arrays in another list before
    # converting to numpy and feeding it to the net.
    array = [board_to_arrays(board)]
    np_array = np.array(array, dtype=int)

    return neural_net_dict["model 1"].predict(np_array)[0][0]


def chess_alpha_value(board):
    """
    Evaluate the board using the chess_alpha_zero neural net, and
    return a single value where 1 means the board is good for white and
    -1 means the board is good for black.
    """
    policy, value = chess_alpha_zero_helper(board)

    # Chess_alpha_zero rates the board using 1 to represent the board
    # being good for the player that just moved. The minimax expects
    # the board to be rated as 1 if good for white and -1 if good for
    # black, so convert from chess_alpha's representation to the
    # minimax's before returning.
    # TODO: QUESTION FOR BEN: WHAT DOES MINIMAX WANT?
    if board.turn == chess.BLACK:
        value *= -1
    return value


def new_model_prediction(boards):
    """
    Predict the likelihood of the moving player winning for multiple
    chess boards using the chess_alpha_zero neural net.

    :param (list(python-chess Board)) boards: A list of boards
    representing the current state of the multiple games

    :return ((n, 1) float numpy array): Values between -1 and 1, which
    are predictions of how good each board is for the moving player (1
    is good, -1 is bad)
    """
    array = [board_to_arrays_alpha_chess(b) for b in boards]
    np_array = np.array(array, dtype=int)
    values = neural_net_dict["chess_alpha_zero"].predict(np_array)[1]
    return values


move_labels = create_uci_labels()


def chess_alpha_policy(board):
    """
    Evaluate the board using the chess_alpha_zero neural net, and
    return the UCI representation of the move that the policy network
    rates as having the highest probability.
    """
    policy, value = chess_alpha_zero_helper(board)

    # Find the index of the move with the highest probability.
    best_move_index = policy.index(max(policy))
    best_move = move_labels[best_move_index]
    return best_move


# Hardcoded list of names of neural nets to use.
# TODO: check if there is a better way to integrate this list with models.py
# NOTE: don't change this list of neural net names without also
# changing model_predict_func_dict!
neural_net_names = ["model 1", "chess_alpha_zero"]

# TODO: (optional optimization) lazily load neural nets rather than upfront
# Load every Keras neural net Model, then store them in a dictionary
# mapping from name to neural net.
neural_nets = load_neural_nets(neural_net_names)
# Adding a net._make_predict_function() call after every load
# seems to stop a weird error.
for net in neural_nets:
    net._make_predict_function()

neural_net_dict = {}
for i in range(len(neural_net_names)):
    neural_net_dict[neural_net_names[i]] = neural_nets[i]

# This dictionary specifies the function to call to get a prediction
# for each of the models specified in models.py.
model_predict_func_dict = {
    "model 1": model_1_prediction,
    "chess_alpha_zero": chess_alpha_value,
    "alt_minimax": new_model_prediction,
    "chess_alpha_zero_policy": chess_alpha_policy,
}


def evaluation_function(board, model_name):
    """
    Take in a board, call the function associated with that model, and
    return the neural net's prediction. This prediction might be a
    board evaluation (number from -1 to 1), a list of board
    evaluations, a move, or other, depending on the function called.
    This means that models using evaluation_function should take care
    to ensure that they are going to receive the kind of output
    that they are expecting.
    """
    # Use the prediction function associated with the given model.
    return model_predict_func_dict[model_name](board)
