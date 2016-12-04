from math import log
import numpy as np


def rgb2ii(alpha, r, g, b, print_output=False):
    if r <= 0 or g <= 0 or b <= 0:
        return 0
    else:
        r /= 255
        g /= 255
        b /= 255
        invariant = 0.5 + log(g) - alpha * log(b) - (1 - alpha) * log(r)

        # Clamp to [0, 1]
        if invariant < 0:
            invariant = 0
        if invariant > 1:
            invariant = 1

        if print_output:
            print('RGB: [{}, {}, {}] -> Invariant: [{}]'.format(r, g, b, invariant))

        return invariant * 255


def ycbcr2rgb(y, cb, cr, print_output=False):
    """ https://en.wikipedia.org/wiki/YCbCr """
    r = round(y + 1.402 * (cr - 128))
    g = round(y - 0.344136 * (cb - 128) - 0.714136 * (cr - 128))
    b = round(y + 1.772 * (cb - 128))
    if print_output:
        print('YCbCr: [{}, {}, {}] -> RGB: [{}, {}, {}]'.format(y, cb, cr, r, g, b))
    return r, g, b


def main():
    lookup_table = np.zeros((256, 256, 256))
    alpha = 0.333
    color_range = list(range(256))

    for y in color_range:
        print('Loop: Current Y - {}'.format(y))
        for cb in color_range:
            for cr in color_range:
                r, g, b = ycbcr2rgb(y, cb, cr)
                if r < 0 or g < 0 or b < 0:
                    continue
                else:
                    lookup_table[y][cb][cr] = rgb2ii(alpha, r, g, b)


if __name__ == '__main__':
    main()
