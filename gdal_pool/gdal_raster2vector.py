from osgeo import gdal, ogr, osr
import sys
import os


def raster2vector(src_raster, target_dir, dst_layername, field_name="gridcode"):
    """
    Converts src_raster to a polygon shapefile in target dir
    WARNING: FUNCTION NOT YET FULLY TESTED - MAY NOT WORK UNDER ALL CIRCUMSTANCES
    :param src_raster: STR of full directory of a source raster
    :param target_dir: STR of the directory where the shapefile will be created
    :param dst_layername: STR of new shapefile name (without .shp ending)
    :param field_name: STR of fieldname for raster value storage
    :return: None
    """
    gdal.UseExceptions()

    # Go to target dir
    os.chdir(target_dir)

    # Open source
    src_ds = gdal.Open(src_raster)
    if src_ds is None:
        print('Unable to open %s' % src_raster)
        sys.exit(1)
    src_band = src_ds.GetRasterBand(1)

    # Checkout driver
    drv = ogr.GetDriverByName("ESRI Shapefile")

    # Make new shapefile
    dst_ds = drv.CreateDataSource(dst_layername + ".shp")

    # Get coordinate system from source raster
    srs = osr.SpatialReference()
    srs.ImportFromWkt(src_ds.GetProjection())

    dst_layer = dst_ds.CreateLayer(dst_layername, srs=srs)
    new_field = ogr.FieldDefn(field_name, ogr.OFTInteger)
    dst_layer.CreateField(new_field)

    gdal.Polygonize(src_band, None, dst_layer, 0, [], callback=None)
