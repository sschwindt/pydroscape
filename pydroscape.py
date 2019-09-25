import os, sys
print(sys.version)
print(sys.executable)

try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    sys.path.append(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(__file__) + '/data_processing/')
    sys.path.append(os.path.dirname(__file__) + '/gdal_pool/')
    sys.path.append(os.path.dirname(__file__) + '/sediment_transport/')
except:
    pass

try:
    import e_plot
    import e_xlsx
    import e_sed1d
except:
    print("ERROR: Cannot access own scripts. Check installation and write rights.")

try:
    from osgeo import gdal
    import e_geostat
except:
    print("WARNING: Cannot find osgeo and gdal. The geostatistic functions (e_geostat) are not available.")

try:
    import qgis.core
    import e_geocalc
except:
    print("Qgis.core (and therefore, e_geocalc) is not available.\nCheck QGIS instructions: https://docs.qgis.org/3.4/en/docs/pyqgis_developer_cookbook/intro.html#python-applications")

try:
    import pandas as pd
except:
    try:
        import e_data
    except:
        print("WARNING: Cannot load e_data.")
    print("Note: Cannot find pandas. The data processing function (e_data) will write data without labels.")

try:
    from gdal_pool.gdal_raster2vector import raster2vector
    from gdal_pool.gdal_vector2raster import vector2raster
    from gdal_pool.gdal_change_raster_format import float2int_overwrite
    from gdal_pool.gdal_float2int import float2int
except:
    print("WARNING: Cannot import gdal_pool scripts.")
