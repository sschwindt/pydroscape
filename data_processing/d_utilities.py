#!/usr/bin/python
import os
import numpy as np
try:
    import pandas as pd
except:
    print('Skipping pandas import (missing package).')
import fileinput


def averageValues(data, avg_len, *args, **kwargs):
    # function returns average values out of avg_len (int) values
    n = int(data[:, 1].size / avg_len)  # number of rows
    m = data[1, :].size  # number of cols
    _results = np.zeros((n, m))
    for i in range(1, n + 1):
        _pStart = (i - 1) * avg_len
        _pEnd = _pStart + avg_len - 1
        _results[i - 1, 0] = data[_pEnd, 0]

        for j in range(1, m):
            _results[i - 1, j] = np.mean(data[_pStart:_pEnd + 1, j])
    return _results


def cacheRemove(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # get base working directory of script
    os.chdir(script_dir+'/.cache')
    if os.path.isfile(file_name):
        os.remove(file_name)
    os.chdir(script_dir)


def chkData(data):
    # returns 0 if data are empty
    data = np.array(data)
    return int(np.sum(data))


def chkIsEmpty(variable):
    try:
        value = float(variable)
    except ValueError:
        pass
    try:
        value = str(variable)
    except ValueError:
        pass
    try:
        return bool(value)
    except:
        return False


def chkFolderStructure(folder_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # get base working directory of script
    if not (os.path.exists(script_dir + '\\' + folder_name)):
        os.mkdir(script_dir + '\\' + folder_name)


def chkInteger(args):
    # assigns 1 to values which should be integer but are not defined
    for i in range(0, len(args) - 1):
        if not type(args[i]) == int:
            args[i] = 1
    return args


def chkIsCacheFile(file_name):
    # returns TRUE if the file exists in cache folder
    script_dir = os.path.dirname(os.path.abspath(__file__))  # get base working directory of script
    os.chdir(script_dir+'/.cache')
    if os.path.isfile(file_name+'.inp'):
        os.chdir(script_dir)
        return True
    else:
        os.chdir(script_dir)
        return False


def delNewLine(arg):
    arg = arg.strip('\n')
    return arg


def fitDataLength(data, data_length):
    # cuts matrix rows which are unimportant, according to datalength
    fitted_data = data[0:data_length, :]
    return fitted_data


def extendDigits(number, n_digits):
    n_digits = int(n_digits)
    if n_digits != 0:
        n2str = str(number)
        fullN = zeroList(n_digits)

        lenN = len(fullN)
        dLen = lenN - len(n2str)

        for i in range(0,lenN):
            if i < dLen:
                fullN[i] = str(fullN[i])
            else:
                j = i - dLen
                fullN[i] = n2str[j]
        return ''.join([str(i) for i in fullN])
    else:
        return str(number)


def extendValues(data, ext_len):
    # inserts rows with repetitions of data in row i for ext_len rows
    # overwrites the first column!
    n = data[:, 0].size
    m = data[0, :].size
    n_new = n * ext_len
    _manip = np.zeros((n_new, m))

    for i in range(1, n + 1):
        for k in range(0, ext_len):
            pos = (i - 1) * ext_len + k + 1
            _manip[pos - 1, 0] = pos  # write time mark
            for j in range(1, m):
                _manip[pos - 1, j] = data[i - 1, j]
    return _manip


def findValuePosition(arr, value, prec):
    # finds the position of a certain value in an Vector array
    # precision defines the precision with which the value has to be suitable
    count = 0
    positionList = []
    for i in range(0, arr.size):
        if (float(arr[i]) > float(value) - prec) and (float(arr[i]) < float(value) + prec):
            positionList.append(count)
        count += 1
    return np.array(positionList)


def getUsrSettings(setting_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # get base working directory of script
    os.chdir(script_dir+'/.cache')
    settings = []
    f = open(setting_name+'.inp')
    for line in f:
        entry = line
        try:
            entry = int(entry)
        except ValueError:
            pass

        if type(entry) == str:
            entry.strip()
        try:
            settings.append((entry))
        except ValueError:
            print('Could not make float from UsrInput ' + setting_name + '.\n In e_data.f_functions getUsrSettings.')
    os.chdir(script_dir)
    return settings


def linFun(p1, p2, x):
    val = p1 * x + p2
    return val


def normalize(*args):
    # takes a series (vector) of numbers and normalizes it
    # make sure that at least one of the input arguments is of type 'float'
    args = np.array(args)
    max = args.max()
    min = args.min()
    dVal = max-min

    for i in range(0, args[0, :].size, 1):
        if dVal > 0:
            args[0, i] = (args[0, i] - min) / dVal
        else:
            args[0, i] = args[0, i]
    return args


def readCache(c_name):
    # c_name = the name of the cache file to read (without '.inp') [STR]
    script_dir = os.path.dirname(os.path.abspath(__file__))  # get base working directory of script
    os.chdir(script_dir + '/.cache')

    data = []
    f = open(c_name + '.inp')
    for line in f:
        entry = line
        try:
            entry = float(entry)
        except ValueError:
            pass

        if type(entry) != float:
            entry=entry.split()
            new_entry=[]
            for i in range(1,len(entry)-1):
                if i != len(entry)-1:
                    new_entry.append(float(entry[i]))
                else:
                    _temp = entry[i].split(']')
                    new_entry.append(float(_temp[0]))
                    entry = new_entry
        try:
            data.append((entry))
        except ValueError:
            print('Could not make float from UsrInput '+c_name+'.\n In e_data.f_functions getUsrSettings.')
    fileinput.close()
    os.chdir(script_dir)

    return data


def setDataHeaders(matrix, col_names):
    # col_names = LIST
    # matrix = numpy.array
    try:
        _PD_matrix = pd.DataFrame(matrix)
        _colNos = np.arange(len(col_names))
        _PD_dict = dict(zip(_colNos, col_names))
        _PD_matrix = _PD_matrix.rename(columns=_PD_dict)
    except:
        print("Warning: Could not assign matrix column names (missing pandas).")
        _PD_matrix = matrix
    return _PD_matrix


def str2frac(arg):
    arg = arg.split('/')
    return int(arg[0])/int(arg[1])


def str2num(arg, SEP):
    # function converts string of type 'X[SEP]Y' to number
    # SEP is either ',' or '.'
    # e.g. '2,30' is converted with SEP = ',' to 2.3
    _num = arg.split(SEP)
    _a = int(_num[0])
    _b = int(_num[1])
    return _a+_b*10**(-1*len(str(_b)))


def str2tuple(arg):
    try:
        arg = arg.split(',')
    except ValueError:
        print('Bad assignment of separator.\nSeparator must be [,].')
    return int(arg[0]), int(arg[1])


def tuple2num(arg):
    # function converts float number with ',' separator for digits to '.' separator
    # type(arg) = tuple with two entries, e.g. (2,40)
    # call: tuple2num((2,3))
    return arg[0]+arg[1]*10**(-1*len(str(arg[1])))


def write2cache(set_name, set_info, *args):
    # setName is the data name, type STR, --> e.g. 'thename'
    # setInfo is the data itself, type numeric
    # args[0] = STR of an alternative directory
    # args[1] = STR of alternative file ending
    try:
        script_dir = args[0]
        os.chdir(script_dir)
    except:
        script_dir = os.path.dirname(os.path.abspath(__file__))  # get base working directory of script
        os.chdir(script_dir + '/.cache')
    try:
        f_ending = args[1]
    except:
        f_ending = 'inp'
    f = open(set_name + '.' + f_ending, 'w')
    for i in set_info:
        f.write(str(i) + '\n')
    f.close()
    os.chdir(script_dir)


def writeData(folder_dir, file_name, data):
    if not os.path.exists(folder_dir):
            os.mkdir(folder_dir)
    os.chdir(folder_dir)
    try:
        _PD_data = pd.DataFrame(data)
        _PD_data.to_csv(folder_dir + '\\' + file_name + '.csv', header=0, index=0)  # set header = 1 for col-names and index = 1 for row-names
    except:
        write2cache(file_name, data, folder_dir, 'csv')
        print('Warning: Could not import pandas --> writing unsorted data ...')
    print('Data written to: \n' + folder_dir + '\\' + str(file_name))


def zeroList(n):
    list_of_zeros = [0] * n
    return list_of_zeros
