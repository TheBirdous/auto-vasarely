"""
auto_vasarely: tiles.py module
Author: Marek Dohnal
Date: 18/03/2023
"""
import numpy as np
from shapes import Shape, Shapes
import random
from alphabet import Alphabet


class Tile:
    """
    Represents a tile from the input grid.
    """
    def __init__(self, fill_layers=None,
                 color=(255, 0, 0),
                 shape=None,
                 size=5):
        if fill_layers is None:
            fill_layers = []
        self.fill_layers = fill_layers
        """ Layers filled during recognition containing pixel coordinates (row, col) on the input grid """
        self.color = color
        """ The background color of the tile (R, G, B) """
        if shape is None:
            shape = Shape()
        self.shape = shape
        """ Inner shape of the tile """
        self.size = size
        """ Tile size is the number of fill layers """

    def add_fill_layer(self, fill_layer):
        """
        Adds a fill layer to the tile
        :param fill_layer: A fill layer filled during recognition
        """
        self.fill_layers.append(fill_layer)

    def set_size(self):
        """
        Sets the size of the tile based on the length of fill layers.
        """
        self.size = len(self.fill_layers)

    def __str__(self):
        """
        Converts a tile into a string containing the coordinates of
        the first point in it's fill_layers.
        The word PHANTOM is returned if it's a virtual tile.
        """
        try:
            return str(self.fill_layers[0][0])
        except IndexError:
            return "PHANTOM"


class TileGrid:
    """
    Represents an array of tiles, is an abstraction of the input grid.
    """
    def __init__(self, grid=None):
        if grid is None:
            grid = []
        self.grid = grid
        """ Two dimensional array containing tiles """
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
        """
        Sorts tiles in a row in ascending order based
        on the column of the first point in fill layers.
        """
        def get_key(tile):
            first_row, first_col = tile.fill_layers[0][0]
            return first_col

        for row in self.grid:
            row.sort(key=get_key)

    def to_rect_shape(self):
        """
        Converts the tile grid into a rectangular shape if
        it has rows of different lengths.
        """
        longest_row = 0

        # Get length of longest row
        for row in self.grid:
            row_len = len(row)
            if row_len > longest_row:
                longest_row = row_len

        for row in self.grid:
            if len(row) < longest_row:
                row_len = len(row)
                while row_len < longest_row:
                    diff = longest_row - row_len
                    # Row differs by an even number, add 2 tiles
                    # one at the beginning
                    # one at the end
                    if diff % 2 == 0:
                        row.insert(0, Tile())
                        row.append(Tile())
                        row_len += 2
                    else:
                        row.append(Tile())
                        row_len += 1

    def init_tile_attributes(self, bg_colors, shape_colors, shapes):
        """
        Represents an initial permutation of the tile grid.
        Tiles are initialized with specified values.
        :param shape_colors: A list of shape colors and their occurrences
        :param bg_colors: A list of background colors and their occurrences
        :param shapes: A list of shapes to choose from randomly
        """

        for row in self.grid:
            for tile in row:
                tile_color_rand = random.random()
                shape_color_rand = random.random()
                for color, occurrence in bg_colors:
                    if tile_color_rand < occurrence:
                        tile.color = color
                        break

                tile.shape.color = tile.color
                for color, occurrence in shape_colors:
                    if shape_color_rand < occurrence:
                        tile.shape.color = color
                        break
                tile.shape.type = shapes[random.randint(0, len(shapes) - 1)]
                tile.shape.size = random.randint(int(tile.size/4), tile.size)

    @staticmethod
    def _extend_tile_into_borders_(orig_grid, out_img):
        """
        Extends the fill of all tiles into borders, until all borders are erased.
        :param orig_grid: The input grid
        :param out_img: The output image, where borders are erased
        """
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
        """
        Converts the input grid and it's corresponding tile grid into an output image
        :param grid: the input grid
        :param border_color: the color of the tile borders, if None, then tile fill is extended
                into borders
        :return: output image
        """
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
                        for fill_layer in tile.fill_layers:
                            for pixel_row, pixel_col in fill_layer:
                                out_img[pixel_row][pixel_col] = tile.color
                        tile.shape.draw(grid, out_img, tile.fill_layers[-1][-1])
        # Remove # borders
        if fill_borders:
            self._extend_tile_into_borders_(grid, out_img)
        out_img = out_img[1:-1, 1:-1]
        return out_img

    @staticmethod
    def _direction_to_coords_(direction, row, col):
        """
        :param direction: A relative direction from the perspective of a central
        cell in a Moore neighbourhood
        :param row: row of the central cell
        :param col: column of the central cell
        :return: absolute coordinates of a cell in the chosen direction
        """
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

    def apply_transformation_step(self, smaller_shape_dir=None, lighter_bg_color_dir=None,
                                  lighter_shape_color_dir=None, is_sorted_by_type=False):
        """
        Applies a transformation (sorting) step according to specified properties
        :param is_sorted_by_type: True if sort by shape type is wished to be applied, false otherwise
        :param smaller_shape_dir: direction of movement of a tile with a smaller shape
        :param lighter_bg_color_dir: direction of movement of a tile with a lighter background color
        :param lighter_shape_color_dir: direction of movement of a tile with a lighter shape color
        :return: true if the order of anything was changed.
        """
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
                            temp = tile.shape.size
                            tile.shape.size = comp_tile.shape.size
                            comp_tile.shape.size = temp
                            swapped = True
                if lighter_bg_color_dir is not None:
                    comp_tile_row, comp_tile_col = self._direction_to_coords_(lighter_bg_color_dir, row, col)
                    if (0 <= comp_tile_col < len(row_content) and
                            0 <= comp_tile_row < len(self.grid)):
                        comp_tile = self.grid[comp_tile_row][comp_tile_col]
                        if sum(tile.color) < sum(comp_tile.color):
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
                        if sum(tile.shape.color) < sum(comp_tile.shape.color):
                            # buffer.append((tile, comp_tile))
                            temp = tile.shape.color
                            tile.shape.color = comp_tile.shape.color
                            comp_tile.shape.color = temp
                            swapped = True
                if is_sorted_by_type and tile.shape.type != Shapes.CONTOUR:
                    shape_type_to_dir = {
                        Shapes.TRIANGLE_UP: "U",
                        Shapes.TRIANGLE_DOWN: "D",
                        Shapes.SQUARE: "L",
                        Shapes.SQUARE_45DEG: "R"
                    }
                    type_dir = shape_type_to_dir[tile.shape.type]
                    comp_tile_row, comp_tile_col = self._direction_to_coords_(type_dir, row, col)
                    if (0 <= comp_tile_col < len(row_content) and
                            0 <= comp_tile_row < len(self.grid)):
                        comp_tile = self.grid[comp_tile_row][comp_tile_col]
                        # buffer.append((tile, comp_tile))
                        if tile.shape.type != comp_tile.shape.type:
                            temp = tile.shape.type
                            tile.shape.type = comp_tile.shape.type
                            comp_tile.shape.type = temp
                            swapped = True
        return swapped

    def __str__(self):
        """
        Coverts a tile grid into a string containing the coordiantes of tiles
        and a basic description
        :return: Stringified TileGrid
        """
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
