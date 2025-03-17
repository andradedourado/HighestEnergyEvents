import numpy as np

RESULTS_DIR = '../results'
PARTICLES = ['1H', '4He', '14N', '28Si', '56Fe']
ZSS = [1, 2, 7, 14, 26]
GMMS = [-2., -1., 0., 1., 2.]
CTS = np.logspace(0, 3.5, num = 71)
ES = np.delete(np.logspace(0, 4, num = 81), 0)
E = np.logspace(4./(2.*(len(ES) - 1)), 4. - 4./(2.*(len(ES) - 1)), num = len(ES) - 1)

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
def compute_UF24_definition_matrix(gmm, Rcut, Zs, is_EGMF):

    earth_file = f"{RESULTS_DIR}/earth_spectrum_matrix_{str(gmm).replace('.', 'p')}_{format_Rcut_label(Rcut)}_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.dat"
    source_file = f"{RESULTS_DIR}/source_spectrum_matrix_{str(gmm).replace('.', 'p')}_{format_Rcut_label(Rcut)}_{PARTICLES[iZs(Zs)]}.dat"
    matrix = np.loadtxt(earth_file) / np.loadtxt(source_file)    
    np.savetxt(f"{RESULTS_DIR}/UF24_definition_matrix_{str(gmm).replace('.', 'p')}_{format_Rcut_label(Rcut)}_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.dat", matrix, fmt = '%e', delimiter = '\t')

# ----------------------------------------------------------------------------------------------------
def compute_UF24_definition_cut(gmm, Rcut, Zs, is_EGMF):

    data = np.loadtxt(f"{RESULTS_DIR}/UF24_definition_matrix_{str(gmm).replace('.', 'p')}_{format_Rcut_label(Rcut)}_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.dat")

    with open(f"{RESULTS_DIR}/UF24_definition_cut_{str(gmm).replace('.', 'p')}_{format_Rcut_label(Rcut)}_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.dat", 'w') as f:
        for iE in range(len(E)):
            for icts in range(len(CTS)):
                if data[icts, iE] < 0.1:
                    break
            f.write(f'{E[iE]:.15e}\t{CTS[icts]:.15e}\n')

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    # for Zs in ZSS:
    #     compute_UF24_definition_matrix(1., 10**18.6, Zs, False)
    #     compute_UF24_definition_cut(1., 10**18.6, Zs, False)

    for gmm in GMMS:
        compute_UF24_definition_matrix(gmm, 10**18.6, 26, False)
        compute_UF24_definition_cut(gmm, 10**18.6, 26, False)

# ----------------------------------------------------------------------------------------------------