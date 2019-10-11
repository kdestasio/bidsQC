# Convert Dicoms to Niftis

The scripts in this directory build off of [cbedetti's Dcm2Bids package](https://github.com/cbedetti/Dcm2Bids), which on its own will allow you to convert all of the DICOM files in a given directory to Nifti files on a local machine. See [cbedetti's tutorial](https://cbedetti.github.io/Dcm2Bids/tutorial/) to learn how to do the basic conversion and for detailed instructions on how to create the configuration file specific to _your_ study's dicoms.

The scripts in this folder allow the user to **convert dicoms for all or only a subset of participants in the dicom directory and to run the conversion on Talapas**, the University of Oregon's high performance cluster. And here is some additional information on [running the helper script on Talapas](helper_readme.md).

## `config_dcm2bids_helper.py`
  
Requires you to edit it. This script is where you enter the information used by the `dcm2bids_helper`, which will convert one participant's dicoms to niftis and also generate `.json` files for each sequence that contain metadata you will use to uniquely identify each type of scan. This script can be used locally or on Talapas.

## `dcm2bids_helper.py`  

You should not need to edit this script. After updating `config_dcm2bids_helper.py`, run this script by typing `python3 dcm2bids_helper.py` in the terminal of the machine on which you want to run the conversion. This will run the Dcm2Bids conversion on your test subject, creating the nifti and `.json` files needed to specify the `study_config.json` file.

## `study_config.json`

This file is an example of what a study configuration file should look like. You will need to create a custom `study_config.json` for your data. Make sure it is named `study_config.json` and is located in the `conversion` folder. It is used in the Dcm2Bids conversion and is required by the `dcm2bids_batch.py` script. For detailed instructions on how to create this file for your own study, see [cbedetti's tutorial](https://cbedetti.github.io/Dcm2Bids/tutorial/).

## `subject_list.txt`

This file is an example of what a subject list should look like. Each entry in the file takes the format `dicomFolderName,subjectID,sessionLabel`. Each line is one dicom directory and the entries on that line are comma separated with no spaces.

## `config_dcm2bids_batch.py`
  
Requires you to edit it. This script will convert all of the dicoms in the source directory that you define for any participant directories that are listed in the `subject_list.txt file`. Niftis will be renamed and put into BIDS structure using the dcm2Bids package. This script can be used locally or on Talapas.

## `dcm2bids_batch.py`
  
You should not need to edit this script. After updating `config_dcm2bids_batch.py`, `study_config.json`, and `subject_list.txt` files, run this script by typing `python3 dcm2bids_batch.py` in the terminal of the machine on which you want to run the conversion. This will run the Dcm2Bids conversion.

## `fmap_intendedfor.py`

Requires you to edit it. In order to meet the BIDS specifications, this script will insert the following fields into the `.json` file for each fieldmap:

- `"IntendedFor"`
  - Followed by a list of all the functional runs in the `func` folder associated with the matching subject and session.
- `"EchoTime1"`
  - Followed by a list of the echo time you enter in the script. You need to look-up what the echo time is for your specific fieldmap. You can set `include_echo_time = False` if you do not want to include the echo time in the `.json` file.
- `"EchoTime2"`
  - Followed by a list of the echo time you enter in the script. You need to look-up what the echo time is for your specific fieldmap. You can set `include_echo_time = False` if you do not want to include the echo time in the `.json` file.

Here is an example of what the output would look like:

```{json}
    "IntendedFor": [
        "func/sub-REV001_ses-wave1_task-react_acq-2_run-02_bold.nii.gz",
        "func/sub-REV001_ses-wave1_task-sst_acq-1_run-01_bold.nii.gz",
        "func/sub-REV001_ses-wave1_task-bart_acq-1_bold.nii.gz",
        "func/sub-REV001_ses-wave1_task-gng_acq-1_run-02_bold.nii.gz",
        "func/sub-REV001_ses-wave1_task-react_acq-1_run-01_bold.nii.gz",
        "func/sub-REV001_ses-wave1_task-sst_acq-2_run-02_bold.nii.gz",
        "func/sub-REV001_ses-wave1_task-gng_acq-2_run-01_bold.nii.gz"
    ],
    "EchoTime1": "0.00437",
    "EchoTime2": "0.00683"
```
