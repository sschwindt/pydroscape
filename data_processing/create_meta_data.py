#!/usr/bin/python
import os


class MetaMaker:
    def __init__(self):
        self.meta_dir = str()

        self.in_path = str()
        self.file_pre = str()
        self.meas_no_a = int()
        self.meas_no_b = int()
        self.meas_no_digits = int()
        self.file_suffix = str()
        self.file_type = str()
        self.data_delimiter = str()
        self.header_len = int()
        self.data_name = str()
        self.data_columns = int()
        
        self.applicable_methods = []
        self.timestamp = int()
        
        self.fluid = 'WATER'
        self.fluid_temp = 18

        self.out_graph_path = str()
        self.out_graph_name = str()
        self.out_data_path = str()
        self.out_data_name = str()

        self.inp_file_name = str()

        self.sline = str()
        self.eline = str()

    def input_path(self):
        self.in_path = input('Please enter the path to the data:\n>> ')
        return self.in_path

    def datafiles(self):
        print('------- DATAFILE DESCRIPTION --------------------------------------------------------------------------')
        self.file_pre = input('Please enter the Prefix of the data file names (INT PREFIXnumberSuffix.type):\n>> ')
        self.meas_no_a = input('Please enter the lowest/first file number (INT prefixNUMBERsuffix.type):\n>> ')
        self.meas_no_b = input('Please enter the highest/last file number (INT prefixNUMBERsuffix.type):\n>> ')
        self.meas_no_digits = input('How many digits does the file number count (INT if this equals the file numbers digits, enter 0)?:\n>> ')
        self.file_suffix = input('Please enter the Suffix of the data file names (STR prefixNumberSUFFIX.type):\n>> ')
        self.file_type = input('Please enter the Type of the data file names (STR prefixNumberSuffix.TYPE, i.e. csv, txt etc.):\n>> ')
        self.data_delimiter = input('Please enter the self.data_delimiter of data columns (STR << , ; or tab >>):\n>> ')
        self.header_len = int(input('How long is the header (INT number of rows, if there is no header, enter 0):\n>> '))
        self.data_columns = input('How many columns does the input data file have (INT)?')
        self.data_name = input('Please name the data (STR, e.g. discharges, levels):\n>>')

    def computation(self):
        print('------- SPECIFICATION OF COMPUTATION METHODS ----------------------------------------------------------')
        print('Enter one of the following computation method you want to apply.\n')
        self.applicable_methods.append(input('< SORT, plotData,  >:\n>> '))
        print('Set the time stamp (stop watch used?).')
        self.timestamp = input('Time stamp in seconds (INT):\n>> ')

    def fluid_spec(self):
        print('------- SPECIFICATION OF THE self.fluid ---------------------------------------------------------------')
        print('Please specify one of the following self.fluid types.')
        self.fluid = input('< WATER >:\n>> ')
        self.fluid_temp = float(input('Please enter the self.fluid temperature in degree Celsius:\n>> '))

    def output_desc(self):
        print('------- OUTPUT DESCRIPTION ----------------------------------------------------------------------------')
        self.out_graph_path = input('Please enter the path for graphic output files, i.e. figures (NOT APPLICABLE - LEAVE EMPTY):\n>> ')
        self.out_graph_name = input('Please enter the prefix name for output figures (nan for no figures):\n>> ')
        self.out_data_path = input('Please enter the path for output data files (e.g. subfolder\\subfolderdata - nan for no file output):\n>> ')
        self.out_data_name = input('Please enter the prefix name for output data file (nan for no file output):\n>> ')

    def write_basic(self, finalCond, *args, **kwargs):
        self.sline = '#---------------------------------------------------------------------------------------\n'
        self.eline = '# \n'
        os.chdir(self.meta_dir)
        f = open(self.inp_file_name, 'w')
        f.write(self.eline)
        f.write('#INPUT PATH\n')
        f.write(self.sline)
        f.write('Data path = {0} #[STRING]\n'.format(self.in_path))
        f.write(self.eline)
        f.write('#DESCRIPTION OF DATAFILES - PrefixNumberSuffix.Type \n')
        f.write(self.sline)
        f.write('Start measurement number = {0} #[INTEGER]\n'.format(self.meas_no_a))
        f.write('Final measurement number = {0} #[INTEGER]\n'.format(self.meas_no_b))
        f.write('Digits of measurement number = {0} #[INTEGER]\n'.format(self.meas_no_digits))
        f.write('Data filename (prefix) = {0} #[STRING]\n'.format(self.file_pre))
        f.write('Data filename (suffix) = {0} #[STRING]\n'.format(self.file_suffix))
        f.write('Data file type = {0} #[STRING]\nData self.data_delimiter = {1} #[STRING] TAB by tab\nHeader length = {2} #[INTEGER]\nData name = {3} #[STRING]\n'.format(self.file_type, self.data_delimiter, self.header_len, self.data_name))
        f.write('Data columns = {0} #[STRING]\n'.format(self.data_columns))

        if finalCond != 1:
            f.close()
            print('------->> INPUT SPECIFICATION FILE WRITTEN TO:')
            print(os.getcwd(), '\\', self.inp_file_name)
        else:
            print('------->> INPUT SPECIFICATION FILE UNDER CONSTRUCTION')
        return f

    def write_output(self, f):
        f.write(self.eline)
        f.write('#SPECIFICATION OF COMPUTATION \n')
        f.write(self.sline)
        f.write('Method(s) = {0} #[STRING]\nTime stamp = {1} #[STRING]\n'.format(self.applicable_methods, self.timestamp))
        f.write(self.eline)
        f.write('#self.fluid PARAMETERS \n')
        f.write(self.sline)
        f.write('self.fluid type = {0} #[STRING]\nself.fluid temperature = {1} #[INTEGER]\n'.format(self.fluid, self.fluid_temp))
        f.write(self.eline)
        f.write('#OUTPUT \n')
        f.write(self.sline)
        f.write('Output path for figures = {0} #[STRING] (e.g. subfolder\\subfolderForFigures, nan for no figures)\nOutput path for data files = {2} #[STRING] (e.g. subfolder\\subfolderForData, nan for no file output)\nOutput name for figures = {1} #[STRING] nan for no figures\nOutput name for data files = {3} #[STRING] nan for no file output\n'.format(self.out_graph_path, self.out_graph_name, self.out_data_path, self.out_data_name))
        f.close()
        print('------->> INPUT SPECIFICATION FILE WRITTEN TO:')
        print(self.meta_dir, '/', self.inp_file_name)

    def basic_file(self):
        # CREATE INPUT SPECIFICATIONS BASE FILE
        print('Creation of basic input specification file chosen.')
        # get user input
        self.input_path()
        self.datafiles()
        self.computation()
        self.fluid_spec()
        self.output_desc()
        # write to file
        self.inp_file_name = 'MetaData.inp'
        file = self.write_basic(1)
        self.write_output(file)

    def create_meta_data(self):
        print('This is the generation of the input file structure which is stored in the file <<MetaDataX.inp>> which can be modified later on.')
        print('The target directory is: ' + self.meta_dir)
        self.basic_file()
        print('Done.')

    def __call__(self, meta_dir, *args, **kwargs):
        self.meta_dir = meta_dir
        self.create_meta_data()







