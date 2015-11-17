"""Solves Sudoku puzzles.
"""

import tabulate
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
        numbers for that cell."""

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


    def process_rows_cols(self, grid):
        """Iterate through Sudoku grid by rows and cols, confirming known 
        numbers.
        """
        new_grid = []
        # Go through grid row by row.
        for row in grid:
            new_grid.append(self.remove_duplicates(row))
       
        # Transpose grid so rows become columns and vice versa.
        trans_grid = map(list, zip(*new_grid))

        # Go through grid column by column.
        new_grid = []
        for col in trans_grid:
            new_grid.append(self.remove_duplicates(col))
        #self.grid = new_grid

    def process_segments(self, grid):
        """Split 9x9 grid into 3x3 segments, then check for confirmed numbers
        in each.
        
        Segments are arranged accordingly:
           a   b   c
           d   e   f
           g   h   i
        """

        # Divide grid into segments.
        arr_grid = numpy.array(new_grid)
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

        # Flatten each segment.
        flat_seg = []
        for seg in segments:
            flat_seg.append(numpy.ravel(seg).tolist())

        # Confirm numbers and reduce possibilities.
        segments = []
        for seg in flat_seg:
            segments.append(self.remove_duplicates(seg))

        # Wrap up each segment and convert back to array.
        segs = []
        for seg in segments:
            #segs.append(numpy.reshape(numpy.array(seg), (3,3)))
            s = numpy.array(seg, dtype=object)
            s_re = numpy.reshape(s, (3,3))
            segs.append(s_re)

        # Join up segments back into 9x9 grid.
        new_arr_grid = arr_grid
        new_arr_grid[0:3,0:3] = segs[0]
        new_arr_grid[3:6,0:3] = segs[1]
        new_arr_grid[6:9,0:3] = segs[2]
        new_arr_grid[0:3,3:6] = segs[3]
        new_arr_grid[3:6,3:6] = segs[4]
        new_arr_grid[6:9,3:6] = segs[5]
        new_arr_grid[0:3,6:9] = segs[6]
        new_arr_grid[3:6,6:9] = segs[7]
        new_arr_grid[6:9,6:9] = segs[8]

        print new_arr_grid


    def confirmed_nums(self):
        return [[0 if type(cell) is list else cell for cell in row]
                     for row in self.grid]

        # TODO: add logic for 3x3 grid reduction.

st = SudokuTable(EASY)

#print st.grid
st.process_rows_cols(st.grid)
#print ""
#print st.grid
#st.process_rows_cols(st.grid)
#print ""
#print st.grid
#st.process_rows_cols(st.grid)
#print ""
#print st.grid
#print tabulate.tabulate(st.confirmed_nums())
#print st.confirmed_nums()
