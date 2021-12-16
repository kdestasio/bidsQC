import os
from datetime import datetime

######################## CONFIGURABLE PART BELOW ########################

# Set your Talapas user group
group = "sanlab"
partition = "ctn" # ignored if running locally
dcm2bidsImageName = "dcm2bids_latest_2021-11-18.sif" # ignored if running locally
config_file = "study_config.json"

# Set directories
# These variables are used in the main script and mustbe defined here.
# They need to exist prior to running the script
pathToStudyFolder = os.path.join(os.sep, "projects", "sanlab", "shared", "studyName") # folder that contains pathToBidsFolder and pathToConversionFolder
pathToDicomFolder = os.path.join(os.sep, "projects", "lcni", "dcm", "sanlab", "Berkman", "REV")
pathToConversionFolder = os.path.join(pathToStudyFolder, "bidsQC", "conversion")  # Contains subject_list.txt, config file, and dcm2bids_batch.py
pathToConfigFile = os.path.join(pathToConversionFolder, config_file)  # Don't cahnge this one
singularity_image = os.path.join(os.sep, "projects", "sanlab", "shared", "containers", dcm2bidsImageName) # Set equal to "NA" if you are running the script locally

# These variables are also used in the main script and need to be defined here.
# If the directories don't exist, they will be created by the script
pathToBidsFolder = os.path.join(os.sep, "projects", group, "shared", "studyName", "bids_data") # Where the niftis will be put
logdir = os.path.join(pathToBidsFolder, "logs_dcm2bids")
outputlog = os.path.join(logdir, "outputlog_dcmn2bids" + datetime.now().strftime("%Y%m%d-%H%M") + ".txt")
errorlog = os.path.join(logdir, "errorlog_dcm2bids" + datetime.now().strftime("%Y%m%d-%H%M") + ".txt")

# Source the subject list (needs to be in your current working directory)
subjectlist = "subject_list.txt"

# Run on local machine (run_local = True) or high performance cluster with slurm (run_local = False)
run_local = False