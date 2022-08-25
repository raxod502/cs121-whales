"""
Module containing the neural nets. When this file is run, it loads all
neural nets and stores them in NEURAL_NETS. Outside actors wanting to
get the prediction of a chess board from a neural net named 'net_name'
should call NEURAL_NET_PREDICT[net_name](board). This can also be used
to get the predictions of a list of boards.
"""
import os

import numpy as np
import onnxruntime as ort

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
        neural_nets.append(ort.InferenceSession(file_path + ".onnx"))
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
    if not isinstance(board_input, list):
        # Chess_alpha_zero's neural net wants prediction input to be in
        # the form nx18x8x8, so wrap the 18x8x8 board_input array in
        # another list.
        array = [board_to_arrays_alpha_chess(board_input)]
    else:
        # Otherwise we can just convert each chess board to the
        # nx18x8x8 representation because they're already in a list.
        array = [board_to_arrays_alpha_chess(b) for b in board_input]

    # Convert to numpy and feed to the neural net.
    np_array = np.array(array, dtype=np.float32)

    return NEURAL_NET_DICT["chess_alpha_zero"].run(None, {"input_1": np_array})


# Hardcoded list of names of neural nets to use.
NEURAL_NET_NAMES = ["chess_alpha_zero"]

# Load every neural net, then store them in a dictionary mapping from
# name to neural net.
NEURAL_NETS = load_neural_nets(NEURAL_NET_NAMES)

NEURAL_NET_DICT = {}
for i, net_name in enumerate(NEURAL_NET_NAMES):
    NEURAL_NET_DICT[net_name] = NEURAL_NETS[i]

# A dictionary mapping from the name of a neural net to a function that
# takes in a board or list of boards, and returns that neural net's
# prediction of that input.
NEURAL_NET_PREDICT = {"chess_alpha_zero": chess_alpha_zero_helper}
