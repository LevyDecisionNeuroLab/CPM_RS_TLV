## Analysis for resting-state data - comparing two datasets
----------------------------------------------------------

In this repository we will analyze RS data from TLV data (ZBZ) and AURORA study. 

The analysis will include cleaning of signal (after preprocessing)
We will then use parcellation and build a CPM model on 1 data set.
Later we will compare this one to another data set

The cleaning folder contains a jupyter notebook that extracts two specific condound files (.1D nonsteady file and a .csv confound file), and a python script that runs the actual AFNI command
