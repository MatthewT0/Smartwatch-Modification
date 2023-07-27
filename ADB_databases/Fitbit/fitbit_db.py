""" fitbit_db.py
    Author: Matthew Thomson
    Date: 2023
"""
import pandas as pd
from sqlalchemy import create_engine
import scripts.csv_analyser as csv_analyser
import scripts.edit_db as edit_db
import shutil
import os

def main():
    # copies the two databases to the current directory
    current_directory = os.getcwd()
    shutil.copyfile("dbs\\activity_db", current_directory + "\\activity_db")
    shutil.copyfile("dbs\\exercise_db", current_directory + "\\exercise_db")

    # reads in the dataframes
    exercise_segment_df, exercise_session_df, split_df, activity_df, exercise_event_df = csv_analyser.read_dbs()

    # gives relevant activity files (to exercise ones)
    session_activity_df = csv_analyser.session_id_activity(activity_df, exercise_event_df)

    # edits the dataframes
    exercise_event_df_edited, session_activity_df, exercise_session_df, exercise_segment_df, split_df = edit_db.dataframe_process_control(exercise_event_df, session_activity_df,  exercise_segment_df, exercise_session_df, split_df)

    # merging the databases together    
    exercise_event_df_edited = csv_analyser.add_back_in(exercise_event_df_edited, exercise_event_df)
    exercise_event_df_edited.to_csv("exercise\\edited_ex_df.csv", index=False)

    session_activity_df = csv_analyser.add_back_in(session_activity_df, activity_df)
    session_activity_df.to_csv("activity\\edited_act_df.csv", index=False)

    # put df in the databases exercise_df
    csv_analyser.replace_db(session_activity_df, exercise_event_df_edited,exercise_session_df,exercise_segment_df,split_df)

    # deletes field
    csv_analyser.delete_field(session_activity_df, exercise_event_df_edited)


if __name__ == "__main__": 
    main()
