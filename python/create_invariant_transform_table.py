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


def write_lut(alpha, output_file):
    color_range = list(range(256))

    with open(output_file, 'w') as f:
        f.write('static const uint8_t ycbcr2ii[256][256][256] = {\n')
        for i, y in enumerate(color_range):
            f.write('\t{\n')
            print('Loop: Current Y - {}'.format(y))
            for j, cb in enumerate(color_range):
                f.write('\t\t{ ')
                for k, cr in enumerate(color_range):
                    r, g, b = ycbcr2rgb(y, cb, cr)
                    if r < 0 or g < 0 or b < 0:
                        f.write('0')
                    else:
                        f.write(str(rgb2ii(alpha, r, g, b)))
                    if k < len(color_range) - 1:
                        f.write(', ')

                if j < len(color_range) - 1:
                    f.write('},\n')
                else:
                    f.write('}\n')

            if i < len(color_range) - 1:
                f.write('\t},\n')
            else:
                f.write('\t}\n')
        f.write('};\n')


def main():
    alpha = 0.333
    out_file = 'LUT.hpp'
    write_lut(alpha, out_file)

if __name__ == '__main__':
    main()
