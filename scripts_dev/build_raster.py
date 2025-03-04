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

x = np.linspace(-4.0, 4.0, 240)
y = np.linspace(-3.0, 3.0, 180)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-2 * np.log(2) * ((X - 0.5) ** 2 + (Y - 0.5) ** 2) / 1 ** 2)
Z2 = np.exp(-3 * np.log(2) * ((X + 0.5) ** 2 + (Y + 0.5) ** 2) / 2.5 ** 2)
Z = 10.0 * (Z2 - Z1)

res = (x[-1] - x[0]) / 240.0
transform = Affine.translation(x[0] - res / 2, y[0] - res / 2) * Affine.scale(res, res)
transform
Affine(0.033333333333333333, 0.0, -4.0166666666666666,
       0.0, 0.033333333333333333, -3.0166666666666666)

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
