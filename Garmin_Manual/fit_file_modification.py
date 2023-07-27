""" fit_file_modification.py

    Author: Matthew Thomson
    Date: 2023

    References:
    [1] https://developer.garmin.com/fit/cookbook/datetime/
    [2] https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html#pandas.to_datetime

    Note: Error handling needs to be added
"""
import pandas as pd
import os
import additional_files.time_mod as time_mod
import additional_files.gps_mod as gps_mod

def read_file():
    """ allows the user to choose whatever filename they want from the options then turns it to a dataframe """
    files = []
    filename = ""

    try:
        # finds all files in the csv directory with a .csv extension
        for fname in os.listdir("csv"):
            if fname.endswith(".csv"):
                files.append(fname)
                print(f"{fname} \n")
        
        # asks the user to select a file to process that is within the directory
        while filename not in files:
            filename = input("From the files listed above, which would you like to process? \n")

        df = pd.read_csv("csv\\" + filename)

    except FileNotFoundError as err:
        print("File was not found. Ensure directory names are correct and file exists")
    
    return df


def main():
    df = read_file()
    #df = pd.read_csv("csv\\2023-06-02-21-58-59.csv")
    df1 = df.copy()

    df1.to_csv("output\\before_changes.csv", index=False)

    time_df = time_mod.timestamp_mod(df)
    df1["Value 1"] = time_df

    gps_df = gps_mod.gps(df)
    df1[["Value 2", "Value 3"]] = gps_df
    
    # gets rid of added column
    df1 = df1.rename(columns={'Unnamed: 39': ' '})
    df1.to_csv("output\\after_changes.csv", index=False)
    

    # terminal prints for tests:
    #print(df.columns)
    #print(df)
    #print(df1)
    #print(df2)

if __name__ == "__main__": 
    main()
