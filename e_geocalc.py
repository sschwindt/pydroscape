try:
    from qgis.core import *
    from qgis.analysis import QgsRasterCalculatorEntry, QgsRasterCalculator
except:
    print("ERROR: Cannot import qgis.core. Check interpreter and installation.")

from e_geostat import *

print(os.path.abspath(os.path.abspath(os.path.dirname(sys.argv[0]))))
logging.basicConfig(filename='logfile.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

try:
    QgsApplication.setPrefixPath('C:/Program Files/QGIS 3.4/apps/Python37/', True)  # True says that QgsApp is standalone
    qgs = QgsApplication([], False)
    qgs.initQgis()
except:
    print("ERROR: Cannot initiate QgsApplication.")


class QgsHandle(GeoHandle):
    def __init__(self):
        GeoHandle.__init__(self)

    def calculate_raster(self, exp, output_ras, input_ras_dirs):
        # raster calculator function for multi-layer-operations
        # exp = STR containing calculation expression
        # output_ras = STR of output Raster name
        # input_ras_dirs = LIST of calculator entries created with self.convert_to_calc_entry() function

        logging.info(' *** expression: ' + exp)
        logging.info(' *** output target Raster: ' + str(output_ras))
        ras_lyrs = []
        entries = []
        for i in input_ras_dirs:
            lyr, ras = self.convert_to_calc_entry(i)
            ras_lyrs.append(ras)
            entries.append(lyr)
        try:
            if ras_lyrs[0].isValid():
                '''
                self.ras_lyrs[0].extent().width = self.output_size
                self.ras_lyrs[0].extent().height = self.output_size
                self.ras_lyrs[0].width= self.output_size
                self.ras_lyrs[0].height= self.output_size
                '''
                try:
                    logging.info(" *** -- calculating ... ")
                    calc = QgsRasterCalculator(exp, output_ras, 'GTiff', ras_lyrs[0].extent(), ras_lyrs[0].width(),
                                               ras_lyrs[0].height(), entries)
                    try:
                        logging.info(" *** -- " + str(calc.processCalculation()))
                    except:
                        print(calc.processCalculation())
                    logging.info(" *** -- calculation success (done).")
                except:
                    logging.warning("FAILED Raster Calculation.")
                    return -1

                if QgsRasterLayer(output_ras).isValid():
                    logging.info(" *** -- created Raster: " + output_ras + "\n")
                else:
                    logging.warning("INVALID Output Raster: " + output_ras)

            else:
                try:
                    logging.warning("INVALID Raster: " + ras_lyrs[0].ref)
                except:
                    logging.warning("INVALID Raster.")
        except:
            logging.info("ERROR: Testing raster_layer.isValid() failed.")

    def convert_to_calc_entry(self, file_name):
        # Raster calculator entry type for using QgsRasterCalculator
        my_raster = QgsRasterLayer(file_name)
        my_layer = QgsRasterCalculatorEntry()
        my_layer.raster = my_raster
        my_layer.ref = file_name.split('/')[-1] + '@1'
        my_layer.bandNumber = 1
        return my_layer, my_raster

    def get_pixel_size(self, file_name):
        lyr, ras = self.convert_to_calc_entry(file_name)
        x = ras.rasterUnitsPerPixelX()
        y = ras.rasterUnitsPerPixelY()
        return x, y

    def __call__(self, *args, **kwargs):
        print('Class Info: <type> = QgsMaster (inherits from qgis.core and e_geocalc.QgsHandle).')





