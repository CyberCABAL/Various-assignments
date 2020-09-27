from . import Critic
import numpy as np


class GenericNeuralCritic(Critic):
    def __init__(self, model, learn_rate: float, trace_decay: float, discount: float = 0.9):
        super().__init__(model, learn_rate, trace_decay, discount)

    def value(self, state):    # Must expand dims due to how TF handles batches.
        return self.association.predict(np.expand_dims(np.array([int(s) for s in state]), 0))[0]

    def update(self, state, error, eligibility: float = 1):   # V(s) ← V(s) + αδe(s)
        self.association.fit(np.expand_dims(np.array([int(s) for s in state]), 0),
                             self.value(state) + self.learn_rate * error * eligibility, epochs=1, verbose=0)
