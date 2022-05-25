#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 14:39:36 2022

@author: nicolekoko

Plot TIP data to look at the specific times

IMPORTANT: READ ALL COMMENTS 
- change file names

"""

import numpy as np
import matplotlib.pyplot as plt

file = "TIP Data file"
tipData = np.loadtxt(file, delimiter= ',', skiprows= 1, usecols= 5)
timeData = np.loadtxt(file, delimiter= ',', skiprows= 1, usecols= 0)

timeData = timeData - 604800*2030 - 24*60*60*7 # CHANGE SUBTRACTION BASED ON TIME TO BE SECONDS WITHIN 1 DAY 

plt.figure
plt.plot(timeData, tipData)
plt.xlim(1500,3800) # limit x by time period
plt.ylim(0, 2000) # limit y to see better
plt.show()

