'''
Created on Feb 3, 2017

@author: npvance2
'''
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
import sys
import json
import os.path
from collections import deque

def idLogPath():
    cwd = os.getcwd()
    filePath = cwd+"/twitterStreamMongoIDCheck.txt"
    return filePath

def idCheck(tweetID):
    if os.path.isfile(idLogPath()):
        inputFile = open(idLogPath(), "r")
        fileString = inputFile.read()
        fileString = fileString[:-1]
        log = deque(fileString.split(","), maxlen = 1000)
        if tweetID in log:
            idChecker = False
        else:
            idChecker = True
            log.append(tweetID)
        outputFile = open(idLogPath(), "w")
        for i in log:
            outputFile.write(i+",")
        outputFile.close()
    else:
        idCheckFile = open(idLogPath(), "w")
        idCheckFile.write(tweetID)
        idCheckFile.close()
        idChecker = True
    return idChecker

def mongoDB(data):
    client = MongoClient()
    db = client['twitterSampleStream']
    tweetCol = db['tweets']
    tweet = json.loads(data)
    if ("created_at" in tweet):
        tweetID = tweet["id_str"]
        if idCheck(tweetID):
            tweetCol.insert_one({"_id": tweetID, "tweetInfo": tweet})
            tweetID = tweetID
        else:
            print("Duplicate tweetID: "+tweetID)
        
class StdOutListener(StreamListener):
    #Receives Tweet objects
    def on_data(self, data):
        mongoDB(data)
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
    #This starts a stream to receive 1% of total Tweets in real time from the Twitter API.
    twitterStream().sample()

if __name__ == '__main__':
    main()