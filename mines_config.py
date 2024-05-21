"""
This file contains the configuration of the minesweeper game
"""

DEFAULT_GRID_SIZE = (16, 16)
FLAG_MINE = "F"
MAYBE_MINE = "M"
HIDDEN = "H"
BLANK = "B"
# value of a mine 10 is chosed because cell value is 0-8, 9 is confusing
MINE = 10
BACKROUND_COLOR = (220 / 255, 219 / 255, 214 / 255)
GREY = (149 / 255, 151 / 255, 150 / 255)
BUTTONS_GAP = 0.013
BUTTONS_Y = 0.05
TO_BE_REVEALED = "X"
REVEALED_FACE_COLOR = (208 / 255, 208 / 255, 204 / 255)
HIDDEN_FACE_COLOR = (220 / 255, 219 / 255, 214 / 255)
# number of hidden mines placed in the grid
NUN_OF_MINES = 40
# colors for the numbers
colors = {
    1: "blue",
    2: "green",
    3: "goldenrod",  # darke yellow
    4: "orange",
    5: "red",
    6: "purple",
    7: "brown",
    8: "black",
    10: "black",
    11: "black",
    12: "black",
}
