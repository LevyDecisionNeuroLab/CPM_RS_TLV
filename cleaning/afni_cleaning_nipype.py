
import os
import pandas as pd
import numpy as np

# nipype libraries

from nipype.interfaces import afni
import nipype.interfaces.io as nio  # Data i/o
import nipype.interfaces.utility as util  # utility
import nipype.pipeline.engine as pe  # pypeline engine
import nipype.algorithms.modelgen as model  # model specification
from nipype import Node, Workflow, MapNode

from nipype.interfaces.utility import Function

outputtype = 'nifti'
# Adjust locations
data_dir =   '/gpfs/gibbs/pi/levy_ifat/Ziv/NIH-PTSD_Rest/'
output_dir =  '/gpfs/gibbs/pi/levy_ifat/Or/ZivResults/' 
work_dir = '/home/oad4/scratch60/work'

# subject list with nonSteady - if you use this list - add the non-steady in template
subject_list = ['2512','2155','0678','0193', '2846','2326','0081','2267','2772',
'3659','1887','2468','3319']
# if you use the steady list - remove non-steady from template and conenct
subject_list_steady = ['3671', '0687', '1632', '1060', '0545',
       '1750', '1216', '1749', '2942', '1062',
       '3135', '3354', '1038', '2958', '2608',
       '2646', '0435', '1936', '1428', '1460',
       '2714', '0758', '1127', '3146', '1316',
       '2108', '1551', '2645', '2759', '2199',
       '1718', '1565', '1016', '1393', '2070',
       '2064', '2105', '1513', '0695', '3256',
       '2520', '1990', '0939', '2680', '1766',
       '1954', '2025', '0034', '2288', '2405',
       '3541', '2124', '3128', '2113', '1148',
       '1888', '3299', '2169', '1343', '1800',
       '1498', '0216', '0366', '2377', '2196',
       '3143', '1163', '1255', '2392', '1775',
       '1333', '2590', '1010', '2228', '0497',
       '2527', '3646', '3315', '0708', '3625',
       '1306', '3408', '3148', '0454', '3612',
       '2492', '3191', '3025', '1361', '2037',
       '0643', '1909', '1482', '1803', '1238',
       '2032', '1159', '3586', '2236', '0839',
       '2099', '3259', '3533', '3056', '0875',
       '2019', '2333', '2828', '1519', '2028',
       '2544', '2530', '3121', '0682', '2845',
       '1904', '2027', '3029', '0727', '0862',
       '2010', '1959', '0790', '2417', '1319',
       '2692', '2795', '2164', '3447', '1470',
       '3610', '2423', '0365', '2393', '1350',
       '2896', '0005', '2701', '2142', '1716',
       '1331', '2167', '1860', '2823', '1619',
       '0789']

templates = {
    'func': data_dir + 'derivatives/fmriprep/sub-{subject_id}/ses-1/func/sub-{subject_id}_ses-1_task-rest_space-MNI152NLin2009cAsym_desc-smoothAROMAnonaggr_bold.nii.gz',
   # 'non_steady': output_dir + '/confounds/sub-{subject_id}_nonSteady.1D',
    'confound': output_dir + '/confounds/sub-{subject_id}_WM_csf_gs.csv',
   
}


# grab functional files
infosource = pe.Node(util.IdentityInterface(fields=['subject_id']),
                  name="infosource")

infosource.iterables = [('subject_id', subject_list_steady)]

# Flexibly collect data from disk to feed into flows.

selectfiles = pe.Node(nio.SelectFiles(templates),
                      #base_directory=data_dir),
                      name="selectfiles")
                
# run via afni and save files
cleanAfni = pe.Node(afni.TProject(
    bandpass = (0.01,0.1),
    outputtype = 'NIFTI_GZ'), 
    name = 'cleanAfni'
)
#cleanAfni.inputs.out_file = 'sub-0216_ses-1_task-rest_space-MNI152NLin2009cAsym_desc-smoothAROMAnonaggr_bold.nii'

wfAfni = Workflow(name="afni_cleaning", base_dir=output_dir)

wfAfni.connect([
    (infosource, selectfiles, [('subject_id', 'subject_id')]),
    (selectfiles, cleanAfni, [('func', 'in_file'),
                           # ('non_steady', 'censor'),
                            ('confound', 'ort'),
                           
                           ])
                    
                ])

wfAfni.run('MultiProc', plugin_args={'n_procs': 5})

