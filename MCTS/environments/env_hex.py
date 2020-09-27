from games import Hex
from . import RLEnvironment, SimulationEnvironment
from games.actions import Place
from .hex_rendering import create_render

from networkx import draw
from matplotlib.pyplot import pause, clf

import numpy as np


# Hex environment.
class HexEnvironment(RLEnvironment, SimulationEnvironment):
    def __init__(self, board_size: int, players: list = None, start_player: int = 0, empty_colour: str = "c",
                 visualize=False, render_delay=0.01):
        game = Hex(start_player=start_player, map_size=board_size, visualize=visualize)

        super().__init__(game=game, visualize=visualize)
        self.board_size = board_size
        self.start_player = start_player
        self.render_delay = render_delay

        if players is not None and len(players) == 2:
            self.colour_map = {game.empty_colour: empty_colour,
                               self.game.players[0].colour: players[0].colour,
                               self.game.players[1].colour: players[1].colour}
        else:
            self.colour_map = {game.empty_colour: empty_colour,
                               game.players[0].colour: "b",
                               game.players[1].colour: "r"}

        self.__nxgraph = None
        self.__graph_pos = None

    def reward(self, state: tuple, action) -> int:
        pass

    def get_turn(self, state: tuple = None):
        return self._check_state(state)[0]

    def set_turn(self, state: tuple = None, index: int = 0):
        return self.game.set_turn(index)

    def action(self, action, state: tuple = None, render=None):
        real = state is None
        render = render if render is not None else self.visualize

        a = self.translate_action(action, state)
        success, new_state = self.game.action_on_state(state, a) if not real else self.game.do_action(a)
        if success:
            if render and real:  # Don't render simulations.
                print(a)
                self.render_game(action)
            self.previous_action = a
        return new_state, success

    def __update_render(self, state: tuple):  # Updated render based on state.
        colours = []
        s = state[1]
        for i in range(len(s)):
            for j in range(len(s[i])):
                colours.append(self.colour_map[s[i][j]])
        clf()  # Clear before re-drawing.
        draw(self.__nxgraph, node_color=colours, pos=self.__graph_pos)

    def render_game(self, action: int = -1, state: tuple = None):
        s = self._check_state(state)
        if self.__nxgraph is None:
            self.__nxgraph, self.__graph_pos = create_render(s[1])
        if action > -1:
            self.__update_render(s)
        pause(self.render_delay)  # Hacky way to make the window not freeze execution.

    def encode(self, state: tuple = None) -> tuple:  # 1D encoding. 2D might also be desirable.
        s = self._check_state(state)
        encoded_game = [s[0]]
        for row in s[1]:
            for e in row:
                value = 0  # Player is fixed, Player 0 is always going in X. If assumption doesn't match, mirror board.
                if e == self.game.players[0].colour:
                    value = 1
                elif e == self.game.players[1].colour:
                    value = 2
                encoded_game.append(value)
        return s[0], encoded_game, s[2]  # Could also be a string.

    def decode(self, state) -> tuple:
        k = self.board_size
        decoded_game = []
        for i in range(k):
            row = []
            for j in range(k):
                e = state[1][i * k + j]
                value = self.game.empty_colour  # Player is fixed, Player 0 is always going in X. If assumption doesn't match, mirror board.
                if e == 1:
                    value = self.game.players[0].colour
                elif e == 2:
                    value = self.game.players[1].colour
                row.append(value)
            decoded_game.append(row)
        return state[0], decoded_game, state[2]

    def mirror(self, state: tuple = None):
        state = self._check_state(state)
        m_state = state[1]
        mirror_state = np.zeros((self.board_size, self.board_size))
        for i in range(self.board_size):
            for j in range(self.board_size):
                mirror_state[j][i] = m_state[i][j]
        return state[0], mirror_state, state[2]

    def flip_sides(self, state: tuple = None):  # Swap the colours of the game units.
        state = self._check_state(state)
        m_state = state[1]
        flipped_state = np.zeros((self.board_size, self.board_size))
        p0 = self.game.players[0].colour
        p1 = self.game.players[1].colour
        for i in range(self.board_size):
            for j in range(self.board_size):
                if m_state[i][j] == p0:
                    flipped_state[i][j] = p1
                elif m_state[i][j] == p1:
                    flipped_state[i][j] = p0
        return (state[0] + 1) % 2, flipped_state, state[2]

    def flip_players(self, state):  # Mirror and flip the board.
        return self.flip_sides(self.mirror(state))

    def flip_action(self, action):  # Flip action into the mirror reality.
        a = self.action_space[action]
        return self.action_space.index((a[1], a[0]))

    def flip_linear(self, array):   # Mirror a 1d array using k.
        new_arr = []
        k = self.board_size
        for i in range(k):
            for j in range(k):
                new_arr.append(array[i + j * k])
        return new_arr

    def score(self, state: tuple = None) -> int:    # Result.
        p = self.game.won(state)
        return p.player_num if p is not None else None

    def translate_action(self, action, state: tuple = None) -> Place:  # Turn action index into an action object.
        state = self._check_state(state)
        return Place(self.action_space[action], self.game.players[state[0]])

    def actions_done(self) -> int:
        return self.game.moves

    def result(self, state: tuple):
        return super().result(state).player_num

    def reset(self, new_map=(None, 0)):  # Complete reset of the game.
        self.game = Hex(
            self.game.players, new_map[0] if new_map[0] is not None else self.start_player,
            map_size=new_map[1] if new_map[1] > 0 else self.board_size,
            visualize=self.game.visualize
        )
