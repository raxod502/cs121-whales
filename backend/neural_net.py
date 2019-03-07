import keras
import numpy as np
from keras.layers import Conv2D, Dense, Flatten
from keras.models import Sequential, model_from_json


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


# TODO: try using Conv3D


input_shape = (7, 8, 8)

model = Sequential(name="model 1")

# Convolutional Layer 1
model.add(
    Conv2D(
        # Somewhat arbitrarily chosen number of filters
        filters=32,
        # Kernel size also somewhat arbitrary
        # 5x5 is kind of large, when the input is only 8x8, the relevant
        # information in a chess board might be very spread out.
        kernel_size=(5, 5),
        # Because the data is 7x8x8, use channels_first (it defaults to channels
        # last)
        data_format="channels_first",
        activation="relu",
        input_shape=input_shape,
        # Padding allows it to use the kernel up against the edges and not lose
        # edge data
        # TODO: check how padding=same works
        #   (check if it replicates data along the edges, because we want the
        #    padding to be all 0s, not replicated data)
        padding="same",
    )
)

# Convolutional Layer 2
model.add(
    Conv2D(
        filters=64,
        kernel_size=(5, 5),
        data_format="channels_first",
        activation="relu",
        padding="same",
    )
)

# Convolutional Layer 3
model.add(
    Conv2D(
        filters=64,
        kernel_size=(5, 5),
        data_format="channels_first",
        activation="relu",
        padding="same",
    )
)

# Convolutional Layer 4
model.add(
    Conv2D(
        filters=64,
        kernel_size=(5, 5),
        data_format="channels_first",
        activation="relu",
        padding="same",
    )
)

# Fully connected final layers
model.add(Dense(units=32, activation="relu"))

# Flatten helps fix the dimensionality of the output of the first Dense layer,
# which is still a 3D matrix, down to a single vector which the final Dense
# layer can condense to a single scalar.
model.add(Flatten())

model.add(
    Dense(
        # We want only 1 output for final layer
        units=1,
        # Use activation function bounded between 1 and -1 (because that's how the
        # data is labeled)
        activation="tanh",
    )
)

model.compile(
    # Mean squared error
    loss=keras.losses.mse,
    # Randomly chosen optimizer
    optimizer=keras.optimizers.Adam(),
    metrics=["accuracy"],
)

# Print out a description of the model's structure
model.summary()

# Load in the training data
x = np.load("x_data_1000.npy")
y = np.load("y_data_1000.npy")

# Separate into training and validation

# What percent of the data to use as validation
validation_split = 0.2

# The index where the data switches from training to validation
split_point = int(x.shape[0] * (1 - validation_split))

x_training = x[:split_point]
y_training = y[:split_point]
x_validation = x[split_point:]
y_validation = y[split_point:]

# Flag to determine whether to train the model or just load the saved model.
train = False

if train:
    # Train and save the model
    history = model.fit(
        x=x_training,
        y=y_training,
        batch_size=128,
        epochs=1,
        verbose=1,  # Show progress bar
        validation_data=(x_validation, y_validation),
    )
    save_models([model])
else:
    model = load_models(["model 1"])[0]

# Predict all of the data in the validation set to get an idea of how the
# model is doing.
predictions = model.predict(x_validation)  # Has shape nx1
predictions = predictions.reshape(y_validation.shape)

# Compare predictions to the actual labels (creates an n array of booleans)
correct = ((predictions > 0) & (y_validation > 0)) | (
    (predictions < 0) & (y_validation < 0)
)

# Print the percentage of predictions that were correct
print(sum(correct) / correct.shape[0])
