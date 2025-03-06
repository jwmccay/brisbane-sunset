import pathlib
from datetime import datetime

from brisbane_sunset.scripts.reproject_tif import reproject_tif_main
from brisbane_sunset.scripts.run_combined import run_combined_main


def test_run_combined_runs(synthetic_raster):

    dt = run_combined_main("2025-1-18", "37.6924344,-122.4150331",
                           synthetic_raster, "xy", False, None)

    assert isinstance(dt, datetime)


def test_run_combined_reprojected(synthetic_raster, reproject_raster):

    reproject_tif_main("7131", synthetic_raster, reproject_raster)
    dt = run_combined_main("2025-1-18", "37.6924344,-122.4150331",
                           reproject_raster, "xy", False, None)

    # NOTE: just a stability test for now since the raster doesn't
    # make a lot of sense.

    assert dt.hour == 17


def test_reproject_tif_runs(synthetic_raster, reproject_raster):

    reproject_tif_main("7131", synthetic_raster, reproject_raster)
    assert pathlib.Path.exists(reproject_raster)
