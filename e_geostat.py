
import numpy as np
import os, sys, logging
from collections import Iterable  # used in the flatten function
from osgeo import gdal, gdalconst

print(os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0]))))
logging.basicConfig(filename='logfile.log', format='%(asctime)s %(message)s', level=logging.DEBUG)


class GeoHandle:
    def __init__(self):
        self.dir_master = os.path.abspath(os.path.dirname(__file__)) + "/"
        self.no_data_value = -999.9
        self.reference = None
        self.reference_proj = str()
        self.reference_trans = tuple()
        self.band_ref = gdal.Band
        self.x_ref = int()
        self.y_ref = int()
        self.reference_file = 'empty'

    def align_raster(self, raster2align_path, *args):
        # raster2align_path = STRE (full path to raster that should be aligned with base_ras)
        # args[0] = STR (full path to reference raster)
        logging.info(' *** -- aligning raster ... ')
        input = gdal.Open(raster2align_path, gdalconst.GA_ReadOnly)
        input_proj = input.GetProjection()

        try:
            self.set_reference_raster(args[0])
        except:
            self.set_reference_raster()

        try:
            outputfile = raster2align_path.split('.tif')[0] + 'a.tif'  # Path to output file
            logging.info(' *** -- creating aligned raster (' + outputfile + ') ... ')
            if os.path.exists(outputfile):
                try:
                    logging.info(' *** -- removing existing file (' + outputfile + ') ... ')
                    os.remove(outputfile)
                except:
                    logging.info('WARNING: Cannot write aligned output (' + outputfile + ' is locked).')
            driver = gdal.GetDriverByName('GTiff')
            output = driver.Create(outputfile, self.x_ref, self.y_ref, 1, self.band_ref.DataType)
            output.SetGeoTransform(self.reference_trans)
            output.SetProjection(self.reference_proj)

            gdal.ReprojectImage(input, output, input_proj, self.reference_proj, gdalconst.GRA_Bilinear)
            new_path = outputfile
            logging.info(' *** -- OK - aligned raster path: ' + new_path)
        except:
            logging.info('ERROR: Alignment failed.')
            new_path = 'none'
        return new_path

    def correlate_rasters(self, ras_1, ras_2, output_dir, *args, **kwargs):
        # ras_1 / ras_2 = STR of raster directories (full paths)
        # kwargs:
        #   normalize=BOOL (default: True)
        #   spec=STR (specifier for output saving)
        try:
            for opt_var in kwargs.items():
                if 'normalize' in opt_var[0]:
                    normalize = opt_var[1]
                if 'spec' in opt_var[0]:
                    spec = opt_var[1]
        except:
            pass

        if not ('normalize' in locals()):
            normalize = True
        if not ('spec' in locals()):
            spec = 'c'

        [array_1, array_1_stats] = self.raster2array(ras_1, normalize=normalize)
        [array_2, array_2_stats] = self.raster2array(ras_2, normalize=normalize)

        if normalize:
            array_1 = (array_1 - np.nanmean(array_1)) / np.nanstd(array_1)
            array_2 = (array_2 - np.nanmean(array_2)) / np.nanstd(array_2)

        corr = self.stat_pearson_r(list(self.flatten_array(array_1)), list(self.flatten_array(array_2)))
        logging.info('    * writing correlation of ' + str(corr) + ' to ' + output_dir + 'correlation_' + str(spec) + '.txt')
        f = open(output_dir + 'correlation_' + str(spec) + '.txt', 'a')
        f.write('Correlation of:\n' + str(ras_1) + "\nand\n" + str(ras_2))
        f.write("\n" + str(corr) + "\n\n")
        f.write(str(ras_1) + ' statistics [Min, Max, Mean, Stdev]: \n' + str(array_1_stats) + "\n")
        f.write(str(ras_2) + ' statistics [Min, Max, Mean, Stdev]: \n' + str(array_2_stats) + "\n")
        f.close()
        logging.info(" -- correlation written to: " + output_dir)

    def flatten_array(self, array):
        # function flattens an array into a list
        # usage flattened_array = list(flatten_array(array))
        for item in array:
            if isinstance(item, Iterable) and not isinstance(item, str):
                for x in self.flatten_array(item):
                    yield x
            else:
                yield item

    def raster2array(self, file_name, *args, **kwargs):
        # file_name = STR of raster path (full directory)
        # args[0][0] = float number below which all raster values will be set to np.nan
        # args[0][1] = float number above which all raster values will be set to np.nan
        # kwargs:
        #   normalize=BOOL (default: True)

        try:
            for opt_var in kwargs.items():
                if 'normalize' in opt_var[0]:
                    normalize = opt_var[1]
        except:
            pass

        if not ('normalize' in locals()):
            normalize = True

        gdal.AllRegister()
        file_name = self.align_raster(file_name)
        print('* screeninfo: processing ' + file_name)
        try:
            logging.info(" *** opening file " + str(file_name) + " ...")
            file = gdal.Open(file_name)
            ras = file.GetRasterBand(1)
        except:
            logging.info('WARNING: Could not open ' + str(file_name))
            return -1

        try:
            logging.info(" *** converting Raster to Array ...")
            ras_array = ras.ReadAsArray()
        except:
            logging.info('WARNING: Could not convert raster to array.')
            return -1

        # make non-relevant pixels np.nan
        if normalize:
            logging.info(" *** normalizing Array (identify nan and apply sigmoid normalization) ...")
        else:
            logging.info(" *** identifying nan values ...")
        try:
            ras_array = ras_array.astype(float)
        except:
            logging.info('WARNING: Could not convert array(raster) to floats --> error will likely occur.')

        ras_array[ras_array <= self.no_data_value] = np.nan
        try:
            ras_array[ras_array < args[0][0]] = np.nan  # lower nan-threshold
            ras_array[ras_array > args[0][1]] = np.nan  # upper nan-threshold
        except:
            pass
        ras_array[ras_array == 0] = np.nan

        array_dim = ras_array.shape

        for i in range(0, array_dim[0] - 1):
            for j in range(0, array_dim[1] - 1):
                if not (np.isnan(ras_array[i][j]) or np.round(ras_array[i][j], 1) == self.no_data_value or np.round(ras_array[i][j], 4) == 0.0000):
                    try:
                        if normalize:
                            ras_array[i][j] = 1 / (1 + np.exp(-ras_array[i][j]))
                    except:
                        ras_array[i][j] = np.nan
                else:
                    ras_array[i][j] = np.nan

        logging.info("     Max array value: " + str(np.nanmax(ras_array)))
        logging.info("     Min array value: " + str(np.nanmin(ras_array)))
        logging.info(" *** calculating Array statistics ...")
        stats = ras.GetStatistics(0, 1)
        print('* processed * ' + str(file_name))

        return [ras_array, stats]

    def set_reference_raster(self, *ref_ras_name):
        # refras_name[0] = STR(reference raster to use)
        logging.info(' *** -- setting reference raster ... ')
        try:
            self.reference_file = ref_ras_name[0]  # Path to reference file
        except:
            if self.reference_file == 'empty':
                logging.info('ERROR: No reference raster provided.')
                return -1

        logging.info('        ref. name: ' + self.reference_file)
        try:
            print('*')  # do not delete -- print msg imposes a required variable evaluation break
            del self.reference
            print('* pace')  # do not delete -- print msg imposes a required variable evaluation break
            self.reference = gdal.Open(self.reference_file, gdalconst.GA_ReadOnly)
        except:
            logging.info('WARNING: Cannot open reference raster.')
        try:
            self.reference_proj = self.reference.GetProjection()
            self.reference_trans = self.reference.GetGeoTransform()
            self.band_ref = self.reference.GetRasterBand(1)
            self.x_ref = self.reference.RasterXSize
            self.y_ref = self.reference.RasterYSize
        except:
            logging.info('WARNING: Cannot access properties of reference raster.')
        logging.info(' *** -- OK (reference set) ')

    def stat_pearson_r(self, X, Y):
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

    def __call__(self, *args, **kwargs):
        print('Class Info: <type> = Geo_Handle (requirements: osgeo.gdal, numpy).')





