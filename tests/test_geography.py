from math import sqrt

import numpy as np
from numpy.testing import assert_allclose

from brisbane_sunset.geography import (
    card_to_cart, xy_range_from_az
)


def test_card_to_cart():

    xy_90 = card_to_cart(2.6, 90.)
    assert_allclose(xy_90, [2.6, 0.], rtol=1e-10)

    xy_60 = card_to_cart(1.0, 60.)
    assert_allclose(xy_60, [sqrt(3.) / 2., 0.5], rtol=1e-10)


def test_xy_range_from_az():

    distance_list = np.array([0, 1])

    x_origin = 1.1
    y_origin = 2.2

    y_list_90, x_list_90 = xy_range_from_az(y_origin, x_origin,
                                            90., distance_list)

    assert_allclose([2.2, 2.2], y_list_90)
    assert_allclose([1.1, 2.1], x_list_90)
