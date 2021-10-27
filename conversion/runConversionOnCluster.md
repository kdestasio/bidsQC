# Running the `/conversion` scripts on a Linux Cluster

## A note on editing scripts

I find it easiest to edit scripts using a code editor with syntax highlighting (e.g. VS code, Sublime, pycharm) on my local machine. You can use the editor on your local machine, save the script, use git to push your changes to your repository, and then pull those changes into your repository on Talapas.

## Dependencies

- SLURM (already available on the UO cluster)
- Python3
- Dcm2Bids singularity container*. You need to download it if you don't have access to a copy on Talapas.
  - Instructions for getting the singularity container are available here: https://unfmontreal.github.io/Dcm2Bids/docs/1-usage/#containers
  - If the above link doesn't get you what you need, try:
    - instructions on copying singularity containers, see [Containers: Docker & Singularity](https://uoregonctn.atlassian.net/wiki/spaces/FSS/pages/138248203/Containers+Docker+Singularity)
    - Follow the [instructions](https://uoregonctn.atlassian.net/wiki/spaces/FSS/pages/138248203/Containers+Docker+Singularity#Containers:Docker&Singularity-trueFromgithub) to build the singularity container on Talapas 

To check if Python 3, dcm2niix, or other packages are available on a Linux cluster, type module avail [packageName] at the command line, e.g. module avail Python3

***Important:** when you copy the container, you either need to name it `Dcm2Bids-master.simg` or change the image name in the `config_dcm2bids_batch.py` script.

## Steps to convert DICOMS to BIDS
  
  1. [Get dicom metadata](#clust1)
  2. [Edit the `study_config.json`](#clust2)
  3. [Create `subject_list.txt`](#clust3)
  4. [Edit `config_dcm2bids_batch.py`](#clust4)
  5. [Run `dcm2bids_batch.py`](#clust5)
  6. [Check your data](#clust6)

### 1. Get dicom metadata <a name="clust1">

If you need the metadata to populate the `study_config.json` file, use the dcm2bids helper.

1. Log into the HPC   
`ssh -X username@Talapas-ln1.uoregon.edu`
2. `cd` into the `bidsQC/conversion` directory.
3. Change the variables and/or paths in the `config_dcm2bids_helper.py` script for your study.  
4. Load python3 by typing in the terminal:  
`module load python3`
5. Run the helper script by typing:   
`python3 dcm2bids_helper.py`  
    - This will run Dcm2Bids on your test subject, creating the nifti and `.json` files needed to construct the `study_config.json` file.
    - It may take some time for the job to complete. You can check the status using `squeue` with either the `-j` flag to specify the jobn number or the `-u` flag to specufy your username.  
    e.g. `squeue -j 16534789`
6. `cd` to the `conversion` folder where there should now be a new folder called `logs_helper`.

    ```{bash}
    $ cd /path/to/studyName/bidsQC/conversion/logs_helper
    $ ls 

    errorlog_helper.txt  outputlog_helper.txt  subjectID_helper_error.txt  subjectID_helper_output.txt
    ```

    - In the `logs_helper` folder, you will find:
      - `errorlog_helper.txt`: lists any subjects for which there was an error during the job.
      - `outputlog_helper.txt`: lists the subjects for which the job was successfully run.
      -`subjectID_helper_output.txt`: gives you the path to where the Nifti and .json files were put.
      - `subjectID_helper_error.txt`: gives you the errors for that subject.
7. Navigate to the folder indicated in the file `subjectID_helper_output.txt`. View the`.json` files and use that info to edit the fields of the `study_config.json` file. 

### 2. Edit the `study_config.json` <a name="clust2">

Instructions and two examples are available on the unfMontreal Dcm2Bids tutorial page, [here](https://unfmontreal.github.io/Dcm2Bids/docs/3-configuration/) and [here](https://unfmontreal.github.io/Dcm2Bids/docs/2-tutorial/#building-the-configuration-file).

### 3. Create `subject_list.txt` <a name="clust3">

Each row has the input: `dicomFolderName,subjectID,sessionLabel`.

An easy way to do this is to `cd` into your DICOM directory and use the command `ls >> subject_list.txt` , which will create a text file of that name and populate it with all the directories/files in your working directory. You can then move that `subject_list.txt` file to the directory from which you will be running your code and add the subject ID and time-point columns.

The subject_list should be formatted such that each row consists of: the subject directory names (that contains the dicoms), desired subject ID, and data collection wave number. Each field is comma separated without spaces, e.g.:

```
sub01_20150909,REV001,wave1  
sub01_20150909,REV001,wave2
sub02_20150909,REV001,wave1
```

### 4. Edit `config_dcm2bids_batch.py` <a name="clust4">

Change the variables and/or paths in `config_dcm2bids_batch.py` script for your study and set `run_local = False`

### 5. Run `dcm2bids_batch.py` <a name="clust5">

- Log into the HPC  
  `ssh -X username@Talapas-ln1.uoregon.edu`
- Navigate into the `bidsQC/conversion` directory.  
  `cd path/to/bidsQC/conversion`
- Load python3  
  `module load python3`
- Run the batch script  
  `python3 dcm2bids_batch.py`
- Check the niftis, output logs, and error logs.

### 6. Check that your data are in BIDS <a name="clust6">

- Check the [specification.](https://bids.neuroimaging.io/)
- Use the [BIDS validator](http://incf.github.io/bids-validator)

If your data do not meet BIDS standards, see whether the scripts in the [bidsQC/qualityCheck folder](../qualityCheck) may be of use.

<hr>