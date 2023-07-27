""" time_mod.py

    Author: Matthew Thomson
    Date: 2023

    References:
    [1] https://developer.garmin.com/fit/cookbook/datetime/
"""
import pandas as pd


def timestamp_mod(df):
    """ calls all the timestamp functions """
    time_df = format_ts(df)

    # edits the timestamp
    time_df = edit_ts(time_df)

    # changes time stamp back to original fit format
    time_df = tsFit_format(time_df)

    time_df.to_csv("output\\time_changes.csv", index=False)

    return time_df["New Timestamp"]


def format_ts(df):
    """ edits the timestamps """
    # gets the timestamp values
    time_df = df[["Value 1"]].copy()

    time_df["Original"] = time_df["Value 1"]

    # convert to utc +1 timestamp ref: [2]
    time_df.loc[:,"Value 1"] = pd.to_datetime((time_df["Value 1"] + 631065600), unit="s") + pd.Timedelta(hours=1)

    return time_df


def edit_ts(time_df):
    """ edit the timestamp """
    hr_no = float(input("How many hours do you want to move the timestamp by? (add a '-' in front of your value to go back time) \n"))
    time_df["New"] = time_df["Value 1"] + pd.Timedelta(hours=hr_no)

    return time_df


def tsFit_format(time_df):
    """ changing the timestamps back to fit format """

    # Convert datetime column back to fit timestamps
    time_df["Fit Timestamp"] = ((time_df["Value 1"] - pd.Timedelta(hours=1)).astype('int64') / 1e9) - 631065600
    time_df["Fit Timestamp"] = time_df["Fit Timestamp"].apply(lambda x: format(x, ".0f"))
    
    # this is the one to put back in df
    time_df["New Timestamp"] = ((time_df["New"] - pd.Timedelta(hours=1)).astype('int64') / 1e9) - 631065600
    time_df["New Timestamp"] = time_df["New Timestamp"].apply(lambda x: format(x, ".0f"))

    return time_df
