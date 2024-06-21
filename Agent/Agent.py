from .. import Game
import time
import numpy as np
import random


class Agent:
    def __int__(self, game):
        self.game = game
    def monte_carlo_rollout(self, policy, G, gamma=0.99, n=10):
        returns = []
        for _ in range(n):
            self.game.episode_reset()
            state = self.game.get_state()
            episode = []
            while True:
                action = policy[f"{state}"]
                '''
                next_state: x_pos, y_pos, velocity
                reward: either 1 or 5 if collision
                done: boolean
                '''
                next_state, reward, done = self.game.change_state(action)
                episode.append((state, action, reward))
                if done:
                    break
                state = next_state
            for state, action, reward in reversed(episode):
                G = reward + gamma * G
                returns.append((state, action, G))

                return returns

    def init_policy(self):
        #state: x,y, (x_speed, y_speed)
        # velocity x: [-4,+4] y:[-4,+4]
        #x,y needs to contain S,X,Z
        #default action is always accelerate up
        policy = {}
        self.X_SIZE = len(self.game.MAP[0])
        self.Y_SIZE = len(self.game.MAP)
        for row in range(self.Y_SIZE):
            for col in range(self.X_SIZE):
                if self.game.MAP[row][col] in ["S","X", "Z"]:
                    for x_speed in range(-4,5):
                        for y_speed in range(-4,5):
                            state = {"x": col, "y": row, "velocity": {"x": x_speed, "y": y_speed}}
                            action = self.game.ACTIONS[4]
                            policy[f"{state}"] = action
        return policy
    def policy_iteration_mc(self, gamma=0.99, theta=0.0001, n_rollouts=10):
        value_function = {}
        possible_actions = self.game.get_selectable_actions()

        # Initialize random policy
        policy = self.init_policy()
        G=0
        while True:
            # Policy Evaluation
            delta = 0
            returns = self.monte_carlo_rollout(policy, G, gamma, n_rollouts)
            for state, action, G in returns:
                if state not in value_function:
                    value_function[f"{state}"] = 0
                old_value = value_function[f"{state}"]
                value_function[f"{state}"] += (G - value_function[f"{state}"])
                delta = max(delta, abs(G - old_value))

            if delta < theta:
                break

            # Policy Improvement
            policy_stable = True
            for row in range(self.Y_SIZE):
                for col in range(self.X_SIZE):
                    if self.game.MAP[row][col] in ["S", "X", "Z"]:
                        for x_speed in range(-4, 5):
                            for y_speed in range(-4, 5):
                                state = {"x": col, "y": row, "velocity": {"x": x_speed, "y": y_speed}}
                                old_action = policy[f"{state}"]
                                action_values = {}
                                for action in possible_actions:
                                    self.game.pos = {"x": row, "y": col}
                                    self.game.velocity = {"x": x_speed, "y": y_speed}
                                    next_state, reward, _ = self.game.change_state(action)
                                    if next_state not in value_function:
                                        value_function[f"{next_state}"] = 0
                                    action_values[action] = reward + gamma * value_function[f"{next_state}"]
                                best_action = max(action_values, key=action_values.get)
                                policy[f"{state}"] = best_action
                                if old_action != best_action:
                                    policy_stable = False
            if policy_stable:
                break

        return policy, value_function















def run(game, policy):
    while game.episode[-2][1] != "Z":
        #do sth
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
    agent = Agent(game_map1_start1)

# policy = [{s0: a0}, {s1: a1}]
