"""
This module implements a custom version of Conway's Game of Life.
The game is played on a grid of cells, where each cell can be in one of four states:
0 - dead
1 - alive
2 - red: Used to mark initial wave that destroys all non-cross shapes
3 - blue: Used to mark wave from cross edges to the center
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.colors import ListedColormap


class GameOfLife:
    def __init__(self, grid_size):
        # TODO: Maybe change the implementation to use bits instead of integers
        # This will allow to use the same grid for both current and next day:
        # for example we can set the first 2 bits to be the current state-
        # and the next 2 bits to be the next state up to 4 states on the same cell.
        # we can use bitwise operations to get the current state and the next state-
        # or keep the bits and use bitwise for redo/undo
        self.grid_size = grid_size
        self.grid = self.create_grid(grid_size)
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        self.cmap = ListedColormap(
            ['white', 'black', 'red', 'blue', 'green'], N=5)
        self.img = self.ax.imshow(
            self.grid, cmap=self.cmap, interpolation='nearest')
        self.ax.set_title('My Cross Game of Life')
        self.ax.set_axis_off()
        self.setup_button()
        self.setup_reset_button()

    def draw_random_cross(self, grid, size):
        # cross is equal arms, in this context a + shape
        cross_size = np.random.randint(3, 10)
        cross_middle = np.random.randint(
            0, size[0] - cross_size), np.random.randint(0, size[1] - cross_size)
        while cross_middle[0] + cross_size > size[0] or cross_middle[1] + cross_size > size[1]:
            cross_middle = np.random.randint(
                0, size[0] - cross_size), np.random.randint(0, size[1] - cross_size)

        for i in range(cross_size):
            grid[cross_middle[0] + i, cross_middle[1] + cross_size // 2] = 1
            grid[cross_middle[0] + cross_size // 2, cross_middle[1] + i] = 1

    def create_grid(self, size):
        # draw some cross patterns
        grid = np.zeros(size, dtype=np.int8)
        # select a random cross pattern and place it in a random valid position
        self.draw_random_cross(grid, size)
        self.draw_random_cross(grid, size)

        # draw some random cells not intersecting with the cross
        for i in range(size[0]):
            for j in range(size[1]):
                if grid[i, j] == 0 and self.get_neighberhood(i, j, grid) == [0, 0, 0,
                                                                             0, 0, 0,
                                                                             0, 0, 0]:
                    grid[i, j] = np.random.randint(0, 2)

        return grid

    def get_neighberhood(self, i, j, grid=None):
        if grid is None:
            grid = self.grid
        rows = grid.shape[0]
        cols = grid.shape[1]
        neighbor_hood = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        x = i
        y = j
        # moves clockwise from top left
        moves = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1), (0, 0), (0, 1),
                 (1, -1), (1, 0), (1, 1)]

        # set neighbor_hood in order to check the rules
        # set cell in the middle of the neighbor_hood
        for move in moves:
            if 0 <= x + move[0] < rows and 0 <= y + move[1] < cols:
                neighbor_hood[moves.index(
                    move)] = grid[x + move[0], y + move[1]]

        return neighbor_hood

    def transition(self, i, j):
        """
        This function implements the rules of the game
        """
        neighbor_hood = self.get_neighberhood(i, j)

        ############################
        # start the first wave
        if neighbor_hood == [0, 1, 0,
                             1, 1, 1,
                             0, 1, 0]:
            return 2

        if neighbor_hood == [0, 1, 0,
                             0, 1, 0,
                             0, 1, 0]:
            return 2

        if neighbor_hood == [0, 1, 0,
                             0, 1, 0,
                             1, 1, 1]:
            return 2

        if neighbor_hood == [1, 1, 1,
                             0, 1, 0,
                             0, 1, 0]:
            return 2

        if neighbor_hood == [1, 0, 0,
                             1, 1, 1,
                             1, 0, 0]:
            return 2

        if neighbor_hood == [0, 0, 1,
                             1, 1, 1,
                             0, 0, 1]:
            return 2

        if neighbor_hood == [0, 0, 0,
                             1, 1, 1,
                             0, 0, 0]:
            return 2

        elif neighbor_hood == [0, 1, 0,
                               0, 1, 0,
                               0, 1, 0]:
            return 2

        elif neighbor_hood == [0, 0, 0,
                               1, 1, 1,
                               0, 0, 0]:
            return 2

        ############################
        # start second wave from arms edges toward the center
        #
        #  0 ..       3       .. 0
        #             |
        #             v
        #  3 ->  ->   2  <-  <-  3
        #             ^
        #             |
        #  0 ..       3       .. 0
        #
        elif neighbor_hood == [0, 0, 0,
                               0, 1, 0,
                               1, 1, 1]:
            return 3

        elif neighbor_hood == [1, 1, 1,
                               0, 1, 0,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               0, 1, 0,
                               0, 1, 0]:
            return 3

        elif neighbor_hood == [0, 0, 1,
                               0, 1, 1,
                               0, 0, 1]:
            return 3

        elif neighbor_hood == [1, 0, 0,
                               1, 1, 0,
                               1, 0, 0]:
            return 3

        elif neighbor_hood == [0, 1, 0,
                               0, 1, 0,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               1, 1, 0,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               0, 1, 1,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               0, 1, 0,
                               0, 1, 0]:
            return 3

        elif neighbor_hood == [0, 0, 2,
                               3, 2, 2,
                               0, 0, 2]:
            return 3

        elif neighbor_hood == [2, 2, 2,
                               0, 2, 0,
                               0, 3, 0]:
            return 3

        elif neighbor_hood == [2, 0, 0,
                               2, 2, 3,
                               2, 0, 0]:
            return 3

        elif neighbor_hood == [0, 3, 0,
                               0, 2, 0,
                               2, 2, 2]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               2, 2, 3,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 2, 0,
                               0, 2, 0,
                               0, 3, 0]:
            return 3

        elif neighbor_hood == [0, 3, 0,
                               0, 2, 0,
                               0, 2, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               3, 2, 2,
                               0, 0, 0]:
            return 3

        ############################
        # Wave in progress - keep middle cells state
        elif neighbor_hood == [0, 2, 0,
                               2, 2, 2,
                               0, 2, 0]:
            return 2

        elif neighbor_hood == [0, 2, 0,
                               0, 2, 0,
                               2, 2, 2]:
            return 2

        elif neighbor_hood == [2, 0, 0,
                               2, 2, 2,
                               2, 0, 0]:
            return 2

        elif neighbor_hood == [0, 2, 0,
                               0, 3, 0,
                               0, 3, 0]:
            return 3

        elif neighbor_hood == [0, 3, 0,
                               0, 3, 0,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 3, 0,
                               0, 3, 0,
                               0, 2, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               0, 3, 3,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               3, 3, 0,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               3, 3, 2,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 2, 0,
                               0, 2, 0,
                               0, 2, 0]:
            return 2

        elif neighbor_hood == [0, 2, 0,
                               0, 2, 0,
                               2, 2, 2]:
            return 2

        elif neighbor_hood == [0, 3, 0,
                               0, 3, 0,
                               0, 2, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               2, 2, 2,
                               0, 0, 0]:
            return 2

        elif neighbor_hood == [0, 0, 2,
                               2, 2, 2,
                               0, 0, 2]:
            return 2

        elif neighbor_hood == [2, 2, 2,
                               0, 2, 0,
                               0, 2, 0]:
            return 2

        elif neighbor_hood == [2, 0, 0,
                               2, 2, 2,
                               2, 0, 0]:
            return 2

        elif neighbor_hood == [0, 0, 0,
                               2, 3, 3,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 2, 0,
                               2, 2, 2,
                               0, 2, 0]:
            return 2

        elif neighbor_hood == [0, 3, 0,
                               0, 3, 0,
                               0, 2, 0]:
            return 3

        elif neighbor_hood == [0, 2, 0,
                               0, 3, 0,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               0, 3, 2,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               2, 3, 0,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               0, 3, 0,
                               0, 2, 0]:
            return 3

        ############################
        # Wave complete successfully

        elif neighbor_hood == [0, 3, 0,
                               3, 2, 3,
                               0, 3, 0]:
            return 3

        elif neighbor_hood == [0, 0, 3,
                               0, 3, 2,
                               0, 0, 3]:
            return 3

        elif neighbor_hood == [3, 0, 0,
                               2, 3, 0,
                               3, 0, 0]:
            return 3

        elif neighbor_hood == [3, 2, 3,
                               0, 3, 0,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 3,
                               0, 3, 2,
                               0, 0, 3]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               0, 3, 0,
                               3, 2, 3]:
            return 3

        elif neighbor_hood == [3, 2, 3,
                               0, 3, 0,
                               0, 3, 0]:
            return 3

        elif neighbor_hood == [0, 3, 0,
                               0, 3, 0,
                               3, 2, 3]:
            return 3

        elif neighbor_hood == [0, 0, 3,
                               3, 3, 2,
                               0, 0, 3]:
            return 3

        elif neighbor_hood == [3, 0, 0,
                               2, 3, 3,
                               3, 0, 0]:
            return 3

        ############################
        # Final state - preserve cross shapes
        elif neighbor_hood == [0, 3, 0,
                               3, 3, 3,
                               0, 3, 0]:
            return 3

        elif neighbor_hood == [3, 0, 0,
                               3, 3, 3,
                               3, 0, 0]:
            return 3

        elif neighbor_hood == [3, 3, 3,
                               0, 3, 0,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 3,
                               0, 3, 3,
                               0, 0, 3]:
            return 3

        elif neighbor_hood == [3, 0, 0,
                               3, 3, 0,
                               3, 0, 0]:
            return 3

        elif neighbor_hood == [3, 3, 3,
                               0, 3, 0,
                               0, 3, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               0, 3, 0,
                               3, 3, 3]:
            return 3

        elif neighbor_hood == [0, 3, 0,
                               0, 3, 0,
                               3, 3, 3]:
            return 3

        elif neighbor_hood == [0, 0, 3,
                               3, 3, 3,
                               0, 0, 3]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               3, 3, 3,
                               0, 0, 0]:
            return 3

        elif neighbor_hood == [0, 0, 0,
                               0, 3, 0,
                               0, 3, 0]:
            return 3

        elif neighbor_hood == [0, 3, 0,
                               0, 3, 0,
                               0, 3, 0]:
            return 3

        ############################
        # destruction

        if 1 in neighbor_hood and 3 in neighbor_hood:
            # The default rules will handle the final destruction
            return 1

        if neighbor_hood[4] == 2 and (neighbor_hood[1] != 3 or neighbor_hood[7] != 3 or neighbor_hood[3] != 3 or neighbor_hood[5] != 3):
            return 1

        # The following rules are redundant - I left them here for reference
        if neighbor_hood == [0, 3, 0,
                             2, 2, 2,
                             0, 2, 0]:
            return 1

        if neighbor_hood == [0, 3, 0,
                             2, 2, 2,
                             0, 0, 0]:
            return 1

        if neighbor_hood == [0, 3, 0,
                             3, 2, 3,
                             0, 0, 0]:
            return 1

        if neighbor_hood == [0, 3, 0,
                             3, 2, 0,
                             0, 0, 0]:
            return 1

        if neighbor_hood == [0, 3, 0,
                             0, 2, 3,
                             0, 0, 0]:
            return 1

        if neighbor_hood == [0, 0, 0,
                             3, 2, 0,
                             0, 3, 0]:
            return 1

        if neighbor_hood == [0, 0, 0,
                             0, 2, 3,
                             0, 3, 0]:
            return 1

        if neighbor_hood == [0, 3, 0,
                             3, 2, 0,
                             0, 3, 0]:
            return 1

        if neighbor_hood == [0, 3, 0,
                             0, 2, 3,
                             0, 3, 0]:
            return 1

        if neighbor_hood == [0, 2, 0,
                             3, 2, 2,
                             0, 2, 0]:
            return 1

        if neighbor_hood == [0, 3, 0,
                             3, 2, 2,
                             0, 2, 0]:
            return 1

        if neighbor_hood == [0, 2, 0,
                             2, 2, 3,
                             0, 2, 0]:
            return 1

        if neighbor_hood == [0, 2, 0,
                             2, 2, 3,
                             0, 3, 0]:
            return 1

        if neighbor_hood == [0, 2, 0,
                             0, 2, 3,
                             0, 3, 0]:
            return 1

        if neighbor_hood == [0, 2, 0,
                             2, 2, 2,
                             0, 3, 0]:
            return 1

        if neighbor_hood == [0, 2, 0,
                             0, 2, 0,
                             3, 2, 2]:
            return 1

        if neighbor_hood == [0, 2, 0,
                             0, 2, 0,
                             3, 2, 3]:
            return 1

        if neighbor_hood == [0, 2, 0,
                             0, 2, 0,
                             2, 2, 3]:
            return 1

        if neighbor_hood == [3, 2, 2,
                             0, 2, 0,
                             0, 2, 0]:
            return 1

        if neighbor_hood == [3, 2, 2,
                             0, 2, 0,
                             0, 3, 0]:
            return 1

        if neighbor_hood == [3, 2, 2,
                             0, 3, 0,
                             0, 3, 0]:
            return 1


        elif neighbor_hood == [0, 3, 0,
                               0, 3, 0,
                               0, 1, 0]:
            return 1

        elif neighbor_hood == [0, 0, 0,
                               3, 3, 1,
                               0, 0, 0]:
            return 1

        elif neighbor_hood == [0, 0, 0,
                               1, 3, 3,
                               0, 0, 0]:
            return 1

        elif neighbor_hood == [0, 1, 0,
                               0, 3, 0,
                               0, 3, 0]:
            return 1

        elif neighbor_hood == [0, 3, 0,
                               0, 3, 0,
                               3, 1, 3]:
            return 1

        elif neighbor_hood == [0, 0, 3,
                               3, 3, 1,
                               0, 0, 3]:
            return 1

        elif neighbor_hood == [3, 0, 0,
                               1, 3, 3,
                               3, 0, 0]:
            return 1

        elif neighbor_hood == [3, 1, 3,
                               0, 3, 0,
                               0, 3, 0]:
            return 1


        elif neighbor_hood == [0, 0, 0,
                               1, 3, 0,
                               0, 0, 0]:
            return 1

        elif neighbor_hood == [0, 0, 0,
                               0, 3, 1,
                               0, 0, 0]:
            return 1

        elif neighbor_hood == [0, 0, 0,
                               0, 3, 0,
                               0, 1, 0]:
            return 1

        elif neighbor_hood == [0, 1, 0,
                               0, 3, 0,
                               0, 0, 0]:
            return 1


        else:
            return 0

    def on_click(self, event):
        i, j = int(event.ydata), int(event.xdata)
        if 0 <= i < self.grid_size[0] and 0 <= j < self.grid_size[1]:
            self.grid[i, j] = 1 if self.grid[i, j] == 0 else 0
            self.img.set_data(self.grid)
            self.update_grid()

    def draw_grid(self):
        self.ax.imshow(self.grid, cmap=self.cmap)
        # draw cell lines
        for i in range(self.grid.shape[0]):
            self.ax.plot([-0.5, self.grid.shape[1] - 0.5],
                         [i - 0.5, i - 0.5], color='black')
        for j in range(self.grid.shape[1]):
            self.ax.plot([j - 0.5, j - 0.5],
                         [-0.5, self.grid.shape[0] - 0.5], color='black')
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i, j] == 0:
                    self.ax.add_patch(plt.Rectangle(
                        (j-0.5, i-0.5), 1, 1, color='white'))
                    # self.ax.text(j, i, self.grid[i, j], ha="center", va="center", color="w")
                elif self.grid[i, j] == 1:
                    self.ax.add_patch(plt.Rectangle(
                        (j-0.5, i-0.5), 1, 1, color='black'))
                    # self.ax.text(j, i, self.grid[i, j], ha="center", va="center", color="b")
                elif self.grid[i, j] == 2:
                    self.ax.add_patch(plt.Rectangle(
                        (j-0.5, i-0.5), 1, 1, color='red'))
                    # self.ax.text(j, i, self.grid[i, j], ha="center", va="center", color="r")
                elif self.grid[i, j] == 3:
                    self.ax.add_patch(plt.Rectangle(
                        (j-0.5, i-0.5), 1, 1, color='blue'))
                    # self.ax.text(j, i, self.grid[i, j], ha="center", va="center", color="g")

    def update_grid(self):
        # refresh canvas
        self.fig.canvas.draw_idle()
        self.draw_grid()

    def next_day(self, event):
        new_grid = self.grid.copy()
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                new_grid[i, j] = self.transition(i, j)
        self.grid = new_grid
        self.img.set_data(self.grid)
        self.update_grid()

    def setup_button(self):
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.button = Button(axnext, 'Next Day')
        self.button.on_clicked(self.next_day)

    def setup_animation(self):
        self.anim = animation.FuncAnimation(
            self.fig, self.next_day, interval=50, blit=False)

    def setup_reset_button(self):
        axreset = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.reset_button = Button(axreset, 'Reset')
        self.reset_button.on_clicked(self.reset)

    def reset(self, event):
        self.grid = self.create_grid(self.grid_size)
        self.img.set_data(self.grid)
        self.update_grid()

    def run(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.show()


if __name__ == '__main__':
    grid_size = (20, 20)
    game = GameOfLife(grid_size)
    game.run()
