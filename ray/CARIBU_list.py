#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 18:24:30 2018

@author: ray
"""

import matplotlib.pyplot as plt
#import numpy as np
import matplotlib.pyplot as plt
import numpy as np 


CARIBU_file = './CARIBU_list_2.txt'

Z_list, N_list, cf_yield_list = np.genfromtxt( CARIBU_file, skip_header = 1,
                                               usecols = [ 0, 2, 3 ], unpack = 1 )

Z_list = Z_list.astype( int )
N_list = N_list.astype( int ) 

magicZ = [2,8,20,28,50,82,126]
magicN = [2,8,20,28,50,82,126]


# Z = np.arange( 0, 126 )
# N = np.arange( 200 )

cf_yields = np.zeros( ( 126, 200 ) )

cf_yields[:] = np.nan

cf_yields[ Z_list - 1, N_list - 1 ] = cf_yield_list 

print( Z_list - 1 ) 

f = plt.figure( figsize = ( 8, 8 ) ) 

ax = plt.axes()

ax.set_title( 'My Chart of Nuclides' )
ax.set_xlabel( 'Z' )
ax.set_ylabel( 'N' ) 

ax.imshow( cf_yields.T[ :140, :90 ], origin = 'lower', aspect = 'auto' ) 


for i in range( 3, 6 ) :
    ax.axhline( magicZ[i], linewidth=5, color='k', alpha = 0.2 )

for i in range( 4, 7 ) :
    ax.axvline( magicN[i], linewidth=5, color='k', alpha = 0.2 )  


plt.show() 



