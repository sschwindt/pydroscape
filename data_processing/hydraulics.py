#!/usr/bin/python
import sys, os
import numpy as np
sys.path.append(os.path.dirname(__file__))
from utilities import *

class Hydraulics(object):
    def __init__(self, fluidT, nCol):
        self.h = []     # [m] water depth
        self.Fr = []    # [-] Froude number
        self.A = []     # [m2] surface of water cross section
        self.P = []     # [m] wetted perimeter of water surface
        self.Rh = []    # [m] hydraulic radius
        self.Q = []     # [m3/s] liquid discharges
        self.u = []     # [m/s] flow velocity
        self.kst = 0.   # [m1/3 / s] Strickler coefficient
        self.info = []  # list containing information about data column to be treated
        self.g = 9.80665  # [m/s2] gravity acceleration
        self.nu = (1.14 - 0.031 * (fluidT - 15) + 0.00068 * (fluidT - 15) ** 2) * 10 ** -6  # [m2/s] fluid viscosity by Julien 2002
        self.rhof = 1000 # [kg/m3] fluid density
        self.rhos = 2680 # [kg/m3] sediment density
        self.w = 0.      # [m] flume width
        self.beta = 0.   # [deg] flume bank slope
        self.J = 0.      # [-] channel slope
        self.columnNames = []
        self.nCol = nCol
        print('Info: fluid density pre-defined by rhof = {0} [kg/m3] and sediment density by rhos = {1} [kg/m3]'.format(self.rhof,self.rhos))
        self.callInfo = {'getQ' : self.getQ,
                         'getH' : self.getH,
                         'getU' : self.getU}
        self.ctrlCols = 0 # necessary for naming columns
        self.colDict = {0: 'flow depth [m]', 1: 'flow velocity [m/s]', 2: 'Froude number [-]'}
        self.resultMatrix = self.data

    def cacheInformation(self):
        if chkIsCacheFile('flowParameters'):
            self.kst, self.J, _col,_ask = getUsrSettings('flowParameters')
            self.kst = float(self.kst.strip())
            self.J = float(self.J.strip())
            _col = int(_col)
            try:
                _ask = int(_ask)
                print('Flow depth is known and will be loaded form input data file column No. {0}'.format(_ask))
            except ValueError:
                print('Flow depth is unknown and will be interpolated...')
            print('Found existing boundary values from recent computation. Applying kst = {0}, J = {1} and load discharges series from input data column {2}.'.format(self.kst,self.J,_col))


        else:
            self.kst = float(input(prompt='Please enter roughness coefficient kst [m1/3 / s] :\n  >> '))
            self.J = float(input(prompt='Please enter channel slope J[-]:\n  >> '))
            _col = input(prompt='Please enter the data column with discharge series:\n  >> ')
            _ask = input(prompt='If the flow depth is known, enter its column in input data, else enter n:\n  >> ')
            saveUsrSettings('flowParameters', [self.kst, self.J, _col, _ask])

        self.Q = np.array(self.data[:, _col])
        # # for implementation of back-calculating discharges, uncomment the following lines
        #_ask = input('Are the discharges Q [m3/s] known (enter y/n)?:\n  >> ')
        #self.callInfo[getQ](_ask)

        self.callInfo['getH'](_ask)
        self.callInfo['getU']()

    def froude(self, *args):
        self.cacheInformation()
        for i in range(0, len(self.h) - 1):
            self.Fr.append(self.u[i] / np.sqrt(self.g * self.h[i]))
        self.makeColumnNames(2)
        self.makeResultMatrix(self.h)
        results = setDataHeaders(self.resultMatrix, self.columnNames)
        return results

    def getH(self, *args):
        if not args == 'y':
            if not chkIsCacheFile('channelGeometry'):
                self.w = float(input(prompt='Please enter the flume width w [m]:\n  >> '))
                self.beta = float(input(prompt='Please enter the bank slope [deg]:\n  >> '))
                _col = 0
                saveUsrSettings('channelGeometry', [self.w, self.beta, _col])
            else:
                self.w, self.beta, _col = getUsrSettings('channelGeometry')
                self.w = float(self.w.strip())
                self.beta = float(self.beta.strip())
                _col = int(_col)
            _n = self.kst**(-1/3)  # [-] Manning coefficient
            _m = 1/np.tan(np.radians(self.beta))
            for i in range(0, len(self.Q)):
                _err = 1
                _count = 1
                self.A.append(0)
                self.P.append(0)
                self.h.append(1)
                self.Rh.append(0)
                # use Raphson-Newton Algorithm for interpolation of flow depth
                while _err > 0.0001:
                    self.A[i] = self.w * self.h[i] + _m * self.h[i] ** 2
                    self.P[i] = self.w + 2 * self.h[i] * np.sqrt(_m ** 2 + 1)
                    dA_dh = self.w + 2 * _m * self.h[i]  # correction factor for flow cross section
                    dP_dh = 2 * np.sqrt(_m ** 2 + 1)  # correction factor for wetted perimeter
                    _Q = self.A[i] ** (5 / 3) * np.sqrt(self.J) / (_n * self.P[i] ** (2 / 3))
                    _f = _n * self.Q[i] * self.P[i] ** (2 / 3) - self.A[i] ** (5 / 3) * np.sqrt(self.J)  # correction factor
                    df_h = 2 / 3 * _n * self.Q[i] * self.P[i] ** (-1 / 3) * dP_dh - 5 / 3 * self.A[i] ** (2 / 3) * np.sqrt(self.J) * dA_dh
                    self.h[i] = np.abs(self.h[i] - _f / df_h)  # compute new value for flow depth
                    _err = np.abs(self.Q[i] - _Q) / self.Q[i]
                    print('Flow depth interpolation step No.{0} (error = {1})'.format(_count,_err))
                    _count += 1
                    if _count > 25:
                        print('Flow depth interpolation break at an error value of {0}.'.format(_err))
                        break
                self.A[i] = self.w*self.h[i]+_m*self.h[i]**2
                self.P[i] = self.w+2*self.h[i]*np.sqrt(_m**2+1)
        else:
            if not chkIsCacheFile('channelGeometry'):
                _col = input('Please enter the data column with flow depth series:\n  >> ')
                saveUsrSettings('channelGeometry', [self.w, self.beta, _col])
            self.h = self.data[:, _col]
        self.makeColumnNames(0)
        self.makeResultMatrix(self.h)
        self.A = np.array(self.A)
        self.P = np.array(self.P)

    def getQ(self, _ask):
        if _ask == 'y':
            _col = input('Please enter the data column with discharge series:\n  >> ')
            self.Q = np.array(self.data[:, _col])
        else:
            print('Code currently requires values for discharges...')

    def getU(self):
        for i in range(0, len(self.h)):
            self.u.append(self.Q[i] / self.A[i])
        self.makeColumnNames(1)
        self.makeResultMatrix(self.u)

    def makeColumnNames(self, *args):
        if not self.ctrlCols == 1:
            for i in range(0, self.nCol+1):
                self.columnNames.append('InputCol.' + str(i))
            self.ctrlCols = 1
        self.nCol += 1
        self.columnNames.append(self.colDict[args[0]])

    def makeResultMatrix(self, *resultCol):
        _nRows, _nCols = self.resultMatrix.shape
        try:
            resultCol = np.array(resultCol)
            resultCol = resultCol.transpose()
        except ValueError:
            print('Invalid result data.')
        _shape = (_nRows, _nCols+1)
        _temp = self.resultMatrix.copy()
        self.resultMatrix = np.zeros(_shape)
        self.resultMatrix[:, 0:_nCols] = _temp
        self.resultMatrix[:, _nCols:] = resultCol

















