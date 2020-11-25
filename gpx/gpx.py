import xml.etree.ElementTree as ET
import haversine
import pandas as pd

from statistics import median
from math import sqrt, floor
from datetime import datetime


GPX_NAMESPACE = '{http://www.topografix.com/GPX/1/1}'


def smooth(data, points):
    return [median(data[x:x+points]) for x in range(0, len(data))]


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

    def to_dataframe(self):
        data = []
        for pt in self.points:
            data.append(pt.to_dict())

        # Generate initial data frame from source GPX data
        df = pd.DataFrame(data=data, columns=['long', 'lat', 'elev', 'time'])

        # copmpute additional data based on source
        elevation_diff = [0]
        time_diff = [0]
        dist_haversine = [0]
        dist_hav_no_elev = [0]
        dist_diff_hav_2D = [0]
        speed = [0]
        pace_km = [0]

        for index in range(1, len(self.points)):
            start = self.points[index-1]
            stop = self.points[index]

            # Calculate the great-circle distance between 2 points in metres
            # This is without taking into account the elevation difference
            distance_hav_2D = haversine.haversine(
                (start.latitude, start.longitude),
                (stop.latitude, stop.longitude)) * 1000

            dist_diff_hav_2D.append(distance_hav_2D)

            dist_hav_no_elev.append(dist_hav_no_elev[-1] + distance_hav_2D)

            # Determine elevation difference between the 2 points
            elevation_delta = stop.elevation - start.elevation
            elevation_diff.append(elevation_delta)

            # Calculate distance between the 2 points by taking into account the elevation
            distance_hav_3D = sqrt(distance_hav_2D ** 2 + elevation_delta ** 2)

            dist_haversine.append(dist_haversine[-1] + distance_hav_3D)

            # Determine the time difference between the 2 points
            time_delta = (stop.time - start.time).total_seconds()
            time_diff.append(time_delta)

            # Calculate the speed (distance/time) - this will be in m/s
            point_speed = distance_hav_3D / \
                ((stop.time - start.time).total_seconds())
            speed.append(point_speed)

            # Calculate pace in min/km
            pace_km.append(16.666666667 / float(point_speed))

        df['dist_hav_2D'] = dist_hav_no_elev
        df['dist_hav_3D'] = dist_haversine

        # smooth the elevation data to get rid of any outliers
        df['elevation_diff'] = smooth(elevation_diff, 10)
        df['time_diff'] = time_diff
        df['speed'] = speed
        df['pace_km'] = pace_km

        # Smooth pace to remove any blips
        pace_km_smoothed = smooth(pace_km, 10)
        df['pace_km_smoothed'] = pace_km_smoothed

        return df


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
