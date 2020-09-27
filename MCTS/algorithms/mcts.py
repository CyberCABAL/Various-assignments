from environments import SimulationEnvironment
from data_types import Tree, Node
import numpy as np
import random as r


# Default policy for the rollout, tree policy in the tree. Greedy argmax/min action, P1 is max, P2 is min.
class MCTS:
    def __init__(self, sim_env: SimulationEnvironment, default_policy=None,
                 rollouts: int = 1, simulation_steps: int = 10, eps=1.0, eps_decay=0.995):
        self.env = sim_env
        self.tree = Tree()
        self.tree.root.set_value([[0, 0, 1], 0, sim_env.get_data()])  # (wins, games, visited), exploration, node state.
        self.rollouts = rollouts
        self.simulation_steps = simulation_steps
        self.next_root = None

        # Added this for randomness control.
        self.eps = eps
        self.init_eps = eps
        self.eps_decay = eps_decay

        if default_policy is not None:
            self.default_policy = default_policy
        else:   # Default default policy. Random actions.
            def default_policy(s, state): return r.choice(s.env.get_legal_actions(state))
            self.default_policy = default_policy

    def get_distribution(self, node: Node):  # Is this right?
        arr = np.array([n.value[0][2] for n in node.nodes])  # Normalize.
        s = arr.sum()
        return node.value[2], arr / s

    def update_root(self):
        self.tree.set_root(self.tree.root.nodes[self.next_root])
        self.tree.root.super_node = None

    def decay_eps(self):
        self.eps *= self.eps_decay

    def reset_eps(self):
        self.eps = self.init_eps

    def get_root(self):
        return self.tree.get_root()

    def tree_reset(self):   # Clears tree structure.
        self.tree.set_root(Node(value=[[0, 0, 1], 0, self.env.get_data()]))

    def search(self, action_policy=None):
        i = 0
        while i < self.simulation_steps:
            node = self.select_next()   # Goes from root.

            over, node.value[2] = self.env.is_game_over(node.value[2])
            if not over:
                self.expand(node)
                for sn in node.nodes:
                    self.eval_leaf(sn)
                    self.backprop(sn)
            i += 1

        a = self.select_action(action_policy)  # Is it supposed to be max visit count? Lecture claims so.
        self.next_root = a
        return a

    def select_next(self):
        node = self.tree.root
        while not node.is_empty():
            new_node = node.nodes[self.greed_policy(node)]  # Tree policy.
            new_node.super_node = node
            node = new_node
        return node

    def expand(self, node: Node) -> list:
        state = node.value[2]
        actions = self.env.get_legal_actions(state)

        for a in actions:   # Expands all. Assumes order of legal actions returned will always be the same.
            new_state, s = self.env.action(a, state)
            new_node = Node(value=[[0, 0, 1], 0, new_state])
            new_node.super_node = node
            node.nodes.append(new_node)  # (wins, games), visited, exploration, node state.
        return node.nodes

    def eval_leaf(self, node: Node) -> (int, bool):
        end = False
        over, node.value[2] = self.env.is_game_over(node.value[2])
        if not over:
            results = self.simulate(node)
            # result_types = {}
            result = sum([1 if res == 0 else 0 for res in results])
        else:   # Case when end node was selected.
            result = self.rollouts * (1 if self.env.result(node.value[2]) == 0 else 0)   # Player 0 won this many times.
            end = True
        self.update_node_stats(node, (result, self.rollouts, 0))
        return result, end

    def simulate(self, from_node: Node):
        stats = []
        for _ in range(self.rollouts):
            state = from_node.value[2]
            over, from_node.value[2] = self.env.is_game_over(state)
            while not over:
                action = self.default_policy(self, state)
                new_state, s = self.env.action(action, state)

                over = self.env.is_game_over(new_state)[0]
                state = new_state

            stats.append(self.env.result(state))
        return stats

    def backprop(self, node: Node):
        val = node.value[0]
        while node.super_node is not None:
            self.update_exploration(node)    # This supposed to be here? Also, moved from below.
            node = node.super_node
            self.update_node_stats(node, (val[0], val[1], 1))

            # NOTE: N(s,a) for node n is the N(s) of the node after action a.

    def update_node_stats(self, node: Node, t: tuple):
        for i in range(len(node.value[0])):  # Q is not stored explicitly, as that is hard to update.
            node.value[0][i] += t[i]

    def select_action(self, policy=None):
        if policy is None:
            return self.greed_policy(self.tree.root)  # Supposed to be visit count? Seems strange, but lecture claims so.
        return policy(self.tree.root)

    def __get_qs(self, node: Node):  # Q is not stored explicitly, as that is hard to update.
        if self.env.get_turn(node.value[2]) == 0:   # These are the fractions of games that were won, for max.
            return [(n.value[0][0] / n.value[0][1]) + n.value[1] for n in node.nodes]
        else:   # These are the fractions of games that were lost, but negative for min.
            return [(-(n.value[0][1] - n.value[0][0]) / n.value[0][1]) - n.value[1] for n in node.nodes]

    def greed_policy(self, node: Node):  # Possible source of issue.
        values = self.__get_qs(node)
        turn = self.env.get_turn(node.value[2])
        # Greedy. NOTE: Min for other players.
        # Also note, using min is not strictly necessary.
        # Can use max for both in this implementation, if we drop using negative values.
        return np.argmax(values) if turn == 0 else np.argmin(values)  # Watch out, might be incorrect minmax!

    def update_exploration(self, node: Node):
        node.value[1] = self.exploration_bonus(node)

    def exploration_bonus(self, node: Node, c: int = 1):
        return c * np.sqrt(np.log(node.super_node.value[0][2]) / (1 + node.value[0][2]))
