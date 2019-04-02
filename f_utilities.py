try:
    import os
except:
    print("ExceptionERROR: Missing fundamental packages (required: os).")


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


def dict_values2list(dictionary):
    # converts the values of a dicionary into a list
    l = []
    for e in dictionary.values():
        l.append(e)
    return l


def get_subdir_names(directory):
    subdir_list = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    return subdir_list


def interpolate_linear(x1, x2, y1, y2, xi):
    # returns linear interpolation yi of xi between two points 1 and 2
    return float(y1) + ((float(xi) - float(x1)) / (float(x2) - float(x1)) * (float(y2) - float(y1)))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def read_file(full_path, col_separator):
    # full_path = STR of full path to text file
    # col_separator = STR, e.g., ',' or 'TAB'
    # returns nested list of data contained in a text file

    data = []
    f = open(full_path)
    f_lines = f.readlines()
    for line in f_lines:
        try:
            l = line.strip('\n').split(col_separator)  # remove newline symbol if exists
        except:
            try:
                l = line.split(col_separator)
            except:                
                l = line
        l_entries = []
        for e in l:
            try:
                l_entries.append(float(e))
            except:
                l_entries.append(str(e))
        try:
            data.append(l_entries)
        except ValueError:
            print('Could not read file information from: ' + str(full_path))
    f.close()
    return data


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

