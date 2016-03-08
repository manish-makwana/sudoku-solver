#!/usr/bin/python

"""Solves Sudoku puzzles.

Attributes:
    EASY: An easy sudoku puzzle.
    MEDIUM: A medium difficulty sudoku puzzle.
    MEDIUM2: Another medium difficulty sudoku puzzle.
    HARD: Hard difficulty puzzle.
    SudokuTable(grid): A class for storing puzzle data, and methods for
        solving and displaying it.
    main(): Create a SudokuTable instance with one of the given puzzles
        and solve it. The results are printed in human-readable format.
"""

# Note: Code checked with pylint version 1.1.0-1. Several of the disabled
#   warnings in this module are no longer applicable in the latest version.


import numpy
import unittest
from collections import namedtuple
Result = namedtuple("Result", ["solved", "iterations"])
a = Result(True, 5)
print a


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

HARD = [
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,3, 0,8,5],
    [0,0,1, 0,2,0, 0,0,0],

    [0,0,0, 5,0,7, 0,0,0],
    [0,0,4, 0,0,0, 1,0,0],
    [0,9,0, 0,0,0, 0,0,0],

    [5,0,0, 0,0,0, 0,7,3],
    [0,0,2, 0,1,0, 0,0,0],
    [0,0,0, 0,4,0, 0,0,9]]


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

    def lists_in_group(self, group):    # pylint: disable-no-self-use
        """Return the unconfirmed numbers in a group (row, col or 3x3 grid)."""
        return [cell for cell in group if type(cell) is list]


    def remove_duplicates(self, group):
        """Remove duplicates between confirmed numbers in group and possible
        numbers for that cell.

        Args:
            group: A list containing integers for confirmed sudoku numbers,
                and lists of possible numbers for unconfirmed cells.
        Returns:
            A list containing integers for confirmed numbers, and lists of
            possible numbers for unconfirmed cells.
        """
        lst = []
        while lst != temp_lst:
            for cell in group:
                # Cell is a confirmed number.
                if isinstance(cell, int):
                    lst.append(cell)

                # Cell is confirmed, but formatted as list.
                elif len(cell) == 1:
                    lst.append(cell[0])

                else:
                    # Compare current unconfirmed numbers for cell against
                    # confirmed numbers in the entire group.
                    nums = self.nums_in_group(group)
                    reduced_poss = [poss for poss in cell if not poss in nums]
                    if len(reduced_poss) == 1:
                        lst.append(reduced_poss[0])
                    else:
                        lst.append(reduced_poss)
            temp_lst = lst
        #self.find_hidden_confirmed(lst)

        return lst

    def find_hidden_confirmed(self, group):
        # Compare unconfirmed numbers against other unconfirmed
        # numbers. If it only appears once, it must be confirmed.
        num_count = [0] * 10
        cell_pos = [0] * 10
        for i, cell in enumerate(group):
            if type(cell) is list:
                for num in cell:
                    num_count[num] += 1
                    cell_pos[num] = i
        if num_count.count(1) == 1:
            confirmed_num = num_count.index(1)
            group[cell_pos[confirmed_num]] = confirmed_num
        return group

    def hidden_by_row_col_seg(self):
        # By row.
        new_grid = []
        # Go through grid row by row.
        for row in self.grid:
            new_grid.append(self.find_hidden_confirmed(row))
        self.grid = new_grid

        # By column.
        new_grid = []
        trans_grid = self.transpose_grid(self.grid)
        for col in trans_grid:
            new_grid.append(self.find_hidden_confirmed(col))
        self.grid = self.transpose_grid(new_grid)

        # By segment.
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
            s = self.find_hidden_confirmed(s)
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

    def process_rows(self, grid):
        """Iterate through Sudoku grid by rows, confirming known numbers."""
        new_grid = []
        # Go through grid row by row.
        for row in grid:
            new_grid.append(self.remove_duplicates(row))
        return new_grid

    def process_cols(self):
        """Iterate through Sudoku grid by columns, confirming known numbers."""
        # Transpose.
        trans_grid = self.transpose_grid(self.grid)
        # Confirm numbers.
        new_grid = self.process_rows(trans_grid)
        # Transpose back to original layout.
        self.grid = self.transpose_grid(new_grid)

    def transpose_grid(self, grid):
        """Transpose grid so rows become columns and vice versa."""
        # pylint: disable=bad-builtin
        # pylint: disable=star-args
        trans_grid = map(list, zip(*grid))
        return trans_grid

    def process_segments(self):
        """Split 9x9 grid into 9 segments, then check for confirmed numbers
        in each."""

        # Divide grid into segments.
        # pylint: disable=too-many-locals
        # pylint: disable=invalid-name
        # pylint: disable=no-member
        # -------------------
        # |     |     |     |
        # |  a  |  d  |  g  |
        # |     |     |     |
        # |------------------
        # |     |     |     |
        # |  b  |  e  |  h  |
        # |     |     |     |
        # |------------------
        # |     |     |     |
        # |  c  |  f  |  i  |
        # |     |     |     |
        # |------------------
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
        prev_grid = []
        while solved == False:
            #import pdb; pdb.set_trace()
            count += 1
            # Check for confirmed numbers.
            self.grid = self.process_rows(self.grid)
            self.process_cols()
            #import pdb; pdb.set_trace()
            self.process_segments()
            solved = True

            # Program can't progress with current algorithms - same results as
            # last iteration.
            if self.grid == prev_grid:
                self.hidden_by_row_col_seg()

            prev_grid = self.grid

            # Clear solved flag if any cell still contains multiple
            # possibilities.
            for row in self.grid:
                for cell in row:
                    if type(cell) == list:
                        solved = False
            if count > 50:
                break
        return (solved, count)

class SudokuTableTests(unittest.TestCase):
    """Unit tests."""

    def test_initial_grid_populates_guesses(self):
        st = SudokuTable(EASY)
        expected = [
            [5,3,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],7,[1,
            2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4,
            5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]], [6,[1, 2, 3, 4, 5, 6,
            7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 1,9,5, [1, 2, 3, 4, 5, 6, 7,
            8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9]],
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],9,8, [1, 2, 3, 4, 5, 6, 7, 8, 9],[1,
            2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4,
            5, 6, 7, 8, 9],6, [1, 2, 3, 4, 5, 6, 7, 8, 9]], [8,[1, 2, 3, 4, 5,
            6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8,
            9],6,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],[1,
            2, 3, 4, 5, 6, 7, 8, 9],3], [4,[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2,
            3, 4, 5, 6, 7, 8, 9], 8,[1, 2, 3, 4, 5, 6, 7, 8, 9],3, [1, 2, 3, 4,
            5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 1], [7,[1, 2, 3, 4, 5,
            6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8,
            9],2,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],[1,
            2, 3, 4, 5, 6, 7, 8, 9],6], [[1, 2, 3, 4, 5, 6, 7, 8, 9],6,[1, 2,
            3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5,
            6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 2,8, [1, 2, 3, 4, 5, 6, 7,
            8, 9]], [[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 4,1,9, [1, 2, 3, 4, 5, 6, 7, 8, 9],[1,
            2, 3, 4, 5, 6, 7, 8, 9],5], [[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3,
            4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6,
            7, 8, 9],8,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8,
            9],7,9]]
        self.assertEqual(st.grid, expected)

    def test_nums_in_group(self):
        st = SudokuTable(EASY)
        a = [1,2,3,4,5,6,7,8,9]
        self.assertEqual(st.nums_in_group(a), a)
        b = [1,2,3,4,5,6,7,[8,9],[8,9]]
        self.assertEqual(st.nums_in_group(b),
                         [1,2,3,4,5,6,7])
        c = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[7,9]]
        self.assertEqual(st.nums_in_group(c), [])

    def test_lists_in_group(self):
        st = SudokuTable(EASY)
        a = [1,2,3,4,5,6,7,8,9]
        self.assertEqual(st.lists_in_group(a), [])
        b = [1,2,3,4,5,6,7,[8,9],[8,9]]
        self.assertEqual(st.lists_in_group(b), [[8,9],[8,9]])
        c = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[7,9]]
        self.assertEqual(st.lists_in_group(c), c)

    def test_remove_duplicates(self):
        st = SudokuTable(EASY)
        a = [1,2,3,4,5,6,7,8,9]
        self.assertEqual(st.remove_duplicates(a), a)
        b = [1,2,3,4,5,6,7,8,[8,9]]
        self.assertEqual(st.remove_duplicates(b),
                         [1,2,3,4,5,6,7,8,9])
        c = [1,2,3,[3,4],5,6,7,8,[8,9]]
        self.assertEqual(st.remove_duplicates(c),
                         [1,2,3,4,5,6,7,8,9])
        d = [1,2,3,[3,4,8],5,6,7,8,[8,9]]
        self.assertEqual(st.remove_duplicates(d),
                         [1,2,3,4,5,6,7,8,9])
        e = [1,2,3,[3,4,8],[5,6],[5,6],7,8,[8,9]]
        self.assertEqual(st.remove_duplicates(e),
                         [1,2,3,4,[5,6],[5,6],7,8,9])

    def test_find_hidden_unconfirmed(self):
        st = SudokuTable(EASY)
        a = [1,2,3,4,5,6,7,8,9]
        self.assertEqual(st.find_hidden_confirmed(a), a)
        b = [[1,2,3],[2,3],[2,3],4,5,6,7,8,9]
        self.assertEqual(st.find_hidden_confirmed(b),
                         [1,[2,3],[2,3],4,5,6,7,8,9])

    def test_process_rows(self):
        easy_input = [
            [5,3,0, 0,7,0, 0,0,0],
            [6,0,0, 1,9,5, 0,0,0],
            [0,9,8, 0,0,0, 0,6,0],

            [8,0,0, 0,6,0, 0,0,3],
            [4,0,0, 8,0,3, 0,0,1],
            [7,0,0, 0,2,0, 0,0,6],

            [0,6,0, 0,0,0, 2,8,0],
            [0,0,0, 4,1,9, 0,0,5],
            [0,0,0, 0,8,0, 0,7,9]]
        easy_1_step = [
            [5,3,[1,2,4,6,8,9], [1,2,4,6,8,9],7,[1,2,4,6,8,9], [1,2,4,6,8,9],[1,2,4,6,8,9],[1,2,4,6,8,9]],
            [6,[2,3,4,7,8],[2,3,4,7,8], 1,9,5, [2,3,4,7,8],[2,3,4,7,8],[2,3,4,7,8]],
            [[1,2,3,4,5,7],9,8, [1,2,3,4,5,7],[1,2,3,4,5,7],[1,2,3,4,5,7], [1,2,3,4,5,7],6,[1,2,3,4,5,7]],

            [8,[1,2,4,5,7,9],[1,2,4,5,7,9], [1,2,4,5,7,9],6,[1,2,4,5,7,9], [1,2,4,5,7,9],[1,2,4,5,7,9],3],
            [4,[2,5,6,7,9],[2,5,6,7,9], 8,[2,5,6,7,9],3, [2,5,6,7,9],[2,5,6,7,9],1],
            [7,[1,3,4,5,8,9],[1,3,4,5,8,9], [1,3,4,5,8,9],2,[1,3,4,5,8,9], [1,3,4,5,8,9],[1,3,4,5,8,9],6],

            [[1,3,4,5,7,9],6,[1,3,4,5,7,9], [1,3,4,5,7,9],[1,3,4,5,7,9],[1,3,4,5,7,9], 2,8,[1,3,4,5,7,9]],
            [[2,3,6,7,8],[2,3,6,7,8],[2,3,6,7,8], 4,1,9, [2,3,6,7,8],[2,3,6,7,8],5],
            [[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6], [1,2,3,4,5,6],8,[1,2,3,4,5,6], [1,2,3,4,5,6],7,9]]

        st = SudokuTable(easy_input)
        grid_rowed = st.process_rows(st.grid)
        self.assertEqual(grid_rowed, easy_1_step)

    def test_process_cols(self):
        easy_input = [
            [5,3,0, 0,7,0, 0,0,0],
            [6,0,0, 1,9,5, 0,0,0],
            [0,9,8, 0,0,0, 0,6,0],

            [8,0,0, 0,6,0, 0,0,3],
            [4,0,0, 8,0,3, 0,0,1],
            [7,0,0, 0,2,0, 0,0,6],

            [0,6,0, 0,0,0, 2,8,0],
            [0,0,0, 4,1,9, 0,0,5],
            [0,0,0, 0,8,0, 0,7,9]]
        easy_1_step = [
            [5,3,[1,2,3,4,5,6,7,9], [2,3,5,6,7,9],7,[1,2,4,6,7,8], [1,3,4,5,6,7,8,9],[1,2,3,4,5,9],[2,4,7,8]],
            [6,[1,2,4,5,7,8],[1,2,3,4,5,6,7,9], 1,9,5, [1,3,4,5,6,7,8,9],[1,2,3,4,5,9],[2,4,7,8]],
            [[1,2,3,9],9,8, [2,3,5,6,7,9],[3,4,5],[1,2,4,6,7,8], [1,3,4,5,6,7,8,9],6,[2,4,7,8]],

            [8,[1,2,4,5,7,8],[1,2,3,4,5,6,7,9], [2,3,5,6,7,9],6,[1,2,4,6,7,8], [1,3,4,5,6,7,8,9],[1,2,3,4,5,9],3],
            [4,[1,2,4,5,7,8],[1,2,3,4,5,6,7,9], 8,[3,4,5],3, [1,3,4,5,6,7,8,9],[1,2,3,4,5,9],1],
            [7,[1,2,4,5,7,8],[1,2,3,4,5,6,7,9], [2,3,5,6,7,9],2,[1,2,4,6,7,8], [1,3,4,5,6,7,8,9],[1,2,3,4,5,9],6],

            [[1,2,3,9],6,[1,2,3,4,5,6,7,9], [2,3,5,6,7,9],[3,4,5],[1,2,4,6,7,8], 2,8,[2,4,7,8]],
            [[1,2,3,9],[1,2,4,5,7,8],[1,2,3,4,5,6,7,9], 4,1,9, [1,3,4,5,6,7,8,9],[1,2,3,4,5,9],5],
            [[1,2,3,9],[1,2,4,5,7,8],[1,2,3,4,5,6,7,9], [2,3,5,6,7,9],8,[1,2,4,6,7,8], [1,3,4,5,6,7,8,9],7,9]]

        st = SudokuTable(easy_input)
        st.process_cols()
        self.assertEqual(st.grid, easy_1_step)

    def test_transpose_grid(self):
        # Check basic list transpose.
        easy_input = [
            [5,3,0, 0,7,0, 0,0,0],
            [6,0,0, 1,9,5, 0,0,0],
            [0,9,8, 0,0,0, 0,6,0],

            [8,0,0, 0,6,0, 0,0,3],
            [4,0,0, 8,0,3, 0,0,1],
            [7,0,0, 0,2,0, 0,0,6],

            [0,6,0, 0,0,0, 2,8,0],
            [0,0,0, 4,1,9, 0,0,5],
            [0,0,0, 0,8,0, 0,7,9]]
        transposed_man = [
            [5,6,0, 8,4,7, 0,0,0],
            [3,0,9, 0,0,0, 6,0,0],
            [0,0,8, 0,0,0, 0,0,0],

            [0,1,0, 0,8,0, 0,4,0],
            [7,9,0, 6,0,2, 0,1,8],
            [0,5,0, 0,3,0, 0,9,0],

            [0,0,0, 0,0,0, 2,0,0],
            [0,0,6, 0,0,0, 8,0,7],
            [0,0,0, 3,1,6, 0,5,9]]
        st = SudokuTable(easy_input)
        transposed_auto = st.transpose_grid(easy_input)
        self.assertEqual(transposed_auto, transposed_man)

        # Check transpose with nested lists.
        easy_input_guesses = [
            [5,3,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],7,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9]],
            [6,[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 1,9,5, [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9]],
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],9,8, [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],6,[1, 2, 3, 4, 5, 6, 7, 8, 9]],

            [8,[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],6,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],3],
            [4,[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 8,[1, 2, 3, 4, 5, 6, 7, 8, 9],3, [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],1],
            [7,[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],2,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],6],

            [[1, 2, 3, 4, 5, 6, 7, 8, 9],6,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 2,8,[1, 2, 3, 4, 5, 6, 7, 8, 9]],
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 4,1,9, [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],5],
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],8,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],7,9]]
        transposed_man_guesses = [
            [5,6,[1, 2, 3, 4, 5, 6, 7, 8, 9], 8,4,7, [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9]],
            [3,[1, 2, 3, 4, 5, 6, 7, 8, 9],9, [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 6,[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9]],
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],8, [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9]],

            [[1, 2, 3, 4, 5, 6, 7, 8, 9],1,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],8,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],4,[1, 2, 3, 4, 5, 6, 7, 8, 9]],
            [7,9,[1, 2, 3, 4, 5, 6, 7, 8, 9], 6,[1, 2, 3, 4, 5, 6, 7, 8, 9],2, [1, 2, 3, 4, 5, 6, 7, 8, 9],1,8],
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],5,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],3,[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],9,[1, 2, 3, 4, 5, 6, 7, 8, 9]],

            [[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 2,[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9]],
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],6, [1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 8,[1, 2, 3, 4, 5, 6, 7, 8, 9],7],
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 2, 3, 4, 5, 6, 7, 8, 9], 3,1,6, [1, 2, 3, 4, 5, 6, 7, 8, 9],5,9]]
        transposed_auto_guesses = st.transpose_grid(easy_input_guesses)
        self.assertEqual(transposed_auto_guesses, transposed_man_guesses)

    def test_process_segments(self):
        easy_input = [
            [5,3,0, 0,7,0, 0,0,0],
            [6,0,0, 1,9,5, 0,0,0],
            [0,9,8, 0,0,0, 0,6,0],

            [8,0,0, 0,6,0, 0,0,3],
            [4,0,0, 8,0,3, 0,0,1],
            [7,0,0, 0,2,0, 0,0,6],

            [0,6,0, 0,0,0, 2,8,0],
            [0,0,0, 4,1,9, 0,0,5],
            [0,0,0, 0,8,0, 0,7,9]]
        easy_1_step = [
            [5,3,[1,2,4,7], [2,3,4,6,8],7,[2,3,4,6,8], [1,2,3,4,5,7,8,9],[1,2,3,4,5,7,8,9],[1,2,3,4,5,7,8,9]],
            [6,[1,2,4,7],[1,2,4,7], 1,9,5, [1,2,3,4,5,7,8,9],[1,2,3,4,5,7,8,9],[1,2,3,4,5,7,8,9]],
            [[1,2,4,7],9,8, [2,3,4,6,8],[2,3,4,6,8],[2,3,4,6,8], [1,2,3,4,5,7,8,9],6,[1,2,3,4,5,7,8,9]],

            [8,[1,2,3,5,6,9],[1,2,3,5,6,9], [1,4,5,7,9],6,[1,4,5,7,9], [2,4,5,7,8,9],[2,4,5,7,8,9],3],
            [4,[1,2,3,5,6,9],[1,2,3,5,6,9], 8,[1,4,5,7,9],3, [2,4,5,7,8,9],[2,4,5,7,8,9],1],
            [7,[1,2,3,5,6,9],[1,2,3,5,6,9], [1,4,5,7,9],2,[1,4,5,7,9], [2,4,5,7,8,9],[2,4,5,7,8,9],6],

            [[1,2,3,4,5,7,8,9],6,[1,2,3,4,5,7,8,9], [2,3,5,6,7],[2,3,5,6,7],[2,3,5,6,7], 2,8,[1,3,4,6]],
            [[1,2,3,4,5,7,8,9],[1,2,3,4,5,7,8,9],[1,2,3,4,5,7,8,9], 4,1,9, [1,3,4,6],[1,3,4,6],5],
            [[1,2,3,4,5,7,8,9],[1,2,3,4,5,7,8,9],[1,2,3,4,5,7,8,9], [2,3,5,6,7],8,[2,3,5,6,7], [1,3,4,6],7,9]]

        st = SudokuTable(easy_input)
        st.process_segments()
        self.assertEqual(st.grid, easy_1_step)

    # def test_process_rows_cols(self):
    #     easy_input_rowed = [
    #         [5,3,[1,2,4,6,8,9], [1,2,4,6,8,9],7,[1,2,4,6,8,9], [1,2,4,6,8,9],[1,2,4,6,8,9],[1,2,4,6,8,9]],
    #         [6,[2,3,4,7,8],[2,3,4,7,8], 1,9,5, [2,3,4,7,8],[2,3,4,7,8],[2,3,4,7,8]],
    #         [[1,2,3,4,5,7],9,8, [1,2,3,4,5,7],[1,2,3,4,5,7],[1,2,3,4,5,7], [1,2,3,4,5,7],6,[1,2,3,4,5,7]],

    #         [8,[1,2,4,5,7,9],[1,2,4,5,7,9], [1,2,4,5,7,9],6,[1,2,4,5,7,9], [1,2,4,5,7,9],[1,2,4,5,7,9],3],
    #         [4,[2,5,6,7,9],[2,5,6,7,9], 8,[2,5,6,7,9],3, [2,5,6,7,9],[2,5,6,7,9],1],
    #         [7,[1,3,4,5,8,9],[1,3,4,5,8,9], [1,3,4,5,8,9],2,[1,3,4,5,8,9], [1,3,4,5,8,9],[1,3,4,5,8,9],6],

    #         [[1,3,4,5,7,9],6,[1,3,4,5,7,9], [1,3,4,5,7,9],[1,3,4,5,7,9],[1,3,4,5,7,9], 2,8,[1,3,4,5,7,9]],
    #         [[2,3,6,7,8],[2,3,6,7,8],[2,3,6,7,8], 4,1,9, [2,3,6,7,8],[2,3,6,7,8],5],
    #         [[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6], [1,2,3,4,5,6],8,[1,2,3,4,5,6], [1,2,3,4,5,6],7,9]]
    #     easy_1_step = [
    #         [5,3,[1,2,4,6,9], [2,6,9],7,[1,2,4,6,8], [1,4,6,8,9],[1,2,4,9],[2,4,8]],
    #         [6,[2,4,7,8],[2,3,4,7], 1,9,5, [3,4,7,8],[2,3,4],[2,4,7,8]],
    #         [[1,2,3],9,8, [2,3,5,7],[3,4,5],[1,2,4,7], [1,3,4,5,7],6,[2,4,7]],

    #         [8,[1,2,4,5,7],[1,2,4,5,7,9], [2,5,7,9],6,[1,2,4,7], [1,4,5,7,9],[1,2,4,5,9],3],
    #         [4,[2,5,7],[2,5,6,7,9], 8,5,3, [5,6,7,9],[2,5,9],1],
    #         [7,[1,4,5,8],[1,3,4,5,9], [3,5,9],2,[1,4,8], [1,3,4,5,8,9],[1,3,4,5,9],6],

    #         [9,6,[1,3,4,5,7,9], [3,5,7,9],[3,4,5],[1,4,7], 2,8,[4,7]],
    #         [[2,3],[2,7,8],[2,3,6,7], 4,1,9, [3,6,7,8],[2,3],5],
    #         [[1,2,3],[1,2,4,5],[1,2,3,4,5,6], [2,3,5,6],8,[1,2,4,6], [1,3,4,5,6],7,9]]

    #     st = SudokuTable(easy_input_rowed)
    #     st.process_cols()
    #     self.assertEqual(st.grid, easy_1_step)

    # def test_process_rows_cols_segs(self):
    #     easy_input = [
    #         [5,3,0, 0,7,0, 0,0,0],
    #         [6,0,0, 1,9,5, 0,0,0],
    #         [0,9,8, 0,0,0, 0,6,0],

    #         [8,0,0, 0,6,0, 0,0,3],
    #         [4,0,0, 8,0,3, 0,0,1],
    #         [7,0,0, 0,2,0, 0,0,6],

    #         [0,6,0, 0,0,0, 2,8,0],
    #         [0,0,0, 4,1,9, 0,0,5],
    #         [0,0,0, 0,8,0, 0,7,9]]
    #     easy_rowed_coled = [
    #         [5,3,[1,2,4,6,9], [2,6,9],7,[1,2,4,6,8], [1,4,6,8,9],[1,2,4,9],[2,4,8]],
    #         [6,[2,4,7,8],[2,3,4,7], 1,9,5, [3,4,7,8],[2,3,4],[2,4,7,8]],
    #         [[1,2,3],9,8, [2,3,5,7],[3,4,5],[1,2,4,7], [1,3,4,5,7],6,[2,4,7]],

    #         [8,[1,2,4,5,7],[1,2,4,5,7,9], [2,5,7,9],6,[1,2,4,7], [1,4,5,7,9],[1,2,4,5,9],3],
    #         [4,[2,5,7],[2,5,6,7,9], 8,5,3, [5,6,7,9],[2,5,9],1],
    #         [7,[1,4,5,8],[1,3,4,5,9], [3,5,9],2,[1,4,8], [1,3,4,5,8,9],[1,3,4,5,9],6],

    #         [9,6,[1,3,4,5,7,9], [3,5,7,9],[3,4,5],[1,4,7], 2,8,[4,7]],
    #         [[2,3],[2,7,8],[2,3,6,7], 4,1,9, [3,6,7,8],[2,3],5],
    #         [[1,2,3],[1,2,4,5],[1,2,3,4,5,6], [2,3,5,6],8,[1,2,4,6], [1,3,4,5,6],7,9]]
    #     easy_1_step = [
    #         [5,3,[1,2,4], [2,6],7,8, [1,4,8,9],[1,2,4,9],[2,4,8]],
    #         [6,[2,4,7],[2,4,7], 1,9,5, [3,4,7,8],[2,3,4],[2,4,7,8]],
    #         [[1,2],9,8, [2,3],[3,4],[2,4], 5,6,[2,4,7]],

    #         [8,[1,2,5],[1,2,5,9], [7,9],6,[1,4,7], [4,5,7,9],[2,4,5,9],3],
    #         [4,[2,5],[2,5,6,9], 8,5,3, [5,7,9],[2,5,9],1],
    #         [7,[1,5],[1,3,5,9], 9,2,[1,4], [4,5,8,9],[4,5,9],6],

    #         [9,6,[1,3,4,5,7,9], [3,5,7],[3,5],7, 2,8,4],
    #         [[2,3],[2,7,8],[2,3,7], 4,1,9, [3,6],3,5],
    #         [[1,2,3],[1,2,4,5],[1,2,3,4,5], [2,3,5,6],8,[2,6], [1,3,4,6],7,9]]

    #     st = SudokuTable(easy_rowed_coled)
    #     st.process_segments()
    #     self.assertEqual(st.grid, easy_1_step)

    def test_solve_easy(self):
        easy_solution_manual = [
            [5,3,4, 6,7,8, 9,1,2],
            [6,7,2, 1,9,5, 3,4,8],
            [1,9,8, 3,4,2, 5,6,7],

            [8,5,9, 7,6,1, 4,2,3],
            [4,2,6, 8,5,3, 7,9,1],
            [7,1,3, 9,2,4, 8,5,6],

            [9,6,1, 5,3,7, 2,8,4],
            [2,8,7, 4,1,9, 6,3,5],
            [3,4,5, 2,8,6, 1,7,9]]

        easy_solution_computed = SudokuTable(EASY)
        easy_solution_computed.solve()
        self.assertEqual(easy_solution_computed.grid, easy_solution_manual)

    def test_solve_medium(self):
        med_solution_manual = [
            [6,2,9, 1,7,8, 4,3,5],
            [8,4,5, 3,6,2, 7,9,1],
            [1,3,7, 5,9,4, 8,2,6],

            [2,7,8, 6,4,3, 5,1,9],
            [3,9,1, 2,8,5, 6,7,4],
            [4,5,6, 7,1,9, 2,8,3],

            [9,6,3, 8,5,7, 1,4,2],
            [5,8,4, 9,2,1, 3,6,7],
            [7,1,2, 4,3,6, 9,5,8]]

        med_solution_computed = SudokuTable(MEDIUM)
        med_solution_computed.solve()
        self.assertEqual(med_solution_computed.grid, med_solution_manual)

    def test_solve_medium2(self):
        easy_solution_manual = [
            [5,3,4, 6,7,8, 9,1,2],
            [6,7,2, 1,9,5, 3,4,8],
            [1,9,8, 3,4,2, 5,6,7],

            [8,5,9, 7,6,1, 4,2,3],
            [4,2,6, 8,5,3, 7,9,1],
            [7,1,3, 9,2,4, 8,5,6],

            [9,6,1, 5,3,7, 2,8,4],
            [2,8,7, 4,1,9, 6,3,5],
            [3,4,5, 2,8,6, 1,7,9]]

        #easy_solution_computed = SudokuTable(MEDIUM2)
        #easy_solution_computed.solve()
        #self.assertEqual(easy_solution_computed.grid, easy_solution_manual)

    def test_solve_hard(self):
        easy_solution_manual = [
            [5,3,4, 6,7,8, 9,1,2],
            [6,7,2, 1,9,5, 3,4,8],
            [1,9,8, 3,4,2, 5,6,7],

            [8,5,9, 7,6,1, 4,2,3],
            [4,2,6, 8,5,3, 7,9,1],
            [7,1,3, 9,2,4, 8,5,6],

            [9,6,1, 5,3,7, 2,8,4],
            [2,8,7, 4,1,9, 6,3,5],
            [3,4,5, 2,8,6, 1,7,9]]

        #easy_solution_computed = SudokuTable(EASY)
        #easy_solution_computed.solve()
        #self.assertEqual(easy_solution_computed.grid, easy_solution_manual)

def solve_test_puzzles():
    """Solve a test Sudoku puzzle using the SudokuTable class and methods."""
    # pylint: disable=invalid-name
    grid_to_solve = MEDIUM
    st = SudokuTable(grid_to_solve)
    print "Starting grid:"
    for row in grid_to_solve:
        print row
    it = st.solve()
    # The grid was solved.
    if it[0] == True:
        print "The solved Sudoku grid is:"
        st.print_grid()
        print "This took %i iterations." %it[1]
    # while loop was terminated before the grid was solved.
    else:
        print "A solution was not found within %i iterations." %it[1]
        print "Best attempt:"
        st.print_confirmed()
        print "With possibilities:"
        st.print_grid()

def main():
    """Run tests."""
    solve_test_puzzles()
    unittest.main()


if __name__ == "__main__":
    main()
