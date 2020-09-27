from . import Critic
import random


class TableCritic(Critic):
    def __init__(self, learn_rate: float, trace_decay: float, discount: float = 0.9):
        super().__init__({}, learn_rate, trace_decay, discount)

    def value(self, state: str):
        if state not in self.association:
            self.insert(state)
        return self.association[state]

    def insert(self, state: str):
        if state not in self.association:
            self.association[state] = random.uniform(0, 0.01)

    def update(self, state: str, error, eligibility: float = 1):   # V(s) ← V(s) + αδe(s), removed next_state from here.
        self.association[state] = self.value(state) + self.learn_rate * error * eligibility
