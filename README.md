# auto-vasarely

Author: Marek Dohnal  
Date: 06/04/2023

Practical part of bachelor thesis at FIT BUT.

Fills and trasforms an input grid, which is specified by its path.
Creates a video, which contains transformations between states of the
filled input grid. The grid is filled with colors according to the chosen
color palette, and with inner shapes depending on the user's choice. 
Each state of the filled grid is saved into a separate folder.

## Repository Structure

- `doc/` contains documentation of the application.
- `excel/` contains presentation materials for Excel@FIT 2023
- `profiling/` contains statistical data regarding execution time of the application.
- `report/` contains source files, from which the thesis/report can be generated.
- `resources/` contains inputs and outputs from early testing.
- `src/` contains source files of the application.
- `test/` contains tests.
- `test_report/` contains tests, which showcase final outputs of the application.
- `LICENSE` is a file containing license info regarding the correct usage and
distribution of this application.
- `README.md` contains general information regarding this repository, and
a usage guide for the application.
- `xdohna48.pdf` contains the compiled thesis/report.

## Prerequisities

In this section are included required libraries, as well as a version of the 
Python interpreter necessary to run this software.

### Interpreter
- **[Python 3.10](https://www.python.org/downloads/release/python-310)**

### Libraries
- **[cv2](https://pypi.org/project/opencv-python/)**
- **[numpy](https://numpy.org/)**
- **[extcolors](https://pypi.org/project/extcolors/)**

## Documentation

Documentation of modules can be found in the `doc/` folder.

Built documentation can be accessed by opening the `index.html`
file contained in the following directory: `doc/_build/html`.

If one wishes to build
the documentation themselves, 
**[sphinx](https://www.sphinx-doc.org/en/master/index.html)**
must be installed first.

Then, in order to build an html version, enter the following command
within the `doc/` directory:

`make html`

## Example configurations

Examples of launch configurations can be found by consulting the file `report_test.py` contained 
in the `test` folder.

The script can also be launched to obtain example output by entering:

`py .\test\report_test.py`

## Usage
The following usage guide assumes the program is run from the src folder.  

`py auto-vasarely`  
`grid_path row_sequence background_colors_path output_path`  
`[-h]`   
`[-b BORDER_COLOR_PATH]`  
`[-c SHAPE_COLORS_PATH]`  
`[-s SHAPES]`  
`[-n NUMBER_OF_TRANSFORMATIONS]`   
`[-st]`   
`[-ss {U,D,L,R,UL,UR,DL,DR,N}]`   
`[-lb {U,D,L,R,UL,UR,DL,DR,N}]`  
`[-ls {U,D,L,R,UL,UR,DL,DR,N}]`  
`[-o OUTPUT_SCALE]`  
`[-t THRESHOLD]`   
`[-f FRAMERATE]`

## Positional arguments:
### Grid path             
Path to the input grid represented by an image (.jpg or .png recommended)
### Row sequence          
Describes the pattern created by changing number of tiles on rows of the input grid. Row lengths are separated by a "-" (hyphen) character in the row_sequence
argument, pattern of lengths a, b, c would be written as a-b-c Example: a grid with 7 tiles on a row would have 7 as a sequence, whereas a grid with a pattern
of 5 tiles per row followed by 2 tiles would be represented by a sequence 5-2
### Background colors path
Path to an image containing colors to be extracted into a palette. If the optional argument shape_colors_path is not specified, the colors from this argument
are used for both background and shapes. 
### Output path           
Path represents a folder into which the output is saved.

## Options

### Help

`-h, --help`       

Show this help message and exit

### Border color path

`-b PATH, --border_color_path PATH`

Optional PATH to an image containing a color which will be applied to tile borders. Color with the highest occurence is used. Borders are removed if this
argument is not used.

### Shape colors path

`-c PATH, --shape_colors_path PATH`

Optional argument containing a PATH to an image which is extracted into a palette used for shapes

### Shapes

`-s SHAPES, --shapes SHAPES`

Describes the inner shapes of tiles to be drawn to the output image. SHAPES are specified as a sequence containing one of the following letters in any order:
RUDS. The letters choose the following shapes: U - Triangle rotated up, D - Triangle rotated down, S - Square, R - Square rotated 45 degrees. If empty, the
chosen shape is CONTOUR.

### Number of transformations

`-n NUMBER_OF_TRANSFORMATIONS, --number_of_transformations NUMBER_OF_TRANSFORMATIONS`

Optional argument specifying the NUMBER_OF_TRANSFORMATIONS to be applied to the tile grid. If no value is passed, transformations are carried out until tiles are sorted. A value 0 should be passed for no transformations to occur.

### Sort shape types

`-st, --sort_types`

Optional argument specifying whether shapes are sorted according to their types.If set, the sorting pattern applied is: triangles pointed up: UP, triangles
pointeddown: DOWN, squares: LEFT, rotated squares: RIGHT

### Smaller shape direction

`-ss {U,D,L,R,UL,UR,DL,DR,N}, --smaller_shape_dir {U,D,L,R,UL,UR,DL,DR,N}`

Optional argument specifying the DIRECTION smaller shapes move up in when transformations are executed. Default value is U. Movement can be turned off by
passing N as an argument.

### Lighter background direction

`-lb {U,D,L,R,UL,UR,DL,DR,N}, --lighter_background_dir {U,D,L,R,UL,UR,DL,DR,N}`

Optional argument specifying the DIRECTION in which lighter background move up when transformations are executed. Default value is UL. Movement can be turned
off by passing N as an argument.

### Lighter shape direction

`-ls {U,D,L,R,UL,UR,DL,DR,N}, --lighter_shape_dir {U,D,L,R,UL,UR,DL,DR,N}`

Optional argument specifying the DIRECTION in which lighter shapes move up when transformations are executed. Default value is DR. Movement can be turned off
by passing N as an argument.

### Output scale

`-o OUTPUT_SCALE, --output_scale OUTPUT_SCALE`

Optional argument which changes the scale relative to an output image. Default is 1 values > 1 enlarge the resolution, smaller values shrink it. Argument must
be in the interval (0, 100]

### Threshold

`-t THRESHOLD, --threshold THRESHOLD`

Optional argument specifying the threshold used when converting the input grid from a colored image into an image containing only black and white. Values
should be in the following interval: [0, 255]

### Framerate

`-f FRAMERATE, --framerate FRAMERATE`

Number of frames per second of the output video. Values should be in the following interval: [0, 60]

### Jump over transformations

 `-jt, --jump_transformations` 

 If this flag is set, only the first and last state are returned on output. States in between are not saved as frames.
 