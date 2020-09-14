# Preprocessing of image data and creation of persistence barcodes
##############################################################################
# We use images and select 3x3-pixel-patches.
# We normalize the patches and detect "dense" regions in the dataset.
# We use Javaplex to create persistence barcodes to determine the "shape" in these regions.


# Load necessary libraries
import numpy as np, numpy.random as npr, array, os, random, matplotlib.pyplot as plt, pandas as pd
from sklearn.neighbors import NearestNeighbors
from ripser import ripser
from persim import plot_diagrams
import matlab.engine
from barcode_creation.functions import open_file, select_patches, select_all_patches, take_subset, calc_norm
from barcode_creation.preprocess import preprocess
from barcode_creation.dense_subset import dense_subset
from barcode_creation.use_javaplex import use_javaplex
from barcode_creation.save_intervals import save_intervals


#################################################################################
# 1) Try to reproduce analysis from "On the Local Behavior of Spaces of Natural Images"

# 1.1) Select randomly 5000 3x3-patches from each image, keep 20% of patches with highest D-norm 
# --> 4.167*10^6 patches
data = pd.DataFrame() 
path = "VanHateren_Images\\"
for file in os.listdir((path)): # contains pixel data from all images
    img = open_file(path, file)
    patches_img = select_patches(img, 5000) # randomly select 5000 patches from each image
    data = data.append(patches_img)
data = data.sort_values(by = "D_Norm", ascending = False).reset_index(drop=True)
data = data.loc[range(int(round(len(data)*0.2)))] # select 20% of patches with highest contrast

# 1.2) Normalize patches by subtracting mean and dividing by D-norm, change basis 
# --> percentage*4.167*10^6 patches on 7-dimensional sphere
data = preprocess(data)

# 1.3) Select dense subset of 10% 
# --> could either use angular distance or euclidean distance to measure density
# For angular distance: We need to take a smaller subset of the data due to computational complexity 
dense_data_angular = dense_subset(take_subset(data, 15), 15)
dense_data_eucl = dense_subset(data, 100, angular = False)

# 1.4) Javaplex
# Use Javaplex in Matlab to determine the persistence barcodes
# --> play with parameters for variation of results
use_javaplex(take_subset(dense_data_angular, 10), "Dense Subset Angular euclmat ", angular = False)
use_javaplex(take_subset(dense_data_eucl, 1.5), "Dense Subset All euclmat  ", angular = False)

use_javaplex(take_subset(dense_data_angular, 10), "Dense Subset Angular randomlandmark ")
use_javaplex(take_subset(dense_data_eucl, 1.5), "Dense Subset All randomlandmark ")

super_dense_data = dense_data_eucl.head(round(len(dense_data_eucl)*0.3))
use_javaplex(take_subset(super_dense_data, 5), "Super Dense Subset 3% ")


#####################################################################################
# 2) Use similar precedure to determine persistence barcodes for morphed and original passport photos
# Do not only save barcodes as pictures but also as intervals in a table (--> save_intervals)
# --> we can use the intervals for further processing with machine learning techniques
from PIL import Image

# 2.1) For morphed images
path = "Morphed_Images\\"
for file in os.listdir((path)): # contains pixel data from all images
    print(file)
    img = Image.open(path+file).convert('L')  # convert image to 8-bit grayscale
    width, height = img.size
    img = np.array(img.getdata()).reshape(height, width)
    data = select_all_patches(img)
    data = data.sort_values(by = "D_Norm", ascending = False).reset_index(drop=True)
    data = data.loc[range(int(round(len(data)*0.2)))] # select 20% of patches with highest contrast
    # 2.2) 
    data = preprocess(data)
    # 2.3) 
    dense_data = dense_subset(data, 10, angular = False)
    # 2.4)
    name = "".join(letter for letter in [file[i] for i in [0,1,2]]) + "+" + "".join(letter for letter in [file[i] for i in [7,8,9]])
    intervals = use_javaplex(take_subset(dense_data, 50), name)
    save_intervals(name, intervals)


# 2.1) For original images (same precedure only different name for image title)
path = "Original_Images\\"
for file in os.listdir((path)): # contains pixel data from all images
    print(file)
    img = Image.open(path+file).convert('L')  # convert image to 8-bit grayscale
    width, height = img.size
    img = np.array(img.getdata()).reshape(height, width)
    data = select_all_patches(img)
    data = data.sort_values(by = "D_Norm", ascending = False).reset_index(drop=True)
    data = data.loc[range(int(round(len(data)*0.2)))] # select 20% of patches with highest contrast
    # 2.2) 
    data = preprocess(data)
    # 2.3) 
    dense_data = dense_subset(data, 10, angular = False)
    # 2.4)
    name = "".join(letter for letter in [file[i] for i in [0,1,2]])
    intervals = use_javaplex(take_subset(dense_data, 50), name)
    save_intervals(name, intervals)
