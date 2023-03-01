import parser
import recognition
import cv2


def test_fill1():
    grid = parser.img_to_grid("../resources/hexagons.png")

    tile_grid = recognition.recognize_tiles(grid, [17])
    out_img = tile_grid.to_image(grid)
    print(tile_grid)
    cv2.imwrite("../resources/test_out_fill1.out.png", out_img)


if __name__ == '__main__':
    test_fill1()
