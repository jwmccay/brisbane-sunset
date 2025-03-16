import pathlib
from datetime import datetime

import pytest

from brisbane_sunset.scripts.reproject_tif import reproject_tif_main
from brisbane_sunset.scripts.run_combined import run_combined_main


@pytest.fixture
def synth_origin():
    return "37.78,-122.403"


@pytest.fixture
def winter_date():
    return "2025-1-18"


def test_run_combined_runs(synthetic_raster, synth_origin, winter_date):

    dt = run_combined_main(winter_date, synth_origin,
                           synthetic_raster, "xy", False, None)

    assert isinstance(dt, datetime)


def test_run_combined_xy(synthetic_raster, reproject_raster,
                         winter_date, synth_origin):

    reproject_tif_main("7131", synthetic_raster, reproject_raster)
    dt = run_combined_main(winter_date, synth_origin,
                           reproject_raster, "xy", False, None)

    # To avoid making tests unstable, check that the hour is right and
    # minutes are within three of the test. Note that the current test
    # is showing 4:18 on 2025-01-18.
    assert dt.hour == 16
    assert abs(dt.minute - 8) < 3


def test_run_combined_latlon(synthetic_raster, reproject_raster,
                             winter_date, synth_origin):

    dt = run_combined_main(winter_date, synth_origin,
                           synthetic_raster, "latlon", False, None)

    # Should be similar to xy but slower.
    assert dt.hour == 16
    assert abs(dt.minute - 8) < 3


def test_reproject_tif_runs(synthetic_raster, reproject_raster):

    reproject_tif_main("7131", synthetic_raster, reproject_raster)
    assert pathlib.Path.exists(reproject_raster)
