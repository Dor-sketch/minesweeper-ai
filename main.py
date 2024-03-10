"""
This is the main file for the Cross Game of Life.
"""

from game import GameOfLife

if __name__ == "__main__":
    grid_size = (32, 32)
    game = GameOfLife(grid_size)
    game.run()
