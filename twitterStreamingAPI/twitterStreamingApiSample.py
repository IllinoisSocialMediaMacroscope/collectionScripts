'''
Created on Jan 8, 2017

@author: npvance2
'''
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import codecs
import os
import sys

def filePath():
    cwd = os.getcwd()
    filePath = cwd+"/TwitterStreamingAPIResults.csv"
    return filePath

def tweetParser(data):
    #Reads Tweet JSON and pulls the parts
    outputFile = codecs.open(filePath(), "a", "utf-8")
    data = data.decode('utf8')
    theJSON = json.loads(data)
    #Some returned objects are tweet delete requests, this skips those as "created_at" is only in new post objects
    if ("created_at" in theJSON):
        date_time = theJSON["created_at"]
        if not date_time:
            date_time = ""
        tweetID = theJSON["id_str"]
        if not tweetID:
            tweetID = ""
        contents = theJSON["text"]
        if not contents:
            contents = ""
        author = theJSON["user"]["screen_name"]
        if not author:
            author = ""
        display_name = theJSON["user"]["name"]
        if not display_name:
            display_name = ""
        profile_location = theJSON["user"]["location"]
        if not profile_location:
            profile_location = ""
        tweetInfo = [tweetID, date_time, author, display_name, contents, profile_location]
        count2 = 1
        for i in tweetInfo:
            outputFile.write("\"")
            outputFile.write(i)
            if count2 < 6:
                outputFile.write("\",")
            else:
                outputFile.write("\"\n")
            count2 = count2+1
        outputFile.close()
        
class StdOutListener(StreamListener):
    #Receives Tweet objects
    def on_data(self, data):
        tweetParser(data)
        return True

    def on_error(self, status):
        print status

def twitterStream():
    #Establishes authenticated connection
    #Enter your Twitter keys below
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_secret = ''
    if (consumer_key == '') or (consumer_secret =='') or (access_token =='') or (access_secret ==''):
        print("Not all Twitter keys have been entered, please add them to the script and try again")
        sys.exit(0)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, StdOutListener())
    return stream


def main():
    outputFile = codecs.open(filePath(), "a", "utf-8")
    outputFile.write("tweetID,date_time,author,display_name,contents,profile_location\n")
    outputFile.close()
    #This starts a stream to receive 1% of total Tweets in real time from the Twitter API.
    twitterStream().sample()

if __name__ == '__main__':
    main()