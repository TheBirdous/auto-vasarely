import parser
import recognition
import cv2
import palette
import shapes

def test_fill1():
    grid = parser.img_to_grid("../resources/hexagons.png")

    tile_grid = recognition.recognize_tiles(grid, [17])
    cv2.imwrite("../resources/test_out_fill1.grid.out.png", grid)

    out_img = tile_grid.to_image(grid)
    print(tile_grid)
    cv2.imwrite("../resources/test_out_fill1.out.png", out_img)


def test_fill2():
    grid = parser.img_to_grid("../resources/test_new_begin.png")

    tile_grid = recognition.recognize_tiles(grid, [3])
    out_img = tile_grid.to_image(grid)
    print(tile_grid)
    cv2.imwrite("../resources/test_out_fill2.out.png", out_img)


def test_rand_fill1():
    grid = parser.img_to_grid("../resources/test_new_begin.png")

    tile_grid = recognition.recognize_tiles(grid, [3])
    colors = palette.img_to_palette("../resources/colors/MAJUS.jpg")
    shape_list = [shapes.Shapes.TRIANGLE_UP, shapes.Shapes.TRIANGLE_DOWN, shapes.Shapes.SQUARE_45DEG, shapes.Shapes.SQUARE]
    tile_grid.init_tile_attributes(colors, shape_list)
    out_img = tile_grid.to_image(grid)
    print(tile_grid)
    cv2.imwrite("../resources/test_rand_fill1.out.png", out_img)


def test_rand_fill2():
    grid = parser.img_to_grid("../resources/hexagons.png")

    tile_grid = recognition.recognize_tiles(grid, [17])
    colors = palette.img_to_palette("../resources/colors/MAJUS.jpg")
    shape_list = [shapes.Shapes.TRIANGLE_UP, shapes.Shapes.TRIANGLE_DOWN, shapes.Shapes.SQUARE_45DEG,
                  shapes.Shapes.SQUARE]
    tile_grid.init_tile_attributes(colors, shape_list)
    out_img = tile_grid.to_image(grid)
    print(tile_grid)
    cv2.imwrite("../resources/test_rand_fill2.out.png", out_img)


def test_transform1():
    grid = parser.img_to_grid("../resources/test_new_begin.png")

    tile_grid = recognition.recognize_tiles(grid, [3])
    colors = palette.img_to_palette("../resources/colors/MAJUS.jpg")
    shape_list = [shapes.Shapes.TRIANGLE_UP, shapes.Shapes.TRIANGLE_DOWN, shapes.Shapes.SQUARE_45DEG, shapes.Shapes.SQUARE]
    tile_grid.init_tile_attributes(colors, shape_list)
    out_img = tile_grid.to_image(grid)
    print(tile_grid)
    cv2.imwrite("../resources/test_before_transform.out.png", out_img)
    tile_grid.apply_transformation_step("U", None, None)
    out_img = tile_grid.to_image(grid)
    cv2.imwrite("../resources/test_after_transform.out.png", out_img)


def test_transform2():
    print("Parsing image...")
    grid = parser.img_to_grid("../resources/hexagons.png")
    print("Recognizing grid...")

    tile_grid = recognition.recognize_tiles(grid, [17])
    print("Extracting colors...")
    colors = palette.img_to_palette("../resources/colors/MAJUS.jpg")
    shape_list = [shapes.Shapes.TRIANGLE_UP, shapes.Shapes.TRIANGLE_DOWN, shapes.Shapes.SQUARE_45DEG,
                  shapes.Shapes.SQUARE]
    print("Initializing tile grid...")
    tile_grid.init_tile_attributes(colors, shape_list)
    print("Converting to image...")
    out_img = tile_grid.to_image(grid)
    print(tile_grid)
    cv2.imwrite("../resources/test_before_transform2.out.png", out_img)
    print("Applying transformations...")
    for i in range(10):
        tile_grid.apply_transformation_step("U", None, None)
    print("Converting to image...")
    out_img = tile_grid.to_image(grid)
    cv2.imwrite("../resources/test_after_transform2.out.png", out_img)


if __name__ == '__main__':
    #test_fill1()
    #test_fill2()
    #test_rand_fill1()
    #test_rand_fill2()
    #test_transform1()
    test_transform2()
