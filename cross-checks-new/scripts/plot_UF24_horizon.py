import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

FIGURES_DIR = "../figures"
REFERENCES_DIR = "../references"
RESULTS_DIR = "../results"

CTSS = np.logspace(0, 2.5, num = 201)
ENERGY_EDGES = np.linspace(10**1.5, 10**3, num = 201)
ENERGY_CENTERS = (ENERGY_EDGES[:-1] + ENERGY_EDGES[1:]) / 2

plt.rcParams.update({
    'legend.fontsize': 'x-large',
    'legend.title_fontsize': 'x-large',
    'axes.labelsize': 'x-large',
    'axes.titlesize': 'xx-large',
    'xtick.labelsize': 'x-large',
    'ytick.labelsize': 'x-large'
})

# ----------------------------------------------------------------------------------------------------
def plot_att_factor_matrix():

    data = np.loadtxt(f"{RESULTS_DIR}/UF24_att_factor_matrix.dat")

    mask_E = (ENERGY_CENTERS >= 89.72541001) & (ENERGY_CENTERS <= 312.45217139) # EeV

    im = plt.pcolor(ENERGY_CENTERS[mask_E], CTSS, data[:, mask_E], cmap = "ocean_r")
    plt.colorbar(im, label = r'Attenuation factor')

    data = np.loadtxt(f"{RESULTS_DIR}/UF24_horizon.dat")
    plt.plot(data[:,0], data[:,1], c = 'k')

    plt.yscale('log')
    plt.xlim([89.72541001, 312.45217139])
    plt.xlabel(r'$\rm Energy \: [EeV]$')
    plt.ylabel(r'Propagation distance$\: \rm [Mpc]$')
    plt.savefig(f"{FIGURES_DIR}/att_factor_matrix.pdf", bbox_inches = 'tight')
    plt.savefig(f"{FIGURES_DIR}/att_factor_matrix.png", bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_max_distance_comparison():

    LAD_data = np.loadtxt(f"{RESULTS_DIR}/UF24_horizon.dat")
    UF24_data = np.loadtxt(f"{REFERENCES_DIR}/UF24_horizon.dat")

    plt.plot(LAD_data[:,0], LAD_data[:,1], c = 'k', label = 'LAD')
    plt.plot(UF24_data[:,0] * 1e2, UF24_data[:,1], c = 'r', label = 'UF24')
    plt.yscale('log')
    plt.xlim([89.72541001, 312.45217139])
    plt.xlabel(r'$\rm Energy \: [EeV]$')
    plt.ylabel(r'Horizon$\: \rm [Mpc]$')
    plt.legend(title = 'Results')
    plt.savefig(f"{FIGURES_DIR}/max_distance_comparison.pdf", bbox_inches = 'tight')
    plt.savefig(f"{FIGURES_DIR}/max_distance_comparison.png", bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    plot_att_factor_matrix()
    plot_max_distance_comparison()

# ----------------------------------------------------------------------------------------------------