#!/usr/bin/python
import sys, os
import numpy as np

# import functions (utilities)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from f_utilities import *


class HEC1D:
    def __init__(self, input_file_name):
        self.f_name = input_file_name
        self.start_row = 3
        self.sep = ','      # sep = column delimiter e.g. ','
        self.data = []
        self.n_Q = 0
        self.n_prof = 1
        self.profile_names = ''
        self.discharge_names = ''

    def del_new_line(self, arg):
        return arg.strip('\n')

    def fit_data_array(self, _data):
        _data = np.array(_data)
        for _p in range(0, self.n_prof):
            _posJump = _p + self.n_Q * (_p + 1)
            print(' * reading profile No. {0} ...'.format(_data[_posJump - 1, 1]))
            for _q in range(0, self.n_Q):
                _posAct = _p + self.n_Q * _p + _q
                if not(_posAct == _posJump):
                    for i in range(0, len(_data[0, :])):
                        if not(i == 16):
                            self.data[_p, _q, i] = _data[_posAct, i]
                            if i > 2:
                                self.data[_p, _q, i] = float(self.data[_p, _q, i])
        self.profile_names = self.data[:, 0, 1]
        self.discharge_names = self.data[0, :, 2]

    def parse_file_dim(self):
        if os.path.isfile(self.f_name):
            _f = open(self.f_name)
            _data = []                  # private list containing data file content
            _count = 0
            _nQ = 0
            for line in _f:
                if not(_count < self.start_row - 1):
                    _entries = line.split(self.sep)
                    _nn = len(_entries)
                else:
                    _entries = ['NaN']
                _data.append(_entries)
                _count += 1
                if len(_entries[0]) > 0:
                    _nQ += 1
                else:
                    if not(self.n_Q > 0):
                        self.n_Q = _nQ - 2
                    self.n_prof += 1
            if not(_nn == 16):
                print('Bad column description in HEC-RAS output file; check manual.')

    def read_csv(self):
        # reads *.CSV file without header
        if os.path.isfile(self.f_name):
            _f = open(self.f_name)
            _data = []                  # private list containing data file content
            _count = 0
            for line in _f:
                if not(_count < self.start_row - 1):
                    _entries = line.split(self.sep)
                    _nn = len(_entries)
                    for j in range(0, _nn, 1):  # convert input data to float
                        try:
                            if not j == _nn:
                                if _entries[j] == '\n':
                                    _entries[j] = self.del_new_line(_entries[j])
                                _entries[j] = float(_entries[j])

                        except ValueError:
                            try:
                                _temp = self.del_new_line(_entries[j])
                                _entries[j] = str2num(_temp.strip('\n'), '.')
                            except ValueError:
                                pass
                                # print('Input is NaN: {0}'.format(_entries[j]))
                    _data.append(_entries)
                _count += 1
            self.fit_data_array(_data)

            print(' * ' + self.f_name + ' has been imported.')

        else:
            print(os.curdir)
            print('There is no file ' + self.f_name + '. Check file path.')
            return()

    def __call__(self):
        self.parse_file_dim()
        self.data = np.array(np.zeros((self.n_prof, self.n_Q, 16)), dtype=object)
        self.read_csv()


class GrainInfo:
    def __init__(self, input_dir):
        self.f_name = input_dir + 'GrainData.csv'
        self.N = 0      # number of grain classes (size distributions)
        self.classes = 0
        self.g_names = ''
        self.sep = ','
        self.percentages = np.array([0., 0.1, 0.16, 0.2, 0.3, 0.35, 0.4, 0.5, 0.6, 0.65, 0.7, 0.8, 0.84, 0.9, 1])
        self.D16 = np.nan
        self.D30 = np.nan
        self.D35 = np.nan
        self.D50 = np.nan
        self.Dm = np.nan
        self.D84 = np.nan
        self.D90 = np.nan
        self.Dmax = np.nan

    def assign_D(self):
        # assigns names to descriptive data values
        self.D16 = np.nan * np.ones((self.N, 1))
        self.D30 = np.nan * np.ones((self.N, 1))
        self.D35 = np.nan * np.ones((self.N, 1))
        self.D50 = np.nan * np.ones((self.N, 1))
        self.Dm = np.nan * np.ones((self.N, 1))
        self.D84 = np.nan * np.ones((self.N, 1))
        self.D90 = np.nan * np.ones((self.N, 1))
        self.Dmax = np.nan * np.ones((self.N, 1))
        for j in range(0, self.N):
            if not(np.isnan(self.data[1, j])):
                self.D16[j] = self.data[1, j]
            if not(np.isnan(self.data[3, j])):
                self.D30[j] = self.data[3, j]
            if not(np.isnan(self.data[4, j])):
                self.D35[j] = self.data[4, j]
            if not(np.isnan(self.data[6, j])):
                self.D50[j] = self.data[6, j]
            if not(np.isnan(self.data[11, j])):
                self.D84[j] = self.data[11, j]
            else:
                if not (np.isnan(self.D50[j])):
                    self.D84[j] = self.D50[j] * 2.1  # Wolman (1954)
            if not(np.isnan(self.data[12, j])):
                self.D90[j] = self.data[12, j]
            # impose Dmax
            if not(np.isnan(self.data[13, j])):
                self.Dmax[j] = self.data[13, j]
            else:
                self.Dmax[j]=self.get_Dmax(j)
            # impose Dmean
            if not(np.isnan(self.data[14, j])):
                self.Dm[j] = self.data[14, j]
            else:
                self.Dm[j] = self.get_Dm(j)
        print(' * grain size parameter assignment OK.')

    def del_new_line(self, arg):
        return arg.strip('\n')

    def get_Dm(self, j):
        # Dmax needs to be assigned first
        _valuePositions = []
        for i in range(0, self.classes):
            if not(np.isnan(self.data[i, j])):
                _valuePositions.append(i)
        _mi = []
        _miDi = []
        for k in range(0,len(_valuePositions)):
            if not(k == len(_valuePositions)+1):
                if not(k > 0):
                    _val_m = self.percentages[_valuePositions[k]]
                    _val_Di = 0.5 * self.data[_valuePositions[k], j]
                else:
                    _val_m = self.percentages[_valuePositions[k]] - self.percentages[_valuePositions[k - 1]]
                    _val_Di = 0.5 * (self.data[_valuePositions[k], j] + self.data[_valuePositions[k - 1], j])
                _mi.append(_val_m)
                _miDi.append(_val_m*_val_Di)
        Dm = sum(_miDi) / sum(_mi)
        return Dm

    def get_Dmax(self, j):
        _valuePositions = []
        for i in range(0, self.classes):
            if not(np.isnan(self.data[i, j])):
                _valuePositions.append(i)

        Dclose = self.data[_valuePositions[len(_valuePositions)-1], j]
        Dperc = self.percentages[_valuePositions[len(_valuePositions)-1]]
        Dmax = Dclose / Dperc
        self.data[self.classes, j] = Dmax
        return Dmax

    def parse_file_dim(self):
        if os.path.isfile(self.f_name):
            _f = open(self.f_name)
            _lines = _f.readlines()
            _entries = _lines[0].split(self.sep)
            self.N = len(_entries)-1
            self.classes = len(_lines)-3
            _names = _entries[1:]
            _nNames = len(_names)-1
            _last = _names[_nNames].split('\n')
            _names[_nNames] = _last[0]
            self.g_names = _names

    def read_grains(self):
        # reads *.CSV file without header
        if os.path.isfile(self.f_name):
            _f = open(self.f_name)
            _data = []                  # private list containing data file content
            _count = 0
            for line in _f:
                if not(_count < 1):
                    _entries = line.split(self.sep)
                    _nn = len(_entries)
                    for j in range(0, _nn, 1):  # convert input data to float
                        try:
                            if not j == _nn:
                                if _entries[j] == '\n':
                                    _entries[j] = self.del_new_line(_entries[j])
                                _entries[j] = float(_entries[j])

                        except ValueError:
                            try:
                                _temp = self.del_new_line(_entries[j])
                                _entries[j] = str2num(_temp.strip('\n'), '.')
                            except ValueError:
                                pass
                                # print('Input is NaN: {0}'.format(_entries[j]))
                    _data.append(_entries)
                _count += 1
            _data = np.array(_data)
            for i in range(0, self.classes + 2):
                for j in range(1, self.N + 1):
                    _check = _data[i, j]
                    if not (j == self.N + 1) and len(_check) > 0:
                        self.data[i, j - 1] = float(_data[i, j])
                    else:
                        self.data[i, j - 1] = np.nan
            print(' * number of grain size classes: {0}'.format(self.N))
            return 0

        else:
            print('Error: Cannot find ' + self.f_name)
            return -1

    def __call__(self):
        self.parse_file_dim()
        self.data = np.array(np.zeros((self.classes + 2, self.N)), dtype=object)
        load_data = self.read_grains()
        if not (load_data == -1):
            self.assign_D()
        else:
            return -1





