# from matplotlib import lines
# from matplotlib.offsetbox import AnchoredText
# from matplotlib.pylab import cm
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'legend.fontsize': 'large',
'legend.title_fontsize': 'large',
'axes.labelsize': 'x-large',
'axes.titlesize': 'xx-large',
'xtick.labelsize': 'x-large',
'ytick.labelsize': 'x-large'})

# ----------------------------------------------------------------------------------------------------
def plot_UF24_original():

    data = np.loadtxt('../data/UF24_original.dat')
    plt.plot(data[:,0], data[:,1], color = 'k') 
    plt.yscale('log')
    plt.xlabel(r'Energy$\: \rm [EeV]$')
    plt.ylabel(r'Distance$\: \rm [Mpc]$')
    plt.savefig('../figures/UF24_original.pdf', bbox_inches = 'tight')
    plt.savefig('../figures/UF24_original.png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_UF24_comparison():

    data_UF24 = np.loadtxt('../data/UF24_original.dat')
    data_LAD = np.loadtxt('../results/UF24_definition_cut.dat')
    plt.plot(data_UF24[:,0]*100, data_UF24[:,1], color = 'k', label = 'UF24') 
    plt.plot(data_LAD[:,0], data_LAD[:,1], color = 'r', label = 'LAD')
    plt.yscale('log')
    plt.xlim([100, 300])
    plt.ylim([0, 200])
    plt.xlabel(r'Energy$\: \rm [EeV]$')
    plt.ylabel(r'Distance$\: \rm [Mpc]$')
    plt.legend(title = r'Results')
    plt.savefig('../figures/UF24_comparison.pdf', bbox_inches = 'tight')
    plt.savefig('../figures/UF24_comparison.png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    # plot_UF24_original()
    plot_UF24_comparison()

# ----------------------------------------------------------------------------------------------------