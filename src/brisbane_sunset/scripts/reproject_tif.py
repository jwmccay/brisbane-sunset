"""
Reproject a tif.

python reproject_tif.py \
    -i data/n37_w123_subset.tif \
    -o data/n37_w123_subset_reproject.tif \
    -e 7131
"""

import argparse

import rasterio
from rasterio.warp import (calculate_default_transform,
                           reproject,
                           Resampling)


def parse_args():

    parser = argparse.ArgumentParser(
                        prog='subset_tif',
                        description='Reproject an SRTM tif')

    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-e', '--epsg', type=int)

    args = parser.parse_args()

    return args


def reproject_tif_main(epsg, input_raster, output_raster):

    dst_crs = rasterio.CRS.from_epsg(epsg)

    with rasterio.open(input_raster) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        # values_src = src.read()

        with rasterio.open(output_raster, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.cubic_spline)


def reproject_tif():
    args = parse_args()
    reproject_tif_main(args.epsg, args.input, args.output)
