"""
Contains the alphabet used by recognition.

Author: Marek Dohnal

Date: 17/03/2023

"""

from enum import Enum


class Alphabet(Enum):
    """
    The set of elements in the input grid. The values represent
    grayscale colors for easy debugging.
    """
    IMG_BORDER = 200    # - # symbol
    TILE_BORDER = 0     # - B symbol
    FILL = 150          # - F symbol
    FILL_BEGIN = 100    # - F_B symbol
    EMPTY = 255         # - E symbol
