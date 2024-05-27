from Action import Action
from Topology import Topology
from Screen import Screen


class Game:
    speed = {"x": 0, "y": 0}
    position = {"x": None, "y": None}
    action = {"x": Action, "y": Action}
    actions = {"acceleration": Action.acceleration, "hold": Action.hold, "slow": Action.slow}
    timestep = 0
    map = None

    def __init__(self, selected_map, starting_pos):
        if selected_map == 1:
            self.map = Topology.map1
            self.position = Topology.getStartingPos(self.map, 1, 1)
        elif selected_map == 2:
            self.map = Topology.map2
            self.position = Topology.getStartingPos(self.map, 1, 1)
        self.screen = Screen(self.map)

    def set_position(self):
        self.position = {"x": self.position.x + self.speed.x, "y": self.position.y + self.speed.y}

    def check_for_collision(self):
        pass

    def control(self, action, speed):
        self.timestep += 1
        action(speed)

    def update_screen(self):
        self.screen.show_map()

    def update_player(self):
        self.screen.show_player()


