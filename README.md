# ExtractFilesFromSubfolders


## Description:

Easily extract all unique files from all sub folders within a chosen folder and move them to chosen folder's root directory.
When run, it creates log file named logs.txt in working directory to write program execution details. You can open it to see what it did, or errors that might have occured in there.
It also creates a folder ....restore in working directory. Please do not delete this folder as it is required for proper restoration of files.


## Safety Precautions:
1. It should be obvious that if the data is critical, it should be backed up before making any modifications.
2. Keep in mind that this program is only tested on windows 10 by me. So test it on windows or linux of your machine on dummy data to see if it works. 
3. If you are modifying the code, remember that the program calls shutil.rmtree(default_restore_folder) only once throughout the whole porgram to delete restore folder after restoration attempt. So, make sure that the default_restore_folder does not point to anything you don't want getting deleted.


## Steps to Extract Files: 

1. Put ExtractFilesFromSubfolders.py file in a folder where you want to extract subfolder files out to this folder. 
2. Execute ExtractFilesFromSubfolders.py file using Python.
3. Result: Files should have been extracted now. Empty subfolders from which files were extrated should have been deleted now. A restore folder "....restore" and log file "logs.txt" should have been created in the working directory.


## Steps to Restore Files:

1. Execute ExtractFilesFromSubfolders.py file using Python.
2. Result: Files should have been restored now. Restore folder "....restore" should have been deleted, and log file should have been updated(created if it does not exist).


## What's not done:

Only one file that has several names will be extrated to working directory. Rest of the similar named files will not be moved. 
Non empty subfolders will not be deleted. 
