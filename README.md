# sudoku-solver

This program was inspired by a similar project a friend was working on. I was
interested in the challenge of devising an algorithm for solving sudoku
puzzles, and implementing it.

I've chosen python as I've been using it a lot lately. The current software
design is probably not the most efficient or pythonic, but my emphasis is on
getting working and well documented code.

# usage

Clone this repository into a folder on your computer, or download the file
directly. 

Import sudoku\_solver.py into your module or python shell. Instantiate the
class SudokuTable with a 9x9 list of lists of integers: 1-9 for the starting
cells, and 0 for unknown cells. This should look like the following:

```python
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
```

And thus creating a class will be:

```python
st = sudoku_solver.SudokuTable(EASY)
```

The given sudoku puzzle can be solved, and the solution displayed, with:

```python
st.solve()
st.print_grid()
```

See the module documentation with `pydoc sudoku_solver` for more details.

# licence

See `LICENCE.md`.
