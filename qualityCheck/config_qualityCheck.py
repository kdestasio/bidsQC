import os
from datetime import datetime
from sequence import Sequence
from timepoint import TimePoint

######################## CONFIGURABLE PART BELOW ########################

# Set directories (Check these for your study)
# These variables are used in the main script and need to be defined here. 
# They need to exist prior to running the qualityCheck.py
path_bidsdata = os.path.join(os.sep, 'projects', "sanlab", 'shared', "studyName", 'bids_data')  # Where your subjects' nifti directories are
logdir = os.path.join(os.getcwd(), 'logs_qualityCheck')  # Log files will go in the folder from which this script is run

# Create a dictionary (the thing below) for each timepoint in your study.
# The first entry after Sequence is the directory name
# e.g. Sequence('func', ...) means the directory is named func
# The key:value pairs within the curly {} braces are taskName:numberOfRuns
# e.g. a task named stopsignal that the subject completed twice would be entered as {'stopsignal':2}
sequence1 = Sequence('func', {'stopsignal': 2, 'react':1})
sequence3 = Sequence('anat', {'T1w':1})
sequence4 = Sequence('fmap', {'dir-ap':1, 'dir-pa':1})  # Example of fieldmap with multiple phase encoded directions
sequence5 = Sequence("fmap", {"magnitude1":1, "magnitude2":1, "phasediff":1 }) # Example of fieldmap with phase-difference map and multiple magnitude images
timepoint1 = TimePoint('ses-wave1', [sequence1, sequence3, sequence4])   # Create an entry for each timepoint in your study
timepoint2 = TimePoint('ses-wave2', [sequence1, sequence5])  # Add as many timepoints as needed and fill it with the correct sequences
expected_timepoints = [timepoint1, timepoint2]


# Files g-zipped or not? 
# NOTE: All files must be either zipped or unzipped. 
# A mixture won't work properly.
gzipped = True

# If you have different versions of the same task - e.g. stopsignal was run twice with different images
# And those runs were named differently - e.g. stopsignalA and stopsignalB
# You need them to be recognized as multiple runs of the same task. 
# List them below to have the 'run-#' field appended to indicate the order in which they were run.
order_sequences = True
tasks_to_order = 'stopsignal'    # comma seperated if multiple


######################## DO NOT CHANGE ########################
tempdir = os.path.join(path_bidsdata, 'tmp_dcm2bids')  # holding folder for undesired files
outputlog = os.path.join(logdir, 'outputlog_qualityCheck' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.txt')
errorlog = os.path.join(logdir, 'errorlog_qualityCheck' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.txt')
derivatives = os.path.join(path_bidsdata, 'derivatives')  # Where processed data will go
