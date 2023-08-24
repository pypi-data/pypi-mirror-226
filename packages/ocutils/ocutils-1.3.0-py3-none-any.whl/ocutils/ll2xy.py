"""
ll2xy function definition
"""

import numpy
from ocutils import earth_radius as earth_rad


def ll2xy(lat, lon, latc, lonc, earth_radius=None):

    """
    Convert from latitude and longitude to Cartesian coordinates using a flat Earth approximation.

    args...
        lat: latitude (degrees), single value or NumPy array
        lon: longitude (degrees), single value or NumPy array
        latc: central latitude (degrees)
        lonc: central longitude (degrees)
    kwargs...
        earth_radius: value for Earth radius (m) to override default
    returns...
        x: Cartesian x coordinate (m), same type as lon
        y: Cartesian y coordinate (m), same type as lat
    """

    if earth_radius is None:
        earth_radius = earth_rad

    y = earth_radius * numpy.deg2rad(lat - latc)
    x = earth_radius * numpy.cos(numpy.deg2rad(latc)) * numpy.deg2rad(lon - lonc)

    return x, y
