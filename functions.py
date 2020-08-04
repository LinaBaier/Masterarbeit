# Load necessary libraries
import numpy as np, numpy.random as npr, array, os, random, matplotlib.pyplot as plt, pandas as pd
from sklearn.neighbors import NearestNeighbors
from ripser import ripser
from persim import plot_diagrams
import matlab.engine

# Open file that contains pixel values of an image
def open_file(path, file):
    with open(path+file, 'rb') as handle:
       s = handle.read()
    arr = array.array('H', s)
    arr.byteswap()
    img = np.array(arr, dtype='uint16').reshape(1024, 1536)
    return img
    
# Calculate D-norm for a 3x3 Patch 
def calc_norm(patch):
    patch = patch.reshape(9,1)
    D = np.array([[2, -1, 0, -1, 0, 0, 0, 0, 0], 
              [-1, 3, -1, 0, -1, 0, 0, 0, 0],
              [0, -1, 2, 0, 0, -1, 0, 0, 0],
              [-1, 0, 0, 3, -1, 0, -1, 0, 0],
              [0, -1, 0, -1, 4, -1, 0, -1, 0], 
              [0, 0, -1, 0, -1, 3, 0, 0, -1],
              [0, 0, 0, -1, 0, 0, 2, -1, 0],
              [0, 0, 0, 0, -1, 0, -1, 3, -1],
              [0, 0, 0, 0, 0, -1, 0, -1, 2]
             ])
    return np.sqrt(float(np.transpose(patch).dot(D).dot(patch)))
  
# Select 5000 patches from an image
def select_patches(img, no_patches): # randomly select 5000 patches in each image
    patches = []
    D_norms = []
    all_coords = [str(i) + ' ' + str(j) for i in range(2,1021) for j in range(2,1533)]
    npr.seed(123) # replicability of random selection
    coords =  npr.choice(all_coords, no_patches, replace = False) # upper left corner of patch
    for coord in coords:
        coord = coord.split()
        x, y = int(coord[1]), int(coord[0])
        patch = np.array([[img[y+c][x] for c in [0, 1, 2]],
                         [img[y+c][x+1] for c in [0, 1, 2]],
                         [img[y+c][x+2] for c in [0, 1, 2]]])
        patch = np.log(patch)
        D_norm = calc_norm(patch) 
        patches.append(patch)
        D_norms.append(D_norm)
    return pd.DataFrame(dict(Patch = patches, D_Norm = D_norms))

# Select all patches
def select_all_patches(img): 
    patches = []
    D_norms = []
    x_max, y_max = len(img[0])-2, len(img)-2
    for x in range(x_max):
        for y in range(y_max):
            patch = np.array([[img[y+c][x] for c in [0, 1, 2]],
                             [img[y+c][x+1] for c in [0, 1, 2]],
                             [img[y+c][x+2] for c in [0, 1, 2]]])
            patch = np.log(patch)
            D_norm = calc_norm(patch)
            patches.append(patch)
            D_norms.append(D_norm)
    return pd.DataFrame(dict(Patch = patches, D_Norm = D_norms))

# Plot the image
def plot_pixels(img):
    plt.imshow(img, cmap="gray")
    plt.show()

# Take a smaller subset due to computational complexity of knn
def take_subset(data, percentage):
    no_datapoints = int(round(len(data) * percentage / 100))
    random_list = npr.choice(range(len(data)), no_datapoints, replace = False)
    indeces = [data.index[i] for i in random_list] 
    return data.loc[indeces]
