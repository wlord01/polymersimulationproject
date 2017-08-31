#!/usr/bin/env python

"""Script for analysing entropy of random walks/self avoiding walks for different N"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import analysis

__author__ = "William Lord"

def func(x, a, b, c):
	return a * np.exp(-b * x) + c

def func2(x, a, b):
	return a*x + b

def plotExpFit(nList,entropyList,x,poptExp):
	poptExp, pcovExp = curve_fit(func, nList, entropyList)
	plt.figure()
	plt.plot(nList,entropyList,'ko',label='Simulation data')
	plt.plot(x, func(x, *poptExp), 'b-', label='Exponential fit')
	plt.legend()
	plt.show()

def plotLinFit(nList,entropyList,x,poptLin,indices):
	poptLin, pcovLin = curve_fit(func2, nList[indices[0]:indices[1]], entropyList[indices[0]:indices[1]])
	plt.figure()
	plt.plot(nList,entropyList,'ko',label='Simulation data')
	plt.plot(x, func2(x, *poptLin), 'r-', label='Linear fit')
	plt.legend()
	plt.show()

nList = [4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50]#,52,54,56,58,60]
entropyList = []
trials = 10000
dim = 3
walkType = 'saw'
x = np.linspace(0,60,100)
indices = [round(len(nList)/1.25), len(nList)]

for N in nList:
	[p, acceptedWalksRate] = analysis.simulateWalks(trials,dim,N,walkType)
	entropy = analysis.getEntropy(dim,N,walkType,acceptedWalksRate)
	print(entropy)
	entropyList.append(entropy)

plotExpFit(nList,entropyList,x,poptExp)
plotLinFit(nList,entropyList,x,poptLin)