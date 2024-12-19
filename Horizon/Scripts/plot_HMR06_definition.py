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

particles = ['1H', '4He', '14N', '28Si', '56Fe']
particles_legend = [r'$^1\mathrm{H}$', r'$^4\mathrm{He}$', r'$^{14}\mathrm{N}$', r'$^{28}\mathrm{Si}$', r'$^{56}\mathrm{Fe}$']
Zss = [1, 2, 7, 14, 26]

fractions = [0.05, 0.1]

# ----------------------------------------------------------------------------------------------------
def iZs(Zs):

    for iZs in range(len(Zss)):
        if Zs == Zss[iZs]:
            return iZs

# ----------------------------------------------------------------------------------------------------
def EGMF(is_EGMF):

    if is_EGMF == False:
        return 'NoEGMF'
    elif is_EGMF == True:
        return 'EGMF'

# ----------------------------------------------------------------------------------------------------
def get_ls(fraction):

    if fraction == 0.05:
        return '--'
    elif fraction == 0.1:
        return '-'

# ----------------------------------------------------------------------------------------------------
def plot_HMR06_definiton_matrix(Zs, is_EGMF):

    cts = np.logspace(0, 3.5, num = 71)
    E = np.logspace(4./(2.*79), 4. - 4./(2.*79), num = 79) 

    data = np.loadtxt('../Runs/Files/HMR06_definition_matrix_{0}_{1}.dat'.format(particles[iZs(Zs)], EGMF(is_EGMF)))

    im = plt.pcolor(np.log10(E * 1.e18), cts, data, cmap = 'cubehelix_r')  
    plt.colorbar(im, label = r'Fraction $F$')

    at = AnchoredText(r'{0}'.format(particles_legend[iZs(Zs)]), loc = 'upper left', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)
    
    plt.yscale('log')
    plt.ylim([1, 500])
    plt.xlim([np.log10(40 * 1.e18), np.log10(240 * 1.e18)])
    plt.xlabel(r'$\log_{10}({\rm Energy/eV})$')
    plt.ylabel(r'$\text{Propagation distance}{\rm \: [Mpc]}$')
    plt.savefig('../Runs/Plots/HMR06_definiton_matrix_{0}.pdf'.format(particles[iZs(Zs)]), format = 'pdf', bbox_inches = 'tight')
    plt.savefig('../Runs/Plots/HMR06_definiton_matrix_{0}.png'.format(particles[iZs(Zs)]), format = 'png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_HMR06_definition_cut_Zs():

    for Zs in Zss:
        data = np.loadtxt('../Runs/Files/HMR06_definition_cut_{0}_NoEGMF_10.dat'.format(particles[iZs(Zs)]))  
        plt.plot(np.log10(data[:,0] * 1.e18), data[:,1], label = '{}'.format(particles_legend[iZs(Zs)]))
    
    at = AnchoredText(r'No EGMF | $F = 0.1$', loc = 'upper right', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)	

    plt.yscale('log')
    # plt.xlim([np.log10(40 * 1.e18), np.log10(240 * 1.e18)])
    plt.xlabel(r'$\log_{10}({\rm Energy/eV})$')
    plt.ylabel(r'Horizon$\: \rm [Mpc]$')
    plt.legend()
    plt.savefig('../Runs/Plots/HMR06_definition_cut_Zs.pdf', bbox_inches = 'tight')
    plt.savefig('../Runs/Plots/HMR06_definition_cut_Zs.png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
def plot_HMR06_definition_cut_fraction():

    for fraction in fractions:
        data_14N = np.loadtxt('../Runs/Files/HMR06_definition_cut_14N_NoEGMF_{0:02d}.dat'.format(int(fraction * 100)))  
        data_56Fe = np.loadtxt('../Runs/Files/HMR06_definition_cut_56Fe_NoEGMF_{0:02d}.dat'.format(int(fraction * 100)))  
        plt.plot(np.log10(data_14N[:,0] * 1.e18), data_14N[:,1], ls = get_ls(fraction), color = cm.tab10(np.linspace(0, 1, 10)[2]))
        plt.plot(np.log10(data_56Fe[:,0] * 1.e18), data_56Fe[:,1], ls = get_ls(fraction), color = cm.tab10(np.linspace(0, 1, 10)[4]))
    
    at = AnchoredText(r'No EGMF', loc = 'upper left', frameon = False, prop = {'fontsize': 'large'})
    plt.gca().add_artist(at)

    N = lines.Line2D([], [], color = cm.tab10(np.linspace(0, 1, 10)[2]), label = '{}'.format(particles_legend[2]))
    Fe = lines.Line2D([], [], color = cm.tab10(np.linspace(0, 1, 10)[4]), label = '{}'.format(particles_legend[4]))
    lgnd_01 = plt.legend(title = r'$Z_s$', handles = [N, Fe], frameon = True, loc = 'lower left')
    plt.gca().add_artist(lgnd_01)

    F05 = lines.Line2D([], [], color = 'black', ls = '--', label = '0.05')
    F10 = lines.Line2D([], [], color = 'black', ls = '-', label = '0.10')
    lgnd_02 = plt.legend(title = r'Fraction $F$', handles = [F05, F10], frameon = True, loc = 'lower left', bbox_to_anchor = (0.21, 0.))	
    plt.gca().add_artist(lgnd_02)

    plt.yscale('log')
    plt.xlim([np.log10(40 * 1.e18), np.log10(240 * 1.e18)])
    plt.xlabel(r'$\log_{10}({\rm Energy/eV})$')
    plt.ylabel(r'Horizon$\: \rm [Mpc]$')
    plt.savefig('../Runs/Plots/HMR06_definition_cut_fraction.pdf', bbox_inches = 'tight')
    plt.savefig('../Runs/Plots/HMR06_definition_cut_fraction.png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    is_EGMF = False

    # for Zs in Zss:
    #     plot_HMR06_definiton_matrix(Zs, is_EGMF)

    # plot_HMR06_definition_cut_Zs()
    plot_HMR06_definition_cut_fraction()

# ----------------------------------------------------------------------------------------------------