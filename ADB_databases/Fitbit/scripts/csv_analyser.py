""" csv_analyser.py
    Author: Matthew Thomson
    Date: 2023

    References:
    [1] https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isin.html
    [2] https://docs.sqlalchemy.org/en/14/core/connections.html
"""
import pandas as pd
from sqlalchemy import create_engine, text
import os

def read_dbs():
    """ reads in the databases using SQL queries """
    # opens the engine for the sqlite database exercise_db
    engine = create_engine("sqlite:///exercise_db")
    
    query1 = "SELECT * FROM EXERCISE_SEGMENT"
    exercise_segment_df = pd.read_sql_query(query1, engine)

    query2 = "SELECT * FROM EXERCISE_SESSION"
    exercise_session_df = pd.read_sql_query(query2, engine)

    query3 = "SELECT * FROM SPLIT"
    split_df = pd.read_sql_query(query3, engine)

    query4 = "SELECT * FROM EXERCISE_EVENT"
    exercise_df = pd.read_sql_query(query4, engine)

    # opens the engine for the sqlite database activity_db
    engine1 = create_engine("sqlite:///activity_db")
    query5 = "SELECT * FROM ACTIVITY_LOG_ENTRY"
    activity_df = pd.read_sql_query(query5, engine1)

    return exercise_segment_df, exercise_session_df, split_df, activity_df, exercise_df


def session_id_activity(activity_df,exercise_df):
    """ extract df the dfs and only gives the activity fields that match gps info in the exercise file """
    session_activity_df = activity_df[activity_df["DETAILS_ID"].isin(exercise_df["SESSION_ID"])]
    
    return session_activity_df


def add_back_in(edited_df, original_df):
    """ adds the modified data back in the original dataframe """

    # sets both dfs to use the _id field as their index
    edited_df.set_index("_id", inplace=True)
    original_df.set_index("_id", inplace=True)
    # updates the dataframe
    original_df.update(edited_df)
    # adds the _id index back in 
    original_df.reset_index(inplace=True)

    return original_df


def replace_db(session_activity_df, exercise_df,exercise_session_df,exercise_segment_df,split_df):
    """ replaces the activity and exercise sqlite databases with the new dataframes """
    
    activity_engine = create_engine("sqlite:///activity_db")
    session_activity_df.to_sql("ACTIVITY_LOG_ENTRY", activity_engine, if_exists="replace", index=False)
    
    exercise_engine = create_engine("sqlite:///exercise_db")
    exercise_df.to_sql("EXERCISE_EVENT", exercise_engine, if_exists="replace", index=False)
    exercise_session_df.to_sql("EXERCISE_SESSION", exercise_engine, if_exists="replace", index=False)
    exercise_segment_df.to_sql("EXERCISE_SEGMENT", exercise_engine, if_exists="replace", index=False)
    split_df.to_sql("SPLIT", exercise_engine, if_exists="replace", index=False)


def delete_field(session_activity_df, exercise_event_df):
    """ delete entry from sqlite database [2] using SQL queries """
    # set up engines
    activity_engine = create_engine("sqlite:///activity_db")    
    exercise_engine = create_engine("sqlite:///exercise_db")

    # ask the user which id they want to delete
    print(session_activity_df[["SERVER_ID", "DETAILS_ID", "LOG_DATE", "START_TIME"]])
    session_id = input(" 1. Pick a details_id from the above list to delete \n 2. If there is no session_id pick the server_id \n 3. type 'exit' to quit \n")

    if session_id == "exit":
        os.sys.exit()
    
    elif session_id not in session_activity_df["DETAILS_ID"].values:
        # deletes by server_id instead which is an activity only present in the activity_db database
        print("Activity has no GPS information - deleting from activity_db now...")
        with activity_engine.connect() as connection:
            delete_query = text("DELETE FROM ACTIVITY_LOG_ENTRY WHERE SERVER_ID = :server_id")
            connection.execute(delete_query, {"server_id": session_id})
            connection.commit()
            print(f"server_id {session_id} deleted")
        os.sys.exit()
    
    elif session_id  in session_activity_df["DETAILS_ID"].values:
        with activity_engine.connect() as connection:
            delete_query = text("DELETE FROM ACTIVITY_LOG_ENTRY WHERE DETAILS_ID = :session_id")
            connection.execute(delete_query, {"session_id": session_id})
            connection.commit()

        with exercise_engine.connect() as connection:
            delete_query1 = text("DELETE FROM EXERCISE_EVENT WHERE SESSION_ID = :session_id")
            connection.execute(delete_query1, {"session_id": session_id})
            connection.commit()

            delete_query2 = text("DELETE FROM EXERCISE_SEGMENT WHERE SESSION_ID = :session_id")
            connection.execute(delete_query2, {"session_id": session_id})
            connection.commit()

            delete_query3 = text("DELETE FROM EXERCISE_SESSION WHERE UUID = :session_id")
            connection.execute(delete_query3, {"session_id": session_id})
            connection.commit()

            delete_query4 = text("DELETE FROM SPLIT WHERE SESSION_ID = :session_id")
            connection.execute(delete_query4, {"session_id": session_id})
            connection.commit()

        print(f"Session_id {session_id} deleted")
    
    else:
        print("Something went wrong")
