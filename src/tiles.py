import numpy as np
from shapes import Shape, Shapes


class Tile:
    def __init__(self, fill_layers=None,
                 color=(255, 0, 0),
                 shape=Shape()):
        if fill_layers is None:
            fill_layers = []
        self.fill_layers = fill_layers
        self.color = color
        self.shape = shape

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
                    tile.shape.draw(grid,
                                    out_img,
                                    tile.fill_layers[-1][-1],
                                    (tile_min_row, tile_min_col),
                                    (tile_max_row, tile_max_col))
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
