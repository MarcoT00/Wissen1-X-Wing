from .. import Game
import time


class Agent:

    def run(game, policy):
        pass

    def evaluate_policy(self, policy, game, num_episodes):
        policy_cost = 0
        learn_rate = 0
        episode_count = 1
        while episode_count <= num_episodes:
            learn_rate = 1 / episode_count
            # run game with given policy
            self.run(game, policy)

            policy_cost = policy_cost + learn_rate * (game.episode_cost - policy_cost)

            episode_count += 1
        return policy_cost

    def improve_policy(policy):
        pass


if __name__ == "__main__":
    game_map1_start1 = Game(map_id=1, start_pos_index=1)

    g.update_screen()
    time.sleep(25)

# policy = [{s0: a0}, {s1: a1}]
