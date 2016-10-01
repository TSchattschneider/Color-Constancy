from __future__ import print_function
import numpy as np
import cv2


def rgb2ii(img):
    """Convert RGB image to illumination invariant image."""
    alpha = 0.333

    ii_image = (0.5 + np.log(img[:, :, 1]) -
                alpha * np.log(img[:, :, 2]) -
                (1 - alpha) * np.log(img[:, :, 0]))

    return ii_image


def convert_255_to_1(img):
    """Convert given image from 0..255 to ~0..1"""
    max_range = 1
    min_range = 0.01
    converted = img / float(255)
    converted *= (max_range - min_range)
    converted += min_range

    return converted


if __name__ == "__main__":

    source_img = cv2.imread("../images/leipzsch.png", cv2.CV_LOAD_IMAGE_UNCHANGED)

    transformed_img = convert_255_to_1(source_img)

    invariant_img = rgb2ii(transformed_img)
    invariant_img /= np.amax(invariant_img)

    cv2.imshow("RGB Image", source_img)
    cv2.waitKey()
    cv2.imshow("Illumination Invariant", invariant_img)
    cv2.waitKey()
