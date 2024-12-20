import numpy as np

cts = np.logspace(0, 3.5, num = 71)
Es = np.logspace(0, 4, num = 81)
Es = np.delete(Es, 0)

particles = ['1H', '4He', '14N', '28Si', '56Fe']
Zss = [1, 2, 7, 14, 26]

dir = '/Users/andradedourado/Simulations/Runs/Analysis'

# ----------------------------------------------------------------------------------------------------
def w_sim(Es, cts): 

	Es = Es * 1.e18
	w = Es * cts

	return w

# ----------------------------------------------------------------------------------------------------
def w_spec(Es, Zs, gmm, Rmax):
        
	Es = Es*1.e18
	w = Es**(-gmm) * np.exp(-Es/(Zs*Rmax))
	
	return w

# ----------------------------------------------------------------------------------------------------
def iZs(Zs):

    for iZs in range(len(Zss)):
        if Zs == Zss[iZs]:
            return iZs
            
# ----------------------------------------------------------------------------------------------------
def EGMF(is_EGMF):

    if is_EGMF == False:
        return 'NoEGMF'
    elif is_EGMF == True:
        return 'EGMF'

# ----------------------------------------------------------------------------------------------------
def compute_intensity_matrix(gmm, Rmax, Zs, is_EGMF):

    matrix = np.zeros((len(cts), 79))

    if is_EGMF == False:

        for icts in range(len(cts)):

            for iEs in range(len(Es)):

                data = np.loadtxt(dir + '/{0}/S_ID{1:02d}D{2:02d}E0{3:02d}.dat'.format(particles[iZs(Zs)], iZs(Zs), icts, iEs))
                
                for idata in range(len(data)):
                    matrix[icts, idata] += data[idata] * w_spec(Es[iEs], Zs, gmm, Rmax) * w_sim(Es[iEs], cts[icts])

    # elif is_EGMF == True:

    np.savetxt('../results/intensity_matrix_{0}_{1}.dat'.format(particles[iZs(Zs)], EGMF(is_EGMF)), matrix, fmt = '%e', header = 'gmm = {0} | Rmax = 10^{{{1}}} V | Zs = {2}'.format(gmm, np.log10(Rmax), Zs), delimiter = '\t')

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    gmm = 1.
    Rmax = 10**18.6 # V

    is_EGMF = False

    for Zs in Zss:
        compute_intensity_matrix(gmm, Rmax, Zs, is_EGMF)

# ----------------------------------------------------------------------------------------------------
