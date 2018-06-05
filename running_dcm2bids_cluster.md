# Running dcm2bids on a Linux Cluster
## Dependencies

- SLURM
- Python3
- Dcm2Bids singularity container **You need to download it.**
    - For instructions on copying singularity containers, see [Containers: Docker & Singularity](https://uosanlab.atlassian.net/wiki/spaces/SW/pages/45285423) (and, as always, read the [documentation](http://singularity.lbl.gov/docs-build-container))
    - The container is available on [Singularity Hub](https://singularity-hub.org/collections/544)
    - \* Note that when you copy the container, you either need to name it `Dcm2Bids-master.simg` or change the image name in the `config_dcm2bids_batch.py` script.


## Steps to convert DICOMS to BIDS

1. Create the `subject_list.txt` where each row has the input: `directoryName,subjectID,waveNumber`
    - An easy way to do this is to `cd` into your DICOM directory and use the command `ls >> subject_list.txt` , which will create a text file of that name and populate it with all the directories/files in your working directory. You can then move that subject_list.txt file to the directory from which you will be running your code and add the subject ID and time-point columns.
    - The subject_list should be formatted such that each row consists of: the subject directory names (that contains the dicoms), desired subject ID, and data collection wave number. Each field is comma separated, all without spaces, e.g.:

    `sub01_20150909,REV001,wave1`

    `sub01_20150909,REV001,wave2`

    `sub02_20150909,REV001,wave1`

2. Edit the `study_config.json` file such that it works for your study.  
    - See the [dcm2Bids](https://github.com/cbedetti/Dcm2Bids) repository for documentation and instructions. ← for real, you'll need to read the instructions.  
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