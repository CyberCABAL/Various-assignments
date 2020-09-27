import abc
from games import Game
from . import Environment


# Generic environment.
class RLEnvironment(Environment):
    __metaclass__ = abc.ABCMeta

    def __init__(self, game: Game, visualize=False):
        super().__init__(game, visualize)
        self.action_space = game.get_potentially_legal_actions()

    @abc.abstractmethod
    def reward(self, state, action) -> int:
        pass

    def get_action_space(self) -> list:
        return self.action_space

    def get_legal_actions(self, state=None):
        return [
            i for i in range(0, len(self.action_space))
            if self.game.is_action_legal(self.translate_action(i, state), state)
        ]

    def action(self, action: int, state=None, render=None) -> int:
        success, _ = self.game.do_action(self.translate_action(action))
        if self.visualize and success:
            self.render_game(action)
        return self.reward(self.get_data(), action)     # What is the reward for having done this action?
