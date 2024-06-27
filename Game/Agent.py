from Game import Game
from Topology import Topology
import json
from itertools import accumulate
import os


class Agent:

    X_SIZE = 0
    Y_SIZE = 0

    game = None

    def __init__(self):
        pass

    def find_optimal_policy(
        self, map_id, start_pos_index, num_episode, stochastic_movement=False
    ):
        policy, init_value_function, init_g, start_pos = self.initialize(
            map_id, start_pos_index
        )

        iteration = 1
        optimal_policy_found = False
        changes = {}
        while not optimal_policy_found:
            print("Iteration: ", iteration)
            value_function = self.evaluate_policy(
                num_episode,
                policy,
                init_value_function,
                init_g,
                start_pos,
                map_id,
                stochastic_movement,
            )
            # interesting_part_of_value_function = {}
            # for state, value in value_function.items():
            #     if value != 0:
            #         interesting_part_of_value_function[state] = value
            # print(dict(sorted(interesting_part_of_value_function.items())))
            old_policy = policy.copy()
            policy = self.improve_policy(
                map_id=map_id,
                policy=policy,
                value_function=value_function,
                stochastic_movement=stochastic_movement,
            )
            iteration += 1
            self.game = Game(
                map_id=map_id,
                x_pos=start_pos["x"],
                y_pos=start_pos["y"],
                x_speed=0,
                y_speed=0,
            )

            changes = {}
            for state, action in policy.items():
                if action != old_policy[state]:
                    changes[state] = action
            if len(changes) == 0:
                optimal_policy_found = True

            print(f"{len(changes)} changes from the previous policy")

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
                            if (y_speed < 0 and x_speed != 0) or (
                                y_speed <= -2 and x_speed == 0
                            ):
                                action = self.game.ACTIONS[5]  # ("H", "V")
                            elif y_speed == -1 and x_speed == 0:
                                action = self.game.ACTIONS[2]  # ("B", "V")
                            else:
                                action = self.game.ACTIONS[3]  # ("H", "B")
                            policy[state] = action
                            init_value_function[state] = 0
                            init_g[state] = 0
        return policy, init_value_function, init_g, start_pos

    def evaluate_policy(
        self,
        num_episode,
        policy,
        init_value_function: dict,
        init_g: dict,
        start_pos,
        map_id,
        stochastic_movement,
    ):
        t = 1
        value_function = init_value_function.copy()
        while t <= num_episode:
            g = init_g.copy()
            self.update_g(policy, g, map_id, stochastic_movement)
            self.update_value_function(g, value_function, learn_rate=1 / t)
            self.game = Game(
                map_id=map_id,
                x_pos=start_pos["x"],
                y_pos=start_pos["y"],
                x_speed=0,
                y_speed=0,
            )
            t += 1
        return value_function

    def update_g(self, policy, g, map_id, stochastic_movement):
        transition_costs = []
        visited_states = [self.game.get_state()]
        while not self.game.is_finished():
            action = policy[self.game.get_state()]
            cost = self.game.change_state(action, stochastic_movement)
            transition_costs.append(cost)
            visited_states.append(self.game.get_state())
        episode_g = list(reversed(list(accumulate(list(reversed(transition_costs))))))
        for i in range(len(episode_g)):
            g[visited_states[i]] = episode_g[i]

        for visited_state in visited_states[:-1]:
            self.game = Game(
                map_id=map_id,
                x_pos=visited_state[0],
                y_pos=visited_state[1],
                x_speed=visited_state[2][0],
                y_speed=visited_state[2][1],
            )
            selectable_actions = self.game.get_selectable_actions()
            for action in selectable_actions:
                self.game.change_state(action, stochastic_movement)
                next_state = self.game.get_state()
                if next_state in visited_states:
                    self.game.reset_to_original_state()
                    continue
                temp_game = Game(
                    map_id=map_id,
                    x_pos=next_state[0],
                    y_pos=next_state[1],
                    x_speed=next_state[2][0],
                    y_speed=next_state[2][1],
                )
                path_cost_from_next_state = 0
                while not temp_game.is_finished():
                    cost = temp_game.change_state(
                        policy[temp_game.get_state()], stochastic_movement
                    )
                    path_cost_from_next_state += cost
                g[next_state] = path_cost_from_next_state
                self.game.reset_to_original_state()

    def update_value_function(self, g, value_function, learn_rate):
        """
        Update value function in Monte Carlo algorithm
        """
        for state in g.keys():
            old_value = value_function[state]
            value_function[state] = old_value + (learn_rate * (g[state] - old_value))

    def improve_policy(self, map_id, policy, value_function, stochastic_movement):
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
            action_costs = {}
            for action in selectable_actions:
                cost = self.game.change_state(action, stochastic_movement=False)
                deterministic_next_state = self.game.get_state()
                if stochastic_movement:
                    self.game.reset_to_original_state()
                    self.game.change_state(
                        action,
                        stochastic_movement=True,
                        require_stochastic_next_state=True,
                    )
                    stochastic_next_state = self.game.get_state()
                    action_costs[action] = 0.5 * (
                        cost + value_function[stochastic_next_state]
                    ) + 0.5 * (cost + value_function[deterministic_next_state])
                else:
                    action_costs[action] = (
                        cost + value_function[deterministic_next_state]
                    )
                self.game.reset_to_original_state()
            if action_costs != {}:
                min_cost = min(action_costs.values())
                actions_with_min_cost = [
                    action for action, cost in action_costs.items() if cost == min_cost
                ]
                if policy[state] in actions_with_min_cost:
                    best_action = policy[state]
                else:
                    best_action = actions_with_min_cost[0]
            else:
                best_action = policy[state]
            greedy_policy[state] = best_action
        return greedy_policy


if __name__ == "__main__":
    agent = Agent()
    print("Start Agent")
    map_id = 1
    start_pos_index = 1
    stochastic_movement = False
    optimal_policy = agent.find_optimal_policy(
        map_id=map_id,
        start_pos_index=start_pos_index,
        num_episode=1,
        stochastic_movement=stochastic_movement,
    )
    stringified_optimal_policy = {}
    for state, action in optimal_policy.items():
        stringified_optimal_policy[str(state)] = str(action)
    print(
        f"Agent has found optimal policy for start position index {start_pos_index} in map {map_id}"
    )

    folder_name = "optimal_policies"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if stochastic_movement:
        type = "stochastic"
    else:
        type = "deterministic"

    file_path = os.path.join(
        folder_name, f"map{map_id}_index{start_pos_index}_{type}.json"
    )

    with open(file_path, "w") as f:
        json.dump(stringified_optimal_policy, f, indent=4)
