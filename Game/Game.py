from Topology import Topology
from Screen import Screen
import itertools
import random


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

    def __init__(self, map_id, x_pos, y_pos, x_speed, y_speed):
        self.MAP = Topology.get_map(map_id)
        self.START_POS = {"x": x_pos, "y": y_pos}
        self.START_VELOCITY = {"x": x_speed, "y": y_speed}

        self.timestep = 0
        self.velocity = self.START_VELOCITY.copy()
        self.pos = self.START_POS.copy()
        self.num_collision = 0
        self.screen = Screen(self.MAP)

    def reset_to_original_state(
        self,
    ):
        """
        Reset the game after each episode
        """
        self.timestep = 0
        self.velocity = self.START_VELOCITY.copy()
        self.pos = self.START_POS.copy()
        self.num_collision = 0
        self.screen = Screen(self.MAP)

    def change_state(self, selected_action: tuple):
        self.timestep += 1
        cost = 0

        # Get new velocity based on selected action
        new_velocity = self.get_new_velocity(selected_action)

        # Get possible routes and movement sequences when moving with the new velocity
        possible_routes, possible_movement_sequences = (
            self.get_possible_routes_and_movement_sequences(
                current_pos=self.pos, velocity=new_velocity
            )
        )

        escape_is_possible, escape_pos = self.check_escape(possible_routes)
        if escape_is_possible:
            self.velocity = new_velocity
            self.pos = self.get_new_pos(
                velocity=new_velocity,
                escape_is_possible=True,
                escape_pos=escape_pos,
            )
            cost = 1
        elif self.collision_is_certain(possible_routes):
            while self.collision_is_certain(possible_routes):
                velocity_after_collision = self.get_velocity_after_collision(
                    possible_movement_sequences
                )
                possible_routes, possible_movement_sequences = (
                    self.get_possible_routes_and_movement_sequences(
                        current_pos=self.pos,
                        velocity=velocity_after_collision,
                    )
                )
            self.velocity = velocity_after_collision
            self.pos = self.get_new_pos(
                velocity=velocity_after_collision,
                escape_is_possible=False,
                escape_pos=None,
            )
            cost = 1 + 5
            self.num_collision += 1
        else:
            self.velocity = new_velocity
            self.pos = self.get_new_pos(
                velocity=new_velocity, escape_is_possible=False, escape_pos=None
            )
            cost = 1

        return cost

    def get_velocity_after_collision(self, possible_movement_sequences: list):
        # Each elem of each sequence is one of the following types:
        # (x, 1), (x, -1), (y, 1), (y, -1) : Right, Left, Up, Down
        # All sequences have at least one type and at most two types
        # Last elem is the movement that causes collision
        colliding_movements = []
        for movement_seq in possible_movement_sequences:
            colliding_movements.append(movement_seq[-1])
        colliding_movement_types = list(set(colliding_movements))

        if len(colliding_movement_types) == 1:
            match colliding_movement_types[0]:
                case ("x", 1):
                    return {"x": 0, "y": 1}
                case ("x", -1):
                    return {"x": 0, "y": 1}
                case ("y", 1):
                    return {"x": 1, "y": 0}
                case ("y", -1):
                    return {"x": 1, "y": 0}
        else:
            match colliding_movement_types:
                case set([("x", 1), ("y", 1)]):
                    return {"x": -1, "y": -1}
                case set([("x", 1), ("y", -1)]):
                    return {"x": -1, "y": 1}
                case set([("x", -1), ("y", 1)]):
                    return {"x": 1, "y": -1}
                case set([("x", -1), ("y", -1)]):
                    return {"x": 1, "y": 1}

    def check_escape(self, possible_routes: list):
        for route in possible_routes:
            if route[-1][1] == "Z":
                return True, route[-1][0]
        return False, None

    def collision_is_certain(self, possible_routes: list):
        for route in possible_routes:
            if route[-1][1] != "R":
                return False
        return True

    def get_possible_routes_and_movement_sequences(self, current_pos, velocity):
        """
        Route: sequence of cells until no movement left or the agent has reached R or Z
        """

        # Get possible movement sequences
        num_x_moves = abs(velocity["x"])
        num_y_moves = abs(velocity["y"])
        x_move = (
            ("x", int(velocity["x"] / num_x_moves)) if num_x_moves != 0 else ("x", 0)
        )
        y_move = (
            ("y", int(velocity["y"] / num_y_moves)) if num_y_moves != 0 else ("y", 0)
        )
        movement_list = [x_move] * num_x_moves + [y_move] * num_y_moves
        unique_permutations = set(itertools.permutations(movement_list))
        available_movement_sequences = [
            list(permutation) for permutation in unique_permutations
        ]

        # From possible movement sequences, extract the possible routes
        # For each movement sequence, stop extracting when reaching R or Z
        possible_movement_sequences = []
        possible_routes = []

        for movement_seq in available_movement_sequences:
            route = [
                (
                    current_pos,
                    self.MAP[current_pos["y"]][current_pos["x"]],
                )
            ]
            possible_movement_seq = []

            for movement in movement_seq:
                next_pos = {
                    "x": route[-1][0]["x"],
                    "y": route[-1][0]["y"],
                }
                if movement[0] == "x":
                    next_pos[movement[0]] = next_pos[movement[0]] + movement[1]
                else:
                    next_pos[movement[0]] = next_pos[movement[0]] - movement[1]
                next_pos_type = self.MAP[next_pos["y"]][next_pos["x"]]
                route.append((next_pos, next_pos_type))
                possible_movement_seq.append(movement)
                if next_pos_type in ["R", "Z"]:
                    break

            possible_routes.append(route)
            possible_movement_sequences.append(possible_movement_seq)

        return possible_routes, possible_movement_sequences

    def get_new_pos(self, velocity: dict, escape_is_possible: bool, escape_pos: dict):
        """if random.random() < 0.5:
            x_move = int(velocity["x"] / abs(velocity["x"])) if velocity["x"] != 0 else 0
            y_move = int(velocity["y"] / abs(velocity["y"])) if velocity["y"] != 0 else 0
            if x_move != 0 and y_move != 0:
                if random.random() < 0.5:
                    x_move = 0
                else:
                    y_move = 0
            return {
                "x": self.pos["x"] + x_move,
                "y": self.pos["y"] - y_move,
            }
        else:"""
        if escape_is_possible:
            return escape_pos
        else:
            return {
                "x": self.pos["x"] + velocity["x"],
                "y": self.pos["y"] - velocity["y"],
            }

    def get_new_velocity(self, action: tuple):
        new_velocity = self.velocity

        if self.velocity["x"] in range(0, 5):
            match action[0]:
                case "B":
                    if self.velocity["x"] < 4:
                        new_velocity["x"] += 1
                case "V":
                    new_velocity["x"] -= 1
        elif self.velocity["x"] in range(-4, 0):
            match action[0]:
                case "B":
                    if self.velocity["x"] > -4:
                        new_velocity["x"] -= 1
                case "V":
                    self.velocity["x"] += 1

        if self.velocity["y"] in range(0, 5):
            match action[1]:
                case "B":
                    if self.velocity["y"] < 4:
                        new_velocity["y"] += 1
                case "V":
                    new_velocity["y"] -= 1
        elif self.velocity["y"] in range(-4, 0):
            match action[1]:
                case "B":
                    if self.velocity["y"] > -4:
                        new_velocity["y"] -= 1
                case "V":
                    new_velocity["y"] += 1

        return new_velocity

    def get_selectable_actions(self):
        if self.pos["x"] == 0 and self.pos["y"] == 0:
            return self.ACTIONS
        else:
            velocity_prediction = {}
            for a in self.ACTIONS:
                velocity_prediction[a] = self.get_new_velocity(a)
            selectable_actions = [
                a
                for a in velocity_prediction.keys()
                if velocity_prediction[a]["x"] != 0 or velocity_prediction[a]["y"] != 0
            ]
            return selectable_actions

    def get_state(self):
        return (self.pos["x"], self.pos["y"], (self.velocity["x"], self.velocity["y"]))

    def is_finished(self):
        return self.MAP[self.pos["y"]][self.pos["x"]] == "Z"

    def update_screen(self):
        self.screen.show_map()

    def update_player(self):
        self.screen.show_player(self.pos)
