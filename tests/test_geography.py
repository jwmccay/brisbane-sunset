from math import sqrt

from numpy.testing import assert_allclose

from brisbane_sunset.geography import (
    card_to_cart
)


def test_card_to_cart():

    xy_90 = card_to_cart(2.6, 90.)
    assert_allclose(xy_90, [2.6, 0.], rtol=1e-10)

    xy_60 = card_to_cart(1.0, 60.)
    assert_allclose(xy_60, [sqrt(3.) / 2., 0.5], rtol=1e-10)
