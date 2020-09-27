from environments import SimulationEnvironment
from data_types import Node
from . import MCTS


class CriticMCTS(MCTS):
    def __init__(self, sim_env: SimulationEnvironment, default_policy=None, rollouts=1,
                 simulation_steps: int = 10, rollout_chance: float = 1, rollout_decay: float = 0.9):
        super().__init__(sim_env, default_policy, rollouts, simulation_steps)
        self.rollout_chance = rollout_chance
        self.rollout_decay = rollout_decay
        if default_policy is not None:
            self.default_policy = default_policy  # Make this be neural network.

    def decay_rollout(self):
        self.rollout_chance *= self.rollout_decay

    def eval_leaf(self, node: Node) -> (int, bool):
        end = False
        if not self.env.is_game_over(node.value[2])[0]:
            results = self.simulate(node)
            result = sum([1 if res == 0 else 0 for res in results])
        else:   # Case when end node was selected.
            result = self.rollouts * (1 if self.env.result(node.value[2]) == 0 else -1)   # Player 0 won this many times.
            end = True
        self.update_node_stats(node, (result, self.rollouts, 0))
        return result, end
