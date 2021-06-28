import fiona
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import rasterio
import shapely
import pandas as pd
from shapely.geometry import LineString

import glob
import os

from eobox.sampledata import get_dataset
from eobox.vector import calc_distance_to_border


DATADIR = "D:/DHI/Data_EBD/images/S2_32VNJ/"
OUTDIR = "D:/DHI/Data_EBD/distance/S2_32VNJ/"

src_file_vector = 'D:/DHI/Parcels/2020/all-crops-32VNJ-extract.shp'

interim_file_lines = OUTDIR +"_interim_sample_vector_dataset_lines.shp"
interim_file_lines_raster = OUTDIR + "_interim_sample_vector_dataset_lines_raster.tif"

files = os.listdir(DATADIR)
for file in files:
	print(file)
	template_file_raster = DATADIR + file

	dst_file_proximity = OUTDIR + file

	calc_distance_to_border(polygons=src_file_vector,
                        template_raster=template_file_raster,
                        dst_raster=dst_file_proximity,
                        overwrite=False,
                        keep_interim_files=True)  # stores the vector and rasterized lines

'''
template_file_raster = "D:/DHI/composites/03_test_composite.tif"


src_file_vector = 'D:/DHI/Parcels/2020/all-crops-32VNH-extract.shp'



interim_file_lines = "D:/DHI/distance_from_boundary/_interim_sample_vector_dataset_lines.shp"
interim_file_lines_raster = "D:/DHI/distance_from_boundary/_interim_sample_vector_dataset_lines_raster.tif"

dst_file_proximity = "D:/DHI/distance_from_boundary/result_test.tif"

calc_distance_to_border(polygons=src_file_vector,
                        template_raster=template_file_raster,
                        dst_raster=dst_file_proximity,
                        overwrite=False,
                        keep_interim_files=True)  # stores the vector and rasterized lines

r_d2b = rasterio.open(dst_file_proximity)
print(r_d2b)
'''