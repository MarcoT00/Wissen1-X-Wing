from Game import Game
from Topology import Topology
import json
from itertools import accumulate
import os
import ast


class Agent:

    X_SIZE = 0
    Y_SIZE = 0

    game = None

    def __init__(
        self,
        start_pos_index,
        map_id,
        stochastic_movement,
        num_episode,
        continue_from_last_interim=False,
    ):
        print("Commencing Battle of Yavin!\n")
        print(f"Entering start position {start_pos_index} in map {map_id}...")
        print("Calculating shortest path to fire position...")

        optimal_policy = self.find_optimal_policy(
            map_id=map_id,
            start_pos_index=start_pos_index,
            num_episode=num_episode,
            stochastic_movement=stochastic_movement,
            continue_from_last_interim=continue_from_last_interim,
        )

        print(
            f"Shortest path found for start position {start_pos_index} in map {map_id}! All ships, follow our lead!"
        )

        self.save_policy(
            map_id,
            start_pos_index,
            stochastic_movement,
            policy=optimal_policy,
            folder_name="optimal_policies",
            iteration=None,
        )

    def find_optimal_policy(
        self,
        map_id,
        start_pos_index,
        num_episode,
        stochastic_movement=False,
        continue_from_last_interim=False,
    ):
        policy, init_value_function, init_g, start_pos = self.initialize(
            map_id, start_pos_index
        )

        interim_folder_name = "interim_policies"
        if continue_from_last_interim:
            policy, iteration = self.read_last_interim_policy(
                map_id, start_pos_index, stochastic_movement, interim_folder_name
            )
        else:
            self.save_policy(
                map_id,
                start_pos_index,
                stochastic_movement,
                policy,
                interim_folder_name,
                iteration=0,
            )
            self.save_visual(
                policy=policy,
                type="stochastic" if stochastic_movement else "deterministic",
                iteration=0,
                map_id=map_id,
                start_pos_index=start_pos_index,
            )
            iteration = 1

        optimal_policy_found = False
        while not optimal_policy_found:
            print(f"|---Iteration {iteration}:")

            # Policy Evaluation
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

            # Policy Improvement
            print("|\tImproving policy...")
            previous_policy = policy.copy()
            policy = self.improve_policy(
                map_id=map_id,
                policy=policy,
                value_function=value_function,
                stochastic_movement=stochastic_movement,
            )
            self.game = Game(
                map_id=map_id,
                x_pos=start_pos["x"],
                y_pos=start_pos["y"],
                x_speed=0,
                y_speed=0,
            )
            print("|\tPolicy improvement completed.")

            # Calculate changes
            changes = {}
            for state, action in policy.items():
                if action != previous_policy[state]:
                    changes[state] = action
            if len(changes) == 0:
                optimal_policy_found = True
            print(f"|\t{len(changes)} changes from the previous policy")

            # Calculate expected flight cost with previous and new policies
            previous_flight_cost = self.get_expected_flight_cost(
                previous_policy, map_id, start_pos, num_episode, stochastic_movement
            )
            print(
                f"|\tExpected flight cost with previous policy: {previous_flight_cost}"
            )
            new_flight_cost = self.get_expected_flight_cost(
                policy, map_id, start_pos, num_episode, stochastic_movement
            )
            print(f"|\tExpected flight cost with new policy: {new_flight_cost}")

            # Save interim results
            print("|\tSaving new policy...")
            self.save_policy(
                map_id,
                start_pos_index,
                stochastic_movement,
                policy,
                interim_folder_name,
                iteration=iteration,
            )
            self.save_visual(
                policy=policy,
                type="stochastic" if stochastic_movement else "deterministic",
                iteration=iteration,
                map_id=map_id,
                start_pos_index=start_pos_index,
            )
            print("|\tSave completed.")

            iteration += 1

        return policy

    def read_last_interim_policy(
        self, map_id, start_pos_index, stochastic_movement, interim_folder_name
    ):
        type = "stochastic" if stochastic_movement else "deterministic"
        last_interim_file = sorted(
            [
                f
                for f in os.listdir(interim_folder_name)
                if f"{type}_map{map_id}_index{start_pos_index}" in f
            ]
        )[-1]
        last_iteration = int(last_interim_file.split(".")[0][-1])
        current_iteration = last_iteration + 1
        file_path = os.path.join(interim_folder_name, last_interim_file)
        with open(file_path) as f:
            policy_input = json.load(f)
        policy = {}
        for key, value in policy_input.items():
            tuple_key = ast.literal_eval(key)
            policy[tuple_key] = tuple(value)
        return policy, current_iteration

    def save_policy(
        self,
        map_id,
        start_pos_index,
        stochastic_movement,
        policy,
        folder_name,
        iteration,
    ):
        stringified_policy = {}
        for state, action in policy.items():
            stringified_policy[str(state)] = action

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        type = "stochastic" if stochastic_movement else "deterministic"
        if iteration is not None:
            file_path = os.path.join(
                folder_name,
                f"{type}_map{map_id}_index{start_pos_index}_ite{iteration}.json",
            )
        else:
            file_path = os.path.join(
                folder_name,
                f"{type}_map{map_id}_index{start_pos_index}.json",
            )
        with open(file_path, "w") as f:
            json.dump(stringified_policy, f, indent=4)

    def get_expected_flight_cost(
        self, policy, map_id, start_pos, num_episode, stochastic_movement
    ):
        expected_flight_cost = 0
        t = 1
        while t <= num_episode:
            episode_cost = self.get_episode_cost(
                policy,
                map_id,
                (start_pos["x"], start_pos["y"], (0, 0)),
                stochastic_movement,
            )
            expected_flight_cost = expected_flight_cost + (1 / t) * (
                episode_cost - expected_flight_cost
            )
            t += 1
        return expected_flight_cost

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
                            turning_row = 7 if map_id == 1 else 10
                            if row >= turning_row:
                                if (y_speed < 0 and x_speed != 0) or (
                                    y_speed <= -2 and x_speed == 0
                                ):
                                    action = self.game.ACTIONS[5]  # ("H", "V")
                                elif y_speed == -1 and x_speed == 0:
                                    action = self.game.ACTIONS[2]  # ("B", "V")
                                else:
                                    action = self.game.ACTIONS[3]  # ("H", "B")
                            else:
                                if (x_speed < 0 and y_speed != 0) or (
                                    x_speed <= -2 and y_speed == 0
                                ):
                                    action = self.game.ACTIONS[7]  # ("V", "H")
                                elif x_speed == -1 and y_speed == 0:
                                    action = self.game.ACTIONS[6]  # ("V", "B")
                                else:
                                    action = self.game.ACTIONS[1]  # ("B", "H")
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
        # else:
        #     for visited_state in visited_states[:-1]:
        #         self.game = Game(
        #             map_id=map_id,
        #             x_pos=visited_state[0],
        #             y_pos=visited_state[1],
        #             x_speed=visited_state[2][0],
        #             y_speed=visited_state[2][1],
        #         )
        #         selectable_actions = self.game.get_selectable_actions()
        #         for action in selectable_actions:
        #             if action == policy[visited_state]:
        #                 continue

        #             self.game.change_state(action)
        #             deterministic_next_state = self.game.get_state()
        #             self.game.reset_to_original_state()
        #             g[deterministic_next_state] = self.get_episode_cost(
        #                 policy, map_id, deterministic_next_state, stochastic_movement
        #             )

        #             self.game.change_state(
        #                 action,
        #                 stochastic_movement=True,
        #                 require_stochastic_next_state=True,
        #             )
        #             stochastic_next_state = self.game.get_state()
        #             self.game.reset_to_original_state()
        #             g[stochastic_next_state] = self.get_episode_cost(
        #                 policy, map_id, stochastic_next_state, stochastic_movement
        #             )

    def get_episode_cost(self, policy, map_id, start_state, stochastic_movement):
        temp_game = Game(
            map_id=map_id,
            x_pos=start_state[0],
            y_pos=start_state[1],
            x_speed=start_state[2][0],
            y_speed=start_state[2][1],
        )
        path_cost_from_start_state = 0
        while not temp_game.is_finished():
            cost = temp_game.change_state(
                selected_action=policy[temp_game.get_state()],
                stochastic_movement=stochastic_movement,
            )
            path_cost_from_start_state += cost
        return path_cost_from_start_state

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

    def save_visual(self, policy, map_id, iteration, type, start_pos_index):
        episode_cost = 0
        start_pos = Topology.get_start_pos(map_id, start_pos_index)
        temp_game = Game(
            map_id=map_id,
            x_pos=start_pos["x"],
            y_pos=start_pos["y"],
            x_speed=0,
            y_speed=0,
            show_screen=True,
        )
        temp_game.update_screen()
        temp_game.update_player(episode_cost)
        while not temp_game.is_finished():
            action = policy[temp_game.get_state()]
            cost = temp_game.change_state(action)
            episode_cost += cost
            temp_game.update_player(episode_cost)
        folder_name = "image"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        img_file_name = os.path.join(
            folder_name, f"{type}_map{map_id}_index{start_pos_index}_ite{iteration}.jpg"
        )
        temp_game.save_as_image(name=img_file_name)
        temp_game.close_window()


if __name__ == "__main__":
    Agent(
        start_pos_index=0,
        map_id=2,
        stochastic_movement=False,
        num_episode=1,
        continue_from_last_interim=False,
    )
