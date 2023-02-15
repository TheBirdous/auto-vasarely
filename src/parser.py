import cv2
import numpy as np
from alphabet import Alphabet


def img_to_grid(img_path: str):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    grid = np.pad(array=bw_img, mode='constant', constant_values=Alphabet.IMG_BORDER.value, pad_width=((1, 1), (1, 1)))
    return grid
