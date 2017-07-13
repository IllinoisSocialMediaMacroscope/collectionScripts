'''
Created on Jun 14, 2017

@author: npvance2
'''
# This program gets Reddit Auth and saves to a text file. 
# You'll need to add your own Reddit Application keys and chose where the file will be written to.

from flask import Flask
from flask import abort, request
from uuid import uuid4
import urllib
import requests
import requests.auth

app = Flask(__name__)
CLIENT_ID = "ENTER YOUR APP KEYS"
CLIENT_SECRET = "ENTER YOUR APP KEYS"
REDIRECT_URI = "http://localhost:65010/reddit_callback"

@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with reddit</a>'
    return text % make_authorization_url()

def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "permanent",
              "scope": "identity"}
    url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
    return url

@app.route('/reddit_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    # We'll change this next line in just a moment
    return get_token(code)

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    try:
        access_token = token_json["access_token"]
    except:
        return token_json["message"]
    if access_token:
        outputFileName = 'CHOOSE OUTPUT LOCATION'
        expiration = token_json["expires_in"]
        refresh_token = token_json["refresh_token"]
        with open(outputFileName, "w") as output:
            output.write(access_token+'\n')
            output.write(str(expiration)+'\n')
            output.write(refresh_token+'\n')
        output.close()
        return access_token

# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
    pass
def is_valid_state(state):
    return True


if __name__ == '__main__':
    app.run(debug=True, port=65010)