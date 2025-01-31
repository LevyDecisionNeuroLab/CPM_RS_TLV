## Analysis for fMRI data
----------------------------------------------------------

In this repository we will analyze resting-state and task-based fMRI data from the  Neurobehavioral Moderators of Posttraumatic Disease Trajectories (NMPTDT) study (ClinicalTrials.gov NCT03756545)

The analysis will include cleaning of signal, after preprocessing with fMRIprep. We will then perform connectome-based predictive modeling (CPM).

The cleaning folder contains a jupyter notebook that extracts two specific condound files (.1D nonsteady file and a .csv confound file), and a python script that runs the actual AFNI command.
