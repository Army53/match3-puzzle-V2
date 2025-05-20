# src/game/utils.py

import random

def generate_random_gem_color():
    colors = ['red', 'green', 'blue', 'yellow', 'purple']
    return random.choice(colors)

def validate_initial_board_setup(board):
    red_count = sum(gem.color == 'red' for row in board for gem in row)
    green_count = sum(gem.color == 'green' for row in board for gem in row)
    return red_count <= 3 and green_count <= 3