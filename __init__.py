import os, sys
print(sys.version)
print(sys.executable)

try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    sys.path.append(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(__file__) + '/data_processing')
except:
    pass

try:
    import logging
    logging.basicConfig(filename='logfile.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.StreamHandler().setLevel(logging.DEBUG)
    logging.StreamHandler().setFormatter("%(asctime)s - %(message)s")
    logging.addLevelName(logging.INFO, '*INFO')
    logging.addLevelName(logging.WARNING, '!WARNING')
    logging.addLevelName(logging.ERROR, '!ERROR')
except:
    print("LOGGING ERROR: Could not start logging.")

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
    import pandas as pd
except:
    try:
        import e_data
    except:
        print("WARNING: Cannot load e_data.")
    print("Note: Cannot find pandas. The data processing function (e_data) will write data without labels.")



