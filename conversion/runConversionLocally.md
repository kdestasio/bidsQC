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
sub01_20150909,REV001,wave1  
sub01_20150909,REV001,wave2
sub02_20150909,REV001,wave1
```

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

<hr>