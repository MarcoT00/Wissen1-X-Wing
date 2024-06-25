from ..Game.Topology import Topology
from ..Game.Game import Game
import json
import time


class Simulate:
    num_collision = None
    policy = None

    def __init__(self, map_id=1, start_pos_index=1, num_test_flight=100):
        self.num_collision = 0
        with open("optimal_policy.json") as f:
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
        for i in range(1, 1 + num_test_flight):
            self.execute_simulation(game)
            print(
                f"{i}-th flight, number of actions leading to collision: {game.num_collision}"
            )
            if game.num_collision != 0:
                self.num_collision += 1
            game.episode_reset()
        print(
            f"Number of flights in which collision occurred: {self.num_collision}/100"
        )

    def execute_simulation(self, game: Game):
        episode_cost = 0
        game.update_screen()
        while not game.is_finished():
            state = game.get_state()
            action = self.policy[state]
            cost = game.change_state(action)
            episode_cost += cost
            game.update_player()
            time.sleep(1)
