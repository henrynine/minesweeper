#base minesweeper app
import random

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
                self.known.append((x, y))

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
        self.known.append((x, y))

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

    def chord_square(self, x, y):
        #count adjacent flags
        #if as many flags as values, click all adjacent unflagged
        adj_flags = 0
        for square in self.get_adj_squares(x, y):
            if square in self.flagged:
                adj_flags+=1
        if adj_flags == self.values[(x, y)]:
            for square in self.get_adj_squares(x, y):
                if square not in self.flagged:
                    self.check_square(square[0], square[1])
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
        for row in rows:
            print(row)