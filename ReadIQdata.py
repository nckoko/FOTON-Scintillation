#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 12:36:06 2021

@author: nicolekoko

Read the IQ data. Necessary for S4parameters file.

"""

import numpy as np


class IQdata:
    
    def __init__(self, datafile):
        self.datafile = datafile
    
    def readFile(self):
        wholedata = np.loadtxt(self.datafile)
        return wholedata

    def getTime(self):
        time = np.loadtxt(self.datafile, usecols = 1)
        return time
               
    def getGPSweek(self):
        GPSweek_array = np.loadtxt(self.datafile, usecols = 2)
        return GPSweek_array
    
    def getGPSsecond(self):
        GPSsecond_array = np.loadtxt(self.datafile, usecols = 3)
        return GPSsecond_array
    
    def getGPSfrac(self):
        GPSfrac_array = np.loadtxt(self.datafile, usecols = 4)
        return GPSfrac_array
    
    def getBeatCarPhase(self):
        beatCarPhase_array = np.loadtxt(self.datafile, usecols = 5)
        return beatCarPhase_array
    
    def getIdata(self):
        i_array = np.loadtxt(self.datafile, usecols = 6)
        return i_array
    
    def getQdata(self):
        q_array = np.loadtxt(self.datafile, usecols = 7)        
        return q_array
    
    def getDataSymbol(self):
        dataSymbol_array = np.loadtxt(self.datafile, usecols = 8)
        return dataSymbol_array
    
    def getSignalType(self):
        signalType_array = np.loadtxt(self.datafile, usecols = 10)
        return signalType_array
    
    def getTXID(self):
        txid_array = np.loadtxt(self.datafile, usecols = 11)
        return txid_array

