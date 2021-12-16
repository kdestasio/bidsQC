import os
import json

####################### Change these to your own paths/times/etc.#######################
path_bidsdata = os.path.join(os.sep, 'projects', 'sanlab', 'shared', 'studyName', 'bids_data')
include_echo_time = True
echo_time1 = '0.00437'
echo_time2 = '0.00683'
########################################################################################

def main():
    subjectdirs = get_subjectdirs()
    for subjectdir in subjectdirs:
        timepoints = get_timepoints(subjectdir)
        for timepoint in timepoints:
            func_dir_path = os.path.join(path_bidsdata, subjectdir, timepoint, 'func')
            fmap_dir_path = os.path.join(path_bidsdata, subjectdir, timepoint, 'fmap')
            if os.path.isdir(func_dir_path):
                func_niftis_partialpath = get_funcdir_niftis(func_dir_path, timepoint)
                if os.path.isdir(fmap_dir_path):
                    fmap_jsons = get_fmap_jsons(fmap_dir_path)
                    write_to_json(func_niftis_partialpath, fmap_jsons, fmap_dir_path, echo_time1, echo_time2)
            else:
                continue


def get_subjectdirs() -> list:
    """
    Returns subject directory names (not full path) based on the path_bidsdata (bids_data directory).

    @rtype:  list
    @return: list of subdirectories in bids_data that start with the prefix sub
    """
    bidsdir_contents = os.listdir(path_bidsdata)
    has_sub_prefix = [subdir for subdir in bidsdir_contents if subdir.startswith('sub-')]
    subjectdirs = [subdir for subdir in has_sub_prefix if os.path.isdir(os.path.join(path_bidsdata, subdir))]
    subjectdirs.sort()
    return subjectdirs


def get_timepoints(subject: str) -> list:
    """
    Returns a list of ses-wave directory names in a participant's directory.

    @type subject:  string
    @param subject: subject folder name

    @rtype:  list
    @return: list of ses-wave folders in the subject directory
    """
    subject_fullpath = os.path.join(path_bidsdata, subject)
    subjectdir_contents = os.listdir(subject_fullpath)
    return [f for f in subjectdir_contents if not f.startswith('.')]


def get_funcdir_niftis(func_dir_path:str, timepoint:str) -> list:
    """
    Returns a list of json files in the func directory.
    """
    func_niftis_partialpath = [os.path.join(timepoint, 'func/', f) for f in os.listdir(func_dir_path) if f.endswith('.nii.gz')]
    return func_niftis_partialpath


def get_fmap_jsons(fmap_dir_path):
    fmap_jsons = [f for f in os.listdir(fmap_dir_path) if f.endswith('.json')]
    return fmap_jsons


def write_to_json(func_niftis_partialpath:list, fmap_jsons:list, fmap_dir_path:str, echo_time1:str, echo_time2:str):
    for fmap_json in fmap_jsons:
        json_path = os.path.join(fmap_dir_path, fmap_json)
        with open(json_path) as target_json:
            json_file = json.load(target_json)
            json_file['IntendedFor'] = func_niftis_partialpath
            if include_echo_time:
                json_file['EchoTime1'] = echo_time1
                json_file['EchoTime2'] = echo_time2
        with open(json_path, 'w') as target_json:
            json.dump(json_file, target_json, indent=4)

main()
