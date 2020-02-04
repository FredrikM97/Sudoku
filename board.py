from random import sample
from copy import deepcopy
class Board:
    def __init__(self, base=3, procent=70):
        self.base = base
        self.tiles2Remove=procent
        self.side = base**2
        self.area = self.side**2
        self.board = []
        self.SolvedBoard = []

    def run(self):
        model = range(self.base) 

        rows = self.build_side(model)
        cols = self.build_side(model)

        self.board = self.combine_board(rows, cols)
        self.SolvedBoard = deepcopy(self.board)
        self.remove_numbers(self.tiles2Remove)

    def build_side(self, model):
        """
        Used to build rows and columns based on the shuffle function
        """
        
        return [val*self.base + side for val in self.shuffle(model) for side in self.shuffle(model)]

    def combine_board(self, rows, cols):
        """
        Combine two boards using the pattern function in order to decide what value should be at position
        """
        nums  = self.shuffle(range(1,self.base**2+1))
        return [[nums[self.pattern(r,c)] for c in cols] for r in rows]

    def pattern(self, row, column):
        """
        Create pattern for board that gives a valid solution
        """
        return (self.base*(row%self.base) + row//self.base+column)%self.side

    def shuffle(self, size):
        """
        Shuffle input
        """
        return sample(size, len(size))

    def remove_numbers(self, procentage):
        """
        Remove percentage of total area
        """
    
        model = range(self.area)
        cnt_removed_tiles = int(self.area * procentage/100)

        for tile in sample(model, cnt_removed_tiles):
            self.board[tile//self.side][tile%self.side] = 0

    def pretty_prints(self, board):
        tileSize = len(str(self.side))
        x = lambda n: f'{n or ".":{tileSize}}'

        for line in board:
            row = [x(n) for n in line]
            print('['+' '.join(row) + "]")
 
    def check_Solved(self):
        """
        TODO
        """
        pass