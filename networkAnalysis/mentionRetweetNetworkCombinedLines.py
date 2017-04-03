'''
Created on Oct 11, 2016

@author: npvance2
'''
import csv
#This version combines all the authors who mentioned a specific account into one line
def main():
    print("Please enter the full path for the file you'd like to analyze.")
    fileName = raw_input(' ')
    outputFileName = os.getcwd()+"/networkAnalysisCombined.csv"
    with open(fileName, "rU") as f, open(outputFileName, "w") as output:
        lines = csv.DictReader(f)
        network = {}
        mentionCount = {}
        for line in lines:
            if(line['Contents'].startswith("RT")):
                postType = "Retweet"
                words = line['Contents'].split(" ", 3)
                mention = (words[1]+","+postType+",")
                if network.has_key(mention):
                    current = network[mention]
                    authors = current+","+line['Author']
                    network[mention] = authors
                    currentCount = mentionCount[mention]
                    currentCount = currentCount + 1
                    mentionCount[mention] = currentCount
                else:
                    tempNetwork = {mention: line['Author']}
                    network.update(tempNetwork)
                    tempMentionCount = {mention: 1}
                    mentionCount.update(tempMentionCount)
            elif(line['Contents'].startswith("@")):
                postType = "Reply"
                words = line['Contents'].split(" ", 2)
                mention = (words[0]+","+postType+",")
                if network.has_key(mention):
                    current = network[mention]
                    authors = current+","+line['Author']
                    network[mention] = authors
                    currentCount = mentionCount[mention]
                    currentCount = currentCount + 1
                    mentionCount[mention] = currentCount
                else:
                    tempNetwork = {mention: line['Author']}
                    network.update(tempNetwork)
                    tempMentionCount = {mention: 1}
            elif(line['Contents'].startswith(".@")):
                postType = "Reply"
                words = line['Contents'].split(" ", 2)
                mention = (words[0]+","+postType+",")
                if network.has_key(mention):
                    current = network[mention]
                    authors = current+","+line['Author']
                    network[mention] = authors
                    currentCount = mentionCount[mention]
                    currentCount = currentCount + 1
                    mentionCount[mention] = currentCount
                else:
                    tempNetwork = {mention: line['Author']}
                    network.update(tempNetwork)
                    tempMentionCount = {mention: 1}
            else:
                postType = "Mention"
                mention = ""
        output.write("mentionedAccount,postType,count,authorAccounts\n")
        for i in network:
            mention = i
            author = network[i]
            count = mentionCount[i]
            output.write(mention.replace(",","")+count+author.replace(",","")+"\n")
            

if __name__ == '__main__':
    main()