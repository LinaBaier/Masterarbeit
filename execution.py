# Load necessary libraries
import numpy as np, numpy.random as npr, array, os, random, matplotlib.pyplot as plt, pandas as pd
from sklearn.neighbors import NearestNeighbors
from ripser import ripser
from persim import plot_diagrams
import matlab.engine

from functions import open_file, select_patches
from preprocess import preprocess
from dense_subset import dense_subset
from use_javaplex import use_javaplex


# Take a smaller subset due to computational complexity of knn
def take_subset(data, percentage):
    no_datapoints = int(round(len(data) * percentage / 100))
    random_list = npr.choice(range(len(data)), no_datapoints, replace = False)
    indeces = [data.index[i] for i in random_list] 
    return data.loc[indeces]

'''
# 1) Try to reproduce analysis from "On the Local Behavior of Spaces of Natural Images"

# 1.1) Select randomly 5000 3x3-patches from each image, keep 20% of patches with highest D-norm --> 4.167*10^6 patches
data = pd.DataFrame()
path = "D:\\vanhateren_imc\\"
for file in os.listdir((path)): # contains pixel data from all images
    img = open_file(path, file)
    patches_img = select_patches(img, 5000) # randomly select 5000 patches from each image
    data = data.append(patches_img)
data = data.sort_values(by = "D_Norm", ascending = False).reset_index(drop=True)
data = data.loc[range(int(round(len(data)*0.2)))] # select 20% of patches with highest contrast

# 1.2) Normalize patches by subtracting mean and dividing by D-norm, change basis --> percentage*4.167*10^6 patches on 7-dimensional sphere
data = preprocess(data)

# 1.3) Select dense subset of 10% --> could either use angular distance or euclidean distance to measure density
# For angular distance: We need to take a smaller subset of the data due to computational complexity 
dense_data_angular = dense_subset(take_subset(data, 15), 15)
dense_data_eucl = dense_subset(data, 100, angular = False)
# Tried to reduce noise by substituting patch by mean of its nearest neighbors but it did not change the results 
'''

dense_data_angular = pd.read_pickle("dense_data_angular.pkt")
dense_data_eucl = pd.read_pickle("dense_data_all_100.pkt")
# 1.4) MatLab
#use_javaplex(take_subset(dense_data_angular, 10), "Dense Subset Angular euclmat ", angular = False)
#use_javaplex(take_subset(dense_data_eucl, 1.5), "Dense Subset All euclmat  ", angular = False)

use_javaplex(take_subset(dense_data_angular, 10), "Dense Subset Angular randomlandmark ")
use_javaplex(take_subset(dense_data_eucl, 1.5), "Dense Subset All randomlandmark ")