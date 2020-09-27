from .game import Game
from .rules import RuleSet
from .maps import HexMap
from data_types import HexagonGrid
from .actions import Action
import abc


# A game taking place on some hex grid.
class HexGame(Game):
    __metaclass__ = abc.ABCMeta

    def __init__(self, players: list = None, rule_set: RuleSet = None, game_map: HexMap = None, visualize=False):
        super().__init__(players=players, rule_set=rule_set, game_map=game_map, visualize=visualize)

    @abc.abstractmethod
    def get_score(self):
        pass

    def is_action_legal(self, action: Action, state=None, debug_print: bool = False) -> bool:
        state = self._check_state(state)
        return self.rules.is_valid(action, HexMap(HexagonGrid(state, triangle=self.game_map.get_map().triangle)), debug_print)

    def render_game(self, state: list = None):
        print(self.game_map.display_format())
