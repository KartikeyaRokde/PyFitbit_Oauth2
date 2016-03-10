# Python Fitbit OAuth 2.0

This library is for testing Fitbit's OAuth 2.0 flow.

It is made from reference to Fitbit's OAuth 2.0 documentation:-

[Fitbit OAuth 2.0] (https://dev.fitbit.com/docs/oauth2/)


## Installation
 * Download the source code & extract it in your folder
 * OR just clone this repository:
   ```
   $ git clone https://github.com/KartikeyaRokde/PyFitbit_Oauth2.git
   ```
* Install by running the `setup.py` in your virtual environment
  ```
  $ python setup.py install
  ```

* DEPENDENCIES: python-requests
  ```
  $ pip install requests
  ```
## Testing Fitbit's OAuth 2.0 flow

You'll need to collect information from your registered Fitbit application.
You need the following data: You can get it from (https://dev.fitbit.com/) > MANAGE MY APPS
* Fitbit OAuth 2.0 `client_id`
* Consumer Secret `consumer_secret`
* OAuth 2.0 `redirect_uri`. (Redirect URI is mandatory in OAuth 2.0 flow)

### STEP 1:

Authorize application to access Fitbit's data. You need to get authorization URL where you can get authorization from Fitbit user.

```python
import json
from PyFitbit_Oauth2 import PyFitbit_Oauth2

client_id = "Your Fitbit OAuth 2.0 client_id"
client_secret = "Your application's consumer secret"
redirect_uri = "Your Oauth 2.0 redirect_uri"

# Initializing Fitbit OAuth2
fitbit_oauth2 = PyFitbit_Oauth2.PyFitbit_Oauth2(client_id,client_secret,redirect_uri)

# Generate Fitbit authorization URL
authorization_url = fitbit_oauth2.GenerateAuthUrl()
print authorization_url
```

Sample authorization url:
```
https://www.fitbit.com/oauth2/authorize?scope=activity+heartrate+location+nutrition+profile+settings+sleep+social+weight&redirect_uri=https%3A%2F%2Fyoursite.com&response_type=code&client_id=123XYZ
```
Copy this URL & paste in your broswer. You'll see Fitbit's login page. Enter Fitbit user credentials and grant access to the application to access data.


You'll be redirected to your specified *redirect_uri*, you'll get the authorization code as **code** parameter in your redirect uri. Copy this code and go to STEP 2.

NOTE: This code is valid only for 10 minutes

## STEP 2:

Get access token from given authorization code

```python
# Getting access token
access_token_response = fitbit_oauth2.GetAccessToken("Authorization code obtained from STEP 1")
print json.dumps(access_token_response)
```

You'll get the access token response as below:
```javascript
{
    "user_id": "USERID", 
    "access_token": "LONG ACCESS TOKEN .eyJleHAiOjE0NTc1MTkxNDIsInNjb3BlcyI6Indsb2Mgd3BybyB3bnV0IHdzZXQgd3NsZSB3d2VpIHdociB3YWN0IHdzb2MiLCJzdWIiOiIyWkdKSjQiLCJhdWQiOiIyMjlKVloiLCJpc3MiOiJxxxxx VERY LONG ACCESS TOKEN", 
    "expires_in": 3600, 
    "token_type": "Bearer", 
    "scope": "heartrate profile location activity weight sleep nutrition settings social", 
    "refresh_token": "SHORT REFRESH TOKEN fb34914e866d4d14438ed2e0741fd52c3f89fxxxxxxx"
    }
```

## STEP 3:

Testing API call on fitbit

```python
# Accessing Fitbit activities data
api_response = fitbit_oauth2.TestFitbitApiCall(access_token=access_token_response['access_token'],                       endpoint="https://api.fitbit.com/1/user/-/activities/log/steps/date/today/1d.json")

print json.dumps(api_response)
```

This will print a response something like this:
```javascript
{"activities-log-steps": [{"value": "108", "dateTime": "2016-03-09"}]}
```

## Refreshing access token

You can refresh a access token. You may need it when your access token is expired

```python
# Getting refresh token
refresh_token = fitbit_oauth2.RefreshAccessToken(access_token_response['refresh_token'])

print json.dumps(refresh_token)
```

You'll get a new access token
```javascript
{
    "user_id": "USERID", 
    "access_token": "NEW LONG ACCESS TOKEN", 
    "expires_in": 3600, 
    "token_type": "Bearer", 
    "scope": "heartrate profile location activity weight sleep nutrition settings social", 
    "refresh_token": "NEW SHORT REFRESH TOKEN"
    }
```
