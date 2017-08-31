#!/usr/bin/env python

"""A class for self avoiding walks in 1, 2, 3 or 4 dimensions"""

import numpy as np
import random as rnd
import matplotlib.pyplot as plt

__author__ = "William Lord"

class Walker:
	"""
	A class defining a self-avoiding random walker (SAW)
	
	Variables:
	self.pos = position of SAW
	self.traj = An array storing visited positions

	Methods:
	walk() - Makes random walker walk N steps
	display() - Prints the trajectory of the walker
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
		
		self.pos = np.zeros((1,self.d))
		self.traj = np.zeros((self.N,self.d))
		self.moves = np.concatenate((np.identity(self.d,int), -1*np.identity(self.d,int)))

	def walk(self):
		"""
		This method takes a step in a random direction, then updates position and trajectory array.
		
		The move is made in a random direction, omitting the direction from which the walker just came.
		Trajectory is checked and walk terminated if there is an intersection.
		"""
		self.traj = np.zeros((1,self.d),int)
		lastMove = np.zeros(self.d,int)    # Dummy variable
		for step in range(1,self.N):
			move = rnd.choice(self.moves[~np.all(self.moves==-1*lastMove, axis=1)])
			self.pos += move
			
			intersect = False    # Dummy variable
			if len(self.traj) == len(np.unique(np.concatenate((self.traj,self.pos)), axis=0)):
				intersect=True
				break
			if intersect == True:
				self.traj = self.traj[0:step]
				break

			self.traj = np.concatenate((self.traj,self.pos))

			lastMove -= lastMove
			lastMove += move

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
		self.traj = np.zeros((self.N,self.d))
		self.moves = np.concatenate((np.identity(self.d,int), -1*np.identity(self.d,int)))