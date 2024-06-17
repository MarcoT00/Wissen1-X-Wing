from .. import Game
import time


class Agent:
    num_episodes = 10
    learn_rate = 1

    def evaluate_policy(policy):
        pass

    def improve_policy(policy):
        pass


if __name__ == "__main__":
    g = Game(map_id=1, start_pos_index=1)
    g.update_screen()
    time.sleep(25)

# policy = [{s0: a0}, {s1: a1}]
