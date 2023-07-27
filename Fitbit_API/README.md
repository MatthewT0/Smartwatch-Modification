# Fitbit API Modifier
This directory contains scripts to view, modify, and delete Fitbit API activities and information. 

## Scripts
- main.py
- fitbit_api.py

## Pip Install's
```shell
pip install requests_oauthlib
```
## Setup
Make sure to fill in the config file with your information and do not upload or share this!

### Running the Script
Once clicking run on the main.py script, you will need to authenticate the session using the url. When you go to this url you will need to log in and provide permissions that you feel acceptable to provide. After providing the permissions it will take you to your redirect link set up from the app. Copy the URL that appears on this page and paste it back in. This will then authenticate your session and allow you to choose one of the options from the interactive terminal.  

It is currently implemented to allow for:
- profile_info - view all profile information 
- activity_date - view activities from a specified date. Specified in endpoint code.
- all_activities - view all activities
- all_sleep - view all sleep
- gps - view a specified gps/tcx file. Specified in interactive terminal.
- delete_activity - delete a specified activity. Specified in interactive terminal.
- delete_sleep - delete a specified sleep file. Specified in interactive terminal.
- create_activity - create a new activity through interactive terminal.

## Output
Depending on what you choose a JSON or TCX file will appear in the same directory as the main.py. This will contain the information of the output. If you choose one of the deletes this will contain information based on whether it was successful or not.  
**Note**: This file will be overwritten each time you run the script if you don't rename or move it.
