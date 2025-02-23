"""
Functions for handling terrain grids
"""

import numpy as np
from scipy.interpolate import (LinearNDInterpolator,
                               RegularGridInterpolator)
import rasterio
from pyproj import Transformer


class RasterData:

    def __init__(self, raster_fname):
        self.fname = raster_fname

        self._read()

    def _read(self):

        with rasterio.open(self.fname) as ds:

            # Store CRS to use for figuring out transforms with XY
            # interpolation
            self.crs: rasterio.crs.CRS = ds.crs

            values = ds.read()

            # assume one band
            self.values_grid = values[0, :, :]

            self.lons_grid, self.lats_grid = self._meshgrid_from_raster(
                ds.shape[0], ds.shape[1], ds.transform)

        self.points, self.point_values = self._points_from_meshgrid(
            self.lons_grid, self.lats_grid, self.values_grid)

    @staticmethod
    def _meshgrid_from_raster(height, width, transform):

        cols, rows = np.meshgrid(np.arange(width), np.arange(height))
        xs, ys = rasterio.transform.xy(transform, rows, cols)
        lons_grid = np.array(xs)
        lats_grid = np.array(ys)

        return lons_grid, lats_grid

    @staticmethod
    def _points_from_meshgrid(lons_grid, lats_grid, values):

        points = np.transpose(
            np.stack(
                (np.ravel(lons_grid), np.ravel(lats_grid))))

        point_values = np.ravel(values)

        return points, point_values


def setup_interpolator(rd: RasterData, interp_mode="RegularGrid"):

    if interp_mode == "LinearND":
        interp = LinearNDInterpolator(rd.points, rd.point_values)
    elif interp_mode == "RegularGrid":
        interp = RegularGridInterpolator(
            (rd.lons_grid[0, :], rd.lats_grid[:, 0]),
            np.transpose(rd.values_grid)
        )
    else:
        raise ValueError("Invalid interpolation type.")

    return interp


def setup_transformer(epsg_latlon: int, epsg_xy: int):

    src_crs = rasterio.CRS.from_epsg(epsg_latlon)
    dst_crs = rasterio.CRS.from_epsg(epsg_xy)

    transformer = Transformer.from_crs(
        src_crs.to_string(), dst_crs.to_string())

    return transformer
