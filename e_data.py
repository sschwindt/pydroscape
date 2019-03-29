#!/usr/bin/python
import sys, os
import numpy as np

sys.path.append(os.path.dirname(__file__))

from data_processing.create_meta_data import MetaMaker
from data_processing.utilities import *
from data_processing.read_data import GetData
from data_processing.compute import Compute

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
        self.voltage_calibration = np.array(())
        self.p1_solid_discharge = float()
        self.p2_solid_discharge = float()
        self.p1_scale_voltage = float()
        self.p2_scale_voltage = float()

    def calibrate(self, signal_type, p1, *p2):
        # signal_type = STR: either 'voltage', 'solid_q', 'scale_voltage', 'voltage_calibration'
        # p1, p2[0] = LISTs of floats OR FLOATS for y = p1 * x + p2
        if signal_type == 'voltage':
            self.p1_volt = p1
            try:
                self.p2_volt = p2[0]
            except:
                self.p2_volt = [0]
        if signal_type == 'solid_q':
            self.p1_solid_discharge = p1
            try:
                self.p2_solid_discharge = p2[0]
            except:
                self.p2_solid_discharge = 0.0
        if signal_type == 'scale_voltage':
            self.p1_scale_voltage = p1
            try:
                self.p2_scale_voltage = p2[0]
            except:
                self.p2_scale_voltage = 0.0
        if signal_type == 'voltage_calibration':
            self.voltage_calibration = p1

    def launch(self, *args):
        # args[0] = 5-digits STR of experiment number (shape: >> XXXXX )
        # args[1] = INT meta file number to process
        # args[2] = STR of metafile directory, if not yet set.
        try:
            self.no_exp = args[0]
        except:
            self.no_exp = str(input('Please enter the experiment number (STR >> \'XXXXX\') \n>> '))

        try:
            self.no_inp_files = args[1] + 1
        except:
            self.no_inp_files = int(input('Enter the number of input file to process (INT) \n>> ')) + 1

        try:
            self.meta_directory = args[2]
        except:
            self.meta_directory = self.own_dir
        chkFolderStructure(self.own_dir + '/data_processing/.cache')  # unless it already exists, this builds the program cache folder

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
                        try:
                            result.refVal = np.zeros((1, self.p1_volt.__len__()))
                        except:
                            pass
                    except:
                        print('NOTE: No voltage linear transformation parameters p1 and p2 set.')
                        print('       if required, use Launcher().calibrate(\'voltage\', list(p1), list(p2))')
                        print('          consider also to set a \'voltage_calibration\' np.array()')
                    try:
                        result.p1_solid_q = self.p1_solid_discharge
                        result.p2_solid_q = self.p2_solid_discharge
                    except:
                        print('NOTE: No solid_q linear transformation parameters p1 and p2 set.')
                        print('       if required, use Launcher().calibrate(\'solid_q\', float(p1),  float(p2))')
                    try:
                        result.p1_weight_voltage = self.p1_scale_voltage
                        result.p2_weight_voltage = self.p2_scale_voltage
                    except:
                        print('NOTE: No scale voltage linear transformation parameters p1 and p2 set.')
                        print('       if required, use Launcher().calibrate(\'scale_voltage\',  float(p1),  float(p2))')
                    try:
                        result.calibrationVolt = self.voltage_calibration
                    except:
                        print('NOTE: No Voltage calibration defined.')
                        print('      if required, use Launcher().calibrate(\'voltage_calibration\', p1=np.array)')
                        print('      p1 should have the same number of elements as defined for \'voltage\' calibration.')

                    result()
                    Results['file{0}'.format(_fileN)] = result.result
                    print('------------------------------------------------------------------------------')
                    if not data.outDataName.lower() == 'nan':
                        filename = data.outDataName + str(extendDigits(_fileN, 3))
                        writeData(data.outDataPath, filename, result.result)
            print('------------------------------------------------------------------------------')
            print('DATA SUCCESSFULLY PROCESSED.')
        try:
            os.rmdir(self.own_dir + '/data_processing/.cache')
            os.rmdir(self.own_dir + '/data_processing/__pycache__')
        except:
            pass

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



