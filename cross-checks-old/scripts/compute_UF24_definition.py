import numpy as np

RESULTS_DIR = '../results'
CTS = np.logspace(0, 3.5, num = 71)
ES = np.delete(np.logspace(0, 4, num = 81), 0)
E = np.logspace(4./(2.*(len(ES) - 1)), 4. - 4./(2.*(len(ES) - 1)), num = len(ES) - 1)

# ----------------------------------------------------------------------------------------------------
def compute_UF24_definition_matrix():

    matrix = np.loadtxt(f'{RESULTS_DIR}/earth_spectrum_matrix_UF24.dat') / np.loadtxt(f'{RESULTS_DIR}/source_spectrum_matrix_UF24.dat')
    np.savetxt(f'{RESULTS_DIR}/UF24_definition_matrix.dat', matrix, fmt = '%e', header = 'gmm = 1 | Rcut = 10^18.6 V | Zs = 26', delimiter = '\t')

# ----------------------------------------------------------------------------------------------------
def compute_UF24_definition_cut():

    data = np.loadtxt(f'{RESULTS_DIR}/UF24_definition_matrix.dat')

    with open(f'{RESULTS_DIR}/UF24_definition_cut.dat', 'w') as f:
        for iE in range(len(E)):
            for icts in range(len(CTS)):
                if data[icts, iE] < 0.1:
                    break
            f.write(f'{E[iE]:.15e}\t{CTS[icts]:.15e}\n')

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    compute_UF24_definition_matrix()
    compute_UF24_definition_cut()

# ----------------------------------------------------------------------------------------------------