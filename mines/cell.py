"""
This module contains the classes representing the cells in the Minesweeper grid
and the rules of the Minesweeper game
"""

import copy
from config import MINE, HIDDEN, FLAG_MINE, TO_BE_REVEALED


class Cell:
    def __init__(self, value=0):
        self.value = value
        self.hidden = True
        self.flagged = False

    def __repr__(self):
        if self.flagged:
            return FLAG_MINE
        if self.hidden:
            return HIDDEN
        if self.value == MINE:
            return MINE
        return str(self.value)

    def is_mine(self):
        return self.value == MINE

    def is_empty(self):
        return self.value == 0

    def reveal(self):
        self.hidden = False

    def flag(self):
        self.flagged = not self.flagged

    def __int__(self):
        return self.value

    def __str__(self):
        if self.flagged:
            return FLAG_MINE
        if self.hidden:
            return "_"
        if self.value == MINE:
            return MINE
        return str(self.value)


class MinesweeperRules:
    def __init__(self, visible_grid):
        self.grid_size = (len(visible_grid), len(visible_grid[0]))
        self.visible_grid = visible_grid

    def transition(self):
        next_grid = copy.deepcopy(self.visible_grid)
        for i in range(len(self.visible_grid)):
            for j in range(len(self.visible_grid[i])):
                if self.visible_grid[i][j] != FLAG_MINE and self.visible_grid[i][j] != "_":
                    self.apply_rules(i, j, next_grid)
        return next_grid

    def apply_rules(self, i, j, next_grid):
        neighborhood = self.get_neighborhood(i, j)
        mines_on_neighbors = sum(
            1 for cell in neighborhood if cell == FLAG_MINE)
        hidden_cells = sum(1 for cell in neighborhood if cell == "_")

        cell_value = int(self.visible_grid[i][j])

        if hidden_cells + mines_on_neighbors == cell_value:
            for ni, nj in self.get_neighborhood_indices(i, j):
                if self.visible_grid[ni][nj] == "_":
                    next_grid[ni][nj] = FLAG_MINE

        for ni, nj in self.get_neighborhood_indices(i, j):
            if self.visible_grid[ni][nj] != FLAG_MINE and self.visible_grid[ni][nj] != "_":
                neighborhood = self.get_neighborhood(ni, nj)
                mines_on_neighbors = sum(
                    1 for cell in neighborhood if cell == FLAG_MINE)
                if mines_on_neighbors == int(self.visible_grid[ni][nj]):
                    for nni, nnj in self.get_neighborhood_indices(ni, nj):
                        if self.visible_grid[nni][nnj] == "_":
                            next_grid[nni][nnj] = TO_BE_REVEALED

    def get_neighborhood(self, i, j):
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
        indices = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                ni, nj = i + x, j + y
                if 0 <= ni < len(self.visible_grid) and 0 <= nj < len(
                    self.visible_grid[ni]
                ):
                    indices.append((ni, nj))
        return indices
