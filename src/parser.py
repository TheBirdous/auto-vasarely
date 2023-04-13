"""
Contains functions, which parse an image into an input grid.

Author: Marek Dohnal

Date: 17/03/2023
"""

import cv2
import numpy as np
from alphabet import Alphabet


MAX_SIZE = 1500


def img_to_grid(img_path: str, threshold=170, interpolation=cv2.INTER_LINEAR):
    """ Returns a numpy array of numbers representing a padded grid ready for recognition
        from an input image.

        :param interpolation: interpolation to be used while resizing, default is cv2.INTER_LINEAR
        :param threshold: threshold to be used by the cv2.threshold() function
        :param img_path: path to an image containing a suitable grid

        :return: padded grid ready for recognition
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape
    img = _resize_img_(img, interpolation)
    ret, bw_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    grid = np.pad(array=bw_img, mode='constant', constant_values=Alphabet.IMG_BORDER.value, pad_width=((1, 1), (1, 1)))
    return grid, (height, width)


def _resize_img_(img, interpolation):
    """
    Resizes image if it's longest side is longer than 1000 pixels

    :param img: the image to be resized
    :param interpolation: interpolation to be used while resizing

    :return: resized image
    """
    height, width = img.shape
    if max(width, height) > MAX_SIZE:
        if height >= width:
            divisor = height / MAX_SIZE
            height = MAX_SIZE
            width = int(width / divisor)
        else:
            divisor = width / MAX_SIZE
            width = MAX_SIZE
            height = int(height / divisor)
        img = cv2.resize(img, (width, height), interpolation=interpolation)

    return img
