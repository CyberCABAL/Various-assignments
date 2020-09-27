import abc
from games import Game
from . import Environment
import random as r


# Generic sim environment.
class SimulationEnvironment(Environment):
    __metaclass__ = abc.ABCMeta

    def __init__(self, game: Game, visualize=False):
        super().__init__(game, visualize)
        self.previous_action = None  # In case one wants to reach it after execution.
        self.action_space = game.get_potentially_legal_actions()

    def action(self, action, state=None, render=None):
        render = render if render is not None else self.visualize
        a = self.translate_action(action, state)
        success, new_state = self.game.action_on_state(state, a) if state is not None else self.game.do_action(a)
        if success:
            if render:
                print(a)
                self.render_game()
            self.previous_action = a
        return new_state, success

    def get_turn(self, state=None):
        return state[1] if state is not None else None

    def set_turn(self, state=None, index: int = 0):
        if state is not None:
            state[1] = index
        return state

    def get_action_space(self) -> list:
        return self.action_space

    def result(self, state):
        return self.game.won(state)

    def simulate_random(self, from_state, sim_amount: int = 1) -> list:
        stats = []
        for _ in range(sim_amount):
            state = from_state
            over = self.is_game_over(state)[0]
            while not over:
                action = r.choice(self.get_legal_actions(state))
                _, new_state = self.action(action, state)

                over = self.is_game_over(new_state)[0]
                state = new_state

            stats.append(self.result(state))
        return stats

    @abc.abstractmethod
    def translate_action(self, action, state=None):
        return action

    def adjust_to_space(self, state, array1d: list) -> list:
        adjusted = []
        i = 0
        for p in range(len(self.action_space)):
            if self.is_action_legal(state, p):
                adjusted.append(array1d[i])
                i += 1
            else:
                adjusted.append(0)
        return adjusted
