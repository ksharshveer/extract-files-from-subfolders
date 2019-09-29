# extract-files-from-subfolders

## Description:
Easily extract all unique files from all folder(s) within a chosen folder and move them to this chosen folder's root directory.

## Program Behavior
When run, it creates log file named "logs.txt" in working directory to write program execution details. You can open it to see what it did, or errors that might have occured in there.
It also creates a folder "....restore" in working directory. Please do not delete this folder as it is required for proper restoration of files.

## Safety Precautions:
* If the data is critical, it should be backed up before using this program.
* If you are modifying the code, remember that the program calls shutil.rmtree(default_restore_folder) only once throughout the whole porgram to delete restore folder after restoration attempt. So, make sure that the `default_restore_folder` does not point to anything you don't want getting deleted.

## Steps to Extract Files: 
1. Put extract.py file in a folder where you want to extract subfolder files out to this folder. 
2. Execute extract.py file using Python.
3. Result: Files should have been extracted now. Empty subfolders from which files were extrated should have been deleted now. A restore folder "....restore" and log file "logs.txt" should have been created in the working directory.

## Steps to Restore Files:
1. Execute extract.py file again using Python.
2. Result: Files should have been restored now. Restore folder "....restore" should have been deleted, and log file "logs.txt" should have been updated(created if it did not already exist).

## What's not done:
Only one file which is encountered first during execution, that has several exact same names will be extracted to working directory. Rest of the same named files will not be moved.
Non empty subfolders will not be deleted. 
Created log file "logs.txt" is never deleted.
