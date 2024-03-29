import parser
import recognition
import cv2
import palette
import shapes
import videoenc


def test_video1():
    print("Parsing image...", end='\r')
    grid = parser.img_to_grid("../../resources/test_new_begin.png")
    print("Recognizing grid...", end='\r')

    tile_grid = recognition.recognize_tiles(grid, [17])
    print("Extracting colors...", end='\r')
    bg_colors = palette.img_to_palette("../../resources/colors/MAJUS.jpg")
    shape_colors = palette.img_to_palette("../../resources/colors/MAJUS.jpg")
    shape_list = [shapes.Shapes.SQUARE, shapes.Shapes.SQUARE_45DEG, shapes.Shapes.TRIANGLE_UP, shapes.Shapes.TRIANGLE_DOWN]
    print("Initializing tile grid...", end='\r')
    tile_grid.init_tile_attributes(bg_colors, shape_colors, shape_list)
    shapes.init_shape_fill_templates(tile_grid)
    print(tile_grid)
    imgs = []
    print("Converting to images...", end='\r')
    for i in range(0, 5):
        out_img = tile_grid.to_image(grid)
        imgs.append(out_img)
        cv2.imwrite(f"../resources/videotest1/frame{i}.out.png", out_img)
        print(f"Applying transformation {i}...", end='\r')
        tile_grid.apply_transformation_step("U", "UL", "L", True)
    print("Encoding video...", end='\r')
    videoenc.imgs_to_video("../../resources/videotest1.avi", imgs, 100)


def test_video2():
    print("Parsing image...")
    grid, shape = parser.img_to_grid("../resources/hexagons.png")
    print("Recognizing grid...")

    tile_grid = recognition.recognize_tiles(grid, [17])
    print("Extracting colors...")
    bg_colors = palette.img_to_palette("../../resources/colors/MAJUS.jpg")
    shape_colors = palette.img_to_palette("../../resources/colors/MAJUS.jpg")
    shape_list = [shapes.Shapes.SQUARE, shapes.Shapes.SQUARE_45DEG, shapes.Shapes.TRIANGLE_UP, shapes.Shapes.TRIANGLE_DOWN]
    print("Initializing tile grid...")
    tile_grid.init_tile_attributes(bg_colors, shape_colors, shape_list)
    shapes.init_shape_fill_templates(tile_grid)
    print(tile_grid)
    imgs = []
    print("Converting to images...")
    for i in range(0, 1):
        out_img = tile_grid.to_image(grid, (145, 163, 176))
        imgs.append(out_img)
        cv2.imwrite(f"../resources/videotest2/frame{i}.out.png", out_img)
        print(f"Applying transformation {i}...", end='\r')
        tile_grid.apply_transformation_step("U", "UL", "L", True)
        imgs.append(out_img)
    print("Encoding video...")
    videoenc.imgs_to_video("../resources/videotest2.avi", imgs, 1.5)


if __name__ == '__main__':
    test_video2()
