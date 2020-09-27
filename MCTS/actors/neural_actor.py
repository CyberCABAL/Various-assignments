from numpy import argmax


class NeuralActor:
    def __init__(self, model):
        self.model = model

    def train(self, x, y, ep, v=True):
        self.model.fit(x, y, epochs=ep, verbose=v)

    def predict(self, state) -> int:
        return self.model.predict_on_batch(state)

    def filter(self, legal_func, state, data):
        return [data[i] for i in range(len(data)) if legal_func(state, i)]

    def policy(self, dist):
        return argmax(dist)
