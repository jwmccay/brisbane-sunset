"""
Combined calc
"""

import argparse

from brisbane_sunset.containers import Origin, Date
from brisbane_sunset.dusk import (standard_preparation,
                                  interp_wrapper,
                                  time_blocked)


def parse_date(date_string: str) -> Date:
    """"Turns YYYY-M(M)-D(D) string into Date object"""

    date_list = date_string.split("-")
    date_list = [int(d) for d in date_list]

    assert len(date_list) == 3, f"{date_string} cannot be parsed"

    date = Date(date_list[0], date_list[1], date_list[2])

    return date


def parse_coordinate(coord_string: str):
    """"Turns Lat,Lon into a two element list of floats

    The first element is the latitude and the second is the
    longitude. Both must be in decimal format.
    """

    coord_list = coord_string.split(",")
    coord_list = [float(c) for c in coord_list]

    assert len(coord_list) == 2, "too many or two few coordinate dimensions"

    return coord_list


def parse_args():

    parser = argparse.ArgumentParser(
                        prog='sunset-run-combined',
                        description='Reproject an SRTM tif')

    parser.add_argument("-r", "--raster")
    parser.add_argument("-d", "--date")
    parser.add_argument("-oc", "--origin_coordinate")
    parser.add_argument("-cm", "--coord_mode")
    parser.add_argument("-dp", "--draw_plots", action='store_true')
    parser.add_argument("-fd", "--figure_directory", default=None)
    args = parser.parse_args()

    return args


def run_combined_main(date_str, origin_coordinate, raster_fname, coord_mode,
                      draw_plots, figure_directory):

    date = parse_date(date_str)
    lat_origin, lon_origin = parse_coordinate(origin_coordinate)

    if coord_mode == "xy":
        epsg_latlon = 4326
    elif coord_mode == "latlon":
        epsg_latlon = None
    else:
        assert False, f"coord_mode {coord_mode} is not a valid coordinate mode"

    # Options that have not migrated to argparse yet
    distance = 1800.0
    num_points = 10000

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

    dt = time_blocked(origin, distance, date, interp, rd,
                      draw_plots=draw_plots,
                      coord_mode=coord_mode,
                      num_points=num_points,
                      fig_dir=figure_directory)

    return dt


def run_combined():
    args = parse_args()
    dt = run_combined_main(args.date, args.origin_coordinate, args.raster,
                           args.coord_mode, args.draw_plots,
                           args.figure_directory)

    hour = dt.hour - 12
    minute = str(dt.minute).rjust(2, "0")

    print(f"Sunset at {hour}:{minute} on {dt.month}/{dt.day}/{dt.year}")
