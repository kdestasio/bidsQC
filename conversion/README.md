# Convert Dicoms to Niftis

The scripts in this directory build off of [cbedetti's Dcm2Bids package](https://github.com/cbedetti/Dcm2Bids), which on its own will allow you to convert all of the DICOM files in a given directory to Nifti files on a local machine. See [cbedetti's tutorial](https://cbedetti.github.io/Dcm2Bids/tutorial/) to learn how to do the basic conversion and for detailed instructions on how to create the configuration file specific to _your_ study's dicoms.

The scripts in this folder allow the user to **convert dicoms for all or only a subset of participants in the dicom directory and to run the conversion on Talapas**, the University of Oregon's high performance cluster. And here is some additional information on [running the helper script on Talapas](helper_readme.md).

## Scripts

### `config_dcm2bids_helper.py`
  
Requires you to edit it. This script is where you enter the information used by the `dcm2bids_helper`, which will convert one participant's dicoms to niftis and also generate `.json` files for each sequence that contain metadata you will use to uniquely identify each type of scan. This script can be used locally or on Talapas.

## `dcm2bids_helper.py`  

You should not need to edit this script. After updating `config_dcm2bids_helper.py`, run this script by typing `python3 dcm2bids_helper.py` in the terminal of the machine on which you want to run the conversion. This will run the Dcm2Bids conversion on your test subject, creating the nifti and `.json` files needed to specify the `study_config.json` file.

### `study_config.json`<a name="config"/>

This file is an example of what a study configuration file should look like. You will need to create a custom `study_config.json` for your data. Make sure it is named `study_config.json` and is located in the `conversion` folder. It is used in the Dcm2Bids conversion and is required by the `dcm2bids_batch.py` script. For detailed instructions on how to create this file for your own study, see [cbedetti's tutorial](https://cbedetti.github.io/Dcm2Bids/tutorial/).

### `subject_list.txt`

This file is an example of what a subject list should look like. Each entry in the file takes the format `dicomFolderName,subjectID,sessionLabel`. Each line is one dicom directory and the entries on that line are comma separated with no spaces.

### `config_dcm2bids_batch.py`
  
Requires you to edit it. This script will convert all of the dicoms in the source directory that you define for any participant directories that are listed in the `subject_list.txt file`. Niftis will be renamed and put into BIDS structure using the dcm2Bids package. This script can be used locally or on Talapas.

### `dcm2bids_batch.py`
  
You should not need to edit this script. After updating `config_dcm2bids_batch.py`, `study_config.json`, and `subject_list.txt` files, run this script by typing `python3 dcm2bids_batch.py` in the terminal of the machine on which you want to run the conversion. This will run the Dcm2Bids conversion.

### `fmap_intendedfor.py`

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

## Running dcm2bids on a Linux Cluster

### Dependencies

- SLURM
- Python3
- Dcm2Bids singularity container **You need to download it.**
  - For instructions on copying singularity containers, see [Containers: Docker & Singularity](https://uosanlab.atlassian.net/wiki/spaces/SW/pages/45285423) (and, as always, read the [documentation](http://singularity.lbl.gov/docs-build-container))
  - The container is available on [Singularity Hub](https://singularity-hub.org/collections/544)
  - Note that when you copy the container, you either need to name it `Dcm2Bids-master.simg` or change the image name in the `config_dcm2bids_batch.py` script.

### Steps to convert DICOMS to BIDS

1. Create the `subject_list.txt` where each row has the input: `directoryName,subjectID,waveNumber`
    - An easy way to do this is to `cd` into your DICOM directory and use the command `ls >> subject_list.txt` , which will create a text file of that name and populate it with all the directories/files in your working directory. You can then move that subject_list.txt file to the directory from which you will be running your code and add the subject ID and time-point columns.
    - The subject_list should be formatted such that each row consists of: the subject directory names (that contains the dicoms), desired subject ID, and data collection wave number. Each field is comma separated, all without spaces, e.g.:

    `sub01_20150909,REV001,wave1`

    `sub01_20150909,REV001,wave2`

    `sub02_20150909,REV001,wave1`

2. Edit the `study_config.json` file such that it works for your study.  
    - See instructions [above](#config)
3. Change the variables and/or paths in `config_``dcm2bids_batch.py` script for your study
    - Select whether the jobs are to be run serially on a local machine or in parallel on a HPC
4. Log into the HPC.  

  `ssh -X username@Talapas-ln1.uoregon.edu`

5. `cd` to the directory that has your code in it. 
6. Load the python3 module.  

  `module load python3`

7. Run the batch script.  

  `python3 dcm2bids_batch.py`

8. Check the niftis, output logs, and error logs.

## Running dcm2bids Locally

### Steps to convert DICOMS to BIDS

1. Create the `subject_list.txt` where each row has the input: `directoryName,subjectID,waveNumber`
    - An easy way to do this is to `cd` into your DICOM directory and use the command `ls >> subject_list.txt` , which will create a text file of that name and populate it with all the directories/files in your working directory. You can then move that subject_list.txt file to the directory from which you will be running your code and add the subject ID and time-point columns.
    - The subject_list should be formatted such that each row consists of: the subject directory names (that contains the dicoms), desired subject ID, and data collection wave number. Each field is comma separated, all without spaces, e.g.:

    `sub01_20150909,REV001,wave1`

    `sub01_20150909,REV001,wave2`

    `sub02_20150909,REV001,wave1`

2. Edit the `study_config.json` file such that it works for your study.  
    - See instructions [above](#config)  
3. Change the variables and/or paths in `config_``dcm2bids_batch.py` script for your study
    - Select whether the jobs are to be run serially on a local machine or in parallel on a HPC. (Select local)
4. `cd` to the directory that has your code in it. 
5. Run the batch script.  

  `python3 dcm2bids_batch.py`

8. Check the niftis, output logs, and error logs.