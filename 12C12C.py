#!/usr/bin/env python
############################################################################    
# Drew Blankstein 
# University of Notre Dame
# 
# ATHENA Energy Loss Simulation Program
# Utilizes pysrim package to interface with TRIM to preform ionization
# loss calculations. 
############################################################################ 

from srim import Ion, Layer, Target, TRIM
from srim.output import Phonons, Ioniz
from srim.output import Results

import sys
import os
import random
import math

import matplotlib.pyplot as plt
import numpy as np 
import matplotlib.mlab as mlab

from srim.output import Results
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from scipy.interpolate import interp1d
import scipy.integrate as integrate

srim_executable_directory = '/Users/drewblankstein/Documents/research/simulation/SRIM'


num_ions= 25 #num of ions used to strip 
beam_energy = 30 #MeV



############################################################################
############################################################################
############################################################################
############################################################################
#IONS TO BE ANALYZED


class particle: 
	def __init__(self,title,A,Z,M,E,color):
		self.E = E
		self.A = A
		self.Z = Z
		self.M = M
		self.title = title
		self.strip = np.zeros(18)
		self.color = color

	def strip_eloss(self,energy):
		if(energy <= 0.0):
			self.E = 0.0
			return 0.0
		else:
			beam_trim = TRIM(target, Ion(self.title, energy=energy*1.0e6,mass=self.M), number_ions=num_ions, calculation=1)
			beam_results = beam_trim.run(srim_executable_directory)

			beam_energy = beam_results.ioniz.ions*100
			beam_depth = beam_results.ioniz.depth*1e-8

			f = interp1d(beam_depth,beam_energy, kind='linear')
			xnew = np.linspace(0.0157,1.57,100)
			ynew = f(xnew)

			eloss = integrate.quad(f,0.0157,1.57)[0]

			return eloss

	def plot(self, beam_strip, strip_int):
		strip = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
		plt.scatter(strip,beam_strip, color = 'b',label='Carbon Beam')
		plt.plot(strip,beam_strip, color = 'b')
		plt.scatter(strip,self.strip, color = self.color,label=self.title)
		plt.plot(strip,self.strip, color = self.color)
		plt.grid(True)
		plt.ylabel('Energy Loss (MeV)')
		plt.xlabel('Strip Number')
		plt.legend(loc='upper right')


############################################################################
############################################################################
############################################################################
############################################################################
#TARGET

gas_pressure1 = 100 #torr

#strip gas density given target pressure 
def gas_density(pressure): 
	pressure = 133.322*pressure
	molar_mass = 16.04
	R = 8.3144598*10**6
	T = 273
	return molar_mass*pressure/(R*T)

# Construct a layer of 1.75 cm thick target layers consisting of Methane gas @ 100 torr
layer = Layer({
        'C': {
            'stoich': 0.2,
            'E_d': 10.0,
            'lattice': 3.0,
            'surface': 2.0
        },
        'H': {
            'stoich': 0.8,
            'E_d': 28.0,
            'lattice': 3.0,
            'surface': 7.41,
        }}, density=gas_density(gas_pressure1), width=0.157e9,phase=1)



# Construct a target of a single layer of Methane
target = Target([layer])


############################################################################
############################################################################
############################################################################
############################################################################


for i in range(0,18):
	reaction_occured = False	
	carbon_beam = particle('C',12.0,6.0,12.0,beam_energy,'b') 
	oxygen_er = particle('O',16.0,8.0,15.999 ,0.0,'r')
	neon_er = particle('Ne',20.0,10.0,20.1797,0.0,'k')
	sodium_er = particle('Na',23.0,11.0,22.989769,0.0,'g')
	flourine_er = particle('F',19.0,9.0,18.99840322,0.0,'y')
	for k in range(0,18):
		if(i == k):
			carbon_beam.strip[k] = carbon_beam.strip_eloss(carbon_beam.E)
			carbon_beam.E = carbon_beam.E - carbon_beam.strip[k]

			oxygen_er.E = carbon_beam.E
			sodium_er.E = carbon_beam.E
			neon_er.E = carbon_beam.E
			flourine_er.E = carbon_beam.E

			oxygen_er.strip[k] = oxygen_er.strip_eloss(oxygen_er.E)
			flourine_er.strip[k] = flourine_er.strip_eloss(flourine_er.E)
			sodium_er.strip[k] = sodium_er.strip_eloss(sodium_er.E)
			neon_er.strip[k] = neon_er.strip_eloss(neon_er.E)

			oxygen_er.E = oxygen_er.E - oxygen_er.strip[k]
			flourine_er.E = flourine_er.E - flourine_er.strip[k]
			sodium_er.E = sodium_er.E - sodium_er.strip[k]
			neon_er.E = neon_er.E - neon_er.strip[k]


			reaction_occured = True 

		elif(reaction_occured == True): 

			carbon_beam.strip[k] = carbon_beam.strip_eloss(carbon_beam.E)
			carbon_beam.E = carbon_beam.E - carbon_beam.strip[k]

			oxygen_er.strip[k] = oxygen_er.strip_eloss(oxygen_er.E)
			flourine_er.strip[k] = flourine_er.strip_eloss(flourine_er.E)
			sodium_er.strip[k] = sodium_er.strip_eloss(sodium_er.E)
			neon_er.strip[k] = neon_er.strip_eloss(neon_er.E)

			oxygen_er.E = oxygen_er.E - oxygen_er.strip[k]
			flourine_er.E = flourine_er.E - flourine_er.strip[k]
			sodium_er.E = sodium_er.E - sodium_er.strip[k]
			neon_er.E = neon_er.E - neon_er.strip[k]


		elif(reaction_occured == False):
			carbon_beam.strip[k] = carbon_beam.strip_eloss(carbon_beam.E)
			carbon_beam.E = carbon_beam.E - carbon_beam.strip[k]

	oxygen_er.plot(carbon_beam.strip,i)
	sodium_er.plot(carbon_beam.strip,i)
	neon_er.plot(carbon_beam.strip,i)
	flourine_er.plot(carbon_beam.strip,i)
	plt.savefig('/Users/drewblankstein/Documents/research/simulation/srim_out/12C12C/figures05/nrgloss_' + 'strip_' + str(i) + '.pdf')
	plt.close()








