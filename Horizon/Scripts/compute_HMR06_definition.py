import numpy as np
import sys

cts = np.logspace(0, 3.5, num = 71)
Es = np.logspace(0, 4, num = 81)
Es = np.delete(Es, 0)	
E = np.logspace(4./(2.*79), 4. - 4./(2.*79), num = 79) 

particles = ['1H', '4He', '14N', '28Si', '56Fe']
Zss = [1, 2, 7, 14, 26]

gmm = 1.
Rmax = 10**18.6 # V

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
def compute_HMR06_definition_matrix(Zs, is_EGMF):

    data = np.loadtxt('../results/intensity_matrix_{0}_{1}.dat'.format(particles[iZs(Zs)], EGMF(is_EGMF)))

    matrix = np.zeros((len(cts), 79))

    for iE in range(len(E)):
        for icts in range(len(cts)):
            matrix[icts, iE] = np.sum(data[icts:, iE:])

    matrix[0, matrix[0,:] == 0] = sys.float_info.min
    matrix = matrix / matrix[0,:]
    
    np.savetxt('../results/HMR06_definition_matrix_{0}_{1}.dat'.format(particles[iZs(Zs)], EGMF(is_EGMF)), matrix, fmt = '%e', header = 'gmm = {0} | Rmax = 10^{{{1}}} V | Zs = {2}'.format(gmm, np.log10(Rmax), Zs), delimiter = '\t')

# ----------------------------------------------------------------------------------------------------
def compute_HMR06_definition_cut(Zs, is_EGMF, fraction):

    data = np.loadtxt('../results/HMR06_definition_matrix_{0}_{1}.dat'.format(particles[iZs(Zs)], EGMF(is_EGMF)))

    f = open('../results/HMR06_definition_cut_{0}_{1}_{2:02d}.dat'.format(particles[iZs(Zs)], EGMF(is_EGMF), int(fraction * 100)), 'w')

    for iE in range(79):
        for icts in range(len(cts)):
            if data[icts,iE] < fraction:
                break 
        f.write(str('{:.15e}'.format(E[iE])) + '\t')
        f.write(str('{:.15e}'.format(cts[icts])) + '\n')

    f.close()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    is_EGMF = False

    for Zs in Zss:
        compute_HMR06_definition_matrix(Zs, is_EGMF)
        for fraction in fractions:
            compute_HMR06_definition_cut(Zs, is_EGMF, fraction)

# ----------------------------------------------------------------------------------------------------