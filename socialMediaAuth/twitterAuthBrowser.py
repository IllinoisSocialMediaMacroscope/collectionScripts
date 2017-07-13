'''
Created on Jun 13, 2017

@author: npvance2
'''
#This program gets Twitter Auth and saves to a text file. 
#You'll need to add your own Twitter Application keys and chose where the file will be written to.

from flask import Flask, request, redirect, url_for, session, g, flash, \
     render_template
from flask_oauth import OAuth
 
# configuration
SECRET_KEY = 'development key'
DEBUG = True
 
# setup flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()
 
# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authenticate',
    # the consumer keys from the twitter application registry.
    consumer_key='ENTER YOUR APP KEYS',
    consumer_secret='ENTER YOUR APP KEYS'
)
 
 
@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))
 
@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))
 
 
@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
 
    access_token = resp['oauth_token']
    access_secret = resp['oauth_token_secret']
    screen_name = resp['screen_name']
    session['access_token'] = access_token
    session['screen_name'] = screen_name
    outputFileName = 'ENTER FILE PATH'+screen_name+'.txt'
    with open(outputFileName, "w") as output:
        output.write(screen_name+'\n')
        output.write(access_token+'\n')
        output.write(access_secret+'\n')
    output.close()
 
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
 
 
    return redirect(url_for('index'))
 
 
if __name__ == '__main__':
    app.run()