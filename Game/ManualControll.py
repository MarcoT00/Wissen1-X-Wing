from Game import Game
game = Game(map_id=1, start_pos_index=1)

print("To controll the X-Wing press W,A,S,D")
while True:
    game.update_screen()
    game.update_player()
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
            action = game.ACTIONS[2]
        case _:
            action = game.ACTIONS[4]
    game.change_state(action)
