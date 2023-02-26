class Tile:
    def __init__(self, fill_layers=None,
                 background_color=0,
                 inner_shape_color=120,
                 shape_size=0):
        if fill_layers is None:
            fill_layers = []
        self.fill_layers = fill_layers
        # TODO: Need to find out how to save color
        self.background_color = background_color
        self.inner_shape_color = inner_shape_color
        self.shape_size = shape_size

    def add_fill_layer(self, fill_layer):
        self.fill_layers.append(fill_layer)


class TileGrid:
    def __init__(self, grid=None):
        if grid is None:
            grid = []
        self.grid = grid
