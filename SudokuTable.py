"""Class definition for a 9x9 Sudoku grid.
"""


import numpy


EASY = [[0, 2, 0, 1, 7, 8, 0, 3, 0],
        [0, 4, 0, 3, 0, 2, 0, 9, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 0, 8, 6, 0, 3, 5, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 6, 7, 0, 9, 2, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 8, 0, 9, 0, 1, 0, 6, 0],
        [0, 1, 0, 4, 3, 6, 0, 5, 0]]
EASY = numpy.array(EASY)


class SudokuTable:
    """A class for a 9x9 Sudoku grid, containing relevant data and methods.

    """

    # Array representing the Sudoku grid.
    # First two dimensions are the rows and cols of the grid.
    # Third dimension 0: confirmed cell value.
    # Third dimension 1: possible numbers for that cell.
    grid = numpy.zeros(shape=(9,9,2))


    def __init__(self, start_grid):
        """Populate class grid with starting numbers and possible numbers."""

        it = numpy.nditer(self.grid,
                              flags=['multi_index'],
                              op_flags=['readwrite'])

        while not it.finished:
            confirmed_num = start_grid[it.multi_index[0], it.multi_index[1]]

            if it[0] == confirmed_num:
                self.grid[it.multi_index[0],
                          it.multi_index[1],
                          0] = confirmed_num

            else:
                self.grid[it.multi_index[0],
                          it.multi_index[1],
                          1] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            it.iternext()
