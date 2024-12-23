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
if __name__ == '__main__':

    plot_UF24_original()

# ----------------------------------------------------------------------------------------------------