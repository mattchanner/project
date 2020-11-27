import xml.etree.ElementTree as ET
import haversine
import pandas as pd

from statistics import median
from math import sqrt, floor
from datetime import datetime


GPX_NAMESPACE = '{http://www.topografix.com/GPX/1/1}'
TRACKPOINT_EXTENSION_NS = '{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}'


class Trackpoint(object):
    """
    Represents a single track point
    """

    def __init__(self, elem):
        """
        Initializes a new instance of the Trackpoint class
        @param elem The XML element this point represents
        """
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

    @property
    def extensions(self):
        ext_elem = self.elem.find(GPX_NAMESPACE + "extensions")
        extensions = []
        if ext_elem:
            trackpoint = ext_elem.find(
                TRACKPOINT_EXTENSION_NS + "TrackPointExtension")
            if trackpoint:
                for child in trackpoint:
                    extensions.append({'name': child.tag.replace(
                        TRACKPOINT_EXTENSION_NS, ''), 'value': child.text})

        return extensions

    def to_dict(self):

        d = {
            'lng': self.longitude,
            'lat': self.latitude,
            'elev': self.elevation,
            'time': self.time
        }

        extensions = self.extensions
        if extensions:
            for ext in extensions:
                d['ext:' + ext['name']] = float(ext['value'])

        return d

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
