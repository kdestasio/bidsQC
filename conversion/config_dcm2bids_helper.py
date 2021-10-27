# This is the configuration file for the dcm2bids_helper script,
# which will use the dcm2bids_helper to create json files
# for use in creating the study specific configuration file

import os

# The following variables are used in the main script and need to be defined here. Change them for your data. 
# They need to exist prior to running the script.
group = "sanlab" # This is the name of the group on Talapas to which your account belongs


# Directories
# You don't need to use slashes in the path names, just put the parts of the path in quotes as shown below.
pathToStudyFolder = os.path.join(os.sep, "projects", "sanlab", "shared", "studyName") # folder that contains pathToBidsFolder and pathToConversionFolder
pathToDicomFolder = os.path.join(os.sep, "projects", "lcni", "dcm", "sanlab", "Berkman", "REV")
pathToBidsFolder = os.path.join(pathToStudyFolder, "bids_data") # path to the folder where the niftis will be put
pathToConversionFolder = os.path.join(pathToStudyFolder, "bidsQC", "conversion") # Contains subject_list.txt, config file, and dcm2bids_batch.py
logdir = os.path.join(pathToConversionFolder, "logs_helper") # Path to the folder where logs will be created

# Log files
outputlog = os.path.join(logdir, "outputlog_helper.txt")
errorlog = os.path.join(logdir, "errorlog_helper.txt")

# Test subject
test_subject = "REV027_20150518_102229" # Name of a directory that contains DICOMS for one participant. Must be subfolder of pathToDicomsFolder. E.g. pathToDicomsFolder/S001

# Run on local machine (run_local = True) or high performance cluster with slurm (run_local = False)
run_local = False

# If run_local is set to false, enter the path for the singularity image. Else, set to "NA"
singularity_image =  os.path.join(os.sep, "projects", "sanlab", "shared", "containers", "Dcm2Bids-master.simg")