#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 18:24:30 2018

@author: ray and jacob 
"""

import matplotlib.pyplot as plt
#import numpy as np
import matplotlib.colors
import matplotlib.cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np 
 # import seaborn as sns

print( matplotlib.__version__ )
 

CARIBU_file = './CARIBU_list_2.txt'

Z_list, N_list, cf_yield_list = np.genfromtxt( CARIBU_file, skip_header = 1,
                                               usecols = [ 0, 2, 3 ], unpack = 1 )

Z_list = Z_list.astype( int )
N_list = N_list.astype( int ) 

magicZ = [2,8,20,28,50,82,126]
magicN = [2,8,20,28,50,82,126]


# Z = np.arange( 0, 126 )
# N = np.arange( 200 )

cf_yields = np.zeros( ( 118, 200 ) )
cf_yields[:] = np.nan

cf_yields[ Z_list, N_list ] = cf_yield_list
tmp = np.copy( cf_yields )
tmp[ tmp ==0 ] = np.nan 

# print( Z_list - 1 ) 

f = plt.figure( figsize = ( 10, 6 ) ) 

ax = plt.axes()

ax.set_title( '$^{252}$Cf fission yield', fontsize = 20 )
ax.set_ylabel( 'Z', fontsize = 18 )
ax.set_xlabel( 'N', fontsize = 18 ) 

print( np.nanmin( tmp ) ) 


masked_array = np.ma.array( cf_yields, mask=np.isnan( cf_yields ) )
cmap = matplotlib.cm.jet
cmap.set_bad( 'white', 1.0 )

# im = ax.imshow( masked_array, origin = 'lower', aspect = 'auto',
#                 cmap = cmap, 
#                 norm = matplotlib.colors.LogNorm( vmin = np.nanmin( tmp ),
#                                                   vmax = np.nanmax( tmp ) ) )


im = ax.imshow( masked_array, origin = 'lower', aspect = 'auto',
                cmap = cmap, 
                norm = matplotlib.colors.LogNorm( vmin = np.nanmin( tmp ),
                                                  vmax = np.nanmax( tmp ) ) )
# ticks = None ) 

divider = make_axes_locatable( ax )
cax = divider.append_axes("right", size="5%", pad=0.2)
cbar = f.colorbar(im, cax=cax, format='%.2f')
cbar.set_label( '$^{252}$Cf yields (per 100 fissions)', rotation = 270 ) 


ax.set_xlim( ( 25, 120 ) )
ax.set_ylim( ( 20, 75 ) ) 

# <<<<<<< HEAD
#ax.set_xticklabels( np.array( ax.get_xticklabels(), dtype = int ) + 1 ) 
# =======
# >>>>>>> 765b534c003bcdd8168ba017880b3d7cb4f4eef5

for i in range( 3, 6 ) :
    ax.axhline( magicZ[i], linewidth=5, color='k', alpha = 0.2 )

for i in range( 4, 7 ) :
    ax.axvline( magicN[i], linewidth=5, color='k', alpha = 0.2 )  


plt.show() 



