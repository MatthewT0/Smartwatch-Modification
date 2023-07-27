""" gps_mod.py

    Author: Matthew Thomson
    Date: 2023

    References:
    [1] https://developer.garmin.com/fit/cookbook/
"""
import pandas as pd


def gps(df):
    """ modifying the gps """
    # ["Value 2", "Value 3"] are [lat, long]
    gps_df = df[["Value 2", "Value 3"]].copy()

    gps_df = edit_gps(gps_df)

    gps_df.to_csv("output\\gps_changes.csv", index=False)
    #return gps_df[["Lat [semi]", "Long [semi]"]]

    return gps_df[["test lat", "test long"]]


def edit_gps(gps_df):
    """ editing the gps information """
    # formats to degrees
    gps_df["Lat Deg"] = gps_df["Value 2"] / 11930465
    gps_df["Long Deg"] = gps_df["Value 3"] / 11930465
    
    # takes and makes users changes
    lat_change = float(input("What would you like to modify the Latitude value by? (add a '-' in front of your value to subtract) \n"))
    long_change = float(input("What would you like to modify the Longitude value by? (add a '-' in front of your value to subtract) \n"))
    gps_df["New Lat"] = gps_df["Lat Deg"] + lat_change
    gps_df["New Long"] = gps_df["Long Deg"] + long_change

    # formats back to semicircles (fit format)
    gps_df["Lat [semi]"] = gps_df["New Lat"] * 11930465
    gps_df["Long [semi]"] = gps_df["New Long"] * 11930465
    gps_df["test lat"] = gps_df["Lat [semi]"].apply(lambda x: '' if pd.isna(x) else format(x, ".0f"))
    gps_df["test long"] = gps_df["Long [semi]"].apply(lambda x: '' if pd.isna(x) else format(x, ".0f"))

    return gps_df
