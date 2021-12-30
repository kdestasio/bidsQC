# bidsQC Tutorial: University of Oregon

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
3. [git clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) that repo and update it as you make changes.  

#### If you want to track your study directory

***NOTE:** If you take the option of using version control at the level of the `studyName` folder, you will want to familiarize yourself with the `.gitignore` file to ensure you are not commiting any participant data or other sensitive information to your repository. The likelihood is that you will need to use a `.gitignore` file regardless, but it's essential if you will have participant data in your folder.

If you want to track changes for other scripts, files, etc. that you are using for your analyses:  

1. `cd` into the directory where you would like to store the bidsQC scripts (usually a study specific directory)  
e.g. `cd /projects/sanlab/shared/studyDir`  
2. [git clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the bidsQC repository into your folder  
    ```
    git clone https://github.com/kdestasio/bidsQC.git
    ```
3. `cd` into the `bidsQC` directory and remove the `.git` directory  
    ```
    cd bidsQC; rm -rf .git
    ```
4. Create a new repo one level up in your `studyName` directory.
    - On github, go to the "Repositories" tab. Click the green button "New" in the upper right-hand corner to create a new repository.
    - Name the repository EXACTLY what your study folder is named (e.g. if your folder is called Study-name, your repo must also be named Study-name)
    - Do NOT initialize the repository with a README, .gitignore, or license.
    - Click "Create repository"
    - At the command line, make sure you are in your study directory. If you are not `cd` into it. 
    - Follow the GitHub instructions to "create a new repository on the command line" by copy and pasting each command into your terminal.
    - This is a good time to create your .gitignore file. Let's initialize it to ignore the folder that will contain our bids data, as well as our pycache.  
        ```
        cat > .gitignore
        ```
        Then press enter. Now your cursor should be on the next line. Type the following on two seperate lines.
        ```
        bids_data/
        __pycache__/
        ```
        Press Ctrl+D when finished.

    - Be sure to add, commit, and push the .gitignore file nad the bidsQC directory and contents using the following commands.
        ```
        git add .gitignore bidsQC/
        git commit -m "Add bidsQC directory. Contents from https://github.com/kdestasio/bidsQC.git"
        git push
        ```
    - You may need to generate a Personal access token if you haven't yet done so. This is what you use when asked for a password when pushing a repo. To generate a token, click your User icon in the top right of the github page. Then select **Settings > Developer settings > Personal access tokens > Generate new token**. See the [github documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) on setting the token scope. Be sure to save the token somewhere secure where you can look it up later, like a password manager, or you will have to recreate it.

## Accessing the tutorial data

There are sample DICOMS available on Talapas. The path is:  
`/projects/lcni/dcm/repository/REV_examples`

## DICOM to Nifti conversion

Follow the instructions in the [`bidsQC/conversion/README.md`](/conversion/README.md#running-the-scripts-on-a-linux-cluster).  

## BIDS Validator on Talapas

We will create a singularity image of the [BIDS-validator tool](https://github.com/bids-standard/bids-validator) to use on Talapas. Once the image is created, we can submitted instructions via the command line to validate out dataset.

### Pull the singularity image

`cd` into the directory where you would like to store your singularity image.  
Then create the image with the following command, changing the date in the image name to today's.  

```
singularity pull bids-validator_2021-12-28.sif docker://bids/validator
```

### Run validation

From within the directory that contains the singularity image, run the following command from the command line. First change the paths so they point to your data and change the bids-validator image name to match the name you gave yours in the step above.  
```
singularity exec -B /projects/sanlab/shared/ctnTutorial/bids_data:/projects/sanlab/shared/ctnTutorial/bids_data:ro bids-validator_2021-12-28.sif \bids-validator /projects/sanlab/shared/ctnTutorial/bids_data
```
The validation results will be output in your terminal window.  
