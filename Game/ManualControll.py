from GameV2 import Game
from Topology import Topology

start_pos_index=0
MAP_ID=1
start_pos = Topology.get_start_pos(map_id=MAP_ID, start_pos_index=start_pos_index)
#game = Game(map_id=MAP_ID, x_pos=start_pos["x"], y_pos=start_pos["y"], x_speed=0, y_speed=0, show_screen=True)
game = Game(map_id=MAP_ID, x_pos=10, y_pos=7, x_speed=0, y_speed=1, show_screen=True)

print("To controll the X-Wing press W,A,S,D")
game.update_screen()

while not game.is_finished():
    print(f"Speed: {game.velocity}")
    print(f"Pos: {game.pos}")
    key = input()
    action = None
    match key:
        case "w":
            action = game.ACTIONS[3]
        case "a":
            action = game.ACTIONS[7]
        case "s":
            action = game.ACTIONS[5]
        case "d":
            action = game.ACTIONS[1]
        case _:
            action = game.ACTIONS[4]
    print(action)
    cost = game.change_state(action, stochastic_movement=True, require_stochastic_next_state=True)
    game.update_player(cost=cost)
