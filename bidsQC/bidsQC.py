# Import libraries
import fnmatch
import os
import os.path
import shutil
from datetime import datetime
import config_bidsQC as cfg

# Main function
def main():
    """
    Run the things.
    """
    folders_tocheck = cfg.bidsdir, cfg.derivatives, cfg.logdir, cfg.tempdir
    check_dirs(folders_tocheck)
    logfile_fullpaths = cfg.errorlog, cfg.outputlog
    create_logfiles(logfile_fullpaths)
    subjectdirs = get_subjectdirs()
    write_to_outputlog("\nScript ran on %i subject directories\n" % (len(subjectdirs)))
    for subject in subjectdirs:
        write_to_errorlog("\n" + "-"*20 + "\n" + subject + "\n" + "-"*20)
        write_to_outputlog("\n" + "-"*20 + "\n" + subject + "\n" + "-"*20)
        timepoints = get_timepoints(subject)
        check_timepoint_count(timepoints, cfg.expected_timepoints, subject)
        for timepoint in timepoints:
            sequence_folder_names = get_sequences(subject, timepoint)
            expected_timepoint = [etp for etp in cfg.expected_timepoints if etp.name == timepoint]
            if len(expected_timepoint) == 1:
                check_sequence_folder_count(sequence_folder_names, expected_timepoint[0].sequences, subject, timepoint)
            else:
                write_to_errorlog("TIMEPOINT WARNING! %s missing or user entered duplicate or non-existant timepoint." % (timepoint))
            for sequence_folder_name in sequence_folder_names:
                expected_sequence = [es for es in expected_timepoint[0].sequences if es.name == sequence_folder_name]
                if len(expected_sequence) == 1:
                    check_sequence_files(subject, timepoint, sequence_folder_name, expected_sequence[0])
                else:
                    write_to_errorlog("SEQUENCE DIRECTORY WARNING! %s missing or user entered duplicate or non-existant sequence folder name." % (sequence_folder_name))

# Define a function to create files
def touch(path:str):
    """
    Create a new file
    
    @type path:     string
    @param path:    path to - including name of - file to be created
    """
    with open(path, 'a'):
        os.utime(path, None)

# Check and create directories
def check_dirs(dir_fullpaths:list):
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

# Check for subject directories
def get_subjectdirs() -> list:
    """
    Returns subject directory names (not full path) based on the bidsdir (bids_data directory).

    @rtype:  list
    @return: list of bidsdir directories that start with the prefix sub
    """
    bidsdir_contents = os.listdir(cfg.bidsdir)
    has_sub_prefix = [subdir for subdir in bidsdir_contents if subdir.startswith('sub-')]
    subjectdirs = [subdir for subdir in has_sub_prefix if os.path.isdir(os.path.join(cfg.bidsdir, subdir))] # get subject directories
    subjectdirs.sort()
    return subjectdirs

# Get the timepoints
def get_timepoints(subject: str) -> list:
    """
    Returns a list of ses-wave directory names in a participant's directory.

    @type subject:  string
    @param subject: subject folder name

    @rtype:  list
    @return: list of ses-wave folders in the subject directory
    """
    subject_fullpath = os.path.join(cfg.bidsdir, subject)
    subjectdir_contents = os.listdir(subject_fullpath)
    return [f for f in subjectdir_contents if not f.startswith('.')]

# Check subjects' sessions
def check_timepoint_count(timepoints: list, expected_timepoints: list, subject: str):
    """
    Compare the expected number of ses-wave directories to the actual number and print the result to the output or errorlog.

    @type timepoints:                       list
    @param timepoints:                      list of ses-wave folders in the subject directory
    @type expected_timepoints:              list
    @param expected_timepoints:             Number of timepoint folders each subject should have
    @type subject:                          string
    @param subject:                         subject folder name
    """
    number_timepoints_exist = len(timepoints)
    log_message =  "%s has %s ses-wave directories." % (subject, str(number_timepoints_exist))
    if len(expected_timepoints) != number_timepoints_exist:
        write_to_errorlog("\n TIMEPOINT WARNING! %s Expected %s \n" % (log_message, str(len(expected_timepoints))))
    else:
        write_to_outputlog("\n EXISTS: %s \n" % (log_message))

# Get sequences
def get_sequences(subject: str, timepoint: str) -> list:
    """
    Returns a list of sequence directory names (e.g. anat, fmap, etc.) in a participant's directory at a given timepoint.

    @type subject:              string
    @param subject:             Subject folder name
    @type timepoint:            string
    @param timepoint:           Timepoint folder name

    @rtype:                     list
    @return:                    list of sequence folders that exist in the subject directory
    """
    timepoint_fullpath = os.path.join(cfg.bidsdir, subject, timepoint)
    timepoint_contents = os.listdir(timepoint_fullpath)
    return [f for f in timepoint_contents if not f.startswith('.')]

# Check subjects' sessions
def check_sequence_folder_count(sequence_folder_names: list, expected_sequences: list, subject: str, timepoint: str):
    """
    Compare the expected number of ses-wave directories to the actual number and print the result to the output or errorlog.

    @type sequence_folder_names:            list
    @param sequence_folder_names:           List of sequence folders in the subject directory (e.g. anat, fmap, etc.)
    @type expected_sequences:               list
    @param expected_sequences:              Number of sequence folders each subject should have within the timepoint
    @type subject:                          string
    @param subject:                         Subject folder name
    @type timepoint:                        string
    @param timepoint:                       Timepoint folder name
    """
    number_sequences_exist = len(sequence_folder_names)
    log_message =  "%s %s has %s total sequence directories" % (subject, timepoint, str(number_sequences_exist))
    if len(expected_sequences) != number_sequences_exist:
        write_to_errorlog("\n SEQUENCE DIRECTORY WARNING! %s Expected %s.\n" % (log_message, str(len(expected_sequences))))
    else:
        write_to_outputlog("\n EXIST: %s. \n" % (log_message))

# Check files
def check_sequence_files(subject: str, timepoint: str, sequence: str, expected_sequence: object):
    """
    Compare the contents of a given sequence folder to the expected contents.

    @type subject:                          string
    @param subject:                         Subject folder name
    @type timepoint:                        string
    @param timepoint:                       Name of timepoint
    @type sequence:                         str
    @param sequence:                        Name of sequence folder (e.g. anat, fmap, etc.)
    @type expected_sequence:                object
    @param expected_sequence:               The expected sequence
    """
    extension_json = "json"
    extension_nifti = "nii.gz" if cfg.gzipped else ".nii"
    sequence_fullpath = os.path.join(cfg.bidsdir, subject, timepoint, sequence)
    if not os.path.isdir(sequence_fullpath):
        write_to_errorlog("\n FOLDER WARNING! %s folder missing for %s \n" % (sequence, subject))
    else:
        write_to_outputlog("\n EXISTS: %s folder for subject %s \n" % (sequence, subject))
    validate_sequencefilecount(expected_sequence, sequence_fullpath, extension_json, timepoint, subject)
    validate_sequencefilecount(expected_sequence, sequence_fullpath, extension_nifti, timepoint, subject)
    for key in expected_sequence.files.keys():
        fix_files(sequence_fullpath, key, expected_sequence.files[key], extension_json, subject, timepoint)
        fix_files(sequence_fullpath, key, expected_sequence.files[key], extension_nifti, subject, timepoint)

# Validate sequence files
def validate_sequencefilecount(expected_sequence: object, sequence_fullpath: str, extension: str, timepoint: str, subject: str):
    sequence_files = os.listdir(sequence_fullpath)
    found_allfiles = [file for file in sequence_files if file.endswith(extension)]
    if len(found_allfiles) > expected_sequence.get_filecount():
        write_to_errorlog("WARNING! Too many %s files in %s %s %s" % (extension, subject, timepoint, os.path.basename(sequence_fullpath)))
        
# Fix files
def fix_files(sequence_fullpath: str, file_group: str, expected_numfiles: int, extension: str, subject: str, timepoint: str):
    """
    Compare the contents of a given sequence folder to the expected contents. \
    If more than the expected number of runs of a file exist, move the appropriate \
    number of files with the lowest run numbers to the tmp__dcm2bids folder. \
    Then, change the run numbers for the remaining files.

    @type sequence_fillpath:                string
    @param sequence_fullpath:               The full path to to the sequence folder
    @type filegroup:                        string
    @param filegroup:                       Name of files (e.g. T1w, taskname) to check
    @type expected_numfiles:                integer
    @param expected_numfiles:               The expected number of runs for the filegroup
    @type: extension:                       string
    @param extension:                       File extension
    @type subject:                          string
    @param subject:                         Subject folder name
    @type timepoint:                        string
    @param timepoint:                       Name of timepoint
    """
    sequence_files = os.listdir(sequence_fullpath)
    found_files = [file for file in sequence_files if file_group in file and file.endswith(extension)]
    if len(found_files) == expected_numfiles:
        write_to_outputlog("OK: %s has correct number of %s %s files in %s." % (subject, file_group, extension, timepoint))
        return
    if len(found_files) < expected_numfiles:
        write_to_errorlog("FILE WARNING! %s MISSING %s %s files in %s." % (subject, file_group, extension, timepoint))
        return
    if len(found_files) > expected_numfiles:
        difference = len(found_files) - expected_numfiles
        # gng_acq-1 want 2 files, have 3
        # expect 2
        # difference = 1
        # IF too many files exist, diff is positive
        # IF too few files exist (won't happen)
        # IF correct number, (won't happen)
        found_files.sort()
        write_to_outputlog("\n FIXING FILES: %s \n" % (extension))
        for found_file in found_files:
            run_index = found_file.index("_run-")
            run_number = found_file[run_index + 5:run_index + 7] #03
            run_int = int(run_number) #3
            target_file = os.path.join(sequence_fullpath, found_file)
            if run_int <= difference: # if = 1
                move_files_tmp(target_file, subject, timepoint)
            elif run_int > difference: # If there are more files than expected
                if expected_numfiles == 1: # If there should only be one file
                    os.rename(target_file, target_file.replace(found_file[run_index:run_index + 7], ''))
                    write_to_outputlog("RENAMED: %s, dropped run from filename" % (target_file))
                elif expected_numfiles > 1: # If we expect more than 1 file, rename the run-## part of the filename
                    new_int = run_int - difference # 3-1 = 2
                    int_str = str(new_int)
                    new_runnum = int_str.zfill(2) #02
                    os.rename(target_file, target_file.replace(found_file[run_index + 5:run_index + 7], new_runnum))
                    write_to_outputlog("RENAMED: %s with run-%s" % (target_file, new_runnum))


def move_files_tmp(target_file:str, subject:str, timepoint:str):
    tempdir_fullpath = os.path.join(cfg.tempdir, subject + "_" + timepoint)
    if not os.path.isdir(tempdir_fullpath):
        os.mkdir(tempdir_fullpath)
    shutil.move(target_file, tempdir_fullpath)
    target_filename = os.path.basename(target_file)
    write_to_outputlog("MOVED: %s to %s" % (target_filename, tempdir_fullpath))


# Call main
main()


