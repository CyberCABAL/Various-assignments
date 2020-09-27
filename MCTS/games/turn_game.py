from .rules import RuleSet
from .player import Player
from .maps import GameMap
from .actions import Action
from . import Game
import abc


# Generic two player game game.
class TurnBasedGame(Game):
    __metaclass__ = abc.ABCMeta

    def __init__(self, players: list = None, start_player: int = 0, rule_set: RuleSet = None, game_map: GameMap = None, visualize=False):
        super().__init__(players=players, rule_set=rule_set, game_map=game_map, visualize=visualize)
        self.turn_index = start_player

    @abc.abstractmethod
    def render_game(self, state):
        pass

    def turn_up(self):
        self.turn_index += 1
        if self.turn_index == len(self.players):
            self.turn_index = 0

    def turn_down(self):
        self.turn_index -= 1
        if self.turn_index == -1:
            self.turn_index = len(self.players) - 1

    def set_turn(self, index: int, state=None):
        if 0 <= index < len(self.players):
            self.turn_index = index

    def get_turn(self, state=None) -> int:
        return self.turn_index

    def won(self, state=None) -> Player:  # Default to the player whose turn it is in the end wins.
        return self.players[self.get_turn(state)] if self.is_game_over()[0] else None

    def do_action(self, action: Action, debug_print: bool = False) -> (bool, any):
        success, new_state = self.action_on_state(self.get_data(), action, debug_print)
        if success:
            self.game_map.set_map(new_state)
            self.turn_up()
        return success, new_state

    def next_turn(self, state: tuple = None):
        if state is None and not self.is_game_over()[0]:
            return self.turn_up()
        if state is not None and not self.is_game_over(state)[0]:
            return state[0], (state[1] + 1) % len(self.players)
        return state    # Nothing changed, may cause issues.
