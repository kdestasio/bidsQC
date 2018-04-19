##################################
#  Setup
##################################

# Import libraries
import fnmatch
import os
import os.path
import shutil
from datetime import datetime

# Set study info (change these for your study)
group = "sanlab"
study = "REV"

# Set directories (Check these for your study)

# logdir = os.getcwd() + "/logs_bidsQC"
# bidsdir = "/projects/" + group + "/shared/" + study + "/bids_data_copy"
# tempdir = bidsdir + "/tmp_dcm2bids"
# outputlog = logdir + "/outputlog_bidsQC" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
# errorlog = logdir + "/errorlog_bidsQC" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
# derivatives = bidsdir + "/derivatives"

# Set directories for local testing
bidsdir = "/Users/kristadestasio/Desktop/bids_data"
logdir = bidsdir + "/logs_bidsQC"
tempdir = bidsdir + "/tmp_dcm2bids"
outputlog = logdir + "/outputlog_bidsQC_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
errorlog = logdir + "/errorlog_bidsQC_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
derivatives = bidsdir + "/derivatives"


############### In progress chunk / configurable part ###############

class TimePoint:
    def __init__(self, name: str, sequences: list):
        self.name = name
        self.sequences = sequences


class Sequence:
    def __init__(self, name: str, files: dict):
        self.name = name
        self.files = files

    def get_filecount(self):
        filecount = 0
        for key in self.files.keys():
            filecount = filecount + self.files[key]
        return filecount


# Create a dictionary (the thing below) for each timepoint in your study where the pairs are "sequence_directory_name" : "expected_number_runs"
sequence1 = Sequence("func", {"bart": 1, "gng1":1, "gng2":1, "react1":1, "react2":1, "sst1":1, "sst2":1})
sequence2 = Sequence("func", {"bart": 1, "gng3":1, "gng4":1, "react3":1, "react4":1, "sst3":1, "sst4":1})
sequence3 = Sequence("anat", {"T1w":1})
sequence4 = Sequence("fmap", {"magnitude1":2, "magnitude2":2, "phasediff":2 })
timepoint1 = TimePoint("ses-wave1", [sequence1, sequence3, sequence4])
timepoint2 = TimePoint("ses-wave2", [sequence2, sequence3, sequence4])
expected_timepoints = [timepoint1, timepoint2]


# Define a function to create files
def touch(path):
    """Create a new file"""
    with open(path, 'a'):
        os.utime(path, None)


# Check and create directories
if not os.path.isdir(bidsdir):
    os.mkdir(bidsdir)
if not os.path.isdir(derivatives):
    os.mkdir(derivatives)
if not os.path.isdir(logdir):
    os.mkdir(logdir)
if not os.path.isdir(tempdir):
    os.mkdir(tempdir)

# Check/create log files
if not os.path.isfile(outputlog):
    touch(outputlog)
if not os.path.isfile(errorlog):
    touch(errorlog)


# Functions to write to log files
def write_to_outputlog(message):
    with open(outputlog, 'a') as logfile:
        logfile.write(message + os.linesep)
    print(message)


def write_to_errorlog(message):
    with open(errorlog, 'a') as logfile:
        logfile.write(message + os.linesep)
    print(message)


# Main function
def main():
    """
    Run the things.
    """
    subjectdirs = get_subjectdirs()
    write_to_outputlog("\nScript ran on %i subject directories\n" % (len(subjectdirs)))
    for subject in subjectdirs:
        write_to_errorlog("\n" + "-"*20 + "\n" + subject + "\n" + "-"*20)
        write_to_outputlog("\n" + "-"*20 + "\n" + subject + "\n" + "-"*20)
        timepoints = get_timepoints(subject)
        check_timepoint_count(timepoints, expected_timepoints, subject)
        for timepoint in timepoints:
            sequence_folder_names = get_sequences(subject, timepoint)
            expected_timepoint = [etp for etp in expected_timepoints if etp.name == timepoint]
            if len(expected_timepoint) == 1:
                check_sequence_folder_count(sequence_folder_names, expected_timepoint[0].sequences, subject, timepoint)
            else:
                write_to_errorlog("TIMEPOINT ERROR! %s missing or user entered duplicate or non-existant timepoint." % (timepoint))
            for sequence_folder_name in sequence_folder_names:
                expected_sequence = [es for es in expected_timepoint[0].sequences if es.name == sequence_folder_name]
                if len(expected_sequence) == 1:
                    check_sequence_files(subject, timepoint, sequence_folder_name, expected_sequence[0])
                else:
                    write_to_errorlog("SEQUENCE DIRECTORY ERROR! %s missing or user entered duplicate or non-existant sequence folder name." % (sequence_folder_name))


# Check for subject directories
def get_subjectdirs() -> list:
    """
    Returns subject directory names (not full path) based on the bidsdir (bids_data directory).

    @rtype:  list
    @return: list of bidsdir directories that start with the prefix sub
    """
    bidsdir_contents = os.listdir(bidsdir)
    has_sub_prefix = [subdir for subdir in bidsdir_contents if subdir.startswith('sub-')]
    subjectdirs = [subdir for subdir in has_sub_prefix if os.path.isdir(os.path.join(bidsdir, subdir))] # get subject directories
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
    subject_fullpath = os.path.join(bidsdir, subject)
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
        write_to_errorlog("\n TIMEPOINT ERROR! %s Expected %s \n" % (log_message, str(len(expected_timepoints))))
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
    timepoint_fullpath = os.path.join(bidsdir, subject, timepoint)
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
        write_to_errorlog("\n SEQUENCE DIRECTORY ERROR! %s Expected %s.\n" % (log_message, str(len(expected_sequences))))
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
    extension_nifti = "nii.gz"
    sequence_fullpath = os.path.join(bidsdir, subject, timepoint, sequence)
    if not os.path.isdir(sequence_fullpath):
        write_to_errorlog("\n FOLDER ERROR! %s folder missing for %s \n" % (sequence, subject))
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
        write_to_errorlog("FILE ERROR! %s MISSING %s %s files in %s." % (subject, file_group, extension, timepoint))
        return
    if len(found_files) > expected_numfiles:
        difference = len(found_files) - expected_numfiles
        found_files.sort()
        write_to_outputlog("\n FIXING FILES: %s \n" % (extension))
        for found_file in found_files:
            run_index = found_file.index("_run-")
            run_number = found_file[run_index+ 5:run_index + 7]
            run_int = int(run_number)
            target_file = os.path.join(sequence_fullpath, found_file)
            if run_int <= difference:
                tempdir_fullpath = os.path.join(tempdir, subject + "_" + timepoint)
                if not os.path.isdir(tempdir_fullpath):
                    os.mkdir(tempdir_fullpath)
                shutil.move(target_file, tempdir_fullpath)
                target_filename = os.path.basename(target_file)
                write_to_outputlog("MOVED: %s to %s" % (target_filename, tempdir_fullpath))
            elif run_int > difference:
                if expected_numfiles == 1:
                    new_runnum = ''
                    rename_file(found_file, run_number, new_runnum, sequence_fullpath, target_file)
                elif expected_numfiles > 1:
                    new_int = run_int - difference
                    int_str = str(new_int)
                    new_runnum = "_run-" + int_str.zfill(2)
                    rename_file(found_file, run_number, new_runnum, sequence_fullpath, target_file)

# Rename run number segment of sequence file
def rename_file(found_file, run_number, run_replacement, sequence_fullpath, target_file):
    new_filename = found_file.replace("_run-" + run_number, run_replacement)
    new_filename_path = os.path.join(sequence_fullpath, new_filename)
    os.rename(target_file, new_filename_path)
    target_filename = os.path.basename(target_file)
    write_to_outputlog("RENAMED: %s to %s" % (target_filename, new_filename))



# Call main
main()

## TO DO:
# Make a config file
### In config file
### - config option: zipped nifti files or not zipped (.nii or .nii.gz)


