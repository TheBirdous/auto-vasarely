import parser
import recognition
import cv2


def test_tile_recog1():
    grid = parser.img_to_grid("../resources/test_new_begin.png")

    tile_grid = recognition.recognize_tiles(grid, [3])

    cv2.imwrite("../resources/tile_insert_test.out.png", grid)
    print(tile_grid)


def test_tile_recog2():
    grid = parser.img_to_grid("../resources/test_grid.png")

    tile_grid = recognition.recognize_tiles(grid, [8])

    cv2.imwrite("../resources/tile_insert_test2.out.png", grid)
    print(tile_grid)


def test_tile_recog3():
    grid = parser.img_to_grid("../resources/triangles_and_squares.png")

    tile_grid = recognition.recognize_tiles(grid, [14, 28])

    cv2.imwrite("../resources/test_tile_recog3.out.png", grid)
    print(tile_grid)


if __name__ == '__main__':
    # test_tile_recog1()
    # test_tile_recog2()
    test_tile_recog3()