# Make a configuration file
The configuration file is used to identify scans of different types and to assign labels in the file names.

## Using the dcm2bids helper
If you need the metadata to populate the config file, use the dcm2bids helper, which is built into the cbedetti's dcm2bids.

The helper can be run locally, or in a cluster environment. I suggest locally as it's easier.

### Locally
To run the helper locally, use cbdetti's built in command line tool:

`dcm2bids_helper -d DICOM_DIR [-o OUTPUT_DIR]`

### Cluster

Some specific instructions are provided below for the University of Oregon Talapas cluster. Users elsewhere will need to log in and make Python3 available as per your site's protocol.  

1. If you are planning to run the script on data stored on a high performance cluster (HPC), change the variables and/or paths in the `config_dcm2bids_helper.py` script for your study.

2. Log into the HPC

`ssh -X username@Talapas-ln1.uoregon.edu`

4. `cd` to the directory that has your code in it

5. Load the python3 module 

`module load python3`

6. Run the `dcm2bids_helper.py` script

`python3 dcm2bids_helper.py`

7. `cd` to the folder created by the helper (should be in the top level of your study directory), e.g. 

```
cd /projects/sanlab/shared/REV/tmp_dcm2bids/helper

ls


>>> 001_REV001_20150406_AAHScout_20150406145550.nii.gz

>>> 02_REV001_20150406_AAHScout_20150406145550a.json

>>> ... 

>>> ...

>>> ...

>>> 017_REV001_20150406_React2_mb3_g2_2mm_te27_20150406145550.json

>>> 017_REV001_20150406_React2_mb3_g2_2mm_te27_20150406145550.nii.gz
```

8. View the JSON files and use that info to edit the config file so it works for your study. More detailed instructions on using the JSON files to populate the config file are available in the readme of the [cbedetti dcm2Bids](https://github.com/cbedetti/Dcm2Bids) repo.

