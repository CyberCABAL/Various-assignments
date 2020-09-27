import abc


class Critic:
    __metaclass__ = abc.ABCMeta

    def __init__(self, association, learn_rate: float, trace_decay: float, discount: float = 0.9):
        self.association = association  # Values for each state.
        self.learn_rate = learn_rate
        self.discount = discount
        self.trace_decay = trace_decay
        self.episode = []

    @abc.abstractmethod
    def value(self, state):
        pass

    def save_state(self, state):
        self.episode.append(state)

    def error(self, r, state, next_state):
        return r + self.discount * self.value(next_state) - self.value(state)   # The general error formula.

    @abc.abstractmethod
    def update(self, state, error, eligibility: float = 1):
        pass

    def do_trace(self, error, init_trace: float = 1):
        trace = init_trace
        # for state in self.episode: # Whoops, wrong way!
        for i in range(len(self.episode) - 1, -1, -1):
            state = self.episode[i]
            self.update(state, error, trace)
            trace *= self.discount * self.trace_decay

    def clear_trace(self):
        self.episode = []   # Episode over.
