import parser
import recognition


def test_tile_recog1():
    grid = parser.img_to_grid("../../resources/test_new_begin.png")

    tile_grid = recognition.recognize_tiles(grid, [3])

    print(tile_grid)


def test_tile_recog2():
    grid = parser.img_to_grid("../../resources/test_grid.png")

    tile_grid = recognition.recognize_tiles(grid, [8])

    print(tile_grid)


def test_tile_recog3():
    grid = parser.img_to_grid("../../resources/triangles_and_squares.png")

    tile_grid = recognition.recognize_tiles(grid, [14, 28])

    print(tile_grid)


def test_tile_recog4():
    grid = parser.img_to_grid("../resources/hexagons.png")

    tile_grid = recognition.recognize_tiles(grid, [17])

    print(tile_grid)


if __name__ == '__main__':
    # test_tile_recog1()
    # test_tile_recog2()
    #test_tile_recog3()
    test_tile_recog4()