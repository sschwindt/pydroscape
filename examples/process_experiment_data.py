import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')))
import pydroscape.e_data as psd
import logging
logging.basicConfig(filename='logfile.log', format='%(asctime)s %(message)s', level=logging.DEBUG)


def process_data():
    # ensure that file paths in the MetaData__i__.inp files point to the good directories (manual verificatoin required)
    own_dir = os.path.abspath(os.path.dirname(__file__)) + "/"

    logging.info(' START DATA PROCESSING')
    # note that e_data does not create logfiles.
    meta_data_dir = own_dir + 'sample_data/experiment_data/test_01809'
    data_processor = psd.Launcher()

    # # uncomment next line to write new MetaDatafile (this example already includes three MetaData__i__.inp files
    # data_processor.make_meta_file(meta_data_dir)

    # set linear transformation coefficients for ultrasonic Voltage signals
    p1_depth = [0.076, 0.114, 0.079, 0.078, 0.063]
    p2_depth = [-0.057, -0.100, -0.059, -0.054, 0.001]
    p1_solid_q = 558.1
    p2_solid_q = -7.01
    p1_scale_volt = 0.7166
    p2_scale_volt = 195.0
    data_processor.calibrate('voltage', p1_depth, p2_depth)
    data_processor.calibrate('solid_q', p1_solid_q, p2_solid_q)
    data_processor.calibrate('scale_voltage', p1_scale_volt, p2_scale_volt)
    data_processor.launch('01809', 3, meta_data_dir)


    logging.info(' FINISHED CDATA PROCESSING')
    

if __name__ == '__main__':
    process_data()



