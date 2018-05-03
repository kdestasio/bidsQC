# This script will convert all of the dicoms in the sourcedir
# for participant directories that are listed in the subject_list.txt file.
# Niftis will be renamed and put into BIDS structure using the dcm2Bids package
#
# See the dcm2Bids repo for instructions to create the config file:
# https://github.com/cbedetti/Dcm2Bids
#
# More detailed instructions on san wiki:
# https://uosanlab.atlassian.net/wiki/spaces/SW/pages/44269646/Convert+DICOM+to+BIDS
#
# In your current directory, you will need:
#       - dcm2bids_batch.py
#       - subject_list.txt
#       - study_config.json


# Configuration file for dcm2bids_batch.py
import os
from datetime import datetime


# Set study info 
# These variables are used only in the config file path names 
# and can be commented out if not needed.
group = "sanlab"
study = "REV"
parent_dir = "dcm2bids"


# Set directories
# These variables are used in the main script and need to be defined here.
# They need to exist prior to running the script (with the exception of `image` 
# which can be set equal to "NA" if you are running the script locally)
dicomdir = os.path.join(os.sep, "projects", "lcni", "dcm", group, "Archive", study)
codedir = os.path.join(os.sep, "projects", group, "shared", study, "REV_scripts", "org", parent_dir)  # Contains subject_list.txt, config file, and dcm2bids_batch.py
configfile = os.path.join(codedir, "study_config.json")  # path to and name of config file
image = os.path.join(os.sep, "projects", group, "shared", "containers", "Dcm2Bids-master.simg")

# These variables are also used in the main script and need to be defined here.
# If they don't exist, they will be created by the script
niidir = os.path.join(os.sep, "projects", group, "shared", study, "bids_data") # Where the niftis will be put
logdir = os.path.join(codedir, "logs_dcm2bids")
outputlog = os.path.join(logdir, "outputlog_dcmn2bids" + datetime.now().strftime("%Y%m%d-%H%M") + ".txt")
errorlog = os.path.join(logdir, "errorlog_dcm2bids" + datetime.now().strftime("%Y%m%d-%H%M") + ".txt")


# Source the subject list (needs to be in your current working directory)
subjectlist = "subject_list.txt"


# Run on local machine (run_local = True) or high performance cluster with slurm (run_local = False)
run_local = True