# bidsQC Tutuorial: University of Oregon

## Setup
### Create a github account

[Create a github account](https://github.com/) if you don't already have one.

### Get the bidsQC repository for your study

Decide whether you want to use version control to:  

- track only your changes to the bidsQC scripts, or  
- track changes to your bidsQC AND other scripts, files, etc. that you are using for your analyses

#### If you want to track only the bidsQC scripts

1. Fork the bidsQC repo to your own account.
2. `cd` into the directory where you would like to store the bidsQC scripts (usually a study specific directory)  
e.g. `cd /projects/sanlab/shared/studyDir`  
3. `git clone` that repo and update it as you make changes.  

#### If you want to track your study directory

If you want to track changes for other scripts, files, etc. that you are using for your analyses:  

1. `cd` into the directory where you would like to store the bidsQC scripts (usually a study specific directory)  
e.g. `cd /projects/sanlab/shared/studyDir`  
2. `git clone` the bidsQC repository into your folder  
3. remove the `.git` directory  
    `rm -rf .git` 
4. Create a new repo one level up in yout `studyName` directory by following the steps in the [GitHub docs](https://docs.github.com/en/github/importing-your-projects-to-github/importing-source-code-to-github/adding-an-existing-project-to-github-using-the-command-line)
        
***NOTE:** If you take the option of using version control at the level of the `studyName` folder, you will want to familiarize yourself with the `.gitignore` file to ensure you are not commiting any participant data or other sensitive information to your repository. The likelihood is that you will need to use a `.gitignore` file regardless, but it's essential if you will have participant data in your folder.

## Accessing the tutorial data

## DICOM to Nifti conversion

### Convert an entire directory's contents

Follow the steps in the unfmontreal tutorial.

### Convert a subset of participants

1. Collect the metadate from your DICOMs by using the Dcn2Bids helper.
2. Create a file called `subject_list.txt`.



