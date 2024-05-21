import numpy as np


def generate_background(fig=None, grid=None):
    """
    Generate a gradient background for the game
    """
    if fig is None:
        raise ValueError("fig must be provided")
    # Create a gradient image
    gradient = np.linspace(0, 1, 256)  # generate gradient
    gradient = np.vstack((gradient, gradient))  # stack to create 2D array
    # Create a full-figure axis for the gradient background
    bg_ax = fig.add_axes([0, 0, 1, 1], zorder=-1)  # full figure axis
    bg_ax.imshow(
        gradient,
        aspect="auto",
        cmap="YlGnBu",
        extent=[0, len(grid[0]), 0, len(grid)],
    )
    bg_ax.axis("Tight")