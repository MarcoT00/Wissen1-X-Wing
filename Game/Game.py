import Action, Topology

class Game:
    speed = {"x": 0, "y": 0}
    position = {"x": 0, "y": 0}
    action = {"x": Action, "y": Action}
    actions = {"acceleration": Action.acceleration,  "hold": Action.hold, "slow": Action.slow}

    def start_game(self, selected_map, starting_pos):
        if selected_map == 1:
            map = Topology.map1
            starting_pos = Topology.start_map_1[starting_pos]
        elif selected_map == 2:
            map = Topology.map2
            starting_pos = Topology.start_map_2[starting_pos]
