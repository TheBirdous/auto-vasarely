"""
auto_vasarely: auto_vasarely.py MAIN module
Author: Marek Dohnal
Date: 17/03/2023
"""
import argparse
import parser
import recognition
import tiles
import palette
import videoenc
import shapes
import cv2
import os

arg_parser = argparse.ArgumentParser(prog='auto-vasarely',
                                     description='Fills and trasforms an input grid, which is specified by its path.')

arg_parser.add_argument('grid_path',
                        type=str,
                        help='Path to the input grid represented by an image (.jpg or .png recommended)')

arg_parser.add_argument('row_sequence',
                        type=str,
                        help='Describes the pattern created by changing number of tiles on rows of the input grid. '
                             'Row lengths are not separated, pattern of lengths a, b, c would be simply written as abc '
                             'Example: '
                             'a grid with 7 tiles on a row would have 7 for sequence, '
                             'whereas a grid with a pattern of 5 tiles per row followed by '
                             '2 tiles would be represented '
                             'by a sequence 52')

arg_parser.add_argument('background_colors_path',
                        type=str,
                        help='Path to an image containing colors to be extracted into a palette. '
                             'If the optional argument '
                             'shape_colors_path is not specified, the colors from this argument are used for both '
                             'background and shapes.')

arg_parser.add_argument('output_path',
                        type=str,
                        help='Folder into which the output is saved. ')

arg_parser.add_argument('-b', '--border_color_path',
                        type=str,
                        help='Optional path to an image containing a color which will be applied to tile borders. '
                             'Color with the highest occurence is used. '
                             'Borders are removed if this argument is not used.')

arg_parser.add_argument('-c', '--shape_colors_path',
                        type=str,
                        help='Optional argument containing a path to an image which is '
                             'extracted into a palette used for shapes')

arg_parser.add_argument('-s', '--shapes',
                        type=str,
                        help='Describes the inner shapes of tiles to be drawn to the output image. '
                             'Shapes are specified as a sequence containing one of the following letters '
                             'in any order: RUDS. The letters choose the following shapes: '
                             'U - Triangle rotated up, '
                             'D - Triangle rotated down, '
                             'S - Square, '
                             'R - Square rotated 45 degrees. '
                             'If empty, the chosen shape is CONTOUR.')

arg_parser.add_argument('-n', '--number_of_transformations',
                        type=int,
                        default=5,
                        help='Optional argument specifying the '
                             'number of transformations to be applied to the tile grid. Default value is 5.')

arg_parser.add_argument('-st', '--sort_types',
                        action='store_true',
                        help='Optional argument specifying the '
                             'number of transformations to be applied to the tile grid. Default value is 5.')

arg_parser.add_argument('-o', '--output_scale',
                        type=int,
                        default=1,
                        help='Optional argument which changes the scale relative to an output image. Default is 1 '
                             'values > 1 enlarge the resolution, smaller values shrink it.')


args = arg_parser.parse_args()

print("Parsing image...")
grid = parser.img_to_grid(args.grid_path)

print("Recognizing grid...")
int_seq_list = [int(c) for c in list(args.row_sequence)]
tile_grid = recognition.recognize_tiles(grid, int_seq_list)

print("Extracting colors...")
bg_colors = palette.img_to_palette(args.background_colors_path)

if args.shape_colors_path is None:
    shape_colors = bg_colors
else:
    shape_colors = palette.img_to_palette(args.shape_colors_path)

if args.shapes is None:
    shape_list = [shapes.Shapes.CONTOUR]
else:
    shape_dict = {
        'U': shapes.Shapes.TRIANGLE_UP,
        'D': shapes.Shapes.TRIANGLE_DOWN,
        'S': shapes.Shapes.SQUARE,
        'R': shapes.Shapes.SQUARE_45DEG
    }
    shape_list = [shape_dict[c] for c in list(args.shapes)]

print("Initializing tile grid...")
tile_grid.init_tile_attributes(bg_colors, shape_colors, shape_list)
shapes.init_shape_fill_templates(tile_grid)

print(tile_grid)
imgs = []
print("Converting to images...")
for i in range(0, args.number_of_transformations):
    out_img = tile_grid.to_image(grid, args.border_color_path)
    imgs.append(out_img)
    cv2.imwrite(os.path.join(args.output_path, f"frame_{i}.png"), out_img)
    print(f"Applying transformation {i}...", end='\r')
    tile_grid.apply_transformation_step("U", "UL", "L", True)
print("Encoding video...")
videoenc.imgs_to_video(os.path.join(args.output_path, "video.avi"), imgs, args.output_scale)
