from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'legend.fontsize': 'large',
'legend.title_fontsize': 'large',
'axes.labelsize': 'x-large',
'axes.titlesize': 'xx-large',
'xtick.labelsize': 'x-large',
'ytick.labelsize': 'x-large'})

PARTICLES = ['1H', '14N', '56Fe']
PARTICLES_LEGEND = [r'$^1\mathrm{H}$', r'$^{14}\mathrm{N}$', r'$^{56}\mathrm{Fe}$']
ZSS = [1, 7, 26]
EOBS = [150., 300.]

# ----------------------------------------------------------------------------------------------------
def iZs(Zs):

    for iZs in range(len(ZSS)):
        if Zs == ZSS[iZs]:
            return iZs

# ----------------------------------------------------------------------------------------------------
def plot_GFB23_original(Eobs):

    for Zs in ZSS:
        data = np.loadtxt(f"../data/GFB23_original_{PARTICLES[iZs(Zs)]}_{int(Eobs)}EeV.dat") 
        plt.plot(data[:,0], data[:,1], label = r'{0}'.format(PARTICLES_LEGEND[iZs(Zs)]))

    at = AnchoredText(r'GRB23 | {0}$\: \rm EeV$'.format(int(Eobs)), loc = 'upper right', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)

    plt.xscale('log')
    plt.xlabel(r'Source distance$\: \rm [Mpc]$')
    plt.ylabel(r'$a_{\rm GZK}$')
    plt.legend(frameon = False, loc = 'lower left')
    plt.savefig(f"../figures/GFB23_original_{int(Eobs)}EeV.pdf", bbox_inches = 'tight')
    plt.savefig(f"../figures/GFB23_original_{int(Eobs)}EeV.png", bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_GFB23_comparison(Zs, Eobs):

    data_GFB23 = np.loadtxt(f"../data/GFB23_original_{PARTICLES[iZs(Zs)]}_{int(Eobs)}EeV.dat") 
    data_LAD = np.loadtxt(f"../results/GFB23_definition_aGZK_{PARTICLES[iZs(Zs)]}_{int(Eobs)}EeV.dat")
    plt.plot(data_GFB23[:,0], data_GFB23[:,1], label = 'GFB23', color = 'k')
    plt.fill_between(data_LAD[:,0], data_LAD[:,1], data_LAD[:,2], label = 'LAD', color = 'k', alpha = 0.25)
    
    at = AnchoredText(r'GRB23 | {0} | {1}$\: \rm EeV$'.format(PARTICLES_LEGEND[iZs(Zs)], int(Eobs)), loc = 'upper center', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)

    plt.xscale('log')
    plt.xlim([1.e0, 1.e2])
    plt.xlabel(r'Source distance$\: \rm [Mpc]$')
    plt.ylabel(r'$a_{\rm GZK}$')
    plt.legend(title = 'Results')
    plt.savefig(f"../figures/GFB23_comparison_{PARTICLES[iZs(Zs)]}_{int(Eobs)}EeV.pdf", bbox_inches = 'tight')
    plt.savefig(f"../figures/GFB23_comparison_{PARTICLES[iZs(Zs)]}_{int(Eobs)}EeV.png", bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    # plot_GFB23_original(150.)
    # plot_GFB23_original(300.)

    for Eobs in EOBS:
        for Zs in ZSS:
            plot_GFB23_comparison(Zs, Eobs)

# ----------------------------------------------------------------------------------------------------