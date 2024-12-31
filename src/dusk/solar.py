"""
Functions related to sun position.
"""

from datetime import datetime

import numpy as np
import pytz
from suncalc import get_position, get_times


def input_to_datetime(year, month, day, hour, minute, tz):

    dt_base = datetime(year, month, day, hour, minute)
    tz = pytz.timezone(tz)
    dt = tz.localize(dt_base)
    dt_utc = dt.astimezone(pytz.timezone("UTC"))

    return dt, dt_utc


def get_sunset_time(dt_utc, lat, lon, tz_local):

    times = get_times(dt_utc, lon, lat)

    sunset_time = times["sunset"]

    tz_utc = pytz.timezone("UTC")
    sunset_time = tz_utc.localize(sunset_time)
    sunset_time_localized = sunset_time.astimezone(
        pytz.timezone(tz_local))

    return sunset_time_localized


def sun_alt_az_suncalc(dt_utc, lat, lon):
    """Altitude and azimuth for sun from observation point.
    """

    pos = get_position(dt_utc, lon, lat)

    alt = pos["altitude"] * 180 / np.pi
    az = 180. + pos["azimuth"] * 180 / np.pi

    return alt, az


def phi_critical(distance, elevation_blocking, elevation_obs):
    """Angle at which the sun would be blocked
    """

    phi_crit = np.arctan(
        (elevation_blocking - elevation_obs) / distance)

    phi_crit = phi_crit * 180.0 / np.pi

    return phi_crit
