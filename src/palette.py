"""
Contains functions, which extract colors from an image.

Author: Marek Dohnal

Date: 17/03/2023

"""

import extcolors


def img_to_palette(colored_img_path):
    """
    Extracts colors from an image.

    :param colored_img_path: path to an image, from which colors are extracted.

    :return: list of colors and their cummulative occurences
    """

    colors, pixel_count = extcolors.extract_from_path(colored_img_path, tolerance=4)
    colors_cummul = []
    prob_sum = 0
    for color, occurrence in colors:
        probability = occurrence/pixel_count
        prob_sum += probability
        colors_cummul.append((color, prob_sum))
    return colors_cummul

