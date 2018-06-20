# TITLE: CPT contaminant identifier
# AUTHOR: jacob pierce, Argonne National lab
# DATE: 4.27.18
#
# DESCRIPTION: given the cyclotron frequency of something measured in
# the CPT (or elsewhere), CPT, determine all possible nuclides or
# molecules that could produce that cyclotron frequency.

# all masses are given in 10^6 AMU. all frequencies are measured in
# Hz.  charges are measured in units of electron charge


import numpy as np
import sys
import pandas as pd
import os
import pickle
import itertools
import time
import re
import datetime
import sqlite3
from molecule_parser import atom_counter



# define this for database debug
DEBUG_DB = 0



# from periodic_table_dict import get_periodic_table_dict

molecule_db_dir = './storage/'
molecule_db_schema_path = './molecule_db_schema.sql'


ame16_data_path = './data/ame16_all_masses_accurate.txt'
nubase2016_data_path = './data/nubase2016_raw.txt'
wikipedia_molecule_data_path = './data/molecules/wikipedia_molecule_data.txt'
carbon_molecule_data_dir = './data/molecules/carbon_molecules/'
carbon_file_name = 'C'
wallet_card_path = './data/nuclear-wallet-cards.txt'
fission_yield_data_path = './data/fissionyields.txt' 
abundances_path = './data/abundances.txt'




class __nuclide_db( ) :

    def __init__( self ) :

        self.periodic_table_dict = self.get_periodic_table_dict()

        self.masses = self.get_atom_masses()

        self.half_lives = self.get_half_life_data()

        self.rel_abundances = self.get_rel_abundances() 



    def get_periodic_table_dict() :

        periodic_table_string = '''h he
        li be b c n o f ne
        na mg al si p s cl ar
        k ca sc ti v cr mn fe co ni cu zn ga ge as se br kr
        rb sr y zr nb mo tc ru rh pd ag cd in sn sb te i xe
        cs ba la ce pr nd pm sm eu gd tb dy ho er tm yb lu hf ta w re os ir pt au hg tl pb bi  po at rn
        fr ra ac th pa u np pu am cm bk cf es fm md no lr rf db sg bh hs mt ds rg cn nh fl mc lv ts og'''

        keys = periodic_table_string.split() 

        tmp = dict( zip( keys, range( 1, 119 ) )  )

        tmp[ 'd' ] = 1 

        return tmp 





    def get_atom_masses() :

        atom_masses = np.zeros( ( max_Z, max_N ) )

        # default value 
        atom_masses[:] = -1 

        # parse the ame16 data. this only has ground state masses. 

        with open( ame16_data_path ) as f :

            # skip first line 
            f.readline()

            for line in f.readlines() :

                data = line.split( '\t' )
                Z = int(data[1])
                N = int(data[0])

                name = data[3] 
                mass = float( data[4] )

                atom_masses[Z,N] = mass

        return atom_masses 









    def get_rel_abundances_data() :

        abundances = np.zeros( ( 126, 250 ) )

        current_Z = 0

        skiplines = 0 

        with open( abundances_path ) as f :

            for line in f.readlines() :

                if skiplines < 3 :
                    skiplines += 1
                    continue

                line = line.split()

                # print( line ) 

                # if( not line or len( line ) < 4 or not( line[0].isdigit() ) ) :
                #     continue

                if line[0].isdigit() and line[1].isalpha() :
                    Z_idx = 0 
                    Z = int( line[0] )
                    current_Z = Z
                    min_len = 5

                else :
                    Z_idx = -2 
                    Z = current_Z
                    min_len = 3 

                if len( line ) < min_len :
                    continue

                A = int( line[ 2 + Z_idx ] )
                abund = line[ 4 + Z_idx ]

                if '[' in abund :
                    continue

                parenth_idx = abund.find( '(' )
                if parenth_idx != -1 :
                    abund = float( abund[ : parenth_idx ] )

                # print( abund ) 

                N = A - Z

                # print( line )
                # print( Z, N )
                # print( abund ) 

                abundances[Z,N] = abund

        return abundances



    def str_is_int( s ) :
        try: 
            int(s)
            return True
        except ValueError:
            return False


    

    # def get_cf_yield_data() :

    #     cf_yields = np.zeros( ( 126, 200 ) )

    #     with open( fission_yield_data_path ) as f :

    #         for line in f.readlines() :

    #             line = line.split()

    #             if( not line ) :
    #                 continue

    #             element_string = line[0]
    #             A, element_name  = re.findall( r'(\d*)([A-Z][a-z]*)', element_string )[0]
    #             A = int( A )
    #             Z = periodic_table_dict[ element_name.lower() ]
    #             N = A - Z 

    #             fission_yield = float( line[-2] ) / 200
    #             cf_yields[ Z, N ] = fission_yield

    #     return cf_yields 








    def get_half_life_data() :

        half_lives = np.zeros( ( 126, 200 ) )

        with open( wallet_card_path ) as f :

            for full_line in f.readlines()  :

                line = full_line.split()

                if 'STABLE' in full_line :
                    half_life = np.inf

                else :
                    try : 
                        half_life = float( line[-1] )
                    except:
                        continue

                if has_digit( line[0] ) :
                    A_idx = 0

                else :
                    A_idx = 1

                # can't currently handle excited states. 
                if not line[ A_idx ].isdigit() :
                    continue

                else : 
                    A = int( line[ A_idx ] ) 

                Z = int( line[ A_idx + 1 ] ) 

                # this denotes a metastable state
                # A = string_to_numstring( line[0] )
                # if A == '' :
                #     A = int( string_to_numstring( line[ 1 ] ) ) 
                #     Z = int( line[ 2 ] )

                # else :
                #     A = int( A )
                #     Z = int( line[1] ) 

                N = A - Z


                # if Z == 9 :
                #     print( full_line )
                #     print( N ) 
                #     print( half_life ) 

                half_lives[ Z, N ] = half_life


        return half_lives





    def string_to_numstring( s ) :
         return ''.join( [ c for c in s if c.isdigit() ] )


    def has_digit( s ) :
        for c in s :
            if c.isdigit() :
                return 1
        return 0 

                   
                   
    
    # # the cyclotron frequency is qB/m

    # def mass_to_omega( mass, q ) :
    #     omega = q * cesium_133_omega * ( cesium_133_mass - electron_mass ) / mass 
    #     return omega


    # def omega_to_mass( omega, q ) :
    #     return q * cesium_133_omega * ( cesium_133_mass - electron_mass ) / omega 



    def file_len( fname ):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1




    def get_element_name( Z ) :

        try :
            return next( key for key, value in periodic_table_dict.items() if value == Z )

        except :
            print( 'ERROR: no element name for Z = %s' % str( Z ) )
            sys.exit( 0 )
    

        



