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
            print(f"|---Iteration {iteration}:")
            print("|\tEvaluating policy...")
            value_function = self.evaluate_policy(
                num_episode,
                policy,
                init_value_function,
                init_g,
                start_pos,
                map_id,
                stochastic_movement,
            )
            print("|\tPolicy evaluation completed.")
            # interesting_part_of_value_function = {}
            # for state, value in value_function.items():
            #     if value != 0:
            #         interesting_part_of_value_function[state] = value
            # print(dict(sorted(interesting_part_of_value_function.items())))
            print("|\tImproving policy...")
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
            print("|\tPolicy improvement completed.")
            changes = {}
            for state, action in policy.items():
                if action != old_policy[state]:
                    changes[state] = action
            if len(changes) == 0:
                optimal_policy_found = True

            print(f"|\t{len(changes)} changes from the previous policy")

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

        if not stochastic_movement:
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
                    if action == policy[visited_state]:
                        continue

                    self.game.change_state(action)
                    next_state = self.game.get_state()
                    self.game.reset_to_original_state()
                    g[next_state] = self.get_episode_cost(
                        policy, map_id, next_state, stochastic_movement
                    )
        else:
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
                    if action == policy[visited_state]:
                        continue

                    self.game.change_state(action)
                    deterministic_next_state = self.game.get_state()
                    self.game.reset_to_original_state()
                    g[deterministic_next_state] = self.get_episode_cost(
                        policy, map_id, deterministic_next_state, stochastic_movement
                    )

                    self.game.change_state(
                        action,
                        stochastic_movement=True,
                        require_stochastic_next_state=True,
                    )
                    stochastic_next_state = self.game.get_state()
                    self.game.reset_to_original_state()
                    g[stochastic_next_state] = self.get_episode_cost(
                        policy, map_id, stochastic_next_state, stochastic_movement
                    )

    def get_episode_cost(self, policy, map_id, start_state, stochastic_movement):
        temp_game = Game(
            map_id=map_id,
            x_pos=start_state[0],
            y_pos=start_state[1],
            x_speed=start_state[2][0],
            y_speed=start_state[2][1],
        )
        path_cost_from_next_state = 0
        while not temp_game.is_finished():
            cost = temp_game.change_state(
                selected_action=policy[temp_game.get_state()],
                stochastic_movement=stochastic_movement,
            )
            path_cost_from_next_state += cost
        return path_cost_from_next_state

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
                cost = self.game.change_state(action)
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
    print("Commencing Battle of Yavin!")

    MAP_ID = 1
    START_POS_INDEX = 5
    NUM_EPISODE = 1
    STOCHASTIC_MOVEMENT = False
    print(f"Entering start position {START_POS_INDEX} in map {MAP_ID}...")
    print("Calculating shortest path to fire position...")

    optimal_policy = agent.find_optimal_policy(
        map_id=MAP_ID,
        start_pos_index=START_POS_INDEX,
        num_episode=NUM_EPISODE,
        stochastic_movement=STOCHASTIC_MOVEMENT,
    )

    print(
        f"Shortest path found for start position {START_POS_INDEX} in map {MAP_ID}! All ships, follow our lead!"
    )

    stringified_optimal_policy = {}
    for state, action in optimal_policy.items():
        stringified_optimal_policy[str(state)] = action

    folder_name = "optimal_policies"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    type = "stochastic" if STOCHASTIC_MOVEMENT else "deterministic"

    file_path = os.path.join(
        folder_name, f"{type}_map{MAP_ID}_index{START_POS_INDEX}.json"
    )

    with open(file_path, "w") as f:
        json.dump(stringified_optimal_policy, f, indent=4)
