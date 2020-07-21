# Load necessary libraries
import numpy as np, numpy.random as npr, array, os, random, matplotlib.pyplot as plt, pandas as pd
from sklearn.neighbors import NearestNeighbors
from ripser import ripser
from persim import plot_diagrams
import matlab.engine
from functions import calc_norm

# Normalize patches by subtracting their means and dividing by their D-norms
def normalize(data):
    patches = [patch.reshape(9) for patch in data["Patch"]]
    patches_normalized = []
    for patch in patches:
        patch -= np.mean(patch)
        patch /= calc_norm(patch)
        patches_normalized.append(patch)
    data_normalized = data.copy()
    data_normalized["Patch"] = patches_normalized
    return data_normalized

# Change the basis to place the data on a 7-dimensional sphere
def change_basis(data):
    patches = [patch.reshape(9) for patch in data["Patch"]]
    b1 = 1/np.sqrt(6) * np.array([1, 0, -1, 1, 0, -1, 1, 0, -1])
    b2 = 1/np.sqrt(6) * np.array([1, 1, 1, 0, 0, 0, -1, -1, -1])
    b3 = 1/np.sqrt(54) * np.array([1, -2, 1, 1, -2, 1, 1, -2, 1])
    b4 = 1/np.sqrt(54) * np.array([1, 1, 1, -2, -2, -2, 1, 1, 1])
    b5 = 1/np.sqrt(8) * np.array([1, 0, -1, 0, 0, 0, -1, 0, 1])
    b6 = 1/np.sqrt(48) * np.array([1, 0, -1, -2, 0, 2, 1, 0, -1])
    b7 = 1/np.sqrt(48) * np.array([1, -2, 1, 0, 0, 0, -1, 2, -1])
    b8 = 1/np.sqrt(216) * np.array([1, -2, 1, -2, 4, -2, 1, -2, 1])
    B = np.array([b1, b2, b3, b4, b5, b6, b7, b8]).transpose()
    B_inv = np.linalg.pinv(B)
    data_basis = data.copy()
    data_basis["Patch"] = [B_inv.dot(patch) for patch in patches]
    return data_basis

# Combine those steps
def preprocess(data):
    data = normalize(data)
    data = change_basis(data)
    return data