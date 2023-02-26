import parser, recognition
from states import State
import cv2


def test_begin_0():
    grid = parser.img_to_grid("../resources/test_new_begin.png")
    state, row, col = recognition._find_new_beginning_(grid, 0, 0)

    assert state == State.Sa
    assert row == 1
    assert col == 1


def test_begin_1():
    grid = parser.img_to_grid("../resources/test_new_begin_1.png")
    state, row, col = recognition._find_new_beginning_(grid, 0, 0)

    assert state == State.Sa
    assert row == 7
    assert col == 22


def test_begin_2():
    grid = parser.img_to_grid("../resources/test_new_begin_2.png")
    state, row, col = recognition._find_new_beginning_(grid, 0, 0)

    assert state == State.Sr


def test_fill_1():
    grid = parser.img_to_grid("../resources/fill_test1.png")
    # Ensure F_B
    grid[1][1] = 100
    fill_buffer = []
    state, row, col, fill_buffer = recognition._fill_down_(grid, 1, 1, fill_buffer)
    grid = recognition._apply_buffer_(grid, fill_buffer)

    cv2.imwrite("../resources/fill_test1.out.png", grid)


def test_fill_2():
    grid = parser.img_to_grid("../resources/fill_test2.png")
    # Ensure F_B
    grid[1][1] = 100
    fill_buffer = []
    state, row, col, fill_buffer = recognition._fill_down_(grid, 1, 1, fill_buffer)
    grid = recognition._apply_buffer_(grid, fill_buffer)

    cv2.imwrite("../resources/fill_test2.out.png", grid)


def test_fill_3():
    grid = parser.img_to_grid("../resources/fill_test3.png")
    # Ensure F_B
    grid[1][1] = 100
    fill_buffer = []
    state, row, col, fill_buffer = recognition._fill_down_(grid, 1, 1, fill_buffer)
    grid = recognition._apply_buffer_(grid, fill_buffer)

    cv2.imwrite("../resources/fill_test3.out.png", grid)


def test_fill_up_1():
    grid = parser.img_to_grid("../resources/fill_test_up1.png")
    # Ensure F_B
    grid[2][6] = 100
    fill_buffer = []
    state, row, col, fill_buffer = recognition._fill_up_(grid, 23, 10, fill_buffer)
    grid = recognition._apply_buffer_(grid, fill_buffer)

    cv2.imwrite("../resources/fill_test_up1.out.png", grid)


def test_fill_up_2():
    grid = parser.img_to_grid("../resources/fill_test_up2.png")
    # Ensure F_B
    grid[2][6] = 100
    fill_buffer = []
    state, row, col, fill_buffer = recognition._fill_up_(grid, 23, 10, fill_buffer)
    grid = recognition._apply_buffer_(grid, fill_buffer)

    cv2.imwrite("../resources/fill_test_up2.out.png", grid)


def test_new_fill_begin_1():
    grid = cv2.imread("../resources/test_new_fill_begin1.png", cv2.IMREAD_GRAYSCALE)

    state, row, col = recognition._find_new_fill_beginning_(grid, 2, 6)

    assert state == State.Na
    assert row == 3
    assert col == 7

    cv2.imwrite("../resources/test_new_fill_begin1.out.png", grid)


def test_new_fill_begin_2():
    grid = cv2.imread("../resources/test_new_fill_begin2.png", cv2.IMREAD_GRAYSCALE)

    state, row, col = recognition._find_new_fill_beginning_(grid, 11, 9)

    assert state == State.Na
    assert row == 12
    assert col == 9

    cv2.imwrite("../resources/test_new_fill_begin2.out.png", grid)


def test_new_fill_begin_3():
    grid = cv2.imread("../resources/test_new_fill_begin3.png", cv2.IMREAD_GRAYSCALE)

    state, row, col = recognition._find_new_fill_beginning_(grid, 11, 9)

    assert state == State.Nr
    assert row == 23
    assert col == 10

    cv2.imwrite("../resources/test_new_fill_begin3.out.png", grid)


def test_whole_fill1():
    grid = parser.img_to_grid("../resources/fill_test1.png")

    # Ensure F_B
    grid[1][1] = 100

    grid = recognition._fill_tile_(grid, 1, 1)

    cv2.imwrite("../resources/test_whole_fill1.out.png", grid)


def test_whole_fill2():
    grid = parser.img_to_grid("../resources/fill_test3.png")

    # Ensure F_B
    grid[1][1] = 100

    grid = recognition._fill_tile_(grid, 1, 1)

    cv2.imwrite("../resources/test_whole_fill2.out.png", grid)


def test_whole_fill3():
    grid = parser.img_to_grid("../resources/fill_test_up2.png")

    # Ensure F_B
    grid[2][6] = 100

    grid = recognition._fill_tile_(grid, 2, 6)

    cv2.imwrite("../resources/test_whole_fill3.out.png", grid)


def test_whole_fill4():
    grid = parser.img_to_grid("../resources/fill_test_up1.png")

    # Ensure F_B
    grid[2][6] = 100

    grid = recognition._fill_tile_(grid, 2, 6)

    cv2.imwrite("../resources/test_whole_fill4.out.png", grid)


def test_tile_recog1():
    grid = parser.img_to_grid("../resources/test_new_begin.png")

    grid = recognition.recognize_tiles(grid)

    cv2.imwrite("../resources/test_tile_recog1.out.png", grid)


def test_tile_recog2():
    grid = parser.img_to_grid("../resources/test_grid.png")

    grid = recognition.recognize_tiles(grid)

    cv2.imwrite("../resources/test_tile_recog2.out.png", grid)


def test_triangles():
    grid = parser.img_to_grid("../resources/triangles.jpg", threshold=170)

    grid = recognition.recognize_tiles(grid)

    cv2.imwrite("../resources/triangles.out.jpg", grid)


def test_hexagons():
    grid = parser.img_to_grid("../resources/hexagons.png")

    grid = recognition.recognize_tiles(grid)

    cv2.imwrite("../resources/hexagons.out.png", grid)


def test_triangles_and_squares():
    grid = parser.img_to_grid("../resources/triangles_and_squares.png")

    grid = recognition.recognize_tiles(grid)

    cv2.imwrite("../resources/triangles_and_squares.out.png", grid)


if __name__ == "__main__":
    test_begin_0()
    test_begin_1()
    test_begin_2()

    # Fill down
    test_fill_1()
    test_fill_2()
    test_fill_3()

    # Fill up
    test_fill_up_1()
    test_fill_up_2()

    # New fill begin
    test_new_fill_begin_1()
    test_new_fill_begin_2()
    test_new_fill_begin_3()

    # Whole fill test
    test_whole_fill1()
    test_whole_fill2()
    test_whole_fill3()
    test_whole_fill4()

    # Tile recognition test
    # test_tile_recog1()
    # test_tile_recog2()
    # test_triangles()
    # test_hexagons()
    test_triangles_and_squares()
    print("Tests passed.")

