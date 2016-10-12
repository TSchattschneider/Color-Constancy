from __future__ import print_function
import numpy as np
import cv2


def rgb2ii(img, alpha):
    """Convert RGB image to illumination invariant image."""
    ii_image = (0.5 + np.log(img[:, :, 1] / float(255)) -
                alpha * np.log(img[:, :, 2] / float(255)) -
                (1 - alpha) * np.log(img[:, :, 0] / float(255)))

    return ii_image

if __name__ == "__main__":

    source_img = cv2.imread("../images/leipzsch.png", cv2.CV_LOAD_IMAGE_UNCHANGED)

    a = 0.333 # Camera alpha
    invariant_img = rgb2ii(source_img, a)
    invariant_img /= np.amax(invariant_img)

    cv2.imshow("RGB Image", source_img)
    cv2.imshow("Illumination Invariant", invariant_img)
    cv2.waitKey()
