# Smartwatch Modification for Digital Forensics Investigation
This repository was created for the purpose of the practical section of an honours dissertation. It contains a collection of scripts and tools developed for the Garmin and Fitbit smartwatches. The specific smartwatches used for testing were a Garmin Venu and a Fitbit Versa. 

## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Repository Overview](#Repository-Overview)
  - [ADB Databases](#adb-databases)
  - [Fitbit API](#fitbit-api)
  - [Garmin Manual](#garmin-manual)
- [Current Project Status](#current-project-status)
- [Latest Updates](#latest-updates)


## Project Overview
The aim of this project is to test the reliability of digital evidence from smartwatches using basic anti-forensics techniques. These techniques involve the modification and deletion of smartwatch data. The devices are imaged before and after the tampering of data. The digital evidence is then analysed to see if the tampering can be detected and if the unaltered data can be recovered.


## Repository Structure
The repository is structured as follows:
``` 
Smartwatch-Modification
│
├── ADB_databases
│   ├── Fitbit
│   └── Garmin
├── Fitbit API
└── Garmin_Manual
```


## Repository Overview
### ADB Databases
The ADB databases directory contains scripts for interacting with the databases of Fitbit and Garmin devices. These scripts allow you to modify and delete entries in the activity and exercise database files taken from an ADB pull of the phone.  
For more details, see the [Fitbit ADB README](https://github.com/MatthewT0/Smartwatch-Modification/tree/main/ADB_databases/Fitbit) and [Garmin ADB README](https://github.com/MatthewT0/Smartwatch-Modification/tree/main/ADB_databases/Garmin).

### Fitbit API
The API directory contains scripts for interacting with the Fitbit API. These scripts allow you to view, modify, and delete activities from the Fitbit using the API.  
For more details, see the [Fitbit API README](https://github.com/MatthewT0/Smartwatch-Modification/tree/main/Fitbit_API/Fitbit).

### Garmin Manual
The Garmin Manual directory contains scripts for manually modifying Garmin activity fit files.  
For more details, see the [Garmin ADB README](https://github.com/MatthewT0/Smartwatch-Modification/tree/main/Garmin_Manual/Garmin).


## Current Project Status
**NOTE**: This project is still in the testing phase. More updates will be coming soon to add more functionality, improve error handling, fix style issues, and more. Please feel free to report any issues or contribute to the project.  
This project is under MIT licensing, see [LICENSE.md](LICENSE.md).

## Latest Updates
### Version 0.1.0 - 27-07-2023
#### Added
- Repository uploaded. No changes have been made since this first version.

For full changelog, see [CHANGELOG.md](CHANGELOG.md).
