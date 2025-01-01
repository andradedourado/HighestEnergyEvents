import numpy as np

BASE_DIR = '/Users/andradedourado/Simulations/Runs/Analysis'
RESULTS_DIR = '../results'
PARTICLES = ['1H', '4He', '14N', '28Si', '56Fe']
ZSS = [1, 2, 7, 14, 26]
CTS = np.logspace(0, 3.5, num = 71)
ES = np.delete(np.logspace(0, 4, num = 81), 0)

# ----------------------------------------------------------------------------------------------------
def w_sim(Es, cts): 

    return Es * 1.e18 * cts

# ----------------------------------------------------------------------------------------------------
def w_spec(Es, Zs, gmm, Rcut):

    return (Es * 1.e18) ** -gmm * np.exp(-(Es * 1.e18) / (Zs * Rcut))

# ----------------------------------------------------------------------------------------------------
def iZs(Zs):

    try:
        return ZSS.index(Zs)
    except ValueError:
        raise ValueError(f"Zs ({Zs}) not found in ZSS.")
            
# ----------------------------------------------------------------------------------------------------
def EGMF(is_EGMF):

    if is_EGMF == False:
        return 'NoEGMF'
    elif is_EGMF == True:
        return 'EGMF'

# ----------------------------------------------------------------------------------------------------
def save_spectrum_file(matrix, Zs, location, is_EGMF):

    if location == 'source':
        filename = f"{RESULTS_DIR}/{location}_spectrum_matrix_{PARTICLES[iZs(Zs)]}.dat"
    elif location == 'earth':
        filename = f"{RESULTS_DIR}/{location}_spectrum_matrix_{PARTICLES[iZs(Zs)]}_{EGMF(is_EGMF)}.dat"

    np.savetxt(filename, matrix, fmt = '%e', delimiter = '\t')

# ----------------------------------------------------------------------------------------------------
def compute_matrix(gmm, Rcut, Zs, location, is_EGMF, num_particles = 1000):

    matrix = np.zeros((len(CTS), len(ES) - 1))

    for icts, cts in enumerate(CTS):
        for iEs, Es in enumerate(ES[:-1]):
            weight = w_spec(Es, Zs, gmm, Rcut) * w_sim(Es, cts)

            if location == 'earth':
                data = np.loadtxt(f"{BASE_DIR}/{PARTICLES[iZs(Zs)]}/S_ID{iZs(Zs):02d}D{icts:02d}E0{iEs:02d}.dat")
                if is_EGMF == False:
                    matrix[icts] += data * weight
                # elif is_EGMF == True:
            elif location == 'source':
                matrix[icts, iEs] += num_particles * weight

    save_spectrum_file(matrix, Zs, location, is_EGMF)

# ----------------------------------------------------------------------------------------------------  
if __name__ == '__main__':

    for Zs in ZSS:
        compute_matrix(1., 10**18.6, Zs, 'earth', False)
        compute_matrix(1., 10**18.6, Zs, 'source', False)

# ----------------------------------------------------------------------------------------------------