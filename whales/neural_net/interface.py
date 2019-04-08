import numpy as np
import os

from keras.models import model_from_json
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


# evil hack
model = load_models(["model 1"])[0]
model._make_predict_function()


def evaluation_function(board):
    """
    Takes in a board, uses a neural net to classify the board as one
    leading to white winning or black winning, and returns the
    classification.
    """
    # TODO: ensure the correct board-to-arrays conversion is happening for the model in use
    # (chess-alpha-zero uses a different board representation than 'model 1', for example)

    # The neural net wants prediction input to be in the form nx7x8x8, so
    # wrap the 7x8x8 board arrays in another list.
    array = [board_to_arrays(board)]
    np_array = np.array(array, dtype=int)

    return model.predict(np_array)[0][0]
