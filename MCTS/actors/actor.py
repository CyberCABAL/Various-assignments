import random as r
import abc


class Actor:
    __metaclass__ = abc.ABCMeta

    def __init__(self, policy, learn_rate: float, trace_decay: float, epsilon: float, epsilon_decay: float, discount: float, action_space_size: int):
        self.policy = policy    # state action pairs
        self.learn_rate = learn_rate
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.episode = []  # For eligibility.
        self.discount = discount
        self.trace_decay = trace_decay
        self.action_space_size = action_space_size  # Assumes constant action space size.

    @abc.abstractmethod
    def update(self, state, action, error, eligibility: float = 1):
        pass

    def insert(self, state):
        pass

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def decay_epsilon(self):
        self.epsilon = self.epsilon * self.epsilon_decay

    def save_state(self, state, action: int):
        self.episode.append((state, action))    # For eligibility traces.

    def get_action(self, state=None, legal: list = None) -> int:
        if state is None:
            return self.random_action(legal)
        rand = r.uniform(0, 1)
        if rand > self.epsilon:
            return self.best_action(state, legal)
        return self.random_action(legal)

    def random_action(self, legal: list = None) -> int:    # Chooses randomly, but only from legal actions.
        return r.randint(0, self.action_space_size - 1) if legal is None or len(legal) < 1 else r.choice(legal)

    @abc.abstractmethod
    def best_action(self, state, legal: list = None) -> int:
        return self.random_action(legal)

    def clear_trace(self):
        self.episode = []   # End of episode.

    def do_trace(self, error, init_trace: float = 1):
        trace = init_trace
        # for (state, action) in self.episode:  # Whoops, wrong way!
        for i in range(len(self.episode) - 1, -1, -1):
            state, action = self.episode[i]
            self.update(state, action, error, trace)    # The updates are defined in subclasses.
            trace *= self.discount * self.trace_decay
