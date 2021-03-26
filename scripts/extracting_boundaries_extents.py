import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from pathlib import Path
import affine
from rasterio import features

import matplotlib.pyplot as plt
from rasterio.plot import reshape_as_image
from rasterio.windows import Window

image_file = 'D:/DHI/composites/08_test_composite.tif'
with rasterio.open(image_file) as src:
    image = src.read()

print(image.shape)


parcel_data_shp = gpd.read_file('D:/DHI/Parcels/2020/all-crops-32VNH-extract.shp')

def shp_to_tif(gdf, dx, dy, transform, all_touched=True):

    xmin, ymin, xmax, ymax = gdf.total_bounds

    width = int(np.ceil((xmax - xmin) / dx))
    height = int(np.ceil((ymin - ymax) / dy))
    shape = (height, width)
    
    print(width,height)
    print(transform)

    if transform:
        pass
    else:
        transform = affine.Affine(dx, 0, xmin, 0, dy, ymax)
    image = features.rasterize(
        shapes=((g, 1) for g in gdf.geometry),
        out_shape=(10980, 10980),
        transform=transform,
        all_touched=all_touched
    )
    return ((image,width,height,transform))

extent = shp_to_tif(parcel_data_shp, 10, -10, rasterio.open(image_file).transform, all_touched=False)
boundary = shp_to_tif(parcel_data_shp.geometry.boundary, 10, -10, transform=rasterio.open(image_file).transform, all_touched=True)

print(type(extent))
print(boundary)

with rasterio.open('D:/DHI/SampleData/extent/S2_32VNH_202008_extent.tif','w',driver='GTiff',height=extent[2],width=extent[1],count=1,dtype=extent[0].dtype,transform=extent[3]) as dst:
		dst.write(extent[0],1)

with rasterio.open('D:/DHI/SampleData/boundary/S2_32VNH_202008_boundary.tif','w',driver='GTiff',height=boundary[2],width=boundary[1],count=1,dtype=boundary[0].dtype,transform=extent[3]) as dst:
		dst.write(boundary[0],1)