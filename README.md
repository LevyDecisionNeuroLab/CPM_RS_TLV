## Analysis for fMRI data
----------------------------------------------------------

In this repository we will analyze resting-state and task-based fMRI data from the  Neurobehavioral Moderators of Posttraumatic Disease Trajectories (NMPTDT) study (ClinicalTrials.gov NCT03756545)

The analysis will include cleaning of signal and extraction of time-courses, after preprocessing with fMRIprep. The cleaning folder contains a jupyter notebook that extracts two specific condound files (.1D nonsteady file and a .csv confound file), and a python script that runs the actual AFNI command. The time-courses folder includes scripts for extraction of time-courses. 

Scripts for additional analyses - connectome-based predictive modeling (CPM) - can be found here: https://github.com/asimon445/PTSD_CPM.

