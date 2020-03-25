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

from layer_definitions import setlayer

srim_executable_directory = r'C:\Users\drewblankstein\Documents\SRIM-2013'



def main_func(m1_name,m1_mass,m1_energy,m1_Z,m1_A,m4_name,m4_mass,m4_Z,m4_A,gastype,gaspressure,windowthick,reactionstrip):
        ############################################################################
        # INPUT  
        # Input information for incoming particle (m1), outgoing light particlce (m3)
        # and outgoing heavy recoil (m4.)
        ############################################################################

        #this is the number of ions used in the TRIM calculation 
        num_ions= 25 
        #projectile info
        m1_energy = m1_energy
        m1_name = m1_name
        m1_mass = m1_mass
        m1_Z = m1_Z
        m1_A = m1_A

        #target gas options are methane, p_ten, or helium
        target_gas = gastype
        gas_pressure = gaspressure #torr

        #light particle info
        m3_name = 0
        m3_mass = 0
        m3_Z = 0
        m3_A = 0

        #heavy nucleus info
        m4_name = m4_name
        m4_mass =  m4_mass
        m4_Z = m4_Z
        m4_A = m4_A
        """
        #projectile info
        m1_energy = 20 #MeV
        m1_name = 'C'
        m1_mass = 12.0
        m1_Z = 6.0
        m1_A = 12.0

        #target gas options are methan, p_ten, or helium
        target_gas = 'methane'
        gas_pressure = 150 #torr

        #light particle info
        m3_name = 'O'
        m3_mass = 15.003065
        m3_Z = 8.0
        m3_A = 15.0

        #heavy nucleus info
        m4_name = 'O'
        m4_mass =  15.994914
        m4_Z = 8.0
        m4_A = 16.0
        """
        #the strip in which the reaction will take place
        reaction_strip = int(reactionstrip)
        length = 0.157e9
        dead_length = 0.230251e9
        windowthick = 60000
        ############################################################################
        # PARTICLE CLASS DEFINITION
        # Each particle that will undergoe an energy loss calculation will be objects 
        # of the particle class. Particle class will contain all the information of 
        # the particle as it is transported through the material 
        ############################################################################

        class particle: 
                def __init__(self,title,A,Z,M,E,color,linetype):
                        self.E = E
                        self.E_init = E
                        self.A = A
                        self.Z = Z
                        self.M = M
                        self.title = title
                        self.strip = np.zeros(18)
                        self.color = color
                        self.E_0 = 0
                        self.linetype = linetype

                def strip_eloss(self,strip_int):
                        if(self.E <= 0.0):
                                self.E = 0.0
                                return 0.0
                        else:
                                beam_trim = TRIM(target, Ion(self.title, energy=self.E*1.0e6,mass=self.M), number_ions=num_ions, calculation=1)
                                beam_results = beam_trim.run(srim_executable_directory)

                                beam_energy = beam_results.ioniz.ions*100
                                beam_depth = beam_results.ioniz.depth*1e-8

                                f = interp1d(beam_depth,beam_energy, kind='linear')
                                xnew = np.linspace(0.0157,1.57,100)
                                ynew = f(xnew)

                                eloss = integrate.quad(f,0.0157,1.57)[0]

                                self.E = self.E - eloss
                                self.strip[strip_int] = eloss

                        return eloss

                def window_eloss(self):

                        beam_trim = TRIM(window, Ion(self.title, energy=self.E*1.0e6,mass=self.M), number_ions=num_ions, calculation=1)
                        beam_results = beam_trim.run(srim_executable_directory)

                        beam_energy = beam_results.ioniz.ions*100
                        beam_depth = beam_results.ioniz.depth*1e-8
                        print(beam_depth)
                        f = interp1d(beam_depth,beam_energy, kind='linear')
                        xnew = np.linspace(6.00010e-06,6.00000e-04,100)
                        ynew = f(xnew)

                        eloss = integrate.quad(f,6.00010e-06,6.00000e-04)[0]

                        self.E = self.E - eloss

                        return eloss



                def dead_eloss(self):

                        beam_trim = TRIM(dead, Ion(self.title, energy=self.E*1.0e6,mass=self.M), number_ions=num_ions, calculation=1)
                        beam_results = beam_trim.run(srim_executable_directory)

                        beam_energy = beam_results.ioniz.ions*100
                        beam_depth = beam_results.ioniz.depth*1e-8
                        
                        f = interp1d(beam_depth,beam_energy, kind='linear')
                        xnew = np.linspace(0.0230251,2.30251,100)
                        ynew = f(xnew)

                        eloss = integrate.quad(f,0.0230251,2.30251)[0]

                        self.E = self.E - eloss

                        return eloss


                def plot(self):
                        plt.rc('font', family='serif')
                        #		plt.rc('xtick', labelsize=MEDIUM_SIZE)
                        #		plt.rc('ytick', labelsize=MEDIUM_SIZE)

                        strip = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
                        plt.scatter(strip,self.strip, color = self.color,label=self.title)
                        plt.plot(strip,self.strip, color = self.color,ls=self.linetype)
                        plt.xlim(0,18)
                        plt.grid(True)
                        plt.ylabel('Energy Loss (MeV)')
                        plt.xlabel('Strip Number')
                        plt.legend(loc='upper right')

                def plot_bragg(self):

                        target = Target([setlayer(target_gas,gas_pressure,2.8e9)])

                        beam_trim = TRIM(target, Ion(self.title, energy=self.E_init*1.0e6,mass=self.M), number_ions=250, calculation=1)
                        beam_results = beam_trim.run(srim_executable_directory)

                        beam_energy = beam_results.ioniz.ions*100
                        beam_depth = beam_results.ioniz.depth*1e-8

                        f = interp1d(beam_depth,beam_energy, kind='linear')
                        xnew = np.linspace(0.28,28.0,100)
                        ynew = f(beam_depth)

                        plt.plot(beam_depth*0.60714285714,ynew)




############################################################################
############################################################################
############################################################################
############################################################################
        

        target = Target([setlayer(target_gas,gas_pressure,length)])
        dead = Target([setlayer(target_gas,gas_pressure,dead_length)])
        window = Target([setlayer('MYLAR',gas_pressure,windowthick)])
        plt.figure(figsize=(8, 6))

        m1 = particle(m1_name, m1_A, m1_Z, m1_mass, m1_energy,'0.5','dashed') 
        m4 = particle(m4_name, m4_A, m4_Z, m4_mass,      0,   'k','solid')



        window_eloss = m1.window_eloss()
        print(window_eloss)
        dead_eloss = m1.dead_eloss()
        print(dead_eloss)

        reaction_occured = False
        
        for i in range(0,17):
                
                if(i == reaction_strip):

                        m4.E = np.random.uniform(m1.E-1.0,m1.E-9.0)
                        m4.strip[0:reaction_strip] = m1.strip[0:reaction_strip]   

                        #TO IMPLEMENT: Given the energy of m1 at the beginning of this strip, compute the energy and angle for the recoil (m4)
                        #and use that energy to calculate the energy loss!
                        m1.strip_eloss(i)
                        m4.strip_eloss(i)


                        reaction_occured = True 

                elif(reaction_occured == True): 

                        m1.strip_eloss(i)
                        m4.strip_eloss(i)



                elif(reaction_occured == False):
                        m1.strip_eloss(i)



        return window_eloss, dead_eloss, m1.strip, m4.strip


