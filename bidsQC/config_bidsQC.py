import os
from datetime import datetime
from bidsQC_classes import Sequence
from bidsQC_classes import TimePoint

######################## CONFIGURAGBLE PART BELOW ########################

# Set study info (change these for your study)
# These variables are used only in this file for path names.
# They can be removed if desired.
group = 'sanlab'
study = 'CHIVES'

# Set directories (Check these for your study)
# These variables are used in the main script and need to be defined here. 
# They need to exist prior to running the script.
logdir = os.path.join(os.getcwd(), 'logs_bidsQC')
bidsdir = os.path.join(os.sep, 'projects', group, 'shared', study, 'bids_data')
tempdir = os.path.join(bidsdir, 'tmp_dcm2bids')
outputlog = os.path.join(logdir, 'outputlog_bidsQC' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.txt')
errorlog = os.path.join(logdir, 'errorlog_bidsQC' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.txt')
derivatives = os.path.join(bidsdir, 'derivatives')


# Create a dictionary (the thing below) for each timepoint in your study where the pairs are 'sequence_directory_name' : 'expected_number_runs'
# Each unique version of a sequence gets its own entry, e.g. 'gng_acq-1' and 'gng_acq-2'
sequence1 = Sequence('func', {'money': 1, 'words_acq-1':1, 'words_acq-2':1, 'picture_acq-1':1, 'picture_acq-2':1})
sequence3 = Sequence('anat', {'T1w':1})
sequence4 = Sequence('fmap', {'dir-ap':1, 'dir-pa':1})
timepoint1 = TimePoint('ses-wave1', [sequence1, sequence3, sequence4])
expected_timepoints = [timepoint1]


# Files g-zipped or not? 
# NOTE: All files must be either zipped or unzipped. 
# A mixture won't work properly.
gzipped = True


# Do we want runs based on sequence order? Yes = True
# This is for tasks that use counterbalancing (of e.g. stimulus blocks) anf for which we want to identify the content
# with the 'acq-' label and order administered with the 'task-' label
order_sequences = True
tasks_to_order = 'words', 'picture'
