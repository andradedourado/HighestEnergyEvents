from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'legend.fontsize': 'large',
'legend.title_fontsize': 'large',
'axes.labelsize': 'x-large',
'axes.titlesize': 'xx-large',
'xtick.labelsize': 'x-large',
'ytick.labelsize': 'x-large'})

ZS = [1, 2, 7, 14, 26]

# ----------------------------------------------------------------------------------------------------
def larmor_radius(E, Z, B):

    return 1.081 / Z * E / B # Mpc 

# ----------------------------------------------------------------------------------------------------
def plot_larmor_radius():

    E = np.logspace(0, 3, num = 100)

    at = AnchoredText(r'$B = 1 \: \rm nG$', loc = 'upper center', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)
    
    plt.axvline(x = 166e18, color = 'black', linestyle = '--')
    plt.axvline(x = 244e18, color = 'black', linestyle = '--')

    plt.text(166e18, 2.e3, 'PAO191110', color = 'black', horizontalalignment = 'right', fontsize = 'medium')
    plt.text(244e18, 2.e3, 'Amaterasu', color = 'black', horizontalalignment = 'left', fontsize = 'medium')

    for Z in ZS:
        plt.plot(E * 1.e18, larmor_radius(E, Z, B = 1.), label = f'${Z}$')

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel(r'Energy$\: \rm [eV]$')
    plt.ylabel(r'Larmor radius$\: \rm [Mpc]$')
    plt.legend(title = r'$Z$')
    plt.grid(linestyle = ':', color = 'gray', linewidth = 0.25, zorder = -1.0)
    plt.savefig(f"larmor_radius.pdf", bbox_inches = 'tight')
    plt.savefig(f"larmor_radius.png", bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    plot_larmor_radius()

# ----------------------------------------------------------------------------------------------------

