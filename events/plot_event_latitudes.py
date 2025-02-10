from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'legend.fontsize': 'medium',
'legend.title_fontsize': 'medium',
'axes.labelsize': 'large',
'axes.titlesize': 'x-large',
'xtick.labelsize': 'large',
'ytick.labelsize': 'large'})

data = np.genfromtxt('highest_energy_events.dat', dtype = None)

# ----------------------------------------------------------------------------------------------------
def ra_dec_to_gal_lat(idata):
     
    c_equatorial = SkyCoord(ra = data[idata][4] * u.degree, dec = data[idata][5] * u.degree, frame = 'icrs', unit = 'deg')
    c_galactic = c_equatorial.galactic
			
    return c_galactic.b.degree

# ----------------------------------------------------------------------------------------------------
def plot_event_latitudes():

    gal_lat = np.zeros(len(data))
    E = np.zeros(len(data))

    for idata in range(len(data)):
        gal_lat[idata] = ra_dec_to_gal_lat(idata)
        E[idata] = data[idata][1]
        
    plt.figure()
    plt.scatter(E, abs(gal_lat), marker = '^',  color = 'r')
    plt.axhline(y = 30, color = 'gray', linestyle = ':')
    plt.xlim(left = 100)
    plt.xlabel(r'Energy$\: \rm [EeV]$')
    plt.ylabel(r'$|b| \: {\rm [deg]}$')
    plt.savefig('event_latitudes.pdf', format = 'pdf', bbox_inches = 'tight')
    plt.savefig('event_latitudes.png', format = 'png', bbox_inches = 'tight', dpi = 300)
    plt.show()

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    plot_event_latitudes()

# ----------------------------------------------------------------------------------------------------