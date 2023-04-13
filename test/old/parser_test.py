import parser
import cv2


grid = parser.img_to_grid("../../resources/test_grid.png")
print(grid)
# grid = cv2.resize(grid, (960, 540))
# cv2.imshow('Binary Threshold Image', grid)
# cv2.waitKey()