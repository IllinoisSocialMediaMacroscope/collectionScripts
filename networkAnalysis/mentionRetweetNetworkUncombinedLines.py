'''
Created on Oct 11, 2016

@author: npvance2
'''
import csv
#This version list a different line for each mention
def main():
    print("Please enter the full path for the file you'd like to analyze.")
    fileName = raw_input(' ')
    outputFileName = os.getcwd()+"/networkAnalysisUncombined.csv"
    with open(fileName, "rU") as f, open(outputFileName, "w") as output:
        lines = csv.DictReader(f)
        output.write("authorAccount,mentionedAccount,postType\n")
        for line in lines:
            if(line['Contents'].startswith("RT")):
                postType = "Retweet"
                words = line['Contents'].split(" ", 3)
                mention = (words[1]).replace(",","")
                author = line['Author'].replace(",","")
                output.write(mention+","+author+","+postType+"\n")
            elif(line['Contents'].startswith("@")):
                postType = "Reply"
                words = line['Contents'].split(" ", 2)
                mention = (words[0]).replace(",","")
                author = line['Author'].replace(",","")
                output.write(mention+","+author+","+postType+"\n")
            elif(line['Contents'].startswith(".@")):
                postType = "Reply"
                words = line['Contents'].split(" ", 2)
                mention = (words[0]).replace(",","")
                author = line['Author'].replace(",","")
                output.write(mention+","+author+","+postType+"\n")
            else:
                postType = "Mention"
                mention = ""
                
    print("Analysis Complete")

if __name__ == '__main__':
    main()