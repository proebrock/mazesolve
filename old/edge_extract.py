from skimage import morphology
from skimage import img_as_ubyte
import cv2
import numpy as np

im = cv2.imread("vetica.png")
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im = cv2.threshold(im, 0, 255, cv2.THRESH_OTSU)[1]
im = morphology.skeletonize(im > 0)
cv_image = img_as_ubyte(im)

#kernel = np.array([[-1, -1, -1], [ 2, 2, 2], [-1, -1, -1]]);
kernel = np.array([[-1, 2, -1], [ -1, 2, -1], [-1, 2, -1]]);
cv_image = cv2.filter2D(cv_image,-1,kernel)

cv2.imwrite("vetica_skel.png", cv_image)



