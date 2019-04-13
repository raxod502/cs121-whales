import argparse
import os
import numpy as np

from whales.neural_net.interface import load_models


def test_net(model_name: str, data_name: str, use_chess_alpha: bool):
    """
    Compare the predictions from the given chess neural net to
    the actual results of the games, and print the percent of the
    boards that the neural net predicted correctly.

    :param model_name: the name of the model to load.
    - There should be files '{model_name}.h5' and '{model_name}.json'
      to specify the configuration and weights of the model in the same
      directory as this file.
    - The model should be able to take in data representing a chess
      board and return a value between -1 and 1 predicting whether
      black or white will win.

    :param data_name: the name of the data to test the model on.
    - There should be files 'x_{data_name}.npy' and 'y_{data_name}.npy'
      in the same directory as this file. It is the responsibility of
      the user of this function to ensure that the data is in the
      correct format for the neural net being tested.

    :param use_chess_alpha: if enabled, assumes that the board
      evaluation is the second column in the neural net predictions
    """
    model = load_models(model_names=[model_name])[0]

    # Load in the data.
    file_dir = os.path.dirname(__file__)
    x = np.load(os.path.join(file_dir, f"x_{data_name}.npy"))
    y = np.load(os.path.join(file_dir, f"y_{data_name}.npy"))

    # Predict all of the data in the validation set to get an idea of
    # how the model is doing.

    print("\nPredicting...")
    # If the neural net only evaluate the board (ie, returns [value]),
    # "predictions" has shape nx1.
    predictions = model.predict(x)

    # If the neural net returns [policy, value] for predictions,
    # "predictions" has shape nx2x1, so grab the board evaluations
    # (value) to turn it back to nx1.
    if use_chess_alpha:
        predictions = predictions[1]

    predictions = predictions.reshape(y.shape)

    # Compare predictions to the actual labels (creates an n array of
    # booleans). If the game was actually won by white (represented by
    # a 1) and the neural net gave the board any positive value, this
    # counts as a correct prediction. The same is true for black and
    # negative values.
    correct = ((predictions > 0) & (y > 0)) | ((predictions < 0) & (y < 0))

    # Print the percentage of predictions that were correct.
    print(sum(correct) / correct.shape[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "model_name",
        help="the name of the model to test. There should be "
        "<model_name>.json and <model_name>.h5 files in "
        "app/neural_net/",
    )
    parser.add_argument(
        "data_name",
        help="the name of the data to use. There should be "
        "x_<data_name>.npy and y_<data_name>.npy files in "
        "app/neural_net/",
    )
    parser.add_argument(
        "-use_chess_alpha",
        help="Assume that board evaluation will be the second column "
        "in the predictions returned by neural net (the first likely "
        "being policy)",
        # Makes the flag a boolean.
        action="store_true",
    )

    args = parser.parse_args()
    test_net(args.model_name, args.data_name, args.use_chess_alpha)
