from scipy.interpolate import interp1d
import numpy as np

RESULTS_DIR = "../results"
SIMULATIONS_DIR = "../../simulations/results"

CTSS = np.logspace(0, 2.5, num = 201)
ENERGY_EDGES = np.linspace(10**1.5, 10**3, num = 201)
ENERGY_CENTERS = (ENERGY_EDGES[:-1] + ENERGY_EDGES[1:]) / 2
PARTICLES = ['1H', '4He', '14N', '28Si', '56Fe']
ZSS = [1, 2, 7, 14, 26]

# UF24
gmm = 1.
Rcut = 10**18.6 # V 
Zs = 26

# ----------------------------------------------------------------------------------------------------
def iZs(Zs):

    try:
        return ZSS.index(Zs)
    except ValueError:
        raise ValueError(f"Zs ({Zs}) not found in ZSS.")

# ----------------------------------------------------------------------------------------------------
def w_sim(Es): # For the attenuation factor, I don’t need to weight by cts

    return (Es * 1.e18)

# ----------------------------------------------------------------------------------------------------
def w_spec(Es):

    return (Es * 1.e18) ** -gmm * np.exp(-(Es * 1.e18) / (Zs * Rcut))

# ----------------------------------------------------------------------------------------------------
def compute_att_factor_matrix(Zs = 26):

    spec = np.zeros((len(CTSS), len(ENERGY_EDGES)-1))

    for icts in range(len(CTSS)):
        data = np.loadtxt(f"{SIMULATIONS_DIR}/{PARTICLES[iZs(Zs)]}/events_ID{iZs(Zs):02d}D{icts:03d}.txt")
        weights = w_sim(data[:,4]) * w_spec(data[:,4])
        spec[icts] = np.histogram(data[:,2], bins = ENERGY_EDGES, weights = weights)[0]

    data = np.loadtxt(f"{SIMULATIONS_DIR}/{PARTICLES[iZs(Zs)]}/events_ID{iZs(Zs):02d}D0Mpc.txt")
    weights = w_sim(data[:,4]) * w_spec(data[:,4])
    spec_0Mpc = np.histogram(data[:,4], bins = ENERGY_EDGES, weights = weights)[0]
    
    np.savetxt(f"{RESULTS_DIR}/UF24_att_factor_matrix.dat", spec / spec_0Mpc , fmt = "%e", delimiter = "\t")

# ----------------------------------------------------------------------------------------------------
def compute_UF24_horizon(att_factor_cut = 0.1):

    data = np.loadtxt(f"{RESULTS_DIR}/UF24_att_factor_matrix.dat")

    horizon_distance = np.zeros_like(ENERGY_CENTERS)

    for iEs in range(len(ENERGY_CENTERS)):
        for icts in range(len(CTSS)):
            if data[icts, iEs] <= att_factor_cut:
                horizon_distance[iEs] = CTSS[icts]
                break

    np.savetxt(f"{RESULTS_DIR}/UF24_horizon.dat", np.column_stack((ENERGY_CENTERS, horizon_distance)), fmt = "%.15e")

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    compute_att_factor_matrix()    
    compute_UF24_horizon()

# ----------------------------------------------------------------------------------------------------