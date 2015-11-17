"""Solves Sudoku puzzles.
"""

import tabulate
import numpy

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

# This grid copied from Parth's code.
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
       

class SudokuTable:
    """A class for a 9x9 Sudoku grid, containing relevant data and methods.

    """

    def __init__(self, start_grid):
        """Populate class grid with starting numbers and possible numbers."""
        # Convert zeros to Nones.
        all_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.grid = [[all_nums if cell == 0 else cell for cell in row]
                     for row in start_grid]

    def nums_in_group(self, group):
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
        trans_grid = map(list, zip(*new_grid))

        # Go through grid column by column.
        new_grid = []
        for col in trans_grid:
            new_grid.append(self.remove_duplicates(col))
        
        self.grid = map(list, zip(*new_grid))

    def process_segments(self):
        """Split 9x9 grid into 3x3 segments, then check for confirmed numbers
        in each.
        
        Segments are arranged accordingly:
           a   b   c
           d   e   f
           g   h   i
        """

        # Divide grid into segments.
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
            s = numpy.reshape(s, (3,3))
            processed_segs.append(s)
        # Join up segments back into 9x9 grid.
        new_arr_grid = arr_grid
        new_arr_grid[0:3,0:3] = processed_segs[0]
        new_arr_grid[3:6,0:3] = processed_segs[1]
        new_arr_grid[6:9,0:3] = processed_segs[2]
        new_arr_grid[0:3,3:6] = processed_segs[3]
        new_arr_grid[3:6,3:6] = processed_segs[4]
        new_arr_grid[6:9,3:6] = processed_segs[5]
        new_arr_grid[0:3,6:9] = processed_segs[6]
        new_arr_grid[3:6,6:9] = processed_segs[7]
        new_arr_grid[6:9,6:9] = processed_segs[8]
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

st = SudokuTable(EASY)

print st.grid
for _i in range(20):
    st.process_rows_cols()
    print st.grid
    st.process_segments()
    print st.grid
    st.print_confirmed()
