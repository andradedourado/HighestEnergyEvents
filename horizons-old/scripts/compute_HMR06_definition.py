import numpy as np
import sys

RESULTS_DIR = '../results'
PARTICLES = ['1H', '4He', '14N', '28Si', '56Fe']
ZSS = [1, 2, 7, 14, 26]
FRACTIONS = [0.05, 0.1]
CTS = np.logspace(0, 3.5, num = 71)
ES = np.delete(np.logspace(0, 4, num = 81), 0)
E = np.logspace(4./(2.*(len(ES) - 1)), 4. - 4./(2.*(len(ES) - 1)), num = len(ES) - 1)
GMM = 1.
RCUT = 10**18.6 # V

# ----------------------------------------------------------------------------------------------------
def iZs(Zs):

    for iZs in range(len(ZSS)):
        if Zs == ZSS[iZs]:
            return iZs
        
# ----------------------------------------------------------------------------------------------------
def EGMF(is_EGMF):

    if is_EGMF == False:
        return 'NoEGMF'
    elif is_EGMF == True:
        return 'EGMF'

# ----------------------------------------------------------------------------------------------------
def compute_HMR06_definition_matrix(Zs, is_EGMF):

    data = np.loadtxt(f"{RESULTS_DIR}/earth_spectrum_matrix_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.dat")

    matrix = np.zeros((len(CTS), len(ES) - 1))

    for iE in range(len(E)):
        for icts in range(len(CTS)):
            matrix[icts, iE] = np.sum(data[icts:, iE:])

    matrix[0, matrix[0,:] == 0] = sys.float_info.min
    matrix = matrix / matrix[0,:]
    
    np.savetxt(f"{RESULTS_DIR}/HMR06_definition_matrix_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.dat", matrix, fmt = '%e', header = 'gmm = {0} | Rcut = 10^{{{1}}} V | Zs = {2}'.format(GMM, np.log10(RCUT), Zs), delimiter = '\t')

# ----------------------------------------------------------------------------------------------------
def compute_HMR06_definition_cut(Zs, is_EGMF, fraction):

    data = np.loadtxt(f"{RESULTS_DIR}/HMR06_definition_matrix_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.dat")

    f = open(f"{RESULTS_DIR}/HMR06_definition_cut_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}_{int(fraction * 100):02d}.dat", 'w')

    for iE in range(len(ES) - 1):
        for icts in range(len(CTS)):
            if data[icts,iE] < fraction:
                break 
        f.write(str('{:.15e}'.format(E[iE])) + '\t')
        f.write(str('{:.15e}'.format(CTS[icts])) + '\n')

    f.close()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    for Zs in ZSS:
        compute_HMR06_definition_matrix(Zs, False)
        for fraction in FRACTIONS:
            compute_HMR06_definition_cut(Zs, False, fraction)

# ----------------------------------------------------------------------------------------------------