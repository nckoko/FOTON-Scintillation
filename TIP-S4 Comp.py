#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 11:50:10 2021

@author: nicolekoko

Compare the locations of TIP at high TIP data to tangent point of high S4

IMPORTANT: READ ALL COMMENTS 
- change subtraction for tipSec based on day to get seconds within 1 day
- change file names

"""

import numpy as np
from pymap3d import aer
from pymap3d import ecef
import math
 

# import TIP data
tipData = np.loadtxt("TIP Data file")

tipSec = tipData[:,0]- 604800*1997 # CHANGE SUBTRACTION BASED ON TIME TO BE SECONDS WITHIN 1 DAY 
tipVal = tipData[:,1]


time = 103340 #change based on time of high s4
txid = 32 #change based on txid 

navSol = np.loadtxt("Navigation Solution Data file")
txiData = np.loadtxt("TXI Data file")


x = navSol[:,3]
y = navSol[:,4]
z = navSol[:,5]

txiS = txiData[:,1]
elev = txiData[:,4]
TXID = txiData[:,7]
azim = txiData[:,3]

# filter txi data by txid
index = np.where(TXID == txid)
for i in index:
    txiSec = txiS[i]
    elev1 = elev[i]
    azim1 = azim[i]
    
# filter txi data again by time
txiTind = np.where(txiSec == time)
txiTind = txiTind[0]
elev1 = elev1[txiTind]
azim1 = azim1[txiTind]

# filter navigation solution by time
navTime = navSol[:,1]

tInd = np.where(navTime == time)
tInd = tInd[0]

x1 = x[tInd] 
y1 = y[tInd]
z1 = z[tInd]


# trigonometry to find the distance (D) between the ISS and tangent point
C = math.sqrt(x1**2 + y1**2 + z1**2)
D = C * math.sin(math.radians(elev1))
D = abs(D)
print("D: ")
print(D)

# convert xyz to latlonalt
lat, lon, alt = ecef.ecef2geodetic(x1, y1, z1)

# find xyz of tangent point
x2, y2, z2 = aer.aer2ecef(azim1, elev1, D, lat, lon, alt)

print("tangent point: (xyz, lat lon alt)")
print(x2, y2, z2)

# find latlonalt of tangent point
lat2, lon2, alt2 = aer.aer2geodetic(azim1, elev1, D, lat, lon, alt)

print(lat2, lon2, alt2)


TIPtime = 103340 #change time based time of high TIP data

# TIP location 
tIndex = np.where(navTime == TIPtime) 
x0 = x[tIndex]
y0 = y[tIndex]
z0 = z[tIndex]

print("TIP location: (xyz, lat lon alt)")
print(x0, y0, z0)

lat0, lon0, alt0 = ecef.ecef2geodetic(x0, y0, z0)

print(lat0, lon0, alt0)

