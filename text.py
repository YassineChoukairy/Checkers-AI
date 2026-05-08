from checkers_engine import Checkers
game = Checkers()

game.print_board()

moves = game.get_valid_moves(game.current_player)
print("Moves:", moves)

game.make_move(moves[0])

game.print_board()