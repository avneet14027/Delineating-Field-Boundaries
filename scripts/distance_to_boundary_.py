import rasterio
import numpy as np


file = "D:/DHI/SampleData/distance_to_boundary/03.tif"
profile_template = None
with rasterio.open(file) as src:
    data = src.read()
    profile_template = src.profile.copy()

file2 = "D:/DHI/SampleData/boundary/S2_32VNH_202003_boundary.tif"
with rasterio.open(file2) as src:
    data2 = src.read()

data_flipped = np.ones(data2.shape)
data_temp = (data_flipped - data2)

print(data_temp==data2)

print(np.max(data_temp))
print(np.min(data_temp))

new_data = data2 * data

print(new_data.shape)
print(np.max(new_data))
print(np.min(new_data))

with rasterio.open('D:/DHI/result__.tif', 'w', **profile_template) as dst:
        dst.write(new_data.astype('float32'))