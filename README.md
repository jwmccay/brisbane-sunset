# San Bruno Sunset

[![Test and lint](https://github.com/jwmccay/brisbane-sunset/actions/workflows/python-package.yml/badge.svg)](https://github.com/jwmccay/brisbane-sunset/actions/workflows/python-package.yml) [![Sphinx deployment](https://github.com/jwmccay/brisbane-sunset/actions/workflows/sphinx.yml/badge.svg)](https://github.com/jwmccay/brisbane-sunset/actions/workflows/sphinx.yml)

## Install

Normal usage:
```shell
pip install .
```

## Usage

Note: work-in-progress theory and API documentation can be found at https://www.smilacina.com/brisbane-sunset/.

### Step 1: Acquire an SRTM raster

There are a few different ways to do this, but the easiest is via [EarthExplorer](https://earthexplorer.usgs.gov). Look for the SRTM 1 Arc-Second Global DEM data and note that downloads require an account.

### Step 2: Reproject the raster

The SRTM tile is 1-arcsecond square which is much larger than needed for shading calculations. The large tile size makes loading the raster and any interpolation quite slow. `subset_tif.py` is provided to subset the raster. The bounds required by `subset_tif.py` can be found by viewing the initial file with `view_tif.py` with default settings. Typical usage for this step is:

```shell

# View raster and find bounds using the magnifying glass tool in
# the matplotlib viewer.
python view_tif.py -c Spectral_r data/n37_w123_1arc_v3.tif

# Subset it (more details about what the bounds are in the script)
python subset_tif.py \
    -i "data/n37_w123_1arc_v3.tif" \
    -o "data/n37_w123_subset.tif" \
    -b 1900 900 400 400
```

SRTM data comes in the EPSG 4326 CRS, which is a latitude/longitude dataset. Downstream tools support using this coordinate system, but they are faster if given an x/y coordinate system. The `reproject_tif.py` utility is provided to make that transformation. Typical usage is:

```shell
python reproject_tif.py \
    -i data/n37_w123_subset.tif \
    -o data/n37_w123_subset_reproject.tif \
    -e 7131
```

### Step 3: Compute sunset times

To write later...

## Development

Development installation:
```shell
pip install -e .[dev]
```

To build documentation:
```shell
sphinx-build -M html docs/ docs/_build/
```