import numpy as np


class Tile:
    def __init__(self, fill_layers=None,
                 background_color=(255, 0, 0),
                 inner_shape_color=(120, 0, 0),
                 shape_size=10,
                 shape_type=0):
        if fill_layers is None:
            fill_layers = []
        self.fill_layers = fill_layers
        # TODO: Need to find out how to save color
        self.background_color = background_color
        self.inner_shape_color = inner_shape_color
        self.shape_size = shape_size
        self.shape_type = shape_type

    def add_fill_layer(self, fill_layer):
        self.fill_layers.append(fill_layer)

    def __str__(self):
        return str(self.fill_layers[0][0])


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

    def to_image(self, grid):
        height, width = grid.shape
        out_img = np.zeros((height, width, 3), np.uint8)
        for row in self.grid:
            for tile in row:
                # If shape type == inner fill
                for layer_idx, fill_layer in enumerate(tile.fill_layers):
                    if layer_idx >= len(tile.fill_layers) - tile.shape_size:
                        for pixel_row, pixel_col in fill_layer:
                            out_img[pixel_row][pixel_col] = tile.inner_shape_color
                    else:
                        for pixel_row, pixel_col in fill_layer:
                            out_img[pixel_row][pixel_col] = tile.background_color
        # Remove # borders
        out_img = out_img[1:-1, 1:-1]
        return out_img

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
