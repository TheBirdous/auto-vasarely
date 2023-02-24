import parser, recognition
from states import State
import cv2


def resize_test1():
    img = cv2.imread("../resources/test_grid.png", cv2.IMREAD_GRAYSCALE)
    img = parser._resize_img_(img)
    ret, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

    cv2.imwrite("../resources/resize_test1.out.png", img)


if __name__ == "__main__":
    resize_test1()
