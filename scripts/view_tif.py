"""
Read and plot a tif.
"""

import argparse

import numpy as np
from matplotlib import pyplot as plt

from dusk.grid import RasterData

parser = argparse.ArgumentParser(
                    prog='subset_tif',
                    description='Quickly plot an SRTM tif')


parser.add_argument('fname')
parser.add_argument('-o', '--output')
parser.add_argument('-a', '--axis_mode')
# shortcut to plot the latlon axis mode
parser.add_argument('-l', '--latlon', action='store_true')
parser.add_argument('-c', '--cmap', default='viridis')


if __name__ == "__main__":

    args = parser.parse_args()

    cmap = args.cmap

    rd = RasterData(args.fname)

    if (args.axis_mode == "latlon") or args.latlon:
        plt.pcolormesh(rd.lons_grid, rd.lats_grid,
                       rd.values_grid,
                       cmap=cmap)
    elif args.axis_mode == "flip":
        plt.pcolormesh(np.flipud(rd.values_grid),
                       cmap=cmap)
    elif args.axis_mode == "raw":
        plt.pcolormesh(rd.values_grid,
                       cmap=cmap)
    else:
        print("Unrecognized axis option, defaulting to raw.")
        plt.pcolormesh(rd.values_grid,
                       cmap=cmap)

    plt.colorbar()

    if args.output is not None:
        plt.savefig(args.output)
        plt.close()
    else:
        plt.show()
