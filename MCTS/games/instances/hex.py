from games import HexGame, TurnBasedGame
from games.player import ColourPlayer as Player
from games.rules import RuleSet, Rule
from games.maps import HexMap
from data_types import HexagonGrid
from games.actions import Place

# from copy import deepcopy # Too slow!
from _collections import deque
from numpy import full


class Hex(HexGame, TurnBasedGame):
    def __init__(self, players: list = None, start_player: int = 0, rule_set: RuleSet = None, map_size: int = 5, visualize=False):
        self.empty_colour = 0
        self.original_start = start_player
        self.size = map_size

        if rule_set is None:
            rule_set = RuleSet(rules=[Rule(self.cell_free, "Cell is empty.")])
        if players is None:
            players = [Player(0, colour=1), Player(1, colour=2)]

        super().__init__(players=players, rule_set=rule_set, game_map=self.standard_map(map_size), visualize=visualize)
        self.turn_index = start_player
        self.winner = None
        self.player_x_dir = 0   # Player 0 must cross in the "x" direction. Make it a param if it varies.
        self.moves = 0  # Also cells filled.

    def get_score(self):    # No score.
        pass

    def get_data(self):
        return self.turn_index, self.game_map.get_data(), -1

    def set_game(self, state: tuple = None, moves_increment: int = 0):  # Set game to this state.
        self.turn_index = state[0]
        self.game_map = HexMap(HexagonGrid(state[1], False))
        self.winner = self.won(state)
        if moves_increment != 0:    # So we can skip the searching if jumping one move ahead.
            self.moves += moves_increment
        else:
            self.moves = self.count_filled_cells(state)

    def count_filled_cells(self, state: tuple) -> int:
        s = self._check_state(state)[1]
        count = 0
        for row in s:
            for element in row:
                if element != self.empty_colour:
                    count += 1
        return count

    def set_turn(self, index: int, state: tuple = None):
        if 0 <= index < len(self.players):
            if state is None:
                self.turn_index = index
            else:
                return index, state[1], state[2]

    def get_turn(self, state: tuple = None) -> int:
        return self.turn_index if state is None else state[0]

    def is_game_over(self, state: tuple = None) -> (bool, tuple):  # Check that this is correct relative to whose turn it is.
        real_game = False
        if state is None:
            if self.winner is not None:
                return True
            real_game = True
            state = self.get_data()

        if state[2] != -1 and state[2]:
            return True, state

        if self.count_filled_cells(state) < len(state[1]) * 2 - 1:
            return False, state  # For two players, victory can happen no sooner than at K * 2 - 1 moves.

        map_inst = HexMap(HexagonGrid(state[1], False))
        for p in self.players:
            if self.exists_win_path(state, map_inst, p):
                if real_game:
                    self.winner = p
                return True, state
        return False, state  # Ties are impossible.

    def won(self, state=None):  # Test who won. Should implicitly the one whose turn it is.
        if state is None:
            return self.winner
        else:
            if self.count_filled_cells(state) < len(state[1]) * 2 - 1:
                return None  # For two players, victory can happen no sooner than at K * 2 - 1 moves.

            map_inst = HexMap(HexagonGrid(state[1], False))
            for p in self.players:
                if self.exists_win_path(state, map_inst, p):
                    return p

    def exists_win_path(self, state: tuple, map_inst: HexMap, player: Player) -> bool:
        x_dir = player.player_num == self.player_x_dir
        map_state = state[1]

        k = len(map_state)
        seen = []
        for i in range(k):  # Assume it is N*N matrix. Seen is to not loop paths.
            seen.append([0] * k)

        if x_dir:
            range_i = range(k)
            range_j = [0]  # We always start the search at the low-index side. Doesn't really matter.
        else:
            range_i = [0]
            range_j = range(k)
        # Start search just 0 for either i or j! That way we will still know for sure if there is a path.

        colour = player.colour
        edge = k - 1
        queue = deque()

        for i in range_i:
            for j in range_j:   # These two are actually linear! Only loops k times here.
                if not seen[i][j] and map_state[i][j] == colour:
                    self.__queue_filtered_neighbours((j, i), map_state, seen, map_inst, colour, queue)
                    while queue:  # Complexity depends on state, theoretical worst case goes through half of nodes.
                        p = queue.pop()  # Depth first! Solutions are always found at the other end.

                        if not seen[p[1]][p[0]] and map_state[p[1]][p[0]] == colour:
                            if x_dir:  # By using neighbour based search, we got over to the other side.
                                if p[0] == edge:
                                    return True
                            else:
                                if p[1] == edge:
                                    return True

                            self.__queue_filtered_neighbours((p[0], p[1]), map_state, seen, map_inst, colour, queue)

                        seen[p[1]][p[0]] = True
                seen[i][j] = True
        return False  # Total complexity should be O(K*K/2) and Omega(K). We pass through all the nodes ONLY once, and only the player colour.

    def __queue_filtered_neighbours(self, p, m_state, seen, map_inst: HexMap, colour, queue):
        for n_p in map_inst.get_neighbour_points((p[0], p[1])):
            if not seen[n_p[1]][n_p[0]] and m_state[n_p[1]][n_p[0]] == colour:
                queue.append(n_p)

    def __filter(self, x, m_state, seen, colour) -> bool:
        return not seen[x[1]][x[0]] and m_state[x[1]][x[0]] == colour

    def encode(self, state: tuple = None):  # Define state as (player id, map array)
        return self._check_state(state)

    def is_action_legal(self, action: Place, state: tuple = None, debug_print: bool = False) -> bool:
        return self.__legal(action, state)

    def __legal(self, action: Place, state: tuple = None) -> bool:
        state = self._check_state(state)
        return state[1][action.point[1]][action.point[0]] == self.empty_colour   # Need for speed.

    def get_potentially_legal_actions(self, player: Player = None) -> list:  # Search for potential actions, independent of board state.
        l = []
        [l.extend([(j, i) for j in range(self.size)]) for i in range(self.size)]
        return l

    def get_legal_actions(self, state: tuple = None, rule_set: RuleSet = None, player: Player = None) -> list:
        state = self._check_state(state)
        # rule_set = rule_set if rule_set is not None else self.rules
        legal_moves = []
        [legal_moves.extend([(j, i) for j in range(self.size) if self.__legal(Place((j, i)), state)])
         for i in range(self.size)]
        return legal_moves

    def do_action(self, action: Place, debug_print: bool = False) -> (bool, any):
        success, new_state = self.action_on_state(self.get_data(), action, debug_print)
        if success:
            self.game_map.set_map(HexagonGrid(new_state[1], False))
            self.moves += 1
            self.turn_up()
        return success, new_state

    def action_on_state(self, state: tuple, action: Place, debug_print: bool = False) -> (bool, any):
        if self.__legal(action, state):
            temp = HexMap(HexagonGrid(_copy_state(state), triangle=False))
            temp.set(action.point, self.players[state[0]].colour)

            return True, self.next_turn((state[0], temp.get_data(), -1))
        return False, state

    def cell_free(self, action: Place, map_instance: HexMap) -> bool:  # The only rule needed to define the game.
        temp = map_instance if map_instance is not None else self.game_map
        return temp.get(action.point) == self.empty_colour

    def standard_map(self, k: int) -> HexMap:
        return HexMap(HexagonGrid(full((k, k), self.empty_colour), triangle=False))

    def next_turn(self, state: tuple = None):
        if state is None:
            if not self.is_game_over()[0]:
                self.turn_up()
                return self.get_data()
        else:
            over, state = self.is_game_over(state)
            if not over:
                return (state[0] + 1) % len(self.players), state[1], over
        return state  # Nothing changed, may cause issues.


def _copy_state(state: tuple) -> list:
    return [[e for e in row] for row in state[1]]
