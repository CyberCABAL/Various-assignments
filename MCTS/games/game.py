from .rules import RuleSet
from .player import Player
from .maps import GameMap
from .actions import Action
import abc


# Generic game.
class Game:
    __metaclass__ = abc.ABCMeta

    def __init__(self, players: list = None, rule_set: RuleSet = None, game_map: GameMap = None, visualize=False):
        self.players = players
        self.rules = rule_set
        self.game_map = game_map
        self.visualize = visualize
        self.relaxed_rules = RuleSet(rules=[])  # Empty, everything is allowed.

    @abc.abstractmethod
    def render_game(self, state):
        pass

    @abc.abstractmethod
    def encode(self, state=None):
        pass

    def set_game(self, state=None):
        pass

    @abc.abstractmethod
    def won(self, state=None):
        pass

    def get_data(self):
        return self.game_map.get_data() if self.game_map is not None else None

    @abc.abstractmethod
    def is_game_over(self, state=None) -> (bool, any):
        pass

    @abc.abstractmethod
    def get_legal_actions(self, state=None, rule_set: RuleSet = None, player: Player = None) -> list:
        pass

    def get_potentially_legal_actions(self, player: Player = None) -> list:  # Search for potential actions, independent of board state.
        return self.get_legal_actions(self.get_data(), self.relaxed_rules, player)

    @abc.abstractmethod
    def do_action(self, action: Action, debug_print: bool = False) -> (bool, any):
        pass

    @abc.abstractmethod
    def action_on_state(self, state, action: Action, debug_print: bool = False) -> (bool, any):
        pass

    @abc.abstractmethod
    def is_action_legal(self, action: Action, state=None, debug_print: bool = False) -> bool:
        pass

    def get_legal_actions_self(self):
        return self.get_legal_actions(self.get_data())

    def allow_auto_drawing(self, draw: bool):
        self.visualize = draw

    def _check_state(self, state=None):
        return state if state is not None else self.get_data()
