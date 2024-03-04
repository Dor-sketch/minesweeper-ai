"""
This module implements a custom version of Conway's Game of Life.
The game is played on a grid of cells, where each cell can be in one of four states:
0 - dead
1 - alive
2 - red: Used to mark initial wave that destroys all non-cross shapes
3 - blue: Used to mark wave from cross edges to the center
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.colors import ListedColormap
from Rules import Rules, get_neighberhood

def track_changes(func):
    """
    A decorator to track the changes in the grid after calling a function
    """
    def wrapper(self, *args, **kwargs):
        # Store a copy of the grid before changes
        grid_before = np.copy(self.grid)
        # Call the original function
        result = func(self, *args, **kwargs)
        # Find the indices where the grid has changed
        changed_indices = np.where(grid_before != self.grid)
        new_values = self.grid[changed_indices]
        # Store the changed indices
        self.changed_indices = list(
            zip(new_values, changed_indices[0], changed_indices[1])
        )
        return result

    return wrapper


class GameOfLife:
    """
    A class to represent the custom game of life
    """
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = np.zeros(grid_size, dtype=np.int8)
        self.changed_indices = []
        self.create_grid(grid_size)
        self.fig, self.ax = plt.subplots()
        self.init_grid()
        plt.subplots_adjust(bottom=0.2)
        self.cmap = ListedColormap(
            ["white", "black", "red", "blue", "green"], N=5)
        self.img = self.ax.imshow(
            self.grid, cmap=self.cmap, interpolation="nearest")
        self.ax.set_title("My Cross Game of Life")
        self.ax.set_axis_off()
        self.setup_buttons()

    # ========================================================================+
    # setup grid

    @track_changes
    def create_grid(self, size):
        """
        Create a grid with random cells and cross patterns
        """

        # seed the random number generator
        np.random.seed(int(time.time()))

        def draw_random_cross(grid, size):
            """
            select a random cross pattern and place it in a random valid position
            """

            # cross is equal arms, in this context a + shape
            cross_size = np.random.randint(3, self.grid_size[0] // 2)
            cross_middle = np.random.randint(0, size[0] - cross_size), np.random.randint(
                0, size[1] - cross_size
            )
            while (
                cross_middle[0] + cross_size > size[0]
                or cross_middle[1] + cross_size > size[1]
            ):
                cross_middle = np.random.randint(
                    0, size[0] - cross_size
                ), np.random.randint(0, size[1] - cross_size)

            for i in range(cross_size):
                grid[cross_middle[0] + i, cross_middle[1] + cross_size // 2] = 1
                grid[cross_middle[0] + cross_size // 2, cross_middle[1] + i] = 1

        grid = np.zeros(size, dtype=np.int8)
        # draw some cross patterns
        for _ in range(2):
            draw_random_cross(grid, size)

        # draw some random cells not intersecting with the cross
        for i in range(size[0]):
            for j in range(size[1]):
                # avoid drawing cells on the cross
                if grid[i, j] == 0 and get_neighberhood(i, j, grid) == [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ]:
                    grid[i, j] = np.random.randint(0, 2)

        self.grid = grid

    def init_grid(self):
        """
        draw cell lines
        """
        # avoid redrawing the grid lines if the grid is updated
        if hasattr(self, "grid_lines"):
            return
        for i in range(self.grid.shape[0]):
            self.ax.plot(
                [-0.5, self.grid.shape[1] - 0.5], [i - 0.5, i - 0.5], color="black"
            )
        for j in range(self.grid.shape[1]):
            self.ax.plot(
                [j - 0.5, j - 0.5], [-0.5, self.grid.shape[0] - 0.5], color="black"
            )
        self.grid_lines = True

    # ========================================================================+
    # setup buttons

    def setup_buttons(self):
        """
        setup the 3 buttons:
        - Clear: clear the grid
        - Next Day: apply the rules and update the grid
        - Reset: reset the grid to the initial state
        """
        # Create three buttons with equal width and no space in between
        axnext1 = plt.axes([0.2, 0.05, 0.2, 0.075])
        axnext2 = plt.axes([0.4, 0.05, 0.2, 0.075])
        axnext3 = plt.axes([0.6, 0.05, 0.2, 0.075])

        self.button1 = Button(axnext1, "Clear")
        self.button3 = Button(axnext3, "Next Day")
        self.button2 = Button(axnext2, "Reset")

        self.button2.on_clicked(self.reset)
        self.button1.on_clicked(self.clear)
        self.button3.on_clicked(self.next_day)


    def on_click(self, event):
        if (event.xdata is None) or (event.ydata is None):
            print("clicked outside the grid")
            return
        i, j = int(event.ydata), int(event.xdata)
        if i == 0 and j == 0:
            # BUG: There is a bug here, the first cell is connected to the buttons
            print("clicked on the axes")
            return
        if 0 <= i < self.grid_size[0] and 0 <= j < self.grid_size[1]:
            self.grid[i, j] = 1 if self.grid[i, j] == 0 else 0
            self.changed_indices.append((self.grid[i, j], i, j))
            self.update_grid()
        else:
            # maybe clicked on a button
            pass

    def next_day(self, event):
        self.apply_rules()
        self.update_grid()

    def reset(self, event):
        self.create_grid(self.grid_size)
        self.update_grid()

    def clear(self, event):
        self.clear_board()
        self.update_grid()

    def draw_grid(self):
        if self.changed_indices != []:
            self.draw_changes(self.changed_indices)
        self.changed_indices = []
        # TODO: maybe use set_data instead of creating a new image

    def draw_changes(self, changes):
        for change in changes:
            if change[0] == 0:
                self.ax.add_patch(
                    plt.Rectangle(
                        (change[2] - 0.5, change[1] - 0.5), 1, 1, color="white"
                    )
                )
            elif change[0] == 1:
                self.ax.add_patch(
                    plt.Rectangle(
                        (change[2] - 0.5, change[1] - 0.5), 1, 1, color="black"
                    )
                )
            elif change[0] == 2:
                self.ax.add_patch(
                    plt.Rectangle(
                        (change[2] - 0.5, change[1] - 0.5), 1, 1, color="red")
                )
            elif change[0] == 3:
                self.ax.add_patch(
                    plt.Rectangle(
                        (change[2] - 0.5, change[1] - 0.5), 1, 1, color="blue"
                    )
                )

    def update_grid(self):
        # refresh canvas
        self.draw_grid()
        self.fig.canvas.draw_idle()

    @track_changes
    def clear_board(self):
        self.grid = np.zeros(self.grid_size, dtype=np.int8)

    @track_changes
    def apply_rules(self):
        with Rules(self.grid) as r:
            for i in range(self.grid.shape[0]):
                for j in range(self.grid.shape[1]):
                    self.grid[i, j] = r.transition(i, j)

    def run(self):
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        plt.show()
        ani = animation.FuncAnimation(
            self.fig,
            self.update_grid,
            interval=1000,
            blit=True,
            repeat=False,
            save_count=10,
        )

    def generateGif(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_axis_off()
        ax.set_title("My Cross Game of Life")
        cmap = ListedColormap(["white", "black", "red", "blue", "green"], N=5)
        img = ax.imshow(self.grid, cmap=cmap, interpolation="nearest")

        def animate(i):
            # copy first frame 4 times to make the gif slower
            if i < 6:
                return (img,)
            self.apply_rules()
            img.set_data(self.grid)
            return (img,)

        ani = animation.FuncAnimation(
            fig,
            animate,
            interval=100,
            blit=True,
            repeat=False,
            save_count=20,
        )
        ani.save("cross_game.gif", writer="pillow")



if __name__ == "__main__":
    grid_size = (20, 20)
    game = GameOfLife(grid_size)
    game.run()
