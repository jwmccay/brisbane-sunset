"""
Make plots
"""

from matplotlib import pyplot as plt


def make_plots(rd, lon_list, lat_list,
               distance_list, interp_range, phi_range, alt,
               fig_dir=None):

    plt.pcolormesh(rd.lons_grid, rd.lats_grid, rd.values_grid)
    plt.plot(lon_list, lat_list, "r-")
    if fig_dir is not None:
        plt.savefig(f"{fig_dir}/mesh.png")
        plt.close()
    else:
        plt.show()

    plt.plot(distance_list, interp_range)
    plt.grid()
    if fig_dir is not None:
        plt.savefig(f"{fig_dir}/height.png")
        plt.close()
    else:
        plt.show()

    plt.plot(distance_list, phi_range)
    plt.axhline(alt)
    plt.grid()
    if fig_dir is not None:
        plt.savefig(f"{fig_dir}/phi.png")
        plt.close()
    else:
        plt.show()
