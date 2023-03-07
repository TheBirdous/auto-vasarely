import copy
from enum import Enum, auto
from alphabet import Alphabet
import numpy as np


class Shapes(Enum):
    TRIANGLE_UP = 1
    TRIANGLE_DOWN = 2
    SQUARE = 3
    SQUARE_45DEG = 4
    CONTOUR = 5


SHAPE_FILL_TEMPLATES = {
    Shapes.TRIANGLE_UP: [],
    Shapes.TRIANGLE_DOWN: [],
    Shapes.SQUARE: [],
    Shapes.SQUARE_45DEG: []
}


def _pick_neighbourhood_(shape_type, center_row, center_col):
    if shape_type is Shapes.SQUARE_45DEG:
        return [(center_row, center_col + 1), (center_row, center_col - 1),
                (center_row + 1, center_col), (center_row - 1, center_col)]
    if shape_type is Shapes.SQUARE:
        return [(center_row, center_col + 1), (center_row, center_col - 1),
                (center_row + 1, center_col), (center_row - 1, center_col),
                (center_row + 1, center_col + 1), (center_row - 1, center_col + 1),
                (center_row - 1, center_col - 1), (center_row + 1, center_col - 1)]
    if shape_type is Shapes.TRIANGLE_UP:
        return [(center_row, center_col + 1), (center_row, center_col - 1),
                (center_row + 1, center_col), (center_row - 1, center_col),
                (center_row + 1, center_col + 1), (center_row + 1, center_col + 2),
                (center_row + 1, center_col - 2), (center_row + 1, center_col - 1)]
    if shape_type is Shapes.TRIANGLE_DOWN:
        return [(center_row, center_col + 1), (center_row, center_col - 1),
                (center_row + 1, center_col), (center_row - 1, center_col),
                (center_row - 1, center_col + 1), (center_row - 1, center_col + 2),
                (center_row - 1, center_col - 2), (center_row - 1, center_col - 1)]


def init_shape_fill_templates(tile_grid):
    max_shape_size = 0
    for row in tile_grid.grid:
        for tile in row:
            if tile.shape.size > max_shape_size:
                max_shape_size = tile.shape.size

    growing_space_half_size = max_shape_size*2
    orig_growing_space = []
    for row in range(-growing_space_half_size, growing_space_half_size + 1):
        orig_growing_space.append([])
        for col in range(-growing_space_half_size, growing_space_half_size + 1):
            if row == 0 and col == 0:
                orig_growing_space[-1].append([(row, col), True])
            else:
                orig_growing_space[-1].append([(row, col), False])

    for shape in Shapes:
        if shape != Shapes.CONTOUR:
            growing_space = copy.deepcopy(orig_growing_space)
            for i in range(0, max_shape_size):
                buffer = []
                for row, row_value in enumerate(growing_space):
                    for col, cell in enumerate(row_value):
                        if cell[-1] == True:
                            if i == 0:
                                buffer.append((row, col))
                            neighbourhood = _pick_neighbourhood_(shape, row, col)
                            for neigh_row, neigh_col in neighbourhood:
                                if growing_space[neigh_row][neigh_col][-1] == False:
                                    buffer.append((neigh_row, neigh_col))
                shape_fill_buf = []
                for row, col in buffer:
                    growing_space[row][col][-1] = True
                    shape_fill_buf.append(growing_space[row][col][0])
                SHAPE_FILL_TEMPLATES[shape].append(shape_fill_buf)


class Shape:
    def __init__(self,
                 color=(120, 0, 0),
                 size=10,
                 type=Shapes.SQUARE_45DEG):
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

    def new_draw(self, grid, out_img, start):
        start_row, start_col = start
        for layer_idx in range(0, self.size - 1):
            layer = SHAPE_FILL_TEMPLATES[self.type][layer_idx]
            # Check if layer is within tile
            for template_row, template_col in layer:
                row = start_row + template_row
                col = start_col + template_col
                try:
                    if (grid[row][col] == Alphabet.IMG_BORDER.value or
                            grid[row][col] == Alphabet.TILE_BORDER.value):
                        return
                except IndexError:
                    return
            # Fill tile with layer
            for template_row, template_col in layer:
                row = start_row + template_row
                col = start_col + template_col
                out_img[row][col] = self.color
