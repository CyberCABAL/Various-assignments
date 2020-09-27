from environments import SimulationEnvironment
from algorithms import MCTS
import random as r
from collections import deque

import numpy as np
import datetime


class Simulation:
    def __init__(self, env: SimulationEnvironment, mcts: MCTS,
                 memory_size: int = 1000, save_interval=100, verbose: bool = False):
        self.env = env
        self.mcts = mcts
        self.verbose = verbose
        self.save_interval = save_interval
        self.memory = deque(maxlen=memory_size)  # A data structure that keeps a certain amount of elements. At limit, oldest are removed.

    def sim_run(self, G: int, P, model, init_map=None, verbose: bool = None, print_progress=True,
                learning_batches: int = 1, ep_per_game: int = 3, train=True, save_path="models"):  # G = episodes, P = starting player.
        if verbose is None:
            verbose = self.verbose
        re_player = P == "r"    # r for random.
        s_player = P
        p1_wins = 0
        p1_first = G if P == 0 else 0
        self.env.auto_drawing(verbose)

        names = []

        if verbose:
            print("Initial game state:", init_map)
        for g in range(G):
            # Do the modulo model saving thing.
            if train and g % self.save_interval == 0:
                name = save_path + "/Model_" + str(g) + ".h5"
                model.save(name)  # Windows OS error!
                names.append(name)

            if re_player:   # Select start player.
                s_player = r.randint(0, 1)
                if s_player == 0:
                    p1_first += 1

            if print_progress and g % 10 == 0:
                print("\nGame", g)

            # Play the game
            last_state, random_turn = self.game(s_player, verbose, model, train)

            if not train and self.env.score(last_state) != random_turn or train and self.env.score(last_state) == 0:
                p1_wins += 1
                if verbose:
                    print("Player 0 won.")
            elif verbose:
                print("Player 1 won.")

            # Train net on random minibatch from memory.
            if train:
                self.train_model(model, learning_batches, ep_per_game, verbose=print_progress)

            self.reset_game(None, init_map)
            self.mcts.decay_eps()

        print("Player 0 won", p1_wins, "out of", G, "games, and was playing first", p1_first, "times.")
        f = open("game_log.txt", "a+")
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        f.write(" Player 0 won " + str(p1_wins) + " out of " + str(G) + " games, and was playing first " + str(p1_first) + " times.\n")
        f.close()
        self.mcts.reset_eps()
        return names

    def game(self, start_player, verbose, model, train=True):
        self.env.set_turn(index=start_player)
        self.mcts.tree_reset()
        new_state = None
        turn = start_player
        random_turn = r.randint(0, 1)
        while not self.env.is_game_over()[0]:
            if train:
                action = self.mcts.search()  # Is based on array1d D. To change selection, pass different policy function.
                state, dist = self.mcts.get_distribution(self.mcts.get_root())

                self.memory.append((state, dist))  # Save to data structure. (State, D).

                new_state, success = self.env.action(self.env.get_legal_actions(state)[action], render=verbose)
                self.mcts.update_root()
            else:
                state = self.env.get_data()
                if turn == random_turn:  # Random player plays.
                    new_state, success = self.env.action(r.choice(self.env.get_legal_actions(state)), render=verbose)
                else:
                    legal = self.env.get_legal_actions(state)
                    dist = model.predict_on_batch(np.array([self.env.encode()[1]]))[0]
                    dist = filter_legal(self.env, state, dist)
                    action = np.argmax(dist)

                    new_state, success = self.env.action(legal[action], render=verbose)

            turn = (turn + 1) % 2
        return new_state, random_turn

    def reset_game(self, s_player, init_map):
        self.env.reset((s_player, init_map))  # Reset game.
        self.mcts.tree_reset()   # Must be after env reset.

    def train_model(self, model, batches, ep_per_game, verbose=True):
        len_memory = len(self.memory)
        sample = r.sample(range(0, len_memory), min(len_memory, batches))
        x = []
        y = []
        for s in sample:
            state = self.memory[s][0]
            dist = self.env.adjust_to_space(state, self.memory[s][1])
            x.append(self.env.encode(state)[1])  # Flip in encode now.
            y.append(dist)

        model.fit(x, y, epochs=ep_per_game, verbose=verbose)


def filter_legal(env, state, dist):
    d = np.array([dist[i] for i in range(len(dist)) if env.is_action_legal(state, i)])
    s = d.sum()
    return d / s
