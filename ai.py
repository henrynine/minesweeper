import minesweeper as ms
import random as rand

#chords a square with full flags
def vf_chord(b):
    for square in b.known:
        if b.get_vf(square[0], square[1]) == 0:
            b.chord_square(square[0], square[1])

#flags a square where unk., unflagged == vf
def flag_to_vf(b):
    for square in b.known:
        if (b.count_unknown(square[0], square[1]) - b.count_flags(square[0], square[1])) == b.get_vf(square[0], square[1]):
            for sur in b.get_adj_squares(square[0], square[1]):
                if sur not in b.known and sur not in b.flagged:
                    b.flag_square(sur[0], sur[1])

def click_random(b):
    elig = []
    for x in range(b.width):
        for y in range(b.height):
            if ((x, y) not in b.known) and ((x, y) not in b.flagged):
                elig.append((x, y))
    if elig:
        square = rand.choice(elig)
        return b.check_square(square[0], square[1])
    return 0

#compares a board against past format to check if same
def check_same(r, b):
    newr = b.format()
    if r == newr:
        return 1
    return 0

def basic_loop(b):
    initial_state = b.format()
    flag_to_vf(b)
    vf_chord(b)
    if b.format()==initial_state:
        return 0#no change
    return 1#changed

def guess(b):
    return click_random(b)

def orig_loop():
    while str(input('Play?'))=="y":
        d = int(input(("Welcome to Minesweeper AI Edition!\nType '1' for beginner, '2' for intermediate, and '3' for advanced: ")))

        board = ms.Board(ms.diff[d][0], ms.diff[d][1], ms.diff[d][2])

        board.printboard()

        click_random(board)

        while (board.check_over()==0):
            initial_state = board.format()
            print('clicked:')
            board.printboard()
            input('Press enter to advance.')
            flag_to_vf(board)
            print('flagged:')
            board.printboard()
            vf_chord(board)
            if check_same(initial_state, board):
                print('clicking random.')
                click_random(board)

            #repeat flag to vf->chord vf until stuck
            #patterns until stuck
            #guess
        board.printboard()

        if board.check_over()==1:
            print("I won!")
        if board.check_over()==2:
            print("I lost.")

        board.reveal_all()
        '''if :
            print("Game over!")

        else:
            print("You won!")'''

        board.printboard()

def new_loop():
    while str(input('Play?'))=="y":
        d = int(input(("Welcome to Minesweeper AI Edition!\nType '1' for beginner, '2' for intermediate, and '3' for advanced: ")))

        board = ms.Board(ms.diff[d][0], ms.diff[d][1], ms.diff[d][2])

        click_random(board)

        while True:
            l = basic_loop(board)
            while l!=0:
                print('l: ', l)
                l = basic_loop(board)
            print('basic loop is stuck')
            print('check_over: ', board.check_over())
            if board.check_over()!=0:
                print('breaking')
                break
            print('guessing')
            g = guess(board)
            print('g: ', g)
            print('check_over: ', board.check_over())
            if g==0:
                print('breaking bc g==0')
                break
            if board.check_over()!=0:
                print('breaking')
                break
        board.printboard()
        print('final check_over: ', board.check_over())
        print('empty: ', board.empty)
        print('known: ', board.known)
        if board.check_over()==1:
            print("I won!")
        if board.check_over()==2:
            print("I lost.")
        board.reveal_all()
        board.printboard()
