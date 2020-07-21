# Load necessary libraries
import numpy as np, numpy.random as npr, array, os, random, matplotlib.pyplot as plt, pandas as pd
from sklearn.neighbors import NearestNeighbors
from ripser import ripser
from persim import plot_diagrams
import matlab.engine

# Calculate angular distance between patches, only compute "half" of the symmetric matrix
def calculate_distance_matrix(data, angular): 
    print(angular)
    patches = list(data["Patch"])
    distances = np.zeros((len(patches), len(patches)))
    for i in range(len(patches)):
        if i in [1000,2000,3000,4000,5000,6000,7000,10000, 20000, 30000, 40000, 50000, 60000]:
            print(i)
        for j in range(i):
            distance = np.arccos(patches[i].dot(patches[j])) if angular==True else np.linalg.norm(patches[i]-patches[j]) # angular or Euclidean distance
            distances[i][j] = distance
    return distances

# Use Javaplex in MatLab
def use_javaplex(data, name, angular=True):
    distance_matrix = calculate_distance_matrix(data, angular)
    eng = matlab.engine.start_matlab("-desktop")
    eng.cd(r"C:\\Users\\Lina\\Google Drive\\Masterarbeit\\Matlab")
    max_dimension = 3
    max_filtration_value = 0.6
    num_divisions = 30
    nu = 1
    eng.calculate_intervals(matlab.double(distance_matrix.tolist()), 
                            max_dimension, 
                            max_filtration_value, 
                            num_divisions, 
                            nu,
                            name)
    eng.quit()