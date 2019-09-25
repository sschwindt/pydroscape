# Import gdal
from osgeo import gdal


def float2int_overwrite(src_raster, dst_raster):
    """
    Similar to float2int: Converts Float number pixels of a GeoTiff raster in Integer numbers
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

    # Output to new format
    dst_ds = driver.CreateCopy(dst_raster, src_ds, 0)

    # Properly close the datasets to flush to disk
    dst_ds = None
    src_ds = None
