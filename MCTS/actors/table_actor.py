from . import Actor


class TableActor(Actor):
    def __init__(self, learn_rate: float, trace_decay: float, epsilon: float, epsilon_decay: float, discount: float, action_space_size: int):
        super().__init__({}, learn_rate, trace_decay, epsilon, epsilon_decay, discount, action_space_size)

    def value(self, state: str, action: int):   # Retrieve single value.
        if state not in self.policy:
            self.insert(state)  # Insert new state dynamically.
        return self.policy[state][action]

    def insert(self, state: str):
        if state not in self.policy:
            self.policy[state] = [0] * self.action_space_size   # Changed to array.

    def update(self, state: str, action: int, error, eligibility: float = 1):
        self.policy[state][action] = self.value(state, action) + self.learn_rate * error * eligibility
        self.policy[state] = self.policy[state]     # normalize() didn't help, but broke something instead.

    def best_action(self, state: str, legal: list = None) -> int:
        if state not in self.policy:
            self.insert(state)  # Insert new state dynamically. Doesn't do this for random actions for random actions.
        # Get best from legal values if they exist, else best overall.
        if legal is None or len(legal) == 0:
            best = 0
            highest = self.policy[state][0]
            for i in range(1, self.action_space_size):
                value = self.policy[state][i]
                if value > highest:
                    highest = value
                    best = i

        else:
            best = legal[0]
            highest = self.policy[state][legal[0]]
            for l in legal:
                value = self.policy[state][l]
                if value > highest:
                    highest = value
                    best = l

        return best


def normalize(arr: list):  # Attempt at Normalizing the array so that the sum is equal to 1, and in the range [0, 1]
    min_val = min(arr)
    scale = max(arr) - min_val
    for i in range(0, len(arr)):
        if arr[i] != 0:
            arr[i] = (arr[i] - min_val) / scale
    return arr
