import chess
import numpy as np
import os

from functools import partial
from keras.models import model_from_json
from whales.neural_net.chess_alpha_data import board_to_arrays_alpha_chess
from whales.neural_net.data_conversion import board_to_arrays


def save_models(models):
    """
    Saves a list of models to .json files and their weights to .h5
    files.
    """
    for model in models:
        with open("{}.json".format(model.name), "w") as file:
            file.write(model.to_json())
        model.save_weights("{}.h5".format(model.name))


def load_models(model_names):
    """
    Loads a list of models from .json and .h5 files labeled with
    the name of each model.
    """
    models = []
    for index, name in enumerate(model_names):
        file_dir = os.path.dirname(__file__)
        file_path = os.path.join(file_dir, name)
        with open(file_path + ".json", "r") as file:
            models.append(model_from_json(file.read()))
        models[index].load_weights(file_path + ".h5")
    return models


def model_1_prediction(model, board):
    """
    Get a prediction from a neural net which returns a single prediction
    where 1 means the board is good for white and -1 means the board is
    good for black.
    """
    # Model 1's neural net wants prediction input to be in the form nx7x8x8, so
    # wrap the 7x8x8 board arrays in another list before converting to numpy and
    # feeding it to the net.
    array = [board_to_arrays(board)]
    np_array = np.array(array, dtype=int)

    return model.predict(np_array)[0][0]


def model_alpha_prediction(model, board):
    """
    Get a prediction from a neural net which returns [policy, value]
    (where the second prediction is the board evaluation), and where the
    board evaluation rates the board as 1 if it is good for the player
    who moves next.
    """
    # Chess_alpha_zero's neural net wants prediction input to be in the form nx18x8x8, so
    # wrap the 18x8x8 board arrays in another list before converting to numpy and
    # feeding it to the net.
    array = [board_to_arrays_alpha_chess(board)]
    np_array = np.array(array, dtype=int)

    # Chess_alpha_zero returns [policy, value] predictions, and we want the value prediction,
    # of the first board in the list (though the list does only have one board in it).
    prediction = model.predict(np_array)[1][0]

    # Chess_alpha_zero rates the board using 1 to represent the board being good for the player
    # that just moved. The minimax expects the board to be rated as 1 if good for white and -1
    # if good for black, so convert from chess_alpha's representation to the minimax's before returning.
    # QUESTION FOR BEN: WHAT DOES MINIMAX WANT?
    if board.turn == chess.BLACK:
        prediction *= -1
    return prediction


def new_model_prediction(model, boards):
    array = [board_to_arrays_alpha_chess(b) for b in boards]
    np_array = np.array(array, dtype=int)
    values = model.predict(np_array)[1]
    return values


# Hardcoded list of names of models to use
# TODO: check if there is a better way to integrate this list with models.py
# NOTE: don't change this list of model names without also changing model_predict_func_dict
model_names = ["model 1", "chess_alpha_zero"]

# TODO: (optional optimization) lazily load models rather than upfront
# Load every model, then store them in a dictionary mapping from name to model.
models = load_models(model_names)
# Adding a mode._make_predict_function() call after every model load seems to stop a weird error.
for model in models:
    model._make_predict_function()

model_dict = {}
for i in range(len(model_names)):
    model_dict[model_names[i]] = models[i]

# Name of the model to load, and the function to call to get the prediction
model_predict_func_dict = {
    "model 1": partial(model_1_prediction, model_dict["model 1"]),
    "chess_alpha_zero": partial(model_alpha_prediction, model_dict["chess_alpha_zero"]),
    "alt_minimax": partial(new_model_prediction, model_dict["chess_alpha_zero"]),
}


def evaluation_function(board, model_name="chess_alpha"):
    """
    Takes in a board, uses a neural net to classify the board as one
    leading to white winning or black winning, and returns the
    classification.
    """
    # Use the prediction function associated with the given model.
    return model_predict_func_dict[model_name](board)
