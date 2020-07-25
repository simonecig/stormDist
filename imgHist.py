import numpy as np
import cv2

img = cv2.imread('noflash1.jpg', 0)
cv2.imshow('image', img)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
