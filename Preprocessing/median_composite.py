import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import os
from glob import glob

"""#img1 = "D:/DHI/NewData/S2_32VNH_20200301/S2_32VNH_20200301_B02.tif"
img2 = "D:/DHI/NewData/S2_32VNH_20200305/S2_32VNH_20200305_B02.tif"
img3 = "D:/DHI/NewData/S2_32VNH_20200311/S2_32VNH_20200311_B02.tif"

files = [img2, img3]

profile_template = None

for file in files:
    with rasterio.open(file) as src:
        if not profile_template:
            profile_template = src.profile.copy()
            merged = src.read()
        else:
            data = src.read()		
            merged = np.concatenate((merged, data), axis=0)

print(merged)
print(merged.shape)
print(np.argwhere(np.isnan(merged)))
print(np.isnan(merged))
med = np.array([np.median(merged, axis=0)])
print(np.array([med]))
print(med[0][0])

profile_template.update({
	   	'count': 1, # number of bands
})


with rasterio.open('D:/DHI/test_23.tif', 'w', **profile_template) as dst:
		dst.write(med.astype('uint16'))
"""

def compute_median(merged,window_size=400):

	channels,rows,cols = merged.shape
	#print(channels,rows,cols)

	median = np.zeros((10980,10980),dtype=np.float32)

	for i in range(0,rows-window_size,window_size):
		for j in range(0,cols-window_size,window_size):
			#print(i,j)
			subimage = merged[:,i:i+window_size,j:j+window_size]
			submedian = np.ma.median(subimage,axis=0)
			#print(submedian.shape)
			median[i:i+window_size,j:j+window_size] = submedian

	print(np.max(median),np.min(median))
	return median


alldata = "D:\\DHI\\Data_12\\S2_32VNJ*/"
alldirectories = glob(alldata)
print(alldirectories)

groupByMonth = {}
for directory in alldirectories:

	dir_ = directory.split("\\")[-2]
	date = dir_.split("_")[-1].replace("\\","")
	month = date[4:6]
	year = date[0:4]

	dir_ = '_'.join(dir_.split("_")[0:2])

	key =  dir_ + "_" + year + month
	if key in groupByMonth.keys():
		groupByMonth[key].append(directory)
	else:
		groupByMonth[key] = [directory]

print(groupByMonth.keys())
	
print("\n\n\n")

for DATADIR in groupByMonth.keys():
	
	print(DATADIR)
	#DATADIR = DATADIR + "\\*/"

	#DATADIR = "D:\\DHI\\DataUpdated\\{Month}\\*/"

	bands = ['B02','B03','B04','B08']

	directories = groupByMonth[DATADIR]
	print("dates within month:",directories)

	
	monthly_composite = None
	count = 0
	for band in bands: 
		profile_template = None
		for directory in directories:
			print("single date one band:",directory) 
			#month = directory.split("_")[-1][4:6]
			#print(month)
			file = glob(f'{directory}/*{band}.tif')[0]
			print(file)
			with rasterio.open(file) as src:
				if not profile_template:
					profile_template = src.profile.copy()
					merged = np.ma.array([src.read(1, masked=True)])
				else:	
					data = np.ma.array([src.read(1, masked=True)])
					#print(data.shape)	
					merged = np.ma.concatenate((merged, data), axis=0)
					print(merged.shape)

		median = compute_median(merged)	
		print(median.shape)
		median = np.expand_dims(median,axis=0)
	
		#median = np.ma.array([np.ma.median(merged, axis=0)])
		#print(median.shape)
		
	
		if(monthly_composite) is None:
			monthly_composite = median
		else:
			monthly_composite = np.ma.concatenate((monthly_composite, median), axis = 0)
		#print(np.nonzero(monththly_composite))
		print(median.shape)
		print(merged.shape)
		print(monthly_composite.shape)

		
	profile_template.update({
	   	'count': 4, # number of bands
	})

	monthly_composite = monthly_composite.astype('uint16')
	monthly_composite.dtype
	

	OUTDIR = 'D:/DHI/Data_Composites/' + '_'.join(DATADIR.split("_")[0:2])
	if not os.path.exists(OUTDIR):
		os.makedirs(OUTDIR)
	composite_name =  OUTDIR + '/' + DATADIR + '.tif'
	print(composite_name)
	# writing the merged product
	with rasterio.open(composite_name, 'w', **profile_template) as dst:
		dst.write(monthly_composite.astype('uint16'))
	

