import numpy as np

from data_conversion import board_to_arrays
from keras.models import model_from_json


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
        with open(name + ".json", "r") as file:
            models.append(model_from_json(file.read()))
        models[index].load_weights(name + ".h5")
    return models


def evaluation_function(board):
    """
    Takes in a board, uses a neural net to classify the board as one
    leading to white winning or black winning, and returns the
    classification.
    """
    model = load_models(["model 1"])[0]

    # The neural net wants prediction input to be in the form nx7x8x8, so
    # wrap the 7x8x8 board arrays in another list.
    array = [board_to_arrays(board)]
    np_array = np.array(array, dtype=int)

    return model.predict(np_array)