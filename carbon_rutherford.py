#!/usr/bin/env python
############################################################################    
# Drew Blankstein 
# University of Notre Dame
# 
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
	def __init__(self,title,A,Z,M,E):
		self.E = E
		self.A = A
		self.Z = Z
		self.M = M
		self.title = title
		self.strip = np.zeros(18)
		self.angle = 0 


	def strip_eloss(self,energy):
		if(energy <= 1e-4):
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
		plt.scatter(strip,beam_strip, color = 'b',label=('Carbon Beam Angle: '+ str(carbon_beam.angle)[:2]))
		plt.plot(strip,beam_strip, color = 'b')
		plt.scatter(strip,self.strip, color = 'r',label=(self.title + ' Scatter Angle: ' + str(self.angle)[:6]))
		plt.plot(strip,self.strip, color = 'r')
		plt.scatter(strip,beam_strip+self.strip, color = 'k',label=(self.title + ' Total'))
		plt.plot(strip,beam_strip+self.strip, color = 'k')
		plt.grid(True)
		plt.ylabel('Energy Loss (MeV)')
		plt.xlabel('Strip Number')
		plt.legend(loc='upper right')
		plt.savefig('/Users/drewblankstein/Documents/research/simulation/srim_out/12C12C/figures07/nrgloss_' + self.title + 'iter_' + str(strip_int) + 'scatter.pdf')
		plt.close()


	def rutherford(self):
		Z_target = 6.0
		angle = np.linspace(0.0,np.pi,1000.0)
		a = 1.296
		b = ((Z_target**2)/self.E)**2.0
		c = 1.0/(np.sin(angle/2.0))**4.0

		rutherford = a*b*c

		rutherford = a*b*c*np.sin(angle)*2*np.pi

		f = interp1d(angle,rutherford, kind='linear')
		xnew = np.linspace(0.01,np.pi,100)
		ynew = f(xnew)

		rut_cross_section_1 = integrate.quad(f,0.01,np.deg2rad(45))[0]
		rut_cross_section_2 = integrate.quad(f,np.deg2rad(45),np.deg2rad(90))[0]


		plt.plot(angle*(180/np.pi),rutherford)
		plt.yscale('log')
		plt.show()



	def generate_reaction(self,angle):
		be_energy = self.E 
		MeVMass = 938.0
		pi = np.pi

		m1 = self.M
		m2 = self.M
		m3 = self.M
		m4 = self.M

		angle = np.deg2rad(angle)

		#calculate some basic properties here 
		q_value = (m1 + m2 - m3 - m4)*MeVMass
		com_totE = (m1*be_energy)/(m1+m2)

		#com energy of reaction products 
		eje_comE = (m4*((m2/m1)*com_totE+q_value))/(m3+m4) #ejectile -- particle 3
	 	rec_comE = (m3*((m2/m1)*com_totE+q_value))/(m3+m4) #recoil -- partcile 4  

	 	#set random theta for outgoing particles
	 	com_randthetrec = angle 
	  	com_randtheteje = com_randthetrec + np.pi


	 	#K (unitless factor) of outgoing partciles
	 	eje_Kout = np.sqrt((m1*m3*com_totE)/(m2*m4*(com_totE+q_value)))
	 	rec_Kout = np.sqrt((m1*m4*com_totE)/(m2*m3*(com_totE+q_value)))

	 	#lab angle of outgoing particles  
		eje_labtheta = np.arctan((np.sin(com_randtheteje))/(np.cos(com_randtheteje)+eje_Kout))#*(180.0/pi) 
		rec_labtheta = np.arctan((np.sin(com_randthetrec))/(np.cos(com_randthetrec)+rec_Kout))#*(180.0/pi) 

		#lab energy of outgoing particles 
		eje_labE = eje_comE*(1.0 + eje_Kout**2 + 2.0*eje_Kout*np.cos(com_randtheteje))
	 	rec_labE = rec_comE*(1.0 + rec_Kout**2 + 2.0*rec_Kout*np.cos(com_randthetrec)) 

		eje_labtheta = np.arctan((np.sin(com_randtheteje))/(np.cos(com_randtheteje)+eje_Kout))*(180.0/pi) 
		rec_labtheta = np.arctan((np.sin(com_randthetrec))/(np.cos(com_randthetrec)+rec_Kout))*(180.0/pi) 

		kinematics = [eje_labtheta,eje_labE,rec_labtheta,rec_labE]

		return kinematics



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



angle = 0 

for j in range(0,num_iterations):
	for i in range(4,5):
		reaction_occured = False
		carbon_beam = particle('C',12.0,6.0,12.0,beam_energy) 
		carbon_scatter = particle('C',12.0,6.0,12.0,0.0) 
		for k in range(0,18):
			if(i == k):
				kinematics = carbon_beam.generate_reaction(angle)
				carbon_beam.E = kinematics[3]
				carbon_beam.angle = kinematics[2]
				carbon_scatter.E = kinematics[1]
				carbon_scatter.angle = kinematics[0]

				carbon_beam.strip[k] = carbon_beam.strip_eloss(carbon_beam.E)
				carbon_beam.E = carbon_beam.E - carbon_beam.strip[k]

				carbon_scatter.strip[k] = carbon_scatter.strip_eloss(carbon_scatter.E)
				carbon_scatter.E = carbon_scatter.E - carbon_scatter.strip[k]


				reaction_occured = True 

			elif(reaction_occured == True): 

				carbon_beam.strip[k] = carbon_beam.strip_eloss(carbon_beam.E)
				carbon_beam.E = carbon_beam.E - carbon_beam.strip[k]
				
				carbon_scatter.strip[k] = carbon_scatter.strip_eloss(carbon_scatter.E)
				carbon_scatter.E = carbon_scatter.E - carbon_scatter.strip[k]

			elif(reaction_occured == False):
				carbon_beam.strip[k] = carbon_beam.strip_eloss(carbon_beam.E)
				carbon_beam.E = carbon_beam.E - carbon_beam.strip[k]


		carbon_scatter.plot(carbon_beam.strip,j)

	angle = angle + 5.0




