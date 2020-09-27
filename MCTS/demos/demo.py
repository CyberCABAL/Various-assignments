from environments import HexEnvironment
from algorithms import MCTS
from demos.sim import Simulation, filter_legal
from neural_networks import get_dense_model
from tensorflow.keras.optimizers import Adam

import numpy as np
import random as r


def main():
    verbose = False
    render_min_delay = 0.1

    # Amount of runs.
    episodes = 11  # G
    rollouts = 1
    simulation_count = 10

    save_models = 3  # Including first!
    save_interval = int(episodes / (save_models - 1))
    tests = 1000

    # Board size
    k = 5

    # Relevant parameters.
    start_player = "r"

    # Environment.
    env = HexEnvironment(k, render_delay=render_min_delay)

    # NN model.
    nn = [1 + k * k,
          k * k,
          len(env.action_space)]    # Simple example
    act = ["relu", "relu", "softmax"]   # Few layers
    model = get_dense_model(nn, loss="categorical_crossentropy", optimizer=Adam, activation=act, learn_rate=0.0005)

    learning_batches = 128

    # MCTS.
    mc = MCTS(sim_env=env, default_policy=policy(model), rollouts=rollouts, simulation_steps=simulation_count, eps_decay=0.9975)

    # Buffer size.
    max_memory_size = 10000

    # Simulations
    sim = Simulation(env, mc, max_memory_size, save_interval, verbose)
    names = sim.sim_run(G=episodes, P=start_player, model=model, init_map=k, verbose=verbose,
                        learning_batches=learning_batches, ep_per_game=5, train=True, save_path="models")

    sim.sim_run(G=tests, P=start_player, model=model, init_map=k, verbose=verbose, train=False)

    print(names)


def policy(model):  # Produce a policy given a model.
    def default_policy(s, state):
        legal = s.env.get_legal_actions(state)
        if r.uniform(0, 1) < s.eps:
            return r.choice(legal)
        dist = model.predict_on_batch(np.array([s.env.encode(state)[1]]))[0]
        dist = filter_legal(s.env, state, dist)
        a_id = np.argmax(dist)  # Greedy

        return legal[a_id]
    return default_policy


if __name__ == "__main__":
    main()
