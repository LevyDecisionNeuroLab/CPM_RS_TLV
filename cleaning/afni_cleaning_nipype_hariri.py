
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
data_dir =   '/gpfs/gibbs/pi/levy_ifat/Nachshon/rest_clean/'
output_dir =  '/gpfs/gibbs/pi/levy_ifat/Or/ZivResults/' 
work_dir = '/home/oad4/scratch60/work'

# subject list with nonSteady - if you use this list - add the non-steady in template
subject_list = ['sub-1482', 'sub-3319', 'sub-0790', 'sub-1632', 'sub-2846',
       'sub-2027', 'sub-1957', 'sub-1361', 'sub-2530', 'sub-2124',
       'sub-1343', 'sub-3146', 'sub-0366', 'sub-3408', 'sub-1936',
       'sub-2544', 'sub-1887', 'sub-1163', 'sub-2142', 'sub-2333',
       'sub-2105', 'sub-1749', 'sub-2267']
# if you use the steady list - remove non-steady from template and conenct
subject_list_steady = ['sub-0034', 'sub-2377', 'sub-1016', 'sub-3191', 'sub-1716',
       'sub-0875', 'sub-2288', 'sub-3121', 'sub-1888', 'sub-1775',
       'sub-3025', 'sub-2010', 'sub-1060', 'sub-3625', 'sub-3056',
       'sub-0678', 'sub-2772', 'sub-1428', 'sub-0708', 'sub-0643',
       'sub-0939', 'sub-3299', 'sub-0545', 'sub-2393', 'sub-0081',
       'sub-0497', 'sub-2520', 'sub-1010', 'sub-1519', 'sub-2590',
       'sub-1470', 'sub-2512', 'sub-2920', 'sub-2037', 'sub-2759',
       'sub-1319', 'sub-2823', 'sub-2492', 'sub-1460', 'sub-2527',
       'sub-2701', 'sub-1306', 'sub-0839', 'sub-2692', 'sub-1959',
       'sub-0862', 'sub-1498', 'sub-2099', 'sub-0005', 'sub-3135',
       'sub-1904', 'sub-3610', 'sub-2228', 'sub-0216', 'sub-0758',
       'sub-1803', 'sub-2958', 'sub-2070', 'sub-2326', 'sub-3256',
       'sub-1216', 'sub-2155', 'sub-0727', 'sub-2108', 'sub-1513',
       'sub-2942', 'sub-1551', 'sub-2795', 'sub-2896', 'sub-0435',
       'sub-2032', 'sub-1255', 'sub-3659', 'sub-1333', 'sub-1159',
       'sub-2236', 'sub-2164', 'sub-2645', 'sub-1350', 'sub-1750',
       'sub-3029', 'sub-1990', 'sub-2714', 'sub-3143', 'sub-2680',
       'sub-3612', 'sub-0193', 'sub-1800', 'sub-1148', 'sub-1038',
       'sub-1766', 'sub-3354', 'sub-2392', 'sub-2646', 'sub-0892',
       'sub-1718', 'sub-2169', 'sub-3541', 'sub-3315', 'sub-3533',
       'sub-3128', 'sub-1127', 'sub-1062', 'sub-2405', 'sub-1316',
       'sub-1331', 'sub-2423', 'sub-0682', 'sub-3671', 'sub-2196',
       'sub-1954', 'sub-1238', 'sub-2167', 'sub-2828', 'sub-2028',
       'sub-2113', 'sub-3259', 'sub-0695', 'sub-2608', 'sub-1909',
       'sub-2468', 'sub-2064', 'sub-1860', 'sub-3447', 'sub-2019',
       'sub-0789', 'sub-3148', 'sub-3586', 'sub-2417', 'sub-1619',
       'sub-0687']

templates = {
    'func': data_dir + 'derivatives/fmriprep/{subject_id}/ses-1/func/{subject_id}_ses-1_task-hariri_space-MNI152NLin2009cAsym_desc-smoothAROMAnonaggr_bold.nii.gz',
   #  'non_steady': output_dir + '/confounds/{subject_id}_nonSteady_hariri.1D',
    'confound': output_dir + '/confounds/{subject_id}_WM_csf_gs_hariri.csv',
   
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

wfAfni = Workflow(name="afni_cleaning_hariri", base_dir=output_dir)

wfAfni.connect([
    (infosource, selectfiles, [('subject_id', 'subject_id')]),
    (selectfiles, cleanAfni, [('func', 'in_file'),
                           # ('non_steady', 'censor'),
                            ('confound', 'ort'),
                           
                           ])
                    
                ])

wfAfni.run('MultiProc', plugin_args={'n_procs': 6})

