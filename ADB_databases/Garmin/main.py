""" main.py
    Author: Matthew Thomson
    Date: 2023

    References:
    [1] https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html
    [2] https://stackoverflow.com/questions/68864871/why-does-pandas-json-normalizejson-results-raise-a-notimplementederror
    [3] https://www.learndatasci.com/solutions/python-pandas-dfexplode/#:~:text=Pandas'%20explode()%20flattens%20nested,their%20content%20to%20multiple%20rows. 

"""
import pandas as pd
from sqlalchemy import create_engine
import shutil
import os
import json


def read_dbs():
    """ reads in the database and sets it as a pandas dataframe """
    engine = create_engine("sqlite:///gcm_cache.db")
    query = "SELECT * FROM json_activities"
    gcm_cache_activities = pd.read_sql_query(query, engine)

    return gcm_cache_activities


def cached_val_retrieving(gcm_cache_activities):
    """ processes the cached_val column. references: [1-3] """

    # creates original csv for backup purposes
    gcm_cache_activities.to_csv("original\\original_gcm_cache_activities.csv", index=False)

    # copies the dataframe
    cached_val_df = gcm_cache_activities["cached_val"].copy()

    # making a df to put other dfs in for if more than one activity_charts exists
    all_activity_charts_df = []
    index = []

    # get the activity_charts row, cached_val column, out of the df and parses the json
    for row_index in range(len(cached_val_df)):
        if gcm_cache_activities.iloc[row_index]["data_type"] == "ACTIVITY_CHARTS":
            index.append(row_index)
            json_df = json.loads(cached_val_df[row_index])
            activity_charts_df = pd.json_normalize(json_df)

            all_activity_charts_df.append(activity_charts_df)

    # creates original csv for backup purposes
    # all_activity_charts_df.to_csv("original\\all_activity_charts_df.csv", index=False)
    
    return all_activity_charts_df, index


def processing_json(activity_charts_df):
    """ taking apart the json embedded inside the activity_charts rows cached_value field """

    metric_descriptors_json = pd.json_normalize(activity_charts_df["metricDescriptors"].explode())
    activityDetailMetrics_json = pd.json_normalize(activity_charts_df["activityDetailMetrics"].explode())
    gps_json = pd.json_normalize(activity_charts_df["geoPolylineDTO.polyline"].explode())

    # creates original csvs for backup purposes
    metric_descriptors_json.to_csv("original\\original_metric_descriptors_json.csv", index=False)
    activityDetailMetrics_json.to_csv("original\\original_activityDetailMetrics_json.csv", index=False)
    gps_json.to_csv("original\\original_gps_json.csv", index=False)
    activity_info_df = general_table_processing(metric_descriptors_json,activityDetailMetrics_json)

    return activity_info_df, gps_json


def general_table_processing(metrics_descriptors, details):
    """ takes the two embedded json values and merges the headers and details a dataframe """
    activity_info = {}
    
    # turns the keys and units to lists
    key_list = metrics_descriptors["key"].tolist()
    unit_list = metrics_descriptors["unit.key"].tolist()

    # makes the descriptor the key in the general info dictionary
    for index in range(len(key_list)):
        header = key_list[index] + " (" + unit_list[index] + ")"
        activity_info[str(header)] = []

    # adds the details to the key metrics
    for line in details["metrics"]:
        counter = 0
        for key in activity_info:
            activity_info[key].append(line[counter])
            counter += 1

    # turns the dictionary to a dataframe
    activity_info_df = pd.DataFrame(activity_info)

    # creates original csv for backup purposes
    activity_info_df.to_csv("original\\original_activity_info_df.csv", index=True)
    
    return activity_info_df


def time_modification(activity_info, gps_json):
    """ convert the time and modify it """
    gps_df = gps_json.copy()
    activity_df = activity_info.copy()

    hr_no = float(input("How many hours do you want to move the timestamp by? (add a '-' in front of your value to go back time) \n"))
    
    # note this is utc time
    gps_df["time"] = pd.to_datetime(gps_df["time"], unit="ms") + pd.Timedelta(hours=hr_no)
    activity_df["directTimestamp (gmt)"] = pd.to_datetime(activity_df["directTimestamp (gmt)"],
                                                        unit="ms") + pd.Timedelta(hours=hr_no)
    
    activity_df.to_csv("processed\\activity_df_time.csv", index=False)
    gps_df.to_csv("processed\\gps_df_time.csv", index=False)

    gps_df["time"] = (gps_df["time"].astype("int64") / 1e6).astype("int64")
    activity_df["directTimestamp (gmt)"] = (activity_df["directTimestamp (gmt)"].astype("int64") / 1e6).astype("int64")

    return activity_df, gps_df


def gps_modification(activity_info, gps_json):
    """ asking the user what gps modifcation they would like made and changing the gps value as requested """
    gps_df = gps_json.copy()
    activity_df = activity_info.copy()

    lat = float(input("What would you like to modify the Latitude value by? (add a '-' in front of your value to subtract) \n"))
    lon = float(input("What would you like to modify the Longitude value by? (add a '-' in front of your value to subtract) \n"))

    # changes the latitude and longitude by the number given 
    gps_df.loc[:, "lat"] = gps_df["lat"] + lat
    gps_df.loc[:, "lon"] = gps_df["lon"] + lon

    activity_df.loc[:, "directLatitude (dd)"] = activity_df["directLatitude (dd)"] + lat
    activity_df.loc[:, "directLongitude (dd)"] = activity_df["directLongitude (dd)"] + lon

    return activity_df, gps_df, lat, lon 


def updating_activity_charts_gps(activity_original, lat, lon):
    """ adding the latitude and longitude value increase onto every relevant column """
    activity_original.loc[:, "geoPolylineDTO.minLat"] = activity_original["geoPolylineDTO.minLat"] + lat
    activity_original.loc[:, "geoPolylineDTO.maxLat"] = activity_original["geoPolylineDTO.maxLat"] + lat
    activity_original.loc[:, "geoPolylineDTO.minLon"] = activity_original["geoPolylineDTO.minLon"] + lon
    activity_original.loc[:, "geoPolylineDTO.maxLon"] = activity_original["geoPolylineDTO.maxLon"] + lon

    return activity_original


def merge_backwards(all_edited_df, all_activity_info, all_gps_json, gcm_cache_activities, index):
    """ merging the changes back into the original gcm_cache_activities df """
    counter = 0
    for activity_charts_df in all_edited_df:
        activity_charts_df.to_csv("backwards\\before_activity_charts_df" + str(counter) + ".csv", index=False)
        all_activity_info[counter].to_csv("backwards\\before_activity_info" + str(counter) + ".csv", index=False)
        all_gps_json[counter].to_csv("backwards\\before_gps_df" + str(counter) + ".csv", index=False)
        gcm_cache_activities.to_csv("backwards\\before_gcm_cache_activities" + str(counter) + ".csv", index=False)

        # gets the values out of the df
        activity_vals = all_activity_info[counter].values

        # turns the values into lists and sets them as the values of the df column 'metrics'
        details = pd.DataFrame({'metrics': activity_vals.tolist()})

        # adds them back in the activity_charts_df df
        activity_charts_df.loc[:, "activityDetailMetrics"] = str(json.dumps(details.to_dict("records"), separators=(",", ":")))
        activity_charts_df.loc[0, "geoPolylineDTO.polyline"] = str(json.dumps(all_gps_json[counter].to_dict("records"), separators=(",", ":")))

        # adds after csvs for comparison 
        activity_charts_df.to_csv("backwards\\after_activity_charts_df" + str(counter) + ".csv", index=False)

        # merge activity_charts_df back into cached_val
        gcm_cache_activities.loc[index[counter], "cached_val"] = str((activity_charts_df.to_dict("records")))
        gcm_cache_activities.to_csv("backwards\\after_gcm_cache_activities" + str(counter) + ".csv", index=False)
        counter += 1

    return gcm_cache_activities


def replace_db(df):
    """ replaces the activity and exercise sqlite databases with the new dataframes """
    engine = create_engine("sqlite:///gcm_cache.db")
    df.to_sql("json_activities", engine, if_exists="replace", index=False)


def main():
    # copies the two databases to the current directory
    current_directory = os.getcwd()
    shutil.copyfile("dbs\\gcm_cache.db", current_directory + "\\gcm_cache.db")

    gcm_cache_activities = read_dbs()

    # activity_charts table in db
    all_activity_charts_df, index = cached_val_retrieving(gcm_cache_activities)
    
    all_edited_df = []
    all_activity_info = []
    all_gps_json = []

    for activity_charts_df in all_activity_charts_df:
        time = []
        activity_info, gps_json = processing_json(activity_charts_df)

        # prints the date of the chart
        time_df = pd.DataFrame()
        time_df["time"] = gps_json["time"].copy()
        time_df["time"] = (pd.to_datetime(time_df["time"], unit="ms") + pd.Timedelta(hours=1))
    

        if len(time) == 0:
            time = time_df.loc[0,"time"]
            print(f"This chart is time: {time}")
            edit = input("Do you want to modify this file? Y/N \n")

        # checks if the user wants to modify this file
        if edit == "Y":
            # editing the time and gps data 
            activity_info, gps_json = time_modification(activity_info, gps_json)
            activity_info, gps_json, lat, lon = gps_modification(activity_info, gps_json)

            # updates the max and mins for lat and lon values
            activity_charts_df_gps = updating_activity_charts_gps(activity_charts_df, lat, lon)
            all_edited_df.append(activity_charts_df_gps)

        elif edit == "N":
            print("Skipping modification... \n")
            all_edited_df.append(activity_charts_df)

        else:
            print("Exiting - Incorrect options picked")
            os.sys.exit()

        all_activity_info.append(activity_info)
        all_gps_json.append(gps_json)

    # need to merge all dfs back to og df
    full_df_edited = merge_backwards(all_edited_df, all_activity_info, all_gps_json, gcm_cache_activities, index)

    # putting the df into the database
    replace_db(full_df_edited)


if __name__ == "__main__": 
    main()
