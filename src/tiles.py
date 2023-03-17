import numpy as np
from shapes import Shape, Shapes
import random
from alphabet import Alphabet


class Tile:
    def __init__(self, fill_layers=None,
                 color=(255, 0, 0),
                 shape=None,
                 size=5):
        if fill_layers is None:
            fill_layers = []
        self.fill_layers = fill_layers
        self.color = color
        if shape is None:
            shape = Shape()
        self.shape = shape
        self.size = size

    def add_fill_layer(self, fill_layer):
        self.fill_layers.append(fill_layer)

    def set_size(self):
        self.size = len(self.fill_layers)

    def __str__(self):
        try:
            return str(self.fill_layers[0][0])
        except IndexError:
            return "PHANTOM"


class TileGrid:
    def __init__(self, grid=None):
        if grid is None:
            grid = []
        self.grid = grid
        self.grid.append([])

    def add_tile(self, tile, tile_num, num_of_tiles_on_rows):
        """
        Adds tile to the tile grid
        :param tile is the tile to be added
        :param tile_num is the number of the tile, in order of recognition
        :param num_of_tiles_on_rows is a list of
        """
        sum_of_tiles = 0
        while sum_of_tiles <= tile_num:
            for num_of_tiles in num_of_tiles_on_rows:
                # We start next row on the next tile
                if sum_of_tiles == tile_num - 1 and sum_of_tiles != 0:
                    self.grid.append([])
                sum_of_tiles += num_of_tiles

        self.grid[-1].append(tile)

    def sort_tiles(self):
        def get_key(tile):
            first_row, first_col = tile.fill_layers[0][0]
            return first_col

        for row in self.grid:
            row.sort(key=get_key)

    def to_square(self):
        longest_row = 0
        for row in self.grid:
            row_len = len(row)
            if row_len > longest_row:
                longest_row = row_len

        for row in self.grid:
            if len(row) < longest_row:
                row_len = len(row)
                while row_len < longest_row:
                    diff = longest_row - row_len
                    if diff % 2 == 0:
                        row.insert(0, Tile())
                        row.append(Tile())
                        row_len += 2
                    else:
                        row.append(Tile())
                        row_len += 1

    def init_tile_attributes(self, colors, shapes):
        for row in self.grid:
            for tile in row:
                tile_color_rand = random.random()
                shape_color_rand = random.random()
                for color, occurrence in colors:
                    if tile_color_rand < occurrence:
                        tile.color = color
                        break

                tile.shape.color = tile.color
                while tile.shape.color == tile.color:
                    for color, occurrence in colors:
                        if shape_color_rand < occurrence and color != tile.color:
                            tile.shape.color = color
                            break
                tile.shape.type = shapes[random.randint(0, len(shapes) - 1)]
                tile.shape.size = random.randint(int(tile.size/4 ), tile.size)

    @staticmethod
    def _extend_tile_into_borders_(orig_grid, out_img):
        grid = np.copy(orig_grid)
        found_border = True
        while found_border:
            found_border = False
            buffer = []
            for row, row_value in enumerate(grid):
                for col, col_value in enumerate(row_value):
                    if grid[row][col] == Alphabet.TILE_BORDER.value:
                        found_border = True
                        if grid[row][col - 1] == Alphabet.FILL.value:
                            buffer.append(((row, col), out_img[row][col - 1]))
                        elif grid[row][col + 1] == Alphabet.FILL.value:
                            buffer.append(((row, col), out_img[row][col + 1]))
                        elif grid[row - 1][col] == Alphabet.FILL.value:
                            buffer.append(((row, col), out_img[row - 1][col]))
                        elif grid[row + 1][col] == Alphabet.FILL.value:
                            buffer.append(((row, col), out_img[row + 1][col]))
            for (row, col), color in buffer:
                grid[row][col] = Alphabet.FILL.value
                out_img[row][col] = color

    def to_image(self, grid, border_color=None):
        height, width = grid.shape
        fill_borders = False
        if border_color is None:
            border_color = (0, 0, 0)
            fill_borders = True
        out_img = np.full((height, width, 3), border_color, dtype=np.uint8)
        for row in self.grid:
            for tile in row:
                if len(tile.fill_layers) > 0:
                    if tile.shape.type == Shapes.CONTOUR:
                        for layer_idx, fill_layer in enumerate(tile.fill_layers):
                            for pixel_row, pixel_col in fill_layer:
                                if layer_idx >= len(tile.fill_layers) - tile.shape.size:
                                    out_img[pixel_row][pixel_col] = tile.shape.color
                                else:
                                    out_img[pixel_row][pixel_col] = tile.color
                    else:
                        tile_max_row = 0
                        tile_max_col = 0
                        tile_min_row = height
                        tile_min_col = width
                        for fill_layer in tile.fill_layers:
                            for pixel_row, pixel_col in fill_layer:
                                if pixel_row > tile_max_row:
                                    tile_max_row = pixel_row
                                if pixel_col > tile_max_col:
                                    tile_max_col = pixel_col

                                if pixel_row < tile_min_row:
                                    tile_min_row = pixel_row
                                if pixel_col < tile_min_col:
                                    tile_min_col = pixel_col

                                out_img[pixel_row][pixel_col] = tile.color
                        tile.shape.draw(grid, out_img, tile.fill_layers[-1][-1])
        # Remove # borders
        if fill_borders:
            self._extend_tile_into_borders_(grid, out_img)
        out_img = out_img[1:-1, 1:-1]
        return out_img

    @staticmethod
    def _direction_to_coords_(direction, row, col):
        dir_dict = {
            "U": (row - 1, col),
            "D": (row + 1, col),
            "L": (row, col - 1),
            "R": (row, col + 1),
            "UL": (row - 1, col - 1),
            "UR": (row - 1, col + 1),
            "DL": (row + 1, col - 1),
            "DR": (row + 1, col + 1),
        }
        return dir_dict[direction]

    def apply_transformation_step(self, smaller_shape_dir, lighter_bg_color_dir, lighter_shape_color_dir):
        buffer = []
        swapped = False
        for row, row_content in enumerate(self.grid):
            for col, tile in enumerate(row_content):
                if smaller_shape_dir is not None:
                    comp_tile_row, comp_tile_col = self._direction_to_coords_(smaller_shape_dir, row, col)
                    if (0 <= comp_tile_col < len(row_content) and
                            0 <= comp_tile_row < len(self.grid)):
                        comp_tile = self.grid[comp_tile_row][comp_tile_col]
                        if tile.shape.size > comp_tile.shape.size:
                            # buffer.append((tile, comp_tile))
                            temp = tile.shape
                            tile.shape = comp_tile.shape
                            comp_tile.shape = temp
                            swapped = True
                if lighter_bg_color_dir is not None:
                    comp_tile_row, comp_tile_col = self._direction_to_coords_(lighter_bg_color_dir, row, col)
                    if (0 <= comp_tile_col < len(row_content) and
                            0 <= comp_tile_row < len(self.grid)):
                        comp_tile = self.grid[comp_tile_row][comp_tile_col]
                        if sum(tile.color) > sum(comp_tile.color):
                            # buffer.append((tile, comp_tile))
                            temp = tile.color
                            tile.color = comp_tile.color
                            comp_tile.color = temp
                            swapped = True
                if lighter_shape_color_dir is not None:
                    comp_tile_row, comp_tile_col = self._direction_to_coords_(lighter_shape_color_dir, row, col)
                    if (0 <= comp_tile_col < len(row_content) and
                            0 <= comp_tile_row < len(self.grid)):
                        comp_tile = self.grid[comp_tile_row][comp_tile_col]
                        if sum(tile.shape.color) > sum(comp_tile.shape.color):
                            # buffer.append((tile, comp_tile))
                            temp = tile.shape.color
                            tile.shape.color = comp_tile.shape.color
                            comp_tile.shape.color = temp
                            swapped = True
        return swapped

    def __str__(self):
        out = ""
        row_lens = ""
        for row in self.grid:
            row_lens += f"{len(row)} "
            for tile in row:
                out += str(tile)
                out += " "
            out += "\n"
        out += f"Number of rows: {len(self.grid)} \n"
        out += f"Number of columns: {row_lens}"
        return out
