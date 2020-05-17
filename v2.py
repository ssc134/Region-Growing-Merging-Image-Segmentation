'''
This script is for detection of light/bright objects in dark background.
It does not work as intended yet.

After running the script, double left click on any object you want to segment ans press 'esc'.
The double clicked pixel coordinates will be generated and it will start flood_fill algo using the pixel merging criteria
from the function mergeCriteriaMet().

Presently script works fine, except merging criteria needs to be improved.

The test image 'coins.jpg' is available in the project repo.
'''

import cv2
import numpy as np

mean, pixelCount, error = 0, 0, 50


def mergeCriteriaMet(img, px, py):
    global error
    if img[px, py] <= mean + error and img[px,py] >= mean-error:
        return True
    return False


def valid(img, seedX, seedY):
    if seedX < 0 or seedX >= img.shape[1] or seedY < 0 or seedY >= img.shape[0]:
        return False
    return True


def flood_fill(img, seedX, seedY):
    '''
    img = image.
    seedX, seedY = seed coordinates.
    mean = mean of the flood filled region. Initialised by value of pixel while calling this function.
    pixelCount = required for recalculating mean as region grows.
    '''

    global mean, pixelCount

    if not valid(img, seedX, seedY):
        return
    if img[seedY, seedX] == -1:
        return
    if not mergeCriteriaMet(img, seedX, seedY):
        return

    
    sum = mean*pixelCount
    pixelCount += 1
    mean = (sum+img[seedY, seedX])/pixelCount
    img[seedY, seedX] = -1
    print("mean: ", mean)
    print("-------pixelCount: ", pixelCount, "\n")

    flood_fill(img, seedX-1, seedY)
    flood_fill(img, seedX+1, seedY)
    flood_fill(img, seedX, seedY-1)
    flood_fill(img, seedX, seedY+1)
    return


ix, iy = -1, -1
# mouse callback function


def draw_circle(event, x, y, flags, param):
    global ix, iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        ix, iy = x, y


# Open an image and bind the function to the window
img1 = cv2.imread('coins.jpg', 0)
cv2.imshow("original image", img1)
cv2.setMouseCallback('original image', draw_circle)


#cv2.imshow('original image',img1)
k = cv2.waitKey(0) & 0xFF
if k == 27:
    print(ix, iy)
cv2.destroyAllWindows()


# main code


# counting white and grey pixels to be used for determining if a small portion of an image should be merged with current region or not.
threshold = 100
wpc, bpc = 0, 0  # whitePixelCount & blackPixelCount
for i in range(img1.shape[0]):
    for j in range(img1.shape[1]):
        if img1[i, j] >= threshold:
            bpc += 1
        else:
            wpc += 1


img2 = img1.copy()
mean = img2[ix, iy]
flood_fill(img2, ix, iy)

# replace values '-1' in img2 with zero.
for i in range(img2.shape[0]):
    for j in range(img2.shape[1]):
        if img2[i, j] == -1:
            img2[i, j] = 0

cv2.imshow("segmented image", img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
