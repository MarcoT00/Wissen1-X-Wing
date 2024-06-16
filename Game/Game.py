from Topology import Topology
from Screen import Screen
import itertools
import time


class Game:
    # Hyperparameters: Params that do not change during each episode
    ACTIONS = [
        ("B", "B"),
        ("B", "H"),
        ("B", "V"),
        ("H", "B"),
        ("H", "H"),
        ("H", "V"),
        ("V", "B"),
        ("V", "H"),
        ("V", "V"),
    ]
    NUM_EPISODES = 10
    MAP = None
    END_POSITIONS = None

    # Parameters: Params that change during each episode
    timestep = 0
    lern_rate = None
    velocity = {"x": 0, "y": 0}
    position = {"x": None, "y": None}
    episode_cost = 0
    episode = []  # sequence of positions and actions that the agent takes

    def __init__(self, map_id, starting_pos_index):
        self.MAP = Topology.get_map(map_id)
        self.END_POSITIONS = Topology.get_end_positions(map_id)
        self.position = Topology.get_starting_pos(map_id, starting_pos_index)
        self.episode.append(self.position)
        self.screen = Screen(self.MAP)

    def reset(
        self,
    ):
        # TODO: Implement this
        pass

    def change_state(self, selected_action: tuple):
        self.timestep += 1
        self.lern_rate = 1 / self.timestep

        # Get new velocity based on selected action
        new_velocity = self.get_new_velocity(selected_action)

        # Get possible routes when moving with the new velocity
        possible_routes = self.get_possible_routes(
            current_position=self.position, velocity=new_velocity
        )

        escape_possible, escape_position = self.check_escape(possible_routes)
        if escape_possible:
            self.velocity = new_velocity
            self.position = escape_position
            self.episode_cost += 1
        elif self.collision_certain(possible_routes):
            self.velocity = self.get_velocity_after_collision(possible_routes)
            self.position = self.get_new_position(self.velocity)
            self.episode_cost += 1 + 5
        else:
            self.velocity = new_velocity
            self.position = self.get_new_position(self.velocity)
            self.episode_cost += 1

        self.episode.append(selected_action)
        self.episode.append(self.position)

    def get_velocity_after_collision(self, possible_routes):
        # TODO: Implement this
        return {"x": 0, "y": 0}

    def check_escape(possible_routes: list):
        for route in possible_routes:
            if route[-1][1] == "Z":
                return True, route[-1][0]
        return False, None

    def collision_certain(possible_routes: list):
        for route in possible_routes:
            if route[-1][1] != "R":
                return False
        return True

    def get_possible_routes(self, current_position, velocity):
        """
        Route: sequence of cells until no movement left or the agent has reached R or Z
        """

        # Get possible movement sequences
        num_x_moves = abs(velocity["x"])
        num_y_moves = abs(velocity["y"])
        x_move = ("x", velocity["x"] / num_x_moves) if num_x_moves != 0 else ("x", 0)
        y_move = ("y", velocity["y"] / num_y_moves) if num_y_moves != 0 else ("y", 0)
        movement_list = [x_move] * num_x_moves + [y_move] * num_y_moves
        unique_permutations = set(itertools.permutations(movement_list))
        possible_movement_sequences = [
            list(permutation) for permutation in unique_permutations
        ]

        # From possible movement sequences, extract the possible routes
        # For each movement sequence, stop extracting when reaching R or Z
        possible_routes = []
        for movement_seq in possible_movement_sequences:
            route = [
                (
                    current_position,
                    self.MAP[current_position["y"]][current_position["x"]],
                )
            ]
            for movement in movement_seq:
                next_position = {
                    "x": route[-1][0]["x"],
                    "y": route[-1][0]["y"],
                }
                next_position[movement[0]] = next_position[movement[0]] + movement[1]
                next_position_type = self.MAP[next_position["y"]][next_position["x"]]
                route.append((next_position, next_position_type))
                if next_position_type in ["R", "Z"]:
                    break
            possible_routes.append(route)
        return possible_routes

    def get_new_position(self, velocity: dict):
        return {
            "x": self.position["x"] + velocity["x"],
            "y": self.position["y"] + velocity["y"],
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
        if self.position["x"] == 0 and self.position["y"] == 0:
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

    def update_screen(self):
        self.screen.show_map()

    def update_player(self):
        self.screen.show_player()


g = Game(map_id=1, starting_pos_index=1)
g.update_screen()
time.sleep(25)
