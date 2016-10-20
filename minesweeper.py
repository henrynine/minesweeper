#base minesweeper app
import random

diff = {0:(6, 6, 4),
        1:(9, 9, 10),
        2:(16, 16, 40),
        3:(16, 30, 100)}

class Board:

    def __init__(self, h, w, n):

        self.height = h
        self.width = w
        self.num_bombs = n
        self.empty = []
        self.known = []
        self.flagged = []
        self.values = {}

        self.populate()
        self.generate_bombs()
        self.make_values()

    def uncover(self, x, y):
        if (x, y) not in self.known:
            self.known.append((x, y))
        if (x, y) in self.flagged:
            self.flagged.remove((x, y))

    def get_adj_squares(self, x, y):#doesn't loop around
        adj_squares = []
        for xmod in range(-1, 2):
            for ymod in range(-1, 2):
                if (not (xmod==0 and ymod==0)) and x+xmod>=0 and y+ymod>=0 and x+xmod<self.width and y+ymod<self.height:
                    adj_squares.append((x+xmod, y+ymod))
        return adj_squares

    def populate(self):
        for x in range(self.width):
            for y in range(self.height):
                self.empty.append((x, y))


    def reveal_all(self):
        for x in range(self.width):
            for y in range(self.height):
                self.uncover(x, y)

    def generate_bombs(self):
        bcount = self.num_bombs
        while bcount:#if>0
            bsquare = random.choice(self.empty)#pick a random empty square
            self.empty.remove((bsquare[0], bsquare[1]))#add the square
            bcount-=1

    def shift_first(self, x, y):
        for x_index in range(self.width):
            for y_index in range(self.height):
                if (x_index, y_index) in self.empty:
                    self.empty.append((x, y))#mark original space as empty
                    self.empty.remove((x_index, y_index))#mark as bomb
                    self.make_values()
                    return 1

    def make_values(self):
        adj_bomb_count = 0
        for x in range(self.width):
            for y in range(self.height):
                adj_bomb_count = 0
                for square in self.get_adj_squares(x, y):
                    if square not in self.empty:
                        adj_bomb_count+=1
                self.values[(x, y)] = adj_bomb_count

    def check_square(self, x, y):

        first=False
        if len(self.known)==0:
            first=True
        self.uncover(x, y)

        if ((x, y) not in self.empty) and first==False:
            return 0#0=game over
        if (x, y) not in self.empty:#at this point must be first click
            #move bomb to top left, moving right if full
            self.shift_first(x, y)

        #square is at this point known to be empty


        #if no adj bombs, check/click all adjacent unknown squares
        if self.values[(x, y)]==0:
            for square in self.get_adj_squares(x, y):
                if square not in self.known:
                    self.check_square(square[0], square[1])

        return 1#game continues

    def chord_square(self, x, y):#bug: currently duplicates knowns?
        #count adjacent flags
        #if as many flags as values, click all adjacent unflagged
        adj_flags = 0
        for square in self.get_adj_squares(x, y):
            if square in self.flagged:
                adj_flags+=1
        if adj_flags == self.values[(x, y)]:
            for square in self.get_adj_squares(x, y):
                if square not in self.flagged:
                    if self.check_square(square[0], square[1]) == 0:
                        return 0
        return 1

    def flag_square(self, x, y):
        if (x, y) not in self.known:
            self.flagged.append((x, y))
            return 1
        return 0

    def unflag_square(self, x, y):
        if (x, y) in self.flagged:
            self.flagged.remove((x, y))
            return 1
        return 0

    #value - flags, for AI
    def get_vf(self, x, y):
        vf = self.values[(x, y)]
        for square in self.get_adj_squares(x, y):
            if square in self.flagged:
                vf -= 1
        return vf

    #unknown-flags, for AI
    def get_uf(self, x, y):
        uf = 0
        for square in self.get_adj_squares(x, y):
            if not (square in self.flagged or square in self.known):
                uf+=1
        return uf

    #counts flags, for AI
    def count_flags(self, x, y):
        fc = 0
        for square in self.get_adj_squares(x, y):
            if square in self.flagged:
                fc+=1
        return fc

    def count_unknown(self, x, y):
        uc = 0
        for square in self.get_adj_squares(x, y):
            if square not in self.known:
                uc+=1
        return uc

    def check_over(self):#checks if all empty squares are clicked
        for x in range(self.width):
            for y in range(self.height):
                if ((x, y) not in self.empty) and ((x, y) in self.known):
                    return 2#bomb
        for x in range(self.width):
            for y in range(self.height):
                if ((x, y) in self.empty) and ((x, y) not in self.known):
                    return 0#not over
        return 1#won

    #format for printing
    def format(self):
        rows = []
        for xindex in range(self.width):
            row = ''
            for yindex in range(self.height):
                if (xindex, yindex) not in self.known:
                    if (xindex, yindex) not in self.flagged:
                        row += 'X'
                    else:
                        row += 'F'
                elif (xindex, yindex) in self.empty:
                    row+=str(self.values[(xindex, yindex)])
                else:
                    row += 'B'
            rows.append(row)
        return rows

    def printboard(self):
        rows = self.format()
        first = '___'#works up thru 99
        ins = '|||'
        for i in range(self.width):
            first += str(i)
            ins+='|'
        print(first+'\n'+ins)
        for i in range(len(rows)):
            insert = '__'
            if i>9:
                insert = '_'
            print(str(i)+insert+rows[i])
