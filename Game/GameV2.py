from Topology import Topology
from Screen import Screen
import itertools
import random
import math
import numpy

class Game:
    # Params that do not change after each episode
    # (x,y)
    ACTIONS = [
        ("B", "B"),
        ("B", "H"),  # Right
        ("B", "V"),
        ("H", "B"),  # UP
        ("H", "H"),
        ("H", "V"),  # Down
        ("V", "B"),
        ("V", "H"),  # Left
        ("V", "V"),
    ]
    MAP = None
    START_POS = None
    START_VELOCITY = None

    # Params that change after each episode
    timestep = None
    velocity = None
    pos = None
    num_collision = None
    screen = None

    def __init__(self, map_id, x_pos, y_pos, x_speed, y_speed, show_screen=False):
        self.MAP = Topology.get_map(map_id)
        self.START_POS = {"x": x_pos, "y": y_pos}
        self.START_VELOCITY = {"x": x_speed, "y": y_speed}
        self.SHOW_SCREEN = show_screen

        self.timestep = 0
        self.velocity = self.START_VELOCITY.copy()
        self.pos = self.START_POS.copy()
        self.num_collision = 0
        if self.SHOW_SCREEN:
            self.screen = Screen(self.MAP)

    def reset_to_original_state(
        self,
    ):
        """
        Reset the game to original state (when game is initialized)
        """
        self.timestep = 0
        self.velocity = self.START_VELOCITY.copy()
        self.pos = self.START_POS.copy()
        self.num_collision = 0
        if self.SHOW_SCREEN:
            self.screen = Screen(self.MAP)

    def change_state(
        self,
        selected_action: tuple,
        stochastic_movement=False,
        require_stochastic_next_state=False
    ):
        self.timestep += 1
        self.velocity = self.get_new_velocity(selected_action)
        new_position = self.get_new_position(self.pos.copy(), self.velocity)
        self.pos, cost = self.process_change_state(self.velocity, new_position, self.pos.copy())
        if stochastic_movement:
            self.pos, cost = self.get_stochastic_movement(self.pos, cost, require_stochastic_next_state)
        if self.check_collision(self.pos):
            raise Exception()
        return cost

    def process_change_state(self, velocity, new_position, old_position):
        lineare_function = None
        if velocity['x'] != 0:
            lineare_function = self.get_linear_function(new_position, old_position)
        return self.check_route(lineare_function, new_position, old_position, velocity)

    def get_new_velocity(self, action: tuple):
        new_velocity = self.velocity.copy()

        if self.velocity["x"] in range(1, 5):
            match action[0]:
                case "B":
                    if self.velocity["x"] < 4:
                        new_velocity["x"] += 1
                case "V":
                    new_velocity["x"] -= 1
        elif self.velocity["x"] == 0 and action[0] == "B":
            new_velocity["x"] += 1

        if self.velocity["y"] in range(1, 5):
            match action[1]:
                case "B":
                    if self.velocity["y"] < 4:
                        new_velocity["y"] += 1
                case "V":
                    new_velocity["y"] -= 1
        elif self.velocity["y"] == 0 and action[1] == "B":
            new_velocity["y"] += 1

        return new_velocity

    def get_selectable_actions(self):
        if self.is_finished():
            return []
        elif (
            self.MAP[self.pos["y"]][self.pos["x"]] == "S"
            and self.velocity["x"] == 0
            and self.velocity["y"] == 0
        ):
            return self.ACTIONS
        else:
            velocity_prediction = {}
            for a in self.ACTIONS:
                velocity_prediction[a] = self.get_new_velocity(a) # Check this function!!
            selectable_actions = [
                a
                for a in velocity_prediction.keys()
                if velocity_prediction[a]["x"] != 0 or velocity_prediction[a]["y"] != 0
            ]
            return selectable_actions

    def check_route(self, linear_function, new_pos, old_pos, velocity):
        cost = 1
        cost_penalty = 6

        min_x = min(new_pos['x'], old_pos['x'])
        max_x = max(new_pos['x'], old_pos['x'])

        min_y = min(new_pos['y'], old_pos['y'])
        max_y = max(new_pos['y'], old_pos['y'])

        last_pos_without_collision = old_pos
        if velocity['x'] == 0:
            # In case that min_y is negative we need to start at last valid pos
            for y in reversed(range(min_y, max_y+1)):
                pos = {"x": old_pos['x'], "y": y}
                pos, escaped, collision_detected = self.make_checks(pos, last_pos_without_collision)
                if escaped:
                    return pos, cost
                if collision_detected:
                    self.num_collision += 1
                    return pos, cost_penalty
                else:
                    last_pos_without_collision = pos
        else:
            sampling_rate = 100
            x_range = numpy.linspace(min_x, max_x, num=sampling_rate)
            for x in x_range:
                #  Round x and y for this function
                y = round(linear_function(x))
                pos = {"x": round(x), "y": y}
                pos, escaped, collision_detected = self.make_checks(pos, last_pos_without_collision)
                if escaped:
                    return pos, cost
                if collision_detected:
                    self.num_collision += 1
                    return pos, cost_penalty
                else:
                    last_pos_without_collision = pos

        # Doe to floating point error this is needed -_- (10,7 (0,1)) -> (10, 8, (3,1))
        if self.check_collision(new_pos):
            new_pos = last_pos_without_collision
        return new_pos, cost

    def make_checks(self, pos, last_pos_without_collision):
        is_Collision = None
        if not self.check_in_range(pos):
            return last_pos_without_collision, self.check_escape(pos), is_Collision
        if self.check_collision(pos):
            is_Collision = self.find_collision_side(pos)
            pos = self.fix_collision(is_Collision, last_pos_without_collision)
            if is_Collision == 'On-X':
                pos = self._change_pos_in_x(pos)
            elif is_Collision == 'On-Y':
                pos = self._change_pos_in_y(pos)

        return pos, self.check_escape(pos), is_Collision

    # is_Collision tells if collision is on X or Y boarder
    def fix_collision(self, is_Collision, last_pos_without_collision):
        if is_Collision == 'On-X':
            self.velocity = {"x": 1, "y": 0}
            return last_pos_without_collision
        elif is_Collision == 'On-Y':
            self.velocity = {"x": 0, "y": 1}
            return last_pos_without_collision

    # Finds pos which is next to the boarder of the collision
    def find_collision_side(self, pos):
        #  Check if we have collision on X or Y
        pos_x_positive = {'x': pos['x']+1,'y': pos['y']}
        pos_x_negative = {'x': pos['x']-1, 'y': pos['y']}
        pos_y_positive = {'x': pos['x'],'y': pos['y']+1}
        pos_y_negative = {'x': pos['x'], 'y': pos['y']-1}
        if (self.check_in_range(pos_x_positive) and not self.check_collision(pos_x_positive)) \
                or (self.check_in_range(pos_x_negative) and not self.check_collision(pos_x_negative)):
            is_Collision = "On-Y"
            return is_Collision
            #return self._check_temp_pos_positive_in_y(pos), is_Collision
        elif (self.check_in_range(pos_y_positive) and not self.check_collision(pos_y_positive)) \
                or (self.check_in_range(pos_y_negative) and not self.check_collision(pos_y_negative)):
            is_Collision = "On-X"
            return is_Collision
        else:
            raise ValueError("Failed to detect boarder")

    # Determine in which direction the fight should be move after initial collision
    # This function takes the figheter off the wall and puts it directly next to it
    def _change_pos_in_y(self, pos):
        temp_pos_positiv = {"x": pos['x'], "y": pos['y'] + 1}
        temp_pos_negative = {"x": pos['x'], "y": pos['y'] - 1}
        if self.check_in_range(temp_pos_negative) and not self.check_collision(temp_pos_negative):
            return temp_pos_negative
        elif self.check_in_range(temp_pos_positiv) and not self.check_collision(temp_pos_positiv):
            return temp_pos_positiv
        else:
            raise ValueError("No space found next to collision")

    # Determine in which direction the fight should be move after initial collision
    # This function takes the fighter off the wall and puts it directly next to it
    def _change_pos_in_x(self, pos):
        temp_pos_positiv = {"x": pos['x'] + 1, "y": pos['y']}
        temp_pos_negative = {"x": pos['x'] - 1, "y": pos['y']}
        if self.check_in_range(temp_pos_positiv) and not self.check_collision(temp_pos_positiv):
            return temp_pos_positiv
        elif self.check_in_range(temp_pos_negative) and not self.check_collision(temp_pos_negative):
            return temp_pos_negative
        else:
            raise ValueError("No space found next to collision")

    def check_in_range(self, pos):
        X_SIZE = len(self.MAP[0])
        Y_SIZE = len(self.MAP)
        return 0 <= pos['x'] < X_SIZE and 0 <= pos['y'] < Y_SIZE

    def check_escape(self, pos):
        return self.MAP[pos['y']][pos['x']] == "Z"

    def check_collision(self, pos):
        return self.MAP[pos['y']][pos['x']] == "R"

    def get_new_position(self, old_position, velocity):
        old_position['x'] += velocity['x']
        old_position['y'] -= velocity['y']
        return old_position

    def get_stochastic_movement(self, old_pos, cost, require_stochastic_next_state):
        # Determine if a stochastic steps should occure
        if not require_stochastic_next_state:
            if random.random() < 0.5:
                return old_pos, cost

        # Determine in which direction a stochastic step should occure
        if random.random() < 0.5:
            velocity = {'x': 1, 'y':0}
            new_position = self.get_new_position(old_pos.copy(), velocity)
            new_position, stochastic_cost = self.process_change_state(velocity, new_position, old_pos)
        else:
            velocity = {'x': 0, 'y': 1}
            new_position = self.get_new_position(old_pos.copy(), velocity)
            new_position, stochastic_cost = self.process_change_state(velocity, new_position, old_pos)
        if cost <= stochastic_cost:
            cost = stochastic_cost
        return new_position, cost

    def get_linear_function(self, new_pos, old_pos):
        m = (new_pos['y'] - old_pos['y']) / (new_pos['x'] - old_pos['x'])
        b = old_pos['y']-( m * old_pos['x'])
        return lambda x: m*x + b

    def get_state(self):
        return (self.pos["x"], self.pos["y"], (self.velocity["x"], self.velocity["y"]))

    def is_finished(self):
        return self.MAP[self.pos["y"]][self.pos["x"]] == "Z"

    def update_screen(self):
        if self.SHOW_SCREEN:
            self.screen.show_map()

    def update_player(self, cost):
        if self.SHOW_SCREEN:
            self.screen.show_player(self.pos, cost)

    def close_window(self):
        if self.SHOW_SCREEN:
            self.screen.close()

    def save_as_image(self, name):
        if self.SHOW_SCREEN:
            self.screen.save_as_image(name=name)