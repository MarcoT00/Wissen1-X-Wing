from Topology import Topology
from Game import Game
import json
import time
import os
import ast


class Simulate:
    num_collision = None
    policy = None

    def __init__(
        self, map_id=1, start_pos_index=0, num_flight=100, type="deterministic"
    ):
        self.num_collision = 0
        self.policy = self.read_policy_json_input(type, map_id, start_pos_index)

        # n_start = len(Topology.start_positions_map_1)
        start_pos = Topology.get_start_pos(map_id, start_pos_index)
        game = Game(
            map_id=map_id,
            x_pos=start_pos["x"],
            y_pos=start_pos["y"],
            x_speed=0,
            y_speed=0,
            show_screen=True,
        )
        flight_costs = {}
        for i in range(1, 1 + num_flight):
            flight_costs[i] = self.execute_simulation(game)
            print(
                f"{i}-th flight, number of actions leading to collision: {game.num_collision}"
            )
            if game.num_collision != 0:
                self.num_collision += 1
            game.reset_to_original_state()
        print(
            f"Number of flights in which collision occurred: {self.num_collision}/{num_flight}"
        )
        min_cost = min(flight_costs.values())
        min_cost_flights = [
            flight_id for flight_id, cost in flight_costs.items() if cost == min_cost
        ]
        print(f"Flight(s) with minimal cost: {min_cost_flights}; Cost: {min_cost}")

    def execute_simulation(self, game: Game):
        flight_cost = 0
        game.update_screen()
        game.update_player(flight_cost)
        while not game.is_finished():
            action = self.policy[game.get_state()]
            cost = game.change_state(action)
            flight_cost += cost
            game.update_player(flight_cost)
            time.sleep(1)
        time.sleep(15)
        return flight_cost

    def read_policy_json_input(self, type, map_id, start_pos_index):
        folder_name = "optimal_policies"
        file_path = os.path.join(
            folder_name, f"{type}_map{map_id}_index{start_pos_index}.json"
        )
        with open(file_path) as f:
            policy_input = json.load(f)
        policy = {}
        for key, value in policy_input.items():
            tuple_key = ast.literal_eval(key)
            policy[tuple_key] = tuple(value)
        return policy


s = Simulate(map_id=2, start_pos_index=0, num_flight=1, type="deterministic")
