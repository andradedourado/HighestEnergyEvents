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

RESULTS_DIR = '../results'
PARTICLES = ['1H', '4He', '14N', '28Si', '56Fe']
LEGENDS = [r'$^1\mathrm{H}$', r'$^4\mathrm{He}$', r'$^{14}\mathrm{N}$', r'$^{28}\mathrm{Si}$', r'$^{56}\mathrm{Fe}$']
ZSS = [1, 2, 7, 14, 26]
GMMS = [-1., 0., 1., 2.]

# ----------------------------------------------------------------------------------------------------
def iZs(Zs):

    try:
        return ZSS.index(Zs)
    except ValueError:
        raise ValueError(f"Zs ({Zs}) not found in ZSS.")
    
# ----------------------------------------------------------------------------------------------------
def format_Rcut_label(Rcut):

    if Rcut == 10**18.6:
        return '18p6'
    elif Rcut == np.inf:
        return 'inf'
    else:
        return str(Rcut)
    
# ----------------------------------------------------------------------------------------------------
def EGMF(is_EGMF):

    if is_EGMF == False:
        return 'NoEGMF'
    elif is_EGMF == True:
        return 'EGMF'

# ----------------------------------------------------------------------------------------------------
def plot_UF24_definition_cut_Zs(gmm, Rcut, is_EGMF):

    for Zs in ZSS:
        data = np.loadtxt(f"{RESULTS_DIR}/UF24_definition_cut_{str(gmm).replace('.', 'p')}_{format_Rcut_label(Rcut)}_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.dat")  
        plt.plot(data[:,0], data[:,1], label = f'{LEGENDS[iZs(Zs)]}')

    at = AnchoredText(r'UF24 | $\Gamma = {0}$ | $R_{{\rm cut}} = 10^{{{1}}} \: \rm V$'.format(gmm, np.log10(Rcut)), loc = 'upper center', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)

    plt.yscale('log')
    plt.xlim([100, 300])
    plt.ylim(top = 200)
    plt.xlabel(r'Energy$\: \rm [EeV]$')
    plt.ylabel(r'Source distance$\: \rm [Mpc]$')
    plt.legend(title = 'Nuclei')
    plt.savefig(f"../figures/UF24_definiton_matrix_cut_Zs_{str(gmm).replace('.', 'p')}_{format_Rcut_label(Rcut)}_{EGMF(is_EGMF)}.pdf", format = 'pdf', bbox_inches = 'tight')
    plt.savefig(f"../figures/UF24_definiton_matrix_cut_Zs_{str(gmm).replace('.', 'p')}_{format_Rcut_label(Rcut)}_{EGMF(is_EGMF)}.png", format = 'png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_UF24_definition_cut_gmm(Rcut, Zs, is_EGMF):

    for gmm in GMMS:
        data = np.loadtxt(f"{RESULTS_DIR}/UF24_definition_cut_{str(gmm).replace('.', 'p')}_{format_Rcut_label(Rcut)}_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.dat")  
        plt.plot(data[:,0], data[:,1], label = f'{gmm}')

    if Rcut == np.inf:
        at = AnchoredText(r'UF24 | {0} | $R_{{\rm cut}} = \infty$'.format(LEGENDS[iZs(Zs)]), loc = 'upper center', frameon = False, prop = {'fontsize': 'large'})
    else:
        at = AnchoredText(r'UF24 | {0} | $R_{{\rm cut}} = 10^{{{1}}} \: \rm V$'.format(LEGENDS[iZs(Zs)], np.log10(Rcut)), loc = 'upper center', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)

    plt.yscale('log')
    plt.xlim([100, 300])
    plt.ylim(top = 200)
    plt.xlabel(r'Energy$\: \rm [EeV]$')
    plt.ylabel(r'Source distance$\: \rm [Mpc]$')
    plt.legend(title = 'Spectral index', loc = 'lower left')
    plt.savefig(f"../figures/UF24_definition_cut_gmm_{format_Rcut_label(Rcut)}_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.pdf", bbox_inches = 'tight')
    plt.savefig(f"../figures/UF24_definition_cut_gmm_{format_Rcut_label(Rcut)}_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.png", bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    plot_UF24_definition_cut_Zs(1., 10**18.6, False)
    
    plot_UF24_definition_cut_gmm(10**18.6, 26, False)
    plot_UF24_definition_cut_gmm(np.inf, 26, False)

# ----------------------------------------------------------------------------------------------------
