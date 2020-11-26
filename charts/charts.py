import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


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
    axs.plot(df['long'], df['lat'], color='tab:orange')
    axs.set_yticklabels([])
    axs.set_xticklabels([])
    axs.axis('off')


def composite_chart(df, title, filename):
    plt.close()

    fig2x2 = plt.figure(constrained_layout=True, figsize=(15, 10))

    widths = [1]
    heights = [1]

    grid_spec = gridspec.GridSpec(
        ncols=1, nrows=1, width_ratios=widths, height_ratios=heights, figure=fig2x2)

    # lat_long_axs = fig2x2.add_subplot(grid_spec[0, :])
    # latlong(df, lat_long_axs)

    elevation_axs = fig2x2.add_subplot(grid_spec[0:, :])

    elevation_chart(df, elevation_axs)

    pace_axs = elevation_axs.twinx()
    pace_chart(df, pace_axs)

    plt.savefig(filename, dpi=96, format='png',
                orientation='landscape')

    plt.close()
