# Garmin Database Modifier
This directory contains scripts for modifying Garmin activities within the gcm_cache database. It is run interactively, giving options to the user within the terminal when running.

## Scripts
- main.py

## Setup
In the same directory as the main.py, create the following folders:
- "backwards"
- "dbs"
- "original"
- "processed"

Ensure the gcm_cache database is placed within the "dbs" directory.

## Pip Install's
```shell
pip install pandas
pip install sqlalchemy
pip install json
```

## Output
Multiple csv files will be outputed to the backwards, original, and processed directories. These can be used for documentation purposes. The csv's in backwards are numbered by index of activity. Therefore, there may be a lot of these files.  
**Note**: These csv outputs still need to be cleaned up. This will be fixed in a future upload.  

The modified gcm_cache database will appear in the same directory as main.py.

