"""
auto_vasarely: report_test.py TEST module, used to create outputs for the testing chapter of the bachelor thesis.
Author: Marek Dohnal
Date: 13/04/2023
"""

import os


# Call using .\test\report_test.py


def cubes():
    print("Executing cubes: ")
    os.system("py src/auto_vasarely.py "
              "./test_report/cubes/cubes.jpg "
              "8-14 "
              "./test_report/cubes/malevich.jpg "
              "./test_report/cubes "
              "-o 1 "
              "-t 200 "
              "-ss L "
              "-lb U "
              "-ls D "
              )


def hexagons():
    print("Executing hexagons: ")
    os.system("py src/auto_vasarely.py "
              "./test_report/hexagons/hexagons.png "
              "17 "
              "./test_report/hexagons/tahiti.jpg "
              "./test_report/hexagons "
              "-s RUDS "
              "-st "
              "-ss DR "
              "-lb UL "
              "-ls U "
              "-o 1 "
              "-t 200 "
              )


def square_tiles():
    print("Executing square tiles: ")
    os.system("py src/auto_vasarely.py "
              "./test_report/square_tiles/square_tiles.jpg "
              "8-14 "
              "./test_report/square_tiles/yellow_painting.jpg "
              "./test_report/square_tiles "
              "-n 0 "
              "-o 1 "
              "-t 200")


def tilted_squares():
    print("Executing tilted squares: ")
    os.system("py src/auto_vasarely.py "
              "./test_report/tilted/tilted.jpg "
              "11 "
              "./test_report/tilted/cosca2.jpg "
              "-b ./test_report/tilted/cosca2-border.jpg "
              "./test_report/tilted "
              "-s SR "
              "-st "
              "-lb L "
              "-ls R "
              "-o 1 "
              "-t 200 "
              )


def triangles():
    print("Executing triangles: ")
    os.system("py src/auto_vasarely.py "
              "./test_report/triangles/triangles.jpg "
              "28 "
              "./test_report/triangles/MAJUS.jpg "
              "./test_report/triangles "
              "-o 1 "
              "-ss L "
              "-lb U "
              "-ls D "
              "-t 180")


def triangles_low_thresh():
    print("Executing triangles with low threshold: ")
    os.system("py src/auto_vasarely.py "
              "./test_report/triangles-low-thresh/triangles.jpg "
              "28 "
              "./test_report/triangles-low-thresh/MAJUS.jpg "
              "./test_report/triangles-low-thresh "
              "-o 1 "
              "-ss L "
              "-lb U "
              "-ls D "
              "-t 120")


if __name__ == "__main__":
    cubes()
    hexagons()
    square_tiles()
    tilted_squares()
    triangles()
    triangles_low_thresh()
