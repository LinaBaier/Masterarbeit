# Load necessary libraries
import numpy as np, numpy.random as npr, array, os, random, matplotlib.pyplot as plt, pandas as pd
from sklearn.neighbors import NearestNeighbors
from ripser import ripser
from persim import plot_diagrams
import matlab.engine

from functions import open_file, select_patches, select_all_patches, take_subset
from preprocess import preprocess
from dense_subset import dense_subset
from use_javaplex import use_javaplex
from save_intervals import save_intervals



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


dense_data_angular = pd.read_pickle("C:\\Users\\Lina\\Google Drive\\Masterarbeit\\Python\\dense_data_angular.pkt")
dense_data_eucl = pd.read_pickle(""C:\\Users\\Lina\\Google Drive\\Masterarbeit\\Python\\dense_data_all_100.pkt")
# 1.4) MatLab
#use_javaplex(take_subset(dense_data_angular, 10), "Dense Subset Angular euclmat ", angular = False)
#use_javaplex(take_subset(dense_data_eucl, 1.5), "Dense Subset All euclmat  ", angular = False)

#use_javaplex(take_subset(dense_data_angular, 10), "Dense Subset Angular randomlandmark ")
#use_javaplex(take_subset(dense_data_eucl, 1.5), "Dense Subset All randomlandmark ")


dense_data_eucl = pd.read_pickle("C:\\Users\\Lina\\Google Drive\\Masterarbeit\\Python\\dense_data_all_100.pkt")
super_dense_data = dense_data_eucl.head(round(len(dense_data_eucl)*0.3))
use_javaplex(take_subset(super_dense_data, 5), "Super Dense Subset 3% ")

data_single = select_patches(img, 312500)
data_single = data_single.sort_values(by = "D_Norm", ascending = False).reset_index(drop=True)
data_single = data_single.loc[range(int(round(len(data_single)*0.2)))] 
data_single = preprocess(data_single, 100, "") 
dense_data_single_eucl = dense_subspace(data_single, 10, 15, angular=False)
dense_data_single_angular = dense_subspace(data_single, 10, 15)
'''

# 2) For Faces
from PIL import Image

# 2.1) 
a = ['001+027',
 '002+083',
 '002+102',
 '002+107',
 '004+026',
 '004+031',
 '004+128',
 '004+140',
 '004+141',
 '004+172',
 '004+173',
 '005+045',
 '005+067',
 '006+135',
 '007+100',
 '007+139',
 '009+002',
 '009+010',
 '009+083',
 '009+091',
 '009+139',
 '010+097',
 '010+134',
 '011+007',
 '011+086',
 '011+122',
 '011+144',
 '012+017',
 '012+022',
 '012+031',
 '014+013',
 '014+027',
 '014+091',
 '014+094',
 '014+122',
 '016+001',
 '016+002',
 '016+013',
 '016+039',
 '016+083',
 '016+091',
 '016+107',
 '016+124',
 '017+026',
 '017+031',
 '017+033',
 '017+063',
 '017+068',
 '017+092',
 '017+172',
 '018+004',
 '018+105',
 '018+172',
 '019+081',
 '019+086',
 '019+107',
 '019+122',
 '020+039',
 '020+081',
 '020+097',
 '022+092',
 '022+123',
 '022+130',
 '022+138',
 '022+141',
 '026+004',
 '026+031',
 '026+033',
 '026+108',
 '027+002',
 '027+014',
 '027+016',
 '027+020',
 '027+094',
 '027+097',
 '029+104',
 '029+125',
 '029+138',
 '029+141',
 '031+041',
 '031+105',
 '031+123',
 '031+128',
 '031+141',
 '032+094',
 '032+122',
 '033+063',
 '034+087',
 '036+012',
 '036+033',
 '036+103',
 '039+001',
 '039+112',
 '039+136',
 '041+031',
 '041+033',
 '041+103',
 '044+042',
 '044+061',
 '063+004',
 '063+021',
 '063+022',
 '063+026',
 '063+036',
 '063+101',
 '063+138',
 '063+173',
 '068+021',
 '068+036',
 '068+105',
 '068+138',
 '069+004',
 '069+128',
 '069+130',
 '069+173',
 '081+011',
 '081+032',
 '081+086',
 '081+091',
 '081+118',
 '081+144',
 '083+011',
 '083+136',
 '090+086',
 '091+083',
 '091+090',
 '091+124',
 '092+108',
 '094+107',
 '097+016',
 '097+019',
 '097+113',
 '100+002',
 '100+011',
 '100+107',
 '101+004',
 '101+029',
 '101+031',
 '101+036',
 '101+041',
 '101+121',
 '101+131',
 '102+020',
 '102+100',
 '103+004',
 '103+108',
 '103+125',
 '103+132',
 '103+140',
 '104+018',
 '104+026',
 '104+031',
 '104+069',
 '104+103',
 '104+108',
 '104+125',
 '104+130',
 '104+141',
 '104+172',
 '105+012',
 '105+036',
 '105+068',
 '105+108',
 '105+121',
 '105+140',
 '107+001',
 '107+032',
 '107+091',
 '107+094',
 '107+097',
 '108+004',
 '108+017',
 '108+018',
 '108+036',
 '108+138',
 '112+090',
 '112+124',
 '113+007',
 '113+014',
 '113+090',
 '113+094',
 '113+124',
 '114+044',
 '115+037',
 '117+103',
 '117+123',
 '117+130',
 '117+173',
 '118+011',
 '118+039',
 '121+017',
 '121+036',
 '121+041',
 '121+068',
 '121+103',
 '121+105',
 '121+123',
 '122+019',
 '122+102',
 '123+092',
 '125+063',
 '125+104',
 '127+034',
 '128+004',
 '128+026',
 '128+029',
 '128+041',
 '128+105',
 '128+123',
 '128+132',
 '130+021',
 '130+041',
 '130+063',
 '130+092',
 '130+117',
 '131+068',
 '131+092',
 '131+101',
 '131+121',
 '131+125',
 '131+141',
 '132+004',
 '132+017',
 '132+018',
 '132+041',
 '132+068',
 '132+101',
 '132+123',
 '132+125',
 '132+141',
 '132+173',
 '134+039',
 '134+083',
 '136+001',
 '138+004',
 '138+105',
 '139+136',
 '140+022',
 '140+029',
 '140+036',
 '140+138',
 '140+141',
 '141+004',
 '141+026',
 '141+033',
 '141+041',
 '141+103',
 '141+125',
 '141+173',
 '142+037',
 '144+007',
 '144+016',
 '144+039',
 '144+086',
 '144+102',
 '144+139',
 '172+103',
 '172+104',
 '172+131',
 '172+138',
 '172+173']
path = "C:\\Users\\Lina\\Google Drive\\Masterarbeit\\Python\\londondb_morph_combined_alpha0.5_passport-scale_15kb\\"
for file in os.listdir((path)): # contains pixel data from all images
    print(file)

    name = "".join(letter for letter in [file[i] for i in [0,1,2]]) + "+" + "".join(letter for letter in [file[i] for i in [7,8,9]])
    if name in a: 

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
    else:
        print("not in a")

'''
    # 2.1) 
path = "C:\\Users\\Lina\\Google Drive\\Masterarbeit\\Python\\test\\"
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
'''
