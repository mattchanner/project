import os
import re
import datetime
import matplotlib.pyplot as plt
import haversine
import json

from jinja2 import Template
from os import path
from gpx import parse
from analysis import trackpoints_to_dataframe, create_summary
from charts import composite_chart, generate_extension_charts
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
    full_path = os.path.join('results', folder)

    if not os.path.exists(full_path):
        os.mkdir(full_path)

    chart_filename = 'summary.png'
    chart_filepath = os.path.join(full_path, chart_filename)
    composite_chart(df, name, chart_filepath)
    generated_charts = generate_extension_charts(df, full_path)

    return (full_path, chart_filename, generated_charts)


def write_html(df, name, folder, chart_filename, extension_charts):

    summary = create_summary(df, name)
    with open(os.path.join('templates', 'page.jinja')) as fp:
        template = Template(fp.read())

    with open(os.path.join(folder, 'index.html'), 'w') as fp:
        fp.write(template.render({
            'name': name,
            'summary_table': summary.to_html(),
            'filename': chart_filename,
            'points': json.dumps([{'lng': lng, 'lat': lat} for (lng, lat) in zip(df['lng'], df['lat'])]),
            'dataframe': df.to_html(),
            'extension_charts': extension_charts
        }))


def process_file(filename):
    df, name = get_gpx_data(filename)
    folder_path, chart_filename, extension_charts = generate_plots(df, name)
    write_html(df, name, folder_path, chart_filename, extension_charts)


for file in os.listdir('gpxfiles'):
    process_file(os.path.join('gpxfiles', file))
