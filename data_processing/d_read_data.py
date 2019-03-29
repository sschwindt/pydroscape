#!/usr/bin/python
import os
import numpy as np
from d_utilities import *


class GetData(object):
    # This class uses its __call__() method for load the data described in the according MetaDataFile.
    # Instantiate an object by: A = GetData('MetaDataX.txt')
    # The data are read by calling A() and can then be assigned by e.g. B=A.getData() --> l x m x n - matrix
    # l = Number of Files (meas)
    # m = Number of rows in datafiles
    # n = Number of columns in datafiles

    def __init__(self, fN):
        self.inPath = str()
        self.measNa = int()
        self.measNb = int()
        self.measDigits = int()
        self.filePre = str()
        self.fileSuf = str()
        self.fType = str()
        self.delimiter = str()
        self.headLen = str()
        self.dName = str()
        self.nCol = int()
        self.fileName = fN
        self.dataFolder = np.zeros((1, 1, 1), 'float')
        self._maxRows = 0
        self.measNo = 0
        self.counter = 0
        self.cMeth = str()
        self.timestamp = int()
        self.timeext = None
        self.fluid = str()
        self.fluidT = str()
        self.outGraphPath = str()
        self.outGraphName = str()
        self.outDataPath = str()
        self.outDataName = str()
        self.datalength = []

    def __str__(self):
        return 'Meta data file info: %s' % self.fileName

    def assignMetaVariables(self):
        _entries = GetData.readMetaData(self)
        try:
            (self.inPath, self.measNa, self.measNb, self.measDigits, self.filePre, self.fileSuf, self.fType, self.delimiter, self.headLen, self.dName, self.nCol, self.cMeth, self.timestamp, self.timeext, self.fluid, self.fluidT, self.outGraphPath, self.outDataPath, self.outGraphName, self.outDataName) = _entries

            self.measNa = int(self.measNa)
            self.measNb = int(self.measNb)+1
            self.measDigits = int(self.measDigits)
            self.headLen = int(self.headLen)
            self.nCol = int(self.nCol)
            self.timestamp = int(self.timestamp)
            for i in self.timeext:
                if i == '/':
                    self.timeext = str2frac(self.timeext)
                    break
            self.timeext = float(self.timeext)
            if self.delimiter == 'tab':
                self.delimiter = '\t'
            self.fluidT = float(self.fluidT)
            self.cMeth = list(self.cMeth[1:len(self.cMeth) - 1].split(','))

        except ValueError:
            print('Bad assignment of values in MetaData.inp.')
        return()


    def getData(self):
        return self.dataFolder

    def goToData(self):
        os.chdir(self.inPath) 

    def readInputFile(self, fileNo):
        fileNo = extendDigits(fileNo, self.measDigits)  # from f_functions
        if self.measDigits > 0:
            _fileName = self.filePre + fileNo + self.fileSuf + '.' + self.fType
        else:
            _fileName = self.filePre + self.fileSuf + '.' + self.fType
        os.chdir(self.inPath)
        if os.path.isfile(_fileName):
            _f = open(_fileName)
            _data = []  # private list containing data file content
            _count = 0
            for line in _f:
                _count += 1

                if _count <= int(self.headLen):
                    # ignore header lines
                    continue

                _entries = line.split(self.delimiter)

                # convert input data to float
                for j in range(0, self.nCol): 
                    try:
                        if not j == self.nCol:
                            if _entries[j] == '\n':
                                _entries[j] = delNewLine(_entries[j])
                            _entries[j]=float(_entries[j])

                    except ValueError:
                        try:
                            _temp = delNewLine(_entries[j])
                            _entries[j] = str2num(_temp.strip('\n'),',')
                        except ValueError:
                            print('Input is NaN: {0}'.format(_entries[j]))
                _data.append(_entries)
            _res=np.array(_data)
            _count=_count-int(self.headLen)
            print('Reading file '+_fileName+' ...')
            return _res,_count
        else:
            print('There is no file '+_fileName+'. Continue anyway...')
            return 0,0

    def readInputFolder(self):
        _shape = (self.measNo - 1, 1, self.nCol)
        for i in range(self.measNa, self.measNb):
            _iFile, _iRows = self.readInputFile(i)  # read data file
            self.datalength.append(_iRows)
            # enlarge _dataFolder if to fit the data file size if necessary
            if self._maxRows < _iRows:
                _shape = (self.measNo - 1, _iRows, self.nCol)
                _tempArray = self.dataFolder.copy()
                self.dataFolder = np.zeros(_shape, 'float')
                _iTemp = i - 1
                self.dataFolder[:, 0:self._maxRows:1, :] = _tempArray
                self._maxRows = _iRows

            if not (_iRows == 0):
                fileNo = i - self.measNa
                self.dataFolder[fileNo, 0:_iRows:1, :] = _iFile

        return self.dataFolder

    def readMetaData(self):
        _f = open(self.fileName)    # open file
        _entries = []
        for line in _f:
            if line[0] == '#':
                continue
            # PARSE RELEVANT INFORMATION
            __temp = line.split('= ')
            __temp = __temp[1]
            __temp = __temp.split(' #')
            _entries.append(__temp[0])
        _f.close()
        return _entries

    def __call__(self, metaPath):
        os.chdir(metaPath)
        self.assignMetaVariables()  # read in MetaData
        os.curdir = metaPath
        print(os.curdir)
        self.goToData()
        if type(self.measNb) == int:
            self.measNo = self.measNb - self.measNa + 1
            _shape = (self.measNo - 1, 1, self.nCol)

        else:
            self.nCol = int(self.nCol)
            _shape = (1, self.nCol)

        self.dataFolder = np.zeros(_shape, 'float')
        self.goToData()
        self.readInputFolder()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.curdir = os.path.dirname(os.path.abspath(__file__))
        return self.dataFolder







