import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')))
import pydroscape.e_geostat as psg
import logging
logging.basicConfig(filename='logfile.log', format='%(asctime)s %(message)s', level=logging.DEBUG)


def calculate_correlation(reference_raster, raster_1, raster_2, output_dir):
    # reference_raster = STR (path to reference raster
    # raster_1 = STR (path to raster 1)
    # raster_2 = STR (path to raster 2 that is to be correlated with raster 1)

    logging.info(' START CORRELATION OPERATIONS')
    geo_container = psg.GeoHandle()
    geo_container.reference_file = reference_raster
    geo_container.correlate_rasters(raster_1, raster_2, output_dir, normalize=True, spec="test")

    logging.info(' FINISHED CORRELATION OPERATIONS')
    

if __name__ == '__main__':
    
    own_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
    reference_raster = own_dir + "sample_data/rasters/raster_ref.tif"
    raster_1 = own_dir + "sample_data/rasters/raster_1.tif"
    raster_2 = own_dir + "sample_data/rasters/raster_2.tif"

    calculate_correlation(reference_raster, raster_1, raster_2, own_dir)
    logging.info(' * Done.')



