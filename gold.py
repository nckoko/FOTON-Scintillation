#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 14:22:44 2022

@author: nicolekoko

Compare GOLD radiance to TIP data at night (time range 23:00-00:00) and plot

IMPORTANT: READ ALL COMMENTS
- change subtraction for tipSec based on day to get seconds within 1 day
- change file names

"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os
os.environ["PROJ_LIB"] = os.path.join(os.environ["CONDA_PREFIX"], "share", "proj")
from mpl_toolkits.basemap import Basemap

#read file
ncfile = 'GOLD NetCDF file'
f = Dataset(ncfile, 'r')

ew = f.variables['GRID_EW'][:]
ns = f.variables['GRID_NS'][:]
rna = f.variables['RAY_NADIR_ANGLE'][:]
Time_UTC_df = f.variables['TIME_UTC'][:] #increments of 16 seconds
radiance = f.variables['RADIANCE'][:]
wavelength = f.variables['WAVELENGTH'][:]
ref_lat = f.variables["REFERENCE_POINT_LAT"][:]
ref_lon = f.variables["REFERENCE_POINT_LON"][:]
f.close()

#figure out time
Time_UTC = Time_UTC_df.astype(np.str_)
time = Time_UTC[0]
time = time[0] + time[1] + time[2] + time[3] + time[4] + time[5] + time[6] + time[7] + time[8] + time[9] + ' ' + time[11] + time[12] + time[13] + time[14] + time[15] + time[16] + time[17] + time[18]


#unmask lon and lat and delete rows that are completely nan
lon = ref_lon.data
lon = lon[~np.isnan(lon).any(axis=1)]

lat = ref_lat.data
lat = lat[~np.isnan(lat).any(axis=1)]


#narrow wavelength
ids = np.argwhere((135.0 <= wavelength[50,20,:]) & (wavelength[50,20,:] <= 137.0)) #135.6 nm

#find radiance at wavelength band and delete rows of only zero
s1356 = np.nansum(radiance[:,:,ids], axis = 2) * .04 #.4 = spectral resolution
s1356 = s1356[:,:,0]
s1356 = s1356.data
s1356 = s1356[~np.all(s1356 == 0, axis=1)]


#TIP data
tip_data = np.loadtxt('TIP Data file')

tip_time = tip_data[:,0] - (347*24*60*60) - (365*24*60*60*38) - (4*86400) # CHANGE SUBTRACTION BASED ON TIME TO BE SECONDS WITHIN 1 DAY 
print(tip_time)

index = np.where((tip_data[:,4] >= np.min(lat)) & (tip_data[:,4] <= np.max(lat)) & (tip_data[:,5] >= lon[0,0]) & (tip_data[:,5] <= lon[0,len(lon[0])-1]) & (tip_time >= 23*60*60))


tip_data = tip_data[index]
tip_time1 = tip_data[:,0] - (347*24*60*60) - (365*24*60*60*38) - (4*86400) # CHANGE SUBTRACTION BASED ON TIME TO BE SECONDS WITHIN 1 DAY 
tip_counts = tip_data[:,8]
tip_lat = tip_data[:,4]
tip_lon = tip_data[:,5]


#plot 
fig = plt.figure()
m = Basemap(projection='geos',
            rsphere=(6378137.00,6356752.3142),
            resolution='c',
            area_thresh=10000.,
            lon_0=-47.5,
            satellite_height=35785831)
m.drawcoastlines()
m.drawcountries()

# draw parallels and meridians.
m.drawparallels(np.arange(-90.,120.,30.))
m.drawmeridians(np.arange(0.,360.,60.))
m.drawmapboundary()

x, y = m(lon,lat)

#plot the GOLD data
my_cmap = plt.get_cmap('RdYlBu_r')
cs = m.pcolormesh(x,y,s1356,cmap = my_cmap, norm = colors.SymLogNorm(linthresh = 1, linscale= 1, vmin = 0, base=1.01))
m.colorbar(location= 'bottom')

#plot TIP data
a, b = m(tip_lon,tip_lat)
cs1 = m.scatter(a,b,s=1, c=tip_counts, cmap = 'Wistia')

m.colorbar()

plt.title(time)

plt.show()


#find pixels that line up w/ TIP

radiance = np.zeros(len(tip_data))
n = 0
for x in tip_data:
    diff = np.absolute(lat - x[4]) + np.absolute(lon - x[5])
    row, col = np.where(diff == diff.min())
    radiance[0+n] = s1356[row,col]
    n+=1


# plot graph of TIP and radiance
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('TIP Data', color=color)
ax1.plot(tip_time1, tip_counts, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Radiance', color=color)  # we already handled the x-label with ax1
ax2.plot(tip_time1, radiance, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.title(time)
plt.show()


