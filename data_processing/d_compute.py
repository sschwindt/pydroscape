#!/usr/bin/python
import numpy as np
import sys, os
sys.path.append(os.path.dirname(__file__))

from d_utilities import *
from d_manipulate import Manipulate
from d_hydraulics import Hydraulics


class Compute(Manipulate, Hydraulics):
    # This class inherits all computation methods
    # self.options is a dictionary for all functions available --> callable functions must be included here
    # __call__() method invokes all computation methods from cMeth.
    # Instantiate an object by: A = Compute()

    def __init__(self, data, cMeth, timestamp, timeext, fluidT, nDataCols, datalength, fileN):
        self.cMeth = cMeth
        self.nCols = []
        Manipulate.__init__(self, data, timestamp, timeext, datalength, fileN)
        Hydraulics.__init__(self, fluidT, nDataCols)
        self.options = {'convertpumpdischarges': self.convertPumpDischarges,
                        'convertsoliddischarges': self.convertSolidDischarges,
                        'froude': self.froude,
                        'ultrasondstodepth': self.ultrasondsToDepth,
                        'ultrasondstometer': self.ultrasondsToMeter}

        self.result = np.array((1, 1))

    def checkAddInfo(self, _method):
        print('Applying method', _method.upper())
        if _method == 'sort':
            if not chkIsCacheFile('sortSettings'):
                self.nCols.append(int(input(prompt='Enter the column with sorting labels for x values (standard = 0 - if not sure, enter n):\n>> ')))
                self.nCols.append(int(input(prompt='Enter the column with sorting labels for z values (standard = 1 - if not sure, enter n):\n>> ')))
                self.nCols.append(int(input(prompt='Enter the column with data to sort (standard = 2 - if not sure, enter n):\n>> ')))
                self.nCols.append(int(input(prompt='Do you want to normalize the axis (1=yes/0=no - standard = 1):\n>>')))
                self.nCols = chkInteger(self.nCols)
                saveUsrSettings('sortSettings', self.nCols)

            else:
                print('Applying existing sort settings.')
                self.nCols = getUsrSettings('sortSettings')

            self.result = self.options[_method](self.nCols)
        else:
            self.result = self.options[_method]()


    def __call__(self):
        for _str in self.cMeth:
            _method = _str.strip('\'')
            self.checkAddInfo(_method.lower())





