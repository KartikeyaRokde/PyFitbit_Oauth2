"""
A python library for testing Fitbit's OAuth 2.0 flow.
Fitbit OAuth 2.0 documentation: https://dev.fitbit.com/docs/oauth2/
"""

import requests
import urllib
import base64

#------------------------------------------------------------------------------

class PyFitbit_Oauth2():
    
    # # Defining global constants
    
    # Fitbit authorization uri
    FITBIT_AUTH_URL = 'https://www.fitbit.com/oauth2/authorize'
    
    # Fitbit token uri
    FITBIT_TOKEN_URL = 'https://api.fitbit.com/oauth2/token'
    
    # Scopes needs to be specified while getting access token. Only user permitted scopes are given access with the access token
    APPLICATION_SCOPES = ['activity', 'heartrate', 'location', 'nutrition', 'profile', 'settings', 'sleep', 'social', 'weight']
    
    # Fitbit API endpoints
    ACTIVITIES_TIMESERIES_URL = "https://api.fitbit.com/1/user/-/activities/log/steps/date/today/1d.json"
    
    def __init__(self, oauth2_client_id, client_secret, oauth2_redirect_uri):
        """
        @param oauth2_client_id: OAuth2 Client ID obtained from Fitbit application page
                                 - Login to https://dev.fitbit.com/
                                 - You'll find the 'OAuth 2.0 Client ID' under your app in 'MANAGE MY APPS'
        @param client_secret: The client (Consumer) secret of your application
        @param oauth2_redirect_uri: The redirect URI (Callback URL) specified in the application
                                    - Callback URL is mandatory for OAuth 2.0 applications
                                    - You can set a/multiple Callback URLs by editing your application details
                                    - It must be a valid URL where the auth code is redirected.
                                    - an https redirect_uri is recommended
                                    - For iOS/Android, you can specify the registered URI from your application 
        """
        # Initializing client details
        self.client_id = oauth2_client_id
        self.client_secret = client_secret
        self.redirect_uri = oauth2_redirect_uri
        
    def GenerateAuthUrl(self):
        """
        Generates Fitbit authorization URL
            - You need to access this URL in your browser,
            login your fitbit user and grant required permissions to the application.
        
        Sample auth url: https://www.fitbit.com/oauth2/authorize?
                        response_type=code
                        &client_id=12345A
                        &redirect_uri=http%3A%2F%2Fexample.com%2Ffitbit_auth
                        &scope=activity%20nutrition%20heartrate%20location%20nutrition%20
                        profile%20settings%20sleep%20social%20weight
            
        """
        auth_params = {
            'response_type' : 'code',
            'client_id' : self.client_id,
            'redirect_uri' : self.redirect_uri,
            'scope' : ' '.join(self.APPLICATION_SCOPES)
        }
        urlparams = urllib.urlencode(auth_params)
        return "%s?%s" % (self.FITBIT_AUTH_URL, urlparams)
    
    def GetAccessToken(self, auth_code):
        """
        @param auth_code: Authorization code obtained in 'code' parameter in your redirect_uri
        Gets access token from fitbit's token endpoint
        Used Basic authorization for POST request to the endpoint
            - The Basic authorization value is a base64 encoded string of "<your oauth2 client_key>:<consumer secret>"
        """
        # Forming authorization header
        auth_header = base64.b64encode(self.client_id + ':' + self.client_secret)
        headers = {
            'Authorization': 'Basic %s' % auth_header,
            'Content-Type' : 'application/x-www-form-urlencoded'
        }
        
        # Forming payload
        token_payload = {
            'code' : auth_code,
            'grant_type' : 'authorization_code',
            'client_id' : self.client_id,
            'redirect_uri' : self.redirect_uri
        }
        
        # Sending POST request on fitbit access token endpoint
        token_response = requests.post(url=self.FITBIT_TOKEN_URL, 
                                       data=token_payload,
                                       headers=headers)
        
        # Checking if request failed
        if token_response.status_code != 200:
            raise Exception("Error in getting access token. Error: (%s). Error description: (%s)" \
                            % (token_response['errors'][0]['errorType'], token_response['errors'][0]['message']))
            
        # Returning access token response
        return token_response.json()
    
    def RefreshAccessToken(self, refresh_token):
        """
        Refreshes expired fitbit access token
        """
        # Forming authorization header
        auth_header = base64.b64encode(self.client_id + ':' + self.client_secret)
        headers = {
            'Authorization': 'Basic %s' % auth_header,
            'Content-Type' : 'application/x-www-form-urlencoded'
        }
        
        # Forming payload
        token_payload = {
            'refresh_token' : refresh_token,
            'grant_type' : 'refresh_token'
        }
        
        # Sending POST request on fitbit access token endpoint
        refresh_token_response = requests.post(url=self.FITBIT_TOKEN_URL, 
                                       data=token_payload,
                                       headers=headers)
        
        # Checking if request failed
        if refresh_token_response.status_code != 200:
            raise Exception("Error in getting access token from refresh token. Error: (%s). Error description: (%s)" \
                            % (token_response['errors'][0]['errorType'], token_response['errors'][0]['message']))
            
        # Returning access token response
        return refresh_token_response.json()
    
    def TestFitbitApiCall(self, access_token, endpoint=None):
        """
        Makes a API call with given access token
        """
        # Making authorization header
        headers = {
            "Authorization" : "Bearer " + access_token
        }
        
        if not endpoint:
            endpoint = self.ACTIVITIES_TIMESERIES_URL
        
        # Making API call
        api_response = requests.get(url = endpoint, headers = headers)
        
        # Checking if request failed
        if api_response.status_code != 200:
            raise Exception("Error in API call. Error: (%s). Error description: (%s)" \
                            % (api_response['errors'][0]['errorType'], api_response['errors'][0]['message']))
            
        # Returning result
        return api_response.json()
        