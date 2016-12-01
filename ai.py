import minesweeper as ms
import random as rand
import time
'''
11/27: resuming work
       seems very slow especially on advanced
       probably because checking every square
       i'm gonna try adding a list of squares that have already been chorded to not check
       pre-optimization benchmark(200):
         records:  [[150, 50], [138, 62], [75, 125]]
         time:  96.944  seconds
       post-classification benchmark(200):
         records:  [[148, 52], [139, 61], [77, 123]]
         time:  87.800  seconds
       post-self.chorded benchmark(200) (after for square in self.known in vf_chord, flag_to_vf):
         records:  [[157, 43], [140, 60], [55, 145]]
         time:  22.222  seconds
         records:  [[149, 51], [141, 59], [63, 137]]
         time:  24.389  seconds
         records:  [[155, 45], [131, 69], [62, 138]]
         time:  24.834  seconds
       strange: is clearly almost four times as fast but seems to be not quite as good for advanced only - likely just random
       __ can't flag to vf if has already been chorded bc no adjacent unknowns, obviously can't chord twice -- also 60/200 is
       __ closer to 5k pre-optimization benchmark stats
       post-self.chorded benchmark(1000):
         records:  [[725, 275], [675, 325], [349, 651]]
         time:  124.815  seconds
      post-loop change (only traverse once per iteration, not per function) benchmark(200):
        records:  [[148, 52], [138, 62], [73, 127]]
        time:  25.505  seconds (makes sense is a little higher given higher win rate on advanced)
        records:  [[154, 46], [141, 59], [75, 125]]
        time:  25.673  seconds
        records:  [[157, 43], [135, 65], [65, 135]]
        time:  23.045  seconds#approx. 5-10 percent improvement, maybe fluke given later results
        #
        second time around
        #
        records:  [[142, 58], [143, 57], [78, 122]]
        time:  26.952  seconds
        records:  [[146, 54], [133, 67], [65, 135]]
        time:  24.385  seconds
        records:  [[148, 52], [148, 52], [76, 124]]
        time:  25.092  seconds#comparing one line, probably marginally faster

      #INVALID - forgot to remove code so was definitely inefficient
          post-combining known and unchorded into one line:
            records:  [[163, 37], [132, 68], [64, 136]]
            time:  24.272  seconds#actually slower apparently probably because set construction is time consuming?
            records:  [[164, 36], [125, 75], [72, 128]]
            time:  24.261  seconds#maybe not?
            records:  [[150, 50], [142, 58], [67, 133]]
            time:  24.649  seconds

      post-combining known and unchorded into one line:
        records:  [[151, 49], [140, 60], [71, 129]]
        time:  24.168  seconds
        records:  [[144, 56], [137, 63], [76, 124]]
        time:  25.463  seconds











'''
class AI_Board(ms.Board):
    def __init__(self, h, w, n):
        ms.Board.__init__(self, h, w, n)


    '''
    def uncover(self, x, y):
        if (x, y) not in self.known:
            self.known.append((x, y))
        if (x, y) in self.flagged:
            self.flagged.remove((x, y))
    '''
    '''def uncover(self, x, y):
        if (x, y) not in self.known:
            self.known.append((x, y))
            self.known_unchorded
        if (x, y) in self.flagged:
            self.flagged.remove((x, y))
            '''

    #chords a square with full flags
    def vf_chord(self, square):
        if self.get_vf(square[0], square[1]) == 0:
            self.chord_square(square[0], square[1])

    #flags a square where unk., unflagged == vf
    def flag_to_vf(self, square):
        if (self.count_unknown(square[0], square[1]) - self.count_flags(square[0], square[1])) == self.get_vf(square[0], square[1]):
            for sur in self.get_adj_squares(square[0], square[1]):
                if sur not in self.known and sur not in self.flagged:
                    self.flag_square(sur[0], sur[1])

    def click_random(self):
        elig = []
        for x in range(self.width):
            for y in range(self.height):
                if ((x, y) not in self.known) and ((x, y) not in self.flagged):
                    elig.append((x, y))
        if elig:
            square = rand.choice(elig)
            return self.check_square(square[0], square[1])
        return 0

    def one_one(self):
        #find x/y boundaries
        pass

    #compares a board against past format to check if same
    def check_same(r, self):
        newr = self.format()
        if r == newr:
            return 1
        return 0

    def solving_iteration(self):
        initial_state = self.format()
        #for square in (sq for sq in self.known if sq not in self.chorded):
        for square in self.known:
            if square not in self.chorded:
                self.flag_to_vf(square)
                self.vf_chord(square)
        if self.format()==initial_state:
            return 0#no change
        return 1#changed

    def guess(self):
        #final step to improve
        return self.click_random()#this is not the actual final purpose of this function

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

        if board.check_over()==2:
            print("I won!")
        if board.check_over()==1:
            print("I lost.")

        board.reveal_all()
        '''if :
            print("Game over!")

        else:
            print("You won!")'''

        board.printboard()

def new_loop(d):

    board = AI_Board(ms.diff[d][0], ms.diff[d][1], ms.diff[d][2])

    board.click_random()

    while True:
        l = board.solving_iteration()

        while l!=0:
            l = board.solving_iteration()

        if board.check_over()!=0:
            return board.check_over()#1 lost, 2 won

        g = board.guess()

        if board.check_over()!=0:
            return board.check_over()#1 lost, 2 won


def benchmark(num_games):
    records = [[0, 0] for n in range(3)]
    start_time = time.clock()
    for dif in range(len(records)):
        for i in range(num_games):
            records[dif][new_loop(dif)%2]+=1
            if (i+1)%10==0:
                print("diff " + str(dif+1) + ", try " + str(i+1))

    print("records: ", records)
    print("time: ", round((time.clock()-start_time), 3), " seconds")
