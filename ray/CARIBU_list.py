#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 18:24:30 2018

@author: ray
"""

import matplotlib.pyplot as plt
#import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import matplotlib.patches as patches
from numpy import *

#############################################
''' CARIBU '''

CARIBU_file = '/Users/ray/UManitoba/ANL/CPT/PTable and Nuclear Chart/CARIBU_list_2.txt'

CARIBU_Z = genfromtxt(CARIBU_file, usecols = 0)
CARIBU_A = genfromtxt(CARIBU_file, usecols = 1)
CARIBU_N = genfromtxt(CARIBU_file, usecols = 2)
CARIBU_Y = genfromtxt(CARIBU_file, usecols = 3)
CARIBU_Yerr = genfromtxt(CARIBU_file, usecols = 4)

#############################################
x = CARIBU_N 
y = CARIBU_Z 
c = CARIBU_Y 
#############################################

magicZ = [2,8,20,28,50,82,126]
magicN = [2,8,20,28,50,82,126]

#############################################
#############################################

X,Y  = meshgrid(x,y)
#C = vstack((c, c)).T
C = outer(c.T, c)

#combined = vstack((x, y)).T
#C = vstack((c, c)).T

#c = griddata(x,y,z,xmesh,ymesh, interp='linear')

#N = sqrt(len(x)) # Only if squared, adjust accordingly
#x = x.reshape((N, N))
#y = y.reshape((N, N))
#c = c.reshape((N, N))
#pcolormesh(x, y, c)



f = plt.figure()#figsize = (6,10))
ax = f.add_subplot(111, aspect = 'equal')


plt.pcolormesh(X,Y,C,cmap = 'viridis') 
#plt.pcolor(X,Y,C,cmap = 'viridis') 

#plt.pcolormesh(x, y, c, cmap = 'viridis')

#plt.pcolormesh(combined,C,cmap = 'viridis') 

plt.colorbar()


#ax.plot(CARIBU_N, CARIBU_Z, marker='s', markersize = 10, linestyle = None, linewidth = 0)#, color='blue')    

[ax.axhline(_y, linewidth=5, color='k', alpha = 0.2) for _y in magicZ[3:6]]
[ax.axvline(_x, linewidth=5, color='k', alpha = 0.2) for _x in magicN[4:7]]


plt.xlabel('Neutrons (N)')
plt.ylabel('Protons (Z)')

plt.xlim(25,130)
plt.ylim(20,80)

plt.grid()
plt.show()


