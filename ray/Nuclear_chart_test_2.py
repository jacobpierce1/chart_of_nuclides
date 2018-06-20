#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 18:24:30 2018

@author: ray
"""

import matplotlib.pyplot as plt
#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from numpy import *


#############################################
'''AME'''

amefile = '/Users/ray/UManitoba/ANL/CPT/Data_Analysis/PI-ICR/ame_all_masses.txt'

ameN = genfromtxt(amefile, usecols = 0)
ameZ = genfromtxt(amefile, usecols = 1)
ameA = genfromtxt(amefile, usecols = 2)
ameEl = genfromtxt(amefile, usecols = 3, dtype = str)
mass = genfromtxt(amefile, usecols = 4)
mass_err = genfromtxt(amefile, usecols = 5)

#############################################

#############################################
''' Element List '''

listZ = list(set(ameZ))
listEl = []
ameZ_l = ameZ.tolist()

for i in range(len(listZ)):
    k = ameZ_l.index(listZ[i])
    listEl.append(ameEl[k])


#############################################

magicZ = [2,8,20,28,50,82,126]
magicN = [2,8,20,28,50,82,126]

#############################################
#############################################
''' does not display Z-s on the left y axis ''' 

f = plt.figure(figsize = (60,100))
ax = f.add_subplot(111, aspect = 'equal')


ax.plot(ameN, ameZ, color='blue', marker='s', markersize = 10, linestyle = None, linewidth = 0)    


[ax.axhline(_y, linewidth=10, color='k', alpha = 0.3) for _y in magicZ[3:6]]
[ax.axvline(_x, linewidth=10, color='k', alpha = 0.3) for _x in magicN[4:7]]

#ax.set_xlabel('Neutrons (N)')
#ax.set_ylabel('Protons (Z)')

plt.xlabel('Neutrons (N)')
plt.ylabel('Protons (Z)')

ax.yaxis.tick_right()
plt.yticks(listZ, listEl)

plt.grid()
plt.show()


#############################################
''' 2 y-s not the same scale '''    

fig, ax1 = plt.subplots(1, figsize=(50,30))

ax1.plot(ameN, ameZ, 's')
[ax1.axhline(_y, linewidth=4, color='k', alpha = 0.5) for _y in magicZ[3:6]]
[ax1.axvline(_x, linewidth=4, color='k', alpha = 0.5) for _x in magicN[4:7]]

ax1.set_xlabel('N')
ax1.set_ylabel('Z')

ax2 = ax1.twinx()

plt.yticks(listZ, listEl)


fig.tight_layout()
plt.grid()
plt.show()

#############################################
#############################################


