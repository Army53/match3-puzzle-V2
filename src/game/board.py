import random
from .gem import Gem

class Board:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.grid = self.initialize_board()

    def initialize_board(self):
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
        board = [[None for _ in range(self.width)] for _ in range(self.height)]
        red_count = 0
        green_count = 0

        for y in range(self.height):
            for x in range(self.width):
                color = random.choice(colors)
                if color == 'red' and red_count < 3:
                    red_count += 1
                elif color == 'green' and green_count < 3:
                    green_count += 1
                else:
                    while color == 'red' and red_count >= 3:
                        color = random.choice(colors)
                    while color == 'green' and green_count >= 3:
                        color = random.choice(colors)

                board[y][x] = Gem(color)

        return board

    def swap_gems(self, pos1, pos2):
        gem1 = self.grid[pos1[1]][pos1[0]]
        gem2 = self.grid[pos2[1]][pos2[0]]
        self.grid[pos1[1]][pos1[0]], self.grid[pos2[1]][pos2[0]] = gem2, gem1

    def check_for_matches(self):
        matches = set()
        # Check rows
        for y in range(self.height):
            for x in range(self.width - 2):
                c = self.grid[y][x].color
                if c == self.grid[y][x+1].color == self.grid[y][x+2].color:
                    matches.update([(y, x), (y, x+1), (y, x+2)])
        # Check columns
        for x in range(self.width):
            for y in range(self.height - 2):
                c = self.grid[y][x].color
                if c == self.grid[y+1][x].color == self.grid[y+2][x].color:
                    matches.update([(y, x), (y+1, x), (y+2, x)])
        return matches

    def update_board(self):
        # Remove matches and let gems fall down, fill new gems
        while True:
            matches = self.check_for_matches()
            if not matches:
                break
            for y, x in matches:
                self.grid[y][x] = None
            for x in range(self.width):
                col = [self.grid[y][x] for y in range(self.height) if self.grid[y][x] is not None]
                col = [Gem(random.choice(['red','green','blue','yellow','purple','orange'])) for _ in range(self.height-len(col))] + col
                for y in range(self.height):
                    self.grid[y][x] = col[y]