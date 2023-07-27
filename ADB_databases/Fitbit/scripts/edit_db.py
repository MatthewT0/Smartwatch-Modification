""" edit_db.py
    Author: Matthew Thomson
    Date: 2023

    References:
    [1] find again -_-
    [2]
"""
import pandas as pd
import os
import scripts.csv_analyser as csv_analyser

def dataframe_process_control(exercise_event_df, session_activity_df,  exercise_segment_df, exercise_session_df, split_df):
    """ processes the databases """

    # gets the session id of the activity that is to be changed
    session_id = find_session_id(exercise_event_df, session_activity_df)

    # Edits the time and coordinates, additional functions can be added for other fields.
    # However, this is outwith the scope of this experiment.
    exercise_event_df_edited, hr_no = edit_times(exercise_event_df, session_id)
    exercise_event_df_edited = format_timestamp(exercise_event_df_edited)
    exercise_event_df_edited, lat, lon = edit_coords(exercise_event_df_edited, session_id)

    # amend activity details with same time change difference 
    session_activity_df = activity_time(session_activity_df, hr_no, session_id)

    # Edits the time and coordinates for the remaining exercise_db files
    exercise_session_df = edit_segment_session_df(exercise_session_df, hr_no, session_id)
    exercise_segment_df = edit_segment_session_df(exercise_segment_df, hr_no, session_id)
    split_df = edit_split_df(split_df,hr_no, lat, lon, session_id)

    return exercise_event_df_edited, session_activity_df, exercise_session_df, exercise_segment_df, split_df


def find_session_id(exercise_event_df_edited, session_activity_df):
    """ asks the user what session_id / details_id they would like to """
    print(session_activity_df[["SERVER_ID", "DETAILS_ID", "LOG_DATE", "START_TIME"]])
    session_id = input("Pick a details_id from the above list to modify information for: \n ")
    # implement to make sure session id / details id is in both
    
    return session_id


def activity_time(session_activity_df, hr_no, session_id):
    """ adds the same hour number to the activity start time and log date """
    session_activity_df_edit = session_activity_df[session_activity_df["DETAILS_ID"] == session_id]
    session_activity_df_times = session_activity_df_edit[["START_TIME", "LOG_DATE", "TIME_CREATED", "TIME_UPDATED"]].copy()

    # adds the hour number to the times 
    session_activity_df_times["NEW_START_TIME"] = (pd.to_datetime(session_activity_df_times["START_TIME"], unit="ms") + pd.Timedelta(hours=hr_no)).dt.time
    session_activity_df_times["NEW_LOG_DATE"] = pd.to_datetime(session_activity_df_times["LOG_DATE"], unit="ms") + pd.Timedelta(hours=hr_no)
    session_activity_df_times["NEW_TIME_CREATED"] = pd.to_datetime(session_activity_df_times["TIME_CREATED"], unit="ms") + pd.Timedelta(hours=hr_no)
    session_activity_df_times["NEW_TIME_UPDATED"] = pd.to_datetime(session_activity_df_times["TIME_UPDATED"], unit="ms") + pd.Timedelta(hours=hr_no)

    # reformats the times back - find source again
    session_activity_df_times["REFORMAT_START_TIME"] = session_activity_df_times["NEW_START_TIME"].apply(lambda x: (x.hour * 3600 + x.minute * 60 + x.second) * 1e3).astype("int64")
    session_activity_df_times["REFORMAT_LOG_DATE"] =  (session_activity_df_times["NEW_LOG_DATE"].astype("int64") / 1e6).astype("int64")
    session_activity_df_times["REFORMAT_TIME_CREATED"] =  (session_activity_df_times["NEW_TIME_CREATED"].astype("int64") / 1e6).astype("int64")
    session_activity_df_times["REFORMAT_TIME_UPDATED"] =  (session_activity_df_times["NEW_TIME_UPDATED"].astype("int64") / 1e6).astype("int64")

    # adds the time changes to a csv
    session_activity_df_times.to_csv("activity\\time_changes.csv", index=False)

    # merges the changes back into the df
    session_activity_df.loc[:, "START_TIME"] = session_activity_df_times["REFORMAT_START_TIME"]
    session_activity_df.loc[:, "LOG_DATE"] = session_activity_df_times["REFORMAT_LOG_DATE"]
    session_activity_df.loc[:, "TIME_CREATED"] = session_activity_df_times["REFORMAT_TIME_CREATED"]
    session_activity_df.loc[:, "TIME_UPDATED"] = session_activity_df_times["REFORMAT_TIME_UPDATED"]

    return session_activity_df


def edit_times(exercise_event_df, session_id):
    """ changes the time of exercise databases timestamp by x amount of hours chosen by the user. then reformats it as epoch """
    exercise_event_df_id = exercise_event_df[exercise_event_df["SESSION_ID"] == session_id].copy()
    hr_no = float(input("How many hours do you want to move the timestamp by? (add a '-' in front of your value to go back time) \n"))
    exercise_event_df_id.loc[:, "TIME"] = pd.to_datetime(exercise_event_df_id["TIME"], unit="ms") + pd.Timedelta(hours=hr_no)
    return exercise_event_df_id, hr_no


def format_timestamp(exercise_event_df):
    """ change back to correct time format - converts to nanoseconds since 1970-01-01 then divides to give correct epoch [1] """
    exercise_event_df.loc[:, "TIME"] = ((exercise_event_df["TIME"] - pd.Timedelta(hours=1)).astype('datetime64[ns]').view('int64') / 1e6)
    exercise_event_df.loc[:, "TIME"] = exercise_event_df["TIME"].apply(lambda x: format(x, ".0f"))

    return exercise_event_df


def edit_coords(exercise_event_df, session_id):
    """ changes the coordinates in the exercise database by x amount, chosen by the user. """
    exercise_event_df_id = exercise_event_df[exercise_event_df["SESSION_ID"] == session_id]
    lat = float(input("What would you like to modify the Latitude value by? (add a '-' in front of your value to subtract) \n"))
    lon = float(input("What would you like to modify the Longitude value by? (add a '-' in front of your value to subtract) \n"))

    exercise_event_df_id.loc[:, "LATITUDE"] = exercise_event_df_id["LATITUDE"] + lat
    exercise_event_df_id.loc[:, "LONGITUDE"] = exercise_event_df_id["LONGITUDE"] + lon

    return exercise_event_df_id, lat, lon


def edit_segment_session_df(df, hr_no, session_id):
    """ editing the segment dataframe by adding in the new start/stop times """

    # finds if its the segment or session dataframe to get the correct column headers
    if "SESSION_ID" in df.columns:
        filename = "exercise_segment"
        df_edit = df[df["SESSION_ID"] == session_id]
        df_times = df_edit[["START_TIME", "STOP_TIME", "SESSION_ID"]].copy()
    elif "UUID" in df.columns:
        filename = "exercise_session"
        df_edit = df[df["UUID"] == session_id]
        df_times = df_edit[["UUID", "START_TIME", "STOP_TIME"]].copy()
    else:
        print("There seems to be a problem with the dataframes.")
        os.sys.exit()

    # adds same hour to df
    df_times["NEW_START_TIME"] = pd.to_datetime(df_times["START_TIME"], unit="ms") + pd.Timedelta(hours=hr_no)
    df_times["NEW_STOP_TIME"] = pd.to_datetime(df_times["STOP_TIME"], unit="ms") + pd.Timedelta(hours=hr_no)
    df_times["REFORMAT_START_TIME"] =  (df_times["NEW_START_TIME"].astype("int64") / 1e6).astype("int64")
    df_times["REFORMAT_STOP_TIME"] =  (df_times["NEW_STOP_TIME"].astype("int64") / 1e6).astype("int64")

    # merges dfs
    df_edit.loc[:, "START_TIME"] = df_times["REFORMAT_START_TIME"]
    df_edit.loc[:, "STOP_TIME"] = df_times["REFORMAT_STOP_TIME"]

    # adds back to original df
    df.to_csv("test\\" + filename + "_before.csv", index=False)
    df = csv_analyser.add_back_in(df_edit, df)
    df.to_csv("test\\" + filename + "_after.csv", index=False)

    return df


def edit_split_df(split_df,hr_no, lat, lon, session_id):
    """ editing the datadrae for the splits and updating it with the new times and location """
    split_df_edit = split_df[split_df["SESSION_ID"] == session_id]
    split_df_times = split_df_edit[["TIME", "LATITUDE", "LONGITUDE", "SESSION_ID"]].copy()
    
    # adds same hour
    split_df_times["NEW_TIME"] = pd.to_datetime(split_df_times["TIME"], unit="ms") + pd.Timedelta(hours=hr_no)
    split_df_times["REFORMAT_TIME"] =  (split_df_times["NEW_TIME"].astype("int64") / 1e6).astype("int64")

    # adds same lat and lon
    split_df_times.loc[:, "LATITUDE"] = split_df_times["LATITUDE"] + lat
    split_df_times.loc[:, "LONGITUDE"] = split_df_times["LONGITUDE"] + lon

    # merges dfs
    split_df_edit.loc[:, "TIME"] = split_df_times["REFORMAT_TIME"]
    split_df_edit.loc[:, "LATITUDE"] = split_df_times["LATITUDE"]
    split_df_edit.loc[:, "LONGITUDE"] = split_df_times["LONGITUDE"]
    
    # adds back to original df
    split_df.to_csv("test\\split_df_before.csv", index=False)
    split_df = csv_analyser.add_back_in(split_df_edit,split_df)
    split_df.to_csv("test\\split_df_after.csv", index=False)

    return split_df