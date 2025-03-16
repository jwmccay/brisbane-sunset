"""
Main functions for finding sunsets
"""

import numpy as np

from brisbane_sunset.solar import (input_to_datetime,
                                   sun_alt_az_suncalc,
                                   phi_critical,
                                   get_sunset_time)
from brisbane_sunset.geography import (coordinate_range_from_az,
                                       xy_range_from_az)
from brisbane_sunset.plots import make_plots
from brisbane_sunset.grid import (RasterData,
                                  setup_interpolator,
                                  setup_transformer)


def standard_preparation(raster_fname,
                         epsg_latlon=None):

    rd = RasterData(raster_fname)
    interp = setup_interpolator(rd)

    if epsg_latlon is not None:
        transformer = setup_transformer(epsg_latlon, rd.crs.to_epsg())
    else:
        transformer = None

    return rd, interp, transformer


def interp_wrapper(interp, lon_list, lat_list):
    return interp(lon_list, lat_list)


def time_blocked(origin, max_distance, date, interp, rd,
                 draw_plots=False,
                 coord_mode="latlon",
                 num_points=100,
                 fig_dir=None):
    """Find time when a point can no longer see the sun.

    Parameters
    ----------
    origin : containers.Origin
        Location of observer
    max_distance : float
        Distance to check for interpolation (padded by 50%)
    date : containers.Date
        Day for calculation
    rd : grid.RasterData
        Raster for use in plotting
    draw_plots : bool
        Whether to draw plots
    coord_mode : str
        Mode for calculating coordinates. Either `xy` or `latlon`. Note
        that `xy` is faster.
    num_points : int
        Number of points to use for interpolation. More points is more
        accurate but slower.
    fig_dir : Path or None
        Directory to write figures to. If None, figures are shown
        rather than written.

    Returns
    -------
    dt : datetime
        Sunset time in local timezone
    """

    distance_list = np.linspace(1.0, max_distance * 1.5,
                                num=num_points)

    dt, dt_utc = input_to_datetime(date.year, date.month, date.day,
                                   13, 0,
                                   'America/Los_Angeles')

    sunset_time = get_sunset_time(dt_utc, origin.lat, origin.lon,
                                  'America/Los_Angeles')

    minute = sunset_time.minute
    hour = sunset_time.hour

    is_blocked = True

    # walk backwards from sunset until you can see the sun
    while is_blocked:

        # This step is quite slow and could probably be sped up by subtracting
        # a time delta from an initial time
        dt, dt_utc = input_to_datetime(date.year, date.month, date.day,
                                       hour, minute,
                                       'America/Los_Angeles')

        if minute == 0:
            hour -= 1
            minute = 59
        else:
            minute -= 1

        alt, az = sun_alt_az_suncalc(dt_utc, origin.lat, origin.lon)

        if coord_mode == "xy":
            lat_list, lon_list = xy_range_from_az(
                origin.y, origin.x, az, distance_list)
        elif coord_mode == "latlon":
            lat_list, lon_list = coordinate_range_from_az(
                origin.lat, origin.lon, az, distance_list)
        else:
            raise ValueError("Invalid coordinate mode.")

        interp_range = interp_wrapper(interp, lon_list, lat_list)

        phi_range = phi_critical(np.array(distance_list),
                                 np.array(interp_range),
                                 origin.elevation)
        phi_range[phi_range < 0] = 0.

        # if sun is above the most-blocking point, then it's visible
        if alt > np.max(phi_range):
            # print(alt, az)
            is_blocked = False

        # catch winter edge cases for now by cutting off at noon
        if hour == 12 and minute == 0:
            is_blocked = False

    if draw_plots:

        make_plots(rd, lon_list, lat_list,
                   distance_list, interp_range, phi_range, alt,
                   fig_dir=fig_dir)

    return dt
