from ..Game.Game import Game
import json


class Agent:

    X_SIZE = 0
    Y_SIZE = 0

    game = None

    def __init__(self):
        pass

    def find_optimal_policy(self, map_id, num_episode):
        policy, init_value_function = self.init_policy_evaluation()

        old_policy = {}
        while policy != old_policy:
            value_function = self.evaluate_policy(
                map_id, num_episode, policy, init_value_function
            )
            old_policy = policy
            policy = self.improve_policy(
                map_id=map_id, policy=policy, value_function=value_function
            )

        return policy

    def init_policy_evaluation(self):
        # state: (x, y, (x_speed, y_speed))
        # velocity range in both directions: [-4,+4]
        # MAP[y][x] must be one of S,X,Z
        # default action is always accelerate up
        policy = {}
        value_function = {}
        self.X_SIZE = len(self.game.MAP[0])
        self.Y_SIZE = len(self.game.MAP)
        for row in range(self.Y_SIZE):
            for col in range(self.X_SIZE):
                if self.game.MAP[row][col] in ["S", "X", "Z"]:
                    for x_speed in range(-4, 5):
                        for y_speed in range(-4, 5):
                            state = (
                                col,  # x
                                row,  # y
                                (x_speed, y_speed),  # velocity
                            )
                            action = self.game.ACTIONS[3]
                            policy[state] = action
                            value_function[state] = 0
        return policy, value_function

    def evaluate_policy(self, map_id, num_episode, policy, init_value_function):
        t = 1
        curr_value_function = init_value_function
        while t <= num_episode:
            g = {}
            for state in policy.keys():
                self.game = Game(
                    map_id=map_id,
                    x_pos=state[0],
                    y_pos=state[1],
                    x_speed=state[2][0],
                    y_speed=state[2][1],
                )
                g[state] = self.get_episode_cost(policy)
            curr_value_function = self.update_value_function(
                g, curr_value_function, learn_rate=1 / t
            )
            t += 1
        return curr_value_function

    def get_episode_cost(self, policy):
        """
        Get episode cost after applying the given policy to the game in an episode
        """
        episode_cost = 0
        while not self.game.is_finished():
            state = self.game.get_state()
            action = policy[state]
            cost = self.game.change_state(action)
            episode_cost += cost
        return episode_cost

    def update_value_function(self, g, value_function, learn_rate):
        """
        Update value function in Monte Carlo algorithm
        """
        new_value_function = {}
        for state in g.keys():
            new_value_function[state] = value_function[state] + (
                learn_rate * (g[state] - value_function[state])
            )
        return new_value_function

    def improve_policy(self, map_id, policy, value_function):

        for row in range(self.Y_SIZE):
            for col in range(self.X_SIZE):
                if self.game.MAP[row][col] in ["S", "X", "Z"]:
                    for x_speed in range(-4, 5):
                        for y_speed in range(-4, 5):
                            state = (col, row, (x_speed, y_speed))
                            self.game = Game(
                                map_id=map_id,
                                x_pos=state[0],
                                y_pos=state[1],
                                x_speed=state[2][0],
                                y_speed=state[2][1],
                            )
                            possible_actions = self.game.get_selectable_actions()
                            action_values = {}
                            for action in possible_actions:
                                cost = self.game.change_state(action)
                                action_values[action] = (
                                    cost + value_function[self.game.get_state()]
                                )
                            best_action = min(action_values, key=action_values.get)
                            policy[state] = best_action

        return policy


if __name__ == "__main__":
    agent = Agent()
    print("Start Agent")
    policy = agent.find_optimal_policy()
    print("Agent has found optimal policy")
    with open("optimal_policy.json", "w") as f:
        json.dump(policy, f)

# policy = [{s0: a0}, {s1: a1}]
