""" main.py
    
    Author: Matthew Thomson

    References:
    [1] https://dev.fitbit.com/build/reference/web-api/
    [2] https://dev.fitbit.com/build/reference/web-api/activity/get-activity-tcx/
    [3] https://dev.fitbit.com/build/reference/web-api/explore/
"""
import json
import sys
from fitbit_api import fitbit_api
from datetime import date


def defines():
    """ defines the endpoints to be used later in the program """
    # get todays date
    today = date.today().strftime("%Y-%m-%d")


    # ref [1], a list of api requests
    endpoint = {
        "profile_info": "1/user/-/profile.json",
        "activity_date": "1/user/-/activities/date/2023-07-17.json",
        "all_activities": f"1/user/-/activities/list.json?beforeDate={today}&sort=asc&offset=0&limit=50",
        "all_sleep": f"1.2/user/-/sleep/list.json?beforeDate={today}&sort=asc&offset=0&limit=50",
        "gps": "1/user/-/activities/{activityId}.tcx",
        "delete_activity": "1/user/-/activities/{activityId}.json",
        "delete_sleep": "1/user/-/sleep/{sleepId}.json",
        "create_activity": "1/user/-/activities.json",
    }

    return endpoint


def api():
    """ collects the user information and uses the fitbit.api script 
        to get the authorised url and token."""
    # user details for accessing api
    with open("config.json") as conf:
        config = json.load(conf)

    CLIENT_ID = config["CLIENT_ID"]
    CLIENT_SECRET = config['CLIENT_SECRET']
    REDIRECT_URI = config['REDIRECT_URI']

    # pre set api parameters 
    api_parameters = fitbit_api(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    # get the authorisation url
    authorisation_url = api_parameters.get_authorisation_url()
    print("Go to this URL and authorise the app: " + authorisation_url)

    authorisation_response = input("Paste the full redirect URL here: ")
    
    # turns the http into a https
    #api_parameters.fetch_token(authorisation_response[:4] + "s" + authorisation_response[4:])
    # if redirect URL https, uncomment the next line instead
    api_parameters.fetch_token(authorisation_response)

    return api_parameters


def user_request(endpoint):
    """ Asks the user which end point they want and ensures it exists """
    # choose which data request to make
    for key in endpoint:
        print(key)
    request = input("\nWhat request do you want to make? ")

    # make sure request is one available
    while request not in endpoint:
        print("Incorrect request: Try again or type exit to stop")
        request = input("\nWhat request do you want to make?" )
        if request == "exit":
            sys.exit()

    return request


def get_ids(request, api_parameters, endpoint):
    """ getting all the activity ids """
    ids = []

    if request == "gps" or request == "delete_activity":
        entries = api_parameters.get_data(endpoint["all_activities"])
        for item in entries["activities"]:
            ids.append(item['logId'])

    elif request == "delete_sleep":
        entries = api_parameters.get_data(endpoint["all_sleep"])
        for item in entries["sleep"]:
            ids.append(item['logId'])

    print(f"IDs: {ids}")
    chosen_id = 0

    while chosen_id not in ids:
        chosen_id = input("Pick an ID from the above list, or type Exit to cancel \n")
        if chosen_id == "Exit":
            sys.exit()
        chosen_id = int(chosen_id)
    return chosen_id


def data(request, api_parameters, endpoint):
    """ Takes the users request and performs it to get the data that corresponds """
    
    if request[:6] == "delete":
        match request:
            case "delete_activity":
                print("It is recommended that you run 'all_activities' before deleting an ID")
                activityid =  get_ids(request, api_parameters, endpoint)
                print("delete_activity")
                endpoint = endpoint["delete_activity"].format(activityId=activityid)
                print(endpoint)

            case "delete_sleep":
                print("It is recommended that you run 'all_sleep' before deleting an ID")
                sleepid =  get_ids(request, api_parameters, endpoint)
                print("delete_sleep")
                endpoint = endpoint["delete_sleep"].format(sleepId=sleepid)
                print(endpoint)

            case _:
                print("error")

        data = api_parameters.delete_data(endpoint)

    elif request == "gps":
        activityid =  get_ids(request, api_parameters, endpoint)
        endpoint = endpoint["gps"].format(activityId=activityid)
        # [2] reference for tcx
        data = api_parameters.get_data(endpoint)

    elif request == "create_activity":
        print("Example information: \n {'activityId': '90013', 'manualCalories': '300', 'startTime': '10:00', 'durationMillis': '360000', 'date': '2023-06-25', 'distance': '0.50'} \n")
        print("Activity IDs: \n Walking: 90013 \n Running: 90009")
        query_parameters = {}
        keys = ["activityId", "manualCalories", "startTime", "durationMillis", "date", "distance"]
        for key in keys:
            value = input(f"Enter a value for {key}: ")
            if key == "activityId" or key == "manualCalories" or key == "durationMillis":
                query_parameters[key] = int(value)
            elif key == "distance":
                query_parameters[key] = float(value)
            else:
                query_parameters[key] = value
                
        data = api_parameters.create_activity(endpoint[request], query_parameters) 

    else:
        data = api_parameters.get_data(endpoint[request])
    return data


def main():
    endpoint = defines()
    api_parameters = api()
    request = user_request(endpoint)
    output = data(request, api_parameters, endpoint)
    
    # Checking is gps is the request method
    if request == "gps":
        with open('gps.tcx', 'wb') as file:
            file.write(output)
        sys.exit()
    else:
        # Write data to a file as a json dump
        with open(f"{request}.json", "w") as file:
            json.dump(output, file, indent=4)


if __name__ == "__main__":
    main()