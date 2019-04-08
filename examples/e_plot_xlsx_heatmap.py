import os, sys
print(sys.version)
print(sys.executable)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
try:
    os.remove(os.path.abspath(os.path.dirname(__file__)) + '/logfile.log')
except:
    pass
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')))
try:
    import pydroscape.e_xlsx as psx
    import pydroscape.e_plot as psp
except:
    print('ERROR: Cannot import own packages.')

# set up logging
import logging
logging.basicConfig(filename='logfile.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

def get_xlsx_file_names(loc_dir):
    # returns a LIST of files in loc_dir that contain search_str
    # loc_dir = STR of the full directory to scan, ending with '/'
    # search_str = STR that a filename needs to contain for being appended
    file_list = []
    for root, dirs, files in os.walk(loc_dir):
        for file in files:
            if 'xlsx' in str(file).lower():
                file_list.append(loc_dir + file)
    return file_list


def main(file_dir):
    # file_dir = STR of directory where XLSX workbooks with 2D plot data are stored

    own_dir = os.path.abspath(os.path.dirname(__file__)) + '/'
    files = get_xlsx_file_names(file_dir)
    if files.__len__() < 1:
        logging.info('No Data. Ensure that the sample_data folder contains data.')
        return -1
    for f in files:
        try:
            logging.info('PROCESSING: ' + str(f))
            data_wb = psx.Workbook(f, 0)
            logging.info(' - Reading data ...')
            _q_ = data_wb.read_row(1, 'B') # corresponds to x-data
            labels_mu = data_wb.read_column('A', 2) # corresponds to y-data

            corr_data = data_wb.read_matrix('B', 2) # corresponds to Z-data
            logging.info(' - Creating plot ...')
            surf_plot = psp.Plotter()
            surf_plot.width = 6.0
            surf_plot.height = 10.0
            surf_plot.font_size = 11.0
            surf_plot.legend_active = True
            surf_plot.colorbar_aspect = 20
            surf_plot.colorbar_shrink = 0.93
            surf_plot.y_label = 'Morphological Units'
            surf_plot.save_fig_dir = own_dir + 'output/' + str(f.split('/')[-1].split('.')[0]) + '.png'
            
            labels_q = []
            for labs in _q_:
                labels_q.append(str(labs) + ' m3/s')

            surf_plot.colorbar_min_val = -1
            surf_plot.colobar_label = 'Pearson r [--]'
            surf_plot.color_map_type = 'RdYlGn'
            
            
            logging.info(' - Producing figure ... ')
            surf_plot.make_heatmap(corr_data, labels_q, labels_mu)
            
            try:
                data_wb.close()
            except:
                del data_wb
            logging.info(' - OK')
        except:
            logging.info('WARNING: A problem occurred. Check previous ERROR and/or WARNING messages.')

    logging.info('FINISHED.')


if __name__ == '__main__':
    file_dir = os.path.abspath(os.path.dirname(__file__)) + '/sample_data/workbooks/'  # directory of correlation text files
    main(file_dir)



