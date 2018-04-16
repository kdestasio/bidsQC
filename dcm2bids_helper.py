# This script will use the dcm2bids_helper to create json files
# for use in creating the study specific configuration file
#
# See the dcm2Bids repo for instructions to create the config file:
# https://github.com/cbedetti/Dcm2Bids
#
# More detailed instructions on san wiki:
# https://uosanlab.atlassian.net/wiki/spaces/SW/pages/44269646/Convert+DICOM+to+BIDS

##################################
# Setup
##################################

# Import libraries
import os
import subprocess

# Set study info (may need to change for your study)
group = "sanlab"
study = "REV"
gitrepo = "REV_scripts"
test_subject = "REV001_20150406" # Name of a directory that contains DICOMS for one participant

dicomdir = "/projects/lcni/dcm/" + group + "/Archive/" + study
image = "/projects/" + group + "/shared/containers/Dcm2Bids-master.simg"

# Set directories
archivedir = "/projects/" + group + "/shared/" + study + "/archive"
niidir = archivedir + "/clean_nii"
codedir = "/projects/" + group + "/shared/" + study + "/" + gitrepo + "/org/dcm2bids/"
logdir = codedir + "/logs_helper"

outputlog = logdir + "/outputlog_helper.txt"
errorlog = logdir + "/errorlog_helper.txt"


##################################
# Directory Check & Log Creation
##################################

# Define a function to create files
def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


# Check/create log files
if not os.path.isdir(logdir):
    os.mkdir(logdir)
if not os.path.isfile(outputlog):
    touch(outputlog)
if not os.path.isfile(errorlog):
    touch(errorlog)

# Check directory dependencies
if not os.path.isdir(dicomdir):
    with open(errorlog, 'a') as logfile:
        logfile.write("Incorrect dicom directory specified")
if not os.path.isdir(dicomdir + "/" + test_subject):
    with open(errorlog, 'a') as logfile:
        logfile.write("Test participant's folder does not exist - " + test_subject)
if not os.path.isdir(archivedir):
    os.mkdir(archivedir)
if not os.path.isdir(niidir):
    os.mkdir(niidir)


##################################
# Run dcm2bids Helper
##################################

if os.path.isdir(dicomdir):
    with open(outputlog, 'a') as logfile:
        logfile.write(test_subject+os.linesep)
    # Create a job to submit to the HPC with sbatch
    cmd = 'module load singularity; sbatch --job-name helper_{test_subject} --partition=short --time 00:60:00 --mem-per-cpu=2G --cpus-per-task=1 -o {logdir}/{test_subject}_helper_output.txt -e {logdir}/{test_subject}_helper_error.txt --wrap="singularity exec -B {dicomdir} -B /projects/{group}/shared/{study} {image} dcm2bids_helper -d {dicomdir}/{test_subject} -o /projects/{group}/shared/{study}"'.format(dicomdir=dicomdir, test_subject=test_subject, niidir=niidir, group=group, image=image, study=study, logdir=logdir)
    # Submit the job
    subprocess.call([cmd], shell=True)
else:
    with open(errorlog, 'a') as logfile:
        logfile.write(test_subject+os.linesep)
