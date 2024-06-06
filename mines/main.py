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
import asyncio
import numpy as np
import pygame
from pygame.locals import *


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


# Initialize the Pygame video system
pygame.init()



CELL_SIZE = 50
WINDOW_SIZE = (DEFAULT_GRID_SIZE[1] * CELL_SIZE, DEFAULT_GRID_SIZE[0] * CELL_SIZE + CELL_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Minesweeper")

# Grid settings
CELL_SIZE = min(
    WINDOW_SIZE[0] // DEFAULT_GRID_SIZE[0], WINDOW_SIZE[1] // DEFAULT_GRID_SIZE[1]
)  # Ensure the grid fits within the window
GRID_SIZE = DEFAULT_GRID_SIZE

# Font settings
FONT_SIZE = CELL_SIZE * 2 // 3  # Set the font size to half the cell size
FONT = pygame.font.SysFont("monospace", FONT_SIZE, bold=True)

RUNING = True


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
                if (
                    self.visible_grid[i][j] != FLAG_MINE
                    and self.visible_grid[i][j] != "_"
                ):
                    self.apply_rules(i, j, next_grid)
        return next_grid

    def apply_rules(self, i, j, next_grid):
        neighborhood = self.get_neighborhood(i, j)
        mines_on_neighbors = sum(1 for cell in neighborhood if cell == FLAG_MINE)
        hidden_cells = sum(1 for cell in neighborhood if cell == "_")

        cell_value = int(self.visible_grid[i][j])

        if hidden_cells + mines_on_neighbors == cell_value:
            for ni, nj in self.get_neighborhood_indices(i, j):
                if self.visible_grid[ni][nj] == "_":
                    next_grid[ni][nj] = FLAG_MINE

        for ni, nj in self.get_neighborhood_indices(i, j):
            if (
                self.visible_grid[ni][nj] != FLAG_MINE
                and self.visible_grid[ni][nj] != "_"
            ):
                neighborhood = self.get_neighborhood(ni, nj)
                mines_on_neighbors = sum(
                    1 for cell in neighborhood if cell == FLAG_MINE
                )
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


class Minesweeper:
    def __init__(self, grid_size=DEFAULT_GRID_SIZE, n_mines=NUM_OF_MINES):
        self.grid = self.init_grid(grid_size, n_mines)
        self.visible_grid = copy.deepcopy(self.grid)
        self.last_visible_grid = None
        self.grid_size = grid_size
        self.skull_image = pygame.image.load("skull.svg")
        self.skull_image = pygame.transform.scale(
            self.skull_image, (CELL_SIZE, CELL_SIZE)
        )
        self.flag_image = pygame.image.load("flag.svg")
        self.flag_image = pygame.transform.scale(
            self.flag_image, (CELL_SIZE, CELL_SIZE)
        )

        self.screen = pygame.display.set_mode(
            (grid_size[1] * CELL_SIZE, grid_size[0] * CELL_SIZE + 50)
        )
        pygame.display.set_caption("Minesweeper")
        self.buttons = []
        self.setup_buttons()
        self.grid_dirty = True


    def init_grid(self, grid_size=DEFAULT_GRID_SIZE, n_mines=NUM_OF_MINES):
        grid = [[Cell() for _ in range(grid_size[1])] for _ in range(grid_size[0])]
        mines = self.generate_mines(grid_size, n_mines)
        self.populate_grid_with_mines(mines, grid)
        return grid

    def generate_mines(self, grid_size=DEFAULT_GRID_SIZE, num_mines=NUM_OF_MINES):
        mines = np.zeros(grid_size, dtype=np.int8)
        mine_indices = np.random.choice(
            grid_size[0] * grid_size[1], num_mines, replace=False
        )
        mines[np.unravel_index(mine_indices, grid_size)] = 1
        return mines

    def populate_grid_with_mines(self, mines, grid):
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if mines[i][j]:
                    cell.value = MINE
                    self.increment_surrounding_cells(i, j, grid)

    def increment_surrounding_cells(self, i, j, grid):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if 0 <= i + x < len(grid) and 0 <= j + y < len(grid[0]):
                    if grid[i + x][j + y].value != MINE:
                        grid[i + x][j + y].value += 1

    async def draw_buttons(self):
        for button in self.buttons:
            bx, by = button["pos"]
            # Draw button border
            pygame.draw.rect(self.screen, BLACK, (bx, by, 100, 30))
            pygame.draw.rect(
                self.screen, button["color"], (bx + 2, by + 2, 96, 26)
            )  # Draw button
            text_surface = FONT.render(button["text"], True, BLACK)
            text_rect = text_surface.get_rect(center=(bx + 50, by + 15))
            self.screen.blit(text_surface, text_rect)

    async def draw_revealed_cell(self, i, j):
        pygame.draw.rect(
            self.screen,
            REVEALED_FACE_COLOR,
            (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )
        pygame.draw.line(
            self.screen,
            GREY,
            (j * CELL_SIZE, i * CELL_SIZE),
            (j * CELL_SIZE + CELL_SIZE, i * CELL_SIZE),
            1,
        )
        pygame.draw.line(
            self.screen,
            GREY,
            (j * CELL_SIZE, i * CELL_SIZE),
            (j * CELL_SIZE, i * CELL_SIZE + CELL_SIZE),
            1,
        )
        pygame.draw.line(
            self.screen,
            WHITE,
            (j * CELL_SIZE, i * CELL_SIZE + CELL_SIZE),
            (j * CELL_SIZE + CELL_SIZE, i * CELL_SIZE + CELL_SIZE),
            1,
        )
        pygame.draw.line(
            self.screen,
            WHITE,
            (j * CELL_SIZE + CELL_SIZE, i * CELL_SIZE),
            (j * CELL_SIZE + CELL_SIZE, i * CELL_SIZE + CELL_SIZE),
            1,
        )

    async def draw_unrevealed_cell(self, i, j):
        pygame.draw.rect(
            self.screen,
            HIDDEN_FACE_COLOR,
            (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )
        pygame.draw.line(
            self.screen,
            WHITE,
            (j * CELL_SIZE, i * CELL_SIZE),
            (j * CELL_SIZE + CELL_SIZE, i * CELL_SIZE),
            CELL_SIZE // 16,
        )
        pygame.draw.line(
            self.screen,
            WHITE,
            (j * CELL_SIZE, i * CELL_SIZE),
            (j * CELL_SIZE, i * CELL_SIZE + CELL_SIZE),
            CELL_SIZE // 16,
        )
        pygame.draw.line(
            self.screen,
            GREY,
            (j * CELL_SIZE, i * CELL_SIZE + CELL_SIZE),
            (j * CELL_SIZE + CELL_SIZE, i * CELL_SIZE + CELL_SIZE),
            CELL_SIZE // 8,
        )
        pygame.draw.line(
            self.screen,
            GREY,
            (j * CELL_SIZE + CELL_SIZE, i * CELL_SIZE),
            (j * CELL_SIZE + CELL_SIZE, i * CELL_SIZE + CELL_SIZE),
            CELL_SIZE // 8,
        )

    async def draw_grid(self):
        screen.fill(BACKROUND_COLOR)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                cell = self.grid[i][j]
                if cell.hidden:
                    await self.draw_unrevealed_cell(i, j)
                if cell.flagged:
                    screen.blit(self.flag_image, (j * CELL_SIZE, i * CELL_SIZE))
                if not cell.hidden:
                    await self.draw_revealed_cell(i, j)
                    if cell.value > 0 and cell.value < MINE:
                        color = colors.get(cell.value, BLACK)
                        text_surface = FONT.render(str(cell.value), True, color)
                        text_rect = text_surface.get_rect(
                            center=(
                                j * CELL_SIZE + CELL_SIZE // 2,
                                i * CELL_SIZE + CELL_SIZE // 2,
                            )
                        )  # Center the text
                        screen.blit(text_surface, text_rect)
                    elif cell.is_mine():
                        screen.blit(self.skull_image, (j * CELL_SIZE, i * CELL_SIZE))
        await self.draw_buttons()

    def reveal_cell(self, i, j):
        if self.grid[i][j].is_mine():
            self.end_game(i, j)
            return
        self.update_last_visible_grid()
        self.grid[i][j].reveal()
        if self.grid[i][j].is_empty():
            self.reveal_surrounding_cells(i, j)
        if self.check_win():
            print("You won the game!")
            self.screen.fill(GREEN)
        self.grid_dirty = True

    def flag_cell(self, i, j):
        self.update_last_visible_grid()
        self.grid[i][j].flag()
        self.visible_grid[i][j].flag()

    def unflag_cell(self, i, j):
        self.update_last_visible_grid()
        if self.grid[i][j].flagged:
            self.grid[i][j].flagged = False

    def end_game(self, i, j):
        print(f"Game Over! You hit a mine on cell ({i}, {j})")
        self.grid[i][j].value = MINE
        self.screen.fill(RED)
        self.show_all_mines()

    def update_last_visible_grid(self):
        self.last_visible_grid = copy.deepcopy(self.grid)

    def reveal_surrounding_cells(self, i, j):
        for x in range(-1, 2):
            for y in range(-1, 2):
                ni, nj = i + x, j + y
                if self.is_valid_cell(ni, nj) and self.grid[ni][nj].hidden:
                    self.reveal_cell(ni, nj)

    def is_valid_cell(self, i, j):
        return 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0])

    def show_all_mines(self):
        for row in self.grid:
            for cell in row:
                if cell.is_mine():
                    cell.hidden = False

    def check_win(self):
        for row in self.grid:
            for cell in row:
                if not cell.is_mine() and cell.hidden:
                    return False
        return True

    def setup_buttons(self):
        self.buttons = []
        button_y = self.grid_size[0] * CELL_SIZE + 10
        self.buttons.append(
            {
                "text": "Reset",
                "pos": (0, button_y),
                "callback": self.reset_game,
                "color": (255, 0, 0),
            }
        )  # Red
        self.buttons.append(
            {
                "text": "Undo",
                "pos": (110, button_y),
                "callback": self.undo_last_move,
                "color": (0, 255, 0),
            }
        )  # Green
        self.buttons.append(
            {
                "text": "Hint",
                "pos": (220, button_y),
                "callback": self.give_hint,
                "color": (0, 0, 255),
            }
        )  # Blue
        self.buttons.append(
            {
                "text": "Next",
                "pos": (330, button_y),
                "callback": self.next_day,
                "color": (255, 255, 0),
            }
        )  # Yellow


    def undo_last_move(self):
        if self.last_visible_grid:
            self.grid = copy.deepcopy(self.last_visible_grid)
            self.grid_dirty = True

    def apply_rules(self, board):
        rules = MinesweeperRules(board)
        next_visible_grid = rules.transition()
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if next_visible_grid[i][j] == TO_BE_REVEALED:
                    cell.hidden = False
                elif next_visible_grid[i][j] == FLAG_MINE:
                    cell.flagged = True

    def next_day(self):
        self.last_visible_grid = copy.deepcopy(self.grid)
        board = [["_" for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell.flagged:
                    board[i][j] = FLAG_MINE
                elif not cell.hidden:
                    board[i][j] = str(cell.value)
            board.append([])
        self.apply_rules(board)
        self.grid_dirty = True

    def reset_game(self):
        self.screen.fill(BACKROUND_COLOR)
        self.grid = self.init_grid()
        self.visible_grid = copy.deepcopy(self.grid)
        self.last_visible_grid = None
        self.grid_dirty = True

    def give_hint(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if not self.grid[i][j].is_mine() and self.grid[i][j].hidden:
                    self.reveal_cell(i, j)
                    break
        self.grid_dirty = True


    async def run(self):
        global RUNING
        while RUNING:
            if self.grid_dirty:
                await self.draw_grid()  # Draw the grid only when necessary
                self.grid_dirty = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNING = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.grid_dirty = True
                    x, y = event.pos
                    if y < self.grid_size[0] * CELL_SIZE:
                        i, j = y // CELL_SIZE, x // CELL_SIZE
                        if event.button == 1:
                            self.reveal_cell(i, j)
                        elif event.button == 3:
                            self.flag_cell(i, j)
                    else:
                        for button in self.buttons:
                            bx, by = button["pos"]
                            if bx <= x <= bx + 100 and by <= y <= by + 30:
                                button["callback"]()
            pygame.display.flip()
            await asyncio.sleep(0)
        pygame.quit()

async def main():
    game = Minesweeper()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
