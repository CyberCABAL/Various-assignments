from . import GenericNeuralCritic

from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras import Sequential


class DenseNeuralCritic(GenericNeuralCritic):
    def __init__(self, learn_rate: float, trace_decay: float, discount: float = 0.9):
        super().__init__(None, learn_rate, trace_decay, discount)

    def setup_model(self, layers: list):
        model = Sequential()

        model.add(Dense(layers[0], input_dim=layers[0]))
        for l in layers[1:]:
            model.add(Dense(l))
        model.compile(loss="mse", optimizer=SGD(lr=self.learn_rate))
        self.association = model
