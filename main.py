import os
import re
import datetime
import matplotlib.pyplot as plt
import haversine

from os import path
from gpx import parse
from analysis import trackpoints_to_dataframe
from charts import composite_chart
from math import sqrt, floor


def get_gpx_data(file):
    gpx = parse(file)
    name = gpx.tracks[0].name
    df = trackpoints_to_dataframe(gpx.tracks[0].segments[0].points)
    return (df, name)


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
    print('Total time : {0}:{1}:{2}'.format(time_hours, time_mins, time_secs))

    pace_mins = int(floor(average_pace))
    pace_secs = int(60 * (average_pace - pace_mins))
    print('Average Pace : {0}:{1}/km'.format(pace_mins, pace_secs))

    gain = sum([x for x in df['elevation_diff'] if x > 0])
    print('Gain = {0}m'.format(int(gain)))
    print('-' * 120)

    print(df)


def generate_plots(df, name):

    if not os.path.exists('results'):
        os.mkdir('results')

    # Replace any invalid file system characters with an underscore and then generate a folder
    # to output the results
    folder = re.sub('[^\w\-_\. ]', '_', name)
    if not os.path.exists('results/' + folder):
        os.mkdir('results/' + folder)

    composite_chart(df, name, 'results/' + folder + '/summary.png')


def process_file(filename):
    df, name = get_gpx_data(filename)
    print_summary(df, name)
    generate_plots(df, name)


for file in os.listdir('gpxfiles'):
    process_file('gpxfiles/' + file)
