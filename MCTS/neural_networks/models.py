from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD


def get_dense_model(layers: list, loss="categorical_crossentropy", optimizer=SGD, activation: list = None, learn_rate=0.1):
    if activation is None:
        activation = ["relu"] * len(layers)   # default linear?

    dense_model = Sequential()
    dense_model.add(Dense(layers[0], input_dim=layers[0]))
    for i in range(1, len(layers)):
        dense_model.add(Dense(layers[i], activation=activation[i]))
    dense_model.compile(loss=loss, optimizer=optimizer(lr=learn_rate))  # clipvalue=1
    return dense_model
