'''
Assist solving Wordle puzzles
'''
from wordle import Wordle

debug       = False
game        = Wordle(debug)
game.show_status()

while(game.is_running):
    guess = game.get_guess()
    if guess == '': 
        break
    result = game.get_result()
    if result == game.success_result(): 
        break
    game.check_guess(guess, result)
    game.show_status()

print('done\n')