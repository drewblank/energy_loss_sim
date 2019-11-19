#!/usr/bin/env python
############################################################################    
# Drew Blankstein 
# University of Notre Dame
# 
# Generate Reaction calculates the kinematics of 2 body elastic and 
# inelastic scattering reactions with the options to plot E_lab VS E_angle
# as well as E_com vs E_com for both the heavy recoil and the ER given 
# the projectile energy
############################################################################ 

import sys
import os
import random
import math

import matplotlib.pyplot as plt
import numpy as np 
import matplotlib.mlab as mlab




#def generate_reaction(m1,m2,m3,m4): 
MeVMass = 938.0
pi = np.pi

m1_energy = 20

m1 = 12.0
m2 = 12.0
m3 = 15.994914
m4 = 8.01

#theta = np.linspace(0,pi,1000)
theta = np.random.uniform(0,pi/2.0)
#calculate some basic properties here 
q_value = (m1 + m2 - m3 - m4)*MeVMass


p_0 = np.sqrt(2*m1*m1_energy)

a = 1.0 + m4/m3 
b = -1.0*(2.0*p_0*np.cos(theta))
c = p_0**2.0 - 2*m4*m1_energy


p_2pl = (-1.0*b + np.sqrt(b**2.0 - 4.0*a*c))/(2.0*a)
p_2mi = (-1.0*b - np.sqrt(b**2.0 - 4.0*a*c))/(2.0*a)

E_2pl = (p_2pl**2.0)/(2.0*m3)
E_2mi = (p_2mi**2.0)/(2.0*m3)

print(np.rad2deg(theta))
print(E_2pl)
#plt.plot(np.rad2deg(theta),E_2pl)
#plt.plot(np.rad2deg(theta),E_2mi)


plt.show()













"""
max_angle = np.arcsin(np.sqrt(m4/m3 * (m2/m1 - q_value/m1_energy * (1+m2/m1))))
print(np.rad2deg(max_angle))

m3_Eplus = ((np.sqrt(m1*m3*m1_energy)*np.cos(theta) + np.sqrt(m1*m3*m1_energy*(np.cos(theta)**2) + (m1+m2)*(m4*q_value +(m4-m1)*m1_energy)))/(m1+m2))**2
m3_Eminus = ((np.sqrt(m1*m3*m1_energy)*np.cos(theta) - np.sqrt(m1*m3*m1_energy*(np.cos(theta)**2) + (m1+m2)*(m4*q_value +(m4-m1)*m1_energy)))/(m1+m2))**2

print(m3_Eplus)
print(m3_Eminus)
"""



"""
plt.plot(np.rad2deg(theta),m3_Eplus)
plt.plot(np.rad2deg(theta),m3_Eminus)

plt.show()
"""

#	return 





