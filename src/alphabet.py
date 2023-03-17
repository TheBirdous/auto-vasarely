"""
auto_vasarely: alphabet.py module
Author: Marek Dohnal
Date: 17/03/2023
"""
from enum import Enum


class Alphabet(Enum):
    """
    The set of elements in the input grid. The values represent
    grayscale colors for easy debugging.
    """
    IMG_BORDER = 200
    TILE_BORDER = 0
    FILL = 150
    FILL_BEGIN = 100
    SHAPE = 50
    EMPTY = 255
