#!/usr/bin/python
# Filename: tsMain.py
# Desc.: Computation of solid discharge
#        > Based on HEC-RAS computation
#          > Header definition of HEC-RAS file:
#            REACH[1-name] RIVERsTA[2-m] PROFILE[3-Qname] QtOTAL[4m3s] MINcHeL[5-m]
import sys, os

# import own functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/sediment_transport/')
from sediment_transport.sed_calculator import *

class SedimentTransport1D:
    def __init__(self, *args):
        # args[0] = silence (bool True / False=default)
        try:
            silence = args[0]
        except:
            silence = False
        if not silence:
            print('Welcome message from e_sed1d.SedimentTransport1D():')
            print('Start analysis with e_sed1d.SedimentTransport1D.calculate(method).')
            print('Valid methods are: \'AW\', \'AWmod\', \'MPM\', \'Rec13\'.')
        
        self.input_file_dir = os.path.dirname(os.path.abspath(__file__)) + '/'
        self.output_file_dir = os.path.dirname(os.path.abspath(__file__)) + '/'
            
    def calculate(self, method):
        try:
            calculation_container = MethodContainer(method, self.input_file_dir, self.output_file_dir)
        except:
            print('INVALID INPUT DATA AND/OR FORMULA (METHOD).')
            print('Valid methods are: \'AW\', \'AWmod\', \'MPM\', \'Rec13\'.')
        try:
            calculation_container()
        except:
            print('Error: Calculation failed.')
            
    def set_input_file_directory(self, new_dir):
        # new_dir = STR of input directory
        self.input_file_dir = new_dir
        
    def set_output_file_directory(self, new_dir):
        # new_dir = STR of input directory
        self.output_file_dir = new_dir  
            
    def __call__(self):
        print('Valid methods are: \'AW\', \'AWmod\', \'MPM\', \'Rec13\'.')
        method = str(input('Please enter solid transport formula (AW, AWmod, MPM, Rec13) \n>> '))
        self.calculate(method)
