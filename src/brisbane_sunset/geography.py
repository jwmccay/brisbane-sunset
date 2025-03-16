"""
Functions for basic geographic calcs
"""

import numpy as np
from geopy import Point
from geopy.distance import geodesic, great_circle


def card_to_cart(radius: np.ndarray, phi: float):
    """Find an xy coordinate given a radius and a cardinal direction

    Radius can be an array to support typical ussage in this project,
    giving a number of points along a vector. The direction must be
    cardinal degrees (0 is up, 90 is right).

    Parameters
    ----------
    radius: np.array or float
        Array or single value of radii
    phi : float
        Direction in cardinal degrees

    Returns
    -------
    x : np.array or float
        Array or single value of x coordinates
    y : np.array or float
        Array or single value of y coordinates
    """

    # convert from cardinal polar to math polar
    phi_polar = phi - 90.
    if phi <= 90.:
        phi_polar = phi_polar * -1
    else:
        phi_polar = 360. - phi_polar

    # convert to radians
    phi_polar = np.pi * phi_polar / 180.0

    x = radius * np.cos(phi_polar)
    y = radius * np.sin(phi_polar)

    return x, y


def xy_range_from_az(y_origin, x_origin, azimuth, distance_list):

    x_list, y_list = card_to_cart(distance_list, azimuth)

    x_list = x_list + x_origin
    y_list = y_list + y_origin

    return y_list, x_list


def coordinate_from_az(origin, azimuth, dist,
                       distance_method="great_circle"):

    if distance_method == "great_circle":
        distance_func = great_circle
    else:
        distance_func = geodesic

    destination = distance_func(
        kilometers=dist / 1000.).destination(origin, azimuth)

    return destination


def coordinate_range_from_az(lat_origin, lon_origin,
                             azimuth, distance_list):
    """Get lat, lon, and distance lists along an azimuth
    """

    origin = Point(lat_origin, lon_origin)

    lat_list = []
    lon_list = []

    for dist in distance_list:

        destination = coordinate_from_az(origin, azimuth, dist)

        lat_list.append(destination.latitude)
        lon_list.append(destination.longitude)

    return lat_list, lon_list
