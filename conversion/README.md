
# Convert Dicoms to Niftis

The scripts in this folder allow the user to:  

1. Convert dicoms for all or only a subset of participants in the dicom directory.  
2. Run the conversion on Talapas, the University of Oregon's high performance cluster.  

The instructions below presuppose you have the bidsQC repository on your machine (local or cluster) with access to your dicoms. For instructions on getting the repo onto your machine, see the [step-by-step guide.](../uoTutorial.md)

## Table of Contents

- [How to run on a cluster](#cluster)
  1. [Get dicom metadata](#clust1)
  2. [Edit the study_config.json](#clust2)
  3. [Create subject_list.txt](#clust3)
  4. [Run dcm2bids_batch.py](#clust4)
- [How to run locally](#local)
  1. [Use the Dcm2Bids helper](#local1)
  2. [Edit the `study_config.json` ](#local2)
  3. [Create `subject_list.txt`](#local3)
  4. [Run `dcm2bids_batch.py`](local4)
- [More detail on the scripts in this folder](#scripts)
  - [Scripts you need to edit](#edit)
  - [Scripts you don't need to edit](#noEdit)
  
The scripts in this directory build off of the [Dcm2Bids package](https://github.com/UNFmontreal/Dcm2Bids), which on its own will allow you to convert all of the DICOM files in a given directory to Nifti files on a local machine. See the [Dcm2Bids tutorial](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/) to learn how to do the basic conversion and for detailed instructions on how to create the [configuration file](https://unfmontreal.github.io/Dcm2Bids/docs/3-configuration/) specific to _your_ study's dicoms.

Here is some additional information on [running the helper script on Talapas](#clust1) to get the information you need for your configuration file.

<hr>

## Running the scripts on a Linux Cluster <a name="cluster">

### Dependencies

- SLURM (already available on the UO cluster)
- Python3
- Dcm2Bids singularity container*. You need to download it if you don't have access to a copy on Talapas.
  - Instructions for getting the singularity container are available here: https://unfmontreal.github.io/Dcm2Bids/docs/1-usage/#containers
  - If the above link doesn't get you what you need, try:
    - instructions on copying singularity containers, see [Containers: Docker & Singularity](https://uoregonctn.atlassian.net/wiki/spaces/FSS/pages/138248203/Containers+Docker+Singularity)
    - Follow the [instructions](https://uoregonctn.atlassian.net/wiki/spaces/FSS/pages/138248203/Containers+Docker+Singularity#Containers:Docker&Singularity-trueFromgithub) to build the singularity container on Talapas 

To check if Python 3, dcm2niix, or other packages are available on a Linux cluster, type module avail [packageName] at the command line, e.g. module avail Python3

***Important:** when you copy the container, you either need to name it `Dcm2Bids-master.simg` or change the image name in the `config_dcm2bids_batch.py` script.

### Steps to convert DICOMS to BIDS

#### 1. Get dicom metadata <a name="clust1">

If you need the metadata to populate the `study_config.json` file, use the dcm2bids helper.

1. Log into the HPC   
`ssh -X username@Talapas-ln1.uoregon.edu`
2. `cd` into the `bidsQC/conversion` directory.
3. Change the variables and/or paths in the `config_dcm2bids_helper.py` script for your study. 
4. Load python3 by typing in the terminal:  
`module load python3`
5. Run the helper script by typing:   
`python3 dcm2bids_helper.py`  
This will run Dcm2Bids on your test subject, creating the nifti and `.json` files needed to construct the `study_config.json` file.
6. `cd` to the folder created by the helper (should be in the top level of your study directory), e.g. 

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

7. View the `.json` files and use that info to edit the `study_config.json` file. 

#### 2. Edit the `study_config.json` <a name="clust2">

3. Change the variables and/or paths in `config_dcm2bids_batch.py` script for your study and set `run_local = False`

#### 3. Create `subject_list.txt` <a name="clust3">

Each row has the input: `dicomFolderName,subjectID,sessionLabel`.

An easy way to do this is to `cd` into your DICOM directory and use the command `ls >> subject_list.txt` , which will create a text file of that name and populate it with all the directories/files in your working directory. You can then move that `subject_list.txt` file to the directory from which you will be running your code and add the subject ID and time-point columns.

The subject_list should be formatted such that each row consists of: the subject directory names (that contains the dicoms), desired subject ID, and data collection wave number. Each field is comma separated without spaces, e.g.:

```
sub01_20150909,REV001,wave1  
sub01_20150909,REV001,wave2
sub02_20150909,REV001,wave1
```

#### 4. Run `dcm2bids_batch.py` <a name="clust4">

- Log into the HPC  
  `ssh -X username@Talapas-ln1.uoregon.edu`
- Navigate into the `bidsQC/conversion` directory.  
  `cd path/to/bidsQC/conversion`
- Load python3  
  `module load python3`
- Run the batch script  
  `python3 dcm2bids_batch.py`
- Check the niftis, output logs, and error logs.

<hr>

## Running dcm2bids Locally<a name="local">

### Dependencies

- Python3
- dcm2niix
- dcm2bids
- pip

### Steps to convert DICOMS to BIDS

The following steps are to convert specific participants and/or sessions. If you want to convert everything, follow the [unfmontreal tutorial](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/).

#### 1. Use the Dcm2Bids helper <a name="local1">

Get your disom metadate using the [dcm2bids_helper](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/#dicom-to-nifti-conversion)

#### 2. Edit the `study_config.json` <a name="local2">

Change the variables and/or paths in `config_dcm2bids_batch.py` script for your study and set `run_local = True`

#### 3. Create `subject_list.txt` <a name="local3">

Each row has the input: `dicomFolderName,subjectID,sessionLabel`.

An easy way to do this is to `cd` into your DICOM directory and use the command `ls >> subject_list.txt` , which will create a text file of that name and populate it with all the directories/files in your working directory. You can then move that `subject_list.txt` file to the directory from which you will be running your code and add the subject ID and time-point columns.

The subject_list should be formatted such that each row consists of: the subject directory names (that contains the dicoms), desired subject ID, and data collection wave number. Each field is comma separated without spaces, e.g.:

```
sub01_20150909,REV001,wave1  
sub01_20150909,REV001,wave2
sub02_20150909,REV001,wave1
```

#### 4. run `dcm2bids_batch.py` <a name="local4">

- Navigate into the `bidsQC/conversion` directory.  
  `cd path/to/bidsQC/conversion`
- Run the batch script  
  `python3 dcm2bids_batch.py`
- Check the niftis, output logs, and error logs.  

<hr>

## Descriptions of the Scripts<a name="scripts">

### Scripts you need to edit <a name="edit">

#### `config_dcm2bids_helper.py`
  
This script is where you enter the information used by the `dcm2bids_helper`, which will convert one participant's dicoms to niftis and also generate `.json` files for each sequence that contain metadata you will use to uniquely identify each type of scan. This script can be used locally or on Talapas.

#### `study_config.json`<a name="study_config">

This is an example of what a study configuration file should look like. You will need to create a custom `study_config.json` for your data. Make sure it is named `study_config.json` and is located in the `conversion` folder. It is used in the Dcm2Bids conversion and is required by the `dcm2bids_batch.py` script. For detailed instructions on how to create this file for your own study, see the [Dcm2Bids tutorial](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/#building-the-configuration-file).

#### `subject_list.txt`

This file is an example of what a subject list should look like. Each entry in the file takes the format `dicomFolderName,subjectID,sessionLabel`.

#### `config_dcm2bids_batch.py`
  
Requires you to edit it. This script will convert all of the dicoms in the source directory that you define for any participant directories that are listed in the `subject_list.txt file`. Niftis will be renamed and put into BIDS structure using the dcm2Bids package. This script can be used locally or on Talapas.

#### `fmap_intendedfor.py`

If the `qualityCheck.py` script is to be used to alter run numbers, that must be done BEFORE running `fmap_intededfor.py`. 

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

### Scripts you don't edit <a name="noEdit">

#### `dcm2bids_helper.py`

After updating `config_dcm2bids_helper.py`, run this script by typing `python3 dcm2bids_helper.py` in the terminal of the machine on which you want to run the conversion. This will run the Dcm2Bids conversion on your test subject, creating the nifti and `.json` files needed to specify the `study_config.json` file.

#### `dcm2bids_batch.py`
  
After updating `config_dcm2bids_batch.py`, `study_config.json`, and `subject_list.txt` files, run this script by typing `python3 dcm2bids_batch.py` in the terminal of the machine on which you want to run the conversion. This will run the Dcm2Bids conversion.
