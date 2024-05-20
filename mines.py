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
from mines_config import (
    FLAG_MINE,
    HIDDEN,
    MINE,
    BACKROUND_COLOR,
    BUTTONS_GAP,
    BUTTONS_Y,
    TO_BE_REVEALED,
    REVEALED_FACE_COLOR,
    HIDDEN_FACE_COLOR,
    NUN_OF_MINES,
    colors,
)

# set ply font to big for retro look
plt.rcParams.update(
    {"font.family": "monospace", "font.size": 18, "font.weight": "bold"}
)


class Cell:
    """
    Class representing a cell in the Minesweeper grid
    """

    def __init__(self, value=0):
        """
        Initialize the cell with a value
        """
        self.value = value
        self.hidden = True
        self.flagged = False

    def __repr__(self):
        """
        Return a string representation of the cell
        """
        if self.flagged:
            return FLAG_MINE
        if self.hidden:
            return HIDDEN
        if self.value == MINE:
            return MINE
        return str(self.value)

    def is_mine(self):
        """
        Check if the cell is a mine
        """
        return self.value == MINE

    def is_empty(self):
        """
        Check if the cell is empty
        """
        return self.value == 0

    def reveal(self):
        """
        Reveal the cell
        """
        self.hidden = False

    def flag(self):
        """
        Flag the cell
        """
        self.flagged = not self.flagged

    def __int__(self):
        return self.value


class Minesweeper:
    """
    Class representing the Minesweeper game
    """

    def __init__(self, grid_size=(16, 30)):
        """
        Initialize the Minesweeper game with a grid size
        """
        self.grid_size = grid_size
        self.grid = self.create_grid()
        self.visible_grid = copy.deepcopy(self.grid)
        self.last_visible_grid = None
        self.fig, self.ax = plt.subplots()
        self.generate_background()
        self.cmap = ListedColormap(["lightgrey", "white"], name="minesweeper", N=2)
        self.img = self.ax.imshow(
            np.zeros(grid_size),
            cmap=self.cmap,
            interpolation="nearest",
            animated=True,
            aspect="equal",  # set aspect to 'equal' to maintain grid proportions
            origin="upper",
        )
        self.fig.set_size_inches(16, 10)
        self.ax.set_title("Minesweeper")
        self.ax.set_axis_off()
        self.init_grid()
        self.draw_grid()
        self.setup_buttons()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.update_grid()
        # plt.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Remove padding

        # Center the grid in the window
        self.ax.set_xlim(-0.5, grid_size[1] - 0.5)
        self.ax.set_ylim(grid_size[0] - 0.5, -0.5)

    def create_grid(self):
        """
        Create a grid of cells
        """
        return [
            [Cell() for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])
        ]

    def generate_background(self):
        """
        Generate a gradient background for the game
        """
        # Create a gradient image
        gradient = np.linspace(0, 1, 256)  # generate gradient
        gradient = np.vstack((gradient, gradient))  # stack to create 2D array
        # Create a full-figure axis for the gradient background
        bg_ax = self.fig.add_axes([0, 0, 1, 1], zorder=-1)  # full figure axis
        bg_ax.imshow(
            gradient,
            aspect="auto",
            cmap="YlGnBu",
            extent=[0, self.grid_size[1], 0, self.grid_size[0]],
        )
        bg_ax.axis("Tight")

    def init_grid(self):
        """
        Initialize the grid with mines and numbers
        """
        mines = self.generate_mines()
        self.populate_grid_with_mines(mines)

    def generate_mines(self):
        """
        Generate mines in the grid
        """
        mines = np.zeros(self.grid_size, dtype=np.int8)
        num_mines = NUN_OF_MINES
        mine_indices = np.random.choice(
            self.grid_size[0] * self.grid_size[1], num_mines, replace=False
        )
        mines[np.unravel_index(mine_indices, self.grid_size)] = 1
        return mines

    def populate_grid_with_mines(self, mines):
        """
        Populate the grid with mines and numbers
        """
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if mines[i, j] == 1:
                    self.grid[i][j].value = MINE  # Corrected mine value
                    self.increment_surrounding_cells(i, j)

    def increment_surrounding_cells(self, i, j):
        """
        Increment the value of surrounding cells
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                if 0 <= i + x < self.grid_size[0] and 0 <= j + y < self.grid_size[1]:
                    if self.grid[i + x][j + y].value != MINE:
                        self.grid[i + x][j + y].value += 1

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
            [start[0], end[0]], [start[1], end[1]], color=color, linewidth=linewidth
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
            (self.grid_size[1] - offset, -offset),
            (self.grid_size[1] - offset, self.grid_size[0] - offset),
            (-offset, self.grid_size[0] - offset),
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

        Parameters:
        - offset: float, the offset to center the grid
        """
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid[i][j].hidden:
                    self.draw_unrevealed_cell(i, j)
                else:
                    self.draw_revealed_cell(i, j)

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
            self.win_game()

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
        return 0 <= i < self.grid_size[0] and 0 <= j < self.grid_size[1]

    def win_game(self):
        print("You won the game!")
        self.fig.set_facecolor("green")

    def show_all_mines(self):
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid[i][j].is_mine():
                    self.grid[i][j].reveal()

    def check_win(self):
        """
        Check if the game is won
        """
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if not self.grid[i][j].is_mine() and self.grid[i][j].hidden:
                    return False
        return True

    def update_grid(self):
        """
        Update the grid display
        """
        self.ax.clear()
        status = f"Marked: {sum(1 for row in self.grid for cell in row if cell.flagged)} / {sum(1 for row in self.grid for cell in row if cell.is_mine())}"
        self.ax.set_title(status)
        grid_display = np.array(
            [[cell.hidden is False for cell in row] for row in self.grid],
            dtype=np.float32,
        )
        self.img = self.ax.imshow(
            grid_display,
            cmap=self.cmap,
            interpolation="nearest",
            animated=True,
            aspect="equal",
            origin="upper",
        )
        self.ax.set_axis_off()
        self.draw_grid()

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if 0 < self.grid[i][j].value < MINE and not self.grid[i][j].hidden:
                    color = colors.get(self.grid[i][j].value, "black")
                    self.ax.text(
                        j,
                        i,
                        str(self.grid[i][j].value),
                        ha="center",
                        va="center",
                        color=color,
                    )
                elif self.grid[i][j].flagged:
                    self.ax.text(j, i, "⚑", ha="center", va="center", color="black")
                elif self.grid[i][j].is_mine() and not self.grid[i][j].hidden:
                    self.ax.text(j, i, "☠", ha="center", va="center", color="black")

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
            if event.button == 1: # left click
                self.reveal_cell(i, j)
            elif event.button == 3: # right click
                self.flag_cell(i, j)
            self.update_grid()

    def setup_buttons(self):
        """
        Setup the buttons for the game
        """
        button_width = self.grid_size[1] / 8
        # start under the grid buttom left
        buttun_start_x = self.grid_size[1] / 2 - 2 * button_width
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
                    pos / self.grid_size[1] + BUTTONS_GAP,
                    BUTTONS_Y,
                    button_width / self.grid_size[1],
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
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if next_visible_grid[i][j] == TO_BE_REVEALED:
                    self.grid[i][j].hidden = False
                elif next_visible_grid[i][j] == "F":
                    self.grid[i][j].flagged = True
        self.update_grid()

    def next_day(self, event):
        """
        Apply the rules of Minesweeper to update the visible grid one step
        """
        self.last_visible_grid = copy.deepcopy(self.grid)
        board = [
            ["_" for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])
        ]
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid[i][j].flagged:
                    board[i][j] = "F"
                elif not self.grid[i][j].hidden:
                    board[i][j] = str(self.grid[i][j].value)
            board.append([])
        self.apply_rules(board)

    def reset_game(self, event):
        """
        Reset the game
        """
        self.fig.set_facecolor(BACKROUND_COLOR)
        self.grid = self.create_grid()
        self.visible_grid = copy.deepcopy(self.grid)
        self.last_visible_grid = None
        self.init_grid()
        self.update_grid()

    def give_hint(self, event):
        """
        Give a hint by revealing a random hidden cell
        """
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if not self.grid[i][j].is_mine() and self.grid[i][j].hidden:
                    self.reveal_cell(i, j)
                    break
        self.update_grid()

    def run(self):
        """
        Run the Minesweeper game
        """
        plt.show()


class MinesweeperRules:
    """
    Class representing the rules of Minesweeper as a cellular automaton
    """

    def __init__(self, visible_grid):
        # generate a grid of hidden cells and revealed cells
        self.grid_size = (len(visible_grid), len(visible_grid[0]))
        self.visible_grid = visible_grid

    def transition(self):
        """
        Apply the rules of Minesweeper to update the visible grid one step
        """
        for i in range(len(self.visible_grid)):
            for j in range(len(self.visible_grid[i])):
                print(self.visible_grid[i][j], end=" ")
            print()
        next_grid = copy.deepcopy(self.visible_grid)
        for i in range(len(self.visible_grid)):
            for j in range(len(self.visible_grid[i])):
                if self.visible_grid[i][j] != "F" and self.visible_grid[i][j] != "_":
                    self.apply_rules(i, j, next_grid)
        return next_grid

    def apply_rules(self, i, j, next_grid):
        """
        Apply the rules of Minesweeper to update the visible grid at cell (i, j)

        Parameters:
        - i: int, the row index of the cell
        - j: int, the column index of the cell
        - next_grid: list, the next visible grid
        """
        neighborhood = self.get_neighborhood(i, j)
        mines_on_neighbors = sum(1 for cell in neighborhood if cell == "F")
        hidden_cells = sum(1 for cell in neighborhood if cell == "_")

        # Get the value of the current cell
        cell_value = int(self.visible_grid[i][j])

        # Rule 1: Flag cells if hidden_cells + mines_on_neighbors equals the cell value
        if hidden_cells + mines_on_neighbors == cell_value:
            for ni, nj in self.get_neighborhood_indices(i, j):
                if self.visible_grid[ni][nj] == "_":
                    print(f"Flagging cell ({ni}, {nj})")
                    next_grid[ni][nj] = "F"

        for ni, nj in self.get_neighborhood_indices(i, j):
            if self.visible_grid[ni][nj] != "F" and self.visible_grid[ni][nj] != "_":
                # check if the other cell has enough mines around it
                neighborhood = self.get_neighborhood(ni, nj)
                mines_on_neighbors = sum(1 for cell in neighborhood if cell == "F")
                if mines_on_neighbors == int(self.visible_grid[ni][nj]):
                    for nni, nnj in self.get_neighborhood_indices(ni, nj):
                        if self.visible_grid[nni][nnj] == "_":
                            next_grid[nni][nnj] = TO_BE_REVEALED

    def get_neighborhood(self, i, j):
        """
        Get the neighborhood of a cell at (i, j)

        Parameters:
        - i: int, the row index of the cell
        - j: int, the column index of the cell

        Returns:
        - list, the neighborhood of the cell
        """
        neighborhood = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                ni, nj = i + x, j + y
                if 0 <= ni < len(self.visible_grid) and 0 <= nj < len(
                    self.visible_grid[ni]
                ):
                    neighborhood.append(self.visible_grid[ni][nj])
        return neighborhood

    def get_neighborhood_indices(self, i, j):
        """
        Get the indices of the neighborhood of a cell at (i, j)

        Parameters:
        - i: int, the row index of the cell
        - j: int, the column index of the cell

        Returns:
        - list, the indices of the neighborhood of the cell
        """
        indices = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                ni, nj = i + x, j + y
                if 0 <= ni < len(self.visible_grid) and 0 <= nj < len(
                    self.visible_grid[ni]
                ):
                    indices.append((ni, nj))
        return indices


if __name__ == "__main__":
    grid_size = (16, 16)
    game = Minesweeper(grid_size)
    game.run()
