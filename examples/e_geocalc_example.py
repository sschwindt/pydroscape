import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')))
import pydroscape.e_geocalc as psgc

# set up logging
import logging
logging.basicConfig(filename='logfile.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

def start_calculation(raster_1, raster_2, out_dir):
    # reference_raster = STR (path to reference raster
    # raster_1 = STR (path to raster 1, where the folder separators are '/')
    # raster_2 = STR (path to raster 2, where the folder separators are '/')

    logging.info(' START RASTER CALCULATION')
    geo_container = psgc.QgsHandle()
    
    ref_ras1 = raster_1.split('/')[-1] + '@1'
    ref_ras2 = raster_2.split('/')[-1] + '@1'

    expression = '("' + ref_ras1 + '">' + str(0) + ') ' + ' * ("' + ref_ras2 + '"!=' + str(
        0) + ') * log10("' + ref_ras1 + '" *  "' + ref_ras2 + '") + ' + '("' + ref_ras2 + '"=' + str(
        0) + ') * "' + ref_ras1 + '"'

    output_ras = out_dir + 'result.tif'
    
    geo_container.calculate_raster(expression, output_ras, [raster_1, raster_2])

    logging.info(' FINISHED CORRELATION OPERATIONS')


if __name__ == '__main__':
    
    own_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
    raster_1 = own_dir + "sample_data/rasters/raster_1.tif"
    raster_2 = own_dir + "sample_data/rasters/raster_2.tif"

    start_calculation(raster_1, raster_2, own_dir + "output/")


