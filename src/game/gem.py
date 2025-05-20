class Gem:
    def __init__(self, color):
        self.color = color

    def is_adjacent(self, other_gem, pos1, pos2):
        # Returns True if pos1 and pos2 are adjacent on the board
        y1, x1 = pos1
        y2, x2 = pos2
        return abs(y1 - y2) + abs(x1 - x2) == 1