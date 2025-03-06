from datetime import datetime

from brisbane_sunset.scripts.run_combined import run_combined_main


def test_run_combined_runs(synthetic_raster):

    dt = run_combined_main("2025-1-18", "37.6924344,-122.4150331",
                           synthetic_raster, "xy", False, None)

    assert isinstance(dt, datetime)
