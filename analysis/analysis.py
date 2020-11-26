import haversine
import pandas as pd

from statistics import median
from math import sqrt, floor
from datetime import datetime

METRES_PER_SECOND_TO_MIN_PER_KM = 16.666666667

METRES_IN_KM = 1000


class SummaryData:

    def __init__(self):
        pass

    def calculate_average_pace(self):
        pass

    def print_summary(df, name):

        print('Results for ', name)
        print('-' * 120)
        total_time_diff = sum(df['time_diff'])
        average_pace = sum(df['pace_km']) / len(df['pace_km'])
        hav_2d = df['dist_hav_2D']
        hav_3d = df['dist_hav_3D']

        distance_total = hav_2d[len(hav_2d)-1]
        distance_km = floor(distance_total / 1000)
        distance_m = int(distance_total % 1000)
        print('Distance : {0}.{1}km'.format(distance_km, distance_m))

        time_hours = floor(total_time_diff / 60 / 60)
        time_mins = floor((total_time_diff-((time_hours * 60) * 60)) / 60)
        time_secs = int(total_time_diff % 60)
        print('Total time : {0}:{1}:{2}'.format(
            time_hours, time_mins, time_secs))

        pace_mins = int(floor(average_pace))
        pace_secs = int(60 * (average_pace - pace_mins))
        print('Average Pace : {0}:{1}/km'.format(pace_mins, pace_secs))

        gain = sum([x for x in df['elevation_diff'] if x > 0])
        print('Gain = {0}m'.format(int(gain)))
        print('-' * 120)

        print(df)


def smooth(data, points):
    return [median(data[x:x+points]) for x in range(0, len(data))]


def trackpoints_to_dataframe(points):
    data = []
    for pt in points:
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

    for index in range(1, len(points)):
        start = points[index-1]
        stop = points[index]

        # Calculate the great-circle distance between 2 points in metres
        # This is without taking into account the elevation difference
        distance_hav_2D = haversine.haversine(
            (start.latitude, start.longitude),
            (stop.latitude, stop.longitude)) * METRES_IN_KM

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
        pace_km.append(
            0 if point_speed == 0 else METRES_PER_SECOND_TO_MIN_PER_KM / float(point_speed))

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
