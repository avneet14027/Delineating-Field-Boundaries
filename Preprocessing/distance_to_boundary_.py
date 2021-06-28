import rasterio
import numpy as np
import os

extents = "D:/DHI/Data_EBD/extents/S2_32VNJ/"
distances = "D:/DHI/Data_EBD/distance/S2_32VNJ/"
tilename = "/S2_32VNJ/"
OUTDIR = "D:/DHI/Data_EBD/distances"

extents_ = os.listdir(extents)
distances_ = os.listdir(distances)

for i in range(0,len(extents_)):
	extent = extents + extents_[i]
	distance = distances + distances_[i]

	filename = extents_[i]

	profile_template = None
	with rasterio.open(extent) as src:
	    data_extent = src.read()
	    profile_template = src.profile.copy()
	    print(data_extent.shape)

	with rasterio.open(distance) as src:
		data_distance = src.read()
		print(data_distance.shape)

	computed_distance = data_extent * data_distance
	print(computed_distance.shape)

	print(np.min(computed_distance))
	print(np.max(computed_distance))
	new_data_ = (computed_distance - np.min(computed_distance )) / (np.max(computed_distance) - np.min(computed_distance))

	OUTFILE = OUTDIR + "/" + tilename + "/" + filename

	if not os.path.exists((OUTDIR + "/" + tilename)):
		os.makedirs((OUTDIR + "/" + tilename))

	print(OUTFILE)
	profile_template.update(
        dtype=rasterio.float32)
	with rasterio.open(OUTFILE, 'w', **profile_template) as dst:
		dst.write(new_data_)

'''
file = "D:/DHI/SampleData/distance/S2_32VNH_202008_distance.tif"
profile_template = None
with rasterio.open(file) as src:
    data = src.read()
    profile_template = src.profile.copy()

file2 = "D:/DHI/SampleData/extent/S2_32VNH_202008_extent.tif"
with rasterio.open(file2) as src:
    data2 = src.read()


new_data = data * data2
print(new_data.shape)

print(np.min(new_data))
print(np.max(new_data))
new_data_ = (new_data - np.min(new_data)) / (np.max(new_data) - np.min(new_data))

with rasterio.open('D:/DHI/DataForTraining/S2_32VNH_202008_distance.tif', 'w', **profile_template) as dst:
        dst.write(new_data_.astype('float32'))
'''