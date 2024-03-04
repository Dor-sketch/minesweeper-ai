

# add decorator to track changes and store them in a list for further drawing



@staticmethod
def get_neighberhood(i, j, grid):
    """
    Get the neighbor_hood of a cell.
    Note that the cell is included in the neighbor_hood (in the middle)
    also note that the neighbor_hood is a 3x3 grid even if the cell is on the edge
    its padded with zeros. The neighbors are ordered in a clockwise manner
    """
    if grid is None:
        raise ValueError("grid is required")

    rows = grid.shape[0]
    cols = grid.shape[1]
    neighbor_hood = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = i
    y = j
    # moves clockwise from top left
    moves = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 0),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]
    # set neighbor_hood in order to check the rules
    # set cell in the middle of the neighbor_hood
    for move in moves:
        if 0 <= x + move[0] < rows and 0 <= y + move[1] < cols:
            neighbor_hood[moves.index(
                move)] = grid[x + move[0], y + move[1]]
    return neighbor_hood


class Rules:
    def __init__(self, grid):
        self.grid = grid.copy()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """clean resources"""
        del self.grid



    def transition(self, i, j):
        """
        This function implements the rules of the game
        """
        neighbor_hood = get_neighberhood(i, j, self.grid)

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