# BidsQC

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1326895.svg)](https://doi.org/10.5281/zenodo.1326895)

## Overview

The scripts in this repo are a combination of wrappers and quality checking scripts that take neuroimaging files from DICOMS to Niftis named and structured as per [BIDS](http://bids.neuroimaging.io/). They add functionality to the Dcm2Bids scripts that allow the user to:

1. Convert dicoms for all or only a subset of participants in the dicom directory (`/conversion`)
2. Run the conversion on Talapas, the University of Oregon's high performance cluster (`/conversion`)
3. Check that the expected files exist for each participant and notify the user if there is a discrepency (`/qualityCheck`)
4. Rename task runs, retaining those that occured latest in time (`/qualityCheck`)

**The purpose of these scripts is to allow the user to run batches of specific subjects on a high performance cluster -- or -- to run the subjects serially on a local machine. They also provide some functionality to check that the resultant data contains the expected runs.**

## bidsQC Table of Contents

- [Using bidsQC: Overview](#usage)
  - [Dependencies](#dependencies)
- [Repository Contents](#repo-contents)
  - [Conversion Folder Overview](#conversion_folder)
    - [Running dcm2bids](/conversion/README.md)
    - [On a Linux Cluster](/conversion/runConversionOnCluster.md)
    - [Locally](/conversion/runConversionLocally.md)
  - [Bids Quality Check Folder](#qc_folder)
    - [Running qualityCheck](/qualityCheck/README.md)
- [Final BIDS Steps](#final-steps)
- [Detailed tutorial: University of Oregon specific](uoTutorial.md)

## Using BidsQC <a name="usage">

1. Using either [git clone](https://help.github.com/en/articles/cloning-a-repository) or the download button, copy this repo to the machine you will use for dicom conversion. This can be your local machine or a high performance cluster such as the UO's Talapas.
2. Convert your DICOMS to Nifti files that adhere to BIDS. To do so, you can:
   1. Convert all DICOMS in a specified directory. Simply follow the instructions on the [Dcm2Bids tutorial](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/). The tutorial is comprehensive and should have all of the information you need.
   2. Or you can **convert only a subset of the participant data,** or **run the conversion in a cluster environment** such as Talapas. To do so, see the instructions and scripts in the [conversion](/conversion) folder of this repo.
3. Check that the results of the conversion and renaming are as expected. You can use the files in the [qualityCheck](/qualityCheck) folder of this repo to help you do so.
4. Verify your data are in BIDS using the [BIDS Validator](http://incf.github.io/bids-validator/)

## Dependencies<a name="dependencies">

- Python 3 with the `future` module (pip install of cbedetti's `dcm2bids` will install the future module)
- `dcm2niix` conversion tool. **If it is not already available on your machine or cluster, install it.**
  - Get via the [rordenlab github](https://github.com/rordenlab/dcm2niix)
- `dcm2Bids` **If it is not already available on your machine or cluster, install it.**
  - bidsQC is confirmed compatible with `dcm2bids v2.1.5`.
  - Available from [UNFmontreal](https://github.com/UNFmontreal/Dcm2Bids) for your local machine.
  - [Here are instructions](https://unfmontreal.github.io/Dcm2Bids/docs/1-usage/#containers) for getting a singularity image for use on a cluster. You will need to `module load singularity` prior to running the singularity command.

**Note:** to check if Python 3, dcm2niix, or other packages are available on a Linux cluster, type `module avail [packageName]` at the command line, e.g. `module avail Python3`

## Repo Contents<a name="repo-contents">

### Conversion Folder<a name="conversion_folder">

The scripts located in the [conversion folder](/conversion) allow the user to convert dicoms for only a subset of participants in the dicom directory and to run the conversion on Talapas, the University of Oregon's high performance cluster. They build off of [Dcm2Bids](https://github.com/UNFmontreal/Dcm2Bids), which on its own will allow you to convert the DICOM files to Nifti files en masse. See the [Dcm2Bids tutorial](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/) to learn how to do the basic conversion and for detailed instructions on how to create the configuration file specific to _your_ study's dicoms.

For instructions on how to use the conversion scripts, see the conversion folder [README](/conversion/README.md).

### qualityCheck Scripts<a name="qc_folder">

Once Niftis are in BIDS, these scripts can be used to check whether each sequence has the correct number of runs. Files in the target directories are checked against values in the configuration file where the user specifies how many runs of each sequence are expected at each time point. Optional: append the `run-##` key-value string to file names based on sequence order (option specifed in config file).  

For step-by-step instructions and a description of the naming rules, see the [qualityCheck README.](/qualityCheck/README.md)

## Final BIDS Steps<a name="final-steps">
### Manually Create Metadata Files

As per: [http://bids.neuroimaging.io/bids\_spec1.0.0-rc2.pdf](http://bids.neuroimaging.io/bids_spec1.0.0-rc2.pdf)

Place these files in the top level bids directory.

- dataset_description.json
- phasediff.json
- A JSON for each functional task with TaskName and RepetitionTime
- README (optional, but strongly recommended)
- CHANGES (optional, but strongly recommended)

## Check the BIDS Conversion <a name="bidsValidator">

BIDS validator: [http://incf.github.io/bids-validator](http://incf.github.io/bids-validator/)
