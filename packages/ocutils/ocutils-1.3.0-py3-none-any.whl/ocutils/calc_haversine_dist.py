import numpy

from ocutils import earth_radius as earth_rad


def calc_haversine_dist(lat1, lon1, lat2, lon2, earth_radius=None):

    """
    Function to calculate the haversine distance between two sets of latitude & longitude coordinates.
    Inputs can be 1D NumPy arrays or single values.

    args...
        lat1: start latitude (decimal degrees)
        lon1: start longitude (decimal degrees)
        lat2: end latitude (decimal degrees)
        lon2: end longitude (decimal degrees)
    kwargs...
        earth_radius: value for Earth radius (m) to override default
    returns...
        d: haversine distance (m)
    """

    if earth_radius is None:
        earth_radius = earth_rad

    lat1r = numpy.deg2rad(lat1)
    lat2r = numpy.deg2rad(lat2)
    lon1r = numpy.deg2rad(lon1)
    lon2r = numpy.deg2rad(lon2)

    dlat2 = (lat2r - lat1r) / 2
    dlon2 = (lon2r - lon1r) / 2

    d = 2 * earth_radius * numpy.arcsin(numpy.sqrt(numpy.sin(dlat2) ** 2 +
                                                   numpy.cos(lat1r) * numpy.cos(lat2r) *
                                                   numpy.sin(dlon2) ** 2))

    return d
