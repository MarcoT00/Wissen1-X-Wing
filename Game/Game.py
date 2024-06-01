from Action import Action
from Topology import Topology
from Screen import Screen


class Game:
    speed = {"x": 0, "y": 0}
    position = {"x": None, "y": None}
    action = {"x": Action, "y": Action}
    actions = [
        (Action.B, Action.B),
        (Action.B, Action.H),
        (Action.B, Action.V),
        (Action.H, Action.B),
        (Action.H, Action.H),
        (Action.H, Action.V),
        (Action.V, Action.B),
        (Action.V, Action.H),
        (Action.V, Action.V),
    ]
    # actions = {
    #     "acceleration": Action.acceleration,
    #     "hold": Action.hold,
    #     "slow": Action.slow,
    # }
    timestep = 0
    map = None

    def __init__(self, selected_map, starting_pos):
        self.map = Topology.get_map(selected_map)
        if selected_map == 1:
            self.position = Topology.getStartingPos(self.map, 1, 1)
        elif selected_map == 2:
            self.position = Topology.getStartingPos(self.map, 1, 1)
        self.screen = Screen(self.map)

    def set_position(self):
        self.position = {
            "x": self.position.x + self.speed.x,
            "y": self.position.y + self.speed.y,
        }

    def check_for_collision(self):
        pass

    def control(self, action: tuple, speed: dict):
        self.timestep += 1
        match action[0]:
            case Action.B:
                speed["x"] += 1
            case Action.V:
                speed["x"] -= 1
        match action[1]:
            case Action.B:
                speed["y"] += 1
            case Action.V:
                speed["y"] -= 1

        action(speed)

    def update_screen(self):
        self.screen.show_map()

    def update_player(self):
        self.screen.show_player()


g = Game(2, 1)
g.update_screen()
import time

time.sleep(25)
