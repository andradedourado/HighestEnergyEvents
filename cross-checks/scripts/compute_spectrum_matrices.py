import numpy as np

BASE_DIR = '/Users/andradedourado/Simulations/Runs/Analysis'
RESULTS_DIR = '../results'
PARTICLES = ['1H', '4He', '14N', '28Si', '56Fe']
ZSS = [1, 2, 7, 14, 26]
GMMS = [2.2, 2.7]
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
def gmm_filename_suffix(gmm):
     
    if gmm == 2.2:
        return 'thick'
    elif gmm == 2.7:
        return 'thin'

# ----------------------------------------------------------------------------------------------------
def save_spectrum_file(matrix, gmm, Zs, horizon, location):

    filename = f"{RESULTS_DIR}/{location}_spectrum_matrix_{horizon}.dat" \
               if horizon == 'UF24' else \
               f"{RESULTS_DIR}/{location}_spectrum_matrix_{PARTICLES[iZs(Zs)]}_{gmm_filename_suffix(gmm)}.dat"

    header = f"gmm = {gmm} | Rcut = {'∞' if horizon == 'HMR06' else '10^18.6 V'} | Zs = {Zs}"
    
    np.savetxt(filename, matrix, fmt = '%e', header = header, delimiter = '\t')

# ----------------------------------------------------------------------------------------------------
def compute_matrix(gmm, Rcut, Zs, horizon, location, num_particles = 1000):

    matrix = np.zeros((len(CTS), len(ES) - 1))

    for icts, cts in enumerate(CTS):
        for iEs, Es in enumerate(ES[:-1]):
            weight = w_spec(Es, Zs, gmm, Rcut) * w_sim(Es, cts)

            if location == 'earth':
                data = np.loadtxt(f"{BASE_DIR}/{PARTICLES[iZs(Zs)]}/S_ID{iZs(Zs):02d}D{icts:02d}E0{iEs:02d}.dat")
                matrix[icts] += data * weight
            elif location == 'source':
                matrix[icts, iEs] += num_particles * weight

    save_spectrum_file(matrix, gmm, Zs, horizon, location)

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    # HMR06
    # for gmm in GMMS:
    #     for Zs in ZSS:
    #         if Zs not in [2, 7]:
    #             compute_matrix(gmm, np.inf, Zs, 'HMR06', 'earth')
    #             compute_matrix(gmm, np.inf, Zs, 'HMR06', 'source')

    # UF24
    compute_matrix(1.0, 10**18.6, 26, 'UF24', 'earth')
    compute_matrix(1.0, 10**18.6, 26, 'UF24', 'source')

# ----------------------------------------------------------------------------------------------------