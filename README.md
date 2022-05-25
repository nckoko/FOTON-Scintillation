# FOTON Scintillation 
Finding ionospheric scintillation in FOTON data and comparing locations of high S4 to ISS @ high TIP data. 

Required libraries: numpy, scipy, matplotlib.plot, pymap3d, math 

Required files: FOTON IQ data, txi data, navigation solution data, TIP data

File Descriptions: 
  - ReadIQdata
    - Reads IQ data. Necessary for S4parameters file. 
  - S4parameters
    - Finds S4 and graphs it with on TIP data
  - TIP-S4 Comp
    - Compares the locations of TIP at high TIP data to tangent point of high S4
  - TIP Plot
    - Plots TIP data to look at the specific times
    - Can change time range by changing x limits

# GOLD - TIP Comparison
Comparing GOLD radiance to TIP Data at night (time range: 23:00 - 00:00)

Required libraries: numpy, netCDF4, matplotlib.pyplot, matplotlib.colors, mpl_toolkits.basemap, os 

Required files: TIP data with ISS location, GOLD Level 1C NI1 netCDF file (found here: https://gold.cs.ucf.edu/data/search/)

File Description: 
  - gold
    - Compares GOLD radiance to TIP data and plots in two ways: map overlay (TIP path over map of GOLD) and graph of TIP and GOLD at location of TIP path
