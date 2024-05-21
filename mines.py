"""
Minesweeper game with a GUI interface using matplotlib and numpy
Inspired by the Minesweeper game from Microsoft Windows
Includes a reset button, a hint button, a next button, and an undo button

- The next button applies the rules of Minesweeper to reveal hidden cells
based on a costum rule set inspired by Conway's Game of Life
- The undo button undoes the last move
- The hint button reveals a random hidden cell
- The reset button resets the game

The game ends when a mine is hit or all non-mine cells are revealed
The game is won when all non-mine cells are revealed
"""

import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Button
from matplotlib import patches
from utils import generate_background
from mines_config import (
    MINE,
    BACKROUND_COLOR,
    BUTTONS_GAP,
    BUTTONS_Y,
    FLAG_MINE,
    TO_BE_REVEALED,
    REVEALED_FACE_COLOR,
    HIDDEN_FACE_COLOR,
    NUN_OF_MINES,
    DEFAULT_GRID_SIZE,
    colors,
)

from mines_cell import Cell, MinesweeperRules

# set ply font to big for retro look
plt.rcParams.update(
    {"font.family": "monospace", "font.size": 18, "font.weight": "bold"}
)


class Minesweeper:
    """
    Class representing the Minesweeper game
    """

    def __init__(self, grid_size=DEFAULT_GRID_SIZE, n_mines=NUN_OF_MINES):
        """
        Initialize the Minesweeper game with a grid size
        """
        self.grid = self.init_grid(grid_size, n_mines)
        self.visible_grid = copy.deepcopy(self.grid)
        self.last_visible_grid = None
        self.fig, self.ax = plt.subplots()
        generate_background(self.fig, self.grid)
        self.cmap = ListedColormap(
            ["lightgrey", "white"], name="minesweeper", N=2)
        self.fig.set_size_inches(grid_size[1] / 2, grid_size[0] / 2)
        self.ax.set_title("Minesweeper")
        # make grid cells symetric fix aspect ratio of square cells
        self.ax.set_aspect("equal")
        # prevent changing the axis ratio
        self.ax.set_axis_off()
        self.draw_grid()
        self.setup_buttons()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.update_grid()
        # optional - Remove padding around the grid
        # plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

        # Center the grid in the window
        self.ax.set_xlim(-0.5, grid_size[1] - 0.5)
        self.ax.set_ylim(grid_size[0] - 0.5, -0.5)

    def init_grid(self, grid_size=DEFAULT_GRID_SIZE, n_mines=NUN_OF_MINES):
        """
        Initialize the grid with mines and numbers
        """
        grid = [[Cell() for _ in range(grid_size[1])]
                for _ in range(grid_size[0])]
        mines = self.generate_mines(grid_size, n_mines)
        self.populate_grid_with_mines(mines, grid)
        return grid

    def generate_mines(self, grid_size=DEFAULT_GRID_SIZE, num_mines=NUN_OF_MINES):
        """
        Generate mines in the grid
        """
        mines = np.zeros(grid_size, dtype=np.int8)
        mine_indices = np.random.choice(
            grid_size[0] * grid_size[1], num_mines, replace=False
        )
        mines[np.unravel_index(mine_indices, grid_size)] = 1
        return mines

    def populate_grid_with_mines(self, mines, grid):
        """
        Populate the grid with mines and numbers
        """
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if mines[i][j]:
                    cell.value = MINE
                    self.increment_surrounding_cells(i, j, grid)

    def increment_surrounding_cells(self, i, j, grid):
        """
        Increment the value of surrounding cells
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                if 0 <= i + x < len(grid) and 0 <= j + y < len(grid[0]):
                    if grid[i + x][j + y].value != MINE:
                        grid[i + x][j + y].value += 1

    def draw_line_with_shadow(self, start, end, color="black", linewidth=1):
        """
        Draw a line with a shadow effect

        Parameters:
        - start: tuple, the start point of the line
        - end: tuple, the end point of the line
        - color: str, the color of the line
        - linewidth: int, the width of the line
        """
        self.ax.plot(
            [start[0], end[0]], [start[1], end[1]
                                 ], color=color, linewidth=linewidth
        )

    def draw_revealed_cell(self, i, j):
        """
        Draw a revealed cell in the grid

        Parameters:
        - i: int, the row index of the cell
        - j: int, the column index of the cell
        """
        # Draw the cell
        self.ax.add_patch(
            patches.Rectangle(
                (j - 0.5, i - 0.5),
                1,
                1,
                edgecolor="none",
                facecolor=REVEALED_FACE_COLOR,
                linewidth=1,
            )
        )

        # Draw the top and left edges (darker for sunken effect)
        self.draw_line_with_shadow(
            (j - 0.5, i - 0.5), (j + 0.5, i - 0.5), color="grey", linewidth=1
        )
        self.draw_line_with_shadow(
            (j - 0.5, i - 0.5), (j - 0.5, i + 0.5), color="grey", linewidth=1
        )

        # Draw the bottom and right edges (lighter for sunken effect)
        self.draw_line_with_shadow(
            (j - 0.5, i + 0.5), (j + 0.5, i + 0.5), color="white", linewidth=1
        )
        self.draw_line_with_shadow(
            (j + 0.5, i - 0.5), (j + 0.5, i + 0.5), color="white", linewidth=1
        )

    def draw_unrevealed_cell(self, i, j):
        """
        Draw an unrevealed cell in the grid

        Parameters:
        - i: int, the row index of the cell
        - j: int, the column index of the cell
        """
        # Draw the cell
        self.ax.add_patch(
            patches.Rectangle(
                (j - 0.5, i - 0.5),
                1,
                1,
                edgecolor="none",
                facecolor=HIDDEN_FACE_COLOR,
                linewidth=0,
            )
        )

        # Draw the top and left edges (lighter for raised effect)
        self.draw_line_with_shadow(
            (j - 0.5, i - 0.5), (j + 0.5, i - 0.5), color="white", linewidth=1
        )
        self.draw_line_with_shadow(
            (j - 0.5, i - 0.5), (j - 0.5, i + 0.5), color="white", linewidth=1
        )

        # Draw the bottom and right edges (darker for raised effect)
        self.draw_line_with_shadow(
            (j - 0.5, i + 0.5), (j + 0.5, i + 0.5), color="grey", linewidth=1
        )
        self.draw_line_with_shadow(
            (j + 0.5, i - 0.5), (j + 0.5, i + 0.5), color="grey", linewidth=1
        )

    def draw_3d_frame(self, offset=0.5):
        """
        Draw a 3D frame around the entire grid.
        """
        # Coordinates of the outer frame
        frame_points = [
            (-offset, -offset),
            (len(self.grid[0]) - offset, -offset),
            (len(self.grid[0]) - offset, len(self.grid) - offset),
            (-offset, len(self.grid) - offset),
            (-offset, -offset),
        ]

        # Draw the top and left edges (lighter for raised effect)
        self.draw_line_with_shadow(
            frame_points[0], frame_points[1], color="white", linewidth=2
        )
        self.draw_line_with_shadow(
            frame_points[0], frame_points[3], color="white", linewidth=2
        )

        # Draw the bottom and right edges (darker for raised effect)
        self.draw_line_with_shadow(
            frame_points[1], frame_points[2], color="grey", linewidth=2
        )
        self.draw_line_with_shadow(
            frame_points[3], frame_points[2], color="grey", linewidth=2
        )

    def draw_grid(self):
        """
        Draw the grid lines with 3D-like buttons, using an offset to center the grid
        """
        draw_unrevealed_cell = self.draw_unrevealed_cell
        draw_revealed_cell = self.draw_revealed_cell
        grid = self.grid
        grid_size_0 = len(self.grid)
        grid_size_1 = len(self.grid[0])

        for i in range(grid_size_0):
            for j in range(grid_size_1):
                cell = grid[i][j]
                if cell.hidden:
                    draw_unrevealed_cell(i, j)
                else:
                    draw_revealed_cell(i, j)

        # Draw the 3D frame around the grid
        self.draw_3d_frame()

    def reveal_cell(self, i, j):
        """
        Reveal a cell in the grid

        Parameters:
        - i: int, the row index of the cell
        - j: int, the column index of the cell
        """
        if self.grid[i][j].is_mine():
            self.end_game(i, j)
            return
        self.update_last_visible_grid()
        self.grid[i][j].reveal()

        if self.grid[i][j].is_empty():
            self.reveal_surrounding_cells(i, j)

        if self.check_win():
            print("You won the game!")
            self.fig.set_facecolor("green")

    def flag_cell(self, i, j):
        """
        Flag a cell in the grid
        """
        self.update_last_visible_grid()
        if self.grid[i][j].hidden:
            self.grid[i][j].flag()

    def unflag_cell(self, i, j):
        """
        Unflag a cell in the grid
        """
        self.update_last_visible_grid()
        if self.grid[i][j].flagged:
            self.grid[i][j].flagged = False

    def end_game(self, i, j):
        """
        End the game when a mine is hit

        Parameters:
        - i: int, the row index of the cell
        - j: int, the column index of the cell
        """
        print(f"Game Over! You hit a mine on cell ({i}, {j})")
        self.grid[i][j].value = MINE
        self.fig.set_facecolor("red")
        self.show_all_mines()
        self.fig.canvas.draw_idle()

    def update_last_visible_grid(self):
        """
        Update the last visible grid
        """
        self.last_visible_grid = copy.deepcopy(self.grid)

    def reveal_surrounding_cells(self, i, j):
        """
        Reveal the surrounding cells of a cell

        Parameters:
        - i: int, the row index of the cell
        - j: int, the column index of the cell
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                ni, nj = i + x, j + y
                if self.is_valid_cell(ni, nj) and self.grid[ni][nj].hidden:
                    self.reveal_cell(ni, nj)

    def is_valid_cell(self, i, j):
        """
        Check if the cell indices are valid

        Parameters:
        - i: int, the row index of the cell
        - j: int, the column index of the cell
        """
        return 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0])

    def show_all_mines(self):
        """
        Show all the mines in the grid
        """
        for row in self.grid:
            for cell in row:
                if cell.is_mine():
                    cell.hidden = False

    def check_win(self):
        """
        Check if the game is won
        """
        for row in self.grid:
            for cell in row:
                if not cell.is_mine() and cell.hidden:
                    return False
        return True

    def update_grid(self):
        """
        Update the grid display
        """
        self.ax.clear()
        status = (
            f"Marked: {sum(1 for row in self.grid for cell in row if cell.flagged)}"
            f" / {sum(1 for row in self.grid for cell in row if cell.is_mine())}"
        )
        self.ax.set_title(status)

        self.ax.set_axis_off()
        self.draw_grid()
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if 0 < cell.value < MINE and not cell.hidden:
                    color = colors.get(cell.value, "black")
                    self.ax.text(
                        j,
                        i,
                        str(cell.value),
                        ha="center",
                        va="center",
                        color=color,
                    )
                elif cell.flagged:
                    self.ax.text(j, i, "⚑", ha="center",
                                 va="center", color="black")
                elif cell.is_mine() and not cell.hidden:
                    self.ax.text(j, i, "☠", ha="center",
                                 va="center", color="black")

        self.fig.canvas.draw_idle()

    def on_click(self, event):
        """
        Handle the mouse click event

        Parameters:
        - event: event, the mouse click event
        """
        if event.xdata is None or event.ydata is None:
            return

        # check if pressed on a button
        for button in self.buttons:
            if event.inaxes == button.ax:
                return  # button click handled elsewhere

        i, j = round(event.ydata), round(event.xdata)

        if self.is_valid_cell(i, j):
            if event.button == 1:  # left click
                self.reveal_cell(i, j)
            elif event.button == 3:  # right click
                self.flag_cell(i, j)
            self.update_grid()

    def setup_buttons(self):
        """
        Setup the buttons for the game
        """
        button_width = len(self.grid[0]) / 8
        # start under the grid buttom left
        buttun_start_x = len(self.grid[0]) / 2 - 2 * button_width
        button_positions = [
            buttun_start_x,
            buttun_start_x + button_width,
            buttun_start_x + 2 * button_width,
            buttun_start_x + 3 * button_width,
        ]
        button_labels = ["Reset", "Hint", "Next", "Undo"]
        button_colors = ["green", "orange", "blue", "red"]

        self.buttons = []
        for pos, label, color in zip(button_positions, button_labels, button_colors):
            ax = plt.axes(
                [
                    pos / len(self.grid[0]) + BUTTONS_GAP,
                    BUTTONS_Y,
                    button_width / len(self.grid[0]),
                    0.05,
                ]
            )
            button = Button(ax, label, color=color, hovercolor="lightblue")
            button.label.set_fontsize("large")
            self.buttons.append(button)

        self.buttons[0].on_clicked(self.reset_game)
        self.buttons[1].on_clicked(self.give_hint)
        self.buttons[2].on_clicked(self.next_day)
        self.buttons[3].on_clicked(self.undo_last_move)

    def undo_last_move(self, event):
        """
        Undo the last move
        """
        if self.last_visible_grid:
            self.grid = copy.deepcopy(self.last_visible_grid)
            self.update_grid()
            self.fig.canvas.draw_idle()

    def apply_rules(self, board):
        """
        Apply the rules of Minesweeper to update the visible grid one step
        """
        rules = MinesweeperRules(board)
        next_visible_grid = rules.transition()
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if next_visible_grid[i][j] == TO_BE_REVEALED:
                    cell.hidden = False
                elif next_visible_grid[i][j] == FLAG_MINE:
                    cell.flagged = True
        self.update_grid()

    def next_day(self, event):
        """
        Apply the rules of Minesweeper to update the visible grid one step
        """
        self.last_visible_grid = copy.deepcopy(self.grid)
        board = [
            ["_" for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))
        ]
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell.flagged:
                    board[i][j] = FLAG_MINE
                elif not cell.hidden:
                    board[i][j] = str(cell.value)
            board.append([])
        self.apply_rules(board)

    def reset_game(self, event):
        """
        Reset the game
        """
        self.fig.set_facecolor(BACKROUND_COLOR)
        self.grid = self.init_grid()
        self.visible_grid = copy.deepcopy(self.grid)
        self.last_visible_grid = None
        self.update_grid()

    def give_hint(self, event):
        """
        Give a hint by revealing a random hidden cell
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if not self.grid[i][j].is_mine() and self.grid[i][j].hidden:
                    self.reveal_cell(i, j)
                    break
        self.update_grid()

    def run(self):
        """
        Run the Minesweeper game
        """
        plt.show()


if __name__ == "__main__":
    s = (16, 16)
    game = Minesweeper(s)
    game.run()
