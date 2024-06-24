from Game.Game import Game
from Game.Topology import Topology
import json
import time


class Simulate:
    def __int__(self, map_id=1, start_pos_index=1):
        self.num_collision = 0
        with open('optimal_policy.json') as f:
            self.policy = json.load(f)
        #n_start = len(Topology.start_positions_map_1)
        game = Game(map_id, start_pos_index)
        for index in range(100):
            self.execute_simulation(game)
            print("Collision with Wall: ", game.num_collision)
            if game.num_collision != 0:
                self.num_collision +=1
            game.reset()
        print("Number of times the plane collided with a Wall: ", self.num_collision)

    def execute_simulation(self, game):
        episode_cost = 0
        game.update_screen()
        while not game.is_done():
            state = game.get_state()
            action = self.policy[f"{state}"]
            cost = game.change_state(action)
            episode_cost += cost
            game.update_player()
            time.sleep(1)
        print("Episode Cost")



s = Simulate()
