import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


EXTENSION_MAP = {
    'atemp': {
        'name': 'Temperature',
        'label': 'Temperature (C)',
        'title': 'Temperature',
        'color': 'tab:orange'
    },
    'cad': {
        'name': 'Cadence',
        'label': 'Cadence',
        'title': 'Cadence',
        'color': 'tab:green'
    },
    'hr': {
        'name': 'Heart Rate',
        'label': 'Heart Rate (bpm)',
        'title': 'Heart Rate',
        'color': 'tab:red'
    }
}


def pace_chart(df, axs):
    x, y = 'dist_hav_3D', 'pace_km_smoothed'
    xdata = [x / 1000 for x in df[x]]

    color = '#34ACE4'

    axs.plot(xdata, df[y], color=color)
    axs.set_ylabel('Pace min/km', color=color)
    axs.tick_params(axis='y', labelcolor=color)
    axs.set_xlabel('Distance (km)')
    axs.invert_yaxis()


def elevation_chart(df, axs):
    x, y = 'dist_hav_3D', 'elev'
    xdata = [x / 1000 for x in df[x]]

    color = 'tab:purple'

    axs.plot(xdata, df[y], linewidth=1, color='tab:purple')
    axs.fill_between(
        xdata,
        df[y],
        interpolate=True,
        alpha=0.20,
        color='tab:purple')
    axs.set_ylabel('Elevation (m)', color=color)
    axs.set_xlabel('Distance (km)')
    axs.tick_params(axis='y', labelcolor=color)
    axs.set_ylim(min(df['elev']) - 15, max(df['elev'] + 200))
    axs.grid(which='major', axis='y', color='#ddd',
             linestyle='-', linewidth=1)


def latlong(df, axs):
    axs.plot(df['lng'], df['lat'], color='tab:orange')
    axs.set_yticklabels([])
    axs.set_xticklabels([])
    axs.axis('off')


def composite_chart(df, title, filename):
    plt.close()

    fig2x2 = plt.figure(constrained_layout=True, figsize=(10, 3))

    widths = [1]
    heights = [1]

    grid_spec = gridspec.GridSpec(
        ncols=1, nrows=1, width_ratios=widths, height_ratios=heights, figure=fig2x2)

    elevation_axs = fig2x2.add_subplot(grid_spec[0:, :])

    elevation_chart(df, elevation_axs)

    pace_axs = elevation_axs.twinx()
    pace_chart(df, pace_axs)

    plt.savefig(filename, dpi=96, format='png',
                orientation='landscape')

    plt.close()


def generate_extension_charts(df, folder):
    generated_files = []

    xdata = [x / 1000 for x in df['dist_hav_3D']]

    for col in [col for col in df.columns if col.startswith('ext:')]:
        display_name = col[4:]
        if display_name in EXTENSION_MAP:
            extension_info = EXTENSION_MAP[display_name]
            fig, axs = plt.subplots()
            fig.set_size_inches(10, 4)

            axs.plot(xdata, df[col], linewidth=1,
                     color=extension_info['color'])
            axs.set_xlabel('Distance (km)')
            axs.set_ylabel(extension_info['label'])
            axs.set_title(extension_info['title'])

            file_name = extension_info['name'] + '.png'
            full_path = folder + '/' + file_name
            plt.savefig(full_path)
            plt.close()

            generated_files.append(file_name)

    return generated_files
