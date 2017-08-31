#!/usr/bin/env python

"""
Script for analysing end-to-end length of random walks/self avoiding walks and calculating exponent p=2*nu.

simulateWalks() rus a Monte Carlo simulation over m walks of N length of chosen walk type and calculates p=2*nu.
getEntropy() calculates absolute dimensionless entropy per monomer for a Monte Carlo simulation.
"""

import time

import numpy as np
import random as rnd

import randwalk
import saw
import biased

__author__ = "William Lord"

def e2edist(walker):
	"""
	Calculate end-to-end distance of random walk/self avoiding walk starting in origo. 
	Takes end position from walker object.

	In: walker - random walk or self avoiding walk object
	Out: Float type value of end-to-end distance
	"""
	return np.linalg.norm(walker.pos)

def calcExponent(walker):
	"""
	Calculate the exponent p = 2*nu in mean(R_N**2) ~ N^p

	In: walker - random walk or self avoiding walk object
	Out: Exponent p 
	"""
	R_N = e2edist(walker)
	return np.log(R_N**2)/np.log(walker.N)

def calcError(data):
	"""
	Calculate the expected error from a set of data points.

	In: data - numpy array of data points
	"""
	variance = (np.sum(data**2)/len(data)) - (np.sum(data)/len(data))**2
	error = np.sqrt(variance/len(data))
	return error

def getEntropy(dim, steps, walkType, acceptedWalksRate):
	"""
	Calculate dimensionless entropy per monomer for SAWs and random walks.

	In: 
	dim - dimension of lattice (int)
	steps - number of steps in a walk (int)
	walkType - the type of walk (string)
	acceptedWalks - the number of successful attempts (int)

	Out:
	entropy - the dimensionless entropy per monomer (float)
	"""
	if walkType == 'saw':
		omega = acceptedWalksRate * (2*dim - 1)**(steps-2)
	else:
		omega = (2*dim)**(steps-2)
	return np.log(float(omega))/(steps-2)

def simulateWalks(trials, dim, steps, walkType='rand'):
	"""
	Runs a Monte Carlo simulation for chosen walkType and calculates the exponent p=2*nu.

	In: 
	trials - number of trials in simulation (int)
	dim - dimensions of lattice (int)
	steps - number of steps for each trials (int)
	walkType - the type of walk: random walk ('rand'); SAW ('saw') or SAW by biased sampling ('biased') (string)

	Out: [p, acceptedWalks]
	p - the exponent p = 2*nu (float)
	acceptedWalks - the number of successful attempts (int)
	"""
	start = time.time()

	print('Simulation of ', trials, 'walks, ', steps, 'steps each, in', dim, 'dimension(s).')

	e2eSqList = []
	biasE2eSqList = []
	e2eList = []
	lenList = [] 
	aProdList = []
	pList = []
	
	if walkType == 'saw':
		w = saw.Walker(dim, steps)
	elif walkType == 'biased':
		w = biased.Walker(dim, steps)
	else:
		w = randwalk.Walker(dim, steps)
	
	walkStart = time.time()
	# rnd.seed(0)    # Seed for statistics	
	acceptedWalks = 0
	numOfWalks = 0
	print('Simulation started at: ', time.ctime())
	# for walk in range(trials):
	while acceptedWalks < trials:
		w.walk()
		walkLength = len(w.traj)
		lenList.append(walkLength)
		if walkType == 'saw':
			if walkLength == steps:
				e2eSqList.append(e2edist(w)**2)
				e2eList.append(e2edist(w))
				acceptedWalks += 1
		elif walkType == 'biased':
			if w.intersect == False:
				biasE2eSqList.append(np.prod(w.a)*e2edist(w)**2)
				aProdList.append(np.prod(w.a))
				acceptedWalks += 1
		else:
			e2eSqList.append(e2edist(w)**2)
			e2eList.append(e2edist(w))
			acceptedWalks += 1
		if numOfWalks == 0:
			if walkType != 'saw' and walkType != 'biased':
				print('Estimated runtime: ', (time.time()-walkStart)*trials/60, ' min')

		numOfWalks += 1
		w.reset()

	if walkType == 'biased':
		e2eSqAve = np.sum(biasE2eSqList)/np.sum(aProdList)
		e2eSqError = np.std(biasE2eSqList)/np.sqrt(acceptedWalks)
	else:
		e2eSqAve = sum(e2eSqList)/len(e2eSqList)
		e2eSqError = np.std(e2eSqList)/np.sqrt(acceptedWalks)

	p = np.log(e2eSqAve)/np.log(steps)
	
	pError = p - (np.log(e2eSqAve-e2eSqError)/np.log(steps))
	pError2 = (np.log(e2eSqAve+e2eSqError)/np.log(steps)) - p

	print('Runtime: ', (time.time()-start)/60, ' min')

	print('e2eSqAve: ', e2eSqAve)
	print('p: ', p)
	print('e2eSqError: ', e2eSqError)
	print('pError: ', pError)
	print('pError2: ', pError2)
	print('Accepted walks rate: ', acceptedWalks/numOfWalks)
	print('Total number of walks made: ', numOfWalks)

	return p, acceptedWalks/numOfWalks