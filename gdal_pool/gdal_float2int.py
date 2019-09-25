from osgeo import gdal, osr


def float2int(src_raster, dst_raster):
    """
    Converts Float number pixels of a GeoTiff raster in Integer numbers
    WARNING: FUNCTION NOT YET FULLY TESTED - MAY NOT WORK UNDER ALL CIRCUMSTANCES
    :param src_raster: STR of full directory for the source raster (TIFF)
    :param dst_raster:STR of full directory for the output raster (TIFF)
    :return: None
    """
    # Open existing dataset
    src_ds = gdal.Open(src_raster)

    # Open output format driver, see gdal_translate --formats for list
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    srs = osr.SpatialReference()
    srs.ImportFromWkt(src_ds.GetProjection())

    # Output to new format
    ds = gdal.Translate(dst_raster, src_raster, projWin=src_ds.GetProjection())

    # Properly close the datasets to flush to disk
    ds = None
    src_ds = None
