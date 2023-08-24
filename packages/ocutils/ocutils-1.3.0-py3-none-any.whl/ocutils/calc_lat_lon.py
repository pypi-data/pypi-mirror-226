import numpy

from ocutils import earth_radius as earth_rad


def calc_lat_lon(slat, slon, r, theta, earth_radius=None):

    """
    Function to calculate latitude and longitude coordinates at a single distance or multiple distances
    along a great circle arc from a starting latitude, longitude and bearing.

    args...
        slat: starting latitude (decimal degrees)
        slon: starting longitude (decimal degrees)
        r: 1D NumPy array (or single value) of distances (m)
        theta: bearing (degrees, clockwise from zero due north)
    kwargs...
        earth_radius: value for Earth radius (m) to override default
    returns...
        lats: 1D NumPy array (or single value) of latitudes (decimal degrees)
        lons: 1D NumPy array (or single value) of longitudes (decimal degrees)
    """

    if earth_radius is None:
        earth_radius = earth_rad

    delta = r / earth_radius
    cos_delta = numpy.cos(delta)
    sin_delta = numpy.sin(delta)

    sin_slat = numpy.sin(numpy.deg2rad(slat))
    cos_slat = numpy.cos(numpy.deg2rad(slat))

    cos_theta = numpy.cos(numpy.deg2rad(theta))
    sin_theta = numpy.sin(numpy.deg2rad(theta))

    sin_lat = sin_slat * cos_delta + cos_slat * sin_delta * cos_theta
    lats = numpy.rad2deg(numpy.arcsin(sin_lat))

    lons = slon + numpy.rad2deg(numpy.arctan2(sin_theta * sin_delta * cos_slat, cos_delta - sin_slat * sin_lat))

    return lats, lons
