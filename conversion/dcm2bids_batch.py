# Import libraries and configuration file
import os
import subprocess
import config_dcm2bids_batch as cfg

# Main function
def main():
    """
    Run the things.
    """
    folders_tocheck = cfg.pathToBidsFolder, cfg.logdir
    check_dirs(folders_tocheck)
    logfile_fullpaths = cfg.errorlog, cfg.outputlog
    create_logfiles(logfile_fullpaths)
    check_dicomdir(cfg.pathToDicomFolder)
    batch_jobs(cfg.subjectlist, cfg.pathToDicomFolder, cfg.pathToConfigFile, cfg.pathToBidsFolder)


def batch_jobs(subject_list, pathToDicomFolder, pathToConfigFile, pathToBidsFolder):
    with open(subject_list) as file:
        lines = file.readlines()  
    for line in lines:
        entry = line.strip()
        subjectdir = entry.split(",")[0]
        subject = entry.split(",")[1]
        wave = entry.split(",")[2]
        subjectpath = os.path.join(pathToDicomFolder, subjectdir)
        if os.path.isdir(subjectpath):
            write_to_outputlog(subjectdir + os.linesep)
            if cfg.run_local:
                batch_cmd = 'dcm2bids -d {subjectpath} -s {wave} -p {subject} -c {pathToConfigFile} -o {pathToBidsFolder}  --forceDcm2niix --clobber'.format(subjectpath=subjectpath,  wave=wave, subject=subject, pathToConfigFile=pathToConfigFile,  pathToBidsFolder=pathToBidsFolder)
            else:
                batch_cmd = 'module load singularity; sbatch --job-name dcm2bids_{subjectdir} -A {account} --partition={partition} --time 00:60:00 --mem-per-cpu=2G --cpus-per-task=1 -o {logdir}/{subjectdir}_dcm2bids_output.txt -e {logdir}/{subjectdir}_dcm2bids_error.txt --wrap="singularity run -B {pathToDicomFolder} -B {pathToBidsFolder} -B {pathToConversionFolder} {singularity_image} -d {subjectpath} -s {wave} -p {subject} -c {pathToConfigFile} -o {pathToBidsFolder}  --forceDcm2niix --clobber"'.format(partition=cfg.partition, logdir=cfg.logdir, subjectdir=subjectdir, pathToDicomFolder=cfg.pathToDicomFolder, wave=wave, pathToConversionFolder=cfg.pathToConversionFolder, pathToConfigFile=cfg.pathToConfigFile, subject=subject, pathToBidsFolder=cfg.pathToBidsFolder, subjectpath=subjectpath, singularity_image=cfg.singularity_image, account=cfg.group)
            subprocess.call([batch_cmd], shell=True)
        else:
            write_to_errorlog(subjectdir + os.linesep)


def check_dicomdir(pathToDicomFolder):
    if not os.path.isdir(pathToDicomFolder):
        write_to_errorlog("Incorrect dicom directory specified")


def touch(path:str):
    """
    Create a new file
    
    @type path:     string
    @param path:    path to - including name of - file to be created
    """
    with open(path, 'a'):
        os.utime(path, None)


def check_dirs(dir_fullpaths:list):
    """
    Check if a directory exists. If not, create it.

    @type dir_fullpaths:        list
    @param dir_fullpaths:       Paths to directorys to check
    """
    for dir_fullpath in dir_fullpaths:
        if not os.path.isdir(dir_fullpath):
            os.mkdir(dir_fullpath)

            
def create_logfiles(logfile_fullpaths:list):
    """
    Check if a logfile exists. If not, make one.

    @type logfile_fullpaths:         list
    @param logfile_fullpaths:        Paths to logfiles to check
    """
    for logfile_fullpath in logfile_fullpaths:
        if not os.path.isfile(logfile_fullpath):
            touch(logfile_fullpath)


def write_to_outputlog(message):
    """
    Write a log message to the output log. Also print it to the terminal.

    @type message:          string
    @param message:         Message to be printed to the log
    """
    with open(cfg.outputlog, 'a') as logfile:
        logfile.write(message + os.linesep)
    print(message)


def write_to_errorlog(message):
    """
    Write a log message to the error log. Also print it to the terminal.

    @type message:          string
    @param message:         Message to be printed to the log
    """
    with open(cfg.errorlog, 'a') as logfile:
        logfile.write(message + os.linesep)
    print(message)


main()