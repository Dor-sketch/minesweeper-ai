"""
This file contains the configuration of the minesweeper game
"""

colors = {
    1: "blue",
    2: "darkgreen",
    3: "darkgoldenrod",
    4: "darkorange",
    5: "darkred",
    6: "darkpurple",
    7: "brown",
    8: "black",
    10: "black",
    11: "black",
    12: "black",
}


# Game settings
DEFAULT_GRID_SIZE = (16, 30)
NUM_OF_MINES = 99
FLAG_MINE = "F"
MAYBE_MINE = "M"
HIDDEN = "H"
BLANK = "B"
MINE = 10
TO_BE_REVEALED = "X"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GREY = (211, 211, 211)
DARK_GREY = (169, 169, 169)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
BACKROUND_COLOR = (255, 255, 255)
REVEALED_FACE_COLOR = (220, 220, 220)
HIDDEN_FACE_COLOR = (220, 220, 220)


# Button settings
BUTTONS_GAP = 0.013
BUTTONS_Y = 0.05
BUTTONS_HEIGHT = 0.05
BUTTONS_WIDTH = 0.15


# Game variables
NUM_MINES = NUM_OF_MINES
