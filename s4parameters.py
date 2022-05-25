#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 12:24:13 2021

@author: nicolekoko

Find S4 and graph it overlaid on TIP data

IMPORTANT: change file names
"""

import numpy as np
from scipy import signal
from ReadIQdata import IQdata
import matplotlib.pyplot as plt


iqData = IQdata("IQ Data file")
txiData = np.loadtxt("TXI Data file")
tipData = np.loadtxt("TIP Data file")

tipSec = tipData[:,0] - 604800*1997 # CHANGE SUBTRACTION BASED ON TIME TO BE SECONDS WITHIN 1 DAY 
tipVal = tipData[:,1]


S = txiData[:,1]
T = S + txiData[:,2]
elev = txiData[:,4]
TXID = txiData[:,7]
azim = txiData[:,3]

i = iqData.getIdata()

q = iqData.getQdata()
s = iqData.getGPSsecond()
t = s + iqData.getGPSfrac()
txid = iqData.getTXID()
interval = 60

txid_read = np.unique(txid)


for n in txid_read:
    indexnum = np.where(txid == n)
    
    for index in indexnum:
        i1 = i[index]
        q1 = q[index]
        t1 = t[index]
        s1 = s[index]


    indexnum1 = np.where(TXID == n)
    for index1 in indexnum1:
        S1 = S[index1]
        T1 = T[index1]
        elev1 = elev[index1]
        azim1 = azim[index1]

    tipIndex = np.where(np.logical_and(tipSec>=t1[0], tipSec<=t1[len(t1)-1])) 
    for g in tipIndex:
        tipSec1 = tipSec[g]
        tipVal1 = tipVal[g]
 
    timeindex = np.where(np.logical_and(T1>= t1[0], T1 <= t1[len(t1)-1]))
    for tindex in timeindex:
        S1 = S1[tindex]
        T1 = T1[tindex]
        elev1 = elev1[tindex]
        azim1 = azim1[tindex]
    

    #Kai Guo paper for one transmitter
    
    P = np.sqrt(np.square(i1) + np.square(q1)) #signal intensity
    
    #pass the signal through a 6th order butterworth filter
    b, a = signal.butter(6, 0.1)
    
    
    Ptrend = signal.filtfilt(b, a, P)
    #print(len(Ptrend))
    
    #60 second average of Ptrend
    uniqueSec = (np.unique(s1)[np.unique(s1).size-1] - np.unique(s1)[0]) / interval
    
    u = 0
    while u <= uniqueSec:
        tStart = t1[0] + interval*u 
        tEnd = tStart + interval 
        tIndex = np.where(np.logical_and(t1>=tStart, t1<=tEnd))

        for x in tIndex:
            Ptrendvals = Ptrend[x]
            Ptemp = P[x]
            
        PtrendavgVal = np.sum(Ptrendvals)
        PtrendavgVal = PtrendavgVal/Ptrendvals.size
        if u == 0:
            PtrendavgArr = np.full(Ptrendvals.size, PtrendavgVal)
            Pdet = np.divide(Ptemp, PtrendavgArr)

        else:
            PtrendavgArrTemp = np.full(Ptrendvals.size, PtrendavgVal)
            Pdet = np.append(Pdet, np.divide(Ptemp, PtrendavgArrTemp))
            PtrendavgArr = np.append(PtrendavgArr, PtrendavgArrTemp)
        u+=1
    if len(PtrendavgArr) != len(P):
        PtrendavgArr = np.append(PtrendavgArr, PtrendavgVal)
    if len(Pdet) != len(t1):
        Pdet = np.append(Pdet, Ptemp[Ptemp.size-1]/PtrendavgVal)
 
    Pdet = np.divide(P, PtrendavgArr)
       
            
        
    u = 0
    #Finding S4 = (<Pdet^2> - <Pdet>^2)/<Pdet>^2
    while u <= uniqueSec:
        tStart1 = t1[1] + interval*u 
        tEnd1 = tStart1 + interval 
        ti = np.where(np.logical_and(t1>=tStart1, t1<=tEnd1))
        tiArr = ti[0]
    
        for a in ti:
            PdetVals = Pdet[a]
            Pdet2Vals = np.square(Pdet[a])
        PdetSum = np.sum(PdetVals)
        Pdet2Sum = np.sum(Pdet2Vals)
        PdetAvgVal = PdetSum/PdetVals.size
        Pdet2AvgVal = Pdet2Sum/Pdet2Vals.size
        if u == 0:
            PdetAvg = np.full(PdetVals.size, PdetAvgVal)
            Pdet2Avg = np.full(PdetVals.size, Pdet2AvgVal)
        else:
            PdetAvg = np.append(PdetAvg, np.full(PdetVals.size, PdetAvgVal))
            Pdet2Avg = np.append(Pdet2Avg, np.full(PdetVals.size, Pdet2AvgVal))
        u+=1
    if len(PdetAvg) != len(t1):
        PdetAvg = np.append(PdetAvg, PdetAvgVal)
    if len(Pdet2Avg) != len(PdetAvg):
        Pdet2Avg = np.append(Pdet2Avg, Pdet2AvgVal)
    
    S4 = (Pdet2Avg - np.square(PdetAvg)) / np.square(PdetAvg)
    S4 = np.sqrt(S4)

    
    


    fig, ax1 = plt.subplots(2, sharex=True)
    plt.title("TXID: " + str(n))
    color = 'tab:red'
    ax1[0].set_xlabel('Time (s)')
    ax1[0].set_ylabel('S4', color=color)
    ax1[0].plot(t1, S4, color=color)
    ax1[0].axhline(y=0.6, color='k', linestyle='-')
    ax1[0].set_ylim(0, 1.5)
    ax1[0].tick_params(axis='y', labelcolor=color)
    
    

    ax2 = ax1[0].twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'tab:blue'
    ax2.set_ylabel('Elevation Angle', color=color)  # we already handled the x-label with ax1
    ax2.plot(T1, elev1, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax1[1].set_xlabel('Time (s)')
    ax1[1].set_ylabel('TIP data')
    ax1[1].plot(tipSec1, tipVal1)
    
    plt.show()
    
    
