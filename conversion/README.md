
# Convert Dicoms to Niftis

The scripts in this folder allow the user to **convert dicoms for all or only a subset of participants in the dicom directory and to run the conversion on Talapas**, the University of Oregon's high performance cluster. 

## Table of Contents

- [Scripts](#scripts)
- [Running on a cluster](#cluster)
- [Running locally](#local)
  
The scripts in this directory build off of the [Dcm2Bids package](https://github.com/UNFmontreal/Dcm2Bids), which on its own will allow you to convert all of the DICOM files in a given directory to Nifti files on a local machine. See the [Dcm2Bids tutorial](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/) to learn how to do the basic conversion and for detailed instructions on how to create the [configuration file](https://unfmontreal.github.io/Dcm2Bids/docs/3-configuration/) specific to _your_ study's dicoms.

Here is some additional information on [running the helper script on Talapas](#usingHelper) to get the information you need for your configuration file.

## Scripts<a name="scripts"/>

### `config_dcm2bids_helper.py`
  
Requires you to edit it. This script is where you enter the information used by the `dcm2bids_helper`, which will convert one participant's dicoms to niftis and also generate `.json` files for each sequence that contain metadata you will use to uniquely identify each type of scan. This script can be used locally or on Talapas.

## `dcm2bids_helper.py`<a name="helper"/>

You should not need to edit this script. After updating `config_dcm2bids_helper.py`, run this script by typing `python3 dcm2bids_helper.py` in the terminal of the machine on which you want to run the conversion. This will run the Dcm2Bids conversion on your test subject, creating the nifti and `.json` files needed to specify the `study_config.json` file.

### `study_config.json`<a name="study_config"/>

This file is an example of what a study configuration file should look like. You will need to create a custom `study_config.json` for your data. Make sure it is named `study_config.json` and is located in the `conversion` folder. It is used in the Dcm2Bids conversion and is required by the `dcm2bids_batch.py` script. For detailed instructions on how to create this file for your own study, see the [Dcm2Bids tutorial](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/#building-the-configuration-file).

### `subject_list.txt`

This file is an example of what a subject list should look like. Each entry in the file takes the format `dicomFolderName,subjectID,sessionLabel`.

An easy way to do this is to `cd` into your DICOM directory and use the command `ls >> subject_list.txt` , which will create a text file of that name and populate it with all the directories/files in your working directory. You can then move that `subject_list.txt` file to the directory from which you will be running your code and add the subject ID and time-point columns.

The subject_list should be formatted such that each row consists of: the subject directory names (that contains the dicoms), desired subject ID, and data collection wave number. Each field is comma separated without spaces, e.g.:

`sub01_20150909,REV001,wave1`
`sub01_20150909,REV001,wave2`
`sub02_20150909,REV001,wave1`

### `config_dcm2bids_batch.py`
  
Requires you to edit it. This script will convert all of the dicoms in the source directory that you define for any participant directories that are listed in the `subject_list.txt file`. Niftis will be renamed and put into BIDS structure using the dcm2Bids package. This script can be used locally or on Talapas.

### `dcm2bids_batch.py`
  
You should not need to edit this script. After updating `config_dcm2bids_batch.py`, `study_config.json`, and `subject_list.txt` files, run this script by typing `python3 dcm2bids_batch.py` in the terminal of the machine on which you want to run the conversion. This will run the Dcm2Bids conversion.

### `fmap_intendedfor.py`

If the `bidsQC` script is to be used to alter run numbers, that must be done BEFORE running `fmap_intededfor.py`. 

This script requires you to edit it. In order to meet the BIDS specifications, the following fields are inserted into the `.json` file for each fieldmap:

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

## Running the scripts on a Linux Cluster<a name="cluster"/>

### Dependencies

- SLURM
- Python3
- Dcm2Bids singularity container **You need to download it.**
  - For instructions on copying singularity containers, see [Containers: Docker & Singularity](https://uosanlab.atlassian.net/wiki/spaces/SW/pages/45285423) (and, as always, read the [documentation](http://singularity.lbl.gov/docs-build-container))
  - The container is available on [Singularity Hub](https://singularity-hub.org/collections/544)
  - Note that when you copy the container, you either need to name it `Dcm2Bids-master.simg` or change the image name in the `config_dcm2bids_batch.py` script.

### Using the Dcm2Bids helper <a name="usingHelper"/>

If you need the metadata to populate the config file, use the dcm2bids helper.

1. `cd` into the `conversion` directory.
2. Load python3 by typing `module load python3` into the terminal.
3. Use the [helper script](helper).
4. cd to the folder created by the helper (should be in the top level of your study directory), e.g. 

```{bash}
cd /projects/sanlab/shared/REV/tmp_dcm2bids/helper
ls 

    001_REV001_20150406_AAHScout_20150406145550.nii.gz
    002_REV001_20150406_AAHScout_20150406145550a.json
    .
    .
    .
    017_REV001_20150406_React2_mb3_g2_2mm_te27_20150406145550.json
    017_REV001_20150406_React2_mb3_g2_2mm_te27_20150406145550.nii.gz
```

5. View the `.json` files and use that info to [edit the config file](#study_config) so it works for your study.

### Steps to convert DICOMS to BIDS

1. [Create the `subject_list.txt` where each row has the input: `dicomFolderName,subjectID,sessionLabel`](#subject_list).
2. [Edit the `study_config.json` file such that it works for your study.](#config)
3. Change the variables and/or paths in `config_dcm2bids_batch.py` script for your study and set `run_local = False`
4. Log into the HPC.  

  `ssh -X username@Talapas-ln1.uoregon.edu`

5. `cd` into the `conversion` directory.
6. Load the python3 module.  

  `module load python3`

7. Run the batch script.  

  `python3 dcm2bids_batch.py`

8. Check the niftis, output logs, and error logs.

## Running dcm2bids Locally<a name="local"/>

### Using the Dcm2Bids helper

[Use the Dcm2Bids built in command line interface.](https://unfmontreal.github.io/Dcm2Bids/docs/1-usage/#command-line-interface-cli)

### Steps to convert DICOMS to BIDS

1. [Create the `subject_list.txt` where each row has the input: `dicomFolderName,subjectID,sessionLabel`](#subject_list).
2. [Edit the `study_config.json` file such that it works for your study.](#config)
3. Change the variables and/or paths in `config_dcm2bids_batch.py` script for your study and set `run_local = True`
4. `cd` into the `conversion` directory.
5. Load the python3 module.  

  `module load python3`

7. Run the batch script.  

  `python3 dcm2bids_batch.py`

8. Check the niftis, output logs, and error logs.
