from Topology import Topology
from GameV2 import Game
import json
import time
import os
import ast


class Simulate:
    num_collision = None
    policy = None

    def __init__(
        self,
        map_id,
        start_pos_index,
        num_flight,
        stochastic_movement,
        folder_name,
        iteration,
        self,
        map_id,
        start_pos_index,
        num_flight,
        stochastic_movement,
        folder_name,
        iteration,
    ):
        self.num_collision = 0
        type = "stochastic" if stochastic_movement else "deterministic"
        type = "stochastic" if stochastic_movement else "deterministic"
        self.policy = self.read_saved_policy(
            type, map_id, start_pos_index, folder_name, iteration
        )

        print(f"Map {map_id}, start pos index {start_pos_index}, {type}")

        print(f"Map {map_id}, start pos index {start_pos_index}, {type}")

        # n_start = len(Topology.start_positions_map_1)
        start_pos = Topology.get_start_pos(map_id, start_pos_index)
        game = Game(
            map_id=map_id,
            x_pos=start_pos["x"],
            y_pos=start_pos["y"],
            x_speed=0,
            y_speed=0,
            # show_screen=True,
        )
        flight_costs = {}
        for i in range(1, 1 + num_flight):
            flight_costs[i] = self.execute_simulation(game, stochastic_movement)
            # print(f"|\t{i}-th flight - Cost: {flight_costs[i]}")
            flight_costs[i] = self.execute_simulation(game, stochastic_movement)
            # print(f"|\t{i}-th flight - Cost: {flight_costs[i]}")
            if game.num_collision != 0:
                self.num_collision += 1
            game.reset_to_original_state()
        print(
            f"|---Number of flights in which collision did not occur: {num_flight - self.num_collision}/{num_flight}"
            f"|---Number of flights in which collision did not occur: {num_flight - self.num_collision}/{num_flight}"
        )
        min_cost = min(flight_costs.values())
        avg_cost = sum(flight_costs.values()) / len(flight_costs)
        print(f"|---Minimum Cost: {min_cost}")
        print(f"|---Average Cost: {avg_cost}")
        avg_cost = sum(flight_costs.values()) / len(flight_costs)
        print(f"|---Minimum Cost: {min_cost}")
        print(f"|---Average Cost: {avg_cost}")

    def execute_simulation(self, game: Game, stochastic_movement):
    def execute_simulation(self, game: Game, stochastic_movement):
        flight_cost = 0
        game.update_screen()
        game.update_player(flight_cost)
        while not game.is_finished():
            action = self.policy[game.get_state()]
            cost = game.change_state(action, stochastic_movement)
            cost = game.change_state(action, stochastic_movement)
            flight_cost += cost
            game.update_player(flight_cost)
            # time.sleep(1)
        # time.sleep(10)
        return flight_cost

    def read_saved_policy(self, type, map_id, start_pos_index, folder_name, iteration):
        if iteration is None:
            file_path = os.path.join(
                folder_name, f"{type}_map{map_id}_index{start_pos_index}.json"
            )
        else:
            file_path = os.path.join(
                folder_name,
                f"{type}_map{map_id}_index{start_pos_index}_ite{iteration}.json",
            )
        with open(file_path) as f:
            policy_input = json.load(f)
        policy = {}
        for key, value in policy_input.items():
            tuple_key = ast.literal_eval(key)
            policy[tuple_key] = tuple(value)
        return policy


if __name__ == "__main__":
    for s in range(0, 1):
        s = Simulate(
            map_id=1,
            start_pos_index=s,
            num_flight=100000,
            stochastic_movement=False,
            folder_name="optimal_policiesV2",
            iteration=None,
        )
