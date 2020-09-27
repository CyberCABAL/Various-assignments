from critics import *
from actors import *
from environments import *
import matplotlib.pyplot as plot
import time


# The general idea of the actor-critic model.
class ActorCriticModel:
    def __init__(self, environment: RLEnvironment, critic: Critic, actor: Actor):
        self.env = environment
        self.critic = critic
        self.actor = actor
        self.errors = []
        self.progress = []

    def train(self, episodes: int, verbose: bool = True, print_interval: int = 50, win_limit: int = 1000):
        self.errors = []
        self.progress = []
        wins = 0
        ep = 0
        while ep < episodes and wins < win_limit:
            state = self.env.encode()
            a = self.get_action(state)
            game_over = False
            sum_r = 0

            while not game_over:    # Game loop.
                r = self.env.action(a)
                next_state = self.env.encode()

                self.learn(state, next_state, a, r)

                state = next_state
                a = self.get_action(state)

                game_over = self.env.is_game_over()[0]
                sum_r += r

            self.clear_trace()
            if self.env.score() == 1:
                wins += 1
            if verbose and ep % print_interval == 0:
                print("Episode:", ep)
                print("Total r:", sum_r, "Remaining:", self.env.score(), "Moves:", self.env.actions_done(),
                      "Wins:", wins, "Eps:", self.actor.epsilon)
            self.progress.append(self.env.score())

            self.actor.decay_epsilon()
            self.env.reset()
            ep += 1
        # self.plot_loss()
        self.plot_progress()

    def test(self, episodes: int, action_interval: float = 0.5, verbose: bool = True):
        epsilon = self.actor.epsilon
        drawing = self.env.visualize
        self.actor.set_epsilon(0)   # Epsilon = 0 for tests.
        self.env.auto_drawing(True)
        wins = 0

        for ep in range(episodes):
            if verbose:
                print("Episode:", ep)
            state = self.env.encode()
            a = self.get_action(state)
            game_over = False
            sum_r = 0

            while not game_over:
                if verbose:
                    print("Options:", self.env.get_legal_actions(), "Chosen:", a)
                r = self.env.action(a)
                next_state = self.env.encode()

                state = next_state

                game_over = self.env.is_game_over()[0]
                a = self.get_action(state)
                sum_r += r
                time.sleep(action_interval)

            if self.env.score() == 1:
                wins += 1
            if verbose:
                print("Victory:", self.env.score() == 1)
                print("Total r:", sum_r, "Remaining:", self.env.score(), "Moves:", self.env.actions_done(), "Wins:", wins)
            self.env.reset()

        self.actor.set_epsilon(epsilon)  # Reset the original values.
        self.env.auto_drawing(drawing)

    def save_state(self, state, action: int):
        self.actor.save_state(state, action)
        self.critic.save_state(state)

    def do_trace(self, error):
        self.critic.do_trace(error)  # Set e to 1 included here.
        self.actor.do_trace(error)

    def clear_trace(self):
        self.critic.clear_trace()
        self.actor.clear_trace()

    def learn(self, state, next_state, action: int, reward: int):
        self.save_state(state, action)

        err = self.critic.error(reward, state, next_state)  # Was wrong, don't find value here.
        self.do_trace(err)
        self.errors.append(err)

    def get_action(self, state):
        return self.actor.get_action(state, self.env.get_legal_actions())

    def plot_loss(self):
        plot_learning(self.errors, "Actions", "Error")

    def plot_progress(self):
        plot_learning(self.progress, "Episodes", "Progress")


def plot_learning(data, x, y):
    plot.plot(data)
    plot.xlabel(x)
    plot.ylabel(y)
    plot.grid(True)
    plot.show()
