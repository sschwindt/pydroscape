#!/usr/bin/python
import os
import numpy as np
from d_utilities import *


class Manipulate(object):
    # This class offers functions for manipulating data (object)
    # __call__() method does ???.
    # Instantiate an object by: A = Manipulate(???)
    # SORT: if there is no *ncol identifier, SORT uses by default object columns 1, 2 and 3
    def __init__(self, data, timestamp, timeext, datalength, fileN):
        self.data = np.array(data)
        self.fileN = fileN
        self.datalength = datalength
        self.timestamp = timestamp
        self.timeext = timeext
        # necessary to normalize actual probe voltage with calibration voltage
        # UNCOMMENT AND ADAPT !!
        self.calibrationVolt = np.array((float, float, float, float, float))
        self.refVal = np.zeros((1, 5))  # stock multiplier due to first US probe measurement (ref. calib.)
        self.p1_solid_q = float
        self.p2_solid_q = float
        self.p1_weight_voltage = float
        self.p2_weight_voltage = float
        self.p1_volts = []
        self.p2_volts = []

    def __str__(self):  # converts the data stack to string
        return self.data.__str__()

    def convertPumpDischarges(self):
        # creation of data array of size (data_length-timestamp x 2)
        # assumes that a measurement is made every three seconds
        # and that the discharge values are in the fifth column (comma period)
        n = self.data[:, 1].size - self.timestamp
        convData = np.zeros((n - 1, 2))
        for i in range(1,n):
            convData[i - 1, 1] = self.data[i + self.timestamp - 1, 5]
            convData = extendValues(convData, int(self.timeext))
            write2cache('Q', convData)
        return convData

    def convertSolidDischarges(self, *args):
        _mynum_ = np.where(self.data[:, 0] == np.max(self.data[:, 0]))
        metricData = self.data[0:np.max(_mynum_[0][:]), :]
        timeLength = int(np.ceil(np.max(metricData[:, 0])))
        fittedData = np.zeros((timeLength, 2))
        for i in range(0, timeLength):
            _minPos_field = np.where(metricData[:, 0] > i)
            _minPos = _minPos_field[0][0]
            _maxPos_field = np.where(metricData[:, 0] < i + 1)
            _maxPos = _maxPos_field[0][np.max(_maxPos_field[0][:])]
            fittedData[i, 0] = i
            fittedData[i, 1] = linFun(self.p1_solid_q, self.p2_solid_q, np.mean(metricData[_minPos:_maxPos, 1]))
        return fittedData

    def fitNetWeight(self, Q):
        # reduces the basket weight and the weight of water discharges
        return self.p1_weight_voltage * Q + self.p2_weight_voltage

    def getQ(self, time):
        allQ = readCache('Q')
        allQ = np.array(allQ)
        if time > 0:
            _posQ = findValuePosition(allQ[:, 0], time, 0.1)
            Q = allQ[_posQ, 1]
        else:
            Q = 0
        return Q

    def getValues(self, value_name):
        # value_name = name of input file to read e.g. 'level5'
        script_dir = os.path.dirname(os.path.abspath(__file__))  # get base working directory of script
        os.chdir(script_dir + '\\.cache')
        data = []
        f = open(value_name+'.inp')
        for line in f:
            entry = line
            try:
                entry = float(entry)
            except ValueError:
                pass

            if type(entry) == str:
                entry.strip()

            try:
                data.append((entry))
            except ValueError:
                print('Could not make float from UsrInput ' + value_name + '.')

        os.chdir(script_dir)
        return data

    def push(self, value): # adds an element to the data stack
        np.append(self.data, value)

    def setValues(self, setName, setInfo):
        # writes vector of size (n,1) to cache
        script_dir = os.path.dirname(os.path.abspath(__file__))  # get base working directory of script
        os.chdir(script_dir+'\\cache')
        f = open(setName+'.inp','w')
        for i in setInfo:
            text = str(i)
            text = text.strip(' ]')
            text = text.strip('[ ')
            line = text+'\n'
            f.write(line)
        os.chdir(script_dir)



    def ultrasondsToDepth(self,*args): # transforms probe voltage signal to value in meters
        metricData = self.ultrasondsToMeter()
        if not self.fileN > 0:  # write mean bed levels to cache folder
            meanBedLevel = np.nanmean(metricData,0)
            self.setValues('BedLevels',meanBedLevel)
        else:
            bedLevel = self.getValues('Bedlevels')
            for i in range(1, self.data[1, :].size, 1):
                metricData[:, i] = bedLevel[i] - metricData[:, i]  # probe i
            #f itting of auto-values to calibration depth values (implementation 2016-09-29)
            for i in range(1, metricData[:, 0].size, 1):
                metricData[i, 1] = linFun(1., 0., metricData[i, 1])  # probe 1
                metricData[i, 2] = linFun(1., 0., metricData[i, 2])  # probe 2
                metricData[i, 3] = linFun(1., 0., metricData[i, 3])  # probe 3
                metricData[i, 4] = linFun(1., 0., metricData[i, 4])  # probe 4
                metricData[i, 5] = linFun(1., 0., metricData[i, 5])  # probe 5
        write2cache('meterValues' + str(self.fileN), metricData)
        return metricData

    def ultrasondsToMeter(self, *args):
        metricData = np.array(self.data)
        if not self.fileN > 0:
            self.refVal[0,:] = np.average(metricData[:,1:metricData.shape[0]],axis=0,weights=metricData[:,1:metricData.shape[0]].astype(bool)) / self.calibrationVolt # get reference to calibration data
            self.setValues('refVal',np.transpose(self.refVal))
            self.refVal=self.refVal[0,:]
        else:
            self.refVal=np.ones((1, 5))[0, :]

        for i in range(0, self.data[:,1 ].size, 1):
            cc = 0
            for j in self.p1_volts:
                metricData[i, cc + 1] = linFun(j, self.p2_volts[cc], metricData[i, cc + 1] / self.refVal[cc])  # probe cc


            metricData[i,2] = linFun(0.114164320243264,-0.10066506324216,metricData[i,2]/self.refVal[1])   # probe 2
            metricData[i,3] = linFun(0.0795167620431567,-0.0588664252001854,metricData[i,3]/self.refVal[2])  # probe 3
            metricData[i,4] = linFun(0.0789641718675665,-0.0544808366935177,metricData[i,4]/self.refVal[3])  # probe 4
            metricData[i,5] = linFun(0.0629803359274503,0.00132297019029537,metricData[i,5]/self.refVal[4])   # probe 5

        metricData = fitDataLength(metricData, self.datalength[self.fileN])
        timeLength = int(np.ceil(np.max(metricData[:, 0])))
        fittedData = np.zeros((timeLength, 6))
        for i in range(0, timeLength):
            _minPos_field = np.where(metricData[:, 0] > i)
            _minPos = _minPos_field[0][0]
            _maxPos_field = np.where(metricData[:, 0] < i + 1)
            _maxPos = _maxPos_field[0][np.max(_maxPos_field[0][:])]
            fittedData[i, 0] = i
            for j in range(1, 6, 1):
                fittedData[i, j] = np.mean(metricData[_minPos:_maxPos, j])
        return fittedData



















