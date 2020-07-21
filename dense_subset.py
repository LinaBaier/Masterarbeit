# Load necessary libraries
import numpy as np, numpy.random as npr, array, os, random, matplotlib.pyplot as plt, pandas as pd
from sklearn.neighbors import NearestNeighbors
from ripser import ripser
from persim import plot_diagrams
import matlab.engine

# Use angular distance since patches lie on 7-dimensional sphere after preprocessing 
def angular_distance(patch1, patch2):
    return np.arccos(patch1.dot(patch2))

# Choose dense subspace by looking at angular distance to kth nearest neighbor for each patch
def dense_subset(data, no_neighbors, angular=True):
    percentage = 10
    patches = list(data["Patch"])
    if angular:
        print("angular distance")
        nbrs = NearestNeighbors(n_neighbors=no_neighbors+1, metric = angular_distance).fit(patches) # kd_tree not available for customized metric
    else:
        print("euclidean distance")
        nbrs = NearestNeighbors(n_neighbors=no_neighbors+1, metric = "euclidean", algorithm = "kd_tree").fit(patches) # much faster 
    distances = nbrs.kneighbors(patches)[0]
    distances_knn = [dist[no_neighbors] for dist in distances]
    data_distances_knn = data.copy()
    data_distances_knn["Distance_knn"] = distances_knn
    data_distances_knn = data_distances_knn.sort_values(by = "Distance_knn").reset_index()
    data_dense = data_distances_knn.loc[range(int(round(len(data)*percentage/100)))]
    data_dense.index = data_dense["index"]
    data_dense = data_dense.drop(columns = "index")
    return data_dense

# Calculate angular distance between patches, only compute "half" of the symmetric matrix
def calculate_distance_matrix(data): 
    patches = list(data["Patch"])
    distances = np.zeros((len(patches), len(patches)))
    for i in range(len(patches)):
        if i in [1000,2000,3000,4000,5000,6000,7000,10000, 20000, 30000, 40000, 50000, 60000]:
            print(i)
        for j in range(i):
            distance = angular_distance(patches[i], patches[j])
            distances[i][j] = distance
    return distances

'''
# Denoise data by substituting each patch by the mean of its knn
def denoise(data, no_neighbors):
    patches = [patch.reshape(9) for patch in data["Patch"]]
    nbrs = NearestNeighbors(n_neighbors=no_neighbors+1, algorithm="kd_tree", metric = "minkowski", p=2).fit(patches)
    indeces_neighbors = nbrs.kneighbors(patches)[1]
    indeces_neighbors = [index[range(1, no_neighbors+1)] for index in indeces_neighbors]
    patches_means = []
    for indeces in indeces_neighbors:
        patches_mean = sum([patches[i] for i in indeces]) / no_neighbors
        patches_means.append(patches_mean)
    data_means = data.copy()
    data_means["Patch"] = patches_means
    return data_means
'''
