"""
Main module, entry point of the application.

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
from alphabet import Alphabet

directions = ["U", "D", "L", "R", "UL", "UR", "DL", "DR", "N"]

arg_parser = argparse.ArgumentParser(prog='auto-vasarely',
                                     description='Fills and trasforms an input grid, which is specified by its path.')

arg_parser.add_argument('grid_path',
                        type=str,
                        help='Path to the input grid represented by an image (.jpg or .png recommended)')

arg_parser.add_argument('row_sequence',
                        type=str,
                        help='Describes the pattern created by changing number of tiles on rows of the input grid. '
                             'Row lengths are separated by a "-" (hyphen) character in the row_sequence argument, '
                             'pattern of lengths a, b, c would be written as a-b-c '
                             'Example: '
                             'a grid with 7 tiles on a row would have 7 as a sequence, '
                             'whereas a grid with a pattern of 5 tiles per row followed by '
                             '2 tiles would be represented '
                             'by a sequence 5-2')

arg_parser.add_argument('background_colors_path',
                        type=str,
                        help='Path to an image containing colors to be extracted into a palette. '
                             'If the optional argument '
                             'shape_colors_path is not specified, the colors from this argument are used for both '
                             'background and shapes.')

arg_parser.add_argument('output_path',
                        type=str,
                        help='Path represents a folder into which the output is saved. ')

arg_parser.add_argument('-b', '--border_color_path',
                        type=str,
                        help='Optional PATH to an image containing a color which will be applied to tile borders. '
                             'Color with the highest occurence is used. '
                             'Borders are removed if this argument is not used.')

arg_parser.add_argument('-c', '--shape_colors_path',
                        type=str,
                        help='Optional argument containing a PATH to an image which is '
                             'extracted into a palette used for shapes')

arg_parser.add_argument('-s', '--shapes',
                        type=str,
                        help='Describes the inner shapes of tiles to be drawn to the output image. '
                             'SHAPES are specified as a sequence containing one of the following letters '
                             'in any order: RUDS. The letters choose the following shapes: '
                             'U - Triangle rotated up, '
                             'D - Triangle rotated down, '
                             'S - Square, '
                             'R - Square rotated 45 degrees. '
                             'If empty, the chosen shape is CONTOUR.')

arg_parser.add_argument('-n', '--number_of_transformations',
                        type=int,
                        help='Optional argument specifying the '
                             'NUMBER_OF_TRANSFORMATIONS to be applied to the tile grid. If no value is passed, '
                             'transformations are carried out until tiles are sorted. '
                             'A value 0 should be passed for no transformations to occur.')

arg_parser.add_argument('-st', '--sort_types',
                        action='store_true',
                        help='Optional argument specifying whether shapes are sorted according to their types.'
                             'If set, the sorting pattern applied is: triangles pointed up: UP, triangles pointed'
                             'down: DOWN, squares: LEFT, rotated squares: RIGHT')

arg_parser.add_argument('-ss', '--smaller_shape_dir',
                        type=str,
                        default="U",
                        choices=directions,
                        help='Optional argument specifying the '
                             'DIRECTION smaller shapes move up in when transformations are executed. '
                             'Default value is U. Movement can be turned off by passing N as an argument.')

arg_parser.add_argument('-lb', '--lighter_background_dir',
                        type=str,
                        default="U",
                        choices=directions,
                        help='Optional argument specifying the '
                             'DIRECTION in which lighter background move up when transformations are executed. '
                             'Default value is UL. Movement can be turned off by passing N as an argument.')

arg_parser.add_argument('-ls', '--lighter_shape_dir',
                        type=str,
                        default="U",
                        choices=directions,
                        help='Optional argument specifying the '
                             'DIRECTION in which lighter shapes move up when transformations are executed. '
                             'Default value is DR. Movement can be turned off by passing N as an argument.')

arg_parser.add_argument('-o', '--output_scale',
                        type=float,
                        default=1,
                        help='Optional argument which changes the scale relative to an output image. Default is 1 '
                             'values > 1 enlarge the resolution, smaller values shrink it. '
                             'Argument must be in the interval (0, 100]')

arg_parser.add_argument('-t', '--threshold',
                        type=int,
                        default=150,
                        help='Optional argument specifying the threshold used when converting the input grid from '
                             'a colored image into an image containing only black and white. Values should be in '
                             'the following interval: [0, 255]')

arg_parser.add_argument('-f', '--framerate',
                        type=int,
                        default=1,
                        help='Number of frames per second of the output video. Values should be in the following '
                             'interval: [0, 60]')

arg_parser.add_argument('-jt', '--jump_transformations',
                        action='store_true',
                        help='If this flag is set, only the first and last state are returned on output. States in '
                             'between are not saved as frames.')

args = arg_parser.parse_args()

# Argument check

err_found = False
if not os.path.exists(args.grid_path):
    print(f"ERROR: Invalid grid_path, please specify a correct path for the input grid.")
    err_found = True

if not os.path.exists(args.background_colors_path):
    print(f"ERROR: Invalid background_colors_path, please specify a correct path for the image containing "
          f"background colors.")
    err_found = True

if args.border_color_path is not None:
    if not os.path.exists(args.border_color_path):
        print(f"ERROR: Invalid PATH in --border_colors_path (-b), please specify a correct path for the image "
              f"containing border colors.")
        err_found = True

if args.shape_colors_path is not None:
    if not os.path.exists(args.shape_colors_path):
        print(f"ERROR: Invalid PATH in --shape_colors_path (-c), please specify a correct path for the image "
              f"containing shape colors.")
        err_found = True

try:
    int_seq_list = [int(c) for c in args.row_sequence.split("-")]
    for num in int_seq_list:
        if num <= 0:
            print(f"ERROR: The row_sequence argument can only contain numbers larger than 0. "
                  f"Please enter a correct sequence or use the -h flag to see correct usage.")
            err_found = True
            break
except ValueError:
    print(f"ERROR: The row_sequence argument can only contain digits larger than 0. "
          f"Please enter a correct sequence or use the -h flag to see correct usage.")
    err_found = True

if args.shapes is None:
    shape_list = [shapes.Shapes.CONTOUR]
else:
    shape_dict = {
        'U': shapes.Shapes.TRIANGLE_UP,
        'D': shapes.Shapes.TRIANGLE_DOWN,
        'S': shapes.Shapes.SQUARE,
        'R': shapes.Shapes.SQUARE_45DEG
    }
    try:
        args.shapes = args.shapes.upper()
        shape_list = [shape_dict[c] for c in list(args.shapes)]
    except KeyError:
        print(f"ERROR: The optional argument --shapes (-s) can only contain characters "
              f"R, U, D, S.")
        err_found = True

if not (0 < args.output_scale <= 100):
    print(f"ERROR: The optional argument --output_scale (-o) has an incorrect value of {args.output_scale}. "
          f"Argument must be in the interval (0, 100].")
    err_found = True

if not (0 <= args.threshold <= 255):
    print(f"ERROR: The optional argument --threshold (-t) has an incorrect value of {args.threshold}. "
          f"Argument must be in the interval [0, 255].")
    err_found = True

if not (1 <= args.framerate <= 60):
    print(f"ERROR: The optional argument --framerate (-f) has an incorrect value of {args.framerate}. "
          f"Argument must be in the interval [1, 60].")
    err_found = True

if err_found:
    quit()

# Create output directory if it doesn't exist
if not os.path.exists(args.output_path):
    os.makedirs(args.output_path)

# Create directory holding the output frames if it doesn't exist
frames_path = os.path.join(args.output_path, "frames")
if not os.path.exists(frames_path):
    os.makedirs(frames_path)

# print(args)
# print(os.path.join(args.output_path, "video.mp4"))

# Execution of the main body
print("Parsing image...")
grid, (orig_height, orig_width) = parser.img_to_grid(args.grid_path, threshold=args.threshold)

print("Recognizing grid...")
tile_grid = recognition.recognize_tiles(grid, int_seq_list)

if tile_grid is None:
    grid_path = os.path.join(args.output_path, f"unrecognized_grid.png")
    cv2.imwrite(grid_path, grid)
    print(f"ERROR: The input grid could not be recognized. Try changing the threshold value using the "
          f"-t argument. Halted recognition was saved into the following path: ")
    print(grid_path)
    quit()

for row in grid:
    for pixel in row:
        if pixel == Alphabet.FILL_BEGIN.value:
            pixel = Alphabet.FILL.value

print("Extracting colors...")
bg_colors = palette.img_to_palette(args.background_colors_path)

if args.shape_colors_path is None:
    shape_colors = bg_colors
else:
    shape_colors = palette.img_to_palette(args.shape_colors_path)

if args.border_color_path is not None:
    border_color = palette.img_to_palette(args.border_color_path)[0][0]
else:
    border_color = None

print("Initializing tile grid...")
tile_grid.init_tile_attributes(bg_colors, shape_colors, shape_list)
shapes.init_shape_fill_templates(tile_grid)

# print(tile_grid)
imgs = []
print("Converting to frames...")
# First image
out_img = tile_grid.to_image(grid, border_color)
imgs.append(out_img)

# Transformations

trans_cnt = 1

if args.number_of_transformations is None or args.number_of_transformations > 0:
    while True:
        if args.number_of_transformations is not None:
            print(f"Applying transformation {trans_cnt} of total {args.number_of_transformations}...", end='\r')
        else:
            print(f"Applying transformation {trans_cnt}. Transformations are applied until the grid is sorted...", end='\r')
        swapped = tile_grid.apply_transformation_step(args.smaller_shape_dir,
                                                      args.lighter_background_dir,
                                                      args.lighter_shape_dir,
                                                      args.sort_types)
        if trans_cnt == args.number_of_transformations or not args.jump_transformations or not swapped:
            out_img = tile_grid.to_image(grid, border_color)
            imgs.append(out_img)
        if not swapped and args.number_of_transformations is None:
            break
        if args.number_of_transformations == trans_cnt:
            break
        trans_cnt += 1

print()
print("Encoding video...")
video_path = os.path.join(args.output_path, "video.mp4")
videoenc.imgs_to_video(video_path, frames_path, imgs, orig_height, orig_width,
                       args.output_scale, framerate=args.framerate)
print()
print(f"Video was saved into the following file:")
print(os.path.abspath(video_path))
print(f"Frames were saved into the following folder:")
print(os.path.abspath(frames_path))
print()
