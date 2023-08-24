"""
xy2ll function definition
"""

import numpy
from ocutils import earth_radius as earth_rad


def xy2ll(x, y, latc, lonc, earth_radius=None):

    """
    Convert from Cartesian coordinates to latitude and longitude using a flat Earth approximation.

    args...
        x: Cartesian x coordinate (m), single value or NumPy array
        y: Cartesian y coordinate (m), single value or NumPy array
        latc: central latitude (degrees)
        lonc: central longitude (degrees)
    kwargs...
        earth_radius: value for Earth radius (m) to override default
    returns...
        lat: latitude (degrees), same type as y
        lon: longitude (degrees), same type as x
    """

    if earth_radius is None:
        earth_radius = earth_rad

    lat = latc + numpy.rad2deg(y / earth_radius)
    lon = lonc + numpy.rad2deg(x / (earth_radius * numpy.cos(numpy.deg2rad(latc))))

    return lat, lon
