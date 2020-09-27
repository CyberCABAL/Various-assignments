from . import Actor


class RandomActor(Actor):
    def __init__(self, action_space_size: int):
        super().__init__(0, 0, 0, 0, 0, 0, action_space_size=action_space_size)

    def update(self, state, action, error, eligibility: float = 1):
        pass

    def get_action(self, state=None, legal: list = None) -> int:
        return self.random_action(legal)

    def best_action(self, state, legal: list = None) -> int:
        return self.random_action(legal)
