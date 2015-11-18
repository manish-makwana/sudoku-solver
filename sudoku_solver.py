#!/usr/bin/python

"""Solves Sudoku puzzles.

Attributes:
    EASY: An easy sudoku puzzle.
    MEDIUM: A medium difficulty sudoku puzzle.
    MEDIUM2: Another medium difficulty sudoku puzzle.
    SudokuTable(grid): A class for storing puzzle data, and methods for
        solving and displaying it.
    main(): Create a SudokuTable instance with one of the given puzzles
        and solve it. The results are printed in human-readable format.
"""

# Note: Code checked with pylint version 1.1.0-1. Several of the disabled
#   warnings in this module are no longer applicable in the latest version.


import numpy


# pylint: disable=bad-whitespace
MEDIUM = [
    [0,2,0, 1,7,8, 0,3,0],
    [0,4,0, 3,0,2, 0,9,0],
    [1,0,0, 0,0,0, 0,0,6],

    [0,0,8, 6,0,3, 5,0,0],
    [3,0,0, 0,0,0, 0,0,4],
    [0,0,6, 7,0,9, 2,0,0],

    [9,0,0, 0,0,0, 0,0,2],
    [0,8,0, 9,0,1, 0,6,0],
    [0,1,0, 4,3,6, 0,5,0]]

EASY = [
    [5,3,0, 0,7,0, 0,0,0],
    [6,0,0, 1,9,5, 0,0,0],
    [0,9,8, 0,0,0, 0,6,0],

    [8,0,0, 0,6,0, 0,0,3],
    [4,0,0, 8,0,3, 0,0,1],
    [7,0,0, 0,2,0, 0,0,6],

    [0,6,0, 0,0,0, 2,8,0],
    [0,0,0, 4,1,9, 0,0,5],
    [0,0,0, 0,8,0, 0,7,9]]

MEDIUM2 = [
    [1,0,0, 0,0,5, 0,0,4],
    [0,2,3, 4,0,6, 0,5,0],
    [0,0,0, 0,0,0, 0,6,0],

    [9,0,4, 0,0,0, 0,7,0],
    [0,0,0, 5,6,7, 0,0,0],
    [0,5,0, 0,0,0, 8,0,3],

    [0,4,0, 0,0,0, 0,0,0],
    [0,3,0, 7,0,1, 9,8,0],
    [2,0,0, 8,0,0, 0,0,7]]


class SudokuTable(object):
    """A class for a 9x9 Sudoku grid, containing relevant data and methods.

    Attributes:
        grid: A 9x9 list of list, with each cell either the confirmed value
            as an int or a list of unconfirmed ints.
        print_grid(): Print the class grid list line by line, giving it a
            tidy and more human-friendly output.
        solve(): Iterate over the grid as many times as needed to solve the
            Sudoku puzzle, returning the solution grid and the number of
            iterations required. If max iterations are exceeded, the function
            will cancel.
    """

    def __init__(self, start_grid):
        """Populate class grid with starting numbers and possible numbers.

        All zeros are replaced with a list of numbers from 1-9, representing
        the possible solutions for that grid cell.

        Args:
            start_grid: A 9x9 list of lists, with each cell containing an
            integer from 0-9.
        """
        all_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.grid = [[all_nums if cell == 0 else cell for cell in row]
                     for row in start_grid]

    def nums_in_group(self, group):     # pylint: disable=no-self-use
        """Return the confirmed numbers in a group (row, col or 3x3 grid)."""
        return [cell for cell in group if type(cell) is not list]

    def remove_duplicates(self, group):
        """Remove duplicates between confirmed numbers in group and possible
        numbers for that cell.

        Args:
            group: A list containing integers for confirmed sudoku numbers,
                and lists of possible numbers for unconfirmed cells.
        """

        lst = []
        for cell in group:
            # Cell is a confirmed number.
            if isinstance(cell, int):
                lst.append(cell)

            # 1 item left in list. Needed to convert single item list into
            # an integer.
            elif len(cell) == 1:
                lst.append(cell[0])

            # Compare current unconfirmed numbers for cell against confirmed
            # numbers in the entire group.
            else:
                nums = self.nums_in_group(group)
                reduced_poss = [poss for poss in cell if not poss in nums]
                if len(reduced_poss) == 1:
                    lst.append(reduced_poss[0])
                else:
                    lst.append(reduced_poss)
        return lst


    def process_rows_cols(self):
        """Iterate through Sudoku grid by rows and cols, confirming known
        numbers.
        """
        new_grid = []
        # Go through grid row by row.
        for row in self.grid:
            new_grid.append(self.remove_duplicates(row))

        # Transpose grid so rows become columns and vice versa.
        # pylint: disable=bad-builtin
        # pylint: disable=star-args
        trans_grid = map(list, zip(*new_grid))

        # Go through grid column by column.
        new_grid = []
        for col in trans_grid:
            new_grid.append(self.remove_duplicates(col))

        self.grid = map(list, zip(*new_grid))

    def process_segments(self):
        """Split 9x9 grid into 9 segments, then check for confirmed numbers
        in each."""

        # Divide grid into segments.
        # pylint: disable=too-many-locals
        # pylint: disable=invalid-name
        # pylint: disable=no-member
        arr_grid = numpy.array(self.grid, dtype=object)
        a = arr_grid[0:3, 0:3]
        b = arr_grid[3:6, 0:3]
        c = arr_grid[6:9, 0:3]
        d = arr_grid[0:3, 3:6]
        e = arr_grid[3:6, 3:6]
        f = arr_grid[6:9, 3:6]
        g = arr_grid[0:3, 6:9]
        h = arr_grid[3:6, 6:9]
        i = arr_grid[6:9, 6:9]

        segments = [a, b, c, d, e, f, g, h, i]
        processed_segs = []
        for seg in segments:
        # Flatten each segment.
            s = numpy.ravel(seg).tolist()
        # Confirm numbers and reduce possibilities.
            s = self.remove_duplicates(s)
        # Wrap up each segment and convert back to array.
            s = numpy.array(s, dtype=object)
            s = numpy.reshape(s, (3, 3))
            processed_segs.append(s)
        # Join up segments back into 9x9 grid.
        new_arr_grid = arr_grid
        new_arr_grid[0:3, 0:3] = processed_segs[0]
        new_arr_grid[3:6, 0:3] = processed_segs[1]
        new_arr_grid[6:9, 0:3] = processed_segs[2]
        new_arr_grid[0:3, 3:6] = processed_segs[3]
        new_arr_grid[3:6, 3:6] = processed_segs[4]
        new_arr_grid[6:9, 3:6] = processed_segs[5]
        new_arr_grid[0:3, 6:9] = processed_segs[6]
        new_arr_grid[3:6, 6:9] = processed_segs[7]
        new_arr_grid[6:9, 6:9] = processed_segs[8]
        gd = new_arr_grid.tolist()
        self.grid = gd

    def print_grid(self):
        """Print the grid of confirmed and possible numbers by row."""

        print "----------------------------"
        for row in self.grid:
            print row

    def print_confirmed(self):
        """Print the grid of confirmed numbers only, with zeros substituted
        in for unconfirmed cells."""

        grid = [[0 if type(cell) is list else cell for cell in row]
                     for row in self.grid]
        print "----------------------------"
        for row in grid:
            print row

    def solve(self):
        """Solve the Sudoku puzzle, iterating as needed up to 50 iterations.

        Returns:
            (is_solved, iteration_count): A tuple of a boolean indicating
                whether the puzzle was solved, and an integer of the number
                of iterations carried out.
        """
        solved = False
        count = 0
        while solved == False:
            count += 1
            # Check for confirmed numbers.
            self.process_rows_cols()
            self.process_segments()
            solved = True
            # Clear solved flag if any cell still contains multiple
            # possibilities.
            for row in self.grid:
                for cell in row:
                    if type(cell) == list:
                        solved = False
            if count > 50:
                break
        return (solved, count)

def main():
    """Solve a test Sudoku puzzle using the SudokuTable class and methods."""
    # pylint: disable=invalid-name
    st = SudokuTable(EASY)
    it = st.solve()
    # The grid was solved.
    if it[0] == True:
        print "The solved Sudoku grid is:"
        st.print_grid()
        print "This took %i iterations." %it[1]
    # while loop was terminated before the grid was solved.
    else:
        print "A solution was not found within %i iterations." %it[1]

if __name__ == "__main__":
    main()
