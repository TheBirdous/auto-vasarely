import cv2
import numpy as np
from alphabet import Alphabet


MAX_SIZE = 1000


def img_to_grid(img_path: str):
    """ Returns a numpy array of numbers representing a padded grid ready for recognition
        from an input image.
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = _resize_img_(img)
    ret, bw_img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    grid = np.pad(array=bw_img, mode='constant', constant_values=Alphabet.IMG_BORDER.value, pad_width=((1, 1), (1, 1)))
    return grid


def _resize_img_(img):
    width, height = img.shape
    if max(width, height) > MAX_SIZE:
        if height >= width:
            divisor = height / MAX_SIZE
            height = MAX_SIZE
            width = int(width / divisor)
        else:
            divisor = width / MAX_SIZE
            width = MAX_SIZE
            height = int(height / divisor)

        img = cv2.resize(img, (width, height))

    return img
