"""
Convenience containers
"""


class Date:

    def __init__(self, year, month, day):

        self.year = year
        self.month = month
        self.day = day


class Origin:

    def __init__(self, lat, lon, elevation):
        self.lat = lat
        self.lon = lon
        self.elevation = elevation

    def init_xy(self, x, y):
        self.x = x
        self.y = y
