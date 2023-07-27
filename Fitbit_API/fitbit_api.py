""" fitbit_api.py

    Author: Matthew Thomson

    References:
    [1] https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html
    [2] https://dev.fitbit.com/build/reference/web-api/developer-guide/authorization/
    [3] https://www.programcreek.com/python/example/82395/requests_oauthlib.OAuth2Session
"""
from requests_oauthlib import OAuth2Session


class fitbit_api:
    AUTHORISATION_URL = "https://www.fitbit.com/oauth2/authorize"
    TOKEN_URL = "https://api.fitbit.com/oauth2/token"

    def __init__(self, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI):
        """ defines variables for use throughout code and gets the session """
        self.client_secret = CLIENT_SECRET
        # all scopes available
        scope=["activity", "heartrate", "location", "nutrition", 
                "oxygen_saturation", "profile", "respiratory_rate", 
                "settings", "sleep", "social", "temperature", "weight"]
        self.session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=scope)

    def get_authorisation_url(self):
        """ gets the authorised url"""
        authorisation_url, state = self.session.authorization_url(self.AUTHORISATION_URL)
        return authorisation_url


    def fetch_token(self, authorisation_response):
        """ gets the token and returns just the access_token part for use """
        token = self.session.fetch_token(
            self.TOKEN_URL,
            authorization_response=authorisation_response,
            client_secret=self.client_secret
        )
        #print(f"{token} \n")
        return token["access_token"]


    def get_data(self, endpoint):
        """ gets the data from the api based on the endpoint requested and 
            returns it in relevant format, based on choice """
        print(endpoint)
        response = self.session.get(f"https://api.fitbit.com/{endpoint}")
        if endpoint.endswith(".tcx"): 
            # Parse XML response
            return response.content
        else:
            # Parse JSON response
            return response.json()


    def delete_data(self, endpoint):
        """ deletes the data from the session """
        print(endpoint)
        response = self.session.delete(f"https://api.fitbit.com/{endpoint}")
        try:
            return response.json()
        except:
            print(response)
            print("No return performed")


    def create_activity(self, endpoint, query_params):
        """ creates an activity [3] """
        response = self.session.post(f"https://api.fitbit.com/{endpoint}", query_params)
        try:
            return response.json()
        except:
            print(response)
            print("No return performed")
