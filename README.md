# Introduction
`pydroscape` constitutes Python3 functions for many sorts of river-related analyses, including tools for geodata statistics, plotting and processing of other data.

Installed as local package, the functionalities can be accessed in Python with `pydroscape.e_...`, where the following functions are available:

* `e_geostat`: Calculate raster statistics and correlation between two rasters. [More ...][5]
* `e_geocalc`: Performs raster calculations. [More ...][9]
* `e_plot`: x-y, 2D (heatmap), and 3D plots with numpy and matplotlib. [More ...][3]
* `e_xlsx`: Process workbooks. [More ...][4]
* `e_data`: Process experimental data recorded with any kind of data logger. [More ...][6]
* `e_sed1d`: Calculate sediment transport based on 1D cross-section-averaged hydraulic simulations. [More ...][7]


# Requirements
 * Python 3.x 
 * Basic packages: `numpy`, `matplotlib`, `openpyxl`
 * Supplemental packages (required by some functions only): `pandas`, `qgis.core`, `osgeo` (`gdal`)
 
`pydroscape` exclusively uses freely available packages and software (among others: QGIS).

# Usage

Example for reading matrix data from a workbook and plotting the data on a heatmap:

```python
import pydroscape as pye
a_workbook = pye.e_xlsx.read_book('D:/Documents/a_workbook.xlsx')
a_workbook_data_matrix = workbook.read_matrix(start_col='C', start_row=4)  # reads all coherent data from a workbook

a_plot = pye.e_plot.Plotter()
a_plot.make_heatmap(a_workbook_data_matrix, x_data_labels, y_data_labels)  # creates and saves the heatmap

```

Example for geocalculations:
```python
import pydroscape.e_geocalc as psgc

input_raster1_dir = '/home/rasters/raster_1.tif'  # (or in Windows: 'D:/GeoData/Rasters/raster_1.tif')
input_raster2_dir = '/home/rasters/another_raster.tif'  # (or in Windows: 'D:/GeoData/Rasters/another_raster.tif')

ref_raster1 = 'raster_1@1' # (or more general: input_raster1_dir.split('/')[-1] + '@1')
ref_raster2 = 'another_raster@1' # (or more general: input_raster2_dir.split('/')[-1] + '@1')

expression = '("' + ref_raster1 "' > 0) * ("' ref_raster1 '" + "' ref_raster2 '")'

geo_container = psgc.QgsHandle()
output_ras = 'home/rasters/result.tif'
geo_container.calculate_raster(expression, output_ras, [raster_1, raster_2])

```

Example for 1D cross-section and reach-averaged sediment transport:
```python
import pydroscape.e_sed1d as pss

method = 'mpm'  # other options for method: 'AW', 'AWmod', 'Rec13' (upper and lower case do not matter)

sediment_container = pss.SedimentTransport1D(False)  # the BOOL=False argument initiates e_sed1D with messages (silence=False)
sediment_container.set_input_file_directory(os.path.dirname(__file__) + '/sample_data/text/sediment_calculation_1D/')
sediment_container.set_output_file_directory(os.path.dirname(__file__) + '/output/')
sediment_container.calculate(method)

```

# Documentation
The [Wiki][1] contains details about installing and using `pydroscape`.

[1]: https://github.com/sschwindt/pydroscape/wiki/home 
[3]: https://github.com/sschwindt/pydroscape/wiki/Plot-functions
[4]: https://github.com/sschwindt/pydroscape/wiki/Workbook-handling
[5]: https://github.com/sschwindt/pydroscape/wiki/Geostatistics
[6]: https://github.com/sschwindt/pydroscape/wiki/Data-processing-(non-geo)
[7]: https://github.com/sschwindt/pydroscape/wiki/Utility-functions
[8]: https://github.com/sschwindt/pydroscape/wiki/Sediment-transport-1D
[9]: https://github.com/sschwindt/pydroscape/wiki/Geocalculations
