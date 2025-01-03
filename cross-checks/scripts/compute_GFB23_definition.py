import numpy as np

RESULTS_DIR = '../results'
PARTICLES = ['1H', '14N', '56Fe']
ZSS = [1, 7, 26]
EOBS = [150., 300.]
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

    earth_spectrum = np.loadtxt(f"{RESULTS_DIR}/earth_spectrum_matrix_{PARTICLES[iZs(Zs)]}_3ZeV.dat")
    source_spectrum = np.loadtxt(f"{RESULTS_DIR}/source_spectrum_matrix_{PARTICLES[iZs(Zs)]}_3ZeV.dat")

    matrix_num = np.zeros((len(CTS), len(ES) - 1))
    matrix_den = np.zeros((len(CTS), len(ES) - 1))

    for icts in range(len(CTS)):
        for iE in range(len(E)):
            for iiE in range(iE, len(E)):
                matrix_num[icts, iE] += earth_spectrum[icts, iiE]
                matrix_den[icts, iE] += source_spectrum[icts, iiE]

    matrix = matrix_num / matrix_den
    
    filename = f"{RESULTS_DIR}/GFB23_definition_matrix_{PARTICLES[iZs(Zs)]}.dat"
    header = f"gmm = 2.5 | Rcut = 3.e21 / {Zs} V | Zs = {Zs}"
    np.savetxt(filename, matrix, fmt = '%e', header = header, delimiter = '\t')
    
# ----------------------------------------------------------------------------------------------------
def compute_GFB23_definiton_aGZK(Zs, Eobs):

    data = np.loadtxt(f"{RESULTS_DIR}/GFB23_definition_matrix_{PARTICLES[iZs(Zs)]}.dat")

    for iE in range(len(E)):
        if Eobs >= E[iE] and Eobs < E[iE + 1]:
            break

    f = open(f"{RESULTS_DIR}/GFB23_definition_aGZK_{PARTICLES[iZs(Zs)]}_{int(Eobs)}EeV.dat", 'w')
    f.write(f'# [{round(E[iE])}, {round(E[iE + 1])}] EeV\n')    
    for icts, cts in enumerate(CTS):
        f.write(f'{cts:.15e}\t{data[icts, iE]:.15e}\t{data[icts, iE + 1]:.15e}\n')
    f.close()
    
# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    for Zs in ZSS:
        compute_GFB23_definition_matrix(Zs)
    
    for Zs in ZSS:
        for Eobs in EOBS:
            compute_GFB23_definiton_aGZK(Zs, Eobs)

# ----------------------------------------------------------------------------------------------------