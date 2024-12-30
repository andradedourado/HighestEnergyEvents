import numpy as np

RESULTS_DIR = '../results'
PARTICLES = ['1H', '14N', '56Fe']
ZSS = [1, 14, 56]
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
def compute_GFB23_definition_matrix(Zs):

    data_earth = np.loadtxt(f"{RESULTS_DIR}/earth_spectrum_matrix_{PARTICLES[iZs(Zs)]}_3ZeV.dat")
    data_source = np.loadtxt(f"{RESULTS_DIR}/source_spectrum_matrix_{PARTICLES[iZs(Zs)]}_3ZeV.dat")

    matrix_num = np.zeros((len(CTS), len(ES) - 1))
    matrix_den = np.zeros((len(CTS), len(ES) - 1))

    for icts in range(len(CTS)):
        for iE in range(len(E)):
            for iiE in range(iE, len(E)):
                matrix_num[icts, iE] += data_earth[icts, iiE]
                matrix_den[icts, iE] += data_source[icts, iiE]

    matrix = matrix_num / matrix_den
    
    filename = f"{RESULTS_DIR}/GFB23_definition_matrix_{PARTICLES[iZs(Zs)]}_3ZeV.dat"
    header = f"gmm = 2.5 | Rcut = 3.e21 / {Zs} V | Zs = {Zs}"
    np.savetxt(filename, matrix, fmt = '%e', header = header, delimiter = '\t')
    
# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    for Zs in ZSS:
        compute_GFB23_definition_matrix(Zs)

# ----------------------------------------------------------------------------------------------------