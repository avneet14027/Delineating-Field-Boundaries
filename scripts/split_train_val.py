import rasterio
from rasterio.windows import Window
from pathlib import Path


TRAIN_WINDOW = Window(0, 0, 10980, 8784)
VAL_WINDOW = Window(0, 8784, 10980, 2196)

DATADIR = Path('D:/DHI/SampleData/')

#read and split the image
with rasterio.open(DATADIR.joinpath('03_test_composite.tif')) as src:
    train_data = src.read(window=TRAIN_WINDOW)
    val_data = src.read(window=VAL_WINDOW)
    data_profile = src.profile.copy()

#write training data
train_profile = data_profile.copy()
train_profile.update({'height': TRAIN_WINDOW.height,
                      'width': TRAIN_WINDOW.width,
                      'transform': rasterio.windows.transform(TRAIN_WINDOW, data_profile['transform'])
                     }
                    )

with rasterio.open(DATADIR.joinpath('TrainData/03_train.tif'), 'w', **train_profile) as dst:
    dst.write(train_data)

#write test data
val_profile = data_profile.copy()
val_profile.update({'height': VAL_WINDOW.height,
                    'width': VAL_WINDOW.width,
                    'transform': rasterio.windows.transform(VAL_WINDOW, data_profile['transform'])
                   }
                  )
with rasterio.open(DATADIR.joinpath('ValidationData/03_val.tif'), 'w', **val_profile) as dst:
    dst.write(val_data)
    
#read and split the mask
with rasterio.open(DATADIR.joinpath('boundary/S2_32VNH_202003_boundary.tif')) as src:
    train_mask = src.read(window=TRAIN_WINDOW)
    val_mask = src.read(window=VAL_WINDOW)
    mask_profile = src.profile.copy()

#write training mask
train_mask_profile = mask_profile.copy()
train_mask_profile.update({'height': TRAIN_WINDOW.height,
                           'width': TRAIN_WINDOW.width,
                           'transform': rasterio.windows.transform(TRAIN_WINDOW, mask_profile['transform'])
                     }
                    )

with rasterio.open(DATADIR.joinpath('TrainData/03_train_boundary.tif'), 'w', **train_mask_profile) as dst:
    dst.write(train_mask)

#write test data
val_mask_profile = mask_profile.copy()
val_mask_profile.update({'height': VAL_WINDOW.height,
                         'width': VAL_WINDOW.width,
                         'transform': rasterio.windows.transform(VAL_WINDOW, mask_profile['transform'])
                   }
                  )
with rasterio.open(DATADIR.joinpath('ValidationData/03_val_boundary.tif'), 'w', **val_mask_profile) as dst:
    dst.write(val_mask)



# extent
# read and split the mask
with rasterio.open(DATADIR.joinpath('extent/S2_32VNH_202003_extent.tif')) as src:
    train_mask = src.read(window=TRAIN_WINDOW)
    val_mask = src.read(window=VAL_WINDOW)
    mask_profile = src.profile.copy()

#write training mask
train_mask_profile = mask_profile.copy()
train_mask_profile.update({'height': TRAIN_WINDOW.height,
                           'width': TRAIN_WINDOW.width,
                           'transform': rasterio.windows.transform(TRAIN_WINDOW, mask_profile['transform'])
                     }
                    )

with rasterio.open(DATADIR.joinpath('TrainData/03_train_extent.tif'), 'w', **train_mask_profile) as dst:
    dst.write(train_mask)

#write test data
val_mask_profile = mask_profile.copy()
val_mask_profile.update({'height': VAL_WINDOW.height,
                         'width': VAL_WINDOW.width,
                         'transform': rasterio.windows.transform(VAL_WINDOW, mask_profile['transform'])
                   }
                  )
with rasterio.open(DATADIR.joinpath('ValidationData/03_val_extent.tif'), 'w', **val_mask_profile) as dst:
    dst.write(val_mask)