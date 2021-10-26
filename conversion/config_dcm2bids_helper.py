# This is the configuration file for the dcm2bids_helper script,
# which will use the dcm2bids_helper to create json files
# for use in creating the study specific configuration file

import os

# The following variables are used in the main script and need to be defined here. Change them for your data. 
# They need to exist prior to running the script.

# Directories
pathToStudyFolder = os.path.join(os.sep, "projects", "sanlab", "shared", "studyName") # folder that contains bidsdir and pathToConversionFolder
pathToDicomFolder = os.path.join(os.sep, "projects", "shared", "DICOMS")
bidsdir = os.path.join(pathToStudyFolder, "bids_data") # where the niftis will be put
pathToConversionFolder = os.path.join(pathToStudyFolder, "REV_study", "org", "dcm2bids") # Contains subject_list.txt, config file, and dcm2bids_batch.py
logdir = os.path.join(pathToConversionFolder, "logs_helper")

# Log files
outputlog = os.path.join(logdir, "outputlog_helper.txt")
errorlog = os.path.join(logdir, "errorlog_helper.txt")

# Test subject
test_subject = "S001" # Name of a directory that contains DICOMS for one participant

# Run on local machine (run_local = True) or high performance cluster with slurm (run_local = False)
run_local = True

# If false, set the singularity image. Else, set to "NA"
singularity_image =  os.path.join(os.sep, "projects", "sanlab", "shared", "containers", "Dcm2Bids-master.simg")