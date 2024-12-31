"""
Subset a tif.

python subset_tif.py \
    -i "data/n37_w123_1arc_v3.tif" \
    -o "data/n37_w123_subset.tif" \
    -b 1900 900 400 400

Note that the bounds (`-b`) are
- start point in x,
- start point in y,
- number of x point,
- and number of y points
uing the default settings in `view_tif.py`.
"""

import argparse

import rasterio
from rasterio.windows import Window

parser = argparse.ArgumentParser(
                    prog='subset_tif',
                    description='Create a subset of a SRTM tif')


# parser.add_argument('filename')           # positional argument
parser.add_argument('-i', '--input')      # option that takes a value
parser.add_argument('-o', '--output')      # option that takes a value
parser.add_argument('-b', '--bounds', nargs="+", type=int)
# parser.add_argument('-v', '--verbose',
#                     action='store_true')  # on/off flag

if __name__ == "__main__":

    args = parser.parse_args()

    window = Window(args.bounds[0],
                    args.bounds[1],
                    args.bounds[2],
                    args.bounds[3])

    with rasterio.open(args.input) as src:

        kwargs = src.meta.copy()
        kwargs.update({
            'height': window.height,
            'width': window.width,
            'transform': rasterio.windows.transform(window, src.transform)})

        with rasterio.open(args.output, 'w', **kwargs) as dst:
            dst.write(src.read(window=window))
