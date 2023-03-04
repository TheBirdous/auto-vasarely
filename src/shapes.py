from enum import Enum, auto
from alphabet import Alphabet
import numpy as np


class Shapes(Enum):
    TRIANGLE_UP = 1
    TRIANGLE_DOWN = 2
    SQUARE = 3
    SQUARE_45DEG = 4
    CONTOUR = 5


class Shape:
    def __init__(self, fill_layers=None,
                 color=(120, 0, 0),
                 size=10,
                 type=Shapes.SQUARE_45DEG):
        if fill_layers is None:
            fill_layers = []
        self.fill_layers = fill_layers
        self.color = color
        self.size = size
        self.type = type

    def draw(self, grid, out_img, start, tile_min, tile_max):
        grid_copy = np.copy(grid)
        buffer = []
        start_row, start_col = start

        if self.size > 0:
            grid_copy[start_row][start_col] = Alphabet.SHAPE.value
            out_img[start_row][start_col] = self.color

        for layer_cnt in range(self.size):
            tile_min_row, tile_min_col = tile_min
            tile_max_row, tile_max_col = tile_max
            for row in range(tile_min_row, tile_max_row + 1):
                for col in range(tile_min_col, tile_max_col + 1):
                    if grid_copy[row][col] == Alphabet.SHAPE.value:
                        # Test with square 45Deg
                        neighbourhood = [(row, col + 1), (row, col - 1),
                                         (row + 1, col), (row - 1, col)]
                        try:
                            for neigh_row, neigh_col in neighbourhood:
                                if (grid_copy[neigh_row][neigh_col] == Alphabet.IMG_BORDER.value or
                                        grid_copy[neigh_row][neigh_col] == Alphabet.TILE_BORDER.value):
                                    return
                                else:
                                    buffer.append((neigh_row, neigh_col))
                        except IndexError:
                            return
            # Apply buffer
            for row, col in buffer:
                grid_copy[row][col] = Alphabet.SHAPE.value
                out_img[row][col] = self.color
            buffer = []
