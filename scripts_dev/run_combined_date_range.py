"""
Combined calc
"""

import datetime
from matplotlib import pyplot as plt

from brisbane_sunset.containers import Origin, Date
from brisbane_sunset.dusk import (standard_preparation,
                                  interp_wrapper,
                                  time_blocked)


if __name__ == "__main__":

    lon_origin = -122.4150331485603
    lat_origin = 37.692434406915844

    distance = 1800.0

    draw_plots = True

    # coord_mode = "latlon"
    # raster_fname = "data/n37_w123_subset.tif"
    # epsg_latlon = None

    raster_fname = "data/n37_w123_subset_reproject.tif"
    coord_mode = "xy"
    epsg_latlon = 4326

    print("prep")

    rd, interp, transformer = standard_preparation(
        raster_fname,
        epsg_latlon)

    if coord_mode == "xy":
        x_origin, y_origin = transformer.transform(
            lat_origin, lon_origin)
    elif coord_mode == "latlon":
        x_origin = lon_origin
        y_origin = lat_origin

    origin = Origin(lat_origin, lon_origin,
                    interp_wrapper(
                        interp, x_origin, y_origin))
    origin.init_xy(x_origin, y_origin)

    dt_list = []

    base = datetime.datetime(2025, 1, 1, 1, 1)
    day_list = [base + datetime.timedelta(days=x) for x in range(365)]
    hour_list = []

    i = 0

    for day in day_list:
        date = Date(day.year, day.month, day.day)
        dt_day = time_blocked(origin, distance, date, interp, rd,
                              draw_plots=False,
                              coord_mode=coord_mode,
                              num_points=1000)

        dt_list.append(dt_day)

        hour_list.append(dt_day.hour - 12 + dt_day.minute / 60)

        print(i, hour_list[-1])
        i += 1

    if draw_plots:
        plt.plot(day_list, hour_list)
        plt.grid()
        plt.xlabel("Date")
        plt.ylabel("Sunset time [hour since noon]")
        plt.savefig("figs/date_range_dusk.png")
        plt.close()
