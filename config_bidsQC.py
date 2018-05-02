import os
from datetime import datetime
from bidsQC_classes import Sequence
from bidsQC_classes import TimePoint

######################## CONFIGURAGBLE PART BELOW ########################

# Set study info (change these for your study)
group = "sanlab"
study = "REV"

# Set directories (Check these for your study)
logdir = os.path.join(os.getcwd(), "logs_bidsQC")
bidsdir = os.path.join(os.sep, "projects", group, "shared", study, "bids_data")
tempdir = os.path.join(bidsdir, "tmp_dcm2bids")
outputlog = os.path.join(logdir, "outputlog_bidsQC" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt")
errorlog = os.path.join(logdir, "errorlog_bidsQC" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt")
derivatives = os.path.join(bidsdir, "derivatives")

# Create a dictionary (the thing below) for each timepoint in your study.
# Within "Sequence", the first field identifies the type of sequence (name of folder containing the files).
# The subsequent key:value pairs are "sequence_name" : "expected_number_runs", 
# e.g. if we expect 2 runs of the stop signal task in a given folder, we would use "sst": 2
files1 = Sequence("func", {"taskname": 1, "othertaskname":1, "anothertask":2})
files2 = Sequence("func", {"taskname": 1, "othertaskname":1, "anothertask":2})
files3 = Sequence("anat", {"T1w":1})
files4 = Sequence("fmap", {"magnitude1":2, "magnitude2":2, "phasediff":2 })
timepoint1 = TimePoint("ses-wave1", [files1, files3, files4])
timepoint2 = TimePoint("ses-wave2", [files2, files3, files4])
expected_timepoints = [timepoint1, timepoint2]

# Files g-zipped or not? NOTE: All files must be either zipped or unzipped. A mixture won't work properly.
gzipped = True

