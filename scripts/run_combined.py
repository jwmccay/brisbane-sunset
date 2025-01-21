"""
Combined calc
"""

from brisbane_sunset.containers import Origin, Date
from brisbane_sunset.dusk import (standard_preparation,
                                  interp_wrapper,
                                  time_blocked)


if __name__ == "__main__":

    year = 2025
    month = 1
    day = 18
    distance = 1800.0

    # Mission Blue
    lon_origin = -122.4150331485603
    lat_origin = 37.692434406915844

    draw_plots = True

    # interp_mode = "RegularGrid"
    interp_mode = "LinearND"

    # coord_mode = "latlon"
    # raster_fname = "data/n37_w123_subset.tif"
    # epsg_latlon = None
    # epsg_xy = None

    raster_fname = "data/n37_w123_subset_reproject.tif"
    coord_mode = "xy"
    epsg_latlon = 4326
    epsg_xy = 7131

    rd, interp, transformer = standard_preparation(
        raster_fname,
        interp_mode,
        epsg_latlon, epsg_xy)

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

    date = Date(year, month, day)

    dt = time_blocked(origin, distance, date, interp, rd,
                      draw_plots=draw_plots,
                      interp_mode=interp_mode,
                      coord_mode=coord_mode,
                      num_points=10000)

    hour = dt.hour - 12
    minute = str(dt.minute).rjust(2, "0")

    print(f"Sunset at {hour}:{minute} on {dt.month}/{dt.day}/{dt.year}")
