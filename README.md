[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1326895.svg)](https://doi.org/10.5281/zenodo.1326895)


# Overview

The scripts in this repo are a combination of wrappers and quality checking scripts that take neuroimaging files from DICOMS to Niftis named and structured as per [BIDS](http://bids.neuroimaging.io/).

**_Instructions on this page are to run batches of subjects on a high performance cluster running SLURM using a Singularity container of the dcm2Bids package - or - to run the subjects serially on a local machine._**


# Table of Contents

- [Dependencies](#dependencies)
- [Repo Contents](#repo-contents)
- [Creating the dcm2bids Configuration File](helper_readme.md)
- [Running dcm2bids]
  - [On a Linux Cluster](/running_dcm2bids_cluster.md)
  - [Locally](runnung_dcm2bids_local.md)
- [Running bidsQC](/bidsQC/README.md)
- [Final BIDS Steps](#final-steps)
- [Links]


# Dependencies<a name="dependencies"/>
- Python 3 with the `future` module (pip install of cbedetti's `dcm2bids` will install the future module)
- `dcm2niix`conversion tool. **You need to install it.**
  - Get via the [rordenlab github](https://github.com/rordenlab/dcm2niix)
- `dcm2Bids`. **You need to install it.**
  - Get via [cbedetti's github](https://github.com/cbedetti/Dcm2Bids)


# Repo Contents<a name="repo-contents"/>
## dcm2bids Scripts
Wrapper around the rordenlab's  `dcm2niix` and cbedetti's `dcm2Bids`. These scripts convert the DICOM files in subjects' directories, convert them to Niftis, and put them in BIDS.  

  - `config_dcm2bids_batch.py`  
  - `config_dcm2bids_helper.py` 
  - `dcm2bids_batch.py`
  - `dcm2bids_helper.py`  
  - `fmap_intendedfor.py` 
  - `study_config.json` 
  - `subject_list.txt`


## bidsQC Scripts

Once Niftis are in BIDS, these scripts can be used to check whether each sequence has the correct number of runs. Files in the target directories are checked against values in the configuration file where the user specifies how many runs of each sequence are expected at each time point. Optional: append the `run-##` key-value string to file names based on sequence order (option specifed in config file).  

For step-by-step instructions and a description of the naming rules, see the [bidsQC README.](/bidsQC/README.md)


# Final BIDS Steps<a name="final-steps"/>
## Manually Create Metadata Files

As per: [http://bids.neuroimaging.io/bids\_spec1.0.0-rc2.pdf](http://bids.neuroimaging.io/bids_spec1.0.0-rc2.pdf)

Place these files in the top level bids directory.

- dataset_description.json
- phasediff.json
- A JSON for each functional task with TaskName and RepetitionTime
- README (optional, but strongly recommended)
- CHANGES (optional, but strongly recommended)

## Check the BIDS Conversion

BIDS validator: [http://incf.github.io/bids-validator](http://incf.github.io/bids-validator/)