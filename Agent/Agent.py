from ..Game.Game import Game
from ..Game.Topology import Topology
import json
from itertools import accumulate


class Agent:

    X_SIZE = 0
    Y_SIZE = 0

    game = None

    def __init__(self):
        pass

    def find_optimal_policy(self, map_id, start_pos_index, num_episode):
        policy, init_value_function, init_g = self.initialize(map_id, start_pos_index)

        old_policy = {}
        while policy != old_policy:
            value_function = self.evaluate_policy(
                num_episode, policy, init_value_function, init_g
            )
            old_policy = policy
            policy = self.improve_policy(
                map_id=map_id, policy=policy, value_function=value_function
            )

        return policy

    def initialize(self, map_id, start_pos_index):
        # state: (x, y, (x_speed, y_speed))
        # velocity range in both directions: [-4,+4]
        # MAP[y][x] must be one of S,X,Z
        # default action is always accelerate up
        start_pos = Topology.get_start_pos(map_id, start_pos_index)
        self.game = Game(
            map_id=map_id,
            x_pos=start_pos["x"],
            y_pos=start_pos["y"],
            x_speed=0,
            y_speed=0,
        )
        policy = {}
        init_value_function = {}
        init_g = {}
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
                            init_value_function[state] = 0
                            init_g[state] = 0
        return policy, init_value_function, init_g

    def evaluate_policy(
        self, num_episode, policy, init_value_function: dict, init_g: dict
    ):
        t = 1
        value_function = init_value_function.copy()
        while t <= num_episode:
            g = init_g.copy()
            self.update_g(policy, g)
            self.update_value_function(g, value_function, learn_rate=1 / t)
            self.game.reset_to_original_state()
            t += 1
        return value_function

    def update_g(self, policy, g):
        transition_costs = []
        visited_states = [self.game.get_state()]
        while not self.game.is_finished():
            action = policy[self.game.get_state()]
            cost = self.game.change_state(action)
            transition_costs.append(cost)
            visited_states.append(self.game.get_state())
        episode_g = list(reversed(list(accumulate(list(reversed(transition_costs))))))
        for i in range(len(episode_g)):
            g[visited_states[i]] = episode_g[i]

    def update_value_function(self, g, value_function, learn_rate):
        """
        Update value function in Monte Carlo algorithm
        """
        for state in g.keys():
            old_value = value_function[state]
            value_function[state] = old_value + (learn_rate * (g[state] - old_value))

    def improve_policy(self, map_id, policy, value_function):
        # TODO: Check if the method is correct
        greedy_policy = {}

        for state in policy.keys():
            self.game = Game(
                map_id=map_id,
                x_pos=state[0],
                y_pos=state[1],
                x_speed=state[2][0],
                y_speed=state[2][1],
            )
            selectable_actions = self.game.get_selectable_actions()
            action_values = {}
            for action in selectable_actions:
                cost = self.game.change_state(action)
                action_values[action] = cost + value_function[self.game.get_state()]
                self.game.reset_to_original_state()
            best_action = min(action_values, key=action_values.get)
            greedy_policy[state] = best_action

        return greedy_policy


if __name__ == "__main__":
    agent = Agent()
    print("Start Agent")
    map_id = 1
    policy = agent.find_optimal_policy(map_id=map_id, start_pos_index=1, num_episode=10)
    print(f"Agent has found optimal policy for map {map_id}")
    with open(f"optimal_policy_map{map_id}.json", "w") as f:
        json.dump(policy, f)
