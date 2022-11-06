#!/bin/bash
#SBATCH --partition=general
#SBATCH -J nonSteadyAFNI # name of your experiment
#SBATCH --output=afni_non.txt
#SBATCH --error=afni_non.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=5 # should correspond to number of tasks in the python file.
#SBATCH --mem-per-cpu=8G
#SBATCH -t 24:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=or.duek@yale.edu # change to your email


echo "Running script"

module load miniconda
module load AFNI


conda activate neuroAnalysis # change to an enviroment that has nipype installed

python /home/oad4/CPM_RS_TLV/cleaning/afni_cleaning_nipype.py