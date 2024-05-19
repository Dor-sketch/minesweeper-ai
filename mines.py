import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Button
import copy

FLAG_MINE = 'F'
MAYBE_MINE = 'M'
HIDDEN = 'H'
BLANK = 'B'
MINE = 'X'

class Cell:
    def __init__(self, value=0):
        self.value = value
        self.hidden = True
        self.flagged = False

    def __repr__(self):
        if self.flagged:
            return "F"
        if self.hidden:
            return "H"
        if self.flagged:
            return "F"
        if self.value == 10:
            return "X"
        return str(self.value)

    def is_mine(self):
        return self.value == 10

    def is_empty(self):
        return self.value == 0

    def reveal(self):
        self.hidden = False

    def flag(self):
        self.flagged = not self.flagged

    def __int__(self):
        return self.value


class Minesweeper:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = self.create_grid()
        self.visible_grid = copy.deepcopy(self.grid)
        self.last_visible_grid = None
        self.fig, self.ax = plt.subplots()
        self.cmap = ListedColormap(["grey", "white"], name="minesweeper", N=2)
        self.img = self.ax.imshow(np.zeros(grid_size), cmap=self.cmap, interpolation="nearest", animated=True, aspect="equal", origin="upper")
        # make window bigger
        self.fig.set_size_inches(8, 8)
        self.ax.set_title("Minesweeper")
        self.ax.set_axis_off()
        self.draw_grid()
        self.setup_buttons()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.init_grid()
        self.update_grid()

    def create_grid(self):
        return [[Cell() for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]

    def init_grid(self):
        mines = self.generate_mines()
        self.populate_grid_with_mines(mines)

    def generate_mines(self):
        mines = np.zeros(self.grid_size, dtype=np.int8)
        num_mines = 40
        mine_indices = np.random.choice(self.grid_size[0] * self.grid_size[1], num_mines, replace=False)
        mines[np.unravel_index(mine_indices, self.grid_size)] = 1
        return mines

    def populate_grid_with_mines(self, mines):
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if mines[i, j] == 1:
                    self.grid[i][j].value = 10  # Corrected mine value
                    self.increment_surrounding_cells(i, j)

    def increment_surrounding_cells(self, i, j):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if 0 <= i + x < self.grid_size[0] and 0 <= j + y < self.grid_size[1]:
                    if self.grid[i + x][j + y].value != 10:
                        self.grid[i + x][j + y].value += 1

    def draw_grid(self):
        for i in range(self.grid_size[0]):
            self.ax.plot([-0.5, self.grid_size[1] - 0.5], [i - 0.5, i - 0.5], color="black")
        for j in range(self.grid_size[1]):
            self.ax.plot([j - 0.5, j - 0.5], [-0.5, self.grid_size[0] - 0.5], color="black")

    def reveal_cell(self, i, j):
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
        self.update_last_visible_grid()
        if self.grid[i][j].hidden:
            self.grid[i][j].flag()

    def unflag_cell(self, i, j):
        self.update_last_visible_grid()
        if self.grid[i][j].flagged:
            self.grid[i][j].flagged = False

    def end_game(self, i, j):
        print(f"Game Over! You hit a mine on cell ({i}, {j})")
        self.grid[i][j].value = 100
        self.fig.set_facecolor("red")
        self.show_all_mines()
        self.fig.canvas.draw_idle()

    def update_last_visible_grid(self):
        self.last_visible_grid = copy.deepcopy(self.grid)

    def reveal_surrounding_cells(self, i, j):
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
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if not self.grid[i][j].is_mine() and self.grid[i][j].hidden:
                    return False
        return True

    def update_grid(self):
        self.ax.clear()
        status = f'Flags: {sum(1 for row in self.grid for cell in row if cell.flagged)} out of {sum(1 for row in self.grid for cell in row if cell.is_mine())}'
        self.ax.set_title(status)
        grid_display = np.array([[cell.hidden == False for cell in row] for row in self.grid], dtype=np.float32)
        self.img = self.ax.imshow(grid_display, cmap=self.cmap, interpolation="nearest", animated=True, aspect="equal", origin="upper")
        self.ax.set_axis_off()
        self.draw_grid()
        colors = {1: 'blue', 2: 'green', 3: 'yellow', 4: 'orange', 5: 'red', 6: 'purple', 7: 'brown', 8: 'black', 10: 'black', 11: 'black', 12: 'black'}
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if 0 < self.grid[i][j].value < 10 and not self.grid[i][j].hidden:
                    color = colors.get(self.grid[i][j].value, 'black')
                    self.ax.text(j, i, str(self.grid[i][j].value), ha='center', va='center', color=color)
                elif self.grid[i][j].flagged:
                    self.ax.text(j, i, "⚑", ha='center', va='center', color='black')
                elif self.grid[i][j].value == 100:
                    self.ax.text(j, i, "☠", ha='center', va='center', color='black')

        self.fig.canvas.draw_idle()
    def on_click(self, event):
        if event.xdata is None or event.ydata is None:
            return

        # check if pressed on a button
        for button in self.buttons:
            if event.inaxes == button.ax:
                return  # button click handled elsewhere

        i, j = round(event.ydata), round(event.xdata)

        if self.is_valid_cell(i, j):
            if event.button == 1:
                self.reveal_cell(i, j)
            elif event.button == 3:
                self.flag_cell(i, j)
            self.update_grid()

    def setup_buttons(self):
        button_positions = [0.1, 0.2, 0.3, 0.4]
        button_labels = ["Reset", "Hint", "Next", "Undo"]
        button_colors = ["green", "orange", "blue", "red"]

        self.buttons = []
        for pos, label, color in zip(button_positions, button_labels, button_colors):
            ax = plt.axes([pos, 0.01, 0.1, 0.05])
            button = Button(ax, label, color=color, hovercolor='lightblue')
            button.label.set_fontsize('large')
            self.buttons.append(button)

        self.buttons[0].on_clicked(self.reset_game)
        self.buttons[1].on_clicked(self.give_hint)
        self.buttons[2].on_clicked(self.next_day)
        self.buttons[3].on_clicked(self.undo_last_move)

    def undo_last_move(self, event):
        if self.last_visible_grid:
            self.fig.set_facecolor("white")
            self.grid = copy.deepcopy(self.last_visible_grid)
            self.update_grid()
            self.fig.canvas.draw_idle()

    def apply_rules(self):
        rules = MinesweeperRules(copy.deepcopy(self.grid))
        next_visible_grid = rules.transition()
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if next_visible_grid[i][j].hidden == False:
                    self.grid[i][j].hidden = False
                elif next_visible_grid[i][j].flagged:
                    self.grid[i][j].flagged = True
        self.update_grid()

    def next_day(self, event):
        self.last_visible_grid = copy.deepcopy(self.grid)
        self.apply_rules()

    def reset_game(self, event):
        self.fig.set_facecolor("white")
        self.grid = self.create_grid()
        self.visible_grid = copy.deepcopy(self.grid)
        self.last_visible_grid = None
        self.init_grid()
        self.update_grid()

    def give_hint(self, event):
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if not self.grid[i][j].is_mine() and self.grid[i][j].hidden:
                    self.reveal_cell(i, j)
                    break
        self.update_grid()

    def run(self):
        plt.show()


class MinesweeperRules:
    def __init__(self, visible_grid):
        # generate a grid of hidden cells and revealed cells
        self.grid_size = (len(visible_grid), len(visible_grid[0]))
        self.visible_grid = [[Cell() for j in range(self.grid_size[1])] for i in range(self.grid_size[0])]
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                print(f"({i}, {j})")
                self.visible_grid[i][j].hidden = True
                if visible_grid[i][j].flagged:
                    self.visible_grid[i][j].flagged = True
                    self.visible_grid[i][j].value = 10
                    print(f"Flagging cell ({i}, {j})")
                if visible_grid[i][j].hidden == False:
                    self.visible_grid[i][j].value = int(visible_grid[i][j])
                    self.visible_grid[i][j].flagged = False
                    self.visible_grid[i][j].hidden = False

    def transition(self):
        next_grid = copy.deepcopy(self.visible_grid)
        for i in range(len(self.visible_grid)):
            for j in range(len(self.visible_grid[i])):
                if not self.visible_grid[i][j].hidden and 0 < int(self.visible_grid[i][j]) < 10:
                    self.apply_rules(i, j, next_grid)
        return next_grid

    def apply_rules(self, i, j, next_grid):
        neighborhood = self.get_neighborhood(i, j)
        mines_on_neighbors = sum(1 for cell in neighborhood if cell.flagged)
        hidden_cells = sum(1 for cell in neighborhood if cell.hidden)

        cell_value = int(self.visible_grid[i][j])  # Get the value of the current cell

        # Rule 1: Flag cells if hidden_cells + mines_on_neighbors equals the cell value
        if hidden_cells + mines_on_neighbors == cell_value:
            for ni, nj in self.get_neighborhood_indices(i, j):
                if self.visible_grid[ni][nj].hidden and not self.visible_grid[ni][nj].flagged:
                    next_grid[ni][nj].flagged = True


        for ni, nj in self.get_neighborhood_indices(i, j):
            if self.visible_grid[ni][nj].hidden == False:
                # check if the other cell has enough mines around it
                neighborhood = self.get_neighborhood(ni, nj)
                mines_on_neighbors = sum(1 for cell in neighborhood if cell.flagged or cell.value == 10)
                print(neighborhood)
                print(f'({ni}, {nj}) has {mines_on_neighbors} mines on neighbors')
                if mines_on_neighbors == int(self.visible_grid[ni][nj]):
                    for nni, nnj in self.get_neighborhood_indices(ni, nj):
                        if self.visible_grid[nni][nnj].hidden and not self.visible_grid[nni][nnj].flagged:
                            next_grid[nni][nnj].hidden = False
                            print(f"Revealing cell ({nni}, {nnj})")

    def get_neighborhood(self, i, j):
        neighborhood = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                ni, nj = i + x, j + y
                if 0 <= ni < len(self.visible_grid) and 0 <= nj < len(self.visible_grid[i]):
                    neighborhood.append(self.visible_grid[ni][nj])
        return neighborhood

    def get_neighborhood_indices(self, i, j):
        indices = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                ni, nj = i + x, j + y
                if 0 <= ni < len(self.visible_grid) and 0 <= nj < len(self.visible_grid[i]):
                    indices.append((ni, nj))
        return indices


if __name__ == "__main__":
    grid_size = (16, 16)
    game = Minesweeper(grid_size)
    game.run()
