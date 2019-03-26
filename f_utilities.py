try:
    import os, logging, sys, glob, webbrowser, time
    from collections import Iterable  # used in the flatten function
    import numpy as np
except:
    print("ExceptionERROR: Missing fundamental packages (required: os, sys, glob, logging, time, webbrowser).")

try:
    # set logger
    logging.basicConfig(filename='logfile.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
except:
    print("WARNING: fGlobal could not load logger.")

def chk_is_empty(variable):
    try:
        value = float(variable)
    except ValueError:
        value = variable
        pass
    try:
        value = str(variable)
    except ValueError:
        pass
    return bool(value)


def chk_dir(directory):
    if not(os.path.exists(directory)):
            os.makedirs(directory)


def clean_dir(directory):
    # Delete everything reachable IN the directory named in 'directory',
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if directory == '/', it
    # could delete all your disk files.
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def get_subdir_names(directory):
    subdir_list = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    return subdir_list


def interpolate_linear(x1, x2, y1, y2, xi):
    # returns linear interpolation yi of xi between two points 1 and 2
    yi = y1 + ((xi - x1) / (x2 - x1) * (y2 - y1))
    return yi


def pearson_r(X, Y):
    # returns the pearson correlation coefficient of two vectors X and Y (same length)
    # handles np.nan, see https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    if not (X.__len__() == Y.__len__()):
        print('WARNING: Different length of X and Y vectors.')
        try:
            logging.info('WARNING: Different length of X and Y vectors.')
        except:
            print('WARNING: This information could not be written to the logfile.')
        return np.nan
    else:
        mean_x = float(np.nansum(X) / X.__len__())
        mean_y = float(np.nansum(Y) / Y.__len__())
        nominator = 0.0
        denominator_x = 0.0
        denominator_y = 0.0
        for i in range(0, X.__len__()):
            if not (np.isnan(X[i]) or np.isnan(Y[i])):
                nominator += (X[i] - mean_x) * (Y[i] - mean_y)
                denominator_x += float((X[i] - mean_x) ** 2)
                denominator_y += float((Y[i] - mean_y) ** 2)

        try:
            return float(nominator / (np.sqrt(denominator_x) * np.sqrt(denominator_y)))
        except:
            return np.nan


def rm_dir(directory):
    # Deletes everything reachable from the directory named in 'directory', and the directory itself
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if directory == '/' deletes all disk files
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(directory)


def rm_file(full_name):
    # fullname = str of directory + file name
    try:
        os.remove(full_name)
    except:
        pass


def str2frac(arg):
    arg = arg.split('/')
    return int(arg[0]) / int(arg[1])


def str2num(arg, sep):
    # function converts string of type 'X[sep]Y' to number
    # sep is either ',' or '.'
    # e.g. '2,30' is converted with SEP = ',' to 2.3
    _num = arg.split(sep)
    _a = int(_num[0])
    _b = int(_num[1])
    _num = _a + _b * 10 ** (-1 * len(str(_b)))
    return _num


def str2tuple(arg):
    try:
        arg = arg.split(',')
    except ValueError:
        print('ERROR: Bad assignment of separator.\nSeparator must be [,].')
    tup = (int(arg[0]), int(arg[1]))
    return tup


def tuple2num(arg):
    # function converts float number with ',' separator for digits to '.' separator
    # type(arg) = tuple with two entries, e.g. (2,40)
    # call: tuple2num((2,3))
    new = arg[0] + arg[1] * 10 ** (-1 * len(str(arg[1])))
    return new


def write_data(folder_dir, file_name, data):
    if not os.path.exists(folder_dir):
            os.mkdir(folder_dir)
    os.chdir(folder_dir)

    f = open(file_name+'.txt', 'w')
    for i in data:
        line = str(i)+'\n'
        f.write(line)
    print('Data written to: \n' + folder_dir + '\\' + str(file_name) + '.csv')

