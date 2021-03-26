import numpy as np
import rasterio
from pathlib import Path 

DATADIR = Path('D:/DHI/SampleData/')

with rasterio.open(DATADIR.joinpath('TrainData/03_train.tif')) as train_src:
    train_img = train_src.read()
    train_profile = train_src.profile

with rasterio.open(DATADIR.joinpath('TrainData/03_train_boundary.tif')) as boundary_src:
    boundary = boundary_src.read()
    boundary_profile = boundary_src.profile

with rasterio.open(DATADIR.joinpath('TrainData/03_train_extent.tif')) as extent_src:
    extent = extent_src.read()
    extent_profile = extent_src.profile


window = 256
stride = 64

ch, rows, cols = train_img.shape
output_crops = "D:/DHI/SampleData/train_patches/"
boundary_crops = "D:/DHI/SampleData/boundary_patches/"
extent_crops = "D:/DHI/SampleData/extent_patches/"

counter = 0
for i in range(0, rows-window, stride+1):
    for j in range(0, cols-window, stride+1):
        crop_img = train_img[:, i:i+window, j:j+window]
        boundary_img = boundary[:, i:i+window, j:j+window]
        extent_img = extent[:, i:i+window, j:j+window]

        train_profile.update(width=256, height=256)
        boundary_profile.update(width=256, height=256)
        extent_profile.update(width=256, height=256)

        filename_output = output_crops + str(i) + "_" + str(j) + ".tiff"
        filename_boundary = boundary_crops + str(i) + "_" + str(j) + ".tiff"
        filename_extent = extent_crops + str(i) + "_" + str(j) + ".tiff"


        # Save Image
        with rasterio.open(filename_output, 'w', **train_profile) as outds:
            outds.write(crop_img)

        with rasterio.open(filename_boundary, 'w', **boundary_profile) as outds:
            outds.write(boundary_img)

        with rasterio.open(filename_extent, 'w', **extent_profile) as outds:
            outds.write(extent_img)
        
    print(counter)