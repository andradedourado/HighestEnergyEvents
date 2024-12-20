import numpy as np
import sys

cts = np.logspace(0, 3.5, num = 71)
Es = np.logspace(0, 4, num = 81)
Es = np.delete(Es, 0)	
E = np.logspace(4./(2.*79), 4. - 4./(2.*79), num = 79) 

particles = ['1H']
Zss = [1]

gmms = [2.2, 2.7]

fractions = [0.1, 0.3, 0.5, 0.7]

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
def compute_HMR06_definition_matrix(gmm, Zs):

    data = np.loadtxt('../results/intensity_matrix_{0}_{1}.dat'.format(particles[iZs(Zs)], gmm_filename_suffix(gmm)))

    matrix = np.zeros((len(cts), 79))

    for iE in range(len(E)):
        for icts in range(len(cts)):
            matrix[icts, iE] = np.sum(data[icts:, iE:])

    matrix[0, matrix[0,:] == 0] = sys.float_info.min
    matrix = matrix / matrix[0,:]
    
    np.savetxt('../results/HMR06_definition_matrix_{0}_{1}.dat'.format(particles[iZs(Zs)], gmm_filename_suffix(gmm)), matrix, fmt = '%e', header = 'gmm = {0} | Zs = {1}'.format(gmm, Zs), delimiter = '\t')

# ----------------------------------------------------------------------------------------------------
def compute_HMR06_definition_cut(gmm, Zs, fraction):

    data = np.loadtxt('../results/HMR06_definition_matrix_{0}_{1}.dat'.format(particles[iZs(Zs)], gmm_filename_suffix(gmm)))

    f = open('../results/HMR06_definition_cut_{0}_{1}_{2:02d}.dat'.format(particles[iZs(Zs)], gmm_filename_suffix(gmm), int(fraction * 100)), 'w')

    for iE in range(79):
        for icts in range(len(cts)):
            if data[icts,iE] < fraction:
                break 
        f.write(str('{:.15e}'.format(E[iE])) + '\t')
        f.write(str('{:.15e}'.format(cts[icts])) + '\n')

    f.close()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    for gmm in gmms:
        for Zs in Zss:
            compute_HMR06_definition_matrix(gmm, Zs)
            for fraction in fractions:
                compute_HMR06_definition_cut(gmm, Zs, fraction)

# ----------------------------------------------------------------------------------------------------