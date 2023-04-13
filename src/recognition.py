"""
Implements functionality regarding the recognition of an input grid.

Author: Marek Dohnal

Date: 17/03/2023
"""

import numpy as np
from states import State
from alphabet import Alphabet
from tiles import Tile, TileGrid


def recognize_tiles(grid, num_of_tiles_on_rows):
    """
    Recognizes tiles from an input grid and returns them as a 2D array.

    :param grid: is the input grid containing tiles
    :param num_of_tiles_on_rows: is a list representing a pattern given
        by the number of tiles on rows
    :return: array of tiles
    """

    tile_grid = TileGrid()
    tile_num = 1
    state = State.S0
    row = 1
    col = 1
    while True:
        tile = Tile()
        state, row, col = _find_new_beginning_(grid, row, col)
        if state == State.Sr:
            break

        # Handle incorrectly specified input grid
        try:
            grid = _fill_tile_(grid, row, col, tile)
        except IndexError:
            return None

        tile.set_size()
        tile_grid.add_tile(tile, tile_num, num_of_tiles_on_rows)
        tile_num += 1

    tile_grid.sort_tiles()
    tile_grid.to_rect_shape()

    for row, col in np.ndindex(grid.shape):
        if grid[row][col] == Alphabet.FILL_BEGIN.value:
            grid[row][col] = Alphabet.FILL.value
    return tile_grid


def _find_new_beginning_(grid, start_row, start_col):
    """
    Finds the beginning of a new tile based on a grid and current position.
    """

    row = start_row
    col = start_col
    state = State.S0

    # TODO: Maybe delete this check
    x_size, y_size = np.shape(grid)

    if row >= (x_size - 1) or col >= (y_size - 1):
        raise Exception('Recognition out of grid bounds!')

    while True:
        # State S0
        if state == State.S0:
            # Value E
            if grid[row][col] == Alphabet.EMPTY.value:
                state = State.Sa
            # Value #
            elif grid[row][col] == Alphabet.IMG_BORDER.value:
                state = State.S1
                # Jump to next row
                row += 1
                col = 1
            else:
                state = State.S0
                # Move right
                col += 1
        # State S1
        elif state == State.S1:
            # Value #
            if grid[row][col] == Alphabet.IMG_BORDER.value:
                state = State.Sr
            else:
                state = State.S0
        # State Sr or Sa
        else:
            break

    if state == State.Sa:
        # Place new fill beginning
        grid[row][col] = Alphabet.FILL_BEGIN.value

    return state, row, col


def _apply_buffer_(grid, fill_buffer):
    """ Applies the buffer of changes to the grid. """

    for row, col in fill_buffer:
        grid[row][col] = Alphabet.FILL.value
    # Place F_B
    if len(fill_buffer) > 0:
        row, col = fill_buffer[0]
        grid[row][col] = Alphabet.FILL_BEGIN.value
    return grid


def _fill_down_(grid, start_row, start_col, fill_buffer):
    """ Fills the tile down in one layer. Returns modified fill buffer, and end position. """

    row = start_row
    col = start_col
    state = State.D0

    while True:
        # BEGIN FILL DOWN AUTOMATON

        if state == State.D0:
            if grid[row][col] == Alphabet.FILL_BEGIN.value:
                state = State.D1
                # Move right
                col += 1
            else:
                # Reject
                state = State.Dr
        elif state == State.D1:
            if grid[row][col] == Alphabet.EMPTY.value:
                state = State.D4
            else:
                state = State.D2
                # Move left
                col -= 1
        elif state == State.D2:
            state = State.D3
            # Move down
            row += 1
        elif state == State.D3:
            if grid[row][col] == Alphabet.EMPTY.value:
                state = State.D4
            else:
                state = State.Dr
                # Move up
                row -= 1
        elif state == State.D4:
            if grid[row][col] == Alphabet.EMPTY.value:
                state = State.D4
                # Move right
                col += 1
            else:
                state = State.D5
                # Move left
                col -= 1
        elif state == State.D5:
            state = State.D6
            # Move Down
            row += 1
        elif state == State.D6:
            if grid[row][col] == Alphabet.EMPTY.value:
                state = State.D4
                # Move right
                col += 1
            else:
                state = State.D7
                # Move up
                row -= 1
        elif state == State.D7:
            state = State.D8
            # Move left
            col -= 1
        elif state == State.D8:
            if grid[row][col] == Alphabet.EMPTY.value:
                state = State.D6
                # Move down
                row += 1
            else:
                state = State.Da
                # Move right
                col += 1
        # State Da or Dr
        else:
            break
        # END OF AUTOMATON

        # Add empty cell to buffer
        if grid[row][col] == Alphabet.EMPTY.value:
            fill_buffer.append((row, col))
        # End of loop
    return state, row, col, fill_buffer


def _fill_up_(grid, start_row, start_col, fill_buffer):
    """ Fills tile up based on input grid. Returns modified fill buffer, and end position. """

    row = start_row
    col = start_col
    state = State.U0

    while True:
        # BEGIN FILL DOWN AUTOMATON
        if state == State.U0:
            if grid[row][col] == Alphabet.EMPTY.value:
                state = State.U0
                # Move left
                col -= 1
            elif grid[row][col] == Alphabet.FILL_BEGIN.value:
                state = State.Ua
            else:
                state = State.U1
                # Move right
                col += 1
        elif state == State.U1:
            state = State.U2
            # Move up
            row -= 1
        elif state == State.U2:
            if grid[row][col] == Alphabet.EMPTY.value:
                state = State.U0
                # Move left
                col -= 1
            elif grid[row][col] == Alphabet.FILL_BEGIN.value:
                state = State.Ua
            else:
                state = State.U3
                # Move down
                row += 1
        elif state == State.U3:
            state = State.U4
            # Move right
            col += 1
        elif state == State.U4:
            state = State.U2
            # Move up
            row -= 1
        else:
            break
        # END OF AUTOMATON

        # Add empty cell to buffer
        if grid[row][col] == Alphabet.EMPTY.value:
            fill_buffer.append((row, col))
        # End of loop
    # TODO: Maybe add a timeout or a rejecting state
    return state, row, col, fill_buffer


def _find_new_fill_beginning_(grid, start_row, start_col):
    """ Finds new fill beginning (F_B) based on grid and current position """

    row = start_row
    col = start_col
    state = State.N0

    while True:
        if state == State.N0:
            if grid[row][col] == Alphabet.FILL_BEGIN.value:
                state = State.N1
                # Move right
                col += 1
        elif state == State.N1:
            if grid[row][col] == Alphabet.FILL.value:
                state = State.N1
                # Move right
                col += 1
            elif grid[row][col] == Alphabet.EMPTY.value:
                state = State.Na
            else:
                state = State.N2
                # Move left
                col -= 1
        elif state == State.N2:
            state = State.N3
            # Move down
            row += 1
        elif state == State.N3:
            if (grid[row][col] == Alphabet.EMPTY.value
                    or grid[row][col] == Alphabet.FILL.value):
                state = State.N6
                # Move left
                col -= 1
            else:
                state = State.N4
                # Move up
                row -= 1
        elif state == State.N4:
            state = State.N5
            # Move left
            col -= 1
        elif state == State.N5:
            if (grid[row][col] == Alphabet.TILE_BORDER.value
                    or grid[row][col] == Alphabet.IMG_BORDER.value):
                state = State.Nr
                # Move right
                col += 1
            else:
                state = State.N3
                # Move down
                row += 1
        elif state == State.N6:
            if (grid[row][col] == Alphabet.EMPTY.value
                    or grid[row][col] == Alphabet.FILL.value):
                state = State.N6
                # Move left
                col -= 1
            else:
                state = State.N1
                # Move right
                col += 1
        else:
            break

    if state == State.Na:
        # Place new fill beginning
        grid[row][col] = Alphabet.FILL_BEGIN.value

    return state, row, col


def _fill_tile_(grid, start_row, start_col, tile):
    """ Fills the current tile, returns modified grid with filled tile and
        inserts a new tile into the tile array.
    """

    row = start_row
    col = start_col

    while True:
        # Init buffer with F_B
        fill_buffer = [(row, col)]
        # Fill down
        state, row, col, fill_buffer = _fill_down_(grid, row, col, fill_buffer)
        # This F_B is the last one, nothing is left to fill
        if state == State.Da:
            # Fill up
            state, row, col, fill_buffer = _fill_up_(grid, row, col, fill_buffer)
        # Apply buffer
        grid = _apply_buffer_(grid, fill_buffer)
        # Find new F_B
        state, row, col = _find_new_fill_beginning_(grid, row, col)
        # Add buffer as a tile layer
        tile.add_fill_layer(fill_buffer)
        if state == State.Nr:
            break

    return grid
