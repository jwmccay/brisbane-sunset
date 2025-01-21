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


def reproject_tif():

    parser = argparse.ArgumentParser(
                        prog='subset_tif',
                        description='Reproject an SRTM tif')

    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-e', '--epsg', type=int)

    args = parser.parse_args()

    dst_crs = rasterio.CRS.from_epsg(args.epsg)

    with rasterio.open(args.input) as src:
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

        with rasterio.open(args.output, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.cubic_spline)
