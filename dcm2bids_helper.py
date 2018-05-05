# Import libraries
import os
import subprocess
import config_dcm2bids_helper as cfg

def main():
    """
    Run the things.
    """
    dir_fullpaths = cfg.logdir, cfg.bidsdir
    check_dirs_make(dir_fullpaths)
    logfile_fullpaths = cfg.outputlog, cfg.errorlog
    create_logfiles(logfile_fullpaths)
    dirs_and_messages = {cfg.dicomdir:"Incorrect dicom directory specified", os.path.join(cfg.dicomdir, cfg.test_subject):"Test participant's folder does not exist - %s " % (cfg.test_subject)}
    check_dirs(dirs_and_messages)
    if os.path.isdir(cfg.dicomdir):
        write_to_outputlog(cfg.test_subject + os.linesep)
        # Create a job to submit to the HPC with sbatch
        if cfg.run_local:
            cmd = 'dcm2bids_helper -d {dicomdir}/{test_subject} -b {bidsdir}'.format(dicomdir=cfg.dicomdir, test_subject=cfg.test_subject, niidir=cfg.bidsdir)
        else:
            cmd = 'module load singularity; sbatch --job-name helper_{test_subject} --partition=short --time 00:60:00 --mem-per-cpu=2G --cpus-per-task=1 -o {logdir}/{test_subject}_helper_output.txt -e {logdir}/{test_subject}_helper_error.txt --wrap="singularity exec -B {dicomdir} -B {parentdir} {image} dcm2bids_helper -d {dicomdir}/{test_subject} -o {bidsdir}"'.format(dicomdir=cfg.dicomdir, test_subject=cfg.test_subject, bidsdir=cfg.bidsdir, group=cfg.group, image=cfg.singularity_image, study=cfg.study, logdir=cfg.logdir)
        subprocess.call([cmd], shell=True)
    else:
        write_to_errorlog(cfg.test_subject+os.linesep)

# Define a function to create files
def touch(path:str):
    """
    Create a new file.
    
    @type path:     string
    @param path:    path to - including name of - file to be created
    """
    with open(path, 'a'):
        os.utime(path, None)

# Check and create directories
def check_dirs_make(dir_fullpaths:list):
    """
    Check if a directory exists. If not, create it.

    @type dir_fullpaths:        list
    @param dir_fullpaths:       Paths to directorys to check
    """
    for dir_fullpath in dir_fullpaths:
        if not os.path.isdir(dir_fullpath):
            os.mkdir(dir_fullpath)

# Create logs
def create_logfiles(logfile_fullpaths:list):
    """
    Check if a logfile exists. If not, make one.

    @type logfile_fullpaths:         list
    @param logfile_fullpaths:        Paths to logfiles to check
    """
    for logfile_fullpath in logfile_fullpaths:
        if not os.path.isfile(logfile_fullpath):
            touch(logfile_fullpath)

# Functions to write to log files
def write_to_outputlog(message):
    """
    Write a log message to the output log. Also print it to the terminal.

    @type message:          string
    @param message:         Message to be printed to the log
    """
    with open(cfg.outputlog, 'a') as logfile:
        logfile.write(message + os.linesep)
    print(message)

def write_to_errorlog(message):
    """
    Write a log message to the error log. Also print it to the terminal.

    @type message:          string
    @param message:         Message to be printed to the log
    """
    with open(cfg.errorlog, 'a') as logfile:
        logfile.write(message + os.linesep)
    print(message)

# Check directory dependencies
def check_dirs(dirs_and_messages: dict):
    """
    Check if a directory exists. If not, print an error message to the errorlog.
    
    type dir_fullpaths:         list
    param dir_fullpaths:        Paths to the directories to check
    type error_messages:        list
    param error_messages:       Messages to be printed to the error log 
    """
    for k, v in dirs_and_messages.items():
        if not os.path.isdir(k):
            write_to_errorlog(v)

# Call main
main()