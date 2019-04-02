import os, sys
print(sys.version)
print(sys.executable)
print('Script requires pydroscape and runs with Python 3.')
sys.path.insert(0,'D:/Python/')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')))

try:
    import pydroscape.e_xlsx as psx
    import pydroscape.f_utilities as psu
except:
    print("ERROR: Cannot import pydroscape.")

def reset_dicts():
    dict_var1 = {5: 0.0, 10: 0.0, 15: 0.0, 20: 0.0, 30: 0.0, 40: 0.0, 50: 0.0}
    dict_var2 = {5: 0.0, 10: 0.0, 15: 0.0, 20: 0.0, 30: 0.0, 40: 0.0, 50: 0.0}
    dict_var3 = {5: 0.0, 10: 0.0, 15: 0.0, 20: 0.0, 30: 0.0, 40: 0.0, 50: 0.0}
    dict_var4 = {5: 0.0, 10: 0.0, 15: 0.0, 20: 0.0, 30: 0.0, 40: 0.0, 50: 0.0}
    dict_vars = {'Variable 1': dict_var1, 'Variable 2': dict_var2, 
                   'Variable 3': dict_var3, 'Variable 4': dict_var4}
    return dict_var1, dict_var2, dict_var3, dict_var4, dict_vars
    


def main():
    # set variables
    no_of_txt_files = 9
    own_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
    target_wb_name = own_dir + 'sample_data/workbooks/variables_area_statistics.xlsx'
    target_wb_col_dict = {'Variable 1': 'E', 'Variable 2': 'D', 
                          'Variable 3': 'F', 'Variable 4': 'C'}    
    
    
    print('START DATA PROCESSING ...')    
    for i in range(1, no_of_txt_files + 1):
        print('Processing: ' + own_dir + 'sample_data/text/site_' + str(i) + '.txt')
        dict_var1, dict_var2, dict_var3, dict_var4, dict_vars = reset_dicts()        
        
        # load data file as nested list with pye.f_utilities
        file_data = psu.read_file(own_dir + 'sample_data/text/site_' + str(i) + '.txt', ',')
        try:
            # find correct data columns from header names
            col_plant = file_data[0].index('Variable')
            col_lf = file_data[0].index('Persistence')
            col_area = file_data[0].index('Area')
            for l in file_data:
                # sum area of every variable within persistence classes
                if psu.is_number(l[0]):
                    dict_vars[l[col_plant]][l[col_lf]] += l[col_area] / 43560.0 # convert sqft to acres
                else:
                    print('Line of FID = ' + str(l[0]) + ' contains no area value.')
            print(' * Data count OK')                    
        except:
            print('Error: Could not identify columns in ' + own_dir + 
                  'sample_data/site_' + str(i) + '.txt')
            return -1

        print(' * Writing Workbook ...')
        try:
            target_wb = psx.full_handle(target_wb_name, i)
        except:
            print('Error: Could not open workbook sheet No. ' + str(i))
            print('      ' + target_wb_name)
        for p in target_wb_col_dict.keys():
            try:
                target_wb.write_data2column(target_wb_col_dict[p], 5, psu.dict_values2list(dict_vars[p]))
            except:
                print('Error: Could not write data to workbook sheet No. ' + str(i))
                print('      ' + target_wb_name)
                print('Dataset: ' + str(psu.dict_values2list(dict_vars[p])))
                break
        
        try:
            print(' * Saving Workbook ...')
            target_wb.save_close_wb(target_wb_name)
            print(' * OK')
        except:
            print('Error: Could not save workbook.')
            print('      ' + target_wb_name)
            return -1
    
    print('DONE.')



if __name__ == '__main__':
    main()



