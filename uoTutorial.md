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
3. [`git clone`](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) that repo and update it as you make changes.  

#### If you want to track your study directory

If you want to track changes for other scripts, files, etc. that you are using for your analyses:  

1. `cd` into the directory where you would like to store the bidsQC scripts (usually a study specific directory)  
e.g. `cd /projects/sanlab/shared/studyDir`  
2. [`git clone`](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) the bidsQC repository into your folder  
3. `cd` into the `bidsQC` directory and remove the `.git` directory  
    `cd bidsQC; rm -rf .git` 
4. Create a new repo one level up in your `studyName` directory.
    - On github, go to the "Repositories" tab. Click the green button "New" in the upper right-hand corner to create a new repository.
    - Name the repository EXACTLY what your study folder is named (e.g. if your folder is called Tardis-blue, your repo must also be named Tardis-blue)
    - Do NOT initialize the repository with a README, .gitignore, or license.
    - Click "Create repository"
    - Make sure you are in your study directory. If you are not `cd` into it. 
    - Follow the instructions to "create a new repository on the command line" by copy and pasting each command into your terminal.
    - Be sure to add, commit, and push the bidsQC directory and contents as well.
    - You may need to generate a Personal access token if you haven't yet done so. This is what you use when asked for a password when pushing a repo. To generate a token, click your User icon in the top right of the github page. Then select Settings > Developer settings > Personal access tokens > Generate new token. See the [github documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) on setting the token scope. Be sure to save the token somewhere secure where you can look it up later, like a password manager, or you will have to recreate it.


        
***NOTE:** If you take the option of using version control at the level of the `studyName` folder, you will want to familiarize yourself with the `.gitignore` file to ensure you are not commiting any participant data or other sensitive information to your repository. The likelihood is that you will need to use a `.gitignore` file regardless, but it's essential if you will have participant data in your folder.

## Accessing the tutorial data

## DICOM to Nifti conversion

Follow the instructions in the [`bidsQC/conversion/README.md`](/conversion/README.md#running-the-scripts-on-a-linux-cluster).  


