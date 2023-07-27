# Garmin Manual Fit File Modification
This directory contains scripts for manually modifying Garmin activity fit files. It is run interactively, giving options to the user within the terminal when running.

## Scripts
- fit_file_modification.py (main file)
- gps_mod.py
- time_mod.py


## Setup
In the same directory as the fit_file_modification.py, create the following folders:
- "csv"
- "output"

These folders are needed for the program to work correctly. The csv folder is where you should input the csv files that have been converted using the fitSDK. The output folder is where all outputted files from the program are executed.  
This includes:
- "before_changes.csv" - a csv file that should match the same format as the one inputted.
- "changed_fit.csv" - a csv with the changes made from the code formatted into it.
- "time_changes.csv" - a csv with a documentation of time changes made. 

## Using FitCSVTool
Use the fitSDK in the following way to get the csv file needed for the program:
1. Go to the Java directory and open a terminal, then input the following command into the terminal:
```shell
java -jar FitCSVTool.jar -se --defn none --data record "your_fit_filename.fit"
```

> This will output two csv files created from your fit file. 
2. Move the one that doesn't have "_data" on it to the csv folder.

## Pip Install's
```shell
pip install pandas 
```

You are now ready to run the main script! (fit_file_modification.py)


## Output - What Next?
Once the program is run, the "after_changes.csv" is the one you will want to reconvert to .fit format.  
To do this relocated to the Java directory of the fitSDK and open a terminal, also move this csv file to this directory. 

Type the following command into the terminal:
```shell
java -jar FitCSVTool.jar -c "after_changes.csv" "fit_filename_of_choice"
```
>This will place the fit file in the current directory that the terminal is open within.