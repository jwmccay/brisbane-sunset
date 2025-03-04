"""
Build a raster for testing 
"""


import numpy as np
import rasterio
from rasterio.transform import Affine

deg_lon = -122.0
deg_lat = 38.0
delta_lon = 1.0
delta_lat = 1.0
n_lat = 240
n_lon = 180

# Kinda works but x and y are flipped

x = np.linspace(deg_lat, deg_lat + delta_lat, n_lat)
y = np.linspace(deg_lon, deg_lon + delta_lon, n_lon)
X, Y = np.meshgrid(x, y)

# Build a Z grid on something that's the same size
x_temp = np.linspace(-4.0, 4.0, n_lat)
y_temp = np.linspace(-3.0, 3.0, n_lon)
X_temp, Y_temp = np.meshgrid(x_temp, y_temp)
Z1 = np.exp(-2 * np.log(2)
            * ((X_temp - 0.5) ** 2 + (Y_temp - 0.5) ** 2) / 1 ** 2)
Z2 = np.exp(-3 * np.log(2)
            * ((X_temp + 0.5) ** 2 + (Y_temp + 0.5) ** 2) / 2.5 ** 2)
Z = 10.0 * (Z2 - Z1)

res = (x[-1] - x[0]) / n_lat
transform = Affine.translation(
    x[0] - res / 2, y[0] - res / 2) * Affine.scale(res, res)

new_dataset = rasterio.open(
     './new.tif',
     'w',
     driver='GTiff',
     height=Z.shape[0],
     width=Z.shape[1],
     count=1,
     dtype=Z.dtype,
     crs='+proj=latlong',
     transform=transform,
 )

new_dataset.write(Z, 1)
new_dataset.close()
