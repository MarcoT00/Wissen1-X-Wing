from Topology import Topology
from Screen import Screen
import random
import numpy as np


class Game:
    # Params that do not change after each episode
    # (x,y)
    ACTIONS = [
        ("H", "B"),  # UP
        ("V", "B"),
        ("B", "V"),
        ("B", "H"),  # Right
        ("B", "B"),
        ("H", "V"),  # Down
        ("V", "H"),  # Left
        ("H", "H"),
        ("V", "V"),
    ]
    MAP = None
    START_POS = None
    START_VELOCITY = None

    # Params that change after each episode
    velocity = None
    pos = None
    num_collision = None
    screen = None

    def __init__(self, map_id, x_pos, y_pos, x_speed, y_speed, show_screen=False):
        self.MAP = Topology.get_map(map_id)
        self.START_POS = {"x": x_pos, "y": y_pos}
        self.START_VELOCITY = {"x": x_speed, "y": y_speed}
        self.SHOW_SCREEN = show_screen

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
        self.velocity = self.START_VELOCITY.copy()
        self.pos = self.START_POS.copy()
        self.num_collision = 0
        if self.SHOW_SCREEN:
            self.screen = Screen(self.MAP)

    def change_state(
        self,
        selected_action: tuple,
        stochastic_movement=False,
        require_stochastic_next_state=False,
        stochastic_type=None,
    ):
        if self.is_finished():
            return 0

        # Get new velocity based on selected action
        new_velocity = self.get_new_velocity(selected_action)

        # Get possible routes and movement sequences when moving with the new velocity
        possible_route, possible_mvmt_seq = self.get_possible_route_and_mvmt_seq(
            current_pos=self.pos, velocity=new_velocity
        )

        if self.escape_is_possible(possible_route):
            self.velocity = new_velocity
            self.pos = self.get_new_pos(
                escape_is_possible=True,
                escape_pos=possible_route[-1][0],
            )
            return 1
        elif self.collision_is_certain(possible_route):
            velocity_after_collision = self.get_velocity_after_collision(
                possible_mvmt_seq
            )
            self.velocity = velocity_after_collision
            self.pos = self.get_new_pos(
                velocity=velocity_after_collision,
                stochastic_movement=stochastic_movement,
                require_stochastic_next_state=require_stochastic_next_state,
                possible_route=possible_route,
                possible_mvmt_seq=possible_mvmt_seq,
                stochastic_type=stochastic_type,
            )
            self.num_collision += 1
            return 1 + 5
        else:
            self.velocity = new_velocity
            self.pos = self.get_new_pos(
                velocity=new_velocity,
                stochastic_movement=stochastic_movement,
                require_stochastic_next_state=require_stochastic_next_state,
                stochastic_type=stochastic_type,
            )
            return 1

    def get_velocity_after_collision(self, possible_mvmt_seq: list):
        # Each elem of each sequence is one of the following types: (x, 1), (y, 1)
        # All sequences have at least one type and at most two types
        # Last elem in a movement sequence is the movement that causes collision
        match possible_mvmt_seq[-1]:
            case ("x", 1):
                return {"x": 0, "y": 1}
            case ("y", 1):
                return {"x": 1, "y": 0}

    def escape_is_possible(self, possible_route: list):
        return possible_route[-1][1] == "Z"

    def collision_is_certain(self, possible_route: list):
        return possible_route[-1][1] == "R"

    def get_possible_route_and_mvmt_seq(self, current_pos, velocity):
        """
        Route: sequence of cells until no movement left or the agent has reached R or Z
        """

        # Extract movement sequence from given velocity
        if velocity["x"] == 0 or velocity["y"] == 0:
            num_x_moves = abs(velocity["x"])
            num_y_moves = abs(velocity["y"])
            x_move = (
                ("x", int(velocity["x"] / num_x_moves))
                if num_x_moves != 0
                else ("x", 0)
            )
            y_move = (
                ("y", int(velocity["y"] / num_y_moves))
                if num_y_moves != 0
                else ("y", 0)
            )
            movement_seq = [x_move] * num_x_moves + [y_move] * num_y_moves
        else:
            x_flight_pos = list(np.arange(0, velocity["x"] + 0.1, 0.1))
            y_flight_pos = [x * velocity["y"] / velocity["x"] for x in x_flight_pos]
            x_displacements = [round(x) for x in x_flight_pos]
            y_displacements = [round(y) for y in y_flight_pos]
            displacements = list(zip(x_displacements, y_displacements))
            dedup_displacements = []
            for d in displacements:
                if d not in dedup_displacements:
                    dedup_displacements.append(d)
            displacements = dedup_displacements.copy()
            movement_seq = []
            previous_pair = displacements[0]
            for pair in displacements[1:]:
                pair_diff = (pair[0] - previous_pair[0], pair[1] - previous_pair[1])
                if pair_diff[0] == 1 and pair_diff[1] == 1:
                    movement_seq.append(("y", 1))
                    movement_seq.append(("x", 1))
                elif pair_diff[0] == 1 and pair_diff[1] == 0:
                    movement_seq.append(("x", 1))
                elif pair_diff[1] == 1 and pair_diff[0] == 0:
                    movement_seq.append(("y", 1))
                previous_pair = pair

        # Get possible route and possible movement sequence from the above movement sequence
        possible_route = [
            (
                current_pos,
                self.MAP[current_pos["y"]][current_pos["x"]],
            )
        ]
        possible_mvmt_seq = []
        for movement in movement_seq:
            next_pos = {
                "x": possible_route[-1][0]["x"],
                "y": possible_route[-1][0]["y"],
            }
            if movement[0] == "x":
                next_pos[movement[0]] = next_pos[movement[0]] + movement[1]
            else:
                next_pos[movement[0]] = next_pos[movement[0]] - movement[1]
            next_pos_type = self.MAP[next_pos["y"]][next_pos["x"]]
            possible_route.append((next_pos, next_pos_type))
            possible_mvmt_seq.append(movement)
            if next_pos_type in ["R", "Z"]:
                break

        return possible_route, possible_mvmt_seq

    def get_new_pos(
        self,
        velocity=None,
        escape_is_possible=False,
        escape_pos=None,
        stochastic_movement=None,
        require_stochastic_next_state=None,
        possible_route=None,
        possible_mvmt_seq=None,
        stochastic_type=None,
    ):
        if escape_is_possible:
            return escape_pos
        else:
            if (
                possible_route is not None and possible_mvmt_seq is not None
            ):  # Collision
                x_move = 0 if possible_mvmt_seq[-1] == ("x", 1) else 1  # ("y", 1)
                y_move = 1 if possible_mvmt_seq[-1] == ("x", 1) else 0  # ("y", 1)
                new_deter_x_pos = possible_route[-2][0]["x"] + x_move
                new_deter_y_pos = possible_route[-2][0]["y"] - y_move
            else:
                new_deter_x_pos = self.pos["x"] + velocity["x"]
                new_deter_y_pos = self.pos["y"] - velocity["y"]
            if not stochastic_movement:  # deterministic movement
                return {
                    "x": new_deter_x_pos,
                    "y": new_deter_y_pos,
                }
            else:
                if not require_stochastic_next_state:
                    if random.random() < 0.5:
                        return {
                            "x": new_deter_x_pos,
                            "y": new_deter_y_pos,
                        }
                    else:
                        return self.get_stochastic_next_pos(
                            new_deter_x_pos, new_deter_y_pos, stochastic_type
                        )
                else:
                    return self.get_stochastic_next_pos(
                        new_deter_x_pos, new_deter_y_pos, stochastic_type
                    )

    def stochastic_collision(self, deter_x_pos, deter_y_pos):
        return (
            (deter_x_pos + 1) >= len(self.MAP[0])
            or (deter_x_pos + 1) < 0
            or self.MAP[deter_y_pos][deter_x_pos + 1] == "R"
        ) or (
            (deter_y_pos - 1) >= len(self.MAP)
            or (deter_y_pos - 1) < 0
            or self.MAP[deter_y_pos - 1][deter_x_pos] == "R"
        )

    def get_stochastic_next_pos(self, deter_x_pos, deter_y_pos, stochastic_type):
        x_move = (
            0
            if (
                (deter_x_pos + 1) >= len(self.MAP[0])
                or (deter_x_pos + 1) < 0
                or self.MAP[deter_y_pos][deter_x_pos + 1] == "R"
            )
            else 1
        )
        y_move = (
            0
            if (
                (deter_y_pos - 1) >= len(self.MAP)
                or (deter_y_pos - 1) < 0
                or self.MAP[deter_y_pos - 1][deter_x_pos] == "R"
            )
            else 1
        )
        if x_move == 1 and y_move == 1:
            if stochastic_type == "right":
                y_move = 0
            elif stochastic_type == "up":
                x_move = 0
            else:
                if random.random() < 0.5:
                    x_move = 0
                else:
                    y_move = 0
        return {
            "x": deter_x_pos + x_move,
            "y": deter_y_pos - y_move,
        }

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
        if (
            self.MAP[self.pos["y"]][self.pos["x"]] == "S"
            and self.velocity["x"] == 0
            and self.velocity["y"] == 0
        ):
            return [
                ("B", "B"),
                ("B", "H"),
                ("H", "B"),
            ]
        else:
            velocity_prediction = {}
            non_selectable_actions = []
            if self.velocity["x"] == 0:
                non_selectable_actions.extend([a for a in self.ACTIONS if a[0] == "V"])
            elif self.velocity["x"] == 4:
                non_selectable_actions.extend([a for a in self.ACTIONS if a[0] == "B"])
            if self.velocity["y"] == 0:
                non_selectable_actions.extend([a for a in self.ACTIONS if a[1] == "V"])
            elif self.velocity["y"] == 4:
                non_selectable_actions.extend([a for a in self.ACTIONS if a[1] == "B"])
            for a in [a for a in self.ACTIONS if a not in non_selectable_actions]:
                velocity_prediction[a] = self.get_new_velocity(a)
            return [
                a
                for a in velocity_prediction.keys()
                if velocity_prediction[a]["x"] != 0 or velocity_prediction[a]["y"] != 0
            ]

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
