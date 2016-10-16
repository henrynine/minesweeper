import minesweeper as ms

diff = {1:(9, 9, 10),
        2:(16, 16, 40),
        3:(16, 30, 100)}

actions = {'fl': lambda x, y, b: board.flag_square(x, y),
           'cl': lambda x, y, b: board.check_square(x, y),
           'ch': lambda x, y, b: board.chord_square(x, y)}

d = int(input(("Welcome to Minesweeper!\nType '1' for beginner, '2' for intermediate, and '3' for advanced: ")))

board = ms.Board(diff[d][0], diff[d][1], diff[d][2])

game_state = 1

while game_state and (len(board.known)+len(board.flagged)<board.height*board.width):
    board.printboard()
    action = str(input('Flag, click, or chord?'))
    xco = int(input('Enter row: '))
    yco = int(input('Enter column: '))
    game_state = actions[action](xco, yco, board)
    print('game_state: ', game_state)

board.reveal_all()

if game_state==0:
    print("Game over!")

else:
    print("You won!")

board.printboard()
