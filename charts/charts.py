import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def pace_chart(df, axs):
    x, y = 'dist_hav_3D', 'pace_km_smoothed'
    xdata = [x / 1000 for x in df[x]]

    axs.plot(xdata, df[y], color='tab:red')
    axs.set_ylabel('Pace min/km')
    axs.set_xlabel('Distance (km)')


def elevation_chart(df, axs):
    x, y = 'dist_hav_3D', 'elev'
    xdata = [x / 1000 for x in df[x]]
    axs.plot(xdata, df[y], linewidth=1)
    axs.fill_between(
        xdata,
        df[y],
        interpolate=True,
        alpha=0.20)
    axs.set_ylabel('Elevation (m)')
    axs.set_xlabel('Distance (km)')


def latlong(df, axs):
    axs.plot(df['long'], df['lat'])
    axs.set_yticklabels([])
    axs.set_xticklabels([])
    axs.axis('off')


def composite_chart(df, filename):
    plt.close()

    fig2x2 = plt.figure(constrained_layout=True, figsize=(15, 10))

    widths = [1, 1]
    heights = [3, 1]

    grid_spec = gridspec.GridSpec(
        ncols=2, nrows=2, width_ratios=widths, height_ratios=heights, figure=fig2x2)

    lat_long_axs = fig2x2.add_subplot(grid_spec[0, :])
    latlong(df, lat_long_axs)

    elevation_axs = fig2x2.add_subplot(grid_spec[1:, 0])

    elevation_chart(df, elevation_axs)

    pace_axs = fig2x2.add_subplot(grid_spec[1:, 1:])
    pace_chart(df, pace_axs)

    plt.savefig(filename, dpi=96, format='png',
                orientation='landscape')

    plt.close()
