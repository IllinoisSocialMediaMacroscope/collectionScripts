'''
Created on Feb 21, 2017

@author: npvance2
'''
from __future__ import unicode_literals
import urllib2
import json
import codecs
import tweepy
from tweepy import OAuthHandler

def getURL(): #provides URL for Crimson API
    urlStart = "https://api.crimsonhexagon.com/api"
    return urlStart

def getAuthToken(): #provides auth token needed to access Crimson API
    authToken = "&auth=AuthTokenHere"
    return authToken

def getTwitterURL(): #provides URL for Twitter api
    urlStart = "https://api.twitter.com/1.1/statuses/lookup.json?id="
    return urlStart

def twitterAPI(): #Provides access keys for Twitter API, Find info on getting those keys here https://tweepy.readthedocs.io/en/v3.5.0/auth_tutorial.html#auth-tutorial
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_secret = ''
    if (consumer_key == '') or (consumer_secret =='') or (access_token =='') or (access_secret ==''):
        print("Not all Twitter keys have been entered, please add them to the script and try again")
        sys.exit(0)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api
    
def main():
    monitorID = "" #The ID for your monitor
    print("MonitorID is"+monitorID)
    print("If not monitorID is listed you will need to add it to the program before proceeding")
    print("Enter the date you'd like the data to start on")
    print("The date must be in the format YYYY-MM-DD.")
    startDate = raw_input(" ") #If you prefer you can remove these prompts and make them constant but these are needed for the API call.
    print("Enter the date you'd like the data to end on")
    print("The date must be in the format YYYY-MM-DD.")
    endDate = raw_input(' ')
    dates = "&start="+startDate+"&end="+endDate #Combines start and end date into format needed for API call
    urlStart = getURL() #Gets URL
    authToken = getAuthToken() #Gets auth token
    endpoint = "/monitor/posts?id="; #endpoint needed for this query
    extendLimit = "&extendLimit=true" #extends call number from 500 to 10,000
    fullContents = "&fullContents=true" #Brings back full contents for Blog and Tumblr posts which are usually truncated around search keywords. This can occasionally disrupt CSV formatting.
    urlData = urlStart+endpoint+monitorID+authToken+dates+extendLimit+fullContents #Combines all API calls parts into full URL
    print("This query may take a few mins to complete.")
    print("Connecting to "+urlData+"...")
    webURL = urllib2.urlopen(urlData)
    fPath = ""+monitorID+"PostList"+startDate+"&"+endDate+".csv" #names output file, this can be changed if user wants.
    if (webURL.getcode() == 200):
        print("Connected")
        print("This query returns information in a CSV file.")
        print("Fields with commas had them removed to simplify formatting")
        print("If the conversation you are querying has over 10,000 posts, you will be given a random sample from the total conversation that includes no more 10,000 posts.")
        print("To download all posts break your timeframe up into groups of less than 10,000 posts.")
        print("Instagram mentions in this list will not contain the post contents")
        csvFile = codecs.open(fPath, "w+", "utf-8")
        csvFile.write("postType,postDate,postTime,url,tweetID,contents,retweetCount,favoriteCount,location,language,sentiment,neutralScore,positiveScore,negativeScore,followers,friends,author,authorGender,authorTweets\n")
        data = webURL.read().decode('utf8')
        theJSON = json.loads(data)
        postDates = [] #These initialize the attributes of the final output
        postTimes = []
        urls = []
        contents = []
        authors = []
        authorGenders = []
        locations = []
        languages = []
        postTypes = []
        sentiments = []
        neutralScore = []
        positiveScore = []
        negativeScore = []
        tweetIDs = []
        followers = []
        friends = []
        retweetCounts = []
        favoritesCount = []
        statusesCount = []
        tweetCount = 0
        tempTweetIDs = []
        api = twitterAPI()
        c = 0
        for i in theJSON["posts"]:
            postDates.append("")
            postTimes.append("")
            if ('date' in i): #identifies date posted
                tempDate = str(i["date"])
                dateTime = tempDate.split("T")
                postDates[c] = dateTime[0]
                postTimes[c] = dateTime[1]
            urls.append(i["url"])
            contents.append("")
            if ('contents' in i): #identifies post contents
                contents[c] = i["contents"].replace(",","").replace("\n"," ") #replaces commas and new lines to facilitate CSV formatting, this occasionally missed new lines in some blog posts which I'm working to fix
            authors.append("")
            if ('author' in i): #identifies author
                authors[c] = i["author"].replace(",","")
            authorGenders.append("")
            if ('authorGender' in i): #identifies author gender
                authorGenders[c] = i["authorGender"]
            locations.append("")
            if ('location' in i): #identifies location
                locations[c] = i["location"].replace(",","")
            languages.append("")
            if ('language' in i): #identifies language specified in the author's profile
                languages[c] = i["language"]
            postTypes.append(i["type"]) #identifies the type of post, i.e. Twitter, Tumblr, Blog
            tweetIDs.append("")
            followers.append("")
            friends.append("")
            retweetCounts.append("")
            favoritesCount.append("")
            statusesCount.append("")
            if postTypes[c] == "Twitter": #if the post type is Twitter it goes through more processing
                tweetCount = tweetCount + 1 #counts number of tweets
                tweetSplit = urls[c].split("status/") #splits URL to get tweetID
                tweetIDs[c] = tweetSplit[1]
                tempTweetIDs.append(tweetIDs[c])
                if tweetCount == 100: #the max number of TweetIDs in one API call is 100 so a call is run every 100 tweets identified
                    tweepys = api.statuses_lookup(id_=tempTweetIDs) #call to Twitter API
                    for tweet in tweepys:
                        tempID = tweet.id_str #finds tweetsID
                        postMatch = 0
                        for idMatch in tweetIDs:
                            if idMatch==tempID: #matches tweetID in Twitter API call to tweetID stored from Crimson API
                                tempDate = str(tweet.created_at).replace("  "," ") #These all fill the matching Crimson attributes to those found in the Twitter API
                                dateTime = tempDate.split(" ")
                                postDates[postMatch] = dateTime[0]
                                postTimes[postMatch] = dateTime[1]
                                contents[postMatch] = tweet.text.replace(",","")
                                authors[postMatch] = tweet.author.screen_name
                                followers[postMatch] = str(tweet.author.followers_count)
                                friends[postMatch] = str(tweet.author.friends_count)
                                retweetCounts[postMatch] = str(tweet.retweet_count)
                                favoritesCount[postMatch] = str(tweet.favorite_count)
                                statusesCount[postMatch] = str(tweet.author.statuses_count)
                            postMatch = postMatch + 1
                    tweetCount = 0 #clears tweet count for a new 100
                    tempTweetIDs = [] #clears tweetIDs for next call
            sentiments.append("")
            neutralScore.append("")
            positiveScore.append("")
            negativeScore.append("")
            if ('categoryScores' in i): #finds sentiment value and matching attribute
                for l in i["categoryScores"]:
                    catName = l["categoryName"]
                    if catName == "Basic Neutral":
                        neutralScore[c] = l["score"]
                    elif catName =="Basic Positive":
                        positiveScore[c] = l["score"]
                    elif catName == "Basic Negative":
                        negativeScore[c] = l["score"]
            if neutralScore[c] > positiveScore[c] and neutralScore[c] > negativeScore[c]:
                sentiments[c] = "Basic Neutral"
            if positiveScore[c] > neutralScore[c] and positiveScore[c] > negativeScore[c]:
                sentiments[c] = "Basic Positive"
            if negativeScore[c] > positiveScore[c] and negativeScore[c] > neutralScore[c]:
                sentiments[c] = "Basic Negative"
            c = c + 1
        pC = 0
        tweepys = api.statuses_lookup(id_=tempTweetIDs) #after loop the Twitter API call must run one more time to clean up all the tweets since the last 100
        for tweet in tweepys:
            tempID = tweet.id_str
            postMatch = 0
            for idMatch in tweetIDs:
                if idMatch==tempID:
                    tempDate = str(tweet.created_at).replace("  "," ")
                    dateTime = tempDate.split(" ")
                    postDates[postMatch] = dateTime[0]
                    postTimes[postMatch] = dateTime[1]
                    contents[postMatch] = tweet.text.replace(",","")
                    authors[postMatch] = tweet.author.screen_name
                    followers[postMatch] = str(tweet.author.followers_count)
                    friends[postMatch] = str(tweet.author.friends_count)
                    retweetCounts[postMatch] = str(tweet.retweet_count)
                    favoritesCount[postMatch] = str(tweet.favorite_count)
                    statusesCount[postMatch] = str(tweet.author.statuses_count)
                postMatch = postMatch + 1
        tweetCount = 0
        for pDate in postDates: #iterates through the word lists and prints matching posts to CSV
            csvFile.write(postTypes[pC]+","+pDate+","+postTimes[pC]+","+urls[pC]+","+str(tweetIDs[pC])+","+contents[pC].replace("\n"," ")+","+retweetCounts[pC]+","+favoritesCount[pC]+","+locations[pC]+","+languages[pC]+","+sentiments[pC]+","+str(neutralScore[pC])+","+str(positiveScore[pC])+","+str(negativeScore[pC])+","+followers[pC]+","+friends[pC]+","+authors[pC]+","+authorGenders[pC]+","+statusesCount[pC]+"\n")
            pC = pC + 1
        print("File printed as "+fPath)
        csvFile.close()
    else:
        print("Server Error, No Data" + str(webURL.getcode())) #displays error if Crimson URL fails
        
if __name__ == '__main__':
    main()