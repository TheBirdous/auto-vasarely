import parser, recognition
from states import State
import cv2


def resize_test1():
    img = cv2.imread("../resources/hexagons.png", cv2.IMREAD_GRAYSCALE)
    img = parser._resize_img_(img, cv2.INTER_LINEAR)
    ret, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

    cv2.imwrite("../resources/resize_test1.out.png", img)


def resize_test2():
    img = cv2.imread("../resources/test_rand_fill2.out.png")
    height, width, rgb = img.shape
    img = cv2.resize(img, (int(width*4), int(height*4)), interpolation=cv2.INTER_NEAREST)

    cv2.imwrite("../resources/resize_test2.out.png", img)


if __name__ == "__main__":
    resize_test1()
    resize_test2()
