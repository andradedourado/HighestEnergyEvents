from matplotlib import lines
from matplotlib.offsetbox import AnchoredText
from matplotlib.pylab import cm
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'legend.fontsize': 'large',
'legend.title_fontsize': 'large',
'axes.labelsize': 'x-large',
'axes.titlesize': 'xx-large',
'xtick.labelsize': 'x-large',
'ytick.labelsize': 'x-large'})

particles = ['1H'] #, '4He', '14N', '28Si', '56Fe']
particles_legend = [r'$^1\mathrm{H}$'] #, r'$^4\mathrm{He}$', r'$^{14}\mathrm{N}$', r'$^{28}\mathrm{Si}$', r'$^{56}\mathrm{Fe}$']
Zss = [1]#, 2, 7, 14, 26]

fractions = [0.1, 0.3, 0.5, 0.7]
gmms = [2.2, 2.7]

# ----------------------------------------------------------------------------------------------------
def iZs(Zs):

    for iZs in range(len(Zss)):
        if Zs == Zss[iZs]:
            return iZs
        
# ----------------------------------------------------------------------------------------------------
def gmm_filename_suffix(gmm):
     
    if gmm == 2.2:
        return 'thick'
    elif gmm == 2.7:
        return 'thin'

# ----------------------------------------------------------------------------------------------------
def get_color(fraction):

    if fraction == 0.1:
        return cm.Reds(np.linspace(0, 1, 10)[3])
    elif fraction == 0.3:
        return cm.Reds(np.linspace(0, 1, 10)[5])
    elif fraction == 0.5:
        return cm.Reds(np.linspace(0, 1, 10)[7])
    elif fraction == 0.7:
        return cm.Reds(np.linspace(0, 1, 10)[9])

# ----------------------------------------------------------------------------------------------------
def plot_HMR06_original_1H():

    for gmm in gmms:
        for fraction in fractions:
            data = np.loadtxt('../data/HMR06_original_1H_{0}_{1}.dat'.format(gmm_filename_suffix(gmm), int(fraction * 100))) 
            if gmm == 2.2:
                plt.plot(data[:,0], data[:,1], color = get_color(fraction), ls = '-', label = r'${0}$'.format(fraction))
            elif gmm == 2.7:
                plt.plot(data[:,0], data[:,1], color = get_color(fraction), ls = '--')

    at = AnchoredText(r'HMR06 | {0}'.format(particles_legend[0]), loc = 'upper center', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)

    thick = lines.Line2D([], [], color = 'k', ls = '-', label = r'$2.2$')
    thin = lines.Line2D([], [], color = 'k', ls = '--', label = r'$2.7$')
    lgnd_01 = plt.legend(title = r'Spectral index', handles = [thick, thin], frameon = True, loc = 'upper right')
    plt.gca().add_artist(lgnd_01)

    plt.xlabel(r'Energy$\: \rm [EeV]$')
    plt.ylabel(r'Distance$\: \rm [Mpc]$')
    plt.legend(title = r'Fraction $F$', bbox_to_anchor = (1., 0.763))
    plt.savefig('../figures/HMR06_original_1H.pdf', bbox_inches = 'tight')
    plt.savefig('../figures/HMR06_original_1H.png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_HMR06_comparison_1H(gmm):

    for fraction in fractions:
        data_HMR06 = np.loadtxt('../data/HMR06_original_1H_{0}_{1}.dat'.format(gmm_filename_suffix(gmm), int(fraction * 100)))
        data_LAD = np.loadtxt('../results/HMR06_definition_cut_1H_{0}_{1}.dat'.format(gmm_filename_suffix(gmm), int(fraction * 100))) 
        plt.plot(data_HMR06[:,0], data_HMR06[:,1], color = get_color(fraction), ls = '-', label = r'${0}$'.format(fraction))
        plt.plot(data_LAD[:,0], data_LAD[:,1], color = get_color(fraction), ls = '--')

    at = AnchoredText(r'HMR06 | {0} | $\Gamma = {1}$'.format(particles_legend[0], gmm), loc = 'upper center', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)

    HMR06 = lines.Line2D([], [], color = 'k', ls = '-', label = r'HMR06')
    LAD = lines.Line2D([], [], color = 'k', ls = '--', label = r'LAD')
    lgnd_01 = plt.legend(title = r'Results', handles = [HMR06, LAD], frameon = True, loc = 'upper right')
    plt.gca().add_artist(lgnd_01)

    plt.xlim([50, 150])
    plt.ylim([0, 200])
    plt.xlabel(r'Energy$\: \rm [EeV]$')
    plt.ylabel(r'Distance$\: \rm [Mpc]$')
    plt.legend(title = r'Fraction $F$', bbox_to_anchor = (1., 0.763))
    plt.savefig('../figures/HMR06_comparison_1H_{0}.pdf'.format(gmm_filename_suffix(gmm)), bbox_inches = 'tight')
    plt.savefig('../figures/HMR06_comparison_1H_{0}.png'.format(gmm_filename_suffix(gmm)), bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    # plot_HMR06_original_1H()
    for gmm in gmms:
        plot_HMR06_comparison_1H(gmm)

# ----------------------------------------------------------------------------------------------------