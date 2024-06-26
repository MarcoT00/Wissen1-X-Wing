from Topology import Topology
from Game import Game
import json
import time


class Simulate:
    num_collision = None
    policy = None

    def __init__(self, map_id=1, start_pos_index=1, num_flight=100):
        self.num_collision = 0
        with open(f"optimal_policy_map{map_id}.json") as f:
            self.policy = json.load(f)
        # n_start = len(Topology.start_positions_map_1)
        start_pos = Topology.get_start_pos(map_id, start_pos_index)
        game = Game(
            map_id=map_id,
            x_pos=start_pos["x"],
            y_pos=start_pos["y"],
            x_speed=0,
            y_speed=0,
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
        # game.update_screen()
        while not game.is_finished():
            action = self.policy[game.get_state()]
            cost = game.change_state(action)
            flight_cost += cost
            # game.update_player()
            # time.sleep(1)
        return flight_cost