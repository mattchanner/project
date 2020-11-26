import os
import re
import datetime
import matplotlib.pyplot as plt
import haversine
from jinja2 import Template

from os import path
from gpx import parse
from analysis import trackpoints_to_dataframe, create_summary
from charts import composite_chart
from math import sqrt, floor


def get_gpx_data(file):
    gpx = parse(file)
    name = gpx.tracks[0].name
    df = trackpoints_to_dataframe(gpx.tracks[0].segments[0].points)
    return (df, name)


def generate_plots(df, name):
    if not os.path.exists('results'):
        os.mkdir('results')

    # Replace any invalid file system characters with an underscore and then generate a folder
    # to output the results
    folder = re.sub('[^\w\-_\. ]', '_', name)
    full_path = 'results/' + folder
    if not os.path.exists(full_path):
        os.mkdir(full_path)

    chart_filename = 'summary.png'
    chart_filepath = full_path + '/' + chart_filename
    composite_chart(df, name, chart_filepath)

    return (full_path, chart_filename)


def write_html(df, name, folder, chart_filename):

    summary = create_summary(df, name)
    with open('templates/page.jinja') as fp:
        template = Template(fp.read())

    with open(folder + '/index.html', 'w') as fp:
        fp.write(template.render({
            'name': name,
            'summary_table': summary.to_html(),
            'filename': chart_filename,
            'dataframe': df.to_html()
        }))


def process_file(filename):
    df, name = get_gpx_data(filename)
    folder_path, chart_filename = generate_plots(df, name)
    write_html(df, name, folder_path, chart_filename)


for file in os.listdir('gpxfiles'):
    process_file('gpxfiles/' + file)
