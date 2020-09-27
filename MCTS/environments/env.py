import abc
from games import Game


# Generic environment.
class Environment:
    __metaclass__ = abc.ABCMeta

    def __init__(self, game: Game, visualize=False):
        self.game = game
        self.visualize = visualize

    def is_game_over(self, state=None) -> (bool, any):
        return self.game.is_game_over(state)

    def get_data(self):
        return self.game.get_data()

    def is_action_legal(self, state, action: int) -> bool:
        return self.game.is_action_legal(self.translate_action(action), state)

    def get_legal_actions(self, state=None):
        return self.game.get_legal_actions(state)

    def encode(self, state=None):   # Environment should do the encoding. This is the default.
        return self.game.encode(state)

    def decode(self, state):
        pass

    @abc.abstractmethod
    def reset(self, new_map=None):
        pass

    @abc.abstractmethod
    def score(self, state=None) -> int:
        pass

    def render_game(self, update=None):
        self.game.render_game(update)

    @abc.abstractmethod
    def action(self, action: int, state=None, render=None):
        pass

    @abc.abstractmethod
    def actions_done(self) -> int:
        pass

    @abc.abstractmethod
    def translate_action(self, action, state=None):
        return action   # If game needs different format, such as action objects.

    def auto_drawing(self, draw: bool):
        self.visualize = draw

    def _check_state(self, state=None):
        return state if state is not None else self.get_data()

    def flip_linear(self, array):
        pass
