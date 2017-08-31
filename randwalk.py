#!/usr/bin/env python

"""A Walker class for random walk objects in 1, 2, 3 or 4 dimensions"""

import numpy as np
import random as rnd
import matplotlib.pyplot as plt

__author__ = "William Lord"

class Walker:
	"""
	A class defining a random walker
	
	Variables:
	self.pos = position of Walker
	self.traj = A vector storing visited positions

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
		"""
		self.traj[0] = self.pos
		for step in range(1,self.N):
			move = rnd.choice(self.moves)
			self.pos += move
			self.traj[step] = self.pos

	def display(self):
		"""
		This method prints the trajectory of the walker.
		"""
		if self.d == 1:
			plt.plot(np.arange(0,len(self.traj)),self.traj)
		elif self.d == 2:
			plt.plot([p[0] for p in self.traj],[p[1] for p in self.traj])
		elif self.d == 3:
			print('3D plot!')
		elif self.d == 4:
			print('4D plot!')
		else:
			print('The dimension is not supported! Please use an integer dimension within 1 <= d <= 4.')

		plt.show()

	def reset(self):
		"""
		This method resets the walker to initial values.
		"""
		self.pos = np.zeros((1,self.d))
		self.traj = np.zeros((self.N,self.d))
		self.moves = np.concatenate((np.identity(self.d,int), -1*np.identity(self.d,int)))


	def walk2(self):
		"""
		This method takes a step in a random direction, then updates position and trajectory array.
		"""
		self.traj[0] = self.pos

		if self.d == 1 or self.d == 2 or self.d == 3 or self.d == 4:
			for step in range(1,self.N):
				# r = int(2*self.d*rnd.random())
				r = rnd.randint(0,2*self.d-1)
				if r == 0:
					self.pos[0][0] += 1
				elif r == 1:
					self.pos[0][0] -= 1
				elif r == 2:
					self.pos[0][1] += 1
				elif r == 3:
					self.pos[0][1] -= 1
				elif r == 4:
					self.pos[0][2] += 1
				elif r == 5:
					self.pos[0][2] -= 1
				elif r == 6:
					self.pos[0][3] += 1
				elif r == 7:
					self.pos[0][3] -= 1
				else:
					print('Something has gone wrong!')

				self.traj[step] = self.pos
		else:
			print('The dimension is not supported! Please use an integer dimension within 1 <= d <= 4.')