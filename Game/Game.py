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

    timestep = 0
    map = None

    def __init__(self, selected_map, starting_pos_index):
        self.map = Topology.get_map(selected_map)
        topology = Topology()
        if selected_map == 1:
            self.position = topology.get_starting_pos(selected_map, starting_pos_index)
        elif selected_map == 2:
            self.position = topology.get_starting_pos(selected_map, starting_pos_index)
        self.screen = Screen(self.map)

    def change_position(self):
        self.position = {
            "x": self.position.x + self.speed.x,
            "y": self.position.y + self.speed.y,
        }

    def is_collide(self):
        '''new_position = {
            "x": self.position.x + self.speed.x,
            "y": self.position.y + self.speed.y,
        }'''
        new_position = {
            "x": self.position.x,
            "y": self.position.y,
        }
        #X-Crash
        i = max(self.speed["x"], self.speed["y"])


        #Y-Crash


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
        new_speed = self.speed
        if self.speed["x"] in range(0, 5):
            match action[0]:
                case Action.B:
                    if self.speed["x"] < 4:
                        new_speed["x"] += 1
                case Action.V:
                    new_speed["x"] -= 1
        elif self.speed["x"] in range(-4, 0):
            match action[0]:
                case Action.B:
                    if self.speed["x"] > -4:
                        new_speed["x"] -= 1
                case Action.V:
                    self.speed["x"] += 1

        if self.speed["y"] in range(0, 5):
            match action[1]:
                case Action.B:
                    if self.speed["y"] < 4:
                        new_speed["y"] += 1
                case Action.V:
                    new_speed["y"] -= 1
        elif self.speed["y"] in range(-4, 0):
            match action[1]:
                case Action.B:
                    if self.speed["y"] > -4:
                        new_speed["y"] -= 1
                case Action.V:
                    new_speed["y"] += 1
        return new_speed

    def get_selectable_action(self):
        if self.position.x == 0 and self.position.y == 0:
            return self.actions
        else:
            speed_prediction = {}
            for a in self.actions:
                speed_prediction[a] = self.change_speed(a)
            selectable_actions = [a for a in speed_prediction.keys() if speed_prediction[a]["x"] != 0 or speed_prediction[a]["y"] != 0]
            return selectable_actions

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


g = Game(1, 1)
g.update_screen()
import time

time.sleep(25)
