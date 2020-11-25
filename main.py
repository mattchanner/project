import os
import re
import datetime
import matplotlib.pyplot as plt
import haversine

from os import path
from gpx.gpx import parse
from math import sqrt, floor


def get_gpx_data(file):
    gpx = parse(file)
    name = gpx.tracks[0].name
    df = gpx.tracks[0].segments[0].to_dataframe()
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


def generate_plot(df, x, y, xlabel, ylabel, title, filename):
    plt.cool()
    plt.plot(df[x], df[y])
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(False)
    plt.savefig(filename, orientation='landscape')
    plt.close()


def generate_plots(df, name):
    # Replace any invalid file system characters with an underscore and then generate a folder
    # to output the results
    folder = re.sub('[^\w\-_\. ]', '_', name)
    if not os.path.exists(folder):
        os.mkdir(folder)

    # generate individual plots
    generate_plot(
        df,
        'dist_hav_3D',
        'elev',
        'Distance',
        'Elevation',
        'Elevation Plot',
        folder + '/elevation-plot.png')

    generate_plot(
        df,
        'long',
        'lat',
        'longitude',
        'latitude',
        'Map',
        folder + '/map-plot.png')

    generate_plot(
        df,
        'dist_hav_3D',
        'pace_km_smoothed',
        'Distance',
        'Pace',
        'Pace Plot',
        folder + '/pace-plot.png')


def process_file(filename):
    df, name = get_gpx_data(filename)
    print_summary(df, name)
    generate_plots(df, name)


for file in os.listdir('gpxfiles'):
    process_file('gpxfiles/' + file)
