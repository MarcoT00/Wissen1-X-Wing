from .. import Game
import time
import numpy as np
import random


class Agent:
    def __init__(self):
        self.game = None

    def monte_carlo_rollout_for_one_start(self, policy):
        episode_cost = 0
        #episode = []
        while not self.game.is_done():
            action = policy[f"{state}"]
            cost = self.game.change_state(action)
            next_state = self.game.get_state()
            episode_cost += cost
            #episode.append((state, action, cost))
            state = next_state
        return episode_cost


    def init_policy_evaluation(self):
        #state: x,y, (x_speed, y_speed)
        # velocity x: [-4,+4] y:[-4,+4]
        #x,y needs to contain S,X,Z
        #default action is always accelerate up
        policy = {}
        value_function = {}
        self.X_SIZE = len(self.game.MAP[0])
        self.Y_SIZE = len(self.game.MAP)
        for row in range(self.Y_SIZE):
            for col in range(self.X_SIZE):
                if self.game.MAP[row][col] in ["S","X", "Z"]:
                    for x_speed in range(-4,5):
                        for y_speed in range(-4,5):
                            state = {"x": col, "y": row, "velocity": {"x": x_speed, "y": y_speed}}
                            action = self.game.ACTIONS[3]
                            policy[f"{state}"] = action
                            value_function[f"{state}"] = 0
        return policy, value_function

    def policy_evaluation(self, g , value_function, t):
        learn_rate = 1 / t
        for state in g.keys():
            old_value = value_function[state]
            value_function[state] = old_value + (learn_rate * (g[state] - old_value))
        return value_function

    def policy_improvment(self):
        pass

    def main(self, map_id, n_episode):
        policy, value_function = self.init_policy_evaluation()
        policy_cost=0
        g = {}
        t = 1
        for _ in range(n_episode):
            for state in policy.keys():
                self.game = Game(map_id=map_id, x_pos=state['x'], y_pos=state['y'], x_speed=state['velocity']['x'], y_speed=state['velocity']['y'])
                episode_cost = self.monte_carlo_rollout_for_one_start(policy)
                g[state] = episode_cost
            value_function = self.policy_evaluation(g, value_function, t)
        self.policy_improvment()

    def policy_iteration_mc(self, gamma=0.99, theta=0.0001, n_rollouts=10):
        possible_actions = self.game.get_selectable_actions()

        # Initialize random policy
        policy, value_function = self.init_policy_evaluation()
        policy_cost = 0
        while True:
            # Policy Evaluation
            delta = 0
            episode, policy_cost = self.monte_carlo_rollout(policy, policy_cost, gamma, n_rollouts)
            for state, action, cost in episode:
                if state not in value_function:
                    value_function[f"{state}"] = 0
                old_value = value_function[f"{state}"]
                #value_function[f"{state}"] += (policy_cost - value_function[f"{state}"])#cost
                value_function[f"{state}"] = cost
                #delta = max(delta, abs(G - old_value))# value_function[f"{state}"] - old_value
                delta = value_function[f"{state}"] - old_value

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
                                    action_values[action] = reward + gamma * value_function[f"{next_state}"]
                                best_action = max(action_values, key=action_values.get)
                                policy[f"{state}"] = best_action
                                if old_action != best_action:
                                    policy_stable = False
            if policy_stable:
                break

        return policy, value_function

if __name__ == "__main__":
    agent = Agent()
    agent.main()

# policy = [{s0: a0}, {s1: a1}]
