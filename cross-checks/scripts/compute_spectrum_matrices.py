import numpy as np

cts = np.logspace(0, 3.5, num = 71)
Es = np.logspace(0, 4, num = 81)
Es = np.delete(Es, 0)

particles = ['1H', '4He', '14N', '28Si', '56Fe']
Zss = [1, 2, 7, 14, 26]

gmms = [2.2, 2.7]

dir = '/Users/andradedourado/Simulations/Runs/Analysis'

# ----------------------------------------------------------------------------------------------------
def w_sim(Es, cts): 

	Es = Es * 1.e18
	w = Es * cts

	return w

# ----------------------------------------------------------------------------------------------------
def w_spec(Es, Zs, gmm): # No exponential cutoff

	Es = Es*1.e18
	w = Es**(-gmm) 
	
	return w

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
def compute_earth_spectrum_matrix(gmm, Zs):

    matrix = np.zeros((len(cts), 79))

    for icts in range(len(cts)):

        for iEs in range(len(Es)):

            data = np.loadtxt(dir + '/{0}/S_ID{1:02d}D{2:02d}E0{3:02d}.dat'.format(particles[iZs(Zs)], iZs(Zs), icts, iEs))
                
            for idata in range(len(data)):
                matrix[icts, idata] += data[idata] * w_spec(Es[iEs], Zs, gmm) * w_sim(Es[iEs], cts[icts])

    np.savetxt('../results/earth_spectrum_matrix_{0}_{1}.dat'.format(particles[iZs(Zs)], gmm_filename_suffix(gmm)), matrix, fmt = '%e', header = 'gmm = {0} | Rmax = \infty V | Zs = {1}'.format(gmm, Zs), delimiter = '\t')

# ----------------------------------------------------------------------------------------------------
def compute_source_spectrum_matrix(gmm, Zs):

    num_particles = 1000

    matrix = np.zeros((len(cts), 79))

    for icts in range(len(cts)):

        for iEs in range(len(Es)-1):
            
            matrix[icts, iEs] += num_particles * w_spec(Es[iEs], Zs, gmm) * w_sim(Es[iEs], cts[icts])

    np.savetxt('../results/source_spectrum_matrix_{0}_{1}.dat'.format(particles[iZs(Zs)], gmm_filename_suffix(gmm)), matrix, fmt = '%e', header = 'gmm = {0} | Rmax = \infty V | Zs = {1}'.format(gmm, Zs), delimiter = '\t')

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    for gmm in gmms: 
        for Zs in Zss:
            if Zs not in [2, 7]:
                compute_earth_spectrum_matrix(gmm, Zs)
                compute_source_spectrum_matrix(gmm, Zs)

# ----------------------------------------------------------------------------------------------------