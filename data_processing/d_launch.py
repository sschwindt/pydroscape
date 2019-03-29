#!/usr/bin/python
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from d_create_meta_data import MetaMaker
from d_utilities import *
from d_read_data import GetData
from d_compute import Compute

class Launcher:
    def __init__(self, *args):
        # args[0] = silence (bool True / False=default)
        try:
            silence = args[0]
        except:
            silence = False
        if not silence:
            print('Welcome message from e_data.Launcher():')
            print('If any input file is not yet defined, run Launcher.make_meta_file(meta_directory).')
            print('Start analysis with e_data.Launcher.launch(*args).')
        self.no_exp = str()
        self.no_inp_files = int()
        self.own_dir = os.path.dirname(os.path.abspath(__file__))
        self.meta_directory = str()
        self.p1_volt = []
        self.p2_volt = []
        self.p1_solid_discharge = float()
        self.p2_solid_discharge = float()
        self.p1_scale_voltage = float()
        self.p2_scale_voltage = float()

    def calibrate(self, signal_type, p1, p2):
        # signal_type = STR: either 'voltage', 'solid_q', 'scale_voltage'
        # p1, p2 = LISTs of floats OR FLOATS for y = p1 * x + p2
        if signal_type == 'voltage':
            self.p1_volt = p1
            self.p2_volt = p2
        if signal_type == 'solid_q':
            self.p1_solid_discharge = []
            self.p2_solid_discharge = []
        if signal_type == 'scale_voltage':
            self.p1_scale_voltage = []
            self.p2_scale_voltage = []

    def launch(self, *args):
        # args[0] = 5-digits INT of experiment number (shape: >> XXXXX )
        # args[1] = INT meta file number to process
        # args[2] = STR of metafile directory, if not yet set.
        try:
            self.no_exp = args[0]
        except:
            self.no_exp = str(input('Please enter the experiment number (shape: >> XXXXX ) \n>> '))

        try:
            self.no_inp_files = args[1]
        except:
            self.no_inp_files = int(input('Enter the number of input file to process \n>> ')) + 1

        try:
            self.meta_directory = args[2]
        except:
            self.meta_directory = self.own_dir
        chkFolderStructure(self.own_dir + '/.cache')  # unless it already exists, this builds the program cache folder

        for i in range(1, self.no_inp_files):
            # READ DATA
            # os.chdir(os.path.dirname(os.path.abspath(__file__)))
            os.chdir(self.meta_directory)
            MetaDataFile = ('MetaData{0}.inp'.format(i))

            # Read Input Data according to MetaDataX.inp
            data = GetData(MetaDataFile)
            os.chdir(self.own_dir)
            data(self.meta_directory)
            print('------------------------------------------------------------------------------')
            print('END OF DATA INPUT.')

            # DATA PROCESSING
            Results = {}
            for _fileN in range(1, data.measNo):
                if not chkData(data.dataFolder[_fileN - 1, :, :]) == 0:
                    result = Compute(data.dataFolder[_fileN - 1, :, :], data.cMeth, data.timestamp, data.timeext,
                                     data.fluidT, data.nCol, data.datalength, _fileN - 1)
                    try:
                        result.p1_volts = self.p1_volt
                        result.p2_volts = self.p2_volt
                    except:
                        print('WARNING: Could not set voltage linear transformation parameters p1 and p2.')
                        print('         use Launcher().calibrate(\'voltage\', p1=LIST, p2=LIST)')
                    try:
                        result.p1_solid_q = self.p1_solid_discharge
                        result.p2_solid_q = self.p2_solid_discharge
                    except:
                        print('WARNING: Could not set solid_q linear transformation parameters p1 and p2.')
                        print('         use Launcher().calibrate(\'solid_q\', p1=LIST, p2=LIST)')
                    try:
                        result.p1_weight_voltage = self.p1_scale_voltage
                        result.p2_weight_voltage = self.p2_scale_voltage
                    except:
                        print('WARNING: Could not set scale voltage linear transformation parameters p1 and p2.')
                        print('         use Launcher().calibrate(\'scale_voltage\', p1=LIST, p2=LIST)')
                    result()
                    Results['file{0}'.format(_fileN)] = result.result
                    print('------------------------------------------------------------------------------')
                    if not data.outDataName.lower() == 'nan':
                        filename = data.outDataName + str(extendDigits(_fileN, 3))
                        writeData(data.outDataPath, filename, result.result)
            print('------------------------------------------------------------------------------')
            print('DATA SUCCESSFULLY PROCESSED.')

    def make_meta_file(self, meta_dir):
        self.meta_directory = meta_dir
        make_meta = MetaMaker()
        make_meta(meta_dir)





#     else:
#         # empty cache
#         ScriptDir = os.path.dirname(os.path.abspath(__file__))  # get base working directory of script
#         os.chdir(ScriptDir+'\\cache')
#         cacheFiles = os.listdir()
#         os.chdir(ScriptDir)
#         for i in cacheFiles:
#             cacheRemove(i)
#         print('Cache deleted.')



