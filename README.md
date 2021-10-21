# BidsQC

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1326895.svg)](https://doi.org/10.5281/zenodo.1326895)

The scripts in this repo are a combination of wrappers and quality checking scripts that take neuroimaging files from DICOMS to Niftis named and structured as per [BIDS](http://bids.neuroimaging.io/). They add functionality to the Dcm2Bids scripts that allow the user to:

1. Convert dicoms for all or only a subset of participants in the dicom directory (`/conversion`)
2. Run the conversion on Talapas, the University of Oregon's high performance cluster (`/conversion`)
3. Check that the expected files exist for each participant and notify the user if there is a discrepency (`/qualityCheck`)
4. Rename task runs, retaining those that occured latest in time (`/qualityCheck`)

**Instructions on this page are to run batches of subjects on a high performance cluster running SLURM using a Singularity container of the dcm2Bids package -- or -- to run the subjects serially on a local machine.**

## Using BidsQC

1. Using either [git clone](https://help.github.com/en/articles/cloning-a-repository) or the download button, copy this repo to the machine you will use for dicom conversion.
2. Follow the instructions on the [Dcm2Bids tutorial](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/) to convert the DICOM files to Nifti files. The tutorial is comprehensive and should have all of the information you need. Look at it now.
   1. If you want to **(a)** convert only a subset of the participant data, or **(b)** run the conversion on Talapas (the University of Oregon high performance cluster), there are scripts available in the [conversion](/conversion) folder of this repo to help you do so. But first, go look at that tutorial.
3. Check that the results of the conversion and renaming are as expected by using the files in the [qualityCheck](/qualityCheck) folder of this repo to help you do so.

## Table of Contents

- [Dependencies](#dependencies)
- [Repository Contents](#repo-contents)
  - [Conversion Folder](#conversion_folder)
  - [Bids Quality Check Folder](#qc_folder)
- [Creating the dcm2bids Configuration File](helper_readme.md)
- [Running dcm2bids](/conversion/README.md)
  - [On a Linux Cluster](/running_dcm2bids_cluster.md)
  - [Locally](/conversion/README.md)
- [Running qualityCheck](/qualityCheck/README.md)
- [Final BIDS Steps](#final-steps)

## Dependencies<a name="dependencies"/>

- Python 3 with the `future` module (pip install of cbedetti's `dcm2bids` will install the future module)
- `dcm2niix` conversion tool. **You need to install it.**
  - Get via the [rordenlab github](https://github.com/rordenlab/dcm2niix)
- `dcm2Bids`. **You need to install it.**
  - Available from [UNFmontreal](https://github.com/UNFmontreal/Dcm2Bids)

## Repo Contents<a name="repo-contents"/>

### Conversion Scripts<a name="conversion_folder"/>

These scripts are located in the [conversion folder](/conversion). They allow the user to convert dicoms for only a subset of participants in the dicom directory and to run the conversion on Talapas, the University of Oregon's high performance cluster. The scripts in this repo build off of [Dcm2Bids](https://github.com/UNFmontreal/Dcm2Bids), which on its own will allow you to convert the DICOM files to Nifti files. See the [Dcm2Bids tutorial](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/) to learn how to do the basic conversion and for detailed instructions on how to create the configuration file specific to _your_ study's dicoms.

For instructions on how to use the conversion scripts, see the conversion folder [README](/conversion/README.md).

### qualityCheck Scripts<a name="qc_folder"/>

Once Niftis are in BIDS, these scripts can be used to check whether each sequence has the correct number of runs. Files in the target directories are checked against values in the configuration file where the user specifies how many runs of each sequence are expected at each time point. Optional: append the `run-##` key-value string to file names based on sequence order (option specifed in config file).  

For step-by-step instructions and a description of the naming rules, see the [qualityCheck README.](/qualityCheck/README.md)

## Final BIDS Steps<a name="final-steps"/>
### Manually Create Metadata Files

As per: [http://bids.neuroimaging.io/bids\_spec1.0.0-rc2.pdf](http://bids.neuroimaging.io/bids_spec1.0.0-rc2.pdf)

Place these files in the top level bids directory.

- dataset_description.json
- phasediff.json
- A JSON for each functional task with TaskName and RepetitionTime
- README (optional, but strongly recommended)
- CHANGES (optional, but strongly recommended)

## Check the BIDS Conversion

BIDS validator: [http://incf.github.io/bids-validator](http://incf.github.io/bids-validator/)
