import xml.etree.ElementTree as ET
import haversine
import pandas as pd

from statistics import median
from math import sqrt, floor
from datetime import datetime


GPX_NAMESPACE = '{http://www.topografix.com/GPX/1/1}'


class Trackpoint(object):

    def __init__(self, elem):
        self.elem = elem

    @property
    def longitude(self):
        return float(self.elem.attrib["lon"])

    @property
    def latitude(self):
        return float(self.elem.attrib["lat"])

    @property
    def elevation(self):
        return float(self.elem.find(GPX_NAMESPACE + "ele").text)

    @property
    def time(self):
        value = self.elem.find(GPX_NAMESPACE + "time").text
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def to_dict(self):
        return {
            'long': self.longitude,
            'lat': self.latitude,
            'elev': self.elevation,
            'time': self.time
        }

    def __str__(self):
        return "#lat {0} #lon {1} #elev {2} #time {3}".format(
            self.lon, self.lat, self.elevation, self.time)


class TrackSegment(object):

    def __init__(self, elem):
        self.elem = elem
        self.points = [Trackpoint(
            el) for el in self.elem.findall(GPX_NAMESPACE + "trkpt")]


class Track(object):

    def __init__(self, elem):
        self.elem = elem
        self.segments = [TrackSegment(x)
                         for x in elem.findall(GPX_NAMESPACE + "trkseg")]

    @property
    def name(self):
        return self.elem.find(GPX_NAMESPACE + 'name').text

    def __str__(self):
        return "{0}".format(self.name)


class Gpx(object):

    def __init__(self, elem):
        self.tracks = [Track(x) for x in elem.findall(GPX_NAMESPACE + "trk")]
        self.elem = elem


class InvalidGpxFile(Exception):
    pass


def parse(file):
    tree = ET.parse(file)
    root = tree.getroot()

    if root.tag != GPX_NAMESPACE + "gpx":
        raise InvalidGpxFile()

    gpx = Gpx(root)
    return gpx
