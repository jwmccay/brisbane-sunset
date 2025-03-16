"""
Run over a grid.
"""

import numpy as np

from brisbane_sunset.containers import Origin, Date
from brisbane_sunset.grid import setup_transformer
from brisbane_sunset.dusk import (standard_preparation,
                                  interp_wrapper,
                                  time_blocked)

from matplotlib import pyplot as plt


if __name__ == "__main__":

    year = 2024
    month = 11
    day = 10

    distance = 1800.0

    draw_plots = True

    raster_fname = "data/n37_w123_subset_reproject.tif"
    coord_mode = "xy"
    epsg_latlon = 4326

    # # Large region
    # sample_bounds_low = (37.67386, -122.43312)
    # sample_bounds_high = (37.69962, -122.37918)

    # Small region
    sample_bounds_low = (37.676, -122.410)
    sample_bounds_high = (37.686, -122.394)

    print("prep")

    rd, interp, transformer = standard_preparation(
        raster_fname,
        epsg_latlon)

    plt.pcolormesh(rd.lons_grid, rd.lats_grid, rd.values_grid)
    plt.show()

    x_low, y_low = transformer.transform(sample_bounds_low[0],
                                         sample_bounds_low[1])
    x_high, y_high = transformer.transform(sample_bounds_high[0],
                                           sample_bounds_high[1])

    # x_range = rd.lons_grid[(rd.lons_grid > x_low) & (rd.lons_grid < x_high)]
    # y_range = rd.lats_grid[(rd.lats_grid > y_low) & (rd.lats_grid < y_high)]

    xt = (rd.lons_grid[0, :] > x_low) & (rd.lons_grid[0, :] < x_high)
    yt = (rd.lats_grid[:, 0] > y_low) & (rd.lats_grid[:, 0] < y_high)
    vals = rd.values_grid[:, xt]
    vals = vals[yt, :]
    xs = rd.lons_grid[:, xt]
    xs = xs[yt, :]
    ys = rd.lats_grid[:, xt]
    ys = ys[yt, :]

    fig, ax = plt.subplots()
    CS = ax.contour(rd.lons_grid, rd.lats_grid, rd.values_grid, levels=20,
                    linewidths=0.5, vmin=10, colors="k")
    ax.pcolormesh(xs, ys, vals)
    # ax.clabel(CS, inline=True, fontsize=10)
    ax.plot(x_low, y_low, "ro")
    ax.plot(x_high, y_high, "ro")
    plt.colorbar(CS)
    plt.show()

    transformer2 = setup_transformer(rd.crs.to_epsg(), epsg_latlon)

    n = 0
    nt = vals.shape[0] * vals.shape[1]

    results = np.ones_like(vals) * (12. + 3.)

    for i in range(vals.shape[0]):
        for j in range(vals.shape[1]):

            x_origin = xs[i, j]
            y_origin = ys[i, j]

            lat_origin, lon_origin = transformer2.transform(y_origin, x_origin)

            origin = Origin(lat_origin, lon_origin,
                            interp_wrapper(
                                interp, x_origin, y_origin))
            origin.init_xy(x_origin, y_origin)

            date = Date(year, month, day)

            dt_orig = time_blocked(origin, distance, date, interp, rd,
                                   draw_plots=False,
                                   coord_mode=coord_mode)

            if n % 100 == 0:
                print(n, "out of", nt, dt_orig.hour, dt_orig.minute)

            results[i, j] = dt_orig.hour + dt_orig.minute / 60 - 12

            n += 1

    np.savetxt("results.csv", results, delimiter=",", fmt="%.2f")
    np.save("results.npy", results)

    fig, ax = plt.subplots()
    ax.contour(rd.lons_grid, rd.lats_grid, rd.values_grid, levels=20,
               linewidths=0.5, vmin=10, colors="k")
    pcm = ax.pcolormesh(xs, ys, results, cmap="viridis")
    ax.plot(x_low, y_low, "ro")
    ax.plot(x_high, y_high, "ro")
    plt.colorbar(pcm)
    plt.show()
    # plt.savefig("figs/grid_result.png")
    # plt.close()
