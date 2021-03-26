#import fiona
import geopandas as gpd
import matplotlib.pyplot as plt
#import numpy as np
from pathlib import Path
import rasterio
#import shapely
#import pandas as pd
#from shapely.geometry import LineString

from eobox.sampledata import get_dataset
from eobox.vector import calc_distance_to_border


file = "D:/DHI/composites/03_test_composite.tif"

"""profile_template = None
with rasterio.open(file) as src:
    if not profile_template:
        profile_template = src.profile.copy()
        template_file_raster = src.read()


print(template_file_raster.shape)
print(profile_template)"""


#src_file_vector = gpd.read_file('D:/DHI/Parcels/2020/all-crops-32VNH-extract.shp')

ds = get_dataset('s2l1c')

src_file_vector = ds['vector_file_osm']

print(((src_file_vector)))

template_file_raster = ds['raster_files'][0]
print(((template_file_raster)))


interim_file_lines = "D:/DHI/distance_from_boundary/_interim_sample_vector_dataset_lines.shp"
interim_file_lines_raster = "D:/DHI/distance_from_boundary/_interim_sample_vector_dataset_lines_raster.tif"

dst_file_proximity = "D:/DHI/distance_from_boundary/03_12.tif"

calc_distance_to_border(polygons=src_file_vector,
                        template_raster=template_file_raster,
                        dst_raster=dst_file_proximity,
                        overwrite=False,
                        keep_interim_files=True)  # stores the vector and rasterized lines

r_d2b = rasterio.open(dst_file_proximity)
print(r_d2b)