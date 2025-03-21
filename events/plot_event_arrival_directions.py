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
degree = np.pi / 180.

# ----------------------------------------------------------------------------------------------------
def countours_auger_sky():
	
    nbins = int(1.e2)
	
    dec = np.full(nbins, 45) 
    ra = np.linspace(0, 360, num = nbins) 

    countours = np.zeros((nbins, 2))
    
    for icoord in range(nbins):

        c_equatorial = SkyCoord(ra = ra[icoord] * u.degree, dec = dec[icoord] * u.degree, frame = 'icrs')
        c_galactic = c_equatorial.galactic
		
        l = c_galactic.l.radian
        b = c_galactic.b.radian
		
        # Python coordinates
        if 2*np.pi >= l >= np.pi:
            l = 2*np.pi - l
        elif 0 <= l <= np.pi:
            l = -l
        
        countours[icoord, 0] = b
        countours[icoord, 1] = l

    return countours

# ----------------------------------------------------------------------------------------------------
def ra_dec_to_gal_lat(idata):
     
    c_equatorial = SkyCoord(ra = data[idata][4] * u.degree, dec = data[idata][5] * u.degree, frame = 'icrs', unit = 'deg')
    c_galactic = c_equatorial.galactic
			
    return c_galactic.b.radian

# ----------------------------------------------------------------------------------------------------
def ra_dec_to_gal_lon(idata):

    c_equatorial = SkyCoord(ra = data[idata][4] * u.degree, dec = data[idata][5] * u.degree, frame = 'icrs', unit = 'deg')
    c_galactic = c_equatorial.galactic
			
    l = c_galactic.l.radian			
			
    if 2*np.pi >= l >= np.pi:			
        return 2*np.pi - l
    elif 0 <= l <= np.pi:
	    return -l

# ----------------------------------------------------------------------------------------------------
def map_arrival_directions():
	
	plt.figure()
	axs = plt.subplot(111, projection = 'mollweide')
	axs.set_longitude_grid_ends(90)
	
	gal_lon = np.zeros(len(data))
	gal_lat = np.zeros(len(data))
	E = np.zeros(len(data))

	for idata in range(len(data)):
		gal_lon[idata] = ra_dec_to_gal_lon(idata)
		gal_lat[idata] = ra_dec_to_gal_lat(idata)
		E[idata] = data[idata][1]
		
	plt.fill(countours_auger_sky()[:,1], countours_auger_sky()[:,0], facecolor = 'lightgray', edgecolor = None)
	plt.scatter(gal_lon, gal_lat, marker = 'D', c = E, cmap = 'viridis', s = 24)
	plt.colorbar(label = r'Energy of the event$\:$[EeV]', location = 'bottom')

	plt.xlabel(r'Galactic longitude, $l \: {\rm [deg]}$', labelpad = 10)
	plt.ylabel(r'Galactic latitude, $b \: {\rm [deg]}$')
	plt.xticks(ticks = [-120 * degree, -60 * degree, 0 * degree, 60 * degree, 120 * degree],
	labels = [r'$120\degree$', r'$60\degree$', r'$0\degree$', r'$300\degree$', r'$240\degree$'])
	plt.yticks(ticks = [-60 * degree, -30 * degree, 0 * degree, 30 * degree, 60 * degree], 
	labels = [r'$-60\degree$', r'$-30\degree$', r'$0\degree$', r'$30\degree$', r'$60\degree$'])
	plt.grid(linestyle = 'dotted', color = 'black', linewidth = 0.5, zorder = -1.0)
	plt.savefig('highest_energy_events.pdf', format = 'pdf', bbox_inches = 'tight')
	plt.savefig('highest_energy_events.png', format = 'png', bbox_inches = 'tight', dpi = 300)
	
	plt.show()

# ----------------------------------------------------------------------------------------------------
def map_arrival_directions_top4():
	
	plt.figure()
	axs = plt.subplot(111, projection = 'mollweide')
	axs.set_longitude_grid_ends(90)
	
	gal_lon = np.zeros(len(data))
	gal_lat = np.zeros(len(data))
	E = np.zeros(len(data))

	for idata in range(len(data)):
		gal_lon[idata] = ra_dec_to_gal_lon(idata)
		gal_lat[idata] = ra_dec_to_gal_lat(idata)
		E[idata] = data[idata][1]

	gal_lon = gal_lon[[1, 2, 3, 4]]
	gal_lat = gal_lat[[1, 2, 3, 4]]
	E = E[[1, 2, 3, 4]]

	plt.fill(countours_auger_sky()[:,1], countours_auger_sky()[:,0], facecolor = 'lightgray', edgecolor = None)
	plt.scatter(gal_lon, gal_lat, marker = 'D', c = E, cmap = 'viridis', s = 24, vmin = 46, vmax = 166)
	plt.colorbar(label = r'Energy of the event$\:$[EeV]', location = 'bottom')

	plt.xlabel(r'Galactic longitude, $l \: {\rm [deg]}$', labelpad = 10)
	plt.ylabel(r'Galactic latitude, $b \: {\rm [deg]}$')
	plt.xticks(ticks = [-120 * degree, -60 * degree, 0 * degree, 60 * degree, 120 * degree],
	labels = [r'$120\degree$', r'$60\degree$', r'$0\degree$', r'$300\degree$', r'$240\degree$'])
	plt.yticks(ticks = [-60 * degree, -30 * degree, 0 * degree, 30 * degree, 60 * degree], 
	labels = [r'$-60\degree$', r'$-30\degree$', r'$0\degree$', r'$30\degree$', r'$60\degree$'])
	plt.grid(linestyle = 'dotted', color = 'black', linewidth = 0.5, zorder = -1.0)
	plt.savefig('highest_energy_events_top4.pdf', format = 'pdf', bbox_inches = 'tight')
	plt.savefig('highest_energy_events_top4.png', format = 'png', bbox_inches = 'tight', dpi = 300)
	
	plt.show()

# ----------------------------------------------------------------------------------------------------
def main():

	# map_arrival_directions()
	map_arrival_directions_top4()

# ----------------------------------------------------------------------------------------------------
main()