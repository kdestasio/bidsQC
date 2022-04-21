# Running the `/conversion` scripts on a local machine

## Dependencies

- Python3
- dcm2niix
- dcm2bids
- pip

## Steps to convert DICOMS to BIDS

The following steps are to convert specific participants and/or sessions. If you want to convert everything, follow the [unfmontreal tutorial](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/).

1. [Use the Dcm2Bids helper](#local1)
2. [Edit the `study_config.json` ](#local2)
3. [Create `subject_list.txt`](#local3)
4. [Edit `config_dcm2bids_batch.py`](#local4)
5. [Run `dcm2bids_batch.py`](#local5)
6. [Check your data](#local6)

### 1. Use the Dcm2Bids helper <a name="local1">

Get your dicom metadate using the [dcm2bids_helper](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/#dicom-to-nifti-conversion)

### 2. Edit the `study_config.json` <a name="local2">

Instructions and two examples are available on the unfMontreal Dcm2Bids tutorial page, [here](https://unfmontreal.github.io/Dcm2Bids/docs/3-configuration/) and [here](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/#building-the-configuration-file).

### 3. Create `subject_list.txt` <a name="local3">

Each row has the input: `dicomFolderName,subjectID,sessionLabel`.

An easy way to do this is to `cd` into your DICOM directory and use the command `ls >> subject_list.txt` , which will create a text file of that name and populate it with all the directories/files in your working directory. You can then move that `subject_list.txt` file to the directory from which you will be running your code and add the subject ID and time-point columns.

The subject_list should be formatted such that each row consists of: the subject directory names (that contains the dicoms), desired subject ID, and data collection wave number. Each field is comma separated without spaces, e.g.:

```
sub01_20150909,001,wave1  
sub01_20150909,001,wave2
sub02_20150909,002,wave1
```

This would give you BIDS data labled:
```
sub-001_ses-wave1
sub-001_ses-wave2
sub-002_ses-wave1
```

For single session data, simply omit the 3rd column in the subject_list and set `multiple_sessions = False` in the `config_dcm2bids_batch.py` script.  

### 4. Edit `config_dcm2bids_batch.py` <a name="local4">

Change the variables and/or paths in `config_dcm2bids_batch.py` script for your study and set `run_local = True`

### 5. Run `dcm2bids_batch.py` <a name="local4">

- Navigate into the `bidsQC/conversion` directory.  
  `cd path/to/bidsQC/conversion`
- Run the batch script  
  `python3 dcm2bids_batch.py`
- Check the niftis, output logs, and error logs.  

### 6. Check that your data are in BIDS <a name="local6">

- Check the [specification.](https://bids.neuroimaging.io/)
- Use the [BIDS validator](http://incf.github.io/bids-validator)

If your data do not meet BIDS standards, see whether the scripts in the [bidsQC/qualityCheck folder](../qualityCheck) may be of use.

### 7. `fmap_intendedfor.py`

If you are using fieldmaps, the `.json` file associated with each one must specify to which functional runs it is to be applied.  

If the `qualityCheck.py` script is to be used to alter run numbers, that must be done **BEFORE** running `fmap_intendedfor.py`.  

#### Running the script

#####  1. Edit the following
  
`path_bidsdata`: This should be the path to the folder containing your BIDS data.  
`include_echo_time`: Set to `True` or `False` based on whether you want the echo times in the .json files.  
`echo_time1`: You need to look-up what the echo time is for your specific fieldmap. Enter the value here.  
`echo_time2`: You need to look-up what the echo time is for your specific fieldmap. Enter the value here.  

##### 2. Run the script

Via the command line, navigate to the directory that houses the file `fmap_intendedfor.py`.  
Run the command `python3 fmap_intendedfor.py`.  
  
#### Details

In order to meet the BIDS specifications, the following fields are inserted into the .json file for each fieldmap:  

`"IntendedFor"`  
Followed by a list of all the functional runs in the func folder associated with the matching subject and session.  

`"EchoTime1"`  
Followed by a list of the echo time you enter in the script. You need to look-up what the echo time is for your specific fieldmap. You can set `include_echo_time = False` if you do not want to include the echo time in the .json file.  

`"EchoTime2"`  
Followed by a list of the echo time you enter in the script. You need to look-up what the echo time is for your specific fieldmap. You can set `include_echo_time = False` if you do not want to include the echo time in the .json file.  

Here is an example of what the output would look like:

```
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
