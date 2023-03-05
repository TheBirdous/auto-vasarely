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

    def _pick_neighbourhood_(self, center_row, center_col):
        if self.type is Shapes.SQUARE_45DEG:
            return [(center_row, center_col + 1), (center_row, center_col - 1),
                    (center_row + 1, center_col), (center_row - 1, center_col)]
        if self.type is Shapes.SQUARE:
            return [(center_row, center_col + 1), (center_row, center_col - 1),
                    (center_row + 1, center_col), (center_row - 1, center_col),
                    (center_row + 1, center_col + 1), (center_row - 1, center_col + 1),
                    (center_row - 1, center_col - 1), (center_row + 1, center_col - 1)]
        if self.type is Shapes.TRIANGLE_UP:
            return [(center_row, center_col + 1), (center_row, center_col - 1),
                    (center_row + 1, center_col), (center_row - 1, center_col),
                    (center_row + 1, center_col + 1), (center_row + 1, center_col + 2),
                    (center_row + 1, center_col - 2), (center_row + 1, center_col - 1)]
        if self.type is Shapes.TRIANGLE_DOWN:
            return [(center_row, center_col + 1), (center_row, center_col - 1),
                    (center_row + 1, center_col), (center_row - 1, center_col),
                    (center_row - 1, center_col + 1), (center_row - 1, center_col + 2),
                    (center_row - 1, center_col - 2), (center_row - 1, center_col - 1)]

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
                        neighbourhood = self._pick_neighbourhood_(row, col)
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
