import parser, recognition
from states import State
import cv2

def test_begin_0():
    grid = parser.img_to_grid("../resources/test_new_begin.png")
    state, row, col = recognition._find_new_beginning_(grid, 0, 0)

    assert state == State.Qa
    assert row == 1
    assert col == 1


def test_begin_1():
    grid = parser.img_to_grid("../resources/test_new_begin_1.png")
    state, row, col = recognition._find_new_beginning_(grid, 0, 0)

    assert state == State.Qa
    assert row == 7
    assert col == 22


def test_begin_2():
    grid = parser.img_to_grid("../resources/test_new_begin_2.png")
    state, row, col = recognition._find_new_beginning_(grid, 0, 0)

    assert state == State.Qr


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


if __name__ == "__main__":
    test_begin_0()
    test_begin_1()
    test_begin_2()

    test_fill_1()
    test_fill_2()
    test_fill_3()
    print("Tests passed.")

