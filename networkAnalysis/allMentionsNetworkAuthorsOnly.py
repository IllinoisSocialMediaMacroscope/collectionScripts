'''
Created on Jan 13, 2017

@author: npvance2
'''
import csv
import re
import os
import codecs
#Finds and documents all mentions and who mentioned the account including retweets and replies
def main():
    print("Please enter the full path for the file you'd like to analyze.")
    fileName = raw_input(' ')
    outputFileName = os.getcwd()+"/networkAnalysisColumns.csv"
    with open(fileName, "rU") as f, open(outputFileName, "w") as output:
        lines = csv.DictReader(f)
        output.write("mentionedAccount,authorAccount,postType\n")
        authors = []
        for line in lines:
            authors.append(line['Author'])
        f.seek(0)
        next(lines, None)
        for line in lines:
            if line['Author']:
                mentions = re.findall("@[a-zA-z0-9_]+", line['Contents'])
                count = 0
                for m in mentions:
                    if(count == 0):
                        if(line['Contents'].startswith("RT")):
                            postType = "Retweet"
                        elif(line['Contents'].startswith("@")):
                            postType = "Reply"
                        elif(line['Contents'].startswith(".@")):
                            postType = "Reply"
                        else:
                            postType = "Mention"
                    else:
                        postType = "Mention"
                    if m in authors:
                        author = line['Author']
                        tweetInfo = [m, author, postType]
                        count2 = 1
                        for i in tweetInfo:
                            output.write("\"")
                            output.write(i)
                            if count2 < 3:
                                output.write("\",")
                            else:
                                output.write("\"\n")
                            count2 = count2+1
                    count = count+1
        output.close()
        print("Analysis Complete")

if __name__ == '__main__':
    main()