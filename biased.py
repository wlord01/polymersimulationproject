#!/usr/bin/env python

"""A class for self avoiding walks with biased sampling"""

import numpy as np
import random as rnd
import matplotlib.pyplot as plt

__author__ = "William Lord"

class Walker:
	"""
	Self-avoiding random walker (SAW) with biased sampling.
	
	Variables:
	self.pos - position of walker
	self.traj - An array storing visited positions
	self.moves - possible moves

	Methods:
	walk() - Makes walker walk N steps if no intersection
	takeStep() - Moves walker one step by biased sampling
	display() - Prints the trajectory of the walker
	reset() - resets walker to initial conditions
	"""
	def __init__(self,d,N):
		"""
		Set dimension, number of steps, starting position (origo), empty trajectory array and possible moves.

		In: 
		d = integer value of lattice dimension
		N = integer value of number of steps
		"""
		self.d = d
		self.N = N
		
		self.intersect = False
		self.pos = np.zeros((1,self.d), int)
		self.traj = np.zeros((1,self.d),int)
		self.moves = np.concatenate((np.identity(self.d,int), -1*np.identity(self.d,int)))
		self.a = []

	def walk(self):
		"""
		This method makes the walker walk N steps if trajectory does not intersect
		"""
		for step in range(1,self.N):
			if self.intersect==False:
				self.takeStep()

	def takeStep(self):
		"""
		Take a step according to biased sampling.

		The method checks neighboring coordinates and moves walker to a vacant site chosen at random.
		If no neighboring site is vacant, the walk is terminated.
		"""
		possibleNextPos = self.moves+self.pos
		validNextPos = []
		for coord in possibleNextPos:    # check which possible next pos are already in traj
			if np.any(np.all(np.equal(coord*np.ones(self.traj.shape,int), self.traj), axis=1)) == False:
				validNextPos.append(np.array([coord]))
		try:
			self.pos = rnd.choice(validNextPos)
		except:
			self.intersect = True
		if self.intersect == False:
			self.a.append(len(validNextPos)/(2*self.d-1))
			self.traj = np.concatenate((self.traj,self.pos))

	def display(self):
		"""
		This method prints the trajectory of the walker.
		"""
		if self.d == 1:
			plt.plot(np.arange(0,len(self.traj)),self.traj)
		elif self.d == 2:
			plt.plot([p[0] for p in self.traj],[p[1] for p in self.traj])
		elif self.d == 3:
			print('3D plot under construction!')
		else:
			print('The dimension is not supported! Please use an integer dimension within 1 <= d <= 3.')

		plt.show()

	def reset(self):
		"""
		This method resets the walker to initial values.
		"""
		self.pos = np.zeros((1,self.d))
		self.traj = np.zeros((1,self.d),int)
		self.moves = np.concatenate((np.identity(self.d,int), -1*np.identity(self.d,int)))
		self.intersect = False
		self.a = []