from osgeo import ogr, gdal
import subprocess, os


def vector2raster(input_shp, output_dir, output_raster_name, reference_raster, gdalformat='GTiff', burn_value=1):
    """
    Rasterize a shapefile to the same projection and pixel resolution as a reference image
    WARNING: FUNCTION NOT YET FULLY TESTED - MAY NOT WORK UNDER ALL CIRCUMSTANCES
    :param input_shp: STR of full directory to a shapefile
    :param output_raster: STR of full directory for the new raster
    :param reference_raster: STR of full directory to the reference image raster
    :param gdalformat: STR - either 'GTiff'
    :param burn_value: FLOAT / INT value for the output image pixels
    :return: None
    """
    os.chdir(output_dir)

    datatype = gdal.GDT_Byte

    # Get projection info from reference image
    ref_image = gdal.Open(reference_raster, gdal.GA_ReadOnly)

    # Open Shapefile
    shp_file = ogr.Open(input_shp)
    shp_file_layer = shp_file.GetLayer()

    # Rasterize
    print("Rasterizing shapefile...")
    output_raster = os.path.join(output_dir, output_raster_name)
    out_ras = gdal.GetDriverByName(gdalformat).Create(output_raster, ref_image.RasterXSize, ref_image.RasterYSize, 1,
                                                      datatype, options=['COMPRESS=DEFLATE'])
    print("Retrieving projection...")
    out_ras.SetProjection(ref_image.GetProjectionRef())
    print("Setting transformation...")
    out_ras.SetGeoTransform(ref_image.GetGeoTransform())

    # Write data to band 1
    out_band = out_ras.GetRasterBand(1)
    out_band.SetNoDataValue(0)
    gdal.RasterizeLayer(out_ras, [1], shp_file_layer, burn_values=[burn_value])

    # Close datasets
    out_band = None
    out_ras = None
    ref_image = None
    shp_file = None

    # Build image overviews
    subprocess.call("gdaladdo --config COMPRESS_OVERVIEW DEFLATE " + output_raster + " 2 4 8 16 32 64", shell=True)
    print("Done.")
