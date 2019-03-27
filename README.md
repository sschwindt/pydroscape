# Introduction
`pydroscape` constitutes Python3 functions for many sorts of river-related analyses, including tools for geodata statistics, plotting and processing of other data.

Installed as local package, the functionalities can be accessed in Python with `pydroscape.e_...`, where the following functions are available:

* `e_geostat`: Calculate raster statistics and correlation between two rasters.
* `e_plot`: x-y, 2D (heatmap), and 3D plots with numpy and matplotlib.
* `e_xlsx`: Process workbooks.
* `e_data`: _FUTURE IMPLEMENTATION_ Process experimental data recorded with any kind of data logger.


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
x_data_labels = a_workbook.read_row_str(3, 'C')
y_data_labels = a_workbook.read_column('B', 4)
a_workbook.close()

a_plot = pye.e_plot.Plotter()
a_plot.width = 6.0  # figure width in inches
a_plot.height = 9.0  # figure height in inches
a_plot.font_size = 11.0  # set font_size
a_plot.legend_active = True  # put a legend
a_plot.y_label = 'A data y label'
a_plot.colobar_label = 'Pearson r [--]'  # Define a colorbar label
a_plot.colorbar_aspect = 20  # modify a colorbar shape
a_plot.save_fig_dir = 'D:/this_is_where_I_store/figures.png'  # name of the heatmap
a_plot.make_heatmap(a_workbook_data_matrix, x_data_labels, y_data_labels)  # creates and saves the heatmap

```

# Documentation
The [Wiki][1] contains details about installing and using `pydroscape`.

[1]: https://github.com/sschwindt/pydroscape/wiki/home 
