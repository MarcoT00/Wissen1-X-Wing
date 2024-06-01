from Action import Action
from Topology import Topology
from Screen import Screen


class Game:
    speed = {"x": 0, "y": 0}
    position = {"x": None, "y": None}
    action = None
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

    def change_position(self):
        self.position = {
            "x": self.position.x + self.speed.x,
            "y": self.position.y + self.speed.y,
        }

    def is_collide(self):
        new_position = {
            "x": self.position.x + self.speed.x,
            "y": self.position.y + self.speed.y,
        }
        return not (
            0 <= new_position.x
            and len(map[0]) < new_position.x
            and 0 <= new_position.y
            and len(map) < new_position.y
            and map[new_position.x][new_position.y] != "R"
        )

    def fix_position(self):
        x_steps = self.speed.x
        y_steps = self.speed.y
        pass

    def change_speed(self, action: tuple):
        match action[0]:
            case Action.B:
                self.speed["x"] += 1
            case Action.V:
                self.speed["x"] -= 1
        match action[1]:
            case Action.B:
                self.speed["y"] += 1
            case Action.V:
                self.speed["y"] -= 1

    def change_state(self, action: tuple):
        self.timestep += 1
        self.change_speed(action)
        if not self.is_collide():
            self.change_position()
        else:
            self.fix_position()

    def update_screen(self):
        self.screen.show_map()

    def update_player(self):
        self.screen.show_player()


g = Game(2, 1)
g.update_screen()
import time

time.sleep(25)
