"""
Module containing the neural nets. When this file is run, it loads all
neural nets and stores them in NEURAL_NETS. Outside actors wanting to
get the prediction of a chess board from a neural net named 'net_name'
should call NEURAL_NET_PREDICT[net_name](board). This can also be used
to get the predictions of a list of boards.
"""
import os

import numpy as np
from keras.models import model_from_json

from whales.neural_net.chess_alpha_data import board_to_arrays_alpha_chess


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


def chess_alpha_zero_helper(board_input):
    """
    Get a prediction from the chess_alpha_zero neural net.
    Return [policy, value], where policy is a size 1968 vector of
    probabilities associated with each chess move to make next (higher
    probability seems to indicate a better move), and value is a number
    from -1 to 1 indicating how good the current board_input is for the
    player who moves next.

    Board_input can be either a single board or a list of boards. In
    either case the policy and value returned will be vectors.
    """
    if type(board_input) != list:
        # Chess_alpha_zero's neural net wants prediction input to be in
        # the form nx18x8x8, so wrap the 18x8x8 board_input array in
        # another list.
        array = [board_to_arrays_alpha_chess(board_input)]
    else:
        # Otherwise we can just convert each chess board to the
        # nx18x8x8 representation because they're already in a list.
        array = [board_to_arrays_alpha_chess(b) for b in board_input]

    # Convert to numpy and feed to the neural net.
    np_array = np.array(array, dtype=int)
    return NEURAL_NET_DICT["chess_alpha_zero"].predict(np_array)


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


# Hardcoded list of names of neural nets to use.
NEURAL_NET_NAMES = ["chess_alpha_zero"]

# TODO: (optional optimization) lazily load neural nets rather than upfront
# Load every Keras neural net Model, then store them in a dictionary
# mapping from name to neural net.
NEURAL_NETS = load_neural_nets(NEURAL_NET_NAMES)
# Adding a net._make_predict_function() call after every load
# seems to stop a weird error.
for net in NEURAL_NETS:
    net._make_predict_function()

NEURAL_NET_DICT = {}
for i in range(len(NEURAL_NET_NAMES)):
    NEURAL_NET_DICT[NEURAL_NET_NAMES[i]] = NEURAL_NETS[i]

# A dictionary mapping from the name of a neural net to a function that
# takes in a board or list of boards, and returns that neural net's
# prediction of that input.
NEURAL_NET_PREDICT = {"chess_alpha_zero": lambda b: chess_alpha_zero_helper(b)}
