# Masterarbeit-TDA

Code for my master's thesis "Topologische Datenanalyse: Persistente Homologie in Theorie und Praxis"

1. Barcodes: 
* execute file "barcode_creation.py" to preprocess data from images and to calculate the persistence barcodes
* method is adapted to "On the Local Behavior of Spaces of Natural Images" (Gunnar Carlsson, Tigran Ishkhanov, Vin de Silva, Afra Zomorodian)
* input data is not included in this repository, I used natural images from 
		"Independent Component Filters of Natural Images Compared with Simple Cells in Primary Visual Cortex" (van Hateren, van der Schaaf)
		and passport photos from 
		"AMSL Face Morph Image Data Set" (Universität Magdeburg)
* persistence barcodes are determined using the software package Javaplex via Matlab --> https://github.com/appliedtopology/javaplex,
    installation is required to run "barcode_creation.py"
* results for beforementioned image sets in "Results": "Barcodes_..." contains barcodes as images, "Features_Morphs+Originals" contains 0th, 1st and 2nd dimensional barcode for each image from the AMSL Face Morph Image Data Set as sets of intervals in a table
    


2. Morph_Detector:
* execute file "morph_detector.py" to build a classifier to detect morphed images
* classifier is based on features read off from "Features_Morphs+Originals", namely number, length and birth of barcodes
* random forest from Python library skicit-learn is used to build classifier --> https://github.com/scikit-learn/scikit-learn
