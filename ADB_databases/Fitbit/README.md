# Fitbit Database Modifier
This directory contains scripts for modifying and deleting Fitbit activities within the activity and exercise databases. It is run interactively, giving options to the user within the terminal when running.

## Scripts
- fitbit_db.py (the main file)
- csv_analyser.py
- edit_db.py


## Setup
In the same directory as the fitbit_db.py, create the following folders:
- "activity"
- "dbs"
- "exercise"
- "test"

Ensure the activity_db and exercise_db are placed within the "dbs" directory.

## Pip Install's
```shell
pip install pandas
pip install sqlalchemy
```

## Output
Multiple csv files will be outputted to the activity, exercise, and test directories. These can be used for documentation purposes.  
**Note**: These csv outputs still need to be cleaned up. This will be fixed in a future upload.  

The modified activity_db and exercise_db databases will appear in the same directory as fitbit_db.py.
